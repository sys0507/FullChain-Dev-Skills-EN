# Category -> capability -> routing (stack-agnostic)

This table maps scenario categories to **testing capabilities** and to a **routing
destination** — **hardcoding no single-stack tool**. The capabilities are stack-agnostic
("real-database data-layer verification", "concurrency atomicity verification",
"object-level authorisation verification"); **the concrete tools are instantiated by the
executor skill that receives the routing**, which identifies the stack by reading
`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml` and the like, then picks that
stack's tools. This skill only classifies, marks gaps and routes; it does not pick tools on
the project's behalf.

> Methodology follows the `testing-system-blueprint-en` skill as its blueprint; this table
> is that blueprint landed in the feature close-out routing step.

## Status legend

- **Executor built** — this category has its executor skill; route directly.
- **Placeholder, to be built** — the category's executor skill does not exist yet; mark the
  placeholder now, and the routing takes effect once it is built.

## At a glance: category -> capability -> routing

| Category | Testing capabilities needed (stack-agnostic) | Routes to (executor skill) | Status |
|---|---|---|---|
| Backend only | Real-database data layer and migrations, concurrency atomicity, resilience and degradation, object-level authorisation (BOLA, BFLA), optional contract fuzzing | `backend-testing-en` (resolves tools per stack) | Executor built |
| Frontend only | L0/L1 test foundation, L2 visual regression, L3 a11y, L4 cross-browser + responsive, L6 frontend-backend contract mocking (design tokens and hardcoded colours go to the lint gate) | `frontend-testing-en` (wires mature tools per stack, configures them, translates visual contracts) | Executor built |
| Local full-stack slice | 1. Environment orchestration (both sides + dependencies up simultaneously and reproducibly) 2. Contract reality (consumer mock versus real provider) 3. Seam glue (identity propagation / serialisation / error-to-UI mapping) 4. Real-time ordering (conditional: streaming or async only) | `fullstack-slice-testing-en` (stands the real stack up per stack and adds seam assertions; a diff-aware E2E tool is optional, fall back where absent) | Executor built |
| Full functional chain | 1. Path excavation (semi-automatic enumeration from the dependency graph, cross-module contracts and ACs + human confirmation) 2. Criticality grading + take few (P0 safety net, not exhaustive) 3. Whole-system orchestration + external boundary stubs (stub only external third parties) 4. Async / time / cross-channel continuity (fake clock / manual job trigger / poll-retry, no sleep) 5. Journey-level traceability + safety-net localisation (first appearance means backfill a lower layer) | `full-chain-testing-en` (excavates paths per stack, orchestrates the whole system, drives non-UI hops; the UI-traversable segment folds a diff-aware E2E in here, optional, fall back where absent) | Executor built |
| Cross-module contract (candidate category) | Derive a spec from a typed producer -> downstream codegen -> breaking-change diff | That category's skill | Placeholder, to be built |
| (further categories...) | Depends on the project's actual signals | Depends on the nature of that category | Placeholder, to be built |

The details for each category follow. This table describes only "what capability is needed
and who it routes to"; **the concrete tool names come from the executor skill, per stack**.

## Backend only -> routes to `backend-testing-en`

The concrete tools for backend-only work are **not hardcoded in this skill**. This skill
only judges "this is backend-only, and these capability gaps are hit", and hands the gaps,
with the reason each was hit, to the `backend-testing-en` skill, which reads
`pyproject.toml`, `package.json`, `go.mod`, `Cargo.toml` and the like to identify the stack
and pick its tools. Below are only the **stack-agnostic capabilities** and their
"available / must be built" judgements (the multi-stack examples are illustrative, not fixed
answers):

- **Base unit layer:** use **the unit-testing framework the project's stack already uses**;
  all gap work hangs off it, and no second framework is introduced.
  *(Multi-stack examples: Python stacks commonly use `pytest`; JS/TS stacks `vitest` or
  `jest`; Go the built-in `testing`; Rust the built-in `#[test]` — decided by
  `backend-testing-en` per stack, not specified here.)*
