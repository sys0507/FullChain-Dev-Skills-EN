# Frontend-only structural gap list (stack-agnostic capabilities -> routed to `frontend-testing-en`)

This list serves the "frontend only" category: when a feature's frontend tasks are all
green and it enters close-out, the TDD loop (if there was one) has covered only a few
units, while the genuinely high-risk gaps sit where TDD does not usually reach — and the
frontend frequently **has no test foundation at all**. Below, those **structural gaps** are
listed one by one (all of them **stack-agnostic capabilities**) with the approach for each.
**This skill hardcodes no single-stack tool** — once you have judged which gaps are hit,
**route them, with the reason each was hit, to the `frontend-testing-en` skill**, which
reads the project's `package.json` (including framework and test-runner clues) to identify
the stack and wires up that stack's tools to close the gap.

> Methodology follows the `testing-system-blueprint-en` skill as its blueprint. Tool names
> below are **multi-stack examples**, not fixed answers.

## Classification condition (when this is "frontend only")

Changes land **in the frontend layer alone** — components, pages, styles, frontend routing,
frontend state — with no backend business logic and no integration against a live backend.
Once a live backend is involved it belongs to "full functional chain"; frontend-to-backend
wiring within a single feature belongs to "local full-stack slice".

## A difference in shape: the frontend wires tools rather than writing test code

This is what fundamentally separates frontend-only from backend-only:

- **The backend executor (`backend-testing-en`) writes test code itself** — two-user
  escalation assertions, concurrency invariants and the like are mostly hand-written.
- **The frontend executor (`frontend-testing-en`) wires mature tools, configures them, and
  translates the project's visual contracts into assertions** — stylelint, Vitest + RTL,
  Playwright, axe and MSW all exist already; the work is wiring and configuring them for
  the stack and turning the project's visual and contract rules into assertions. **The
  single point needing human review is adjudicating the L2 visual baseline** (a changed
  baseline snapshot needs a person to confirm whether it is an intended redesign or a
  regression).

## Gap list (stack-agnostic)

| Structural gap (capability) | How the process treats it today | Approach | Routes to / example tools |
|---|---|---|---|
| L0/L1 test foundation | **Not touched at all** — `[FE]` outputs often just say "tested manually", with no test runner installed | Must be built: the first action is to lay the foundation | `frontend-testing-en` wires a component testing library for the stack (Vitest + RTL and similar) |
| L2 visual regression (pixels / dark mode / colour contracts) | Eyeballing screenshots | Wire a tool and translate the contracts (**human adjudication of the L2 baseline**) | `frontend-testing-en` wires screenshot snapshots for the stack (Playwright and similar) |
| L3 accessibility (contrast / ARIA / labels) | Zero coverage | Wire a tool | `frontend-testing-en` wires an a11y audit for the stack (axe and similar) |
| L4 cross-browser + responsive | Zero coverage | Wire a tool (multiple viewports + geometry assertions) | `frontend-testing-en` wires multi-viewport runs for the stack |
| L6 frontend-backend contract mocking | Untouched by the process; contracts drift easily | Wire a tool (generate mocks from the spec) | `frontend-testing-en` wires MSW with generation from OpenAPI |
| Design tokens / hardcoded colours | Caught by review | **Enforce at the lint gate, do not write a test** | A lint rule blocks it at the gate (stylelint and similar) |

## Each gap in detail (capability definition + multi-stack examples)

### L0/L1. Test foundation — frequently zero (the first action)

**Capability definition:** a minimal test runner and scaffold that can render components
and drive interactions. A frontend feature's `[FE]` outputs frequently say only "tested
manually" with no test runner installed at all — the foundation itself is missing. So
`frontend-testing-en`'s **first action is to lay that foundation**: install a component
testing library for the stack and get a minimal render-and-interact case passing. Every
upper-layer gap then hangs off it, and no second framework is introduced within one stack.

- **Multi-stack examples (chosen by `frontend-testing-en` per stack):** JS/TS stacks
  commonly use `vitest` or `jest` with a component testing library (React Testing Library
  and similar); other frontend stacks use their own native frameworks. **These are
  examples, not fixed answers.**

### L2. Visual regression (pixels / dark mode / colour contracts) — wire a tool and translate the contracts (the only human-review point)

**Capability definition:** take screenshot snapshots of pages and components, compare them
across versions to catch pixel-level regressions, and translate the project's visual
contracts (dark mode, rise-and-fall colour conventions and the like) into assertions. This
is the **only point in frontend-only work that needs human review** — when a baseline
snapshot changes, a person adjudicates whether it is an intended redesign (accept the new
baseline) or a regression (reject it). An agent MUST NOT refresh the baseline on its own.

- **Multi-stack examples (chosen by `frontend-testing-en` per stack):** Playwright
  screenshot snapshots and similar.

### L3. Accessibility (contrast / ARIA / labels) — wire a tool

**Capability definition:** automatically audit contrast, ARIA roles and attributes, form
label association and other accessibility rules.

- **Multi-stack examples (chosen by `frontend-testing-en` per stack):** the `axe` family of
  audit libraries.

### L4. Cross-browser + responsive — wire a tool

**Capability definition:** run across multiple viewports and browsers, with geometry
assertions on the layout — typically "no horizontal scrollbar at any viewport".

- **Multi-stack examples (chosen by `frontend-testing-en` per stack):** Playwright with
  multiple projects and viewports.

### L6. Frontend-backend contract mocking — wire a tool (drift protection)

**Capability definition:** intercept the frontend's outbound calls with mocks generated
from the interface spec, so the frontend is tested against the real contract shape; when
the backend contract changes, this catches the silent drift of a frontend still reading the
old shape.

- **Multi-stack examples (chosen by `frontend-testing-en` per stack):** MSW with handlers
  generated from an OpenAPI spec.

### Design tokens / hardcoded colours — enforce at the lint gate, do not write a test

Whether colours, spacing and font sizes are hardcoded or go through design tokens is
**blocked by a lint rule at the gate, not written as a test case** — it is a static
constraint, and lint suits it better and runs faster than a test.

- **Multi-stack examples (chosen by `frontend-testing-en` per stack):** `stylelint` with
  custom rules.

## Working with conditional hits

Not every feature hits every gap — take the subset the feature actually touches (the hit
rules are in the "conditional hits" table in `tool-mapping.md`): any frontend change lays
the L0/L1 foundation first (it is usually zero); mark L2 only where there are visual, dark
mode or colour contracts; L3 only where there are interactive components; L4 only where
there are multiple viewports or responsive behaviour; L6 only where it calls a backend
endpoint; hardcoded colours and tokens go to the lint gate. This skill marks only the
capability gaps that are hit; **the concrete tools are always instantiated by
`frontend-testing-en` for the stack, and this skill does not decide them on its behalf.**
