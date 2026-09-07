import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_records import GROUPS, GROUP_BY_NAME, validate_repository


class SourceClaimProjectionContractTests(unittest.TestCase):
    def write_repository(
        self,
        root: Path,
        *,
        artifact_ids: list[str],
        claim_artifact_id_groups: list[list[str]],
    ) -> None:
        referenced_artifacts = {
            artifact_id for group in claim_artifact_id_groups for artifact_id in group
        }
        known_artifacts = sorted(
            artifact_id
            for artifact_id in set(artifact_ids) | referenced_artifacts
            if GROUP_BY_NAME["artifact"].id_pattern.fullmatch(artifact_id)
        )
        for group in GROUPS:
            (root / group.directory).mkdir(parents=True, exist_ok=True)
            schema_path = root / group.schema
            schema_path.parent.mkdir(parents=True, exist_ok=True)
            schema_path.write_text("{}", encoding="utf-8")
            ledger_path = root / group.ledger
            ledger_path.parent.mkdir(parents=True, exist_ok=True)
            rows = [group.ledger_id_column]
            if group.name == "artifact":
                rows.extend(known_artifacts)
            ledger_path.write_text("\n".join(rows) + "\n", encoding="utf-8")

        document = {
            "id": "SRC-9999",
            "artifact_ids": artifact_ids,
            "claims_extracted": [
                {
                    "claim": f"Fixture claim {index}",
                    "locator": f"p. {index + 1}",
                    "certainty": "confirmed",
                    "artifact_ids": claim_artifact_ids,
                }
                for index, claim_artifact_ids in enumerate(claim_artifact_id_groups)
            ],
        }
        (root / "records/sources/SRC-9999.json").write_text(
            json.dumps(document), encoding="utf-8"
        )

    def validate(
        self, *, artifact_ids: list[str], claim_artifact_id_groups: list[list[str]]
    ) -> list[str]:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_repository(
                root,
                artifact_ids=artifact_ids,
                claim_artifact_id_groups=claim_artifact_id_groups,
            )
            return validate_repository(root).errors

    def test_rejects_claim_artifact_omitted_from_source_summary(self) -> None:
        self.assertEqual(
            [
                "records/sources/SRC-9999.json:"
                "$.claims_extracted[0].artifact_ids[0]: artifact ID ART-9002 "
                "is not declared in $.artifact_ids"
            ],
            self.validate(
                artifact_ids=["ART-9001"],
                claim_artifact_id_groups=[["ART-9002"]],
            ),
        )

    def test_accepts_a_complete_source_artifact_summary(self) -> None:
        self.assertEqual(
            [],
            self.validate(
                artifact_ids=["ART-9001", "ART-9002"],
                claim_artifact_id_groups=[["ART-9002"]],
            ),
        )

    def test_allows_summary_artifacts_without_extracted_claims(self) -> None:
        self.assertEqual(
            [],
            self.validate(
                artifact_ids=["ART-9001", "ART-9002"],
                claim_artifact_id_groups=[["ART-9001"]],
            ),
        )

    def test_malformed_claim_id_does_not_add_projection_noise(self) -> None:
        self.assertEqual(
            [
                "records/sources/SRC-9999.json:"
                "$.claims_extracted[0].artifact_ids[0]: "
                "unknown artifact ID not-an-artifact"
            ],
            self.validate(
                artifact_ids=["ART-9001"],
                claim_artifact_id_groups=[["not-an-artifact"]],
            ),
        )

    def test_reports_exact_paths_across_claims_and_artifact_indexes(self) -> None:
        self.assertEqual(
            [
                "records/sources/SRC-9999.json:"
                "$.claims_extracted[0].artifact_ids[1]: artifact ID ART-9002 "
                "is not declared in $.artifact_ids",
                "records/sources/SRC-9999.json:"
                "$.claims_extracted[1].artifact_ids[0]: artifact ID ART-9003 "
                "is not declared in $.artifact_ids",
            ],
            self.validate(
                artifact_ids=["ART-9001"],
                claim_artifact_id_groups=[
                    ["ART-9001", "ART-9002"],
                    ["ART-9003", "ART-9001"],
                ],
            ),
        )


if __name__ == "__main__":
    unittest.main()
