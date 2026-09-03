"""Tests for the orchestrator state machine.

The three most important properties are:
1. Read-only operations do not write files; checking progress must not pollute state.
2. State/artifact disagreement is reported, never auto-corrected; correction can hide real problems.
3. Completed stages are not rerun.

Each assertion type includes a negative sample.
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from chain_state import STAGES, ChainState, load, next_stage, render  # noqa: E402

NL = chr(10)


class Tmp:
    def __init__(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def close(self):
        self.temp.cleanup()


class TestBootstrap(unittest.TestCase):
    def test_empty_project_starts_at_first_stage(self):      # AC-013-1
        fixture = Tmp(); self.addCleanup(fixture.close)
        state = load(fixture.root)
        self.assertEqual(next_stage(state).id, STAGES[0].id)
        self.assertTrue(all(entry.status == "not-started" for entry in state.entries))

    def test_load_does_not_create_file(self):                # AC-013-7
        """Read-only means no write; merely checking progress has no side effect."""
        fixture = Tmp(); self.addCleanup(fixture.close)
        load(fixture.root)
        self.assertFalse((fixture.root / "specs/research/chain-state.md").exists())


class TestProgress(unittest.TestCase):
    def test_completed_stages_are_not_rerun(self):           # AC-013-2
        fixture = Tmp(); self.addCleanup(fixture.close)
        state = load(fixture.root)
        for entry in state.entries[:5]:
            entry.status = "completed"
        self.assertEqual(next_stage(state).id, STAGES[5].id)

    def test_skipped_counts_as_settled(self):
        """A skip is terminal and must not reappear as pending work."""
        fixture = Tmp(); self.addCleanup(fixture.close)
        state = load(fixture.root)
        state.entries[0].status = "completed"
        state.entries[1].status = "skipped"
        state.entries[1].reason = "fewer than two candidates"
        self.assertEqual(next_stage(state).id, STAGES[2].id)

    def test_all_settled_returns_none(self):                 # AC-013-10
        fixture = Tmp(); self.addCleanup(fixture.close)
        state = load(fixture.root)
        for entry in state.entries:
            entry.status = "completed"
        self.assertIsNone(next_stage(state))


class TestSkipRequiresReason(unittest.TestCase):
    def test_skip_without_reason_is_a_problem(self):         # AC-013-6
        fixture = Tmp(); self.addCleanup(fixture.close)
        state = load(fixture.root)
        state.entries[0].status = "skipped"
        self.assertTrue(state.problems(), "a reasonless skip must be reported")

    def test_skip_with_reason_is_clean(self):
        """Negative sample: a skip with a reason must remain clean."""
        fixture = Tmp(); self.addCleanup(fixture.close)
        state = load(fixture.root)
        state.entries[0].status = "skipped"
        state.entries[0].reason = "CLI has no graphical interface"
        self.assertEqual(state.problems(), [])


class TestRoundTrip(unittest.TestCase):
    def test_render_then_load_is_stable(self):               # AC-013-7
        fixture = Tmp(); self.addCleanup(fixture.close)
        state = load(fixture.root)
        state.entries[0].status = "completed"
        state.entries[3].status = "skipped"
        state.entries[3].reason = "no graphical interface"
        path = fixture.root / "specs/research/chain-state.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render(state), encoding="utf-8")
        again = load(fixture.root)
        self.assertEqual(render(again), render(state),
                         "rendering and loading must remain byte-stable across reruns")

    def test_reason_survives_round_trip(self):
        fixture = Tmp(); self.addCleanup(fixture.close)
        state = load(fixture.root)
        state.entries[2].status = "skipped"
        state.entries[2].reason = "fewer than two candidates; nothing to compare"
        path = fixture.root / "specs/research/chain-state.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render(state), encoding="utf-8")
        self.assertIn("nothing to compare", load(fixture.root).entries[2].reason)


class TestStageTableIntegrity(unittest.TestCase):
    def test_stage_ids_are_unique(self):
        self.assertEqual(len(STAGES), len({stage.id for stage in STAGES}))

    def test_every_stage_names_a_skill_or_says_none(self):
        """Every stage names a Skill or explicitly says none; no blank owner."""
        for stage in STAGES:
            self.assertTrue(stage.skill, f"stage {stage.id} has no Skill or explicit none")

    def test_conditional_stages_carry_criteria(self):        # AC-013-4
        conditional = [stage for stage in STAGES if stage.conditional]
        self.assertTrue(conditional, "at least one conditional stage must exist")
        for stage in conditional:
            self.assertTrue(stage.criteria, f"conditional stage {stage.id} lacks criteria")

    def test_non_conditional_have_no_criteria(self):
        """Negative sample: unconditional stages must not force criterion checks."""
        for stage in STAGES:
            if not stage.conditional:
                self.assertFalse(stage.criteria)


class TestDegradedCompletion(unittest.TestCase):
    """A manual fallback's terminal state must be visible in the table.

    Validation E exposed a missing stage-7 Skill whose manual fallback was honestly reported,
    but a three-state table could record only completed. People scan the table, not the change
    log. Three states were insufficient.
    """

    def _state(self):
        fixture = Tmp(); self.addCleanup(fixture.close)
        return load(fixture.root)

    def test_degraded_status_is_valid(self):
        state = self._state()
        state.entries[0].status = "completed-without-skill"
        state.entries[0].reason = "implementation-runway-setup-en missing; used manual path"
        self.assertEqual(state.problems(), [], "a legitimate degraded terminal state must be valid")

    def test_degraded_without_reason_is_flagged(self):
        """Like a skip, degradation without a reason is unexplained."""
        state = self._state()
        state.entries[0].status = "completed-without-skill"
        self.assertTrue(state.problems())

    def test_degraded_counts_as_settled(self):
        state = self._state()
        state.entries[0].status = "completed-without-skill"
        state.entries[0].reason = "Skill not installed"
        self.assertEqual(next_stage(state).id, STAGES[1].id,
                         "degraded completion is terminal, not pending work")

    def test_degraded_survives_round_trip(self):
        fixture = Tmp(); self.addCleanup(fixture.close)
        state = load(fixture.root)
        state.entries[10].status = "completed-without-skill"
        state.entries[10].reason = "runway Skill not installed"
        path = fixture.root / "specs/research/chain-state.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render(state), encoding="utf-8")
        back = load(fixture.root)
        self.assertEqual(back.entries[10].status, "completed-without-skill")
        self.assertIn("not installed", back.entries[10].reason)

    def test_plain_completion_still_needs_no_reason(self):
        """Negative sample: normal completion needs no reason."""
        state = self._state()
        state.entries[0].status = "completed"
        self.assertEqual(state.problems(), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
