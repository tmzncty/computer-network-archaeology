import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from scripts.validate_records import (
    GROUPS,
    LoadedRecord,
    iter_references,
    load_json_object,
    load_schema,
    validate_references,
    validate_repository,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class StrictJSONLoadingTests(unittest.TestCase):
    def test_rejects_duplicate_keys_at_any_depth(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            path = root / "record.json"
            path.write_text(
                '{"metadata":{"claim":"first","claim":"second"}}',
                encoding="utf-8",
            )
            errors: list[str] = []

            document = load_json_object(path, root, errors)

        self.assertIsNone(document)
        self.assertEqual(
            ["record.json: invalid JSON: duplicate object key 'claim'"],
            errors,
        )

    def test_rejects_non_finite_numbers(self) -> None:
        for value in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                path = root / "record.json"
                path.write_text(f'{{"metadata":{{"value":{value}}}}}', encoding="utf-8")
                errors: list[str] = []

                document = load_json_object(path, root, errors)

                self.assertIsNone(document)
                self.assertEqual(
                    [f"record.json: invalid JSON: non-finite number {value!r}"],
                    errors,
                )

    def test_preserves_non_integral_decimal_numbers_exactly(self) -> None:
        for raw_number in ("1880.0000000000000001", "1e-324"):
            with self.subTest(
                raw_number=raw_number
            ), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                path = root / "record.json"
                path.write_text(f'{{"value":{raw_number}}}', encoding="utf-8")
                errors: list[str] = []

                document = load_json_object(path, root, errors)

                self.assertEqual([], errors)
                self.assertIsNotNone(document)
                value = document["value"]
                self.assertIsInstance(value, Decimal)
                self.assertEqual(Decimal(raw_number), value)

    def test_normalizes_integral_decimal_spellings_to_integers(self) -> None:
        cases = {
            "1.88e3": 1880,
            "-0.0": 0,
            "1e400": 10**400,
            "1e4299": 10**4299,
        }
        for raw_number, expected in cases.items():
            with self.subTest(
                raw_number=raw_number
            ), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                path = root / "record.json"
                path.write_text(f'{{"value":{raw_number}}}', encoding="utf-8")
                errors: list[str] = []

                document = load_json_object(path, root, errors)

                self.assertEqual([], errors)
                self.assertIsNotNone(document)
                self.assertIs(type(document["value"]), int)
                self.assertEqual(expected, document["value"])

    def test_rejects_numbers_that_exceed_decoder_resource_limits(self) -> None:
        cases = {
            "unrepresentable exponent": (
                "1e1000000000000000000",
                "unrepresentable decimal exponent",
            ),
            "expanded exponent": ("1e4300", "integer exceeds 4300 decimal digits"),
            "integer literal": ("1" * 4301, "integer exceeds 4300 decimal digits"),
        }
        for name, (raw_number, expected_error) in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                path = root / "record.json"
                path.write_text(f'{{"value":{raw_number}}}', encoding="utf-8")
                errors: list[str] = []

                document = load_json_object(path, root, errors)

                self.assertIsNone(document)
                self.assertEqual(
                    [f"record.json: invalid JSON: {expected_error}"],
                    errors,
                )

    def test_integral_schema_keywords_remain_valid(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "schema.json"
            path.write_text('{"type":"array","minItems":1.0}', encoding="utf-8")
            errors: list[str] = []

            schema = load_schema(path, root, errors)

        self.assertEqual([], errors)
        self.assertIsNotNone(schema)
        self.assertIs(type(schema["minItems"]), int)
        self.assertEqual(1, schema["minItems"])


class ExactNumberRepositoryTests(unittest.TestCase):
    DRAFT = "https://json-schema.org/draft/2020-12/schema"

    def write_repository(self, root: Path, raw_number: str) -> None:
        bounded_integer = {
            "$schema": self.DRAFT,
            "type": "integer",
            "minimum": 0,
            "maximum": 3000,
        }
        artifact_schema = {
            "$schema": self.DRAFT,
            "type": "object",
            "$defs": {"boundedInteger": bounded_integer},
            "properties": {
                "id": {"type": "string"},
                "physical": {
                    "type": "object",
                    "properties": {
                        "nominal_bit_rate_bps": {
                            "$ref": "#/$defs/boundedInteger"
                        }
                    },
                },
            },
        }

        for group in GROUPS:
            (root / group.directory).mkdir(parents=True, exist_ok=True)
            schema_path = root / group.schema
            schema_path.parent.mkdir(parents=True, exist_ok=True)
            schema = artifact_schema if group.name == "artifact" else {}
            schema_path.write_text(json.dumps(schema), encoding="utf-8")
            ledger_path = root / group.ledger
            ledger_path.parent.mkdir(parents=True, exist_ok=True)
            ledger_path.write_text(f"{group.ledger_id_column}\n", encoding="utf-8")

        artifact = root / "records/artifacts/ART-9999.json"
        artifact.write_text(
            '{"id":"ART-9999","physical":{"nominal_bit_rate_bps":'
            f"{raw_number}}}}}",
            encoding="utf-8",
        )

    def test_repository_rejects_precision_bypass_numbers(self) -> None:
        cases = {
            "rounding": ("1880.0000000000000001", "not of type 'integer'"),
            "underflow": ("1e-324", "not of type 'integer'"),
            "large finite value": ("1e400", "greater than the maximum of 3000"),
        }
        for name, (raw_number, expected_error) in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self.write_repository(root, raw_number)

                report = validate_repository(root)

                self.assertEqual(1, len(report.errors), report.errors)
                self.assertIn(
                    "records/artifacts/ART-9999.json:"
                    "$.physical.nominal_bit_rate_bps:",
                    report.errors[0],
                )
                self.assertIn(expected_error, report.errors[0])

    def test_repository_accepts_integral_decimal_spellings(self) -> None:
        for raw_number in ("1.88e3", "-0.0"):
            with self.subTest(
                raw_number=raw_number
            ), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self.write_repository(root, raw_number)

                report = validate_repository(root)

                self.assertEqual([], report.errors)


class RecordDiscoveryTests(unittest.TestCase):
    def test_rejects_noncanonical_record_locations(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            normal = root / "records/artifacts/ART-9996.json"
            nested = root / "records/artifacts/nested/ART-9997.json"
            unknown = root / "records/unknown/ART-9998.json"
            uppercase = root / "records/sources/SRC-9999.JSON"
            for path in (normal, nested, unknown, uppercase):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("{}", encoding="utf-8")

            report = validate_repository(root)

        self.assertEqual(
            {"artifact": 1, "source": 0, "lineage": 0},
            report.record_counts,
        )
        self.assertIn(
            "records/artifacts/nested/ART-9997.json: JSON records must be "
            "directly inside a registered record directory",
            report.errors,
        )
        self.assertIn(
            "records/unknown/ART-9998.json: unregistered record directory 'unknown'",
            report.errors,
        )
        self.assertIn(
            "records/sources/SRC-9999.JSON: JSON record extension must be .json",
            report.errors,
        )

    def test_rejects_record_symlink_outside_repository(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            base = Path(temporary_directory)
            root = base / "repository"
            record_directory = root / "records/artifacts"
            record_directory.mkdir(parents=True)
            external_record = base / "external.json"
            external_record.write_text("{}", encoding="utf-8")
            symlink = record_directory / "ART-9999.json"
            external_directory = base / "external-sources"
            external_directory.mkdir()
            directory_symlink = root / "records/sources"
            try:
                symlink.symlink_to(external_record)
                directory_symlink.symlink_to(
                    external_directory, target_is_directory=True
                )
            except (NotImplementedError, OSError) as error:
                self.skipTest(f"cannot create symlinks on this platform: {error}")

            report = validate_repository(root)

        self.assertEqual(0, report.record_counts["artifact"])
        self.assertEqual(
            1,
            report.errors.count(
                "records/artifacts/ART-9999.json: resolves outside repository root"
            ),
        )
        self.assertEqual(
            1,
            report.errors.count(
                "records/sources: resolves outside repository root"
            ),
        )


class ReferenceExtractionTests(unittest.TestCase):
    def test_extracts_references_from_each_record_shape(self) -> None:
        artifact = {
            "parent_family": "ART-0001",
            "chronology": {
                "announced": {"source_ids": ["SRC-0001", "SRC-0002"]}
            },
            "sources": [{"source_id": "SRC-0003"}],
            "related_artifacts": [{"id": "ART-0002", "relation": "revision-of"}],
        }
        source = {
            "artifact_ids": ["ART-0003"],
            "claims_extracted": [{"artifact_ids": ["ART-0004"]}],
        }
        lineage = {
            "from": {"artifact_id": "ART-0005"},
            "to": {"artifact_id": "ART-0006"},
            "sources": [{"source_ref": "SRC-0004; SRC-0005"}],
        }

        actual = {
            (reference.target_group, reference.target_id)
            for group, document in (
                ("artifact", artifact),
                ("source", source),
                ("lineage", lineage),
            )
            for reference in iter_references(group, document)
        }

        self.assertEqual(
            {
                ("artifact", f"ART-{number:04d}") for number in range(1, 7)
            }
            | {("source", f"SRC-{number:04d}") for number in range(1, 6)},
            actual,
        )

    def test_unknown_reference_reports_its_json_path(self) -> None:
        path = REPOSITORY_ROOT / "records/artifacts/ART-9999-example.json"
        records = [
            LoadedRecord(
                "artifact",
                path,
                {"id": "ART-9999", "sources": [{"source_id": "SRC-9999"}]},
            )
        ]
        errors = validate_references(
            records,
            {"artifact": {"ART-9999"}, "source": set(), "lineage": set()},
            REPOSITORY_ROOT,
        )

        self.assertEqual(
            [
                "records/artifacts/ART-9999-example.json:$.sources[0].source_id: "
                "unknown source ID SRC-9999"
            ],
            errors,
        )


class SourceArtifactSemanticRegressionTests(unittest.TestCase):
    EXPECTED_SOURCE_ARTIFACTS = {
        "SRC-0159": "ART-0170",
        "SRC-0160": "ART-0171",
        "SRC-0161": "ART-0172",
        "SRC-0162": "ART-0173",
        "SRC-0163": "ART-0174",
        "SRC-0164": "ART-0174",
        "SRC-0165": "ART-0169",
    }

    def test_root_hunting_sources_match_their_semantic_artifacts(self) -> None:
        artifacts: dict[str, dict[str, object]] = {}
        for path in (REPOSITORY_ROOT / "records/artifacts").glob("*.json"):
            artifact = json.loads(path.read_text(encoding="utf-8"))
            artifacts[artifact["id"]] = artifact

        for source_id, artifact_id in self.EXPECTED_SOURCE_ARTIFACTS.items():
            with self.subTest(source_id=source_id, artifact_id=artifact_id):
                source_paths = list(
                    (REPOSITORY_ROOT / "records/sources").glob(f"{source_id}-*.json")
                )
                self.assertEqual(1, len(source_paths))
                source = json.loads(source_paths[0].read_text(encoding="utf-8"))

                self.assertEqual([artifact_id], source["artifact_ids"])
                claims = source["claims_extracted"]
                self.assertGreater(len(claims), 0)
                for claim in claims:
                    self.assertEqual([artifact_id], claim["artifact_ids"])

                artifact_source_ids = {
                    citation["source_id"]
                    for citation in artifacts[artifact_id]["sources"]
                }
                self.assertIn(source_id, artifact_source_ids)


class RepositoryValidationTests(unittest.TestCase):
    def test_repository_evidence_graph_is_valid(self) -> None:
        report = validate_repository(REPOSITORY_ROOT)
        self.assertEqual([], report.errors, "\n".join(report.errors))
        self.assertGreater(report.total_records, 400)


if __name__ == "__main__":
    unittest.main()