- **Real-database data layer and migrations (available):** needs the capability to "run
  migrations up and down as a round trip against a real database, plus constraint and
  serialisation verification". **Only a real database catches the schema, constraint and
  serialisation bugs a mock conceals.**
  *(Multi-stack examples: Python has `pytest-alembic` with `pytest-postgresql`; any stack
  can use `testcontainers` — chosen by `backend-testing-en` per stack.)*
- **Concurrency / races / rate-limit atomicity (available):** needs the capability to "fire
  N concurrent requests inside one test and assert rate limits, quotas and unique
  constraints are not broken".
  *(Multi-stack examples: Python `pytest-run-parallel` with `asyncio.gather`; Go goroutines
  with `-race`; JS/TS `Promise.all` — per stack.)*
- **Resilience / fault injection (available):** needs the capability to "inject timeouts and
  error sequences into external dependencies, simulating success on the Nth retry or
  triggering degradation and fallback".
  *(Multi-stack examples: Python httpx stacks `respx` or `pytest-httpx`; Node `nock` or
  `msw`; other stacks their own HTTP mocking library — per stack.)*
- **Contract fuzzing (available, optional):** needs the capability to "fuzz automatically
  from an interface spec and check whether endpoints enforce authorisation".
  *(Multi-stack examples: where an OpenAPI spec exists, tools such as `Schemathesis` — per
  stack.)* Note it can only test **whether** authorisation exists; it **cannot test
  object-level escalation** (see below).
- **Object-level authorisation, BOLA and BFLA (must be built; the judgement is
  stack-agnostic):** there is no off-the-shelf answer — this is business semantics, no stack
  has a plug-and-play tool, and the two-user assertion logic must be built (the approach is
  in `backend-gaps.md`). This judgement does not vary by stack.
- **Routing note:** this skill hands the list of hit capability gaps to `backend-testing-en`;
  any agent behaviour that writes or fixes tests is bound by the five guardrails (see
  `self-healing-guardrails.md`). Defect-hardening methodology reuses the TDD /
  systematic-debugging practice `testing-system-blueprint-en` points at ("for a bug, write
  the failing test first", then fix).
- **Conditional hits / over-testing guard:** the capabilities above are **not all marked** —
  take the subset by what the feature actually touched (see "conditional hits" below and
  `backend-gaps.md`). A simple backend that is pure logic or read-only may hit none of them,
  where TDD plus contracts is enough. Within one stack, never introduce a second unit
  framework.

### Conditional hits (over-testing guard)

Decide which gaps to mark by what this feature actually touched; do not mark them
indiscriminately (the concrete tools are chosen by `backend-testing-en` per stack):

| What this feature actually touched | Capability gap hit | Available / must be built |
|---|---|---|
| Database writes / constraints / migrations | Real-database data-layer verification | Available (pick a real-database or container tool per stack) |
| Multiple users / per-user data isolation / privileged endpoints | Object-level authorisation (BOLA/BFLA) | **Must be built** (see backend-gaps.md; stack-agnostic) |
| Shared resources / rate limits / quotas | Concurrency atomicity verification | Available (pick a concurrency load approach per stack) |
| Calls to external dependencies (external APIs, model services) | Resilience / fault-injection verification | Available (pick an HTTP mocking library per stack) |
| Pure logic or read-only simple backend | Nothing hit | TDD plus contracts is enough |

## Frontend only -> routes to `frontend-testing-en`

**Classification condition:** changes land **in the frontend layer alone** (components,
pages, styles, frontend routing, frontend state), with no backend business logic and no
integration against a live backend — live integration belongs to "full functional chain".

The concrete tools are **not hardcoded in this skill**. This skill only judges "this is
frontend-only, and these structural gaps are hit", and hands them, with the reason each was
hit, to the `frontend-testing-en` skill, which reads `package.json` (including framework and
test-runner clues) to identify the stack and wires the corresponding tools. **The difference
in shape, in one sentence: the backend executor writes test code itself, while the frontend
executor wires mature tools (stylelint, Vitest + RTL, Playwright, axe, MSW), configures them
and translates the project's visual contracts into assertions — and its only human-review
point is adjudicating the L2 visual baseline.** Below are only the **stack-agnostic
capabilities** and their approaches (multi-stack examples are illustrative, not fixed
answers):

- **L0/L1 test foundation (frequently zero; the first action):** many projects' `[FE]`
  outputs say only "tested manually" with no test runner installed, so the foundation itself
  is missing. `frontend-testing-en`'s **first action is to lay it** — wire Vitest + RTL (or
  an equivalent component testing library) for the stack and get a minimal render and
  interaction case passing; all gap work then hangs off it, with no second framework.
