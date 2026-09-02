# Release Go/No-Go Gate (Mechanical Gate, Complete Checklist)

> This document expands SKILL.md §V. Stack-agnostic, project-agnostic.
> Key boundary: **the blueprint provides the release standard; it does not enforce it for you — enforcement MUST rely on CI / hook / pre-commit.**

## What a Gate Is

A release gate is a set of **mechanically decidable** criteria applied before merge / release. "Mechanical" means every item can be answered "pass / fail" automatically by a script, without relying on an on-the-spot human judgment. Any single item failing means **no-go**.

## Three Hard Gate Items (All MUST Be Satisfied Before Merge)

### 1. All tests green
- The tests of the relevant layers (at minimum the part covering P0/P1 behaviors, see risk-tiers.md) all pass.
- **No skip masking**: hiding failing cases behind skip/ignore does not count as green. A skipped P0/P1 test counts as a failure.
- **No flaky pass-through**: a test that is sometimes green and sometimes red cannot serve as evidence of "green"; either stabilize it or isolate it and record that, but never "re-run until green and ship".

### 2. No orphan requirements
- Traceability validation (traceability.md) passes: every AC has a test referencing it, and there are no ghost requirements.
- This item is what lets the gate mechanically answer "was this requirement tested" — it relies on the stable IDs plus the bidirectional validation script from §II.

### 3. No breaking contract changes
- If an external contract (interface shape, field semantics, error codes, event schema, and so on) changes, one of the following MUST hold:
  - It is a **compatible change** (consumers keep working without modification); or
  - It has been **explicitly declared as a breaking change and confirmed by consumers** (recorded, with a versioning policy).
- An undeclared breaking contract change = no-go. It detonates silently on the consumer side and is the most expensive class of regression.

## The Boundary of "Mechanical" (Be Explicit; Do Not Cross It)

**This skill is only the source of the standard, not the gate itself.** What the blueprint can do: define what the three criteria above check and what counts as a pass.
The blueprint **cannot and should not** run those checks for the project.

Real enforcement MUST land in automation:

- **CI pipeline**: run all three items in the merge / release flow, and block the merge on failure.
- **git hook / pre-commit**: catch obviously non-compliant commits at the earlier local stage.
- **Branch protection rules**: require a green gate status before a merge is allowed.

Why write the gate into automation: **human self-discipline is unreliable**. A gate only truly works when a machine runs it automatically on every change and it cannot be casually bypassed. "We agree to check before every release" is not a gate; "you cannot merge while CI is red" is a gate.

## Landing Checklist (For the Skill / Project That Follows This Blueprint)

Instantiate the following logic as CI steps for the project's stack (tools chosen per stack, see capability-tool-mapping.md):

```
gate:
  - run: run the test suite (P0/P1 all green; no skip masking; no flaky pass-through)
  - run: run the traceability validation script (orphans == empty set and ghosts == empty set)
  - run: run the contract diff check (a breaking change MUST already be declared and confirmed)
  - any step fails -> block the merge (non-zero exit)
```

## Relationship to the Other Dimensions

- The gate's inputs come from risk tiering (which items must be green as P0/P1), traceability (orphan / ghost determination), and closed-loop backfill (turning orphans green).
- The gate does not replace those dimensions; it is their **convergence point and enforcement point**.

## Project-Agnostic Reminder

The specific content of a contract and the specific meaning of an AC are project-specific; the structure of "three hard gate items + enforcement by CI" is general across projects.
