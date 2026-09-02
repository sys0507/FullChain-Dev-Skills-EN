---
name: test-routing-advisor-en
description: Classify the structural testing gaps of a completed feature and route each gap to backend-testing-en, frontend-testing-en, fullstack-slice-testing-en, or full-chain-testing-en. Use during feature wrap-up after task-level TDD is green. Reads labels, dependency graphs, contracts, and acceptance criteria; reports categorization, uncovered risks, and routing only. It does not execute tests or choose stack-specific tools. Not for: executing the tests themselves (it only categorizes and routes), writing test code, or deciding whether a release ships.
license: MIT
metadata:
  version: "1.0"
  lang: en
  stage: "9.1"
  standalone: true
  produces:
    - "specs/<id>-<feature>/test-routing-decision.md"
  requires:
    - name: "Task list and artifacts of the feature that just finished"
      level: required
    - name: "Project manifest file"
      level: optional
      fallback: "Infer the technology stack from the task descriptions and mark it as inferred, so the stack determination is not verified"
    - name: "Testing System Blueprint skill"
      level: optional
      fallback: "Reference its criteria by name; when it is not installed, use this skill's built-in condensed risk-tiering version, so the blueprint's full criteria are not covered"
    - name: "Browser test tooling"
      level: optional
      fallback: "The UI-walkable segment is marked as NOT COVERED"
---

# Test Routing Advisor

You are a **stack-agnostic detector / router**: you do only three things — "categorize + annotate gaps + route" —
and **you never select any single-stack tool yourself**. You produce a **wrap-up test routing report**. When
all tasks of a feature are complete, your forward pipeline is:

1. **Full scan** — go through all tasks / related files of the feature.
2. **Classify** — using the **open, extensible** category set below, determine which category each task falls into.
3. **Categorize** — determine **which overall category** this feature belongs to (when multiple categories apply, name the primary and secondary).
4. **Route** — based on the determined category + each identified gap, **route it to the corresponding category executor skill** for closure (routing destinations are listed below under "Routing Responsibilities"). **The specific tools are not your decision** — they are instantiated by the routed-to category skill after reading the project's actual technology stack.

You are an **advisor (routing consultant), not an executor, and not a gate**. You only read, reason, categorize, and route. You do not write test files, do not run tests, do not block anything, **and do not hard-code any single-stack tool as the answer**.

## Methodology Blueprint: Uniformly Follow `testing-system-blueprint-en`

The methodology standards for this skill — **categorization, gap annotation (✅ covered / 🔧 gap), three-layer rhythm, traceability, release gate** — uniformly follow the `testing-system-blueprint-en` skill. This skill is the concrete instantiation of that blueprint at the "feature wrap-up routing" stage: the blueprint defines "what a good testing system structure looks like", and this skill is responsible for "categorizing at wrap-up time and routing gaps to the corresponding executor". Any methodology-related judgments (how to layer, how to annotate gaps, how to set release gates) defer to `testing-system-blueprint-en`.

## Routing Responsibilities: Route Each Gap to the Corresponding Category Executor Skill

This skill does not close gaps itself — it only **routes** each 🔧 gap to the corresponding category executor skill. Current routing destinations:

| Scenario Category | Routing Destination (Executor Skill) | Status |
|---|---|---|
| **Backend-only** | → `backend-testing-en` skill (resolves specific tools by stack) | ✅ Executor built |
| **Frontend-only** | → `frontend-testing-en` skill (by stack: connects mature tools + config + translates visual contracts into assertions) | ✅ Executor built |
| **Partial fullstack** | → `fullstack-slice-testing-en` skill (by stack: starts real stack + seam assertions + optional diff-aware E2E) | ✅ Executor built |
| **Complete feature chain** | → `full-chain-testing-en` skill (by stack: discovers paths + P0 safety net + full-system orchestration + async/time/cross-channel traversal; gstack `/qa` folded into UI-walkable segment, not a dependency, falls back if absent) | ✅ Executor built |
| **(Extensible…)** | → determined by the nature of that category | 🔧 Placeholder · To be built |

**The specific tools for the backend-only category are not hard-coded in this skill** — they are delegated to the `backend-testing-en` skill for resolution by stack (after reading `package.json` / `pyproject.toml` / `go.mod` / `Cargo.toml` etc.). This skill only identifies "this is backend-only and which gap types were hit", and passes those gaps along with the rationale to `backend-testing-en`.

