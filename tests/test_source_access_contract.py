import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class SourceAccessContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        schema = json.loads(
            (REPOSITORY_ROOT / "schema/source-record.schema.json").read_text(
                encoding="utf-8"
            )
        )
        cls.validator = Draft202012Validator(schema, format_checker=FormatChecker())

    def source_with_access(self, access: dict[str, object]) -> dict[str, object]:
        return {
            "id": "SRC-9999",
            "source_type": "other",
            "title": "Example source",
            "research_state": "discovered",
            "rights_status": "unknown",
            "access": access,
        }

    def test_rejects_access_without_availability(self) -> None:
        cases = ({}, {"canonical_url": "https://example.test/source"})

        for access in cases:
            with self.subTest(access=access):
                errors = list(
                    self.validator.iter_errors(self.source_with_access(access))
                )
                self.assertEqual(1, len(errors))
                self.assertEqual(["access"], list(errors[0].absolute_path))
                self.assertEqual("required", errors[0].validator)
                self.assertIn(
                    "'availability' is a required property", errors[0].message
                )

    def test_accepts_explicit_unknown_availability(self) -> None:
        source = self.source_with_access({"availability": "unknown"})

        self.assertTrue(self.validator.is_valid(source))


if __name__ == "__main__":
    unittest.main()
