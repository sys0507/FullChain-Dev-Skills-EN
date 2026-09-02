"""Tests for `scripts/`. The weight is on the anti-fabrication gate, not on coverage.

These scripts claim that every edge carries provenance, that an edge with no evidence to
point at stays a candidate, and that nothing is ever pretended to be confirmed. Once that
gate fails, the whole path inventory becomes a convincing-looking fake graph, which is
more dangerous than no graph. So the tests go there first rather than covering every
function evenly.

Every class of assertion has a negative sample: valid input MUST NOT be flagged.
In this project the checkers have a higher false-positive rate than the subjects have
defects, so with positive samples alone an all-green run proves nothing.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import pathinv  # noqa: E402
from knife4_merge import merge_edges  # noqa: E402


def edge(eid, frm="a", to="b", status="candidate", prov=None, source="spec"):
    return {"id": eid, "from": frm, "to": to, "type": "http",
            "source": source, "status": status,
            "provenance": {"file": "x.py", "line": 1} if prov is None else prov}


def inv(edges, nodes=("a", "b")):
    return {"nodes": [{"id": n} for n in nodes], "edges": edges}


class TestAntiFabricationGate(unittest.TestCase):
    """validate() is the anti-fabrication gate. Whatever it lets through is what the
    system is asserting counts as evidenced."""

    def test_valid_inventory_passes(self):
        """Negative sample: a graph with complete evidence MUST NOT be blocked."""
        self.assertEqual(pathinv.validate(inv([edge("e1")])), [])

    def test_edge_without_provenance_is_rejected(self):
        problems = pathinv.validate(inv([edge("e1", prov={})]))
        self.assertTrue(any("provenance" in p for p in problems))

    def test_provenance_needs_both_file_and_line(self):
        """A file name with no line number points at no specific place - not evidence."""
        problems = pathinv.validate(inv([edge("e1", prov={"file": "x.py"})]))
        self.assertTrue(any("provenance" in p for p in problems),
                        "provenance missing a line number was treated as valid evidence")

    def test_trace_provenance_accepted(self):
        """Negative sample: a trace source evidenced by span or event is equally valid."""
        self.assertEqual(
            pathinv.validate(inv([edge("e1", prov={"span": "s-1"})])), [])

    def test_dangling_endpoint_is_rejected(self):
        """An edge pointing at a non-existent node - the graph is broken, not connected."""
        problems = pathinv.validate(inv([edge("e1", to="ghost")]))
        self.assertTrue(any("no node" in p for p in problems))

    def test_bad_status_is_rejected(self):
        problems = pathinv.validate(inv([edge("e1", status="confirmed-ish")]))
        self.assertTrue(any("bad status" in p for p in problems))


class TestStatusMonotonicity(unittest.TestCase):
    """Status may only rise. A downgrade quietly turns a confirmed edge back into a guess."""

    def test_trace_beats_code_beats_candidate(self):
        self.assertEqual(pathinv.higher_status("trace-confirmed", "code-confirmed"),
                         "trace-confirmed")
        self.assertEqual(pathinv.higher_status("code-confirmed", "candidate"),
                         "code-confirmed")

    def test_order_does_not_matter(self):
        self.assertEqual(pathinv.higher_status("candidate", "trace-confirmed"),
                         pathinv.higher_status("trace-confirmed", "candidate"))

    def test_unknown_status_never_wins(self):
        self.assertEqual(pathinv.higher_status("candidate", "made-up"), "candidate")


class TestEdgeIdentity(unittest.TestCase):
    def test_same_triple_same_id(self):
        self.assertEqual(pathinv.edge_id("a", "b", "http"),
                         pathinv.edge_id("a", "b", "http"))

    def test_direction_matters(self):
        """A->B and B->A are two edges. Conflating them on merge invents bidirectional
        connectivity out of nothing."""
        self.assertNotEqual(pathinv.edge_id("a", "b", "http"),
                            pathinv.edge_id("b", "a", "http"))

    def test_type_matters(self):
        self.assertNotEqual(pathinv.edge_id("a", "b", "http"),
                            pathinv.edge_id("a", "b", "cron"))


class TestMergeUpgradesOnly(unittest.TestCase):
    """Three-source merge: an edge hit by several sources takes the strongest status, and
    MUST NOT be downgraded."""

    def test_code_upgrades_candidate(self):
        merged, _ = merge_edges([
            {"edges": [edge("a--http-->b", status="candidate", source="spec")]},
            {"edges": [edge("a--http-->b", status="code-confirmed", source="code",
                            prov={"file": "s.py", "line": 9})]},
        ])
        self.assertEqual(len(merged), 1, "the same edge MUST NOT appear twice")
        self.assertEqual(list(merged.values())[0]["status"], "code-confirmed")

    def test_weaker_source_does_not_downgrade(self):
        """Reverse order: strong then weak, and the result MUST still be the strong one."""
        merged, _ = merge_edges([
            {"edges": [edge("a--http-->b", status="trace-confirmed", source="trace",
                            prov={"span": "s1"})]},
            {"edges": [edge("a--http-->b", status="candidate", source="spec")]},
        ])
        self.assertEqual(list(merged.values())[0]["status"], "trace-confirmed",
                         "a weaker source downgraded a confirmed edge back to a guess")

    def test_distinct_edges_are_kept(self):
        """Negative sample: distinct edges MUST NOT be merged away."""
        merged, _ = merge_edges([
            {"edges": [edge("a--http-->b"), edge("b--cron-->c", frm="b", to="c")]},
        ])
        self.assertEqual(len(merged), 2)


class TestScriptsImportable(unittest.TestCase):
    """Smoke: every script must import.

    A script that fails on import cannot even print its help, and these are handed to
    users to actually run.
    """

    MODULES = ["pathinv", "knife1_spec", "knife2_static", "knife3_trace",
               "knife4_merge", "knife4b_narrate", "knife5_e2e"]

    def test_all_modules_import(self):
        import importlib
        for m in self.MODULES:
            with self.subTest(module=m):
                importlib.import_module(m)


if __name__ == "__main__":
    unittest.main(verbosity=2)
