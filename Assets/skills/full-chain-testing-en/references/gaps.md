# Complete Functional Chain · Capability Layer + Per-Stack/Scenario Instantiation

> How to use: first excavate the cross-feature path inventory with the **three-source model** per SKILL.md step 0 and identify the stacks and jump types,
> then read the row for that stack/scenario under the matching capability to instantiate tools. Each capability states the **capability** first (stack-agnostic, always true), then gives **instance examples**.
> **Every example is a lookup, never the only answer, and never a hard dependency** — what stack the project uses and whether it has a given tool is decided by the project itself;
> if the environment lacks a tool, fall back to that capability's generic equivalent. This table only maps "capability -> tool for that stack/scenario."
>
> **The core distinctive points of this skill**: (1) the subject under test must be **excavated first** (three-source model, see §1); (2) it is the **safety-net layer** —
> few and precise, covering only P0; **a bug first appearing here = lower-layer coverage gap, back-fill the lower layer**.
>
> **Every "project-specific" input is read at runtime and conditional**: which crons / scheduled tasks exist, whether a given jump is streaming
> (SSE/WS/long-polling), interface shapes, token / one-time login mechanism, what cross-channel uses, whether gstack exists at all, which middleware dependencies exist —
> **always read at runtime, never written into this table, never pre-assumed**. Anything touching jumps / streaming is always written as "**if the journey contains X, then** …".
>
> **Special note (glia)**: glia has a **non-commercial license**; it may be mentioned as an example of the "static code graph" capability, but **commercial products cannot use it**;
> this skill is not bound to any single tool, and the static graph capability can be instantiated by any equivalent.

## Contents

