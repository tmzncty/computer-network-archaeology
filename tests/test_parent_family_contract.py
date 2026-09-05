import json
from pathlib import Path
import tempfile
import unittest

from scripts.validate_records import validate_repository

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class ParentFamilyContractTests(unittest.TestCase):
    def write_repository(
        self,
        root: Path,
        parent_families: dict[str, str],
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

        artifact_directory = root / "records/artifacts"
        artifact_directory.mkdir(parents=True)
        (root / "records/sources").mkdir()
        (root / "records/lineages").mkdir()
        for artifact_id, parent_family in parent_families.items():
            document = {
                "id": artifact_id,
                "canonical_name": f"Artifact {artifact_id}",
                "kind": "other",
                "parent_family": parent_family,
                "research_state": "seed",
                "certainty": "unknown",
                "sources": [
                    {
                        "source_id": "SRC-9000",
                        "supports": ["identity"],
                    }
                ],
            }
            (artifact_directory / f"{artifact_id}.json").write_text(
                json.dumps(document),
                encoding="utf-8",
            )

        data_directory = root / "data"
        data_directory.mkdir()
        (data_directory / "artifact-ledger.csv").write_text(
            "artifact_id\n",
            encoding="utf-8",
        )
        (data_directory / "source-ledger.csv").write_text(
            "source_id\nSRC-9000\n",
            encoding="utf-8",
        )
        (data_directory / "lineage-ledger.csv").write_text(
            "lineage_id\n",
            encoding="utf-8",
        )

    def validate(self, parent_families: dict[str, str]) -> list[str]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.write_repository(root, parent_families)

            return validate_repository(root).errors

    def test_rejects_a_parent_family_self_cycle(self) -> None:
        errors = self.validate({"ART-9001": "ART-9001"})

        self.assertEqual(
            [
                "records/artifacts/ART-9001.json:$.parent_family: "
                "parent_family cycle detected: ART-9001 -> ART-9001"
            ],
            errors,
        )

    def test_rejects_each_multi_record_parent_family_cycle_once(self) -> None:
        errors = self.validate(
            {
                "ART-9000": "ART-9002",
                "ART-9001": "ART-9002",
                "ART-9002": "ART-9001",
                "ART-9010": "ART-9012",
                "ART-9011": "ART-9010",
                "ART-9012": "ART-9011",
            }
        )

        self.assertEqual(
            [
                "records/artifacts/ART-9001.json:$.parent_family: "
                "parent_family cycle detected: "
                "ART-9001 -> ART-9002 -> ART-9001",
                "records/artifacts/ART-9010.json:$.parent_family: "
                "parent_family cycle detected: "
                "ART-9010 -> ART-9012 -> ART-9011 -> ART-9010",
            ],
            errors,
        )

    def test_accepts_acyclic_id_parents_and_textual_family_names(self) -> None:
        errors = self.validate(
            {
                "ART-9001": "Named root family",
                "ART-9002": "ART-9001",
                "ART-9003": "ART-9002",
            }
        )

        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
