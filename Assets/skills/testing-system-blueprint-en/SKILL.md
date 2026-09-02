---
name: testing-system-blueprint-en
description: Define a stack- and project-agnostic testing methodology covering P0-P3 risk tiers, requirements-to-test traceability, three-layer test timing, closed-loop gap backfill, release gates, and capability-to-tool mapping. Use when designing or governing a testing strategy, or as the shared blueprint for routing and executor skills. It defines methods and standards; it does not execute tests or enforce CI gates. Not for: executing tests, producing any file, enforcing gates (gates are enforced by CI / hooks), or hard-coding the tools of a specific language or framework.
license: MIT
metadata:
  version: "1.0"
  lang: en
  stage: "9"
  standalone: true
  requires:
    - name: "Risk profile and requirement items of the project under test"
      level: orchestration
      fallback: "Ask the user to describe the key business flows and risk points; with none available, deliver the blueprint using the generic three-layer rhythm"
---

# Testing System Blueprint

## What This Is / What This Is Not

**Is**: a methodological skeleton that upgrades "testing" from "writing a bunch of test cases" to "a system". It defines six capability dimensions and a rhythm so that any language, any framework, and any project can apply the same thinking to decide "what to test, when to test, how thoroughly, and when to release".

**Is not**: a test executor, nor a technology-stack-specific testing guide. This blueprint does not tell you "use pytest or jest" — it only tells you "at this layer you need unit + contract capabilities; instantiate the tools after you read the project stack".

**Who uses it**: `test-routing-advisor-en` (decides which type of testing a task should use) and category-specific test skills (e.g. `backend-testing-en`, `frontend-testing-en`). They take this blueprint's abstract primitives and apply them to concrete stacks and concrete projects.

## Two Absolute Constraints (Throughout the Entire Document)

1. **stack-agnostic**: This blueprint only specifies "capabilities / dimensions / methods" and never locks in any single stack's tools or libraries. Whenever example tools are given, they are always provided as multi-stack examples in the form "instantiated per stack" (Python / Node / Go / JVM …), with explicit clarification: **specific tools are instantiated by the caller after reading the project's actual technology stack**; this blueprint does not choose for you.
2. **project-agnostic**: No business-specific nouns appear. General testing concepts (BOLA, real-database, migration, concurrency, contract, idempotency) are permitted because they are universal primitives across projects.

---

## Six Capability Dimensions (Quick Reference; Details in References)

| # | Dimension | One-liner | Details |
|---|------|--------|------|
| 1 | Risk tiering P0–P3 | Decide "must-test / should-test / can-defer" by risk, not by chasing coverage numbers | `references/risk-tiers.md` |
| 2 | Requirements↔test traceability | Each acceptance criterion gets a stable ID; tests reference it; bidirectional validation | `references/traceability.md` |
| 3 | Three-layer test rhythm | L1 per task → L2 feature all-green → L3 all complete | §Three-Layer Rhythm below |
| 4 | Closed-loop backfill | Detect gap → generate → run → fix → solidify as regression | `references/closed-loop-backfill.md` |
| 5 | Release go/no-go gate | Mechanical gate before merge; standard is here, enforcement relies on CI | `references/release-gate.md` |
| 6 | Capability→tool mapping principle | Capabilities are universal primitives; tools instantiated per stack | `references/capability-tool-mapping.md` |

Additional guardrail: the 5 safety guardrails for self-healing backfill are in `references/self-heal-guardrails.md` (for reference — always read these before letting any "auto-generate / auto-fix tests" process begin).

---

## I. Risk-Tiered Test Design P0–P3 (Core Philosophy)

> Complete judgment criteria are in `references/risk-tiers.md`. This section provides the skeleton.

Test budgets are always limited. The blueprint advocates: **do not chase coverage numbers — instead, assign a tier to each behavior based on "cost of failure × probability of failure"**, so that limited testing effort is prioritized toward the most expensive failures.

- **P0 must test**: failure causes irreversible damage — data corruption / loss, authorization bypass (any user accessing data / operations not belonging to them), financial or quota miscalculation, security boundary breach. **This tier does not allow "deferral" — it is a hard input to the release gate.**
- **P1 should test**: failure makes a core flow unavailable but is recoverable — primary use case broken, critical integration severed, external contract violated.
- **P2 can defer**: edge paths, non-critical degradation, hint copy, non-critical configuration.
- **P3 can skip testing**: pure display, no-logic passthrough, temporary scaffolding.