0. [Prerequisite discipline (runs last / ordering iron rule / data isolation / no sleep)](#0-prerequisite-discipline-runs-last--ordering-iron-rule--data-isolation--no-sleep)
1. [⭐ Path excavation three-source model (the core of this quadrant: excavate the subject under test first)](#1--path-excavation-three-source-model-the-core-of-this-quadrant-excavate-the-subject-under-test-first)
2. [Select P0 critical journeys (the safety net is few and precise)](#2-select-p0-critical-journeys-the-safety-net-is-few-and-precise)
3. [Whole-system orchestration + stub external boundaries only](#3-whole-system-orchestration--stub-external-boundaries-only)
4. [Drive by jump type (conditional hit)](#4-drive-by-jump-type-conditional-hit)
5. [Two-layer landing: black-box traversal + structured chain assertions](#5-two-layer-landing-black-box-traversal--structured-chain-assertions)
6. [Cross-capability general reminders](#6-cross-capability-general-reminders)

---

## 0. Prerequisite discipline (runs last / ordering iron rule / data isolation / no sleep)

**Runs last**: full-chain inherently needs **the most code** — it has to bring alive every feature that the whole cross-feature journey passes through,
so it is **the quadrant that can actually be executed only last**. **When the code is not yet landed** (the chain exists only in the spec), the static graph and traces are both blind,
and **the spec contract is the only source of truth**; even then you can still "excavate candidate paths + write RED E2E" (written and traceably attached, but not yet green-runnable).

**Ordering iron rule (the most commonly stepped-in pit)**: off-the-shelf E2E tools — whether diff-aware (gstack `/qa` is one) or general-purpose
(Playwright / Cypress) — **only probe an already-running localhost; they do not bring the stack up**. So **bringing up the whole-system stack (§3)
MUST be completed before running E2E (§5 layer one)**; reverse the order and E2E probes an empty address, going all red in a way that means nothing.

**Data isolation discipline**: chain E2E runs on the whole-system real stack and passes through data across multiple features, so there MUST be **seed / teardown
fixtures** — bring up a set of known data -> run the whole journey -> clear it, guaranteeing controllability, no cross-contamination, repeatability.

**No sleep (time-control iron rule, guardrail level)**: when the chain contains scheduled / async / cross-channel jumps, **fixed `sleep` /
`waitForTimeout` to fake readiness or fake the clock reaching a time is forbidden** — slow, fragile, and deceptive. Instead use: **scheduled jump -> fake clock / manually trigger
the scheduled task**; **async / cross-channel jump -> poll-retry to the final state (bounded retries)**.

**Teardown discipline**: the cadence in CI and locally is **bring up the whole-system stack -> run the journey -> tear down**; after testing, always clean up the real stack together with its data to avoid leakage polluting the next run.

---

## 1. ⭐ Path excavation three-source model (the core of this quadrant: excavate the subject under test first)

**Capability**: before testing anything, first **excavate** the "cross-feature end-to-end paths" from the system structure (path inventory) —
because the subject under test in this quadrant **is not given** (in the first three quadrants it is). **No single source can excavate the whole graph**; the three sources MUST complement each other:
each source only reliably excavates one class of edge, and only together do they assemble a complete cross-feature path. **This is a conclusion established by two real projects + a controlled experiment.**

### Three-source capability table

| Source | Edges it reliably excavates (capability) | Instance examples (lookup, **not a dependency**) | Known failure modes (established) |
|---|---|---|---|
| **A static code graph** | backend routes / resources / call graph / shared dependencies — **edges with a clear syntactic fingerprint** | glia (**non-commercial license, commercial products cannot use it**) / OpenLore-style / that stack's built-in call graph and dependency analysis | excavates only **half the graph**; **cannot excavate framework-wrapped cross-service request edges** (modern frontends do not write bare fetch, and once wrapped by AI-SDK / a hand-rolled client / templated URLs the FE<->BE bridge edge breaks); cron/queue decoupled edges are corpus-sparse and not promising |
| **B runtime trace** | **the only reliable way to fill in**: (1) FE<->BE bridge edges; (2) decoupled edges (HTTP/cron/async/cross-channel) | distributed tracing (OpenTelemetry-style) / execution trace recording (AppMap-style) / kernel-level observation (eBPF-style); with no such facility, "temporary log instrumentation + one manual run to stitch edges" | needs a real run before a trace exists; with code not yet landed there is no runtime to trace -> fall back to source C |
| **C spec contract** | backstops **semantics** + **the only source of truth when code is not yet landed** | the project's own cross-feature contract table / AC / design documents (**depends on no tool**) | declares intent only, does not prove implementation; after landing, A/B verification is still needed to show "it really connects" |

### Known failure modes in detail (commit these to memory, don't step in them again)

- **The static graph excavates only "half the graph"**: it covers only syntactically clear edges (explicit function calls / explicit route mounting / explicit shared imports).
- **Framework wrapping eats the syntactic fingerprint -> the FE<->BE bridge edge breaks**: modern frontends **essentially never write bare `fetch`**, and as soon as it goes through framework wrapping
  (AI-SDK / a hand-rolled client / templated URL concatenation), the static graph cannot connect which backend endpoint that frontend interaction actually hits.
  **Reproduced independently in two separate projects**; **a controlled experiment proved the resolver itself is not broken** (the same call, rewritten as a bare fetch, is excavated fine)
  — this is a **structural boundary** of "framework wrapping eats the syntactic fingerprint," not a tool bug. -> **Bridge edges MUST be filled in by source B (trace) or source C (spec).**
- **cron / queue decoupled edges**: the static resolver's corpus is sparse and hit rates are not promising. -> **Prefer filling these in from source B / source C, don't fight the static graph.**
- **When code is not yet landed, static tooling is entirely blind**: no code to analyze, no runtime to trace. -> **Source C (spec contract) is the only source of truth**,
  and you can still "excavate candidate paths + write RED E2E."

### Discipline for using the three sources together

**Source A excavates the backend skeleton (half the graph) -> source B fills in FE<->BE bridge edges + decoupled edges -> source C backstops semantics throughout / sets P0 / serves as the source of truth when code is not yet landed.**
Missing any one source and you cannot assemble a complete cross-feature path.

**Output**: a **path inventory** — each path recording "which features it passes through + which jumps it contains
(UI-walkable segment / scheduled / async / cross-channel) + which source excavated it."

---

## 2. Select P0 critical journeys (the safety net is few and precise)

**First, know what P0 is**: P0–P3 are four tiers for prioritizing "what to test" (the industry Priority/Severity convention, **P0 highest, P3 lowest**) —
P0 = irreversible once it goes wrong (security/funds/permissions/data corruption), P1 = the core flow is blocked but recoverable, P2 = edge/non-critical, P3 = purely presentational.
**Full criteria are in the blueprint's `risk-tiers.md`** (which also carries a one-line "recognize P0–P3" quick-reference table).

**Capability**: from the path inventory, per blueprint §1 **risk tiering, pick only the P0 journeys** — this quadrant is the **safety-net layer**; it does not chase coverage rate, and covers only the critical chains that are "irreversible
once they go wrong + high frequency." **What is tiered here is the whole journey**: if a journey's **final-state effect** hits any P0 criterion
(data corruption / privilege escalation / miscalculated funds or quota / irrevocable outbound delivery / core main flow unavailable), the whole journey is P0.

> **Chain-level P0 examples (to help judge "which journey is worth weaving a net for")**:
> - P0: "place order -> deduct quota -> async generation -> push delivery" — the final state involves **funds/quota + irrevocable delivery**; one wrong step is irreversible.
> - P0: "register/authenticate -> obtain data that belongs to someone else" — the final state is **privilege escalation**.
> - P1: "can the main flow run from start to finish" — core availability, recoverable.
> - P2/P3: "toggle a preference -> some non-critical display changes" — edge, not part of the safety net.
>
> **The safety net is few and precise**: in the path inventory, **only P0 journeys** are woven into E2E; P1 and below are not woven end-to-end in this quadrant (they should be pinned down at cheaper lower layers).

**Why only P0**: chain E2E is slow and fragile (blueprint L3). Weaving every path in the inventory into E2E makes the suite slow and hard to maintain,
and drags defects that should have been caught at a lower layer up to the most expensive layer. **The safety net is few and precise, validating only "the whole chain really connects," the one thing lower layers cannot cover.**

**Safety-net-layer iron rule (distinctive point 2)**: **if a bug is first discovered at the chain layer -> that is a signal of a lower-layer coverage gap** — it should have been caught more cheaply at backend-only /
frontend-only / partial frontend-backend. Besides turning the chain green, **back-fill the lower layer at the same time** (add it as a regression in that quadrant).

**Exclude anything that does not cross features**: every selected journey MUST **genuinely cross multiple features**; anything within a single feature (even if it spans frontend and backend)
belongs to the third quadrant `fullstack-slice-testing-en` and is excluded from this quadrant.

---

## 3. Whole-system orchestration + stub external boundaries only

**Capability**: bring **all features the journey passes through + dependent middleware** alive together, reproducibly, local == CI, in real form,
with health checks passing (ready means ready, **not a fixed sleep**). The scope is larger than the third quadrant's "bring up both sides."

**Stub boundary discipline (key to this quadrant)**:
- **Everything internal is real**: all internal features / services / middleware the journey passes through participate for real — **stubbing out an internal feature under test is forbidden**
  (stub it and the quadrant degrades into a lower layer and loses all meaning).
- **Stub only external third-party boundaries**: stub only dependencies outside the system boundary that are uncontrollable, expensive, or slow — **typically LLM / push channels / payments**.
  **Which ones count as an "external boundary" is read at runtime**; do not pre-assume.

| Orchestration form (capability) | Instance examples (lookup, not the only solution) | Applicability clues |
|---|---|---|
| Container orchestration | docker-compose / equivalent compose, defining all features the journey passes through + middleware as services + healthcheck | multiple features already containerized, many middleware dependencies |
| Process orchestration | process management script / Makefile target / Procfile-style, bringing up multiple services locally + waiting on health checks | lightweight, not fully containerized |
| Reuse existing orchestration | the project's existing compose / startup script / CI service block (**read at runtime; reuse it if present**) | the project already has a one-command bring-up definition |
| External boundary stubbing | in the orchestration, replace external dependencies such as LLM / push / payments with observable stubs (recording what was delivered) | the journey passes through an external third-party boundary |

**Typical landing checklist**: one command brings up every feature the journey involves + dependencies; external boundaries are swapped for observable stubs; health checks wait until
everything is ready; a smoke run of the simplest real journey proves the whole chain can move; seed/teardown is in place; tear the stack down after testing.
**Write no chain assertions before the smoke run is green.**

---

## 4. Drive by jump type (conditional hit)

**Capability**: for each P0 journey, **confirm at runtime which jumps it actually contains**, and choose the driving method by type. A complete chain is often
"the user clicks once -> a scheduled task generates something -> it is pushed asynchronously to some channel -> the user receives it at the other end," and **non-UI jumps cannot be handled by idling on the UI**.

| Jump type | Hit condition | Driving method (capability) | Instance examples (lookup, not the only solution) |
|---|---|---|---|
| **UI-walkable segment** | the journey contains a segment where the user really clicks / types in the interface | an E2E driver walks the UI | diff-aware E2E (gstack `/qa` is one, **prefer it if present, fall back if not**) / general-purpose E2E (Playwright / Cypress or that stack's equivalent) |
| **Scheduled trigger** | the journey advances via cron / scheduler | **orchestration-driven**: fake clock for time control / manually trigger the scheduled task | that stack's time-freezing library / calling the scheduled task's entry function directly / the scheduler's manual trigger API |
| **Async** | the journey advances via messages / queues / background jobs | **orchestration-driven** + poll-retry to the final state | really send a message + bounded polling asserting the final state (**no fixed sleep**) |
| **Cross-channel** | the journey crosses inbound / outbound channels (out through a third party and back) | **orchestration-driven** + observe delivery at the external boundary stub | at the push/channel stub, assert "what was really delivered and whether it landed correctly" |

**Read at runtime**: **whether a given jump is actually streaming (SSE/WS/long-polling), the cron expression, the channel protocol, the one-time token mechanism —
always read the real implementation at runtime**, never pre-assume. **Non-UI jumps are what distinguishes this quadrant from pure frontend E2E**: advance them by orchestration, don't wait on the UI.

---

## 5. Two-layer landing: black-box traversal + structured chain assertions

For each P0 journey, land it in two layers, "black box first, structured second" (details in SKILL.md step 3):

**Layer one · black-box traversal**: run the whole journey end to end on the already-running whole-system real stack, proving "A->B->C really connects."

| E2E form (capability) | Instance examples (lookup, not the only solution) | Selection clues |
|---|---|---|
| diff-aware E2E (focused on change-related journeys) | if the environment **already has** such a tool (gstack `/qa` is one) prefer it — it focuses on the journeys this change touches, saving time | **already present** in the environment; **fall back if it is not**, this skill does not write its installation steps |
| General-purpose E2E (fallback default) | Playwright / Cypress or that stack's equivalent end-to-end driver | the general fallback when no diff-aware tool exists |
| Non-UI jump driving | fake clock / manually trigger the scheduled task / really send a message + poll-retry / observe at the external boundary stub | the journey contains scheduled / async / cross-channel jumps |

> These UI tools **only probe an already-running localhost; they do not bring the stack up** — so **whole-system bring-up (§3) MUST already be complete** (see the §0 ordering iron rule).

**Layer two · structured chain assertions**: assert point by point along the journey's **key handoff points**, hardening the safety net into a regression:
- A's output really became B's input;
- B's artifact really triggered C (including the scheduled/async "artifact -> trigger" edge);
- cross-channel delivery really landed at the correct endpoint (asserted at the external boundary stub);
- the whole journey's **final state** is really reached and consistent (waited for with poll-retry, **no fixed sleep**).

Black-box traversal only proves "it connects"; structured assertions prove "**every handoff point lines up item by item**." Write assertions with the test frameworks of the stacks the journey involves.

**Worth referencing (not a dependency)**: **Pathfinder**'s journey->E2E skeleton generation idea (generate an E2E skeleton from an excavated path) and
**Tracetest**'s trace->assertion idea (turn source B's traces directly into chain handoff-point assertions) — **not binding; if the environment lacks them, use a generic equivalent**.

---

## 6. Cross-capability general reminders

- **Excavate the subject under test first** (§1 three-source model): this is the first step unique to this quadrant; in the first three quadrants the subject is given.
  **All three sources are indispensable**: A excavates half the graph, B fills in bridge edges + decoupled edges, C backstops semantics + is the source of truth when code is not yet landed.
- **The safety-net layer covers only P0** (§2): it does not chase coverage rate; **a bug first appearing at the chain layer = lower-layer coverage gap, back-fill the lower layer** (distinctive point 2).
- **Bring up the whole-system stack first, stub only external boundaries** (§3): everything internal is real, **stubbing out an internal feature under test is forbidden** (stub it and it degrades).
  **Bring-up precedes E2E** (ordering iron rule).
- **Drive non-UI jumps by orchestration** (§4): scheduled -> fake clock / manual trigger; async/cross-channel -> poll-retry to the final state. **No sleep.**
- **Cross multiple features, do not take single slices**: a single slice within a single feature belongs to the third quadrant; this quadrant covers only cross-feature journeys.
- **Data isolation + teardown**: seed/teardown guarantees repeatability; the CI cadence is bring up -> run the journey -> tear down, cleaning up after testing to avoid leakage.
- **RED MUST be meaningful**: first confirm the test is red because of a real chain defect (not because the stack failed to come up, not because the test is wrong, not because the sleep was too short), then GREEN, then harden it.
- **Runs last / when code is not yet landed**: source C is the only source of truth, you can "excavate candidate paths + write RED E2E," and the methodology can be built before the code.
- **Guardrails**: write only tests/orchestration config, never weaken assertions, no faked fixes (including no "quietly stubbing the internal feature under test back out," no "fixed sleep
  pretending the clock arrived," no "standing up a fake service to impersonate the real stack"), bounded retries (chain flakes are not papered over by re-running or sleeping longer), isolated changes + human-reviewed delivery; on finding a real chain bug
  **HALT and hand back to superpowers TDD/debugging**, do not modify product code yourself, **and prompt for a lower-layer back-fill** (see the SKILL.md self-healing guardrails).
- **Archiving**: attach a **journey-level traceable ID** to each new regression (linking the multiple features / multiple ACs it crosses and which jumps it contains),
  tier it by risk (**P0 critical journeys hard-block at the release gate**), align with the three-layer cadence (chain E2E is the slowest, **L3**), following testing-system-blueprint-en.
```
