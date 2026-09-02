# Four Partial Frontend-Backend Seam Gaps · Capability Layer + Per-Stack Instantiation

> How to use: first identify **both sides'** stacks per SKILL.md step 0 (consumer side + provider side may differ), then read the row for that stack under the matching gap to instantiate tools.
> Each gap states the **capability** first (stack-agnostic, always true), then gives **instance examples**. Examples are a lookup, **not the only answer** —
> what stack the project uses, what libraries it installs, what orchestration it picks is decided by the project itself; this table only maps "capability -> tool for that stack/ecosystem."
>
> **The core difficulty of this skill is gap 1, "bringing up the real stack"**: the first two quadrants can mock out the other side and run cheaply in isolation; this quadrant may not mock,
> it must actually bring both sides + dependencies alive. Equivalent to the frontend's "install the runner" and the backend's "bring up the test libraries" — **if the stack doesn't come up, nothing downstream matters.**
>
> **Every "project-specific" input is read at runtime and conditional**: what the orchestration file looks like, whether the seam is streaming (SSE / WS / long-polling / async callback),
> interface shapes, token/auth mechanism, CORS policy, health-check address, which middleware dependencies exist — **always read at runtime, never written into this table,
> never pre-assumed**. Anything touching contracts/streaming is always written as "**if the slice contains X, then** …".

## Contents

