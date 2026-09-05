#!/usr/bin/env python3
"""Validate the repository's structured evidence graph.

The JSON Schemas protect each record in isolation.  This script adds the
repository-level invariants that JSON Schema cannot express: stable IDs,
filename/ID agreement, ledger identities, and references between records.
"""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Mapping, Sequence

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError


@dataclass(frozen=True)
class RecordGroup:
    name: str
    directory: str
    schema: str
    id_prefix: str
    ledger: str
    ledger_id_column: str

    @property
    def id_pattern(self) -> re.Pattern[str]:
        return re.compile(rf"{self.id_prefix}-[0-9]{{4,}}")


GROUPS: tuple[RecordGroup, ...] = (
    RecordGroup(
        "artifact",
        "records/artifacts",
        "schema/artifact-record.schema.json",
        "ART",
        "data/artifact-ledger.csv",
        "artifact_id",
    ),
    RecordGroup(
        "source",
        "records/sources",
        "schema/source-record.schema.json",
        "SRC",
        "data/source-ledger.csv",
        "source_id",
    ),
    RecordGroup(
        "lineage",
        "records/lineages",
        "schema/lineage-edge.schema.json",
        "LIN",
        "data/lineage-ledger.csv",
        "lineage_id",
    ),
)

GROUP_BY_NAME = {group.name: group for group in GROUPS}
SOURCE_ID_TOKEN = re.compile(r"\bSRC-[0-9]{4,}\b")
LEDGER_REFERENCE_COLUMNS: Mapping[str, Mapping[str, str]] = {
    "lineage": {
        "from_artifact_id": "artifact",
        "to_artifact_id": "artifact",
    },
}


@dataclass(frozen=True)
class LoadedRecord:
    group: str
    path: Path
    document: dict[str, object]


@dataclass(frozen=True)
class Reference:
    target_group: str
    target_id: str
    json_path: str


@dataclass(frozen=True)
class LedgerReference:
    target_group: str
    target_id: str
    path: Path
    line_number: int
    column: str


@dataclass
class ValidationReport:
    errors: list[str]
    record_counts: dict[str, int]
    ledger_counts: dict[str, int]

    @property
    def total_records(self) -> int:
        return sum(self.record_counts.values())


class StrictJSONError(ValueError):
    """Raised when Python's permissive JSON decoder accepts invalid JSON."""


def display_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def reject_duplicate_keys(
    pairs: list[tuple[str, object]],
) -> dict[str, object]:
    document: dict[str, object] = {}
    for key, value in pairs:
        if key in document:
            raise StrictJSONError(f"duplicate object key {key!r}")
        document[key] = value
    return document


def reject_non_finite_number(value: str) -> object:
    raise StrictJSONError(f"non-finite number {value!r}")


def resolve_repository_path(
    path: Path,
    root: Path,
    errors: list[str],
    *,
    expected: str,
) -> Path | None:
    """Resolve a repository input without allowing it to escape ``root``."""

    label = display_path(path, root)
    try:
        resolved = path.resolve(strict=True)
    except (OSError, RuntimeError) as error:
        errors.append(f"{label}: cannot resolve path: {error}")
        return None

    try:
        resolved.relative_to(root)
    except ValueError:
        errors.append(f"{label}: resolves outside repository root")
        return None

    if expected == "file" and not resolved.is_file():
        errors.append(f"{label}: expected a regular file")
        return None
    if expected == "directory" and not resolved.is_dir():
        errors.append(f"{label}: expected a directory")
        return None
    if expected == "entry" and not (resolved.is_file() or resolved.is_dir()):
        errors.append(f"{label}: expected a regular file or directory")
        return None
    return resolved


def json_path(parts: Sequence[object]) -> str:
    rendered = "$"
    for part in parts:
        if isinstance(part, int):
            rendered += f"[{part}]"
        else:
            rendered += f".{part}"
    return rendered


def schema_error_sort_key(error: object) -> tuple[tuple[tuple[int, object], ...], str]:
    """Return a key that remains comparable when paths mix keys and indexes."""

    absolute_path = getattr(error, "absolute_path")
    message = getattr(error, "message")
    path_key = tuple(
        (0, part) if isinstance(part, int) else (1, str(part))
        for part in absolute_path
    )
    return path_key, message


