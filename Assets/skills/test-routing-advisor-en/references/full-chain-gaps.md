# Full functional chain structural gap list (stack-agnostic capabilities -> routed to `full-chain-testing-en`)

This list serves the "full functional chain" category: once some feature lands, a user
journey **spanning several features** becomes reachable end to end for the first time. At
that point every feature's own units and local full-stack seams may each be green — but
**the complete journey across those features, including its non-UI hops (scheduled, async,
cross-channel), has never been run end to end by anyone**. Below, those **structural gaps**
are listed one by one (all of them **stack-agnostic capabilities**) with the approach for
each. **This skill hardcodes no single-stack tool** — once you have judged which gaps are
hit, **route them, with the reason each was hit, to the `full-chain-testing-en` skill**,
which reads the project's stack (`package.json`, `pyproject.toml`, `docker-compose.yml`,
`go.mod` and so on) and wires that stack's tools to close the gap.

> Methodology follows the `testing-system-blueprint-en` skill as its blueprint. The tool
> names below (static code graphs, runtime tracing via OpenTelemetry-style tooling,
> docker-compose, WireMock, Playwright `page.clock`, event storming and the rest) are
> **multi-stack examples** — not fixed answers and not dependencies. Some named static-graph
> tools carry **non-commercial licences**; they are listed only as optional examples of
> "instantiate per stack" and constitute no dependency of this skill. Project-specific
> names (journey step names, channel names, job names) are always read live, never hardcoded.
>
> **A clean instance that is available by default**: the `full-chain-testing-en` skill ships
> its own **MIT clean-room reference toolset** (under `scripts/`: knife 1 spec / knife 2
> static / knife 3 trace, merged by knife 4 into `path-inventory.json`, visualised as
> journeys by knife 6, every edge carrying provenance and refusing to fabricate). All three
> sources can be instantiated from it — **with no non-commercial constraint**, making it the
> licence-clean default, and it is itself stack-agnostic (it reads `pyproject.toml` or
> `package.json` and works from there). Other static-graph tools remain optional
> alternatives for other stacks.

## Classification condition (when this is a "full functional chain")

The path under test **crosses the feature boundary and spans several features**. A single
slice reconciled within one feature — even one touching both frontend and backend — belongs
to "local full-stack slice", not here. In essence this is **an end-to-end journey across
several features, including non-UI hops** (scheduled triggers, async consumption,
cross-channel handoffs). The entry point for the classification is exactly this advisor's
distinctive move — **deriving from the dependency graph that some A->B->C has become
connected for the first time**: when a feature happens to supply the last missing link in a
cross-feature journey, that journey belongs here.

## Two differences in shape: the subject must be excavated, and this is the safety-net layer

These are what fundamentally separate the full functional chain from the previous three
categories:

- **The subject under test (the path) must be excavated first.** In backend-only,
  frontend-only and local full-stack slice work the subject is **given** (a unit, a
  component, a slice). Here the subject — an end-to-end path — **hides in the dependency
  graph and appears in no single task**, so it must be semi-automatically enumerated and
  then confirmed by a person. Path excavation is this category's unique first action.
