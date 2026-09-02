---
name: fullstack-slice-testing-en
description: Validate one real consumer-provider seam within a single feature after frontend and backend work are ready. Bring up both sides and required dependencies, reconcile mocked consumer assumptions with provider behavior, test contract authenticity, identity and serialization glue, error mapping, and applicable async timing, then tear down cleanly. Deliver isolated test changes for human review. Use directly or when routed by test-routing-advisor-en. Do not use for cross-feature journeys (those belong to full-chain-testing-en), for single-side work with no frontend-backend seam, or when only one side is finished - mocking the other side destroys the point of the reconciliation.
license: MIT
metadata:
  version: "1.0"
  lang: en
  kind: process-executor
  stage: "9.2"
  standalone: true
  produces:
    - "test code (project test directory)"
    - "evidence archive"
  requires:
    - name: "both frontend and backend closed out within the same feature"
      level: required
      fallback: "Stop - with one side missing there is nothing to reconcile"
    - name: "project manifest files for both sides"
      level: required
      fallback: "Stop - the real environment cannot be orchestrated without them"
    - name: "routing decision report"
      level: orchestration
      fallback: "Ask the user which slice to take"
    - name: "browser testing tool"
      level: optional
      fallback: "Verify at the interface layer instead, and label the UI layer as not covered"
---

# fullstack-slice-testing-en · Partial Frontend-Backend Seam Test Executor

## What This Skill Solves

`backend-testing-en` mocks out the frontend and validates the backend's real behavior in isolation; `frontend-testing-en` mocks out the backend and validates the frontend's rendering and interaction contract in isolation. Both make one side real, but both are built on **assumptions about the other side** — the mock in frontend unit tests that is hand-written or generated from a contract is essentially "a written assumption of what the frontend thinks the backend will return." **This assumption has never met the real backend.**

**Partial frontend-backend testing is that meeting.** Within a **single feature**, it connects the **single slice** between the consumer side (frontend / caller) and the provider side (backend / callee) in **real form**, **stops mocking**, and validates whether the seam truly aligns. In essence it is a **reconciliation**: the "well-intentioned lies" that the single-frontend phase told the backend in order to develop independently (field names, types, status codes, error bodies, auth headers, timing) are all exposed here.

> **Core boundary (must understand)**: This quadrant is **limited to a single slice within a single feature** and **does not cross features**.
> "A user going from feature A to feature B to feature C" — that kind of multi-feature end-to-end journey belongs to the fourth quadrant **"complete functional chain"**, not here. This quadrant asks only one question: **In this one feature, does the frontend's assumption about the backend align with the backend's real behavior?**
> When scoping the slice, **don't be greedy** — a feature may have multiple consumer→provider seams; scope the highest-risk one first, then proceed one at a time.

> **Key insight: The new challenge in this quadrant is not writing assertions, but "bringing up the real stack."** The reason the first two quadrants can each run independently is that they mock out the other side — a mock is a "cheap stand-in," always ready on demand. The entire value of this quadrant is precisely **not being allowed to mock that other side**, so you must actually bring up **both sides + the middleware they depend on** simultaneously and reproducibly. This "environment orchestration" task is a challenge the first two quadrants have never faced — it is equivalent to the frontend's "install test runner" and the backend's "bring up test libraries." **If the stack doesn't come up, all downstream assertions are moot.**

Follows the `testing-system-blueprint-en` (reference by name as needed): risk-tiered ordering, traceable IDs, release gates, three-layer cadence.

---

## Two Absolute Constraints (Read First — Apply Throughout)