def load_json_object(
    path: Path,
    root: Path,
    errors: list[str],
    *,
    label_path: Path | None = None,
) -> dict[str, object] | None:
    label = display_path(label_path or path, root)
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_non_finite_number,
        )
    except (OSError, UnicodeError) as error:
        errors.append(f"{label}: cannot read UTF-8 JSON: {error}")
        return None
    except json.JSONDecodeError as error:
        errors.append(
            f"{label}:{error.lineno}:{error.colno}: invalid JSON: {error.msg}"
        )
        return None
    except StrictJSONError as error:
        errors.append(f"{label}: invalid JSON: {error}")
        return None

    if not isinstance(value, dict):
        errors.append(f"{label}: expected a JSON object at the document root")
        return None
    return value


def load_schema(
    path: Path,
    root: Path,
    errors: list[str],
    *,
    label_path: Path | None = None,
) -> dict[str, object] | None:
    display = label_path or path
    schema = load_json_object(path, root, errors, label_path=display)
    if schema is None:
        return None
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as error:
        errors.append(
            f"{display_path(display, root)}:{json_path(list(error.absolute_path))}: "
            f"invalid JSON Schema: {error.message}"
        )
        return None
    return schema


def discover_record_paths(
    root: Path, errors: list[str]
) -> dict[str, list[tuple[Path, Path]]]:
    """Find the complete, canonical set of structured record files.

    JSON-shaped files are only valid directly inside one of the registered
    group directories.  Walking explicitly also makes hidden nested records,
    unknown categories, and case-variant extensions fail closed.
    """

    discovered: dict[str, list[tuple[Path, Path]]] = {
        group.name: [] for group in GROUPS
    }
    records_path = root / "records"
    resolved_records = resolve_repository_path(
        records_path, root, errors, expected="directory"
    )
    if resolved_records is None:
        return discovered

    categories = {
        Path(group.directory).relative_to("records").as_posix(): group.name
        for group in GROUPS
    }
    pending = [(records_path, resolved_records)]
    visited_directories = {resolved_records}

    while pending:
        lexical_directory, _ = pending.pop()
        try:
            entries = sorted(lexical_directory.iterdir(), key=lambda path: path.name)
        except OSError as error:
            errors.append(
                f"{display_path(lexical_directory, root)}: "
                f"cannot read record directory: {error}"
            )
            continue

        for path in entries:
            resolved = resolve_repository_path(
                path, root, errors, expected="entry"
            )
            if resolved is None:
                continue
            if resolved.is_dir():
                if resolved in visited_directories:
                    errors.append(
                        f"{display_path(path, root)}: record directory resolves "
                        "to an already visited directory"
                    )
                    continue
                visited_directories.add(resolved)
                pending.append((path, resolved))
                continue

            if path.suffix.casefold() != ".json":
                continue

            relative = path.relative_to(records_path)
            if path.suffix != ".json":
                errors.append(
                    f"{display_path(path, root)}: JSON record extension must be .json"
                )
            if len(relative.parts) != 2:
                errors.append(
                    f"{display_path(path, root)}: JSON records must be directly "
                    "inside a registered record directory"
                )
                continue

            group_name = categories.get(relative.parts[0])
            if group_name is None:
                errors.append(
                    f"{display_path(path, root)}: unregistered record directory "
                    f"{relative.parts[0]!r}"
                )
                continue
            if path.suffix == ".json":
                discovered[group_name].append((path, resolved))

    for paths in discovered.values():
        paths.sort(key=lambda pair: pair[0].as_posix())
    return discovered