- **L2 visual regression (wire a tool, translate the contracts):** snapshot and
  regression-compare pixels, dark mode and colour contracts; translate the project's visual
  contracts into assertions. *(Multi-stack examples: Playwright screenshot snapshots — per
  stack.)* **The only human-review point: adjudicating the L2 visual baseline** (a changed
  baseline snapshot needs a person to confirm intended redesign versus regression).
- **L3 accessibility (wire a tool):** automatic auditing of contrast, ARIA and labels.
  *(Multi-stack examples: the `axe` family — per stack.)*
- **L4 cross-browser + responsive (wire a tool):** multi-viewport runs plus geometry
  assertions such as "no horizontal scrollbar". *(Multi-stack examples: Playwright with
  multiple projects and viewports — per stack.)*
- **L6 frontend-backend contract mocking (wire a tool; drift protection):** intercept the
  frontend's outbound calls with mocks generated from the interface spec, so the frontend
  cannot silently keep reading an old shape while the contract drifts. *(Multi-stack
  examples: MSW with handlers generated from OpenAPI — per stack.)*
- **Design tokens / hardcoded colours -> the lint gate, not a test:** whether colours,
  spacing and font sizes are hardcoded or go through tokens is blocked by a lint rule at the
  gate, not written as a test case. *(Multi-stack examples: `stylelint` with custom rules —
  per stack.)*
- **Routing note:** this skill hands the list of hit capability gaps to
  `frontend-testing-en`; any agent behaviour that writes or fixes tests is bound by the five
  guardrails (see `self-healing-guardrails.md`).
- **Conditional hits / over-testing guard:** the capabilities above are **not all marked** —
  mark L2 only where there are visual, dark mode or colour contracts; L3 only for
  interactive components; L4 only for multiple viewports or responsive behaviour; L6 only
  where it calls a backend endpoint. The hit rules are in "conditional hits" below and in
  `frontend-gaps.md`.

### Conditional hits (over-testing guard)

| What this feature actually touched | Capability gap hit | Approach |
|---|---|---|
| Any frontend change (the foundation is usually zero) | L0/L1 test foundation | First action: lay the foundation per stack (Vitest + RTL and similar) |
| Visual / dark mode / colour contracts | L2 visual regression | Wire a tool and translate the contracts (human adjudication of the L2 baseline) |
| Interactive components / forms / controls | L3 a11y | Wire a tool (axe and similar) |
| Multiple viewports / responsive / mobile | L4 cross-browser + responsive | Wire a tool (multiple viewports + geometry assertions) |
| Calls to backend endpoints | L6 frontend-backend contract mocking | Wire a tool (MSW with OpenAPI generation, drift protection) |
| Hardcoded colours / design tokens | The lint gate | Do not write a test; a lint rule blocks it at the gate |

## Local full-stack slice -> routes to `fullstack-slice-testing-en`

