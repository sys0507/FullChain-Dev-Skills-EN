"""Tests for runway_setup.

The primary case is idempotence: two runs are byte-identical and insert one block.

Fixtures are self-contained so repository evolution cannot change the result.
Cross-platform: pathlib and tempfile only.
"""
from __future__ import annotations

import sys
import tempfile
import unittest

NL = chr(10)
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from runway_setup import (  # noqa: E402
    DISCIPLINE_MARKER,
    apply_discipline,
    apply_feature_files,
    detect_discipline,
    detect_file,
    existing_local_configs,
    main,
    normalize,
)

BLOCK = """### Implementation Discipline (for downstream handoff)

- Before executing any tasks.md, ALWAYS read the project constitution FIRST.
- Always follow TDD: Red (failing test) -> Green (minimum code) -> Refactor.
"""

CONSTITUTION_WITH_VERSION = """# Demo Constitution

## Core Principles

### I. Something

Text.

**Version**: 1.0.0 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-01-01
"""

CONSTITUTION_NO_VERSION = """# Demo Constitution

## Core Principles

### I. Something

Text.
"""


class Fixture:
    """Build a minimal fixture independent of the real repository."""

    def __init__(self, constitution: str = CONSTITUTION_WITH_VERSION, features: int = 2):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / ".specify/memory").mkdir(parents=True)
        self.constitution = self.root / ".specify/memory/constitution.md"
        self.constitution.write_text(constitution, encoding="utf-8")
        self.features = []
        for i in range(1, features + 1):
            d = self.root / f"specs/{i:03d}-demo"
            d.mkdir(parents=True)
            (d / "tasks.md").write_text("- [ ] **T01** demo\n", encoding="utf-8")
            self.features.append(d)

    def close(self):
        self.tmp.cleanup()


# ---------------------------------------------------------------- idempotence (primary)

class TestIdempotence(unittest.TestCase):
    """The skill's primary acceptance criterion."""

    def setUp(self):
        self.fx = Fixture()
        self.addCleanup(self.fx.close)

    def test_discipline_inserted_once_then_skipped(self):
        text = self.fx.constitution.read_text(encoding="utf-8")
        self.assertEqual(detect_discipline(text, BLOCK), "absent")

        apply_discipline(self.fx.constitution, text, BLOCK)
        after_first = self.fx.constitution.read_text(encoding="utf-8")
        self.assertEqual(after_first.count(DISCIPLINE_MARKER), 1)

        # Second pass detects existing output and writes nothing.
        self.assertEqual(detect_discipline(after_first, BLOCK), "present_same")

    def test_rerun_produces_byte_identical_output(self):
        text = self.fx.constitution.read_text(encoding="utf-8")
        apply_discipline(self.fx.constitution, text, BLOCK)
        first = self.fx.constitution.read_bytes()

        # Simulate a full rerun: present_same means no write.
        again = self.fx.constitution.read_text(encoding="utf-8")
        if detect_discipline(again, BLOCK) == "absent":
            apply_discipline(self.fx.constitution, again, BLOCK)
        second = self.fx.constitution.read_bytes()

        self.assertEqual(first, second, "rerun output must be byte-identical")

    def test_feature_files_rerun_identical(self):
        tpl_p, tpl_h = "# progress <feature-name>\n", "# handoff <feature-name>\n"
        first = {}
        for d in self.fx.features:
            apply_feature_files(d, tpl_p, tpl_h)
            first[d.name] = (d / "state.md").read_bytes() + (d / "session.md").read_bytes()

        for d in self.fx.features:
            res = apply_feature_files(d, tpl_p, tpl_h)
            self.assertEqual(res["state.md"], "skipped_exists")
            self.assertEqual(res["session.md"], "skipped_exists")
            now = (d / "state.md").read_bytes() + (d / "session.md").read_bytes()
            self.assertEqual(first[d.name], now)


# ---------------------------------------------------------------- edge cases

class TestBoundaries(unittest.TestCase):

    def test_no_version_line_degrades_and_reports(self):
        fx = Fixture(constitution=CONSTITUTION_NO_VERSION)
        self.addCleanup(fx.close)
        text = fx.constitution.read_text(encoding="utf-8")
        outcome = apply_discipline(fx.constitution, text, BLOCK)
        self.assertEqual(outcome, "appended_at_end_position_degraded")
        self.assertEqual(fx.constitution.read_text(encoding="utf-8").count(DISCIPLINE_MARKER), 1)

    def test_version_line_stays_last(self):
        fx = Fixture()
        self.addCleanup(fx.close)
        text = fx.constitution.read_text(encoding="utf-8")
        apply_discipline(fx.constitution, text, BLOCK)
        lines = [l for l in fx.constitution.read_text(encoding="utf-8").splitlines() if l.strip()]
        self.assertTrue(lines[-1].startswith("**Version**:"), "version line must remain last")

    def test_present_but_different_is_detected_not_overwritten(self):
        fx = Fixture()
        self.addCleanup(fx.close)
        text = fx.constitution.read_text(encoding="utf-8")
        apply_discipline(fx.constitution, text, BLOCK)
        before = fx.constitution.read_bytes()

        changed_block = BLOCK + "\n- An extra rule the project added itself.\n"
        state = detect_discipline(fx.constitution.read_text(encoding="utf-8"), changed_block)
        self.assertEqual(state, "present_different")
        # A detected conflict must never be written over.
        self.assertEqual(fx.constitution.read_bytes(), before, "conflicting content must remain unchanged")

    def test_handwritten_file_preserved(self):
        fx = Fixture()
        self.addCleanup(fx.close)
        d = fx.features[0]
        handwritten = "# My handwritten progress\n\nDo not overwrite me\n"
        (d / "state.md").write_text(handwritten, encoding="utf-8")

        apply_feature_files(d, "# progress <feature-name>\n", "# handoff <feature-name>\n")
        self.assertEqual((d / "state.md").read_text(encoding="utf-8"), handwritten)

    def test_missing_candidates_are_not_created(self):
        fx = Fixture()
        self.addCleanup(fx.close)
        (fx.root / ".env").write_text("X=1\n", encoding="utf-8")
        present, missing = existing_local_configs(fx.root, [".env", ".env.local", ".credentials.yaml"])
        self.assertEqual(present, [".env"])
        self.assertEqual(missing, [".env.local", ".credentials.yaml"])
        for m in missing:
            self.assertFalse((fx.root / m).exists(), "missing credential files must not be created")