def load_ledger_ids(
    root: Path,
    group: RecordGroup,
    errors: list[str],
    *,
    references: list[LedgerReference] | None = None,
) -> set[str]:
    label_path = root / group.ledger
    label = display_path(label_path, root)
    ids: set[str] = set()
    path = resolve_repository_path(
        label_path, root, errors, expected="file"
    )
    if path is None:
        return ids
    try:
        handle = path.open(encoding="utf-8-sig", newline="")
    except OSError as error:
        errors.append(f"{label}: cannot read ledger: {error}")
        return ids

    with handle:
        reader = csv.reader(handle, strict=True)
        try:
            fieldnames = next(reader, None)
            if fieldnames is None:
                errors.append(
                    f"{label}: missing required column {group.ledger_id_column!r}"
                )
                return ids
            blank_column_positions = [
                position
                for position, column in enumerate(fieldnames, start=1)
                if column is None or not column.strip()
            ]
            if blank_column_positions:
                rendered = ", ".join(map(str, blank_column_positions))
                errors.append(
                    f"{label}: blank ledger column name(s) at position(s): {rendered}"
                )
                return ids
            duplicate_columns = sorted(
                (
                    column
                    for column, count in Counter(fieldnames).items()
                    if count > 1
                ),
                key=repr,
            )
            if duplicate_columns:
                rendered = ", ".join(repr(column) for column in duplicate_columns)
                errors.append(f"{label}: duplicate ledger column(s): {rendered}")
                return ids
            if group.ledger_id_column not in fieldnames:
                errors.append(
                    f"{label}: missing required column {group.ledger_id_column!r}"
                )
                return ids
            expected_field_count = len(fieldnames)
            id_column_index = fieldnames.index(group.ledger_id_column)
            reference_columns = [
                (fieldnames.index(column), column, target_group)
                for column, target_group in LEDGER_REFERENCE_COLUMNS.get(
                    group.name, {}
                ).items()
                if column in fieldnames
            ]
            for row in reader:
                line_number = reader.line_num
                if not row:
                    continue
                if len(row) != expected_field_count:
                    errors.append(
                        f"{label}:{line_number}: malformed CSV row has "
                        f"{len(row)} fields; expected {expected_field_count}"
                    )
                    continue
                record_id = row[id_column_index].strip()
                if not group.id_pattern.fullmatch(record_id):
                    errors.append(
                        f"{label}:{line_number}: invalid {group.ledger_id_column} "
                        f"{record_id!r}; expected {group.id_prefix}- followed by at least four digits"
                    )
                    continue
                if record_id in ids:
                    errors.append(f"{label}:{line_number}: duplicate ledger ID {record_id}")
                    continue
                ids.add(record_id)
                if references is not None:
                    for index, column, target_group in reference_columns:
                        target_id = row[index].strip()
                        if target_id:
                            references.append(
                                LedgerReference(
                                    target_group,
                                    target_id,
                                    label_path,
                                    line_number,
                                    column,
                                )
                            )
        except csv.Error as error:
            errors.append(f"{label}:{reader.line_num}: invalid CSV: {error}")
    return ids


def strings(value: object) -> Iterator[tuple[int, str]]:
    if not isinstance(value, list):
        return
    for index, item in enumerate(value):
        if isinstance(item, str):
            yield index, item


def iter_references(group: str, document: Mapping[str, object]) -> Iterator[Reference]:
    """Yield typed ID references from one record, with their JSON paths."""

    if group == "artifact":
        parent_family = document.get("parent_family")
        if isinstance(parent_family, str) and GROUP_BY_NAME["artifact"].id_pattern.fullmatch(
            parent_family
        ):
            yield Reference("artifact", parent_family, "$.parent_family")

        chronology = document.get("chronology")
        if isinstance(chronology, dict):
            for milestone, claim in chronology.items():
                if not isinstance(claim, dict):
                    continue
                for index, source_id in strings(claim.get("source_ids")):
                    yield Reference(
                        "source",
                        source_id,
                        f"$.chronology.{milestone}.source_ids[{index}]",
                    )

        sources = document.get("sources")
        if isinstance(sources, list):
            for index, claim in enumerate(sources):
                if isinstance(claim, dict) and isinstance(claim.get("source_id"), str):
                    yield Reference(
                        "source", claim["source_id"], f"$.sources[{index}].source_id"
                    )

        related = document.get("related_artifacts")
        if isinstance(related, list):
            for index, relation in enumerate(related):
                if isinstance(relation, dict) and isinstance(relation.get("id"), str):
                    yield Reference(
                        "artifact", relation["id"], f"$.related_artifacts[{index}].id"
                    )

    elif group == "source":
        for index, artifact_id in strings(document.get("artifact_ids")):
            yield Reference("artifact", artifact_id, f"$.artifact_ids[{index}]")

        claims = document.get("claims_extracted")
        if isinstance(claims, list):
            for claim_index, claim in enumerate(claims):
                if not isinstance(claim, dict):
                    continue
                for artifact_index, artifact_id in strings(claim.get("artifact_ids")):
                    yield Reference(
                        "artifact",
                        artifact_id,
                        f"$.claims_extracted[{claim_index}].artifact_ids[{artifact_index}]",
                    )

    elif group == "lineage":
        for endpoint_name in ("from", "to"):
            endpoint = document.get(endpoint_name)
            if isinstance(endpoint, dict) and isinstance(endpoint.get("artifact_id"), str):
                yield Reference(
                    "artifact", endpoint["artifact_id"], f"$.{endpoint_name}.artifact_id"
                )

        sources = document.get("sources")
        if isinstance(sources, list):
            for index, claim in enumerate(sources):
                if not isinstance(claim, dict) or not isinstance(
                    claim.get("source_ref"), str
                ):
                    continue
                for source_id in SOURCE_ID_TOKEN.findall(claim["source_ref"]):
                    yield Reference(
                        "source", source_id, f"$.sources[{index}].source_ref"
                    )


