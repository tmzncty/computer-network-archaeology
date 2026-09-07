import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPOSITORY_ROOT / "schema" / "source-record.schema.json"
RECORD_DIRECTORY = REPOSITORY_ROOT / "records" / "sources"


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


class SourceClaimContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_json(SCHEMA_PATH)
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(
            cls.schema,
            format_checker=FormatChecker(),
        )

    def complete_record(self) -> dict[str, object]:
        return {
            "id": "SRC-9999",
            "source_type": "other",
            "title": "Example source",
            "research_state": "discovered",
            "rights_status": "unknown",
            "access": {"availability": "unknown"},
            "claims_extracted": [
                {
                    "claim": "The source documents an example fact.",
                    "locator": "Section 1",
                    "certainty": "confirmed",
                }
            ],
        }

    def assert_valid(self, document: dict[str, object]) -> None:
        errors = list(self.validator.iter_errors(document))
        self.assertEqual([], errors)

    def assert_field_error(
        self,
        document: dict[str, object],
        path: list[object],
        validator: str,
    ) -> None:
        errors = list(self.validator.iter_errors(document))
        matching_errors = [
            error
            for error in errors
            if error.validator == validator and list(error.absolute_path) == path
        ]
        self.assertTrue(
            matching_errors,
            f"expected {validator!r} at {path!r}; got {errors!r}",
        )

    def test_all_checked_in_source_records_validate(self) -> None:
        record_paths = sorted(RECORD_DIRECTORY.glob("*.json"))
        self.assertTrue(record_paths, "expected checked-in source records")

        for record_path in record_paths:
            with self.subTest(path=record_path.relative_to(REPOSITORY_ROOT)):
                self.assert_valid(load_json(record_path))

    def test_complete_source_claim_validates(self) -> None:
        self.assert_valid(self.complete_record())

    def test_extracted_claims_require_nonblank_claims_and_locators(self) -> None:
        cases = (
            (None, "type"),
            ("", "minLength"),
            (" \t ", "pattern"),
            ("\N{NO-BREAK SPACE}", "pattern"),
        )
        for field in ("claim", "locator"):
            for value, validator in cases:
                document = self.complete_record()
                document["claims_extracted"][0][field] = value

                with self.subTest(field=field, value=value):
                    self.assert_field_error(
                        document,
                        ["claims_extracted", 0, field],
                        validator,
                    )


if __name__ == "__main__":
    unittest.main()