0. [Prerequisite discipline for bringing up the real stack (ordering iron rule + data isolation)](#0-prerequisite-discipline-for-bringing-up-the-real-stack-ordering-iron-rule--data-isolation)
1. [1. Environment orchestration capability (core difficulty of this quadrant, always hit)](#1-environment-orchestration-capability-core-difficulty-of-this-quadrant-always-hit)
2. [2. Contract authenticity capability](#2-contract-authenticity-capability)
3. [3. Seam adhesion capability](#3-seam-adhesion-capability)
4. [4. Real timing / real-time capability (conditional hit)](#4-real-timing--real-time-capability-conditional-hit)
5. [Two-layer landing: black-box smoke + structured seam assertions](#two-layer-landing-black-box-smoke--structured-seam-assertions)
6. [Cross-gap general reminders](#cross-gap-general-reminders)

---

## 0. Prerequisite discipline for bringing up the real stack (ordering iron rule + data isolation)

**Capability**: before adding any seam assertion, first make "both sides of the slice + dependent middleware come up in real form with one command, reproducibly, with health checks passing" hold.
This is a prerequisite step unique to this quadrant; the first two quadrants have none (they mock out the other side and just run).

**Why this quadrant needs this step specifically**: the definition of this quadrant is "you may not mock the other side under test." Once you mock it back, it degrades into the first two quadrants and loses all meaning.
So the stack must really come up — and bringing up two sides on different stacks (e.g. frontend JS/TS + backend Python) + middleware (DB/cache/queue) simultaneously, reproducibly, local == CI,
is itself an engineering difficulty, and it is the entrance to all of this quadrant's value.

**Ordering iron rule (the most commonly stepped-in pit)**: off-the-shelf E2E tools — whether diff-aware (such as gstack `/qa`) or general-purpose
(Playwright / Cypress) — **usually do not bring the stack up; they only probe an already-running localhost address**.
So **bringing up the stack (gap 1) MUST be completed before running E2E (the first layer of two-layer landing)**; reverse the order and E2E probes an empty address, going all red in a way that means nothing.

**Data isolation discipline (mandatory for seam testing)**: seam tests run on a real stack, so there MUST be **seed / teardown fixtures** —
each test brings up a set of **known data** -> tests -> **clears it**, guaranteeing controllability, no cross-contamination, repeatability. Without isolation, seam tests go falsely red/green on dirty data.

**Teardown discipline**: the cadence in CI and locally is **bring up -> test -> tear down**; after testing, always clean up the real stack together with its data to avoid environment leakage polluting the next run.

---

## 1. Environment orchestration capability (core difficulty of this quadrant, always hit)

**Capability**: bring both sides of the slice (consumer side + provider side) + the middleware they depend on up in real form **simultaneously, reproducibly, and consistently between local and CI**,
and confirm with **health checks** that both sides are genuinely ready (ready means ready, **not a fixed `sleep`**).

**Why this is the core difficulty of this quadrant**: this is something the first two quadrants never faced — each of them brings up only one side and mocks the other. This quadrant must assemble two differently-stacked sides + middleware
into a real runnable small system: ports, networking, dependency startup order, health checks, local/CI consistency — every one has to be made real. **If the stack doesn't come up, nothing downstream matters.**

| Orchestration form (capability) | Instance examples (lookup, not the only solution) | Applicability clues |
|---|---|---|
| Container orchestration | docker-compose / equivalent compose tooling, defining both sides + middleware as services + healthcheck | both sides already containerized, many middleware dependencies |
| Test containers (containers started from code) | testcontainers (available in many languages: Java/Node/Python/Go…), starting/stopping real dependencies within the test lifecycle | you want stack bring-up hosted by test code, decoupled from CI |
| Process orchestration | process management script / Makefile target / Procfile-style, bringing up both sides' processes locally + waiting on health checks | lightweight, not containerized, few dependencies |
| In-memory / in-process test server | that stack's in-memory HTTP test server (only when "real form" permits in-process) | provider side can run for real in-process, no separate deployment needed |

**Read at runtime, do not pre-assume**: if the project **already has orchestration definitions** (compose file / startup script / CI service block), reuse them;
only if it has none do you instantiate a minimal orchestration per the table above. **Which middleware dependencies exist (DB/cache/queue/object storage…) is read at runtime**, not hardcoded in this table.

**Typical landing checklist**: one command brings up both sides + dependencies; health checks wait until both sides are ready; a smoke request goes through end to end proving the stack is alive;
seed/teardown data isolation is in place; tear the stack down after testing. **Write no seam assertions before this step is green.**

---

## 2. Contract authenticity capability

**Capability**: validate whether the **consumer side's assumption** (the mock it used during the frontend-only phase in order to develop independently) matches the **provider side's real behavior** —
reconciling item by item: **field names / types / required-vs-optional / status codes / error body structure**. This is the main body of this quadrant, hunting specifically for "assumption vs reality" drift.

**Why it matters**: the mock in frontend unit tests has never met the real backend. Renamed fields, changed types, restructured error bodies, newly required fields —
the mock never follows automatically. **Frontend-only stays green forever, and collapses on the real backend.** This quadrant is where that lie is exposed on the real stack.

| Reconciliation form (capability) | Instance examples (lookup, not the only solution) | Notes |
|---|---|---|
| Consumer mock <-> provider spec comparison | compare the shape of the frontend's mock field by field against the provider's real response (or its OpenAPI/schema) | most direct; catches field/type/status-code drift |
| Bidirectional contracts (consumer-driven contract) | Pact (multi-language) / equivalent CDC tooling: the consumer publishes expectations, the provider side verifies it satisfies them | each side's CI verifies independently; strong constraint, prevents two-way drift |
| OpenAPI / schema comparison | **if the provider declares contracts with OpenAPI/JSON Schema, then** validate real responses against the schema + compare with the frontend's assumption | first choice when the provider has a contract source |

**Read at runtime**: **whether a contract source exists, and whether it is OpenAPI or Pact or a bare schema — read at runtime**; with no contract source, directly compare real response samples against the frontend mock.

**Typical assertion checklist**: real response field set == frontend assumed field set (nothing extra, nothing missing); types match field by field; success status codes match;
**error body structure** matches the frontend's error-handling expectation (a classic drift point); required fields are not absent from the real response.

---

## 3. Seam adhesion capability

**Capability**: validate that the "glue layer" where the two sides really meet lines up — **identity/credential pass-through, serialization round-trip, error -> consumer-side handling mapping, headers/CORS**.
These are where "the interface shape is right but the seam still leaks": the shape matches, yet it really fails because the token was not passed through, date/number serialization round-trips lossily, error codes are not mapped to the right UI state,
or CORS/headers are not configured.

**Why it matters**: contracts (gap 2) only govern "shape"; adhesion governs "the seams that appear when things are really connected." Single-side testing never touches them —
in the frontend mock the token is always "valid," serialization is always "perfect," errors always come back exactly as the frontend imagined. Only on a real stack do these seams show.

| Adhesion dimension (capability) | What it validates | Instance examples (lookup, not the only solution) |
|---|---|---|
| Credential pass-through | a real token/session is emitted by the consumer and genuinely validated by the provider; invalid credentials are genuinely rejected | real interface integration assertions: hit the real endpoint with real credentials, assert the status code |
| Serialization round-trip | dates/numbers/enums/nested structures do not lose fidelity after real serialization -> deserialization | send known values, assert the real returned values are equal field by field |
| Error -> handling mapping | real provider errors (4xx/5xx/business error codes) are correctly mapped by the consumer side to the corresponding handling/state | trigger the real error path, assert the consumer side lands in the correct fallback/error state |
| Headers / CORS | real CORS / content negotiation / custom headers are not blocked in cross-origin integration | make a real cross-origin request, assert it is not blocked by preflight/header policy |

**Read at runtime**: **the auth mechanism (Bearer/Cookie/signature…), CORS policy, custom headers — read both sides' implementations at runtime**, do not pre-assume.

**Typical assertion checklist**: real credentials -> allowed, missing/wrong credentials -> genuinely rejected; known dates/large numbers/enums are equal after a round trip; when the provider returns a business error code
the consumer side lands in the corresponding error state (not "pretending success"); cross-origin requests are not blocked by CORS/preflight.

---

## 4. Real timing / real-time capability (conditional hit)

**Capability**: **hit only when this slice genuinely contains streaming / real-time / async interaction** — validate **timing and incremental behavior**: whether process-while-receiving is correct,
whether ordering holds under concurrency/races, whether it converges in the end. **Confirm the protocol at runtime first** (which of SSE / WebSocket / long-polling / async callback it is), then instantiate.

**Why it is a conditional hit rather than a fixed gap**: **the vast majority of slices are ordinary request-response** with no timing dimension at all — forcing timing assertions onto them is pure over-testing.
**Streaming is not a fixed gap, it is a conditionally hit item**: for non-streaming slices, skip gap 4 outright. Confirm at runtime whether this slice actually streams, and only then test it.

| Real-time form (capability) | Instance examples (lookup, not the only solution) | What it validates |
|---|---|---|
| Server push-stream observation | a streaming-protocol observing client (instantiate the matching observation method per the real protocol — SSE/WS/long-polling etc.) | incremental chunks arrive in order, processed while received, nothing lost, reordered, or duplicated |
| Async callback/event | real event/callback channel observation + waiting assertions (poll to the final state, no fixed sleep) | eventual consistency, callbacks genuinely delivered, idempotent |
| Concurrent timing | multiple consumers/events triggered concurrently, observing ordering and consistency under races | no lost updates, no error states caused by reordering |

**Read at runtime**: **what the protocol actually is, chunk boundaries, termination signal, heartbeats — always read the real implementation at runtime**, never hardcode "SSE" or any other specific protocol as a premise.

**Typical assertion checklist (streaming/real-time slices only)**: incremental chunks arrive in the expected order; the client renders/processes correctly while receiving; stream interruption/reconnection recovers as expected;
the async final state is reached within the time limit and is idempotent; concurrent triggering produces no reordering-induced errors.

---

## Two-layer landing: black-box smoke + structured seam assertions

For each **hit** gap, land it in two layers, "black box first, structured second" (details in SKILL.md step 3):

**Layer one · black-box smoke**: run an end-to-end smoke test on the already-running real stack, proving "the whole slice connects."

| E2E form (capability) | Instance examples (lookup, not the only solution) | Selection clues |
|---|---|---|
| diff-aware E2E (focused on change-related slices) | if such a tool exists in the environment (gstack `/qa` is one) prefer it — it can focus on the slice this change touches, saving time | the tool is **already present** in the environment; **fall back if it is not**, this skill does not write its installation steps |
| General-purpose E2E (fallback default) | Playwright / Cypress or that stack's equivalent end-to-end driver | the general fallback when no diff-aware tool exists |

> These tools **only probe an already-running localhost; they do not bring the stack up** — so **gap 1 stack bring-up MUST already be complete** (see the §0 ordering iron rule).

**Layer two · structured seam assertions**: for each hit capability (2/3/4), write repeatable seam assertions that harden the "reconciliation" into a regression.
Black-box smoke only proves "it connects"; structured assertions prove "fields/types/status codes/error bodies/credentials/serialization/timing **line up item by item**."
Write assertions with the test frameworks of both sides' stacks (the consumer-side or provider-side test runner, instantiated per the stack identified in §0).

---

## Cross-gap general reminders

- **Bring up the real stack first** (step 1 / §0): the difficulty unique to this quadrant; if the stack doesn't come up, nothing downstream matters. **Bring-up precedes E2E** (ordering iron rule).
- **You may not mock the side under test**: once you mock the other side back in, it degrades into the first two quadrants and loses all meaning (no faked fixes).
- **Hit conditions first, then fill** (SKILL.md step 2): gap 1 always hits; **gap 4 (streaming/real-time) is a conditional hit — non-streaming slices skip it outright**,
  do not manufacture timing tests; gaps 2/3 depend on whether the slice genuinely carries drift risk/auth/error paths.
- **Single slice, don't be greedy, don't cross features**: if a feature has several seams, take them one at a time, scoping the highest-risk single one first; crossing multiple features belongs to the fourth quadrant.
- **Data isolation + teardown**: seed/teardown guarantees repeatability; the CI cadence is bring up -> test -> tear down, cleaning up after testing to avoid leakage.
- **RED MUST be meaningful**: first confirm the test is red because of a real seam defect (not because the stack failed to come up, not because the test is wrong), then GREEN, then harden it into a regression.
- **Guardrails**: write only tests/orchestration config, never weaken assertions, no faked fixes (including no "quietly mocking the side under test back in," no "fixed sleep pretending ready,"
  no "standing up a fake backend to impersonate the real stack"), bounded retries (stack bring-up / timing flakes are not papered over by re-running), isolated changes + human-reviewed delivery; on finding a real seam bug **HALT and hand back to
  superpowers TDD/debugging**, do not modify product code yourself (see the SKILL.md self-healing guardrails).
- **Archiving**: attach a traceable ID to each new regression, tier it by risk (**privilege escalation / contract drift = high, hard-blocking at the release gate**), align with the three-layer cadence
  (seam testing brings up a real stack, so it belongs to the slower L2 integration layer), following testing-system-blueprint-en.
