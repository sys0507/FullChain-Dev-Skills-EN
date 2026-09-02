---
name: platform-design-kickoff-en
description: >-
  Produce the design source of truth before implementation — decide whether this project
  needs interface design at all, choose a design tool that fits the target platform, and
  produce DESIGN.md (design system + tokens + component specs) plus a design reference
  export directory. Stays strictly inside the PRD's Must-have scope; breakpoints, theming,
  accessibility and internationalisation left undefined by the PRD go into Open Questions
  rather than being decided on the user's behalf.
  Trigger keywords: interface design / experience design / UI design / design system /
  DESIGN.md / design tokens / component spec / visual spec / prototype / interaction
  contract / stage 5 / 5.1.
  Do not use for: injecting a design system into the constitution or rewriting specs
  (that is speckit-design-injection-universal-en), writing frontend code, operating a
  design tool on the user's behalf, choosing a component library, or manufacturing an
  interface for a backend-only or non-interactive project.
  Invoke it whenever the task concerns what this project's interface should look like,
  even if the user never says the word "skill".
license: MIT
metadata:
  version: "1.0"
  lang: en
  kind: behavioural
  stage: "5.1"
  standalone: true
  produces:
    - "DESIGN.md"
    - "design-reference/<source>-export/"
  requires:
    - name: "specs/prd.md"
      level: required
      fallback: "Ask the user directly for the target platform and the Must-have list; label the output 'PRD not read, Must-have boundary not cross-checked'"
    - name: "specs/research/05-decision-summary.md"
      level: optional
      fallback: "Report the skip reason in the session instead, and state that it was not written to the decision summary"
    - name: "external design tool"
      level: optional
      fallback: "Still produce DESIGN.md (tokens + component specs); label it 'no design tool used, design-reference/ empty, visual detail unverified against any reference'"
    - name: "speckit-design-injection-universal-en"
      level: orchestration
      fallback: "Output remains complete; tell the user stage 5.2 needs handling separately"
---

# Platform Design Kickoff (Stage 5.1)

## What this skill is guarding against

**Design is where an agent most easily exceeds its scope.** Handed a PRD, it adds the
login page the PRD never mentioned, picks a component library, throws in dark mode.
Each step looks reasonable. Together they are a scope nobody approved.

The value here is not knowing how to draw. It is pinning the boundary before drawing.

## Step 1: does this apply

**Three criteria. Any one of them makes this stage apply; only all three failing skips it.**

| # | Criterion |
|:-:|---|
| 1 | There is a **graphical interface** for end users (web / mobile / desktop / hardware panel) |
| 2 | There is an **interaction contract** worth designing (a multi-step CLI wizard, say) |
| 3 | There is a stated **developer-experience** need (the feel of an SDK's API) |

**"No GUI" does not imply "does not apply."** The criterion is the interaction contract,
not pixels.

When it does not apply: **record the reason** in
`specs/research/05-decision-summary.md`, and produce **no design files at all**.
That is a normal exit, not a failure.

## Step 2: platform first, then tool

The order does not reverse. **The platform picks the tool, never the other way round.**

iOS uses size classes, not breakpoints; embedded uses physical dimensions, not rem.
Hand a DESIGN.md full of web breakpoints to a native project and the downstream
frontend tasks read concepts that do not exist on the target.

Once chosen, state **why this one and why not the alternative**.

See `references/platform-tool-matrix.md` for six platform families, their tools and
export formats.

## Step 3: four interceptions

| # | What it catches | The correct move |
|:-:|---|---|
| 1 | **Adding features** | Write it into Open Questions; do not draw it |
| 2 | **Deciding undefined items** | Breakpoints / theming / accessibility / i18n — ask about all four |
| 3 | **Adopting a component library** | Recommend + justify + **stop for confirmation**, all three |
| 4 | **Tool lock-in** | See step 2 |

### The line that is easy to overshoot

| Scope creep | Not scope creep |
|---|---|
| Adding a **feature** the PRD does not have | Drawing the **states** of a feature already in scope (empty / loading / error / validation) |

Enforce "draw nothing the PRD omits" down to state granularity and the resulting
DESIGN.md is unbuildable. **Plugging a hole must not open a larger one.**

### The reverse: do not ask about what is already defined

Whatever the PRD **has** defined, **adopt without a single question**.
Interrupting at every step turns this skill into noise.
**"Failed to ask" and "asked when it should not have" are two faces of one rule.**

See `references/scope-guardrails.md` for how each constraint is enforced and the
rebuttals to the rationalisations that get past a weaker rule.

## Step 4: output

| Artifact | Location |
|---|---|
| `DESIGN.md` | Project root |
| Design reference exports | `design-reference/<source>-export/`, where `<source>` names the tool actually used |

**Open Questions must be section 0 of `DESIGN.md`, not an appendix.**
Buried at the end it may as well be absent — by the time a reader reaches it they have
already taken everything above as settled.

**Every row of the page list must name the Must-have it serves.** That table is the
scope-creep self-check: a row whose second column cannot be filled is scope creep.

When `DESIGN.md` already exists, **do not overwrite** — show a diff and wait.

See `references/design-md-template.md` for the section skeleton with worked positive
and negative examples.

## Step 5: the gate

**Stop. Wait for the user to confirm `DESIGN.md` is final.**

Then hand off to `speckit-design-injection-universal-en` (stages 5.2–5.3). Injecting
into the constitution, scanning for impact, and rerunning affected features' plans and
tasks **all belong to that skill**. This one touches neither the constitution nor any
spec document.

## Upstream Artifacts

| Artifact | Level | When missing |
|---|:---:|---|
| `specs/prd.md` | **required** | Ask the user for the target platform and Must-have list; label the output "PRD not read" |
| `specs/research/05-decision-summary.md` | optional | Skip reason goes to session output, labelled "not written to the decision summary" |
| External design tool | optional | Still produce `DESIGN.md`, labelled "no reference exports" |
| `speckit-design-injection-universal-en` | orchestration | Output stays complete; note that 5.2 needs separate handling |

## Downstream Consumers

| Consumer | What it takes |
|---|---|
| `speckit-design-injection-universal-en` | `DESIGN.md` + `design-reference/`, to inject into the constitution and rerun specs |
| `claude-md-bootstrap-en` | An `@DESIGN.md` reference |
| `run-feature-en` | Frontend tasks must read `DESIGN.md` before writing tests |

## Standalone Use

**What you provide**: the target platform, and the list of features to design. A PRD
helps; you can start without one.

**What you get**: a `DESIGN.md` — tokens, component specs, page list — plus an Open
Questions section naming every decision still waiting on you.

**What you don't get**: no injection into your constitution and no spec edits (a
different skill owns those); no operating a design tool's GUI for you; no component
library chosen on your behalf, only a recommendation with reasons. Without a PRD the
output carries the label "Must-have boundary not cross-checked" — **density drops,
honesty does not**.
