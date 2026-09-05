import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPOSITORY_ROOT / "schema" / "artifact-record.schema.json"


class ArtifactPhysicalContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(
            cls.schema,
            format_checker=FormatChecker(),
        )

    def complete_record(self) -> dict[str, object]:
        return {
            "id": "ART-9999",
            "canonical_name": "Example interface",
            "kind": "interface",
            "research_state": "seed",
            "certainty": "unknown",
            "sources": [
                {
                    "source_id": "SRC-9999",
                    "supports": ["identity"],
                }
            ],
        }

    def record_with_rate(self, value: object) -> dict[str, object]:
        document = self.complete_record()
        document["physical"] = {"nominal_bit_rate_bps": value}
        return document

    def test_rejects_zero_nominal_bit_rates(self) -> None:
        cases = (
            0,
            0.0,
            -0.0,
            [0],
            [9600, 0],
            [0, 9600],
        )

        for value in cases:
            with self.subTest(value=value):
                self.assertFalse(self.validator.is_valid(self.record_with_rate(value)))

    def test_accepts_positive_integer_rates_at_and_above_the_boundary(self) -> None:
        # JSON Schema treats a number with a zero fractional part as an integer.
        cases = (
            1,
            1.0,
            [1],
            [1, 9600],
        )

        for value in cases:
            with self.subTest(value=value):
                self.assertTrue(self.validator.is_valid(self.record_with_rate(value)))

    def test_preserves_integer_type_rules(self) -> None:
        cases = (
            True,
            "9600",
            0.5,
            [True],
            ["9600"],
            [9600, 0.5],
        )

        for value in cases:
            with self.subTest(value=value):
                self.assertFalse(self.validator.is_valid(self.record_with_rate(value)))

    def test_omits_the_rate_when_unknown_or_not_applicable(self) -> None:
        cases = (
            self.complete_record(),
            {**self.complete_record(), "physical": {}},
            {
                **self.complete_record(),
                "physical": {"medium": "varied by installed interface"},
            },
        )

        for document in cases:
            with self.subTest(physical=document.get("physical")):
                self.assertTrue(self.validator.is_valid(document))

        for sentinel in (None, "unknown", "not-applicable"):
            with self.subTest(sentinel=sentinel):
                self.assertFalse(
                    self.validator.is_valid(self.record_with_rate(sentinel))
                )


if __name__ == "__main__":
    unittest.main()
