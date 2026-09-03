#!/usr/bin/env python3
"""Pre-implementation runway setup: deterministic parts of four sub-items.

The four layers are a structural requirement, not merely a suggested order:

    probe()   discovery          -- read-only; reports availability and reasons
    detect()  idempotence check  -- pure and read-only; returns three states
    apply()   writes             -- only after a negative detect result
    report()  reporting          -- gives a concrete reason for every skipped item

Cross-platform: standard library and pathlib only; identical Windows/POSIX behavior.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

DISCIPLINE_MARKER = "### Implementation Discipline"
VERSION_LINE = re.compile(r"^\*\*Version\*\*:", re.M)


# --------------------------------------------------------------------------
# probe -- discovery layer (read-only)
# --------------------------------------------------------------------------

@dataclass
class Probe:
    root: Path
    constitution: Path | None = None
    feature_dirs: list[Path] = field(default_factory=list)
    ignore_file: Path | None = None
    notes: list[str] = field(default_factory=list)

    @classmethod
    def run(cls, root: Path, constitution: str | None, specs_glob: str) -> "Probe":
        p = cls(root=root)

        cand = root / constitution if constitution else root / ".specify/memory/constitution.md"
        if cand.is_file():
            p.constitution = cand
        else:
            p.notes.append(f"Constitution not found (looked at {cand.relative_to(root) if cand.is_relative_to(root) else cand})")

        p.feature_dirs = sorted(d for d in root.glob(specs_glob) if d.is_dir())
        if not p.feature_dirs:
            p.notes.append(f"No feature directory found (pattern: {specs_glob})")

        gi = root / ".gitignore"
        if gi.is_file():
            p.ignore_file = gi
        else:
            p.notes.append("No ignore-rules file found")
        return p


# --------------------------------------------------------------------------
# detect -- idempotence layer (pure and read-only)
# --------------------------------------------------------------------------

def normalize(text: str) -> str:
    """Normalize before comparison: remove inline emphasis and collapse whitespace.

    Byte comparison would misclassify semantically identical formatting as a conflict.
    """
    text = re.sub(r"[*`_]", "", text)
    text = re.sub(r"[ \t]+$", "", text, flags=re.M)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_block(raw: str) -> tuple[str, str]:
    """Extract the actual discipline block. Return (block, refusal reason).

    `references/discipline-block.md` is explanatory; the real block is fenced inside it.
    Injecting the whole document would put meta-commentary into the constitution.
    """
    body = raw.strip()
    if DISCIPLINE_MARKER not in body:
        return "", "the file has no discipline marker and may be the wrong file"
    if body.startswith(DISCIPLINE_MARKER):
        return body, ""
    lines = raw.splitlines()
    fences = [i for i, line in enumerate(lines) if line.startswith("```")]
    for opening, closing in zip(fences[0::2], fences[1::2]):
        chunk = lines[opening + 1:closing]
        if chunk and chunk[0].startswith(DISCIPLINE_MARKER):
            return "\n".join(chunk).strip(), ""
    return "", "the file looks explanatory and has no fenced block beginning with the marker"


def detect_discipline(constitution_text: str, block: str) -> str:
    """Return one of absent / present_same / present_different.

    Match the heading prefix only; a project may customize the qualifier in parentheses.
    """
    if DISCIPLINE_MARKER not in constitution_text:
        return "absent"
    start = constitution_text.index(DISCIPLINE_MARKER)
    tail = constitution_text[start:]
    end = tail.find("\n## ")
    existing = tail if end == -1 else tail[:end]
    vm = VERSION_LINE.search(existing)
    if vm:
        existing = existing[: vm.start()]
    return "present_same" if normalize(existing) == normalize(block) else "present_different"


def detect_file(path: Path) -> str:
    """Return absent/present for progress and handoff files."""
    return "present" if path.is_file() else "absent"


def existing_local_configs(root: Path, candidates: list[str]) -> tuple[list[str], list[str]]:
    """Return (existing, missing). Never create a missing credential file."""
    present, missing = [], []
    for c in candidates:
        (present if (root / c).is_file() else missing).append(c)
    return present, missing


# --------------------------------------------------------------------------
# apply -- write layer (only after a negative detect result)
# --------------------------------------------------------------------------

def apply_discipline(path: Path, text: str, block: str) -> str:
    """Insert before version metadata; otherwise append and report degraded placement."""
    vm = VERSION_LINE.search(text)
    if vm:
        new = text[: vm.start()] + block.rstrip() + "\n\n" + text[vm.start():]
        path.write_text(new, encoding="utf-8")
        return "inserted_before_version"
    new = text.rstrip() + "\n\n" + block.rstrip() + "\n"
    path.write_text(new, encoding="utf-8")
    return "appended_at_end_position_degraded"


def apply_feature_files(feature_dir: Path, progress_tpl: str, handoff_tpl: str) -> dict[str, str]:
    """Skip existing files; never overwrite potentially handwritten content."""
    out = {}
    for fname, tpl in (("state.md", progress_tpl), ("session.md", handoff_tpl)):
        target = feature_dir / fname
        if detect_file(target) == "present":
            out[fname] = "skipped_exists"
            continue
        target.write_text(tpl.replace("<feature-name>", feature_dir.name), encoding="utf-8")
        out[fname] = "created"
    return out


def apply_include_list(root: Path, present: list[str], missing: list[str], header: str) -> str:
    lines = [header.rstrip(), ""]
    lines.extend(present)
    if missing:
        lines += ["", "# --- These candidates do not exist and remain commented out. Before enabling, confirm each exists and is ignored. ---"]
        lines += [f"# {m}" for m in missing]
    (root / ".worktreeinclude").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return "written"


# --------------------------------------------------------------------------
# report
# --------------------------------------------------------------------------

def report(results: dict[str, object], notes: list[str]) -> str:
    out = ["# Pre-implementation Runway Setup Report", ""]
    for sub, val in results.items():
        out.append(f"## {sub}")
        out.append(f"{val}")
        out.append("")
    if notes:
        out.append("## Skipped Items and Reasons")
        out.extend(f"- {n}" for n in notes)
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Pre-implementation runway setup (deterministic portion)")
    ap.add_argument("--root", default=".", help="project root")
    ap.add_argument("--constitution", default=None, help="relative path to the constitution")
    ap.add_argument("--specs-glob", default="specs/[0-9][0-9][0-9]-*", help="feature-directory glob")
    ap.add_argument("--block-file", default=None, help="discipline-block file; omit to skip item C")
    ap.add_argument("--progress-template", default=None)
    ap.add_argument("--handoff-template", default=None)
    ap.add_argument("--dry-run", action="store_true", help="detect only; do not write")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    p = Probe.run(root, args.constitution, args.specs_glob)
    results: dict[str, object] = {}

    # Item C
    if args.block_file and p.constitution:
        block, refusal = extract_block(Path(args.block_file).read_text(encoding="utf-8"))
        text = p.constitution.read_text(encoding="utf-8")
        state = detect_discipline(text, block) if block else "rejected"
        if state == "rejected":
            results["C discipline block"] = "rejected_not_a_block"
            p.notes.append(f"Item C skipped: {refusal}; constitution unchanged")
        elif state == "absent":
            results["C discipline block"] = "would_insert" if args.dry_run else apply_discipline(p.constitution, text, block)
        elif state == "present_same":
            results["C discipline block"] = "skipped_already_present"
        else:
            results["C discipline block"] = "conflict_present_but_different__not_modified"
            p.notes.append("Discipline block exists with different content: not rewritten; human ruling required")
    else:
        p.notes.append("Item C skipped: no constitution or block file (a constitution was not fabricated)")

    # Item D
    if p.feature_dirs and args.progress_template and args.handoff_template:
        ptpl = Path(args.progress_template).read_text(encoding="utf-8")
        htpl = Path(args.handoff_template).read_text(encoding="utf-8")
        d = {}
        for fd in p.feature_dirs:
            d[fd.name] = ("dry_run" if args.dry_run
                          else apply_feature_files(fd, ptpl, htpl))
        results["D progress and handoff files"] = d
    else:
        p.notes.append("Item D skipped: no feature directory or templates")

    print(report(results, p.notes))
    return 0


if __name__ == "__main__":
    sys.exit(main())