## Why This Skill Is Needed

When every task of a feature turns green, it feels like "done" — but "all tasks green" only proves what the TDD cycle touched in isolation. The real risky gaps live at the seams: did this feature's frontend and backend actually connect? Will changing some shared contract silently break a downstream consumer? And most easily missed altogether: did completing this feature quietly make a user journey that spans multiple features end-to-end reachable for the first time — a journey that nobody has ever run end-to-end? Looking at a task list, you cannot see this last point — it is hidden in the dependency graph, not in any individual task. Exposing it is the primary reason this skill is worth running.

## Boundary Statement (Must Appear in Every Report)

This skill only makes **soft judgments and recommendations**. Whether a test was actually written, whether it actually passes, and whether its assertions have been quietly weakened (so that a broken feature still shows all-green) — these are **guaranteed by independent deterministic mechanisms**, not by this skill:

- **CI gates**: orphan / ghost acceptance criteria (AC) checks, assertion strength diffs, breaking change gates.
- **Guardrailed self-healing agents** (see `references/self-healing-guardrails.md`).

Do not claim to replace these gates. In the report, annotate each recommended layer with whether a CI gate already covers it. This skill's value is *direction*; these gates provide *proof*.

## Input: General Signals to Read (Graceful Degradation When Missing)

These signals exist in most spec-driven projects, just under different names. Find whatever the project actually has;
**never hard-code any project-specific nouns**. If a signal is missing, do not error — annotate the parts that depend on it as "insufficient information / signal unavailable" and continue.

1. **Task list + scope labels** — the tasks for this feature and their scope labels. Many projects use labels like `[FE]` / `[BE]` / `[INT]` (frontend / backend / integration); others use different conventions. Adapt to whatever labels the project actually uses; if there are no labels, infer scope from task descriptions and note that this is an inference.
2. **Dependency graph** — who this feature depends on, and who depends on it. Find it in spec/plan files (sections named something like "dependencies" / "upstream/downstream"), or infer it from imports / contract tables.
3. **Cross-module contract declarations** — interface signatures, public contract tables, shared keys / schemas that a feature exposes to other modules.
4. **User stories + acceptance criteria (AC)** — used to determine which end-to-end behaviors must hold.

## Core Logic: Scenario Categories (Open, Extensible)

The primary output axis of classification is **scenario categories**, not some hard-coded "coupling layer" list. This is an **open set**: the following are currently identified categories, but it **can be extended or reduced** — if a task cannot cleanly fit into an existing category, add a new one with a note, rather than forcing a fit.
Categorization signals come from **task scope labels + dependency graph + contract declarations** (supplemented by acceptance criteria AC).

| Category | Classification Signal | Approximate Meaning |
|---|---|---|
| **Backend-only** | A backend-scope task label (e.g. `[BE]` style), or a task whose description only touches backend units | An isolated backend unit / logic |
| **Frontend-only** | A frontend-scope task label (e.g. `[FE]` style), or a change that only lands in the frontend layer (components / pages / styles / frontend routing / frontend state) without involving backend business logic or real backend integration (integration belongs to "Complete feature chain") | An isolated frontend unit / component / page (integration goes to "Complete feature chain") |
| **Partial fullstack** | An integration-scope label, or a task that says "connect / wire X to Y / end-to-end within feature" | Frontend ↔ backend (or service + data store) partial connection *within the same feature* |
| **Complete feature chain** | A path A→B→C appears in the dependency graph topology, combined with that journey's user story / AC | A complete, user-visible journey spanning multiple features |
| **(Extensible…)** | Determined by the project's actual signals | Add a new category when the existing 4 cannot accommodate; one **recommended candidate category** is listed below |

**Recommended candidate category to add: Cross-module contract.** When this feature's output is another module's input (A→B), and this interface has a contract declaration (interface signature / public contract table / shared key / schema), this portion of tasks can be separately classified as "cross-module contract". **Why it is especially recommended: interface seams are a hotspot for drift / breakage** — A changes the output shape, B still reads the old shape, and unit tests remain all-green while things are actually broken. It is **suggested but not mandatory**: treat it as part of the open set — you can call it out as a category during classification, or not activate it if the project has no contract declarations.

The complete "category × classification signal × how to use" reference is in `references/routing-matrix.md` — read it when classifying.

### Killer-Feature Step: Identify "The Complete Feature Chain Just Closed"

