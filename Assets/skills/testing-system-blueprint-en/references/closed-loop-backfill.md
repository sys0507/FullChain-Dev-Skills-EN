# Closed-Loop Backfill (Complete Process)

> This document expands SKILL.md §IV. Stack-agnostic, project-agnostic.
> Core: make every discovered gap a **long-term regression asset**, not a "patch it once and done" exercise.

## The Five Steps of the Loop

```
(1) Detect gap -> (2) Generate test (reproduce the gap, start red) -> (3) Run -> (4) Fix product code to green -> (5) Solidify as a regression test
```

1. **Detect gap**: through traceability validation (orphan requirements), risk tiering (P0/P1 behaviors that were never tested),
   real bugs surfaced in production / integration, or code review — find the behaviors that "should have been tested but were not".
2. **Generate test**: write a test that **reproduces the gap**; at this moment it MUST **fail (red)**.
   "Red first" is critical — it proves the test actually detects a real problem rather than being a placebo that is green the moment it is written.
3. **Run**: confirm it really is red, and that the reason for the red is precisely that gap (not a mistake in the test itself).
4. **Fix product code to green**: change the **product code** to make the test pass.
   Mind the direction — **you change the product code, you do not weaken the test to make it green** (see self-heal-guardrails.md item 2).
5. **Solidify as a regression test**: merge the test into the **permanent test suite**. This is the essential difference between the loop and "running something once" —
   without solidification the same bug comes back sooner or later; with it, the bug is permanently blocked at the regression line.

## Classify Before Backfilling: Skip vs. Pending Closed-Loop Backfill

Not every candidate gap is worth filling. Label each candidate before starting, to avoid wasted work:

### ✅ Already covered by development-phase TDD / contract tests -> Skip

- This behavior already **has a red-to-green history** at L1 (per-task TDD red-green) or in contract tests.
- It already guards against regression in the permanent suite; re-supplementing wastes effort and bloats and slows the suite.
- Detection signal: an existing test can be found that references the corresponding AC ID and asserts that behavior.

### 🔧 Structural gap -> Pending closed-loop backfill

- A real risk that has **never been tested at any layer**. This is the target closed-loop backfill should consume.
- Hotspots:
  - **Cross-module boundaries**: each module was tested on its own, but nobody tested the handoff where they meet.
  - **Error paths / exception branches**: the happy path is tested, the failure path is not.
  - **Concurrency / idempotency**: duplicate submissions, deductions / writes under a race.
  - **Authorization bypass (BOLA and similar)**: P0 by default, and routinely missed by cases that "only test one's own data".
  - **Problems that only surface under real dependencies**: green when tested against doubles (mocks), wrong once a real database / real migration is attached.

## Classification Decision Table

| State of the candidate gap | Handling |
|---|---|
| An existing test references that AC and asserts that behavior | ✅ Skip |
| The behavior is P0/P1 risk but no test asserts it | 🔧 Pending closed-loop backfill (priority) |
| Cross-module handoff / error path / concurrency / authorization bypass never tested | 🔧 Pending closed-loop backfill |
| The behavior is P2/P3 and the cost is low | Record in the backlog, fill in on rhythm, do not block |

## Relationship to the Three-Layer Rhythm

- A test produced by the loop should be **backfilled to the layer it actually belongs to** (see SKILL.md §III), not dumped wholesale into E2E.
  - A unit-level gap -> backfill to L1.
  - A cross-module integration gap -> backfill to L2 (bound to the corresponding feature boundary).
- If a gap is only discovered at L3, L1/L2 missed it: when backfilling, **push it down to L1/L2** so that next time it is caught earlier and more cheaply.
  L3 is a safety net; it should not permanently carry assertions that belong to lower layers.

## Relationship to the Release Gate

- Closed-loop backfill is the routine way to turn the "no orphan requirements" gate item (release-gate.md) green: traceability finds an orphan -> run the five-step loop -> the gate turns green.
- Any process that automatically detects gaps and automatically generates tests MUST obey the 5 guardrails in self-heal-guardrails.md before it starts.

## Stack-Agnostic Reminder

"How to write a test that reproduces the gap" and "how to run it" are instantiated by the caller per stack. The five steps of the loop and the classification logic are constant across stacks.