- **This is the safety-net layer, not the exhaustive layer.** If a bug is found **for the
  first time** at this layer, that means a lower layer (backend-only, frontend-only, local
  full-stack slice) should have caught it and did not — the correct response is to
  **backfill the missing test at that lower layer**, not to pile assertions up here.
  So this category keeps only a **small number of P0 critical paths** as a safety net, and
  does not aim to cover every path (exhaustiveness is the lower layers' job).

**A layered approach:** the first layer is the **UI-traversable segment** — use a
**diff-aware E2E** run against the real assembled system to walk the part of the journey the
UI can reach (a one-command E2E tool is **optional, preferred where present and falling back
to Playwright and similar where absent**). **Non-UI hops** (scheduled jobs, async
consumption, cross-channel delivery) cannot be reached through the UI, so use
**orchestration-driven** testing instead: manually trigger the job, inject the message, and
poll to assert, stitching those hops together.

## Gap list (stack-agnostic)

| Structural gap (capability) | How the process treats it today | Approach | Routes to / example tools |
|---|---|---|---|
| 1. Path excavation (**three sources** enumerate end-to-end paths + human confirmation) | **Not touched at all** — paths hide in the dependency graph and nobody lists them; and a static graph reaches only **half the graph** | Must be built: three sources (static graph + runtime trace + spec contracts) semi-automatically enumerate, then a person confirms | `full-chain-testing-en` uses a static graph as the base, runtime tracing to add the frontend-backend bridge edges and the cron/async decoupled edges, and spec contracts as the only source where the code does not exist yet |
| 2. Criticality grading + take few (P0 safety net, not exhaustive) | The process tends to "test everything" or "test nothing" | Grade the excavated paths and take only a small handful of P0s | `full-chain-testing-en` grades by risk and takes a few P0 paths (blueprint P0-P3) |
| 3. Whole-system orchestration + external boundary stubs | Each feature mocks its own neighbours; the whole system has never been assembled | Stand the whole system up; stub only the outermost third parties | `full-chain-testing-en` stands the real full stack up (docker-compose, in-process assembly) and stubs only external third parties (WireMock and similar) |
| 4. Async / time / cross-channel continuity | Scheduled, async and cross-channel hops have zero end-to-end coverage | Fake clock + manual job trigger + poll-retry, **`sleep` forbidden** | `full-chain-testing-en` wires a fake clock, manual triggers and polling assertions (Playwright `page.clock` and similar) |
| 5. Journey-level traceability + safety-net localisation | A failure points at one feature, never at the journey | Attach assertions to journey steps; first appearance here means backfill a lower layer | `full-chain-testing-en` provides journey-to-AC traceability plus a "first found here means a lower layer under-tested it" backfill prompt |

## Each gap in detail (capability definition + multi-stack examples)

### 1. Path excavation (enumerate end-to-end paths from the dependency graph, cross-module contracts and user-story ACs) — the first action, unique to this category

**Capability definition:** turn an end-to-end path from implicit into explicit. The previous
three categories are handed their subject; here the subject must be **excavated** first, and
then **confirmed by a person** as to which of them are genuine user journeys
(semi-automatic enumeration reduces the noise; human confirmation sets the boundary). This
is precisely where the advisor's distinctive move — "derive from the dependency graph that
A->B->C is connected for the first time" — lands: **that newly connected chain is where path
excavation starts.**

**Path excavation uses three sources, and needs all three:**

1. **Static code graph** — derive edges statically from the source's imports, calls and
   dependency topology. This reaches only **half the graph**: the syntactically obvious
   edges (direct function calls, explicit imports).
2. **Runtime trace** — run the system and use distributed tracing to observe the real call
   chain, filling in the edges static analysis cannot stitch.
3. **Spec contracts** — when **the code does not exist yet**, neither a static graph nor a
   runtime trace is available, and the spec's cross-module contract declarations and
   user-story ACs are the **only source** of the path.

**Empirical boundary (observed across two projects): a static graph reaches only half the
graph.** Two classes of edge **cannot be stitched statically** and must come from runtime
tracing or spec contracts:

- **Framework-wrapped frontend-backend bridge edges** — calls connected across the frontend
  and backend by a framework convention (a routing table, an RPC proxy, an auto-serialising
  client) leave no plain cross-tier call edge in the source, so static analysis cannot find
  them.
- **Cron and async decoupled edges** — scheduled triggers, message queues and background
  workers are **decoupled in time or by event**, so producer and consumer never reference
  each other in code and the static graph naturally breaks there.

That is why all three sources are needed: the static graph supplies the skeleton, runtime
tracing adds the bridge and decoupled edges, and spec contracts cover the case where the
code has not landed.

- **Multi-stack examples (chosen by `full-chain-testing-en` per stack; all optional
  instances, not dependencies):** static-graph tools to list candidates; runtime tracing to
  observe the real call chain; event-storming style modelling to comb cross-feature domain
  event flows into journeys; a project's own one-command journey tool where it has one —
  **optional, preferred where present, falling back to manual combing where absent. These
  are all examples, not fixed answers.**

### 2. Criticality grading + take few (P0 safety net, not exhaustive)

**Capability definition:** grade each excavated path by **criticality** (how much damage to
the user or the business if this journey breaks), and take only a small handful of the
highest priority (P0) as a safety net, **not every path**. Exhaustiveness is the lower
layers' responsibility; end-to-end tests here are the slowest and most brittle, and more of
them degrades the signal rather than improving it. Grading follows the P0-P3 risk grading in
`testing-system-blueprint-en`.

- **Multi-stack examples (chosen by `full-chain-testing-en` per stack):** rank by how
  strongly the AC says "must hold" plus how much user surface the journey touches, then take
  the top N P0 paths. **Set by the project's actual journeys; the count is not hardcoded.**

### 3. Whole-system orchestration + external boundary stubs (stub only the external third-party boundary)

**Capability definition:** stand the **entire cross-feature system** up for real and
reproducibly, so the whole path can be driven against the genuine assembly; **stub only the
outermost third-party boundary** (payment gateways, external model services, third-party
push and other external dependencies that are uncontrollable, costly or have side effects),
while everything between features inside the system runs against the real assembly and is
never mocked. Compared with the local full-stack slice's "stand the real stack up", the
stack here is larger (several features and several dependencies), and **nothing inside the
external boundary may be stubbed** — otherwise it is not end to end.

- **Multi-stack examples (chosen by `full-chain-testing-en` per stack):** `docker-compose`
  for the whole system; in-process assembly of several features' real handlers; `WireMock` or
  record-and-replay for the external third-party boundary stubs — **nothing inside that
  boundary is stubbed. Depends on the stack.**

### 4. Async / time / cross-channel continuity (fake clock / manual job trigger / poll-retry, no sleep)

**Capability definition:** stitch together and assert continuity across the **non-UI hops**
the journey's UI cannot reach: **scheduled** (cron or scheduler steps that only happen when
the time arrives), **async** (message queue or background worker consumption), and
**cross-channel** (one channel triggers, another finishes — a web action producing an email
or IM push). The key discipline: use a **fake clock** to fast-forward to the scheduled point
(never really wait), **manually trigger** the job or inject the message to pull async steps
into the foreground, and use **poll-retry** (bounded polling until the condition holds) to
assert arrival — **`sleep` is forbidden**, because it makes tests both slow and flaky and is
the single largest source of brittleness in end-to-end testing.