def validate_references(
    records: Sequence[LoadedRecord], known_ids: Mapping[str, set[str]], root: Path
) -> list[str]:
    errors: list[str] = []
    for record in records:
        for reference in iter_references(record.group, record.document):
            if reference.target_id not in known_ids[reference.target_group]:
                errors.append(
                    f"{display_path(record.path, root)}:{reference.json_path}: "
                    f"unknown {reference.target_group} ID {reference.target_id}"
                )
    return errors


def validate_parent_family_cycles(
    records: Sequence[LoadedRecord], root: Path
) -> list[str]:
    """Reject cycles among artifact-ID ``parent_family`` references."""

    artifact_pattern = GROUP_BY_NAME["artifact"].id_pattern
    parents: dict[str, str] = {}
    paths: dict[str, Path] = {}
    for record in records:
        if record.group != "artifact":
            continue
        artifact_id = record.document.get("id")
        parent_family = record.document.get("parent_family")
        if not (
            isinstance(artifact_id, str)
            and artifact_pattern.fullmatch(artifact_id)
            and isinstance(parent_family, str)
            and artifact_pattern.fullmatch(parent_family)
        ):
            continue
        # Duplicate IDs are reported separately. Keep the first canonical path
        # so cycle diagnostics remain stable even in an already-invalid corpus.
        parents.setdefault(artifact_id, parent_family)
        paths.setdefault(artifact_id, record.path)

    errors: list[str] = []
    completed: set[str] = set()
    for start in sorted(parents):
        if start in completed:
            continue
        trail: list[str] = []
        positions: dict[str, int] = {}
        current = start
        while current in parents and current not in completed:
            if current in positions:
                cycle = trail[positions[current] :]
                anchor = min(cycle)
                anchor_index = cycle.index(anchor)
                cycle = cycle[anchor_index:] + cycle[:anchor_index]
                rendered_cycle = " -> ".join([*cycle, anchor])
                errors.append(
                    f"{display_path(paths[anchor], root)}:$.parent_family: "
                    f"parent_family cycle detected: {rendered_cycle}"
                )
                break
            positions[current] = len(trail)
            trail.append(current)
            current = parents[current]
        completed.update(trail)
    return errors


def validate_ledger_references(
    references: Sequence[LedgerReference],
    known_ids: Mapping[str, set[str]],
    root: Path,
) -> list[str]:
    errors: list[str] = []
    for reference in references:
        label = (
            f"{display_path(reference.path, root)}:{reference.line_number}:"
            f"{reference.column}"
        )
        target_group = GROUP_BY_NAME[reference.target_group]
        if not target_group.id_pattern.fullmatch(reference.target_id):
            errors.append(
                f"{label}: invalid {target_group.name} ID {reference.target_id!r}; "
                f"expected {target_group.id_prefix}- followed by at least four digits"
            )
            continue
        if reference.target_id not in known_ids[reference.target_group]:
            errors.append(
                f"{label}: unknown {target_group.name} ID {reference.target_id}"
            )
    return errors