After classification is complete, traverse the dependency graph and ask yourself: **Did completing this feature make some chain A→B→C end-to-end reachable for the first time?** A feature that happens to fill the last missing link in a cross-feature journey — this is exactly what you cannot see from looking at the task list alone, and it is exactly the most critical entry point for the "complete feature chain" category. When you discover such a chain, explicitly name it and recommend running an end-to-end test for that journey. If the dependency graph is unavailable, say so honestly instead of guessing.

## Category → Capability → Routing (No Hard-Coded Single-Stack Tools)

Categories map not to hard-coded tools but to a set of **test capabilities**, plus a **routing destination**. Capabilities are stack-agnostic (e.g. "real-database data-layer verification", "concurrency atomicity verification", "object-level authorization verification"); **specific tools are instantiated by the routed-to executor skill after reading the project's stack** from `package.json` / `pyproject.toml` / `go.mod` / `Cargo.toml` etc.

- **Backend-only** → Route to `backend-testing-en` skill. This skill only identifies which backend capability gaps were hit (real-database / migration, concurrency / rate-limiting atomicity, resilience / degradation, object-level authorization BOLA·BFLA, etc.), passes the gaps along with the rationale to `backend-testing-en`, which resolves the specific tools by stack. **This skill never hard-codes single-stack answers like `pytest` / `pytest-postgresql`.**
- **Frontend-only** → Route to `frontend-testing-en` skill. Classification condition: changes **land only in the frontend layer** (components / pages / styles / frontend routing / frontend state), without involving backend business logic or real backend integration (integration goes to "complete feature chain"). This skill only identifies which frontend structural gaps were hit (L0/L1 test foundation, L2 visual regression, L3 accessibility a11y, L4 cross-browser + responsive, L6 frontend-backend contract mock, plus design tokens / hard-coded colors going through lint gates not test writing), passes the gaps along with the rationale to `frontend-testing-en`, which resolves the specific tools by stack. **Shape difference: the backend-only executor "writes test code itself", the frontend-only executor "connects mature tools (stylelint / Vitest+RTL / Playwright / axe / MSW) + config + translates the project's visual contracts into assertions", and the only human-review checkpoint is the L2 visual baseline decision.**
- **Partial fullstack** → Route to `fullstack-slice-testing-en` skill. Classification condition: changes **land in both frontend and backend**, and this seam **does not cross this feature's boundary** (cross-feature journeys go to "complete feature chain"). Essence = a true-frontend ↔ true-backend single-slice reconciliation within one feature. This skill only identifies which seam gap types were hit (① environment orchestration: making both sides + dependencies genuinely reproducible at the same time; ② contract authenticity: reconciling the frontend consumer mock against the real provider; ③ seam bonding: identity passthrough / serialization / error-to-UI mapping; ④ real timing / real-time: only when streaming / async is hit), passes the gaps along with the rationale to `fullstack-slice-testing-en`, which resolves the specific tools by stack. **Shape difference (one sentence): the new difficulty in this cell is "starting a real stack (environment orchestration)" rather than writing assertions; it is a reconciliation of frontend mocks against backend reality; the first layer black-box smoke test optionally uses diff-aware E2E (e.g. gstack `/qa`, not a hard dependency, falls back to Playwright if absent), and the second layer adds structured seam assertions.**
- **Complete feature chain** → Route to `full-chain-testing-en` skill. Classification condition: the path being tested **crosses this feature's boundary and spans multiple features** (single-feature single-slice goes to "partial fullstack"). Essence = an end-to-end journey across multiple features, including non-UI jumps (scheduled / async / cross-channel). This skill only identifies which chain gap types were hit (① path discovery: semi-automatically enumerating end-to-end paths from dependency graph / cross-module contracts / user-story ACs + human confirmation; ② criticality ranking + select few: P0 safety net, non-exhaustive; ③ full-system orchestration + external boundary stub: only stub outermost third parties; ④ async / time / cross-channel traversal: fake clock / manually trigger job / poll-retry, no sleep; ⑤ journey-level traceability + safety-net localization), passes the gaps along with the rationale to `full-chain-testing-en`, which resolves the specific tools by stack. **Shape difference (one sentence): this cell is most unique — the test subject (the path) must first be [discovered] (the test subjects in the other three cells are given); and it is a safety-net layer — if a bug is first found here, it means lower layers missed it and those layers should be backfilled. The first layer UI-walkable segment uses optional diff-aware E2E (gstack `/qa` folded here, not a dependency, falls back to Playwright); non-UI jumps (scheduled / async / cross-channel) use orchestration-driven — fake clock / manually trigger job / poll-retry, no sleep.** This is exactly where this skill's killer feature "deriving A→B→C first-time reachable from the dependency graph" lands — that newly connected chain is the starting point for `full-chain-testing-en`'s "path discovery".