- **Multi-stack examples (chosen by `full-chain-testing-en` per stack):** Playwright
  `page.clock` or a backend fake clock to fast-forward time; call the scheduler interface
  directly to trigger a cron job; inject a message into the queue and poll for the consumed
  result; assert cross-channel delivery against the target channel's outbound record.
  **Depends on the stack.**

### 5. Journey-level traceability + safety-net localisation (first appearance means backfill a lower layer)

**Capability definition:** attach every assertion **to a specific journey step** (which step,
and which user-story AC it corresponds to), so a failure localises to the hop of the journey
that broke rather than merely surfacing some feature's exception. And enforce the
**safety-net semantics**: if a bug is found **for the first time** at this layer, judge it
explicitly as **a lower layer under-testing**, and prompt in the report to **backfill the
corresponding test at that lower layer** (backend-only, frontend-only, or local full-stack
slice) — this layer keeps only a few P0s as a safety net and is not a stand-in for the
layers below.

- **Multi-stack examples (chosen by `full-chain-testing-en` per stack):** a journey
  step-to-AC traceability matrix; on failure, emit "this is journey step k breaking,
  suspected under-testing at lower layer X, recommend backfilling X's regression".
  **Depends on the stack.**

## Working with conditional hits

Not every feature that completes a chain hits every gap — take the subset by the journey's
actual shape (the hit rules are in the "conditional hits" table in `tool-mapping.md`): any
journey classified here starts with gap 1, path excavation, plus gap 2, grading and taking
few (these are the category's prerequisite actions); mark gap 3, whole-system orchestration
with external boundary stubs, once the whole system has to be stood up; mark gap 4, async /
time / cross-channel continuity, **only when** the journey contains scheduled, async or
cross-channel hops (a purely synchronous UI journey does not, to prevent over-testing); mark
gap 5 when failures need to localise to a journey step and the safety-net backfill semantics
need enforcing. A slice within a single feature belongs to the local full-stack slice, not
here. This skill marks only the chain gaps that are hit; **the concrete tools are always
instantiated by `full-chain-testing-en` for the stack (including optional tools that are
preferred where present and fall back where absent), and this skill does not decide them on
its behalf.**