**Classification condition:** changes land in **both frontend and backend**, and the seam
**does not cross the feature boundary** (journeys spanning several features belong to "full
functional chain"). In essence, a single-slice reconciliation of *real frontend to real
backend* within one feature.

The concrete tools are **not hardcoded in this skill**. This skill only judges "this is a
local full-stack slice, and these seam gaps are hit", and hands them, with the reason each
was hit, to the `fullstack-slice-testing-en` skill, which reads the project's stack
(`package.json`, `pyproject.toml`, `docker-compose.yml`) and wires the corresponding tools.
**The difference in shape, in one sentence: the new difficulty here is standing the real
stack up (environment orchestration) rather than writing assertions; it is a reconciliation
between the frontend's mocks and the backend's reality; the first layer is an optional
diff-aware E2E black-box smoke (fall back to Playwright where absent), and the second layer
adds structured seam assertions.** Below are only the **stack-agnostic capabilities**
(multi-stack examples are illustrative, not fixed answers):

- **1. Environment orchestration (the first action; where the new difficulty lives):** needs
  the capability to "get the frontend, the backend and the real dependencies (data store,
  cache, external services) up simultaneously and reproducibly". This is the first hurdle
  separating this category from single-side work — the assertions are easy to write, the
  real stack is hard to stand up.
  *(Multi-stack examples: `docker-compose` for the whole stack; in-process ASGI/WSGI
  assembly plus `testcontainers` for real dependencies; a one-command stack tool where the
  project has one — preferred where present, falling back where absent, per stack.)*
- **2. Contract reality (seam reconciliation):** needs the capability to "replace the
  consumer mock used in the frontend-only stage with the real provider and reconcile whether
  the shapes match". Green against a mock does not mean the real backend returns the same
  shape — this gap exists to catch that divergence.
  *(Multi-stack examples: replay real backend responses to validate the frontend's MSW
  handlers; or diff an OpenAPI spec in both directions — per stack.)*
- **3. Seam glue (identity propagation / serialisation / error-to-UI mapping):** needs the
  capability to "assert the identity token really propagates across processes, both sides
  agree on serialisation conventions, and backend error states map correctly to UI states".
  Neither side's tests can see these glue points.
  *(Multi-stack examples: drive the whole request path with real auth headers and assert the
  UI renders the corresponding error state — per stack.)*
- **4. Real-time ordering (conditional: streaming or async only):** needs the capability to
  "assert timing and incremental arrival for streaming, async or real-time push". **Marked
  only when this feature actually involves streaming, async or real-time push**; otherwise
  not marked (over-testing guard).
  *(Multi-stack examples: SSE or WebSocket increment assertions; polling arrival ordering
  assertions — per stack.)*
- **Routing note:** this skill hands the list of hit seam gaps to
  `fullstack-slice-testing-en`; any agent behaviour that writes or fixes tests (including a
  diff-aware E2E tool) is bound by the five guardrails (see `self-healing-guardrails.md`).
- **Conditional hits / over-testing guard:** the capabilities above are **not all marked** —
  any change touching both sides marks gap 1 first; mark gap 2 where a consumer mock needs
  reconciling against a real provider; mark gap 3 where identity crosses processes, where
  serialisation matters, or where error states must map to the UI; mark gap 4 **only for
  streaming, async or real-time**. The hit rules are in "conditional hits" below and in
  `fullstack-slice-gaps.md`.

### Conditional hits (over-testing guard)

| What this feature actually touched | Seam gap hit | Approach |
|---|---|---|
| Any change touching both sides | 1. Environment orchestration | First action: stand the real stack up per stack (docker-compose, in-process assembly + testcontainers) |
| A consumer mock in the frontend plus a real provider in this feature | 2. Contract reality | Swap the mock for the real provider and reconcile the shapes |
| Identity across processes / serialisation / error states mapped to UI | 3. Seam glue | Drive with real auth headers and assert the UI error states |
| Streaming / async / real-time push | 4. Real-time ordering | Wire a tool and assert incremental arrival ordering (**marked only for streaming or async**) |
| No frontend-backend seam (pure single side) | Nothing hit | Belongs to backend-only or frontend-only, not here |

