# Local full-stack slice structural gap list (stack-agnostic capabilities -> routed to `fullstack-slice-testing-en`)

This list serves the "local full-stack slice" category: when a feature's frontend and
backend tasks are all green and it enters close-out, the backend tests are green with the
frontend mocked out and the frontend tests are green with the backend mocked out — but
**the seam itself has never been run with both real sides joined together**. Below, those
**structural gaps** are listed one by one (all of them **stack-agnostic capabilities**) with
the approach for each. **This skill hardcodes no single-stack tool** — once you have judged
which gaps are hit, **route them, with the reason each was hit, to the
`fullstack-slice-testing-en` skill**, which reads the project's stack (`package.json`,
`pyproject.toml`, `docker-compose.yml`, `go.mod` and so on) and wires that stack's tools to
close the gap.

> Methodology follows the `testing-system-blueprint-en` skill as its blueprint. The tool
> names below (docker-compose, Playwright, Pact, MSW and the rest) are **multi-stack
> examples**, not fixed answers.

## Classification condition (when this is a "local full-stack slice")

Changes land in **both frontend and backend**, and the seam **does not cross the feature
boundary** — user journeys spanning several features belong to "full functional chain".
In essence this is a single-slice reconciliation of *real frontend to real backend* within
one feature. Pure single-side changes belong to backend-only or frontend-only, not here.

## A difference in shape: the new difficulty is standing the real stack up, not writing assertions

This is what fundamentally separates the local full-stack slice from backend-only and
frontend-only work:

- **The backend executor (`backend-testing-en`) writes test code itself** — two-user
  escalation assertions, concurrency invariants and the like are mostly hand-written.
- **The frontend executor (`frontend-testing-en`) wires mature tools, configures them and
  translates visual contracts** — the tools exist; the work is configuration.
- **The full-stack slice executor (`fullstack-slice-testing-en`) stands the real stack up
  first, then reconciles** — the assertions themselves are not hard to write; **the real
  difficulty is environment orchestration**: getting the frontend, the backend and the real
  dependencies (data store, cache, external services) up simultaneously and reproducibly.
  It is fundamentally **a reconciliation between the frontend's mocks and the backend's
  reality**: the frontend-only stage used a consumer mock to get green, and this stage
  swaps that mock for the real provider to verify the shapes, the timing and the error
  states genuinely line up.

**A layered approach:** first run a **diff-aware E2E** black-box smoke (walk the main path
against the real assembled stack and see whether the seam is connected at all); then add
**structured seam assertions** (precisely assert identity propagation, serialisation
conventions, error-to-UI mapping, real-time ordering). A diff-aware E2E tool is
**optional — prefer one where it exists, fall back to Playwright and similar where it does
not**.

## Gap list (stack-agnostic)

| Structural gap (capability) | How the process treats it today | Approach | Routes to / example tools |
|---|---|---|---|
| 1. Environment orchestration (both sides + dependencies up for real) | **Not touched at all** — each side is green against its own mocks, and the real stack has never been assembled | Must be built: the first action is to stand the real stack up | `fullstack-slice-testing-en` stands it up per stack (docker-compose, in-process assembly + testcontainers) |
| 2. Contract reality (mock versus real provider) | The frontend is green against a consumer mock, never checked against the real backend shape | Swap the mock for the real provider and reconcile | `fullstack-slice-testing-en` replays real responses to validate the mock, or diffs both directions (Pact, OpenAPI diff) |
| 3. Seam glue (identity propagation / serialisation / error-to-UI) | Glue points neither side's tests can see | Drive the path with real auth headers and assert the UI error states | `fullstack-slice-testing-en` drives cross-process and asserts UI state |
| 4. Real-time ordering (conditional hit) | Streaming and async paths have zero coverage | Wire a tool and assert incremental arrival ordering | `fullstack-slice-testing-en` wires SSE / WebSocket / polling assertions (**marked only for streaming or async**) |

## Each gap in detail (capability definition + multi-stack examples)

### 1. Environment orchestration (both sides + dependencies up for real) — the first action, and where the new difficulty lives

**Capability definition:** get the frontend, the backend and the real dependencies (data
store, cache, external services) up simultaneously and reproducibly, so the seam can be
driven once against the genuine assembly. Both sides being green against their own mocks
does not mean they connect when joined — standing the real stack up is this category's
first hurdle, and the precondition for any assertion landing at all.

- **Multi-stack examples (chosen by `fullstack-slice-testing-en` per stack):**
  `docker-compose` for the whole stack; in-process ASGI/WSGI assembly of the real
  application handler plus `testcontainers` for a real data store or cache; a one-command
  stack tool where the project has one — **such a tool is optional, preferred where it
  exists and falling back to docker-compose or in-process assembly where it does not.
  These are examples, not fixed answers.**

### 2. Contract reality (consumer mock versus real provider)

**Capability definition:** replace the **consumer mock** the frontend-only stage used to
reach green with the **real provider**, and reconcile whether the shapes match. Green
against a mock does not mean the real backend returns the same fields, types or nesting —
this gap exists to catch the silent divergence between mock and reality (a missing field, a
changed type, a changed nullability).

- **Multi-stack examples (chosen by `fullstack-slice-testing-en` per stack):** replay real
  backend responses to validate the frontend's MSW handlers; across independently deployed
  services, use `Pact`-style consumer-driven contracts to reconcile "what the frontend
  expects" against "what the backend actually emits"; within one repository, diff an
  OpenAPI spec in both directions. **Depends on the stack and the deployment shape.**

### 3. Seam glue (identity propagation / serialisation / error-to-UI mapping)

**Capability definition:** assert the glue points on the cross-process seam that **neither
side's tests can see**: whether the identity token really propagates from frontend to
backend and is validated correctly; whether both sides agree on serialisation conventions
(dates, numbers, enums, nulls); whether the backend's error states (4xx, 5xx, business
error codes) map correctly to the frontend's corresponding UI states.

- **Multi-stack examples (chosen by `fullstack-slice-testing-en` per stack):** drive the
  whole request path with real auth headers and assert that protected resources are
  reachable and cross-user access is refused; make the backend return each class of error
  and assert the UI renders the corresponding error, empty or degraded state. **Depends on
  the stack.**

### 4. Real-time ordering (conditional: only hit by streaming or async)

**Capability definition:** assert timing and incremental arrival for **streaming, async or
real-time push** — first byte arrival, increment ordering, and UI behaviour on stream end,
interruption or timeout. **Marked only when this feature actually involves streaming, async
or real-time push**; otherwise not marked, to prevent over-testing.

- **Multi-stack examples (chosen by `fullstack-slice-testing-en` per stack):** SSE or
  WebSocket increment and ordering assertions; polling arrival ordering assertions.
  **Depends on the stack.**

## Working with conditional hits

Not every feature hits every gap — take the subset the feature actually touches (the hit
rules are in the "conditional hits" table in `tool-mapping.md`): any change touching both
sides starts with gap 1, environment orchestration (the real stack has often never been
assembled); mark gap 2, contract reality, only where the frontend had a consumer mock and
this feature also has the real provider; mark gap 3, seam glue, where identity crosses
processes, where serialisation matters, or where error states must map to the UI; mark gap
4, real-time ordering, **only for streaming, async or real-time push**. Pure single-side
changes with no frontend-backend seam belong to backend-only or frontend-only, not here.
This skill marks only the seam gaps that are hit; **the concrete tools are always
instantiated by `fullstack-slice-testing-en` for the stack (including optional tools that
are preferred where present and fall back where absent), and this skill does not decide
them on its behalf.**
