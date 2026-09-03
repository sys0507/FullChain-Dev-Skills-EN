"""Script tests for toolchain_setup.

The primary case is hard language isolation: when the Chinese version is missing, the
English version MUST NOT be installed in its place.
After that come idempotence and scope.

Every class carries a negative sample (a case that MUST NOT be reported), without which a
real defect cannot be told apart from a broken checker.
The fixtures are self-built and do not depend on the real repository state.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from toolchain_setup import (  # noqa: E402
    CATALOG,
    compare,
    digest,
    install,
    read_lang,
    render,
    resolve_catalog,
    run,
    verify_language,
)


def make_skill(root: Path, name: str, lang: str | None = "zh", body: str = "content") -> Path:
    d = root / name
    d.mkdir(parents=True)
    fm = "---\nname: %s\n" % name
    if lang is not None:
        fm += "metadata:\n  lang: %s\n" % lang
    fm += "---\n\n# %s\n\n%s\n" % (name, body)
    (d / "SKILL.md").write_text(fm, encoding="utf-8")
    return d


class Fixture:
    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.source = self.base / "assets"
        self.source.mkdir()
        self.project = self.base / "project"
        self.project.mkdir()

    def close(self):
        self.tmp.cleanup()


# ------------------------------------------------ hard language isolation (primary)

class TestLanguageIsolation(unittest.TestCase):

    def setUp(self):
        self.fx = Fixture()
        self.addCleanup(self.fx.close)

    def test_missing_zh_never_substitutes_en(self):
        """This skill primary acceptance: with the Chinese version missing, the English
        version MUST NOT be installed in its place."""
        # the source contains only the English version
        make_skill(self.fx.source, "run-feature-en", lang="en")
        out = run(self.fx.source, self.fx.project, "zh", subset=["run-feature"])

        self.assertEqual(out.installed, [], "nothing may be installed when the Chinese version is missing")
        self.assertEqual(len(out.failed), 1)
        self.assertIn("source does not exist", out.failed[0][1])
        # the point: the English version IS in the source, and was still not installed
        self.assertFalse((self.fx.project / ".claude/skills/run-feature-en").exists())
        self.assertFalse((self.fx.project / ".claude/skills/run-feature").exists())

    def test_language_mismatch_refuses(self):
        """Right directory name, wrong metadata.lang - refuse to install."""
        make_skill(self.fx.source, "run-feature", lang="en")
        out = run(self.fx.source, self.fx.project, "zh", subset=["run-feature"])
        self.assertEqual(out.installed, [])
        self.assertIn("language mismatch", out.failed[0][1])

    def test_missing_lang_field_refuses(self):
        """With no readable lang, refuse rather than mix."""
        make_skill(self.fx.source, "run-feature", lang=None)
        ok, why = verify_language(self.fx.source / "run-feature", "zh")
        self.assertFalse(ok)
        self.assertIn("not declared", why)

    def test_no_fallback_path_exists_in_catalog(self):
        """Structural guarantee: two independent tables, zh and en disjoint, with no
        derivation by concatenation."""
        self.assertEqual(set(CATALOG["zh"]) & set(CATALOG["en"]), set())
        for zh in CATALOG["zh"]:
            self.assertNotIn(zh + "-en", CATALOG["zh"])

    def test_catalog_requires_explicit_lang(self):
        with self.assertRaises(ValueError):
            resolve_catalog("de")

    # ---- negative sample: a matching language MUST install successfully ----
    def test_matching_language_installs(self):
        make_skill(self.fx.source, "run-feature", lang="zh")
        out = run(self.fx.source, self.fx.project, "zh", subset=["run-feature"])
        self.assertEqual(out.installed, ["run-feature"])
        self.assertEqual(out.failed, [])


# ------------------------------------------------ idempotence

class TestIdempotence(unittest.TestCase):

    def setUp(self):
        self.fx = Fixture()
        self.addCleanup(self.fx.close)
        make_skill(self.fx.source, "run-feature", lang="zh")

    def test_second_run_skips_not_overwrites(self):
        run(self.fx.source, self.fx.project, "zh", subset=["run-feature"])
        first = digest(self.fx.project / ".claude/skills/run-feature")

        out = run(self.fx.source, self.fx.project, "zh", subset=["run-feature"])
        self.assertEqual(out.installed, [])
        self.assertEqual(len(out.skipped), 1)
        second = digest(self.fx.project / ".claude/skills/run-feature")
        self.assertEqual(first, second, "a rerun MUST leave the content byte-identical")

    def test_different_content_is_conflict_not_overwrite(self):
        run(self.fx.source, self.fx.project, "zh", subset=["run-feature"])
        dst = self.fx.project / ".claude/skills/run-feature/SKILL.md"
        customised = dst.read_text(encoding="utf-8") + "\na paragraph the user added themselves\n"
        dst.write_text(customised, encoding="utf-8")

        out = run(self.fx.source, self.fx.project, "zh", subset=["run-feature"])
        self.assertEqual(out.installed, [])
        self.assertEqual(len(out.conflicts), 1)
        self.assertEqual(dst.read_text(encoding="utf-8"), customised,
                         "a user customisation MUST NOT be overwritten when content differs")

    def test_compare_three_states(self):
        src = self.fx.source / "run-feature"
        dst = self.fx.project / ".claude/skills/run-feature"
        self.assertEqual(compare(src, dst), "absent")
        run(self.fx.source, self.fx.project, "zh", subset=["run-feature"])
        self.assertEqual(compare(src, dst), "same")
        (dst / "SKILL.md").write_text("changed", encoding="utf-8")
        self.assertEqual(compare(src, dst), "different")


# ------------------------------------------------ scope

class TestScope(unittest.TestCase):

    def setUp(self):
        self.fx = Fixture()
        self.addCleanup(self.fx.close)

    def test_writes_only_inside_project(self):
        make_skill(self.fx.source, "run-feature", lang="zh")
        run(self.fx.source, self.fx.project, "zh", subset=["run-feature"])
        # nothing new appears outside the project
        outside = [p for p in self.fx.base.iterdir() if p.name not in ("assets", "project")]
        self.assertEqual(outside, [])

    def test_install_refuses_outside_project(self):
        make_skill(self.fx.source, "run-feature", lang="zh")
        with self.assertRaises(PermissionError):
            install(self.fx.source / "run-feature",
                    self.fx.base / "elsewhere" / "run-feature",
                    self.fx.project)


# ------------------------------------------------ subsets and the report

class TestSubsetAndReport(unittest.TestCase):

    def setUp(self):
        self.fx = Fixture()
        self.addCleanup(self.fx.close)
        for n in ("prd-writer-universal", "run-feature", "backend-testing"):
            make_skill(self.fx.source, n, lang="zh")

    def test_subset_install_allowed(self):
        """Wanting only two skills is a legitimate use and MUST NOT be refused as incomplete."""
        out = run(self.fx.source, self.fx.project, "zh",
                  subset=["prd-writer-universal", "run-feature"])
        self.assertEqual(sorted(out.installed), ["prd-writer-universal", "run-feature"])
        self.assertFalse((self.fx.project / ".claude/skills/backend-testing").exists())

    def test_unknown_subset_name_rejected(self):
        with self.assertRaises(ValueError):
            resolve_catalog("zh", ["no-such-skill"])

    def test_report_mentions_no_cross_language_fallback(self):
        out = run(self.fx.source, self.fx.project, "zh", subset=["prd-writer-universal"])
        out.failed.append(("x", "source does not exist"))
        text = render(out, "zh", 1)
        self.assertIn("hard language isolation forbids cross-language fallback", text)

    def test_report_counts_every_item(self):
        """The report MUST NOT silently omit any item."""
        out = run(self.fx.source, self.fx.project, "zh")
        total = len(resolve_catalog("zh"))
        text = render(out, "zh", total)
        counted = len(out.installed) + len(out.skipped) + len(out.conflicts) + len(out.failed)
        self.assertEqual(counted, total, "every item MUST be accounted for and none may vanish")
        self.assertIn(f"{total} in the catalogue", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
