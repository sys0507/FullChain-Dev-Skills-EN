#!/usr/bin/env python3
"""Full-chain toolchain installer - project-scoped install, hard language isolation.

Four layers, and the order is a **structural requirement** rather than a suggestion about
execution order:

    resolve_catalog()  take the catalogue for a language  - a lookup, never derived by name
    verify_language()  language verification              - pure function
    compare()          content comparison                 - pure function, three states
    install()          the write                          - always after compare's absent branch

The structural guarantee of hard language isolation: **this module contains no fallback path
to the other language catalogue at all**. When a source is missing it returns a failure; it
never consults the other table. That is the design, not a reminder.

Cross-platform: standard library and pathlib only.
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Two independent catalogues. The naming suffixes are inconsistent (the first four carry
# -universal), so deriving one from the other by concatenation gets those four wrong.
# It MUST be a lookup.
CATALOG: dict[str, list[str]] = {
    "zh": [
        "fullchain-dev-workflow",
        "project-context-ledger",
        "product-research-kickoff-universal",
        "adversarial-architecture-selection-universal",
        "mvp-convergence-brainstorming",
        "prd-writer-universal",
        "speckit-feature-pipeline",
        "platform-design-kickoff",
        "speckit-design-injection-universal",
        "claude-md-bootstrap",
        "implementation-runway-setup",
        "run-feature",
        "testing-system-blueprint",
        "test-routing-advisor",
        "backend-testing",
        "frontend-testing",
        "fullstack-slice-testing",
        "full-chain-testing",
        "learnings-retrospective",
        "release-packaging-router",
    ],
    "en": [
        "fullchain-dev-workflow-en",
        "project-context-ledger-en",
        "product-research-kickoff-universal-en",
        "adversarial-architecture-selection-universal-en",
        "mvp-convergence-brainstorming-en",
        "prd-writer-universal-en",
        "speckit-feature-pipeline-en",
        "platform-design-kickoff-en",
        "speckit-design-injection-universal-en",
        "claude-md-bootstrap-en",
        "implementation-runway-setup-en",
        "run-feature-en",
        "testing-system-blueprint-en",
        "test-routing-advisor-en",
        "backend-testing-en",
        "frontend-testing-en",
        "fullstack-slice-testing-en",
        "full-chain-testing-en",
        "learnings-retrospective-en",
        "release-packaging-router-en",
    ],
}


# -------------------------------------------------------------- catalogue

def resolve_catalog(lang: str, subset: list[str] | None = None) -> list[str]:
    """Look the catalogue up. lang MUST be passed explicitly - never inferred from the
    environment or the locale."""
    if lang not in CATALOG:
        raise ValueError(f"unknown language catalogue {lang!r}; valid values: {sorted(CATALOG)}")
    names = CATALOG[lang]
    if subset:
        unknown = [s for s in subset if s not in names]
        if unknown:
            raise ValueError(f"{unknown} is not in the {lang} catalogue")
        return [n for n in names if n in subset]
    return list(names)


# -------------------------------------------------------------- language verification

def read_lang(skill_dir: Path) -> str | None:
    """Read metadata.lang from the frontmatter of SKILL.md. Returns None when unreadable."""
    sp = skill_dir / "SKILL.md"
    if not sp.is_file():
        return None
    text = sp.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return None
    fm = text.split("---", 2)[1]
    for line in fm.splitlines():
        s = line.strip()
        if s.startswith("lang:"):
            return s.split(":", 1)[1].strip()
    return None


def verify_language(skill_dir: Path, requested: str) -> tuple[bool, str]:
    """Refuse to install when the language does not match the request. An unreadable lang
    field counts as a mismatch - better to refuse than to mix."""
    actual = read_lang(skill_dir)
    if actual is None:
        return False, "metadata.lang is not declared; the language cannot be confirmed, so installation is refused"
    if actual != requested:
        return False, f"language mismatch: requested {requested}, actual {actual}"
    return True, "ok"


# -------------------------------------------------------------- content comparison

def digest(path: Path) -> str:
    """A digest of the directory contents. Content, not a version number - version numbers
    may not be maintained."""
    h = hashlib.sha256()
    for f in sorted(p for p in path.rglob("*") if p.is_file()):
        h.update(f.relative_to(path).as_posix().encode())
        h.update(f.read_bytes())
    return h.hexdigest()


def compare(src: Path, dst: Path) -> str:
    """Three states: absent / same / different. A pure function; it writes nothing."""
    if not dst.exists():
        return "absent"
    return "same" if digest(src) == digest(dst) else "different"


# -------------------------------------------------------------- the write

def install(src: Path, dst: Path, project_root: Path) -> str:
    """Every write is called after compare returns absent.

    Scope check: the target MUST be inside the project directory, or it is refused - never
    write outside the project.
    """
    dst_res, root_res = dst.resolve(), project_root.resolve()
    if root_res not in dst_res.parents and dst_res != root_res:
        raise PermissionError(f"refusing to write outside the project: {dst_res}")
    shutil.copytree(src, dst)
    return "installed"


# -------------------------------------------------------------- orchestration

@dataclass
class Outcome:
    installed: list[str] = field(default_factory=list)
    skipped: list[tuple[str, str]] = field(default_factory=list)
    failed: list[tuple[str, str]] = field(default_factory=list)
    conflicts: list[tuple[str, str]] = field(default_factory=list)


def run(source: Path, project_root: Path, lang: str,
        subset: list[str] | None = None, dry_run: bool = False) -> Outcome:
    out = Outcome()
    target_root = project_root / ".claude" / "skills"
    for name in resolve_catalog(lang, subset):
        src = source / name
        if not src.is_dir():
            # Source missing - record a failure. There is **no** branch here leading to the
            # other language catalogue.
            out.failed.append((name, f"source does not exist: {src}"))
            continue
        ok, why = verify_language(src, lang)
        if not ok:
            out.failed.append((name, why))
            continue
        dst = target_root / name
        state = compare(src, dst)
        if state == "same":
            out.skipped.append((name, "already present with identical content"))
        elif state == "different":
            out.conflicts.append((name, "present but different: not overwritten, needs a human ruling"))
        else:
            if dry_run:
                out.installed.append(name + " (dry-run)")
            else:
                target_root.mkdir(parents=True, exist_ok=True)
                install(src, dst, project_root)
                out.installed.append(name)
    return out


def render(out: Outcome, lang: str, total: int) -> str:
    L = [f"# Toolchain install report (language catalogue: {lang})", ""]
    L.append(f"{total} in the catalogue: {len(out.installed)} installed, "
             f"{len(out.skipped)} skipped, {len(out.conflicts)} conflicting, "
             f"{len(out.failed)} failed")
    for title, items in (("## Installed", [(n, "") for n in out.installed]),
                         ("## Skipped", out.skipped),
                         ("## Conflicting (not overwritten)", out.conflicts),
                         ("## Failed", out.failed)):
        if items:
            L += ["", title]
            L += [f"- {n}{(' - ' + r) if r else ''}" for n, r in items]
    if out.failed:
        L += ["", "> No failure was substituted with the other language version - hard "
                  "language isolation forbids cross-language fallback."]
    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Full-chain toolchain installer (project-scoped)")
    ap.add_argument("--source", required=True,
                    help="the skill asset source directory (parameterised, never hardcoded)")
    ap.add_argument("--project-root", default=".", help="the target project root")
    ap.add_argument("--lang", required=True, choices=sorted(CATALOG),
                    help="the language catalogue; MUST be passed explicitly, never inferred "
                         "from the environment or the locale")
    ap.add_argument("--only", nargs="*", default=None,
                    help="install only the named ones (subset install)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    out = run(Path(args.source), Path(args.project_root), args.lang,
              args.only, args.dry_run)
    print(render(out, args.lang, len(resolve_catalog(args.lang, args.only))))
    return 1 if out.failed else 0


if __name__ == "__main__":
    sys.exit(main())