# ---------------------------------------------------------------- normalization

class TestNormalize(unittest.TestCase):
    """Semantically identical formatting must not be classified as different."""

    def test_emphasis_markers_ignored(self):
        self.assertEqual(normalize("**ALWAYS** read"), normalize("ALWAYS read"))

    def test_trailing_whitespace_and_blank_lines_ignored(self):
        self.assertEqual(normalize("a   \n\n\n\nb"), normalize("a\n\nb"))

    def test_genuinely_different_still_differs(self):
        """A real difference must remain different; normalization must be bounded."""
        self.assertNotEqual(normalize("read the constitution"), normalize("skip the constitution"))


# ---------------------------------------------------------------- CLI

class TestCli(unittest.TestCase):

    def test_no_constitution_skips_and_does_not_create(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "specs/001-demo").mkdir(parents=True)
            rc = main(["--root", str(root)])
            self.assertEqual(rc, 0)
            self.assertFalse((root / ".specify/memory/constitution.md").exists(),
                             "a missing constitution must not be fabricated")

    def test_dry_run_writes_nothing(self):
        fx = Fixture()
        self.addCleanup(fx.close)
        before = fx.constitution.read_bytes()
        block_file = fx.root / "block.md"
        block_file.write_text(BLOCK, encoding="utf-8")
        main(["--root", str(fx.root), "--block-file", str(block_file), "--dry-run"])
        self.assertEqual(fx.constitution.read_bytes(), before)




class TestBlockFileGuard(unittest.TestCase):
    """Reject an explanatory --block-file instead of injecting it verbatim.

    A real defect injected a 130-line explanatory file while reporting success because
    the actual block was fenced inside it. This fixture prevents that regression.
    """

    DOC = (
        "# Item C · Implementation Discipline" + NL + NL
        + "## 2. Discipline Block" + NL + NL
        + "```markdown" + NL + BLOCK + NL + "```" + NL + NL
        + "## 4. Idempotence Algorithm" + NL + NL
        + "### 4.1 Detection Marker" + NL + NL
        + "```" + NL + "### Implementation Discipline" + NL + "```" + NL
    )

    def test_extracts_block_from_fenced_doc(self):
        fx = Fixture()
        self.addCleanup(fx.close)
        doc = fx.root / "discipline-block.md"
        doc.write_text(self.DOC, encoding="utf-8")
        main(["--root", str(fx.root), "--block-file", str(doc)])
        got = fx.constitution.read_text(encoding="utf-8")
        self.assertNotIn("## 4. Idempotence Algorithm", got,
                         "explanatory meta-commentary must not enter the constitution")
        self.assertIn("Always follow TDD", got, "the actual block must be injected")

    def test_extracted_block_is_idempotent(self):
        fx = Fixture()
        self.addCleanup(fx.close)
        doc = fx.root / "discipline-block.md"
        doc.write_text(self.DOC, encoding="utf-8")
        main(["--root", str(fx.root), "--block-file", str(doc)])
        first = fx.constitution.read_bytes()
        main(["--root", str(fx.root), "--block-file", str(doc)])
        self.assertEqual(fx.constitution.read_bytes(), first,
                         "reruns must be byte-identical, not present_different")

    def test_rejects_file_without_marker(self):
        fx = Fixture()
        self.addCleanup(fx.close)
        before = fx.constitution.read_bytes()
        bad = fx.root / "not-a-block.md"
        bad.write_text("# An unrelated document" + NL + NL + "No discipline marker." + NL, encoding="utf-8")
        rc = main(["--root", str(fx.root), "--block-file", str(bad)])
        self.assertEqual(fx.constitution.read_bytes(), before,
                         "a markerless file must not be injected")
        self.assertEqual(rc, 0, "refusal is a normal result, not a crash")

    def test_plain_block_still_works(self):
        """A valid direct block must remain valid after the new guard."""
        fx = Fixture()
        self.addCleanup(fx.close)
        bf = fx.root / "block.md"
        bf.write_text(BLOCK, encoding="utf-8")
        main(["--root", str(fx.root), "--block-file", str(bf)])
        self.assertIn("Always follow TDD",
                      fx.constitution.read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main(verbosity=2)