1. **stack-agnostic**: All four capability gaps are expressed using "**capability description + per-stack instantiation lookup**" exclusively — never hardcode one stack as the only answer. The docker-compose / testcontainers / Playwright / Cypress / gstack `/qa` / MSW / Pact / OpenAPI and other tools appearing in this document and in `references/gaps.md` are **all just "instance examples for a certain stack/ecosystem" — never the only solution**. **Read both sides' stack manifests (`package.json` / `pyproject.toml` / `go.mod` etc.) first, then instantiate corresponding tools.** In particular, **gstack is not a hard dependency** — it is just one instance of "diff-aware E2E tool" in a certain environment; if it's not in the environment, fall back to general-purpose E2E (Playwright / Cypress etc.). This skill does not write any gstack installation steps.
2. **project-agnostic**: No business-specific terms appear here, and no specific framework or protocol is assumed. Everything **project-specific** — what the orchestration file looks like, whether the seam involves streaming (SSE / WebSocket / long-polling), specific interface shapes, token / auth mechanism, CORS policy, health check address — is **always read at runtime, never written into the skill, never pre-assumed**. Always written as **conditionals**: "**if the slice contains streaming/real-time interaction, then** …", "**if both sides declare contracts with OpenAPI, then** …". Special emphasis: **streaming is not a fixed gap** — it is a **conditionally hit** item of the "real timing capability" — non-streaming slices simply don't hit it; don't force-test it.

---

## Four Capability Gaps (All Capabilities, Not Tools)

| # | Capability gap | What it validates | Instance examples (lookup, not the only solution) |
|---|---|---|---|
| 1 | **Environment orchestration capability** (core challenge of this quadrant) | Bring both sides of the slice + dependencies up in real form, **simultaneously and reproducibly**, consistent between local and CI, with health checks passing | Container orchestration / test containers / process orchestration / in-memory test servers |
| 2 | **Contract authenticity capability** | Validate whether the consumer-side assumption (the mock used during the single-frontend phase) matches the provider-side real behavior: fields / types / status codes / error bodies | Consumer mock ↔ provider spec comparison / bidirectional contracts / schema comparison |
| 3 | **Seam adhesion capability** | Identity/credential pass-through, serialization round-trip, error → consumer-side handling mapping, headers / CORS | Real interface integration assertions |
| 4 | **Real timing/real-time capability (conditional hit)** | **Only hits if the slice contains streaming/real-time/async interaction**: validates timing and incremental behavior (process while receiving / race conditions / eventual consistency) | Streaming protocol observation |

> Gap 1 is the unique challenge of this quadrant; gap 4 is **conditionally hit** (skip directly for non-streaming slices). Gaps 2/3 are the main body of seam reconciliation.

---

## Workflow (Six-Step Closed Loop)

> The skeleton is the same structure as the first two quadrants; **differences are concentrated in step ① "bring up the real stack"** — this is the biggest unique engineering challenge of this quadrant.

### Step 0 · Identify Stack + Scope Slice

