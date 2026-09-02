---
name: frontend-testing-en
description: Close frontend-only structural testing gaps after feature-level TDD by detecting the stack, establishing any missing test foundation, and configuring mature tools for lint rules, unit behavior, accessibility, responsive and cross-browser behavior, contract mocks, and visual regression. Translate project design contracts into executable checks, test only applicable gaps, and deliver isolated changes for human review. Use directly or when routed by test-routing-advisor-en. Not for: backend testing, cross-feature end-to-end chains, or reinventing test tooling (this skill only assembles tools and translates rules).
license: MIT
metadata:
  version: "1.0"
  lang: en
  stage: "9.2"
  standalone: true
  produces:
    - "Frontend test code"
    - "Evidence archive"
  requires:
    - name: "Routing decision report, or gaps named directly by the user"
      level: orchestration
      fallback: "Ask the user which frontend layer to close; with no answer, sweep all five layers"
    - name: "Project manifest file"
      level: required
    - name: "Visual / interaction contract (DESIGN.md or equivalent)"
      level: optional
      fallback: "Token and dark-mode assertions are marked as NOT COVERED; the remaining layers proceed as usual"
    - name: "Browser test tooling"
      level: optional
      fallback: "The cross-browser and responsive layer is marked as NOT COVERED"
---

# frontend-testing-en · Frontend-Only Closed-Loop Test Executor

## What This Skill Solves

Development-phase TDD (superpowers) and spec/contract testing (spec-kit) cover "whether functional logic works as specified." But frontend has a class of **structural gaps** that don't belong to any single feature — they belong to the runtime properties of the interface in a real browser: whether visual contracts truly reach the pixel level (whether colors/font sizes/spacing go through tokens, whether dark mode is covered, whether price colors match the target market convention), whether accessibility standards are met, whether layout breaks under cross-browser/multi-viewport conditions, whether the data contract with the backend holds up, whether UI changes have quietly introduced visual regressions. These gaps almost never get naturally written during development — especially when [FE] task "output verification" only says **"manual test"**.

