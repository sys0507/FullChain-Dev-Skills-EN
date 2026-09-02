# Test routing matrix (full version)

This matrix maps a feature's signals to the **scenario category it belongs to**, and the
category then **routes to the executor skill for that category** (see the "category ->
capability -> routing" table in `tool-mapping.md`) to close the gap. **This skill only
classifies, marks gaps and routes; it hardcodes no single-stack tool** — the actual tools
are instantiated by the executor skill against the project's stack. Read this when
classifying at feature close-out. Nothing here is project-specific: substitute your
project's own names for the signals, and degrade gracefully when a signal is absent.

> Methodology (classification / gap marking / three-layer rhythm / traceability / release
> gate) follows the `testing-system-blueprint-en` skill as its blueprint.

## The category set is open

The primary axis of classification is the **scenario category**, and it is **open — you may
add to it**. Below are the categories identified so far, but when a task will not fit
cleanly into an existing one, **add a category and say so** rather than forcing it into an
ill-fitting one. Classification signals come from **task scope labels + the dependency
graph + contract declarations**, supported by acceptance criteria.

## What the columns mean

- **Category** — which scenario category this group of tasks falls into. This is what
  determines which executor skill they route to.
- **Classification signal** — what in the project tells you these tasks belong here.
- **How to use it** — what to do with this category at close-out.
- **Routes to** — which executor skill this category's gaps go to (that skill instantiates
  the concrete tools for the stack).

## The matrix

| Category | Classification signal | How to use it | Routes to (executor skill) |
|---|---|---|---|
| **Backend only** | A backend-scoped task label (a `[BE]`-style marker), or tasks whose description touches only backend units | Unit tests are usually already written during TDD; at close-out only **verify coverage exists**, and route structural gaps out to be filled | `backend-testing-en` (executor built; resolves tools by stack) |
| **Frontend only** | A frontend-scoped task label (an `[FE]`-style marker), or tasks touching only frontend units — changes land **in the frontend layer alone** (components / pages / styles / frontend routing / frontend state), with no backend business logic and no live backend integration (that belongs to "full functional chain") | Unlike backend-only, the frontend L0/L1 test foundation is frequently absent (`[FE]` outputs often say "tested manually" with no test runner installed); at close-out verify the foundation exists, then mark visual-regression / a11y / cross-browser + responsive / contract-mock gaps and route them out | `frontend-testing-en` (executor built; wires mature tools per stack, configures them, and translates visual contracts into assertions — the single human-review point is adjudicating the L2 visual baseline) |
| **Local full-stack slice** | Changes land in **both frontend and backend**, and the seam **does not cross the feature boundary** (journeys spanning several features belong to "full functional chain"); or an integration-scoped label, or a task described as "wire up / connect X to Y / end-to-end within the feature" | After the units are green and before declaring the feature done, add a single-slice reconciliation of *real frontend to real backend* **within the same feature** — the new difficulty is standing the real stack up (environment orchestration), not writing assertions: run a diff-aware E2E black-box smoke first, then add structured seam assertions. This is the most common genuine gap at close-out | `fullstack-slice-testing-en` (executor built; stands up the real stack per the project's stack and adds seam assertions; a diff-aware E2E tool is optional, fall back when absent) |
| **Full functional chain** | The dependency graph topology shows an A->B->C path that **crosses the feature boundary and spans several features**, combined with that journey's user story and acceptance criteria; includes non-UI hops (scheduled / async / cross-channel) | Once the topology shows the journey has **become reachable for the first time**, name that chain; its subject under test (the path) must first be **excavated** (the first three cells give the subject), then take only a small handful of P0s by criticality as a **safety net** (not exhaustive — a bug first surfacing here means a lower layer under-tested it, so backfill the lower layer) | `full-chain-testing-en` (executor built; excavates paths per stack, orchestrates the whole system stubbing only external third parties, and drives async / timing / cross-channel orchestration; a diff-aware E2E tool for UI segments folds in here, optional, fall back when absent) |
| **(further categories...)** | Depends on the project's actual signals | When existing categories will not hold it, add one and state the basis for the classification | Depends on the nature of that category (placeholder, to be built) |

## A recommended candidate category: cross-module contract

When this feature's output is another module's input (A->B), and that interface has a
**contract declaration** (an interface signature, a published contract table, a shared key,
a schema), those tasks can form their own "cross-module contract" category.

- **Why it is worth recommending:** interface seams are where **drift and breakage
  concentrate** — A changes the shape of its output while B still reads the old shape, and
  both sides' unit tests stay green while the seam is broken. Only a contract layer catches
  that silent A->B mismatch.
- **It is a suggestion, not a requirement:** treat it as part of the open set. Where the
  project has contract declarations, call it out as a category; where it has none, do not
  enable it, and say in the report "insufficient information — no contract declaration
  found" rather than inventing one.

## How to use this matrix

1. **Scan everything and classify the tasks.** Read the scope labels (or infer scope) and
   place each task in a category. Backend-only and frontend-only work is usually already
   covered by the TDD loop — your job is to confirm, not to rewrite. The local full-stack
   slice (anything crossing frontend to backend, or service to data store, within this
   feature) is the most common genuine gap at close-out.

2. **Decide which category the feature as a whole belongs to.** When it spans several, name
   the primary and the secondary, and state briefly what the classification rests on.

3. **If the cross-module contract category is enabled, check the contracts.** For every
   contract this feature *exposes* or *changes*, find its consumers in the dependency graph.
   Each changed contract needs a contract check on the producer side plus one regression per
   consumer. Where there is no contract declaration to read, say "insufficient information
   — no contract declaration found".

4. **Walk the dependency graph for full functional chains.** This step is what carries the
   skill's value. Follow the dependency edges and find any path that has become fully
   connected **across the feature boundary, spanning several features**, *because this
   feature just landed*. A newly closed A->B->C path is an end-to-end candidate no single
   task list could reveal — and it is exactly where `full-chain-testing-en` starts its path
   excavation. Name it; route it to `full-chain-testing-en` (which then grades criticality
   and takes only a small handful of P0s as a safety net); mark it as needing human scope
   judgement, unless a CI end-to-end gate already exists.

5. **Route to the executor skill by category.** Look up that category's capability gaps and
   routing destination in `tool-mapping.md`, and carry the status honestly (executor built /
   placeholder to be built). **Do not hardcode a single-stack tool in this skill** — route
   backend-only to `backend-testing-en`, which resolves the concrete tools by reading the
   project manifest (`package.json` / `pyproject.toml` / `go.mod` and so on); route the
   other categories to their category skill.

## Graceful degradation

- No scope labels: infer the category from the task text, and note that it was inferred.
- No dependency graph: you can still classify backend-only / frontend-only / local
  full-stack slice; mark full functional chain (and the cross-module contract candidate)
  as "insufficient information (dependency graph unavailable)".
- No contract declarations: do not enable the cross-module contract candidate, or mark it
  "insufficient information"; suggest the team document their contracts so future routing
  can work.
- No acceptance criteria: full functional chain can still flag that a chain is
  *structurally* complete, while noting the specific journey steps are not yet specified.

Never throw an error over a missing signal. **A partial report carrying honest
"insufficient information" markers is the correct output.**