def validate_repository(root: Path) -> ValidationReport:
    errors: list[str] = []
    record_counts = {group.name: 0 for group in GROUPS}
    ledger_counts = {group.name: 0 for group in GROUPS}
    try:
        root = root.resolve(strict=True)
    except (OSError, RuntimeError) as error:
        errors.append(f"repository root: cannot resolve path: {error}")
        return ValidationReport(errors, record_counts, ledger_counts)
    if not root.is_dir():
        errors.append("repository root: expected a directory")
        return ValidationReport(errors, record_counts, ledger_counts)

    records: list[LoadedRecord] = []
    structured_ids: dict[str, set[str]] = {group.name: set() for group in GROUPS}
    ledger_ids: dict[str, set[str]] = {group.name: set() for group in GROUPS}
    ledger_references: list[LedgerReference] = []
    seen_structured_ids: dict[str, Path] = {}
    discovered_paths = discover_record_paths(root, errors)

    for group in GROUPS:
        schema_label_path = root / group.schema
        schema_path = resolve_repository_path(
            schema_label_path, root, errors, expected="file"
        )
        schema = (
            load_schema(
                schema_path,
                root,
                errors,
                label_path=schema_label_path,
            )
            if schema_path is not None
            else None
        )
        validator = (
            Draft202012Validator(schema, format_checker=FormatChecker())
            if schema is not None
            else None
        )

        record_directory = root / group.directory
        resolved_directory = resolve_repository_path(
            record_directory, root, errors, expected="directory"
        )
        paths = discovered_paths[group.name] if resolved_directory is not None else []

        for path, resolved_path in paths:
            document = load_json_object(
                resolved_path, root, errors, label_path=path
            )
            if document is None:
                continue
            record_counts[group.name] += 1
            records.append(LoadedRecord(group.name, path, document))

            if validator is not None:
                schema_errors = sorted(
                    validator.iter_errors(document),
                    key=schema_error_sort_key,
                )
                for error in schema_errors:
                    errors.append(
                        f"{display_path(path, root)}:{json_path(list(error.absolute_path))}: "
                        f"{error.message}"
                    )

            record_id = document.get("id")
            if not isinstance(record_id, str):
                continue
            structured_ids[group.name].add(record_id)
            previous_path = seen_structured_ids.get(record_id)
            if previous_path is not None:
                errors.append(
                    f"{display_path(path, root)}: duplicate structured ID {record_id}; "
                    f"already used by {display_path(previous_path, root)}"
                )
            else:
                seen_structured_ids[record_id] = path

            if path.stem != record_id and not path.stem.startswith(f"{record_id}-"):
                errors.append(
                    f"{display_path(path, root)}: filename must be {record_id}.json "
                    f"or start with {record_id}-"
                )

        ledger_ids[group.name] = load_ledger_ids(
            root,
            group,
            errors,
            references=ledger_references,
        )
        ledger_counts[group.name] = len(ledger_ids[group.name])

    known_ids = {
        group.name: structured_ids[group.name] | ledger_ids[group.name]
        for group in GROUPS
    }
    errors.extend(validate_references(records, known_ids, root))
    errors.extend(validate_parent_family_cycles(records, root))
    errors.extend(validate_ledger_references(ledger_references, known_ids, root))
    # A registered directory is also visited by the closure scan.  Collapse an
    # identical path failure from those two independent checks into one report.
    errors = sorted(set(errors))
    return ValidationReport(errors, record_counts, ledger_counts)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (defaults to the parent of this script's directory)",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    report = validate_repository(args.root)
    if report.errors:
        print(
            f"Validation failed with {len(report.errors)} error(s):",
            file=sys.stderr,
        )
        for error in report.errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    counts = ", ".join(
        f"{group.name}s={report.record_counts[group.name]}"
        for group in GROUPS
    )
    ledger_counts = ", ".join(
        f"{group.name}s={report.ledger_counts[group.name]}"
        for group in GROUPS
    )
    print(
        f"Validated {report.total_records} structured records ({counts}); "
        f"ledger identities: {ledger_counts}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
