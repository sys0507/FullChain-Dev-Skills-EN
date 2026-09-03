#!/usr/bin/env python3
"""Full-chain state machine: record position and compute the next step.

    python scripts/chain_state.py --root .            # show next step (read-only)
    python scripts/chain_state.py --root . --init     # create the state file

It knows only order, gates, and conditions. Each stage Skill owns how to perform its work;
restating that here would create a second source of truth that drifts from the contract matrix.

Read-only operations write no files. Looking at progress must not create a side effect.

The state file is Markdown rather than JSON because it is primarily for people. After days
away, a user should see immediately where work stopped and why stage 5 was skipped. Parsing
a table costs less than making the user read JSON.

Standard library only; runs on Windows and POSIX.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

STATE_PATH = "specs/research/chain-state.md"
STATUSES = ("not-started", "completed", "skipped", "completed-without-skill")

# The terminal state for a manual fallback. Validation E exposed that with three states it
# could only be recorded as completed; the degradation survived only in the change log,
# while people scan the table.


@dataclass(frozen=True)
class Stage:
    id: str
    name: str
    skill: str
    gate: str
    conditional: bool = False
    criteria: str = ""


# Order, gates, and criteria come from docs/stage-artifact-contract.md. This table is the
# fallback when the matrix is missing; the matrix wins on conflict.
STAGES: tuple[Stage, ...] = (
    Stage("0", "Toolchain setup", "fullchain-toolchain-setup-en", "None"),
    Stage("1.1", "Project ledger", "project-context-ledger-en", "Conditional trigger"),
    Stage("1.2", "Project research", "product-research-kickoff-universal-en", "End of stage"),
    Stage("1.3", "Adversarial selection", "adversarial-architecture-selection-universal-en", "End of stage",
          True, "at least two candidates after research convergence"),
    Stage("2", "MVP convergence", "mvp-convergence-brainstorming-en", "End of stage"),
    Stage("3", "Write PRD", "prd-writer-universal-en", "End of stage"),
    Stage("4", "Four-step documents", "speckit-feature-pipeline-en", "Each feature"),
    Stage("5.1", "Interface design", "platform-design-kickoff-en", "End of stage",
          True, "a graphical interface, interaction contract, or developer-experience design need"),
    Stage("5.2", "Design injection", "speckit-design-injection-universal-en", "Each feature",
          True, "stage 5.1 produced DESIGN.md"),
    Stage("6", "Project context", "claude-md-bootstrap-en", "End of stage"),
    Stage("7", "Runway setup", "implementation-runway-setup-en", "End of stage"),
    Stage("8", "TDD implementation", "run-feature-en", "Each feature"),
    Stage("9.1", "Test routing", "test-routing-advisor-en", "None"),
    Stage("9.2", "Execute tests", "routed by 9.1 to one of four executors", "End of stage"),
    Stage("9.3", "Finish Branch", "run-feature-en", "Each feature"),
    Stage("10", "Retrospective", "learnings-retrospective-en", "None"),
    Stage("11", "Packaging/deployment", "release-packaging-router-en", "End of stage",
          True, "the artifact must be handed to someone else or consumed by another project"),
)


@dataclass
class Entry:
    stage: Stage
    status: str = "not-started"
    reason: str = ""


@dataclass
class ChainState:
    entries: list[Entry] = field(default_factory=list)
    matrix_read: bool = False

    def problems(self) -> list[str]:
        """Report only; never auto-correct, because correction can hide a real problem."""
        out = []
        for entry in self.entries:
            if entry.status in ("skipped", "completed-without-skill") and not entry.reason.strip():
                out.append(f"Stage {entry.stage.id} is {entry.status} without a reason—"
                           f"every skip or degraded completion requires one")
            if entry.status not in STATUSES:
                out.append(f"Stage {entry.stage.id} has an invalid state: {entry.status!r}")
        return out


ROW = re.compile(r"^\|\s*([\d.]+)\s*\|[^|]*\|\s*(\S+)\s*\|\s*(.*?)\s*\|\s*$")


def load(root: Path) -> ChainState:
    """Load state. If absent, return all not-started and do not create a file."""
    state = ChainState(entries=[Entry(stage) for stage in STAGES])
    path = root / STATE_PATH
    if not path.is_file():
        return state
    by_id = {entry.stage.id: entry for entry in state.entries}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = ROW.match(line)
        if not match:
            continue
        stage_id, status, reason = match.group(1), match.group(2), match.group(3)
        if stage_id in by_id:
            by_id[stage_id].status = status
            by_id[stage_id].reason = reason.replace("—", "").strip()
    return state


def next_stage(state: ChainState) -> Stage | None:
    """Return the first unsettled stage; completed and skipped states are settled."""
    for entry in state.entries:
        if entry.status == "not-started":
            return entry.stage  # The other three states are terminal.
    return None


def render(state: ChainState) -> str:
    newline = chr(10)
    rows = [
        "# Full-Chain State",
        "",
        "> Order, gates, and conditional criteria come from `docs/stage-artifact-contract.md`.",
        "> This file records only where we are, what was skipped, and why; **never how to perform a stage**.",
        "",
        "| Stage | Name | State | Skip reason |",
        "|:---:|---|:---:|---|",
    ]
    for entry in state.entries:
        rows.append(f"| {entry.stage.id} | {entry.stage.name} | {entry.status} | "
                    f"{entry.reason if entry.reason else '—'} |")
    rows += ["", "## Change Log", "", "| Date | Stage | Change | Reason |",
             "|---|:---:|---|---|"]
    return newline.join(rows) + newline


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Full-chain state: show next step / initialize")
    parser.add_argument("--root", default=".")
    parser.add_argument("--init", action="store_true", help="create state file; skip if it exists")
    args = parser.parse_args(argv)
    root = Path(args.root)
    state = load(root)

    if args.init:
        path = root / STATE_PATH
        if path.is_file():
            print(f"Skipped: {STATE_PATH} already exists and was not changed")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(render(state), encoding="utf-8")
            print(f"Created {STATE_PATH}")
        return 0

    upcoming = next_stage(state)
    print("# Next Step")
    print()
    if upcoming is None:
        print("Every stage has a terminal state.")
    else:
        print(f"**Stage {upcoming.id} · {upcoming.name}**")
        print()
        print(f"- Invoke: `{upcoming.skill}`")
        print(f"- Gate: {upcoming.gate}")
        if upcoming.conditional:
            print(f"- **Conditional stage**; criterion: {upcoming.criteria}")
            print("- Give the criterion conclusion first, then **wait for user confirmation** before running or recording a skip")
    problems = state.problems()
    if problems:
        print()
        print("## Inconsistencies (Reported Only; Never Auto-corrected)")
        for problem in problems:
            print(f"- {problem}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