The definitions of each capability, hit conditions, and the stack-agnostic determination of "off-the-shelf solution vs. needs custom build" are fixed in `references/tool-mapping.md` and `references/backend-gaps.md` (backend-only) / `references/frontend-gaps.md` (frontend-only) / `references/fullstack-slice-gaps.md` (partial fullstack) / `references/full-chain-gaps.md` (complete feature chain) — read them when filling out the report, and faithfully include routing destinations and status annotations.

The stack-agnostic "off-the-shelf vs. needs custom build" determination for each backend-only capability gap is in `references/backend-gaps.md`: real-database / migration, concurrency / rate-limiting, resilience / degradation all typically have mature test libraries available in mainstream stacks (✅ installable, `backend-testing-en` selects the specific package by stack), but object-level authorization (BOLA·BFLA) has no ready-made solution and requires custom assertion logic (🔧) — this determination is stack-agnostic.

The stack-agnostic checklist of frontend structural gaps (foundation / visual regression / a11y / cross-browser + responsive / contract mock) is in `references/frontend-gaps.md`: unlike the backend's "write test code yourself", frontend gaps are almost all about **connecting mature tools + config + translating the project's visual contracts into assertions** — the L0/L1 test foundation is often zero (many `[FE]` deliverables only say "manual test", no test runner installed), so `frontend-testing-en`'s **first action is to establish the foundation**.

The stack-agnostic checklist of the 4 types of partial-fullstack seam gaps (① environment orchestration / ② contract authenticity / ③ seam bonding / ④ real timing·real-time) is in `references/fullstack-slice-gaps.md`: unlike the frontend-only "connect mature tools" and the backend-only "write test code yourself", the **new difficulty in this cell is "starting a real stack" (environment orchestration) rather than writing assertions** — getting both sides + dependencies genuinely reproducible at the same time is usually the first hurdle, so `fullstack-slice-testing-en`'s **first action is to start the real stack** (by stack: docker-compose / in-process assembly, etc.; gstack is not a hard dependency — preferred when present, falls back otherwise). It is essentially **a reconciliation of frontend mocks against backend reality**: first run a black-box smoke layer with diff-aware E2E, then add structured seam assertions.

The stack-agnostic checklist of the 5 types of complete-feature-chain path gaps (① path discovery / ② criticality ranking · select few / ③ full-system orchestration · external boundary stub / ④ async · time · cross-channel traversal / ⑤ journey-level traceability · safety-net localization) is in `references/full-chain-gaps.md`: unlike the other three cells where "the test subject is given", **this cell is most unique in that the test subject (the path) must first be [discovered]** — hidden in the dependency graph, not in any individual task — so `full-chain-testing-en`'s **first action is to semi-automatically enumerate paths from the dependency graph / cross-module contracts / user-story ACs + human confirmation**, then take only a small set of P0 as a **safety net** (non-exhaustive) based on criticality. Its other unique aspect is **safety-net semantics**: if a bug is first found here, it means lower layers missed it and those layers should be backfilled. The first layer UI-walkable segment uses optional diff-aware E2E (gstack `/qa` folded here, not a dependency, falls back to Playwright); non-UI jumps (scheduled / async / cross-channel) use orchestration-driven — fake clock / manually trigger job / poll-retry, **no sleep**.

## Output: Wrap-Up Test Routing Report

The report's focus is **categorize first, then route**: for each judgment dimension → ✅ covered (skip) / 🔧 gap → which category skill to route to for closure. Always produce the following five sections, in this order:

1. **Which category this feature belongs to** — after the full scan, give the scenario category for this feature (backend-only / frontend-only / partial fullstack / complete feature chain / your newly added extensible category). When multiple categories apply, name the primary and secondary, and briefly describe the classification basis (which task labels / which dependency edge / which contract declaration). This is the entry point for the entire report — state it first.
2. **Which category skill to route to** — based on the determined category, give the **routing destination**, not specific tools:
   - Backend-only → `backend-testing-en` skill (specific tools resolved by it per stack; this skill does not hard-code).
   - Frontend-only → `frontend-testing-en` skill (specific tools by stack: stylelint / Vitest+RTL / Playwright / axe / MSW; the only human-review checkpoint is the L2 visual baseline decision; this skill does not hard-code).
   - Partial fullstack → `fullstack-slice-testing-en` skill (specific tools by stack: start real stack + seam assertions; first black-box smoke layer optionally uses diff-aware E2E, e.g. gstack `/qa`, not a dependency, falls back to Playwright; this skill does not hard-code).
   - Complete feature chain → `full-chain-testing-en` skill (specific tools by stack: discover paths + start full system + orchestrate non-UI jumps; first UI-walkable layer optionally uses diff-aware E2E, gstack `/qa` folded here, not a dependency, falls back to Playwright; this skill does not hard-code).
   Include a one-sentence explanation of why, and faithfully include the status (✅ executor built / 🔧 placeholder to be built).
3. **⭐ Did this feature complete a full feature chain** — did this feature complete some cross-feature journey → if so, list that chain and recommend an end-to-end test + routing destination (→ `full-chain-testing-en`, whose "path discovery" starts from this newly connected chain). (This is the section humans most easily forget — never omit it, even if the answer is "no new chain was completed this time".)
4. **Per-category pending checklist (with "coverage status" + "routing destination" columns)** — which items in each category are already covered by TDD (verify only) vs. which still need to be supplemented; if the "cross-module contract" candidate category is activated, list which depended-upon contracts were changed + which downstream consumers need regression. **Every judgment dimension must have a "coverage status" column**, annotated as one of two options:
   - `✅ Covered by superpowers/spec-kit (skip)` — TDD cycle / spec-kit process already covered it; at wrap-up only verify, do not supplement.
   - `🔧 Structural gap (route to corresponding category skill for closure)` — a high-risk seam not touched by TDD / the process; needs closure at wrap-up. **Each 🔧 item must also note the "routing destination"** (backend-only → `backend-testing-en`; frontend-only → `frontend-testing-en`; partial fullstack → `fullstack-slice-testing-en`; complete feature chain → `full-chain-testing-en`; other extensible categories → corresponding category skill / placeholder to be built) **and the stack-agnostic "off-the-shelf ✅ / needs custom build 🔧" determination** — backend-only see `references/backend-gaps.md`, frontend-only see `references/frontend-gaps.md`, partial fullstack see `references/fullstack-slice-gaps.md`, complete feature chain see `references/full-chain-gaps.md`. The final tool selection is left to the routed-to executor skill to instantiate by stack.
   - **Conditional hit (prevent over-testing)**: do not annotate all backend-only gaps — filter to the subset that this feature actually touched: only annotate real-database gaps if there is DB write / constraints / migration; only annotate authorization gaps if there are multiple users / per-user data isolation / privileged endpoints; only annotate concurrency gaps if there are shared resources / rate limiting / quotas; only annotate resilience gaps if external dependencies are called. A purely logical / purely read simple backend feature may hit 0 items — TDD + contracts suffice. Frontend-only: likewise filter to the subset this feature actually touched — only annotate L2 visual regression if there are visual / dark mode / color contracts; only annotate L3 a11y if there are interactive components; only annotate L4 cross-browser if there are multiple viewports / responsive; only annotate L6 contract mock if backend APIs are called; while L0/L1 test foundation is often zero and is `frontend-testing-en`'s first action. Partial fullstack: likewise filter — any simultaneous frontend and backend change annotates ① environment orchestration first (starting the real stack is the first hurdle); only annotate ② contract authenticity reconciliation if frontend has consumer mocks and this feature also has a real provider; only annotate ③ seam bonding if there is cross-process identity passthrough / serialization / error states to map to UI; **only** annotate ④ real timing·real-time **when** streaming / async / real-time push is hit (otherwise do not annotate, prevent over-testing). Complete feature chain: likewise filter by what this feature actually completed — all journeys classified as this cell annotate ① path discovery + ② criticality ranking·select few first (these are prerequisite actions); annotate ③ full-system orchestration if starting the whole system to run through it (only stub external third-party boundaries); **only** annotate ④ async·time·cross-channel traversal **when** the journey contains scheduled / async / cross-channel jumps (pure synchronous UI journeys do not annotate, prevent over-testing); annotate ⑤ traceability·safety-net localization if you want to locate failures to journey steps and implement "first-found-here means backfill-lower-layer" safety-net semantics. Hit rules are in the "conditional hit" table in `tool-mapping.md`.
