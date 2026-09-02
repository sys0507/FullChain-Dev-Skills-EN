# Risk-Tiered Test Design P0–P3 (Complete Criteria)

> This document expands SKILL.md §I. Stack-agnostic, project-agnostic.
> Core claim: **allocate the test budget by "cost of failure × probability of failure", not by coverage percentage.**

## Meet P0–P3 in One Sentence (Four Priority / Risk Tiers, P0 Highest)

P0–P3 are four tiers that prioritize **what to test**, derived from the industry Priority/Severity convention — **P0 highest, P3 lowest** — descending by "how fatal a failure is":

| Tier | One-liner | Consequence of failure | Testing attitude |
|----|--------|---------|---------|
| **P0** | Security / money / authorization / data; irreversible once it happens | Data corruption, authorization bypass, miscalculated money, security breach, irreversible mistriggered action | **Must test; hard block in the release gate; deferral not allowed** |
| **P1** | Core flow does not work (but is recoverable) | Main flow broken, critical integration broken, external contract violated | Should test; should be all-green before release |
| **P2** | Edge / non-critical | Edge inputs, degradation paths, hint copy | Can defer; goes to the backlog |
| **P3** | Pure display / no logic | Field passthrough, temporary scaffolding | Can skip testing |

**"Pick the P0s"** = out of a pile of candidates (interface behaviors, test points, chain journeys …) **test only the highest tier first** — because the test budget is limited, protect the most fatal outcomes first. The complete criteria for each tier follow.

## Why Risk Tiering Instead of Coverage

Coverage (line coverage, branch coverage) measures "was this code executed", **not "was an important failure asserted against"**.
100% line coverage may contain not a single assertion checking authorization bypass; 50% coverage may happen to pin down every P0 behavior.
So the blueprint replaces coverage with risk tiering as the budget-allocation basis: first answer "which failures are most expensive and most likely", then push the effort there.

## Tiering Is a Property of "Behavior", Not of "Module / File"

Different behaviors inside the same module differ wildly in risk. Tier behaviors, not files.

- Inside one handler: "perform the core write / deduct quota / check authorization" may be P0, while "return hint copy / write a log line" may be P2.
- Do not treat every assertion in a file as P0 just because "this file is important" — that wastes budget on low-risk behaviors.

## Criteria for the Four Tiers

### P0 · Must test (failure causes irreversible damage)
Any one of these triggers P0:
- **Data corruption / permanent loss**: wrong write, wrong delete, a migration that damages existing data and cannot be rolled back.
- **Authorization bypass**: any principal obtaining data or operational capability that does not belong to it. Typical cases: **BOLA (accessing another principal's objects)** and vertical escalation (an ordinary principal obtaining admin capability). **Authorization-related behaviors default to P0.**
- **Money / quota / allowance miscalculation**: over-deduct, under-deduct, double-deduct, bypassing a limit.
- **Security boundary breach**: authentication bypass, injection, sensitive information leakage.
- **Irreversible side effects**: an externally irrevocable submission / dispatch triggered by mistake.

P0 discipline: **deferral is not allowed**. Tests for P0 behaviors are a hard input to the release gate (see release-gate.md); one missing item = no-go.

### P1 · Should test (failure makes a core flow unavailable, but it is recoverable)
- The main use case (happy path) does not work.
- A critical integration is broken (the real database / queue / downstream interface it depends on does not work when genuinely assembled).
- **External contract violated**: the shape / semantics of an interface consumers depend on has changed.
- Critical error paths: a place that should fail gracefully crashes instead, without causing irreversible damage.

P1 is a routine input to the release gate: it should be all-green before release; shipping an individual P1 with a known defect requires an explicit record and a human decision.

### P2 · Can defer (edge / non-critical)
- Edge inputs, non-critical degradation paths, rare configuration combinations.
- Hint copy, non-core formatting, acceptable approximate behavior.

P2 does not block release; it goes to the backlog and is filled in on rhythm (usually backfilled via the closed-loop backfill method, see closed-loop-backfill.md).

### P3 · Can skip testing
- Pure display, no-logic field passthrough, temporary scaffolding / one-off scripts.
- The maintenance cost of writing tests for them > the cost of them being wrong.

## Tiering Quick Reference

| Signal | Default tier |
|------|--------|
| Involves authorization / bypass / authentication boundary | **P0** |
| Involves money / quota / allowance / irreversible submission | **P0** |
| Can corrupt or lose existing data | **P0** |
| Core happy path / critical integration / external contract | **P1** |
| Edge path / non-critical degradation / copy | **P2** |
| Pure display / no-logic passthrough / temporary scaffolding | **P3** |

## How Tiering Feeds the Three-Layer Rhythm (see SKILL.md §III)

- The core assertions for **P0/P1** should be pinned down at **L1 (unit / contract)** wherever possible — the further left, the cheaper.
- P0/P1 items that only surface when genuinely assembled (real-database authorization bypass, concurrent deduction) land at **L2 integration**.
- **L3 E2E** only verifies "the whole chain actually works"; it does not carry the duty of first-discovering P0 assertions (L3 is a safety net, not the first inspection station).

## Stack-Agnostic Reminder

No library name, framework name, or business noun appears in this document. "Which tool to use to assert a P0 behavior" is instantiated by the caller after reading the project stack (see capability-tool-mapping.md). Risk tiering only answers "what to test and whether it must be tested"; it does not answer "what to test it with".
