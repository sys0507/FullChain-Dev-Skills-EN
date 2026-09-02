---
name: backend-testing-en
description: Close backend-only structural testing gaps after feature-level TDD, including real-database behavior, migrations and transactions, authorization boundaries, concurrency and atomicity, and resilience or fault injection. Detect the project stack, test only applicable gaps, archive traceable evidence, and deliver isolated changes for human review. Use directly or when routed by test-routing-advisor-en. Not for: frontend testing, cross-feature end-to-end chains, or modifying product code (product defects that are discovered MUST be handed back to the implementation process).
license: MIT
metadata:
  version: "1.0"
  lang: en
  stage: "9.2"
  standalone: true
  produces:
    - "Backend test code"
    - "Evidence archive"
  requires:
    - name: "Routing decision report, or gaps named directly by the user"
      level: orchestration
      fallback: "Ask the user which class of backend gap to close; with no answer, sweep all four structural gap types"
    - name: "Project manifest file"
      level: required
    - name: "Testing System Blueprint skill"
      level: optional
      fallback: "Reference it by name; when it is not installed, use the built-in condensed risk-ranking version, so the blueprint's full criteria are not covered"
    - name: "External debugging capability"
      level: optional
      fallback: "Fall back to the built-in hypothesis-verification loop to locate failure causes, so no external debugger evidence is covered"
---

# backend-testing-en · Backend-Only Closed-Loop Test Executor

## What Problem This Skill Solves

Development-phase TDD (superpowers) and contract / spec tests (spec-kit) cover "whether functionality works as specified". But the backend has a class of **structural gaps** that do not belong to individual feature points — they belong to the system's runtime properties: real database behavior, access control across identities, invariants under concurrency, resilience when external dependencies fail. These gaps almost never get written naturally during development-phase TDD and only surface as production incidents.

This skill is the **closed-loop backfill executor** for these gaps: it is called when a backend feature is wrapping up (routed by `test-routing-advisor-en` after determining "backend-only", or triggered directly), supplements the hit structural gaps with RED→GREEN testing, solidifies them as regressions, and incorporates them into the release gate per the blueprint.

> Key insight: **code-review ≠ test**. Code review only finds problems through reading and does not generate repeatable regressions; defects "spotted and fixed during review" will recur in the next refactoring if not solidified into tests. This skill's output is **tests that can be run red/green again**, not a review opinion. The methodology for solidifying defects is reusable from `superpowers:test-driven-development` and `superpowers:systematic-debugging`.

Follows the `testing-system-blueprint-en` blueprint (reference by name): risk tiering ordering, traceability IDs, release gate, three-layer rhythm.

---

## Two Absolute Constraints (Read First — Throughout the Entire Workflow)

1. **stack-agnostic**: All four gap types are expressed uniformly as "capability description + per-stack instantiation lookup" — never hard-code a single stack as the only answer. Every capability type gives multi-stack examples and makes it explicit: **read the project stack file first, then instantiate the corresponding tools for that stack**. Which stack and which libraries the project uses is determined by the project itself; this skill only provides the capability-to-tool mapping.
2. **project-agnostic**: No business-specific nouns appear. General backend concepts are permitted (BOLA / BFLA / real-database / migration / transaction / constraints / concurrency / race conditions / rate-limiting / contract / fault injection).

---

## Workflow (Six-Step Closed Loop)

### Step 0 · Identify Stack

Read the project stack file, determine the language and runtime; all subsequent tool choices are instantiated based on this:

| Stack Clue File | Language / Runtime | Subsequent Tool Source |
|---|---|---|
| `pyproject.toml` / `requirements.txt` / `setup.py` | Python | See the Python row for each gap |
| `package.json` (including `tsconfig.json`) | Node / TS | Node row |
| `go.mod` | Go | Go row |
| `pom.xml` / `build.gradle` | JVM | JVM row |
| Other | As needed | Reverse-look up the ecosystem equivalent for that stack using "capabilities" |

> If no stack file is found, stop and ask — do not assume. For multi-stack monorepos, identify the stack closest to the backend directory being tested.

### Step 1 · Conditional Hit (Prevent Over-Testing)

**Do not test all four types** — only supplement for the subset that this feature actually hits. Evaluate each item:

| Gap | Hit Condition | Non-hit Example |
|---|---|---|
| Real-database data layer | Feature involves DB writes / unique constraints · foreign keys · CHECK / schema migration | Pure read-only aggregation, no migration |
| Authorization BOLA·BFLA | Multiple users with object ownership exist / privileged (admin) endpoints exist | Single-tenant internal tool, no identity isolation |
| Concurrency / race conditions | Shared resource contention / rate limiting / quotas / counters / inventory-style deductions exist | Pure functional processing with no shared mutable state |
| Resilience / fault injection | External dependencies called (HTTP API / third-party SDK / message queue / remote cache) | Pure local logic, no external calls |

A purely logical / purely read feature may hit 0–1 items — this is normal; do not force coverage.

### Step 2 · Coverage Differentiation

For each **hit** dimension, first determine whether it is already covered by development-phase TDD / contract tests, then decide whether to supplement:

- `✅ Already covered by development-phase TDD / contract tests (skip)` — do not recreate.
- `🔧 Structural gap (pending closed-loop backfill)` — this skill needs to supplement. For each 🔧 also note the instantiation method:
  - `Off-the-shelf tool ✅ installable` — the stack has a mature library; install and use it.
  - `Needs custom build 🔧` — the stack has no ready-made solution; build fixture / scaffolding per the pattern (authorization types are almost always this).

