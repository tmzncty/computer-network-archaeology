import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPOSITORY_ROOT / "schema" / "lineage-edge.schema.json"
RECORD_DIRECTORY = REPOSITORY_ROOT / "records" / "lineages"


def load_json(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as source:
        return json.load(source)


class LineageEdgeContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_json(SCHEMA_PATH)
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema)
        cls.relations = cls.schema["properties"]["relation"]["enum"]

    def complete_record(self, relation: str = "influenced") -> dict[str, object]:
        return {
            "id": "LIN-9999",
            "from": {"name": "Example predecessor"},
            "to": {"name": "Example successor"},
            "relation": relation,
            "scope": ["interface"],
            "property": "A documented interface convention survives.",
            "certainty": "confirmed",
            "directness": "documented-design",
            "sources": [
                {
                    "source_ref": "SRC-0001",
                    "locator": "Section 1",
                    "supports": "The source documents the carried-over convention.",
                }
            ],
        }

    def assert_valid(self, document: dict[str, object]) -> None:
        errors = list(self.validator.iter_errors(document))
        self.assertEqual([], errors)

    def assert_required(self, document: dict[str, object], field: str) -> None:
        errors = list(self.validator.iter_errors(document))
        matching_errors = [
            error
            for error in errors
            if error.validator == "required"
            and list(error.absolute_path) == []
            and field in error.validator_value
            and field in error.message
        ]
        self.assertTrue(
            matching_errors,
            f"expected the lineage edge to require {field!r}; got {errors!r}",
        )

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
            if error.validator == validator
            and list(error.absolute_path) == path
        ]
        self.assertTrue(
            matching_errors,
            f"expected {validator!r} at {path!r}; got {errors!r}",
        )

    def test_schema_declares_valid_draft_2020_12(self) -> None:
        self.assertEqual(
            "https://json-schema.org/draft/2020-12/schema",
            self.schema["$schema"],
        )

    def test_all_checked_in_lineage_records_validate(self) -> None:
        record_paths = sorted(RECORD_DIRECTORY.glob("*.json"))
        self.assertTrue(record_paths, "expected checked-in lineage records")

        for record_path in record_paths:
            with self.subTest(path=record_path.relative_to(REPOSITORY_ROOT)):
                self.assert_valid(load_json(record_path))

    def test_complete_lineage_edge_validates(self) -> None:
        self.assert_valid(self.complete_record())

    def test_nonempty_scope_does_not_advertise_an_empty_default(self) -> None:
        scope_schema = self.schema["properties"]["scope"]

        self.assertNotIn("default", scope_schema)

    def test_every_relation_requires_shared_claim_fields(self) -> None:
        for relation in self.relations:
            for field in ("scope", "property", "directness"):
                document = self.complete_record(relation)
                del document[field]

                with self.subTest(relation=relation, field=field):
                    self.assert_required(document, field)

    def test_every_relation_requires_nonempty_scope(self) -> None:
        for relation in self.relations:
            document = self.complete_record(relation)
            document["scope"] = []

            with self.subTest(relation=relation):
                self.assert_field_error(document, ["scope"], "minItems")

    def test_every_relation_requires_a_nonblank_property(self) -> None:
        cases = (
            (None, "type"),
            ("", "minLength"),
            (" \t ", "pattern"),
            ("\N{NO-BREAK SPACE}", "pattern"),
        )
        for relation in self.relations:
            for value, validator in cases:
                document = self.complete_record(relation)
                document["property"] = value

                with self.subTest(relation=relation, value=value):
                    self.assert_field_error(document, ["property"], validator)

    def test_every_relation_source_requires_supports(self) -> None:
        for relation in self.relations:
            document = self.complete_record(relation)
            del document["sources"][0]["supports"]
            errors = list(self.validator.iter_errors(document))
            matching_errors = [
                error
                for error in errors
                if error.validator == "required"
                and list(error.absolute_path) == ["sources", 0]
                and "supports" in error.validator_value
                and "supports" in error.message
            ]

            with self.subTest(relation=relation):
                self.assertTrue(
                    matching_errors,
                    f"expected each source to require 'supports'; got {errors!r}",
                )

    def test_every_relation_requires_nonblank_source_reference_and_locator(
        self,
    ) -> None:
        cases = (
            (None, "type"),
            ("", "minLength"),
            (" \t ", "pattern"),
            ("\N{NO-BREAK SPACE}", "pattern"),
        )
        for relation in self.relations:
            for field in ("source_ref", "locator"):
                for value, validator in cases:
                    document = self.complete_record(relation)
                    document["sources"][0][field] = value

                    with self.subTest(
                        relation=relation,
                        field=field,
                        value=value,
                    ):
                        self.assert_field_error(
                            document,
                            ["sources", 0, field],
                            validator,
                        )

    def test_every_relation_requires_nonblank_source_supports(self) -> None:
        cases = (
            (None, "type"),
            ("", "minLength"),
            (" \t ", "pattern"),
            ("\N{NO-BREAK SPACE}", "pattern"),
        )
        for relation in self.relations:
            for value, validator in cases:
                document = self.complete_record(relation)
                document["sources"][0]["supports"] = value

                with self.subTest(relation=relation, value=value):
                    self.assert_field_error(
                        document,
                        ["sources", 0, "supports"],
                        validator,
                    )


if __name__ == "__main__":
    unittest.main()
