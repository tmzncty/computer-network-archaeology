import json
from pathlib import Path
import tempfile
import unittest

from scripts.validate_records import (
    GROUP_BY_NAME,
    LedgerReference,
    load_ledger_ids,
    validate_ledger_references,
    validate_repository,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
LINEAGE_HEADER = (
    "lineage_id,from_artifact_id,from_name,to_artifact_id,to_name\n"
)


class LineageLedgerEndpointContractTests(unittest.TestCase):
    def write_minimal_repository(
        self,
        root: Path,
        lineage_row: str,
        *,
        lineage_header: str = LINEAGE_HEADER,
    ) -> None:
        for schema_name in (
            "artifact-record.schema.json",
            "source-record.schema.json",
            "lineage-edge.schema.json",
        ):
            destination = root / "schema" / schema_name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(
                (REPOSITORY_ROOT / "schema" / schema_name).read_bytes()
            )

        for record_directory in ("artifacts", "sources", "lineages"):
            (root / "records" / record_directory).mkdir(parents=True)
        (root / "records/artifacts/ART-9001.json").write_text(
            json.dumps(
                {
                    "id": "ART-9001",
                    "canonical_name": "Structured-only endpoint",
                    "kind": "other",
                    "research_state": "seed",
                    "certainty": "unknown",
                    "sources": [
                        {
                            "source_id": "SRC-9001",
                            "supports": ["identity"],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )

        data_directory = root / "data"
        data_directory.mkdir()
        (data_directory / "artifact-ledger.csv").write_text(
            "artifact_id\nART-9002\n",
            encoding="utf-8",
        )
        (data_directory / "source-ledger.csv").write_text(
            "source_id\nSRC-9001\n",
            encoding="utf-8",
        )
        (data_directory / "lineage-ledger.csv").write_text(
            lineage_header + lineage_row,
            encoding="utf-8",
        )

    def load_and_validate(
        self,
        content: str,
        *,
        known_artifact_ids: set[str] | None = None,
    ) -> tuple[set[str], list[LedgerReference], list[str]]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            group = GROUP_BY_NAME["lineage"]
            ledger_path = root / group.ledger
            ledger_path.parent.mkdir(parents=True)
            ledger_path.write_text(content, encoding="utf-8")
            errors: list[str] = []
            references: list[LedgerReference] = []

            ledger_ids = load_ledger_ids(
                root,
                group,
                errors,
                references=references,
            )
            errors.extend(
                validate_ledger_references(
                    references,
                    {
                        "artifact": known_artifact_ids or set(),
                        "source": set(),
                        "lineage": ledger_ids,
                    },
                    root,
                )
            )

        return ledger_ids, references, errors

    def test_accepts_blank_endpoint_ids_for_name_only_edges(self) -> None:
        ledger_ids, references, errors = self.load_and_validate(
            LINEAGE_HEADER
            + "LIN-9001,,Named origin,   ,Named destination\n"
        )

        self.assertEqual({"LIN-9001"}, ledger_ids)
        self.assertEqual([], references)
        self.assertEqual([], errors)

    def test_accepts_an_empty_ledger_without_endpoint_columns(self) -> None:
        ledger_ids, references, errors = self.load_and_validate("lineage_id\n")

        self.assertEqual(set(), ledger_ids)
        self.assertEqual([], references)
        self.assertEqual([], errors)

    def test_rejects_missing_endpoint_id_columns(self) -> None:
        cases = (
            (
                "lineage_id,from_name,to_artifact_id,to_name\n"
                "LIN-9001,Named origin,,Named destination\n",
                ("from_artifact_id",),
            ),
            (
                "lineage_id,from_artifact_id,from_name,to_name\n"
                "LIN-9001,,Named origin,Named destination\n",
                ("to_artifact_id",),
            ),
            (
                "lineage_id,from_name,to_name\n"
                "LIN-9001,Named origin,Named destination\n",
                ("from_artifact_id", "to_artifact_id"),
            ),
        )

        for content, missing_columns in cases:
            with self.subTest(missing_columns=missing_columns):
                ledger_ids, references, errors = self.load_and_validate(content)

                rendered = ", ".join(repr(column) for column in missing_columns)
                self.assertEqual(set(), ledger_ids)
                self.assertEqual([], references)
                self.assertEqual(
                    [
                        "data/lineage-ledger.csv: missing required reference "
                        f"column(s): {rendered}"
                    ],
                    errors,
                )

    def test_repository_entrypoint_rejects_missing_endpoint_id_columns(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.write_minimal_repository(
                root,
                "LIN-9001,Named origin,Named destination\n",
                lineage_header="lineage_id,from_name,to_name\n",
            )

            report = validate_repository(root)

        self.assertEqual(
            [
                "data/lineage-ledger.csv: missing required reference column(s): "
                "'from_artifact_id', 'to_artifact_id'"
            ],
            report.errors,
        )

    def test_repository_accepts_structured_and_ledger_identity_union(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.write_minimal_repository(
                root,
                "LIN-9001,ART-9001,Structured endpoint,"
                "ART-9002,Ledger endpoint\n",
            )

            report = validate_repository(root)

        self.assertEqual([], report.errors, "\n".join(report.errors))
        self.assertEqual(
            {"artifact": 1, "source": 0, "lineage": 0},
            report.record_counts,
        )
        self.assertEqual(
            {"artifact": 1, "source": 1, "lineage": 1},
            report.ledger_counts,
        )

    def test_repository_entrypoint_rejects_unknown_endpoint(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.write_minimal_repository(
                root,
                "LIN-9001,ART-9001,Structured endpoint,"
                "ART-9003,Unknown endpoint\n",
            )

            report = validate_repository(root)

        self.assertEqual(
            [
                "data/lineage-ledger.csv:2:to_artifact_id: unknown artifact "
                "ID ART-9003"
            ],
            report.errors,
        )

    def test_rejects_malformed_endpoint_before_resolution(self) -> None:
        ledger_ids, references, errors = self.load_and_validate(
            LINEAGE_HEADER
            + "LIN-9001,ART-123,Malformed endpoint,,Named destination\n"
        )

        self.assertEqual({"LIN-9001"}, ledger_ids)
        self.assertEqual(1, len(references))
        self.assertEqual(
            [
                "data/lineage-ledger.csv:2:from_artifact_id: invalid artifact "
                "ID 'ART-123'; expected ART- followed by at least four digits"
            ],
            errors,
        )

    def test_rejects_unknown_ids_in_both_endpoint_columns(self) -> None:
        ledger_ids, references, errors = self.load_and_validate(
            LINEAGE_HEADER
            + "LIN-9001,ART-9003,Unknown origin,ART-9004,Unknown destination\n"
        )

        self.assertEqual({"LIN-9001"}, ledger_ids)
        self.assertEqual(2, len(references))
        self.assertEqual(
            [
                "data/lineage-ledger.csv:2:from_artifact_id: unknown artifact "
                "ID ART-9003",
                "data/lineage-ledger.csv:2:to_artifact_id: unknown artifact "
                "ID ART-9004",
            ],
            errors,
        )

    def test_diagnostic_uses_physical_line_and_column(self) -> None:
        ledger_ids, references, errors = self.load_and_validate(
            LINEAGE_HEADER
            + "\n"
            + 'LIN-9001,,"Name spanning\nphysical lines",ART-9003,Unknown\n'
        )

        self.assertEqual({"LIN-9001"}, ledger_ids)
        self.assertEqual(1, len(references))
        self.assertEqual(
            [
                "data/lineage-ledger.csv:4:to_artifact_id: unknown artifact "
                "ID ART-9003"
            ],
            errors,
        )

    def test_current_ledger_has_84_valid_edges_and_46_endpoint_refs(self) -> None:
        group = GROUP_BY_NAME["lineage"]
        errors: list[str] = []
        references: list[LedgerReference] = []

        ledger_ids = load_ledger_ids(
            REPOSITORY_ROOT,
            group,
            errors,
            references=references,
        )
        report = validate_repository(REPOSITORY_ROOT)

        self.assertEqual([], errors)
        self.assertEqual(84, len(ledger_ids))
        self.assertEqual(46, len(references))
        self.assertEqual(84, report.ledger_counts["lineage"])
        self.assertEqual([], report.errors, "\n".join(report.errors))


if __name__ == "__main__":
    unittest.main()
