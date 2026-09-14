"""Guard the combined kernel, RFC, veth and iproute2 source identities."""
import csv
import json
import unittest
from collections import Counter
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
# Kernel/userspace: b00efb91894917280bfd046e1bfd57504bde992e.
# RFC/veth: 482a2819e236cdeaa7d97982f46ad712a84e912f.
# These independent snapshot identities must survive together after integration.
EXPECTED_IDENTITIES = {
    "SRC-0271": (
        "https://forum.openvz.org/index.php?goto=20023&rev=19978%3A19977%3A19969%3A19972&t=msg&th=3866",
        (),
    ),
    "SRC-0272": (
        "https://lists.openvz.org/pipermail/devel/2007-September/041006.html",
        (),
    ),
    "SRC-0273": (
        "https://github.com/torvalds/linux/commit/5f256becd868bf63b70da8f2769033d6734670e9",
        (("git", "5f256becd868bf63b70da8f2769033d6734670e9"),),
    ),
    "SRC-0274": (
        "https://github.com/torvalds/linux/commit/9dd776b6d7b0b85966b6ddd03e2b2aae59012ab1",
        (("git", "9dd776b6d7b0b85966b6ddd03e2b2aae59012ab1"),),
    ),
    "SRC-0275": (
        "https://lists.openvz.org/pipermail/devel/2007-September/040800.html",
        (),
    ),
    "SRC-0276": (
        "https://github.com/torvalds/linux/commit/ce286d327341295f58d89864d746a524287cfdf9",
        (("git", "ce286d327341295f58d89864d746a524287cfdf9"),),
    ),
    # RFC 271 and RFC 331 share a title; their document identities do not.
    "SRC-0277": (
        "https://www.rfc-editor.org/rfc/rfc270.html",
        (("RFC", "270"),),
    ),
    "SRC-0278": (
        "https://www.rfc-editor.org/rfc/rfc271.html",
        (("RFC", "271"),),
    ),
    "SRC-0279": (
        "https://www.rfc-editor.org/rfc/rfc331.html",
        (("RFC", "331"),),
    ),
    "SRC-0280": (
        "https://lists.openwall.net/netdev/2007/06/06/30",
        (("Message-ID", "<4666CEAA.8010903@openvz.org>"),),
    ),
    "SRC-0281": (
        "https://lists.openwall.net/netdev/2007/06/06/35",
        (("Message-ID", "<4666D296.2000002@trash.net>"),),
    ),
    "SRC-0282": (
        "https://lists.openwall.net/netdev/2007/07/11/40",
        (("Message-ID", "<4694A363.2070406@openvz.org>"),),
    ),
    "SRC-0283": (
        "https://lists.openwall.net/netdev/2007/07/12/38",
        (("Message-ID", "<4695F0BF.1000305@openvz.org>"),),
    ),
    "SRC-0284": (
        "https://lists.openwall.net/netdev/2007/07/19/45",
        (("Message-ID", "<469F2DE7.9090407@openvz.org>"),),
    ),
    "SRC-0285": (
        "https://lists.openwall.net/netdev/2007/08/09/24",
        (("Message-ID", "<20070808.221827.05602119.davem@davemloft.net>"),),
    ),
    "SRC-0286": (
        "https://github.com/iproute2/iproute2/commit/e2613dc8605e56dbc53890ebbae263f93610bd41",
        (("git", "e2613dc8605e56dbc53890ebbae263f93610bd41"),),
    ),
    "SRC-0287": (
        "https://github.com/iproute2/iproute2/commit/0dc34c7713bb7055378fe5cbc720d63d0db572a1",
        (("git", "0dc34c7713bb7055378fe5cbc720d63d0db572a1"),),
    ),
    "SRC-0288": (
        "https://github.com/iproute2/iproute2/blob/v3.0.0/ip/ipnetns.c",
        (("git-tag", "v2.6.39"), ("git-tag", "v3.0.0")),
    ),
}


def load_source(source_id: str) -> dict:
    path = REPOSITORY_ROOT / "records" / "sources" / f"{source_id}.json"
    return json.loads(path.read_text(encoding="utf-8"))


class NetnsIntegrationIdentityTests(unittest.TestCase):
    def test_combined_sources_keep_their_original_document_identities(self) -> None:
        for source_id, (canonical_url, identifiers) in EXPECTED_IDENTITIES.items():
            with self.subTest(source_id=source_id):
                source = load_source(source_id)
                self.assertEqual(source_id, source["id"])
                self.assertEqual(canonical_url, source["access"]["canonical_url"])
                actual_identifiers = {
                    (item["scheme"], item["value"]) for item in source["identifiers"]
                }
                self.assertTrue(set(identifiers) <= actual_identifiers)

    def test_merged_ledger_preserves_veth_and_userspace_rows(self) -> None:
        with (REPOSITORY_ROOT / "data" / "source-ledger.csv").open(
            encoding="utf-8", newline=""
        ) as stream:
            rows = list(csv.DictReader(stream))
        counts = Counter(row["source_id"] for row in rows)
        by_id = {row["source_id"]: row for row in rows}
        # Kernel/RFC records are already valid JSON identities; promotion does
        # not require a duplicate discovery-ledger row. Both merged branches
        # contribute these nine veth/userspace rows, which must not be lost.
        ledger_ids = [f"SRC-{number:04d}" for number in range(280, 289)]
        for source_id in ledger_ids:
            canonical_url, identifiers = EXPECTED_IDENTITIES[source_id]
            with self.subTest(source_id=source_id):
                self.assertEqual(1, counts[source_id])
                row = by_id[source_id]
                source = load_source(source_id)
                self.assertEqual(canonical_url, row["canonical_url"])
                for field in ("title", "source_type"):
                    self.assertEqual(source[field], row[field])
                for _, value in identifiers:
                    # Identifier labels are free text; existing Message-IDs
                    # are bare values, while commits/tags have scheme labels.
                    self.assertIn(value, row["identifier"])


if __name__ == "__main__":
    unittest.main()