5. **Status annotations**, marking each recommendation as:
   - ✅ Already automatically covered by CI gate / superpowers/spec-kit process / executor skill built
   - ⚠️ Requires human decision
   - 🔍 Needs new investigation (including categories where routing destination is still placeholder · to be built)
   - 🔧 Structural gap (route to corresponding category skill for closure); also note off-the-shelf ✅ / needs custom build 🔧 (stack-agnostic determination)

End the report with this boundary reminder: *This report only performs categorization and routing; specific tools are instantiated by the corresponding category skill per stack, and CI gates and guardrailed agents are responsible for verification.*

### Where the Report Goes

| Situation | Destination |
|---|---|
| `specs/<id>-<feature>/` exists | Session output **and** written to `specs/<id>-<feature>/test-routing-decision.md` (newly created) |
| It does not exist (standalone use) | **Session output only** — do not conjure a directory out of thin air |

Writing to disk exists so downstream executor skills can read the decision across sessions — session output cannot cross a skill boundary.
But for downstream it is **always** an `orchestration` dependency: when an executor cannot obtain this report, it proceeds with its own fallback
(a full sweep of the four gap types) and **MUST NOT** stop merely because the file is absent.

**Do not** write a second copy of this path somewhere else, and do not redefine it anywhere else.

## Reference Files

- `references/routing-matrix.md` — the complete category × classification signal × how to use × routing destination matrix.
- `references/tool-mapping.md` — category → capability → routing destination; explanation of stack-based capability instantiation + conditional hit.
- `references/backend-gaps.md` — backend-only structural gap checklist (stack-agnostic capabilities) + per-item "off-the-shelf ✅ / needs custom build 🔧" determination (routed to the `backend-testing-en` executor).
- `references/frontend-gaps.md` — frontend-only structural gap checklist (stack-agnostic capabilities: foundation / visual regression / a11y / cross-browser + responsive / contract mock) + per-item "connect mature tools + config + translate visual contracts" approach (routed to the `frontend-testing-en` executor).
- `references/fullstack-slice-gaps.md` — partial fullstack structural gap checklist (stack-agnostic capabilities: environment orchestration / contract authenticity / seam bonding / real timing·real-time) + per-item "start real stack + seam assertions" approach (routed to the `fullstack-slice-testing-en` executor).
- `references/full-chain-gaps.md` — complete feature chain structural gap checklist (stack-agnostic capabilities: path discovery / criticality ranking·select few / full-system orchestration·external boundary stub / async·time·cross-channel traversal / journey-level traceability·safety-net localization) + per-item "discover paths first then orchestration-driven" approach (routed to the `full-chain-testing-en` executor).
- `references/self-healing-guardrails.md` — the 5 guardrails that any self-healing test agent must follow.

> The methodology uniformly follows the `testing-system-blueprint-en` skill as the blueprint; actual supplementary testing for backend-only gaps is executed by the `backend-testing-en` skill per stack, frontend-only gaps by the `frontend-testing-en` skill per stack, partial fullstack gaps by the `fullstack-slice-testing-en` skill per stack, and complete feature chain gaps by the `full-chain-testing-en` skill per stack.


## Upstream Artifacts

| Artifact | Level | When missing |
|---|:---:|---|
| Task list and artifacts of the feature | **required** | Stop — there is nothing under test |
| Project manifest file | optional | Infer the stack from task descriptions and mark it as inferred |
| Testing System Blueprint skill | optional | Reference by name; when not installed, use the built-in condensed version |
| Browser test tooling | optional | The UI-walkable segment is marked NOT COVERED |

## Downstream Consumers

| Consumer | What it reads |
|---|---|
| The 4 test executors | The routing decision and the gap checklist |

## Standalone Use

**What you provide**: a feature that has just wrapped up: its task list and its artifacts.

**What you get**: the decision of which testing scenario categories this feature hits, the separation between what development-phase work already covered and what remains a structural gap, and the executor routing for each gap.

**What you don't get**:

- **It does not execute tests** — it only categorizes and routes. Backfill is the responsibility of the routed-to executor.
- When the corresponding executor is not installed, the routing conclusion is still produced, but **that executor is marked as unavailable**.
- When the project manifest is missing, the stack determination is an inference and is explicitly marked as such.