Tiering is a property of **behaviors**, not modules: within the same module, "deduct quota" is P0, "return hint copy" may be P2. Authorization-related behaviors (typically BOLA / privilege escalation reads/writes) default to P0 unless there is an explicit reason to downgrade.

---

## II. Requirements↔Test Traceability (Bidirectional, No Leaks)

> Complete rules and validation script ideas are in `references/traceability.md`. This section provides the skeleton.

The system's credibility comes from "requirements and tests being able to match up". Approach:

1. **Give each acceptance criterion (AC) a stable ID** (e.g. `AC-007.3`); once published, IDs are never renumbered or reused.
2. **Each test references the AC ID it covers in its metadata / name / comment** (e.g. test name contains `AC-007.3` or annotation `@covers AC-007.3`).
3. **Bidirectional mechanical validation**:
   - **No orphan requirements**: no situation where "an AC exists but no test references it" (= missed test).
   - **No ghost requirements**: no situation where "a test references an AC ID that doesn't exist" (= requirement was deleted / mistyped; the test is running naked).

Traceability is not a documentation burden — it is the prerequisite for **letting the release gate mechanically answer "was this requirement tested"** — without IDs, the gate can only rely on human judgment.

---

## III. Three-Layer Test Rhythm (WHEN: What to Test and When)

The blueprint decouples "when to test" from "what to test". The same type of test has different value at different times; blindly "running everything" is both slow and masks problems.

### L1 · Each task (development phase, TDD red-green)
- **What to test**: unit tests + contract tests (shape / semantic conventions of external interfaces).
- **How**: write a failing test first (red) → implement to minimum passing (green) → refactor if necessary. This is the TDD main loop.
- **Why at this layer**: defects are cheapest to catch at the moment they are introduced; contracts are locked within the task, giving subsequent integration a foundation.

### L2 · After feature all-green (integration smoke + review)
- **What to test**: integration smoke within the feature's modules — the happy path running through real dependencies (real database, real migration, real queue).
- **Key discipline**: **integration tests are bound to the feature boundary, not the project boundary**. When all tasks of a feature are green, do integration validation within that feature's boundary; do not wait until the entire project is done to assemble modules for the first time.
- **Why**: a feature is "the minimum verifiable unit of a group of cooperative tasks"; doing integration at its boundary keeps the problem domain small and localization fast; waiting until project level to integrate means stacking all integration risk to the very end.

### L3 · After all is complete (full-chain E2E + cross-module consistency)
- **What to test**: cross-feature end-to-end user journeys + cross-module data / state consistency.
- **Key mindset**: **L3 is a "safety net", not the place to "first discover bugs"**. If a defect that should have been caught at L1/L2 is only exposed at L3, that means L1/L2 missed it — it should be backfilled to the corresponding layer, not treated as a catch-all garbage bin for L3.
- **Why**: E2E is slow and brittle, suitable only for verifying "the whole chain actually works" — the one thing L1/L2 cannot cover; stuffing unit-level assertions into E2E makes the suite slow and hard to maintain.

> The three layers are not sequential approval checkpoints — they are **guidance on which layer a defect should be caught most cheaply**. The further left, the cheaper.

---

## IV. Closed-Loop Backfill (Gap → Solidify as Regression)

> Complete process and judgment criteria are in `references/closed-loop-backfill.md`. This section provides the skeleton.

Systematic testing is not just "supplement tests once" — it is a closed loop that ensures every discovered gap becomes a **long-term regression asset**:

```
Detect gap → Generate test (reproduce gap, start red) → Run → Fix product code to green → Solidify as regression test (enter the permanent suite)
```

Before backfilling, classify each candidate gap to avoid wasted work:

- **✅ Already covered by development-phase TDD / contract tests** → **Skip**. This behavior already has a red-green history at L1; re-supplementing is waste.
- **🔧 Structural gap** → **Pending closed-loop backfill**. A real risk that has never been tested at any layer (typical: cross-module boundaries, error paths, concurrency / idempotency, authorization bypass) — this is the target that closed-loop backfill should consume.

