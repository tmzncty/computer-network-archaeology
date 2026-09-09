"""Keep the iproute2 evidence identities distinct from the RFC source IDs."""
import json
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SOURCES = {
    "SRC-0286": {
        "canonical_url": "https://github.com/iproute2/iproute2/commit/e2613dc8605e56dbc53890ebbae263f93610bd41",
        "identifiers": [{"scheme": "git", "value": "e2613dc8605e56dbc53890ebbae263f93610bd41"}],
        "date": "2008-06-23",
        "artifacts": ["ART-0231", "ART-0250"],
        "claim_artifacts": ["ART-0231", "ART-0250"],
    },
    "SRC-0287": {
        "canonical_url": "https://github.com/iproute2/iproute2/commit/0dc34c7713bb7055378fe5cbc720d63d0db572a1",
        "identifiers": [{"scheme": "git", "value": "0dc34c7713bb7055378fe5cbc720d63d0db572a1"}],
        "date": "2011-07-13",
        "artifacts": ["ART-0231", "ART-0250"],
        "claim_artifacts": ["ART-0250"],
    },
    "SRC-0288": {
        "canonical_url": "https://github.com/iproute2/iproute2/blob/v3.0.0/ip/ipnetns.c",
        "identifiers": [{"scheme": "git-tag", "value": "v2.6.39"}, {"scheme": "git-tag", "value": "v3.0.0"}],
        "date": "2011-10-10",
        "artifacts": ["ART-0250"],
        "claim_artifacts": ["ART-0250"],
    },
}


def load_record(relative_path: str) -> dict:
    return json.loads((REPOSITORY_ROOT / relative_path).read_text(encoding="utf-8"))


class IPNetnsSourceIdentityTests(unittest.TestCase):
    def test_sources_identify_the_original_iproute2_documents(self) -> None:
        for source_id, expected in EXPECTED_SOURCES.items():
            with self.subTest(source_id=source_id):
                source = load_record(f"records/sources/{source_id}.json")
                self.assertEqual(source_id, source["id"])
                self.assertEqual("source-code", source["source_type"])
                self.assertEqual(expected["canonical_url"], source["access"]["canonical_url"])
                self.assertEqual(expected["identifiers"], source["identifiers"])
                self.assertEqual(expected["date"], source["date"]["value"])
                self.assertEqual(expected["artifacts"], source["artifact_ids"])
                claimed_artifacts = {
                    artifact_id
                    for claim in source["claims_extracted"]
                    for artifact_id in claim["artifact_ids"]
                }
                self.assertEqual(set(expected["claim_artifacts"]), claimed_artifacts)

    def test_artifact_citations_resolve_to_userspace_sources_not_rfcs(self) -> None:
        for filename, expected in (
            ("ART-0231-linux-network-namespace.json", {"SRC-0286", "SRC-0287"}),
            ("ART-0250-iproute2-ip-netns.json", set(EXPECTED_SOURCES)),
        ):
            with self.subTest(artifact=filename):
                artifact = load_record(f"records/artifacts/{filename}")
                citations = [citation["source_id"] for citation in artifact["sources"]]
                self.assertEqual(len(citations), len(set(citations)))
                self.assertEqual(expected, set(citations) & set(EXPECTED_SOURCES))
                self.assertTrue({"SRC-0277", "SRC-0278", "SRC-0279"}.isdisjoint(citations))
                for source_id in expected:
                    source = load_record(f"records/sources/{source_id}.json")
                    self.assertIn(artifact["id"], source["artifact_ids"])

    def test_release_chronology_uses_introduction_and_tag_boundary(self) -> None:
        artifact = load_record("records/artifacts/ART-0250-iproute2-ip-netns.json")
        operational = artifact["chronology"]["first_operational"]
        self.assertEqual(["SRC-0287", "SRC-0288"], operational["source_ids"])
        self.assertEqual("2011-10-10", operational["value"])
        self.assertEqual("day", operational["precision"])
        self.assertEqual("confirmed", operational["certainty"])
        for source_id in operational["source_ids"]:
            source = load_record(f"records/sources/{source_id}.json")
            self.assertEqual(EXPECTED_SOURCES[source_id]["canonical_url"], source["access"]["canonical_url"])


if __name__ == "__main__":
    unittest.main()