1. **Identify both sides' stacks**: Read both the consumer side and provider side stack manifests separately (`package.json` / `pyproject.toml` / `go.mod` / `pom.xml` …); all subsequent orchestration and contract tools are instantiated from these. The two sides may use different stacks (frontend JS/TS + backend Python); orchestration must accommodate both.
2. **Scope the slice**: From the contract declaration / AC / dependency graph, identify "**which single seam represents this feature's consumer→provider connection**." A feature may have multiple seams — **scope only the highest-risk single seam** first (single slice, don't be greedy), then proceed to others one at a time. While scoping, confirm that this slice **truly doesn't cross into another feature** — if it does, it belongs to the fourth quadrant "complete functional chain," not here.

> If no stack manifest is found or no clear seam can be scoped, stop and ask — don't assume.

### Step 1 · Bring Up the Real Stack (Core Challenge of This Quadrant, Cannot Be Skipped)

**This is the biggest process difference between this skill and the first two quadrants.** Equivalent to the frontend's "install test runner" and the backend's "bring up test libraries" — **if the stack doesn't come up, everything downstream is moot.** This step does only one thing: **verify / establish that "both sides of the slice + the middleware they depend on can come up in real form, one-command, reproducibly, with health checks passing,"** and ensure **local and CI behavior is consistent**.

1. Read **existing orchestration definitions in the project** (read at runtime, don't pre-assume what they look like): could be container orchestration files, process startup scripts, Makefile targets, service definitions in CI … if they exist, reuse them to make "one command brings up both sides + dependencies" work first.
2. **If no reusable orchestration exists**: instantiate a minimal orchestration for both sides' stacks (see `references/gaps.md` gap 1), bring up the provider side, consumer side, and the middleware they depend on (database / cache / queue etc. — **which ones exist, read at runtime**) together, configure health checks (wait until both sides are ready before considering the stack up — don't use a fixed sleep).
3. **Smoke-test to confirm the foundation is usable**: after bringing up the stack, first push through one simple real request (consumer truly sends, provider truly receives and responds), proving the stack is alive, then proceed to layered assertions. **Before this step is green, don't write any seam assertions.**

> ⚠️ **Ordering iron rule**: Existing E2E tools (whether gstack `/qa` or Playwright / Cypress) **typically don't handle bringing up the stack** — they only probe a **localhost address that is already running**. So **step 1 bringing up the stack must complete before step 3 runs E2E** — otherwise E2E probes an empty address, all red, and the red is meaningless.

### Step 2 · Conditional Hit (Only Test What This Slice Actually Has)

**Not all four gaps are tested** — only supplement the subset that **this slice actually hits**. Evaluate each item (see `references/gaps.md` for details):

| Gap | Hit condition | Non-hit example |
|---|---|---|
| ① Environment orchestration | **Always hits** (prerequisite of this quadrant: both sides must actually be brought up, otherwise it's not a seam test) | — (if it doesn't hit, this isn't the right quadrant) |
| ② Contract authenticity | The slice has contract drift risk — the frontend mock may not match the backend's real response | Interface shape is extremely simple and both sides share the same generated code, almost no drift risk |
| ③ Seam adhesion | The slice has auth / credential pass-through / complex serialization / defined error paths / CORS | No auth, simple JSON round-trip, no error branches |
| ④ Real timing/real-time | **The slice truly contains streaming / real-time / async interaction** (confirm the protocol at runtime, don't assume) | **Non-streaming slice** — ordinary request-response; skip directly, don't force-create timing tests |

Gap 4 is a classic "conditional hit": **first confirm at runtime whether this slice is actually streaming/real-time**, then test timing only if it is, skip if it isn't. A non-streaming slice only hitting ①②③ is completely normal — don't force-write timing assertions to fill all four.

### Step 3 · Two-Layer Landing

For each **hit** gap, land in two layers — "blackbox smoke test first, then structured assertions":

1. **First layer · Blackbox smoke test**: On the already-brought-up real stack, run an end-to-end smoke test to confirm this slice is "connected end-to-end."
   - **If a diff-aware E2E tool exists in the environment** (gstack `/qa` is one example), use it preferentially (can focus on change-related slices, saves time).
   - **Otherwise fall back to general-purpose E2E** (Playwright / Cypress or the stack equivalent).
   - Again: these tools **only probe running localhost — they don't bring up the stack** — so **step 1 must have already brought the stack up**.
2. **Second layer · Structured seam assertions**: For each hit capability (②③④), write repeatable seam assertions — this is the part that solidifies "reconciliation" into regression. Blackbox smoke only proves "it works"; structured assertions prove "fields/types/status codes/error bodies/credentials/timing **match one by one**."

> See `references/gaps.md` for specific tools and assertion patterns; take the row corresponding to both sides' stacks identified in Step 0.

### Step 4 · RED→GREEN + Data Isolation

Supplement in "cheapest hit gap first" order:

1. **Data isolation first**: Seam tests run on the real stack and require **seed / teardown fixtures** to ensure each test's data is controlled, non-polluting, and repeatable (start with known data → test → clean up). Without isolation, seam tests will produce false reds/greens due to dirty data.
2. **RED**: First write failing seam assertions, confirm they are red **because of real seam defects** (frontend assumption doesn't match backend reality, credentials not passed through, error body not mapped, timing wrong) — not because the test is written incorrectly or the stack didn't come up properly. **Red for a good reason**, then proceed.
3. **GREEN**: Make assertions go green.
   - If red exposes a **real seam bug** (typical: a well-intentioned lie the frontend mock told is now exposed here) — **HALT, don't modify product code yourself** (see self-healing guardrails), return to `superpowers:test-driven-development` / `superpowers:systematic-debugging` for fix, then return to this skill to solidify the regression.
   - If it's simply missing coverage and the seam already aligns — supplement tests and go green, no product code change needed.
4. **Assertions must not be weakened**: It is forbidden to relax assertions to make things go green (e.g., changing the status code assertion to `or 200`, deleting error body validation, commenting out timing assertions).

### Step 5 · Archive per Blueprint + Teardown + Isolated Changes for Human Review

For each newly added seam regression test:

- Ordered by **risk tier** per `testing-system-blueprint-en` into release gates — **authorization bypass / contract drift are high risk** (the former leaks others' data, the latter will crash when the real backend is live), **hard-block in release gate**; minor hint/fallback differences can be warning level.
- Attached with **traceable IDs** (associated with feature / AC / scoped slice / hit gaps).
- Aligned with **three-layer cadence**: seam tests require bringing up the real stack; they naturally belong to the slower layer (blueprint L2 integration layer) — don't stuff them into the L1 unit test layer for fast execution.
- **Teardown**: The cadence in CI is **bring up stack → test → teardown stack**; after testing, make sure to clean up the real stack and data together to avoid environment leakage polluting the next run. Same applies locally (stack bring-up and teardown come in pairs).
- Keep supplemental tests in an **isolated branch or change set for human review**; the upper-level wrap-up stage decides merge versus PR. The delivery note lists the scoped slice, hit gaps, skipped gaps and reasons, each regression's gap and risk level, and the stack bring-up and teardown approach.

---

## Four Capability Gaps Landing Structure Quick Reference (See references/gaps.md for details)

Each item = one capability gap. All tools columns are **instance examples for a certain stack/ecosystem** — instantiate by stack, not locked in.

| # | Capability gap | Instance examples (lookup, not the only solution) | Hit nature | Closure type |
|---|---|---|---|---|
| ① | Environment orchestration (this quadrant's challenge) | Container orchestration (docker-compose etc.) / test containers (testcontainers etc.) / process orchestration / in-memory test servers | **Always hits** | Fully automated (bring up stack → smoke → teardown) |
| ② | Contract authenticity | Consumer mock ↔ provider spec comparison / bidirectional contracts (e.g., Pact) / OpenAPI schema comparison | Hits only when drift risk exists | Fully automated RED→GREEN |
| ③ | Seam adhesion | Real interface integration assertions (real credential pass-through / real serialization round-trip / error mapping / headers/CORS) | Hits only when auth/error paths exist | Fully automated RED→GREEN |
| ④ | Real timing/real-time (conditional hit) | Streaming protocol observation (confirm at runtime whether it's SSE / WebSocket / long-polling / async callback, then instantiate) | **Hits only when slice truly contains streaming/real-time** | Fully automated; timing assertions are fragile and need stabilization |

---

## Key Distinctions from the First Two Quadrants (Must Be Clear)

The common prerequisite of the first two quadrants (backend-testing-en / frontend-testing-en) is: **the other side can be mocked**, allowing each to run independently and cheaply. The entire value of this quadrant is the opposite — **the other side cannot be mocked**; both sides must truly be brought up for reconciliation. This creates two fundamental differences:

1. **The new challenge is "bringing up the real stack (environment orchestration)," not writing assertions.** The challenges of the first two quadrants are in assertions (backend builds authorization/concurrency assertions from scratch, frontend translates visual contracts); the assertions in this quadrant are conventional integration-level seam assertions — **the truly hard part is step ① — making heterogeneous-stack both sides + middleware come up one-command, reproducibly, with local = CI parity**. This is an engineering challenge the first two quadrants have never faced, which is why this skill singles it out as a non-skippable core step.
2. **This quadrant is the "reconciliation" of the first two quadrants.** Frontend-only, for the sake of independent development, told a mock "lie" about the backend (the frontend's assumption of what the backend would return); backend-only each managed its own real behavior. **These two sides' realities/assumptions have never been reconciled.** This quadrant is that reconciliation — **the well-intentioned lie the frontend mock told is exposed here.** This also explains why gap ② "contract authenticity" is the main body: it specifically catches the delta between "assumption vs. reality."

---

## Self-Healing Guardrails (Must Not Be Crossed)

The supplemental test process allows bounded automated iteration (bring up stack → RED → GREEN → teardown), but is constrained by the following guardrails (inherited from the blueprint):

- **Only write tests / orchestration config, don't change product code** — this is the default action. This skill is responsible for bringing up the stack, configuring orchestration, and writing seam assertions — **not modifying business implementation**.
- **Assertions must not be weakened** — it is forbidden to relax assertions to make things go green (e.g., loosening the status code assertion to `or 200`, deleting error body validation, commenting out timing assertions, shrinking the contract comparison field set). Going green must come from correct product code or correct tests — not from lowering the standard.
- **Fake fixes are forbidden** — it is not permitted to fake a pass using `skip`, a fixed `sleep` pretending to be ready, secretly mocking back the side that is not supposed to be mocked, or bringing up a fake backend pretending to be the real stack. **Once this quadrant mocks out the side being tested, it degrades to the first two quadrants and loses all its value.**
- **Bounded retry escalation** — stack bring-up/timing naturally has flakiness (port contention, health check jitter, streaming incremental out-of-order); automated iteration has an upper limit; reaching it means stop and escalate to a human — **never use "one more run will fix it" to mask real seam instability**.
- **Isolated changes + human review** — keep orchestration config and seam regressions in an isolated branch or change set for review; the upper-level wrap-up stage decides merge versus PR.
- **Discovering a real bug requires HALT, return to superpowers for fix** — this skill **does not modify product code itself**. During supplemental testing, if RED exposes a real seam defect (frontend assumption doesn't match backend reality, credentials not passed through, error not mapped, timing wrong), **stop**, return the defect to `superpowers:test-driven-development` / `superpowers:systematic-debugging` for a fix cycle, then return to this skill to solidify the regression.

The purpose of these guardrails: allow seam reconciliation to run automatically, but block any shortcut of "mocking back the side being tested," "pretending to pass without the real stack up," or "crossing the line to modify product code."

---

## Relationship to Upstream and Downstream

- Upstream: `test-routing-advisor-en` calls this skill when it determines "partial frontend-backend" (can also be triggered directly by the user).
- Blueprint: all archiving / tiering / release gates / cadence follow `testing-system-blueprint-en` (reference by name; its content is not replicated here).
- Siblings: `backend-testing-en` (backend-only) / `frontend-testing-en` (frontend-only) — this quadrant is the **reconciliation** of those two: they each mock out the other side and independently validate their own reality, this quadrant brings both sides up to validate the seam, exposing the well-intentioned lies that the single-frontend mock told.
- Boundary: **multi-feature end-to-end journeys** belong to the fourth quadrant "**complete functional chain**," not here; this quadrant only handles single slices within a single feature.
- Methodology reuse: Fix and debug of discovered real seam defects reuses `superpowers:test-driven-development` and `superpowers:systematic-debugging` (this skill HALTs and returns to them).

## Upstream Artifacts

| Artifact | Level | When missing |
|---|:---:|---|
| Both sides closed out within the same feature | **required** | Stop - with one side missing there is nothing to reconcile |
| Project manifest files for both sides | **required** | Stop - the real environment cannot be orchestrated |
| Routing decision report | orchestration | Ask the user which slice to take |
| Browser testing tool | optional | Verify at the interface layer instead; label the UI layer as not covered |

## Downstream Consumers

| Consumer | What it reads |
|---|---|
| The full chain skill | A reconciled slice, as trustworthy ground |
| Branch close-out | The seam risks |

## Standalone Use

**What you provide**: a feature with both frontend and backend closed out, plus both sides'
dependency manifests.

**What you get**: one slice verified with the mocks removed and the real shapes joined -
environment orchestration, contract reality, seam glue, real-time ordering.

**What you don't get**:

- **One slice within one feature only** - journeys spanning several features belong to the
  full chain skill.
- **It does not work with only one side present**: this is the one prerequisite that cannot
  be degraded, because mocking either side destroys the point of the reconciliation.
- The new difficulty is standing the real stack up rather than writing assertions; where
  environment orchestration is unavailable, this skill does not apply.