Write the conclusions of this step as a small table (dimension / hit / coverage status / instantiation method) to serve as the checklist for subsequent backfill.

### Step 3 · RED→GREEN Closed-Loop Backfill

For each `🔧` gap, work through them one by one:

1. **RED**: Write a failing test first, confirm it actually runs red (meaningfully red — red because of the defect / uncovered behavior, not because the test was written incorrectly).
2. **GREEN**: Make the test go green.
   - If the defect genuinely exists (spotted during review but not solidified), fix the product code per `superpowers:test-driven-development` / `superpowers:systematic-debugging` to make it turn green.
   - If it is only a coverage gap (the behavior is already correct), supplementing the test should immediately be green; no product code change needed.
3. **Solidify as regression**: Leave the test in `tests/`, enter the regression suite, run automatically from now on.

> Specific tools and code patterns are in `references/gaps.md` — take the corresponding row based on the stack identified in Step 0.

### Step 4 · Archive Per Blueprint

For each newly added regression test:

- Order by **risk tier** per `testing-system-blueprint-en` (high-risk gaps take priority; prioritize entering the release gate).
- Attach a **traceability ID** (link to feature / gap / defect source if available).
- Incorporate into the **release gate**: specify which ones are release blockers (e.g. authorization bypassable, constraint failure) and which are alert-level.
- Align with the **three-layer rhythm** (as defined in the blueprint; real-database and concurrency types usually land in the slower layer; only pure logic goes in the unit test layer).

### Step 5 · Deliver (Isolated Changes · Human Review)

Keep backfill in an isolated branch or change set for **human review**. The upper-level wrap-up stage decides whether to merge directly or open a PR. The delivery note lists hit dimensions, skipped dimensions with reasons, and the gap ID and risk tier for each newly added regression.

---

## Four Gap Types Quick Reference (Details in references/gaps.md)

1. **Real-database data layer / migration / transaction / constraints** — capability: start a real DB container + run migration up/down round-trips, assert constraints, transaction rollback, migration reversibility.
2. **Authentication / authorization BOLA·BFLA** — capability: create token fixtures for two different identities / permission levels, parameterize-traverse object-level and privileged endpoints, assert cross-identity access is rejected (403/404). **Framework-agnostic; almost always requires custom build**.
3. **Concurrency / race conditions / rate-limiting atomicity** — capability: concurrently hit the same endpoint / resource, assert invariants and atomicity (no overselling, no double-spend, rate limiting is accurate).
4. **Resilience / fault injection** — capability: intercept external calls to inject timeout / error sequences, assert that retry, timeout, degradation, and circuit breaking behave as expected.

Every type uses "capability + per-stack lookup" — **read the stack first, then instantiate the corresponding tools, rather than locking in a single stack**.

---

## Self-Healing Guardrails (Not to Be Crossed)

The backfill process allows bounded automatic iteration (RED → fix → GREEN), but is constrained by the following guardrails:

- **Only write to `tests/`, do not modify product code** — if RED exposes a real product defect, stop and return it to the development TDD/debugging workflow. This skill backfills tests; it does not repair implementation code.
- **Assertions cannot be weakened** — it is forbidden to relax assertions in order to make a test go green (e.g. changing `403` to `or 200`, deleting concurrency invariants). Going green must be achieved through correct product code or correct tests — not by lowering the bar.
- **No fake fixes** — do not use sleep, mock out the logic being tested, skip / `skip` markers, or similar means to fake a pass.
- **Bounded retry escalation** — automatic iteration has an upper limit; upon reaching the limit after consecutive failures, stop and escalate to a human — do not loop indefinitely.
- **Isolated changes + human review** — keep all outputs in an isolated branch or change set for review; the upper-level wrap-up stage decides merge versus PR.

The purpose of the guardrails: let the loop run automatically, while blocking every shortcut that "looks green but didn't actually test anything".

---

## Relationship to Upstream and Downstream

- Upstream: `test-routing-advisor-en` calls this skill when it determines "backend-only" (can also be triggered directly by the user).
- Blueprint: all archiving / tiering / release gates / rhythm follow `testing-system-blueprint-en` (referenced by name; its content is not duplicated here).
- Methodology reuse: defect solidification and debugging reuse `superpowers:test-driven-development` and `superpowers:systematic-debugging`.


## Upstream Artifacts

| Artifact | Level | When missing |
|---|:---:|---|
| Routing decision report, or gaps named by the user | orchestration | Ask the user; with no answer, sweep all four gap types |
| Project manifest file | **required** | Stop — with no stack determination, tools cannot be instantiated |
| Testing System Blueprint skill | optional | Reference by name; when not installed, use the built-in condensed version |
| External debugging capability | optional | Built-in hypothesis-verification loop |

## Downstream Consumers

| Consumer | What it reads |
|---|---|
| Branch wrap-up | Test results and residual risks |

## Standalone Use

**What you provide**: a backend feature, plus the project's dependency manifest file (used to determine the technology stack).

**What you get**: closed-loop backfill for the four backend structural gap types: real database / migration / transaction, authorization bypass, concurrency / race conditions, resilience / fault injection.

**What you don't get**:

- **The project manifest MUST be readable** — if the stack cannot be determined, the corresponding tools cannot be instantiated; this is the only required dependency.
- **Tests only**. When a product defect is found, this skill stops and hands the fix back to the implementation process; it does not modify product code itself.
- No frontend work, no cross-feature chains.
