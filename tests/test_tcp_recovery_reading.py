"""Consistency checks for the article's authored paper trace, not a TCP stack.

These tests check the printed ACK arithmetic and the corrected diagram. They
do not authenticate RFC claims or simulate congestion windows and timers.
"""

import re
import unittest
from pathlib import Path


ARTICLE = Path(__file__).resolve().parents[1] / "docs/tcp/tcp-tahoe-reno-newreno-sack-recovery.md"


def read_walk(text):
    match = re.search(r"<!-- ack-walk:start -->(.*?)<!-- ack-walk:end -->", text, re.S)
    if match is None:
        raise ValueError("missing ACK walkthrough table")
    rows = [
        tuple(map(int, row))
        for row in re.findall(r"^\| (\d+) \| (\d+) \| \[(\d+),(\d+)\) \| (\d+) \|$", match[1], re.M)
    ]
    if len(rows) != 6:
        raise ValueError("the paper trace must have six arrivals")
    return rows


def check_ack_arithmetic(rows):
    """Check only the contiguous prefix of the six printed byte intervals."""
    received = set()
    next_segment = 1
    for arrival, segment, start, end, ack in rows:
        if arrival != len(received) + 1 or segment in received:
            raise ValueError("unexpected repeated or out-of-order arrival index")
        if not 1 <= segment <= 6 or (start, end) != (segment * 1000, (segment + 1) * 1000):
            raise ValueError("byte interval disagrees with the segment label")
        received.add(segment)
        while next_segment in received:
            next_segment += 1
        if ack != next_segment * 1000:
            raise ValueError("ACK does not name the next byte after the received prefix")


class TCPRecoveryReadingTests(unittest.TestCase):
    def setUp(self):
        self.text = ARTICLE.read_text(encoding="utf-8")

    def test_reno_graph_exits_on_advancing_ack(self):
        section = self.text.split("## 3. Reno:", 1)[1].split("## 4.", 1)[0]
        graph = re.search(r"```text\n(.*?)\n```", section, re.S)[1]
        self.assertIn("ACK acknowledging previously unacknowledged data", graph)
        self.assertNotIn("covering recover point", graph)

    def test_documented_walk_acknowledges_only_the_contiguous_prefix(self):
        rows = read_walk(self.text)
        check_ack_arithmetic(rows)
        self.assertEqual([row[1] for row in rows], [1, 3, 5, 6, 2, 4])
        self.assertEqual([row[4] for row in rows], [2000, 2000, 2000, 2000, 4000, 7000])
        self.assertEqual(rows[4][4] - rows[3][4], 2000)

    def test_full_ack_covers_the_inclusive_recover_boundary(self):
        rows = read_walk(self.text)
        recover = int(re.search(r"`recover = (\d+)`", self.text)[1])
        self.assertEqual(recover, max(row[3] for row in rows) - 1)
        self.assertLess(rows[4][4] - 1, recover)  # ACK 4000 is partial.
        self.assertEqual(rows[5][4] - 1, recover)  # ACK 7000 is already full.

    def test_ack_beyond_a_hole_is_rejected(self):
        rows = read_walk(self.text)
        arrival, segment, start, end, _ = rows[4]
        rows[4] = (arrival, segment, start, end, 5000)
        with self.assertRaisesRegex(ValueError, "received prefix"):
            check_ack_arithmetic(rows)

    def test_segment_interval_mismatch_is_rejected(self):
        rows = read_walk(self.text)
        arrival, segment, start, end, ack = rows[1]
        rows[1] = (arrival, segment, start + 1, end, ack)
        with self.assertRaisesRegex(ValueError, "byte interval"):
            check_ack_arithmetic(rows)


if __name__ == "__main__":
    unittest.main()