## Full functional chain -> routes to `full-chain-testing-en`

**Classification condition:** the path under test **crosses the feature boundary and spans
several features** (a single slice within one feature belongs to "local full-stack slice").
In essence, an end-to-end journey across several features, including non-UI hops (scheduled,
async, cross-channel).

The concrete tools are **not hardcoded in this skill**. This skill only judges "this is a
full functional chain, and these chain gaps are hit", and hands them, with the reason each
was hit, to the `full-chain-testing-en` skill, which reads the project's stack and wires the
corresponding tools. **The difference in shape, in one sentence: this category is the most
distinctive — the subject under test (the path) must be excavated first (the previous three
categories are handed their subject); and it is the safety-net layer, so a bug found here
first means a lower layer under-tested it and that layer should be backfilled. The first
layer, the UI-traversable segment, is an optional diff-aware E2E (falling back where
absent); the non-UI hops are orchestration-driven.** Below are only the **stack-agnostic
capabilities** (multi-stack examples are illustrative, not fixed answers):

- **1. Path excavation (the first action; unique to this category):** needs the capability to
  "**use three sources** (static code graph + runtime trace + spec contracts) to
  semi-automatically enumerate the end-to-end paths that are currently connected, then have
  a person confirm which are genuine journeys". The previous three categories are handed
  their subject; here it hides in the dependency graph and must be excavated — which is
  exactly where this advisor's distinctive move, "derive from the dependency graph that
  A->B->C is connected for the first time", lands. **Empirical boundary: a static graph
  reaches only half the graph** — framework-wrapped frontend-backend bridge edges and
  cron/async decoupled edges cannot be stitched statically (observed across two projects),
  and must come from runtime tracing or spec contracts; where the code has not landed, spec
  contracts are the only source. See gap 1 in `full-chain-gaps.md`.
  *(Multi-stack examples, all optional instances and not dependencies: static-graph tooling;
  runtime tracing; event-storming to comb domain event flows; a project's own journey tool
  where it has one — preferred where present, falling back to manual combing, per stack.)*
- **2. Criticality grading + take few (P0 safety net, not exhaustive):** needs the capability
  to "grade the excavated paths by criticality and take only a small handful of the highest
  priority as a safety net". Exhaustiveness is the lower layers' responsibility; end-to-end
  is the slowest and most brittle, and more of it degrades the signal. Grading follows P0-P3
  in `testing-system-blueprint-en`.
- **3. Whole-system orchestration + external boundary stubs (stub only external third
  parties):** needs the capability to "stand the entire cross-feature system up for real and
  reproducibly, stubbing only the outermost third-party boundary (payments, external models,
  third-party push) while everything inside runs against the real assembly". The stack is
  larger than in a local slice, and nothing inside the external boundary may be stubbed —
  otherwise it is not end to end.
  *(Multi-stack examples: docker-compose for the whole system, or in-process assembly of
  several features' real handlers; WireMock or record-and-replay for the external boundary
  stubs — per stack.)*
- **4. Async / time / cross-channel continuity (conditional: scheduled, async or
  cross-channel only):** needs the capability to "stitch together and assert continuity
  across the non-UI hops the UI cannot reach" — a fake clock to fast-forward to the scheduled
  point, manual job triggers or message injection to pull async steps forward, and bounded
  poll-retry to assert arrival. **`sleep` is forbidden** (it makes tests slow and flaky).
  **Marked only when the journey contains scheduled, async or cross-channel hops**; a purely
  synchronous UI journey does not (over-testing guard).
  *(Multi-stack examples: Playwright `page.clock` or a backend fake clock; the scheduler
  interface to trigger cron manually; inject into the queue and poll for the consumed
  result; assert cross-channel delivery against the target channel's outbound record — per
  stack.)*
