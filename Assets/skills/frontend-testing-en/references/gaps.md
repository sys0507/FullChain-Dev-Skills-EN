# Five layers of frontend structural gaps: capabilities + per-stack instantiation

> How to use: identify the project's stack per step 0 of SKILL.md, then read that stack's
> row under the relevant layer to instantiate the tools.
> Each layer states the **capability** first (stack-agnostic, always true), then gives
> **example instances** (JS/TS as the primary example). The examples are a lookup, not the
> only answer — the stack and the libraries are the project's own choice; this table only
> maps "capability -> a tool in that stack's ecosystem".
>
> **This skill is a fitter and an inspector, not a construction crew**: every layer below
> has mature tools; do not build your own. The skill's job is **install, configure,
> translate** — wire the generic tool into the project, and turn *this project's* visual and
> interaction contracts into assertions and rules the tool can run.
>
> **Every "project-specific" input is conditional**: wherever token names or values,
> rise-and-fall colour conventions, design specs or must-run pages are involved, the rule is
> always "**if the project has a visual spec document or design tokens, then** read from it
> and generate assertions accordingly"; where it does not, that class of assertion is not hit.

## Contents

0. [Lay the foundation (prerequisite, specific to frontend)](#0-lay-the-foundation-prerequisite-specific-to-frontend)
1. [1. Compile-time lint gate](#1-1-compile-time-lint-gate-cheapest-first)
2. [2. L0/L1 unit tests](#2-2-l0l1-unit-tests)
3. [3. a11y + cross-browser/responsive](#3-3-a11y--cross-browserresponsive)
4. [4. Frontend-backend contract mocking](#4-4-frontend-backend-contract-mocking)
5. [5. Visual regression](#5-5-visual-regression)
6. [The human-review point and what machines cannot assert](#the-human-review-point-and-what-machines-cannot-assert)
7. [Cross-layer reminders](#cross-layer-reminders)

---

## 0. Lay the foundation (prerequisite, specific to frontend)

**Capability**: before filling any layer, confirm the project has a test foundation — a test
runner, a component/DOM testing library, and a browser driver (end-to-end and screenshots).
**If it has none, lay the foundation first**, so that "one trivial test runs and goes green"
holds before anything else.

**Why the frontend needs this step specifically**: a frontend project's test foundation is
**frequently zero** — many `[FE]` tasks state their output verification as "tested
manually", and the runner, component library and browser driver may not be installed at all.
Backend projects usually already have a unit framework; the frontend must not assume it.

| Stack | Test runner | Component/DOM testing library | Browser driver |
|---|---|---|---|
| JS / TS | Vitest (or Jest) | Testing Library | Playwright (or Cypress) |
| Dart / Flutter | Built-in `flutter test` | `flutter_test` (widget tests) | `integration_test` + golden tests |
| .NET / Blazor | xUnit + bUnit | bUnit | Playwright for .NET |
| Other stacks | Look up that stack's mainstream unit runner | Look up that stack's component-render testing library | Look up that stack's browser/end-to-end driver |

**Foundation starting assertion**: once installed, get one trivial render test to green to
prove the foundation works, then move into the layered work.

---

## 1. 1. Compile-time lint gate (cheapest, first)

**Capability**: translate the project's visual contracts into **static lint rules** that
block violations at compile or commit time — **no tests written at all**, the best value for
money, always done first. Three typical rule classes:
- **No bare colour values / only `var()`**: colours, font sizes, spacing and other visual
  values MUST go through token variables; hardcoded literals are forbidden.
- **No second UI library import**: where the project has settled on one component library,
  statically block imports of others.
- **No arbitrary hex classes**: with atomic CSS (Tailwind-style), forbid `[#xxxxxx]`-style
  arbitrary value classes that bypass the tokens.

**Why lint rather than a test**: these are "shape and origin" constraints, decidable
statically at compile time with no rendering and no execution — blocking them furthest left
is cheapest. **Fully automatic, no test written, no human review needed.**

**The translation work (the skill's job)**: stylelint and its peers are generic, but they
**do not know what your tokens are called**. The skill must, **if the project has design
tokens**, configure the permitted `var()` list, the forbidden library names and the
forbidden arbitrary-value patterns into the rules.

| Stack | Bare colour / token enforcement | No second UI library import | No arbitrary value classes |
|---|---|---|---|
| JS / TS | stylelint (`declaration-property-value-disallowed-list`, or a custom rule permitting only `var()`) | ESLint `no-restricted-imports` | stylelint or an ESLint custom rule blocking `[#hex]` arbitrary values |
| Dart / Flutter | A custom lint (`custom_lint`) forbidding literal `Color(0x..)` and forcing the theme | `custom_lint` import restrictions | — |
| Other stacks | Look up that linter's "forbid literals / require variables" rule | Look up that linter's import restrictions | Look up that stack's atomic-CSS arbitrary-value constraint |

**Typical rule list**: colour properties permit only token `var()`; spacing, radius and font
size go through tokens; non-allowlisted UI library imports error; arbitrary hex classes
error. Once these are in CI or pre-commit, a violation cannot even be merged.

---

## 2. 2. L0/L1 unit tests

**Capability**: render components with the component/DOM testing library and assert that
**the visual contract actually reached the computed style**. The key is asserting the
**resolved actual value via `getComputedStyle`** (or the equivalent computed-style read),
not merely that a class name is present — a present class does not mean the token resolved
to the right value. Three typical assertion classes (all conditional, **hit only if the
project has the corresponding contract**):
- **Token resolved value**: an element's computed colour or spacing equals what the design
  token should resolve to.
- **Dark-mode coverage**: under the dark theme, key elements' computed styles really switch
  to the dark tokens (no light-mode remnants left uncovered).
- **Rise-and-fall colours**: the computed colour of a rising or falling element equals the
  project's agreed rise or fall token value (**the convention is the project's** — some
  markets use red for a rise and green for a fall, others the reverse; the tool cannot know
  which is right, so **the skill translates it from the project's visual spec**).

**Why assert the computed value**: CSS variables, theming and the cascade make "right class,
wrong value" a common hidden bug; only reading the computed style catches an unresolved
token, an uncovered dark mode, or rise-and-fall colours wired backwards. **Fully automatic
RED to GREEN.**

| Stack | Render + computed-style assertion |
|---|---|
| JS / TS | Vitest (or Jest) + Testing Library to render, `getComputedStyle(el)` to assert resolved values; where JSDOM does not resolve CSS variables, use browser mode (Vitest browser mode, Playwright component testing) to read the real computed style |
| Dart / Flutter | `flutter_test` widget tests, asserting actual colours and sizes from `Theme.of` or the render object |
| .NET / Blazor | bUnit renders, then assert style and computed properties |
| Other stacks | Look up that stack's "render a component and read computed style" capability |

**The translation work (the skill's job)**: **if the project has design tokens or a visual
spec**, translate the token values into expected assertion values (the rise token's value,
the dark background token's value, and so on); in a project with no visual spec, this layer
asserts structural render logic only and does not assert tokens.

**Typical assertion list**: a key element's computed colour equals the expected token value;
under dark mode, background and foreground switch to the dark tokens; rise and fall elements
match the project's convention; computed values follow when the theme is toggled.

---

## 3. 3. a11y + cross-browser/responsive

**Capability**: two parts, both fully automatic.
- **a11y (the L3 capability)**: scan the rendered page or component with an automated
  accessibility engine to catch the machine-detectable violations (automatic detection
  covers roughly 57% of all a11y problems, of which contrast issues are about 30%).
- **Cross-browser / responsive (the L4 capability)**: run across several browser engines and
  viewports, asserting **geometric invariants** — the classic being "**no horizontal
  scrollbar**": `document.documentElement.scrollWidth <= window.innerWidth`.

**Why it matters**: a11y and contrast problems cannot be fully caught by eye in a single
browser at a single viewport; a responsive break (a horizontal scrollbar appearing on
mobile) only shows at particular viewports and is always green on a single desktop viewport.
It has to run for real across browsers and viewports.

| Stack | a11y engine | Cross-browser/multi-viewport driver |
|---|---|---|
| JS / TS | axe-core; `@axe-core/playwright` for end-to-end, `jest-axe` or `vitest-axe` for component tests | Playwright `projects` configured across browser engines and viewports; assert geometric invariants such as `scrollWidth <= innerWidth` |
| Dart / Flutter | `flutter_test` semantics assertions plus a11y guideline checks | `integration_test` across device sizes plus goldens |
| Other stacks | Look up that stack's axe integration or equivalent a11y scan | Look up that stack's multi-browser/multi-viewport end-to-end driver |

**The translation work (the skill's job)**: axe is generic, but it **does not know which
pages must run, or whether a red result should block a release** — the skill must specify the
must-run page set, align the contrast thresholds with the project's design, and define which
violation levels block a release (serious blocks, minor warns).

**Typical assertion list**: key pages have no serious or critical axe violations; contrast
meets the threshold; no horizontal scrollbar at any viewport; key interactive elements have
accessible names and roles; the main path renders consistently across browser engines.

---

## 4. 4. Frontend-backend contract mocking

**Capability**: **intercept the frontend's network requests to the backend** inside frontend
tests and return controlled data from a mock, so the frontend can be **tested independently
of a real backend**. The key is that **the mock data is generated from the backend contract
source and updates as the contract updates**, avoiding drift between the frontend's mock and
the backend's real responses — otherwise the mock stays green forever and the real backend
breaks. Optionally, a stronger **consumer-driven contract** keeps both sides aligned.

**Why it matters**: if frontend tests use hand-written mocks, a backend field change does not
propagate, the unit tests stay green and the integration breaks. Generating handlers from
the contract (OpenAPI, say) gives the mock the same source as the backend and removes the
drift. **Fully automatic in CI.**

| Stack | Request-interception mock | Generated from contract / bidirectional contract |
|---|---|---|
| JS / TS | MSW (Mock Service Worker, intercepting at the network layer) | Generate MSW handlers from the backend's OpenAPI (tools of the `msw-auto-mock` class) to remove drift; optionally Pact for consumer-driven bidirectional contracts |
| Dart / Flutter | A mock client or interceptor for `http` / `dio` | Generate models and mocks from OpenAPI; optionally Pact Dart |
| Other stacks | Look up that stack's network-layer interception mock | Look up that stack's mock generation from OpenAPI/schema plus bidirectional contract tooling |

**The translation work (the skill's job)**: MSW is generic, but it **does not know what your
backend contract looks like** — the skill must, **if the project has a backend contract
(OpenAPI or schema)**, generate the handlers from it and wire it into CI so contract updates
propagate into the mocks automatically.

**Typical assertion list**: the frontend renders data correctly per the contract shape; under
the contract's error responses (4xx/5xx) the frontend shows the correct fallback or error
state; mock handlers share their source with the backend contract (a contract change
triggers a mock update); optional Pact bidirectional verification passes.

---

## 5. 5. Visual regression

**Capability**: **screenshot** key pages and components and pixel-diff them against an
approved **baseline** to catch unintended UI regressions. The screenshotting and diffing are
**fully automatic**; but **judging whether a diff counts as a regression is human review**
(see the next section). Use **a fixed Docker rendering environment to remove platform
flakiness** (fonts, antialiasing and scaling differing between machines are the main source
of false positives).

**Why a human is needed**: a machine can only compute "N pixels changed"; it **cannot judge
whether that change is an intended redesign (update the baseline) or accidental breakage
(block it)** — that is a semantic judgement. So this layer closes the loop as "**diff
automatic, baseline adjudication human**".

| Stack | Screenshot / visual regression | Removing flakiness |
|---|---|---|
| JS / TS | Playwright `toHaveScreenshot` (self-hosted) or Chromatic (hosted, with its own review UI) | Run screenshots in a fixed Docker rendering environment; standardise fonts, viewport and freeze animations |
| Dart / Flutter | Golden tests (`matchesGoldenFile`) | Generate goldens in a fixed CI container environment |
| Other stacks | Look up that stack's visual regression / screenshot diff option | A containerised fixed rendering environment |

**Minimise the human-review volume (but approval stays human)**: a fixed Docker environment
removes platform flakiness, an optional AI pre-filter removes obvious false positives, and
presenting the diffs as a PR check lets a person approve them in one place. **Final approval
MUST NOT be automated** — do not bypass it by "auto-updating the baseline" (that is
equivalent to switching this layer off).

**Typical flow**: the first run establishes the baseline (human-confirmed) -> subsequent PRs
diff screenshots against it -> where there is a diff, the PR check presents it to a person ->
the person adjudicates: intended redesign means update the baseline, accidental breakage
means block and send back.

---

## The human-review point and what machines cannot assert

**Across the whole suite there is exactly one human-review point: the visual-regression
baseline adjudication in layer 5** (reasons above). The other four layers are fully automatic.

**A further class of visual and semantic concerns can never be asserted by a machine, and is
explicitly kept out of the automated suite** (left to code review and design walkthroughs):

- **Fidelity to a design sample or reference** ("does it look like that approved mockup");
- **Restraint in decoration** (is there superfluous ornament or noise);
- **Cognitive hierarchy** (is the important information visually emphasised correctly);
- **Overall craft and taste** ("does it look professional", "does it look machine-generated").

Forcing assertions onto these only produces brittle, misleading tests — **honestly place them
outside automation.**

---

## Cross-layer reminders

- **Lay the foundation first** (step 1 / section 0): the frontend often has zero foundation;
  install the missing runner, component library or browser driver rather than assuming L0/L1
  is ready.
- **Judge conditional hits before filling** (SKILL.md step 2): the five layers are not a
  checklist to complete; fill only the layers this feature actually hits.
- **Cheapest layer first**: what the layer 1 lint gate can block needs no test; what layer 2
  unit tests can assert needs no layer 5 screenshot.
- **Do not reinvent tools**: every layer has mature tooling — you are a fitter and an
  inspector, doing install, configure and translate; the tools fill the gap, the skill
  translates the contract.
- **Everything project-specific is conditional**: tokens, rise-and-fall colours, design
  specs, must-run pages — always "**if the project has it, then** read it and generate
  assertions accordingly".
- **RED must be meaningful**: confirm the test is red because of a genuine gap before going
  green, then harden it into the regression suite.
- **Guardrails**: write only tests and rules, never weaken an assertion, no fabricated fixes
  (including no "auto-refresh the baseline" to mask a regression), bounded retries, isolated
  changes delivered for human review; on finding a real bug, **HALT and hand it back to the
  TDD loop** rather than editing product code (see the self-healing guardrails in SKILL.md).
- **Archiving**: give every new rule or regression a traceable ID, grade it by risk, fold it
  into the release gate, and align it with the three-layer rhythm (per
  `testing-system-blueprint-en`).