> **Core distinction from backend-testing-en (must understand this)**: Backend gaps (true-database authorization bypass / concurrency / resilience) **have no pip/npm install-and-use tools**; backend-testing-en is a "**construction crew**" — a large amount of test code must be written from scratch.
> Frontend is **not** like this: every layer has mature, widely-adopted tools (linters, test runners + Testing Library, axe, Playwright, MSW, Chromatic...). So this skill **does not reinvent tools** — it is an "**assembler + inspector**": it only does three things: **install** (install the mature tools corresponding to the stack into the project) + **configure** (wire up configuration/CI) + **translate** (*this project's* visual/interaction contract into assertions and rules that these tools can mechanically execute).

### The Value This Skill Adds: Translation + Orchestration + Closed Loop Between General Tools and the Project Visual Contract

Mature tools are **general-purpose**, but they **don't understand your project**:

- stylelint can ban bare color values, but **doesn't know what your tokens are called, what their values are**, or which properties must go through `var()`.
- axe can scan for a11y issues, but **doesn't know which pages should be run**, whether a failure **counts** as a release gate blocker, or which design's contrast thresholds to use.
- Playwright can take screenshots and open multiple viewports, but **doesn't know that "no horizontal scrollbar" is a hard constraint, or what your price-color convention is** (some markets red = up green = down, others red = down green = up — the tool has no way to know which is "correct").
- MSW can mock the backend, but **doesn't know what your backend contract looks like** and won't update itself when fields change.

What this skill does is precisely **translate + orchestrate + close the loop** between **general tools and the project's visual/interaction contract/design tokens**: turning "the approved final product looks like this" into assertions/rules that machines can run repeatedly, wiring them into CI, and solidifying them as regressions. That's the part the tools themselves will never do for you, and the entirety of this skill's value.

Follows the `testing-system-blueprint-en` (reference by name as needed): risk-tiered ordering, traceable IDs, release gates, three-layer cadence.

---

## Two Absolute Constraints (Read First — Apply Throughout)

1. **stack-agnostic**: All five gap layers are expressed using "**capability description + per-stack instantiation lookup**" exclusively — never hardcode one stack as the only answer. The stylelint / Vitest / Playwright / MSW and other tools appearing in this document and in `references/gaps.md` are **example instances for the JS/TS stack** — they are "instances of the capability for that stack," not the only solution. **Read the project manifest (`package.json` or equivalent) first, then instantiate the tools corresponding to that stack.**
2. **project-agnostic**: No business-specific terms appear here, and no specific framework is assumed (no assumption of Next.js / React / any UI library). Everything project-specific — **design spec documents, design token names, token values, price-color conventions, which pages must be run** — is always written as a **conditional**: "**if the project has a visual spec / design tokens, then** read them and generate assertions accordingly." Used as examples, not as prerequisites: for projects without a visual spec, token-type assertions simply don't hit, and only structural/geometric/a11y layers run.

---

## Workflow (Six-Step Closed Loop)

### Step 0 · Identify the Stack

Read the project manifest file to determine the frontend stack and runtime; all subsequent tool choices are instantiated from this:

| Stack clue file | Frontend stack | Subsequent tool source |
|---|---|---|
| `package.json` (with `tsconfig.json`) | JS / TS (including various frameworks) | See the JS/TS row for each layer (main example stack for this skill) |
| `pubspec.yaml` | Dart / Flutter | Reverse-lookup capability equivalents for that stack (widget test / golden test / multi-device) |
| `*.csproj` + Blazor | .NET frontend | Reverse-lookup component testing + Playwright .NET for that stack |
| Other | As needed | Reverse-lookup ecosystem equivalents using the "capability" description |

> If no manifest file is found, stop and ask — don't assume. For monorepos, identify nearest to the frontend directory under test.

### Step 1 · Lay the Foundation (Frontend-Specific, Cannot Be Skipped)

**This is the biggest process difference between this skill and backend-testing-en**: frontend project test foundations are **often zero** — many [FE] task output verifications only say "manual test," and the project **may have no test runner / component test library / browser driver installed at all**. So wrapping up with supplemental tests **cannot assume L0/L1 is in place** — the foundation must be verified first and established if missing:

1. Check the manifest file to confirm whether it already has: ① a test runner; ② a component/DOM test library; ③ a browser driver (end-to-end/screenshot).
2. **If no test runner**: lay the foundation first (JS/TS stack example: Vitest + Testing Library + Playwright), wire up minimal configuration and scripts, and get "run one simple test and have it pass" to work first. **Without a working foundation, no subsequent layer can be discussed.**
3. If part of the foundation already exists, only fill in the missing parts — don't reinstall or replace already-chosen tools (surgical).

> Therefore this skill's coverage lower bound starts **from laying the foundation**, not "assume unit tests are in place, only supplement L2–L6."

### Step 2 · Conditional Hit (Prevent Over-Testing)

**Not all five layers are tested** — only supplement the subset that the feature actually hits. Evaluate layer by layer (see `references/gaps.md` for details):

| Layer | Hit condition | Non-hit example |
|---|---|---|
| ① Compile-time lint gate | Project has a visual spec / tokens, needs to ban bare color values, ban a second UI library, ban arbitrary values | No visual contract, no component library constraint |
| ② L0/L1 unit tests | Feature contains components / render logic / themes / price-colors or other visual behavior requiring assertions | Pure static copy, no logic pass-through |
| ③ a11y + cross-browser/responsive | Has interactive components, forms, multi-viewport/multi-browser requirements, geometric constraints (e.g., no horizontal scrollbar) | Pure backend with no UI |
| ④ Frontend-backend contract mock | Feature consumes backend APIs, needs to isolate backend and test frontend independently | No external data, purely static |
| ⑤ Visual regression | Has key pages/components that need to "look right" and will evolve | One-time internal pages, no visual contract |

Purely static / no visual contract features may only hit 1–2 layers — that is normal; don't force coverage.

### Step 3 · Instantiate Tools by Stack (Install + Configure)

For each **hit** layer, use the stack identified in Step 0 and take the corresponding row from `references/gaps.md` to **instantiate mature tools**: install them, wire up configuration, and include them in CI. **Don't build tools from scratch** (this is the fundamental difference from backend-testing-en). Label each layer with its closure type: **fully automated** (lint / unit tests / a11y / cross-browser / contract mock) vs **requires human review for decision** (only L2 visual baseline).

### Step 4 · Lint Gates + RED→GREEN Supplemental Tests

Supplement in "cheapest layer first" order:

1. **Add lint gates first (①, cheapest — no tests to write)**: Translate the project visual contract into lint rules (ban bare color values / only allow `var()`, ban second UI library imports, ban arbitrary-value hex classes). Blocked at compile time — no tests even needed — best cost-effectiveness ratio, do this first.
2. **L0/L1/a11y/responsive/contract (②③④, fully automated RED→GREEN)**: First write tests that will fail, confirm they are red because of a real gap/uncovered path (not because the test is written wrong) → then make them go green. **Translation happens here**: e.g., translate "price-color token values" into `getComputedStyle` assertions, translate "no horizontal scrollbar" into a geometric invariant assertion `scrollWidth <= clientWidth`, translate backend OpenAPI into MSW handlers.
3. **Visual regression (⑤) baseline left to human review**: Screenshot diffs are produced by machines, but "**does this diff count as a regression**" is a semantic judgment — **machines can only produce diffs, they cannot make the call**. Leave the baseline decision to humans (see "Human Review Node" below).

> See `references/gaps.md` for specific tools and code patterns; take the row corresponding to the stack identified in Step 0.

### Step 5 · Archive per Blueprint + Isolated Changes for Human Review

For each new lint rule / regression test added:

- Ordered by **risk tier** per `testing-system-blueprint-en` (e.g., authorization-style visual errors — price-color reversed misleads decisions — prioritized into release gate).
- Attached with **traceable IDs** (associated with feature / AC / hit layer).
- Included in **release gate**: clearly define which ones block release (e.g., wrong price-color, severe a11y violations, contract drift) and which are warning-level.
- Aligned with **three-layer cadence** (lint/unit tests land in fast layer; cross-browser/visual regression land in slower layers).
- Keep supplemental tests in an **isolated branch or change set for human review**; the upper-level wrap-up stage decides merge versus PR. The delivery note lists hit layers, skipped layers and reasons, and each new regression's corresponding layer and risk level.

---

## Five-Layer Landing Structure Quick Reference (See references/gaps.md for details)

Each layer = one gap type. All tools columns are **JS/TS stack examples** — instantiate by stack, not locked in.

| Layer | Mature tools (JS/TS examples, instantiate by stack) | Closure type |
|---|---|---|
| ① Compile-time lint gate (cheapest, highest priority) | stylelint (ban bare color values / only allow `var()`), ban second UI library import, ban Tailwind arbitrary-value hex classes | **Fully automated, no tests written** |
| ② L0/L1 unit tests | Vitest + Testing Library; including `getComputedStyle` assertions for token resolved values / dark mode coverage / price-color values | Fully automated RED→GREEN |
| ③ a11y + cross-browser/responsive | axe-core / @axe-core/playwright (auto-detects ~57% of a11y issues, contrast accounts for ~30%); Playwright projects multi-viewport + geometric invariant assertions (no horizontal scrollbar `scrollWidth<=innerWidth`) | Fully automated |
| ④ Frontend-backend contract mock | MSW + generate handlers from backend OpenAPI (anti-drift), optionally Pact bidirectional contract | Fully automated in CI |
| ⑤ Visual regression | Playwright screenshots / Chromatic, Docker run to eliminate platform flakiness | Screenshot diff automated, **baseline decision requires human review** |

---

## Human Review Node: The Entire Suite Has Only One = L2 Visual Baseline Decision

In this entire supplemental test suite, **machines have automated the vast majority of what they can** — lint, unit tests, a11y, cross-browser, responsive geometry, contract mocks are all deterministic judgments. **The only node in the entire suite that truly requires human review is: L2 visual regression baseline decision.**

- **Why only this one requires a human**: "Does this screenshot diff count as a regression" is a **semantic judgment** — it could be an intentional design revision (should update baseline) or accidental breakage (should block). Machines can only compute "N pixels changed" — **they cannot judge whether that change is good or bad**.
- **How to minimize the human review workload**: Docker fixes rendering environment to eliminate platform flakiness (biggest source of false positives) + optionally AI pre-filter obvious false positives + present diffs centrally as a PR check. But **final approval is still human** — this is the inherent non-automatable nature, don't pretend it can be eliminated.

### Another Category: Things Machines Can Never Assert — Only Human Review (Explicitly Excluded from Automation)

Beyond the "baseline decision," there is another category of visual/semantic items **that fundamentally cannot be written as machine assertions** and must be listed separately, explicitly **excluded** from the automated suite, and left to human review (typically code review / design walkthrough):

- **Fidelity to design samples/references** ("does it look like the approved final-product reference");
- **Decorative restraint** (whether there is unnecessary decoration or noise);
- **Cognitive hierarchy** (whether important information is visually emphasized correctly);
- **Overall quality/taste** ("does it look professional," "does it have an AI-generated feel").

Forcing assertions for these items only produces brittle, misleading tests. **Explicitly placing them outside the automation scope is an honest part of this system.**

---

## Self-Healing Guardrails (Must Not Be Crossed)

The supplemental test process allows bounded automated iteration (RED→GREEN), but is constrained by the following guardrails (inherited from the blueprint):

- **Only write tests / lint rules, don't change product code** — this is the default action. This skill is an "assembler + inspector"; its responsibility is to install tools, configure rules, and translate assertions — **not to modify business implementation**.
- **Assertions must not be weakened** — it is forbidden to relax assertions to make tests go green (e.g., commenting out price-color assertions, lowering contrast thresholds, deleting the "no horizontal scrollbar" geometric assertion, adding allowlist exemptions for a11y violations). Going green must come from correct product code or correct tests — not from lowering the standard.
- **Fake fixes are forbidden** — it is not permitted to fake a pass using `skip`, forcibly updating visual baselines to mask real regressions, or mocking out the rendering being tested.
- **Bounded retry escalation** — automated iteration has an upper limit; reaching it without passing means stop and escalate to a human — don't loop forever (visual flakiness especially must not be misread as "one more run will fix it").
- **Isolated changes + human review** — keep all outputs in an isolated branch or change set for review; the upper-level wrap-up stage decides merge versus PR.
- **Discovering a real bug requires HALT, return to superpowers TDD for fix** — this skill **does not modify product code itself**. During supplemental testing, if a RED exposes a real product defect (not just missing coverage), **stop**, return the defect to `superpowers:test-driven-development` / `superpowers:systematic-debugging` for a fix cycle, then return to this skill to solidify the regression.

The purpose of these guardrails: allow the closed loop to run automatically, but block any shortcut that makes things "look green without actually being tested" or "crosses the line to modify product code."

---

## Relationship to Upstream and Downstream

- Upstream: `test-routing-advisor-en` calls this skill when it determines "frontend-only" (can also be triggered directly by the user).
- Blueprint: all archiving / tiering / release gates / cadence follow `testing-system-blueprint-en` (reference by name; its content is not replicated here).
- Sibling: `backend-testing-en` handles "backend-only"; their fundamental responsibilities differ — backend **builds test code from scratch** (construction crew), frontend **assembles mature tools + translates visual contract** (assembler + inspector).
- Methodology reuse: Fix and debug of discovered real defects reuses `superpowers:test-driven-development` and `superpowers:systematic-debugging` (this skill HALTs and returns to them).


## Upstream Artifacts

| Artifact | Level | When missing |
|---|:---:|---|
| Routing decision report, or gaps named by the user | orchestration | Ask the user; with no answer, sweep all five layers |
| Project manifest file | **required** | Stop — the technology stack cannot be determined |
| Visual / interaction contract | optional | Token and dark-mode assertions are marked NOT COVERED |
| Browser test tooling | optional | Cross-browser and responsive coverage is marked NOT COVERED |

## Downstream Consumers

| Consumer | What it reads |
|---|---|
| The partial-fullstack seam skill | The frontend-side mock assumptions |
| Branch wrap-up | Test results and residual risks |

## Standalone Use

**What you provide**: a frontend feature and the project dependency manifest. Visual assertions can only land when a design source of truth exists.

**What you get**: backfill for the five layers of frontend structural gaps: lint gates, unit tests, a11y / cross-browser, frontend-backend contract mocks, visual regression.

**What you don't get**:

- **No visual contract means no visual assertions** — assertions such as tokens and dark mode are marked NOT COVERED; no standard is invented out of thin air.
- No reinvented tooling; only assembly and rule translation.
- Tests only; product code is not modified.
