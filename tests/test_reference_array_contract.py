import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class ReferenceArrayContractTests(unittest.TestCase):
    def load_validator(self, schema_name: str) -> Draft202012Validator:
        schema = json.loads(
            (REPOSITORY_ROOT / "schema" / schema_name).read_text(encoding="utf-8")
        )
        return Draft202012Validator(schema, format_checker=FormatChecker())

    def test_rejects_duplicate_ids_within_one_claim(self) -> None:
        cases = (
            (
                "artifact chronology source IDs",
                self.load_validator("artifact-record.schema.json"),
                {
                    "id": "ART-9999",
                    "canonical_name": "Example artifact",
                    "kind": "other",
                    "research_state": "seed",
                    "certainty": "unknown",
                    "sources": [
                        {"source_id": "SRC-0001", "supports": ["identity"]}
                    ],
                    "chronology": {
                        "announced": {
                            "value": "1970",
                            "precision": "year",
                            "certainty": "unknown",
                            "source_ids": ["SRC-0001", "SRC-0001"],
                        }
                    },
                },
            ),
            (
                "source claim artifact IDs",
                self.load_validator("source-record.schema.json"),
                {
                    "id": "SRC-9999",
                    "source_type": "other",
                    "title": "Example source",
                    "research_state": "discovered",
                    "rights_status": "unknown",
                    "access": {"availability": "unknown"},
                    "claims_extracted": [
                        {
                            "claim": "Example claim",
                            "locator": "p. 1",
                            "certainty": "unknown",
                            "artifact_ids": ["ART-0001", "ART-0001"],
                        }
                    ],
                },
            ),
        )

        for label, validator, document in cases:
            with self.subTest(case=label):
                errors = list(validator.iter_errors(document))
                self.assertEqual(["uniqueItems"], [error.validator for error in errors])

    def test_accepts_distinct_ids_within_one_claim(self) -> None:
        artifact = {
            "id": "ART-9999",
            "canonical_name": "Example artifact",
            "kind": "other",
            "research_state": "seed",
            "certainty": "unknown",
            "sources": [{"source_id": "SRC-0001", "supports": ["identity"]}],
            "chronology": {
                "announced": {
                    "value": "1970",
                    "precision": "year",
                    "certainty": "unknown",
                    "source_ids": ["SRC-0001", "SRC-0002"],
                }
            },
        }
        source = {
            "id": "SRC-9999",
            "source_type": "other",
            "title": "Example source",
            "research_state": "discovered",
            "rights_status": "unknown",
            "access": {"availability": "unknown"},
            "claims_extracted": [
                {
                    "claim": "Example claim",
                    "locator": "p. 1",
                    "certainty": "unknown",
                    "artifact_ids": ["ART-0001", "ART-0002"],
                }
            ],
        }

        self.assertTrue(
            self.load_validator("artifact-record.schema.json").is_valid(artifact)
        )
        self.assertTrue(
            self.load_validator("source-record.schema.json").is_valid(source)
        )


if __name__ == "__main__":
    unittest.main()
