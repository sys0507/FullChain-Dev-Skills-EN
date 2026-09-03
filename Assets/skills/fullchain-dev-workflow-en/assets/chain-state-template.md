# Full-Chain State

> Order, gates, and conditional criteria come from `docs/stage-artifact-contract.md`.
> This file records only “where we are, what was skipped, and why”; it **never records how to perform a stage**.

| Stage | Name | State | Skip reason |
|:---:|---|:---:|---|
| 0 | Toolchain setup | not-started | — |
| 1.1 | Project ledger | not-started | — |
| 1.2 | Project research | not-started | — |
| 1.3 | Adversarial selection | not-started | — |
| 2 | MVP convergence | not-started | — |
| 3 | Write PRD | not-started | — |
| 4 | Four-step documents | not-started | — |
| 5.1 | Interface design | not-started | — |
| 5.2 | Design injection | not-started | — |
| 6 | Project context | not-started | — |
| 7 | Runway setup | not-started | — |
| 8 | TDD implementation | not-started | — |
| 9.1 | Test routing | not-started | — |
| 9.2 | Execute tests | not-started | — |
| 9.3 | Finish Branch | not-started | — |
| 10 | Retrospective | not-started | — |
| 11 | Packaging/deployment | not-started | — |

**Four state values:** `not-started` / `completed` / `skipped` / `completed-without-skill`.

| Value | When to use it |
|---|---|
| `completed` | Normal execution using the stage Skill |
| `skipped` | A conditional stage was found not applicable |
| `completed-without-skill` | **The Skill was missing and the manual path was used**—the work was done without that Skill's constraints |

**The last two require a reason**—the script reports an empty reason as an inconsistency.

## Change Log

| Date | Stage | Change | Reason |
|---|:---:|---|---|