- **5. Journey-level traceability + safety-net localisation (first appearance means backfill
  a lower layer):** needs the capability to "attach every assertion to a journey step and its
  AC, so a failure localises to the hop that broke", and to enforce the safety-net semantics:
  a bug found **for the first time** at this layer means a lower layer under-tested it, so
  prompt to backfill that layer's test. This layer keeps only a few P0s and is not a stand-in
  for the layers below.
- **Routing note:** this skill hands the list of hit chain gaps to `full-chain-testing-en`;
  any agent behaviour that writes or fixes tests (including a diff-aware E2E tool) is bound
  by the five guardrails (see below).
- **Conditional hits / over-testing guard:** the capabilities above are **not all marked** —
  any journey classified here marks gap 1 plus gap 2 first; mark gap 3 once the whole system
  must be stood up; mark gap 4 **only for streaming, async, scheduled or cross-channel**;
  mark gap 5 where failures must localise to a journey step and the backfill semantics must
  be enforced. The hit rules are in "conditional hits" below and in `full-chain-gaps.md`.

### Conditional hits (over-testing guard)

| What chain this feature actually completed | Chain gap hit | Approach |
|---|---|---|
| Any cross-feature journey classified here | 1. Path excavation + 2. criticality grading and taking few | Prerequisite actions: semi-automatic enumeration + human confirmation, then take only P0s as the safety net |
| Standing the whole system up end to end | 3. Whole-system orchestration + external boundary stubs | Stand the real full stack up, stubbing only external third parties (WireMock and similar) |
| Scheduled / async / cross-channel hops | 4. Async / time / cross-channel continuity | Fake clock / manual job trigger / poll-retry, **no sleep** (**marked only when such hops exist**) |
| Failures needing to localise to a journey step | 5. Journey-level traceability + safety-net localisation | Attach assertions to journey step and AC; first appearance means backfill a lower layer |
| A single slice within one feature (not crossing features) | Nothing hit | Belongs to local full-stack slice, not here |

## Cross-module contract (candidate category) -> that category's skill (placeholder, to be built)

- **Capability needed:** derive an interface spec from a **typed producer** -> feed it to
  **downstream codegen** so consumers compile against the real shape -> run **breaking-change
  detection** between versions -> optionally verify by reflection that the live signature
  still matches the declaration.
- **Routes to:** that category's executor skill (to be built). Concrete tools are
  instantiated by that skill per stack *(multi-stack examples: typed web frameworks emitting
  OpenAPI or JSON Schema, paired with an `oasdiff`-style diff; escalating to `Pact`-style
  consumer-driven contract tests where producer and consumer are deployed independently by
  different teams — depends on stack and deployment shape)*.
- **Why:** generating the contract from typed code keeps producer and consumer in sync for
  free; a breaking-change diff catches the silent A->B mismatch unit tests cannot see — which
  is the value at a high-drift seam.
- **When to deviate:** in a single monorepo, "derive the spec and diff it" is lighter and
  sufficient; escalate to consumer-driven contract testing only when producer and consumer
  are deployed independently by different teams.

## Letting this table grow

This is a living table. Once a placeholder category's executor skill is built, change that
routing destination's status from "placeholder, to be built" to "executor built". **Note:
this skill only ever records which executor skill something routes to, and never hardcodes a
single-stack tool in this table** — choosing the concrete tool is always the receiving
executor skill's responsibility, instantiated per stack.

## Guardrail reminder

Any **agent behaviour above that writes or fixes tests** (including a diff-aware E2E tool
folded into the full functional chain's UI-traversable segment) MUST run under the five
guardrails in `self-healing-guardrails.md`. This skill only classifies and routes; it never
runs a tool itself, and it never picks a single-stack tool on the project's behalf.