"Solidify as regression" is the conclusion of the loop, and also the essential difference between it and "run a test once temporarily": the supplemented tests must be merged into the permanent suite, otherwise the same bug will return.

---

## V. Release Go/No-Go Gate (Mechanical Gate)

> The complete gate checklist is in `references/release-gate.md`. This section provides the skeleton and boundary.

Mechanical criteria that must be satisfied before merge / release (any one unsatisfied = no-go):

1. **All tests green**: all relevant layers (at minimum P0/P1 corresponding tests) pass; no skip masking, no flaky tests being let through.
2. **No orphan requirements**: traceability validation passes — every AC has a test referencing it (see §II).
3. **No breaking contract changes**: if an external contract changes, it must be a compatible change, or it has been explicitly declared and confirmed by consumers.

**On the boundary of "mechanical" (must be clear)**: this blueprint **only provides the release standard, it does not enforce it for you**. Real gate enforcement must land in **CI pipelines / git hooks / pre-commit** and other automation facilities — they automatically run these criteria before merge and block non-compliant changes. This skill is "the source of the standard", not "the gate itself". Writing enforcement into automation is what makes the gate not rely on human self-discipline.

---

## VI. Stack-Agnostic Tool Mapping Principle

> The complete multi-stack reference table is in `references/capability-tool-mapping.md`. This section provides the principle.

Everything in the blueprint is a **capability** — a universal primitive, such as "unit assertion", "HTTP contract", "real-database integration", "E2E driver". **A tool is an instantiation of a capability in a specific stack**, selected by the caller after reading the project's actual technology stack.

Principle: **first determine which capability is needed, then instantiate that capability as the tool for that stack**; the blueprint always stops at the capability layer and never locks in tools.

Illustration (only to show "the same capability has different instantiations in different stacks", **does not constitute recommendations, does not lock in anything**):

| Capability (universal primitive) | Python example | Node example | Go example | JVM example |
|---|---|---|---|---|
| Unit / assertion | That stack's mainstream unit test framework | That stack's mainstream unit test framework | Built-in testing | That stack's mainstream unit test framework |
| HTTP / interface contract | Contract / schema validation library | Contract / schema validation library | Contract / schema validation library | Contract / schema validation library |
| Real-database integration | Temporary real database instance | Temporary real database instance | Temporary real database instance | Temporary real database instance |
| E2E driver | Browser / API driver | Browser / API driver | Browser / API driver | Browser / API driver |

Library names are intentionally omitted from the table — specific libraries are instantiated by `test-routing-advisor-en` or category skills after reading the project stack.

---

## How to Use This Blueprint (For Skills That Follow It)

1. **Router (`test-routing-advisor-en`)**: use §I to tier tasks, use §III to determine which layer they fall into, use §VI to pass capabilities to the corresponding stack's category skill.
2. **Category skills (e.g. `backend-testing-en`)**: within their responsible stack, instantiate §VI capabilities into specific tools, maintain traceability per §II, do closed-loop backfill per §IV, and ultimately align with the release gate in §V.
3. For any "auto-generate / auto-fix tests" action, read the 5 guardrails in `references/self-heal-guardrails.md` first.


## Upstream Artifacts

| Artifact | Level | When missing |
|---|:---:|---|
| Risk profile and requirement items of the project under test | orchestration | Ask the user to describe the key flows; with none available, deliver the generic blueprint |

## Downstream Consumers

| Consumer | What it takes from this skill |
|---|---|
| The test routing skill | The categorization criteria |
| The 4 test executors | The three-layer rhythm and the self-healing guardrails |

This skill produces no file. Consumers follow it **by name** — there is no artifact on disk for them to read.

## Standalone Use

**What you provide**: the key business flows and known risk points; it also works without them, in which case you get the generic blueprint.

**What you get**: a stack-agnostic testing methodology skeleton — risk tiering, traceability, three-layer rhythm, closed-loop backfill, release gate.

**What you don't get**: it produces no file at all (this skill is a blueprint that is followed by name); it does not execute tests; it does not enforce gates; it does not hard-code the tools of any language or framework.
