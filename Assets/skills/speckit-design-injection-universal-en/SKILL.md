---
name: speckit-design-injection-universal-en
description: Inject DESIGN.md and visual reference artefacts into a Spec-Kit project that has already completed specify, clarify, plan, and tasks, then update the affected plan/tasks through constitution rules, impact scanning, and targeted reruns. Use for the later integration of Stitch, Figma, Claude Design, HTML prototypes, or a hand-written design system. Do not use for a new project, a project with no design artefacts, a backend-only project, or a minor change to a few tokens.
metadata:
  version: "1.0"
  lang: en
  stage: "5.2"
  standalone: true
  produces:
    - ".specify/memory/constitution.md"
    - "specs/00X-*/plan.md"
    - "specs/00X-*/tasks.md"
  requires:
    - name: "DESIGN.md or an equivalent design source of truth"
      level: required
    - name: "visual and interaction reference sample directory"
      level: orchestration
      fallback: "Inject from DESIGN.md alone and mark sample-related constraints as not covered"
    - name: "feature directories that have completed specify and clarify"
      level: orchestration
      fallback: "Ask the user which features to rerun; with none, perform only the constitution injection"
    - name: "specification toolchain"
      level: optional
      fallback: "Use the equivalent plan/tasks rewrite flow"
---

# Spec-Kit Design System Injection (Universal English Version)

## Language Convention

- This Skill is the English execution version: interaction with the user, check reports,
  Open Questions, and newly generated explanatory documents use English by default.
- Code, commands, file paths, APIs, component names, design tokens, and existing project
  identifiers remain in their original form.
- `references/prompts.md` contains the English examples used by this version.
- Chinese source material is used only as methodological input and must not switch output to
  Chinese. A Chinese-only workflow must call `speckit-design-injection-universal`; the two
  versions must not be mixed in the same workflow.

## Goal and Boundaries

This Skill integrates a design system created later into a project that has already completed
the Spec-Kit documentation flow, without discarding existing business specifications or
architecture decisions. The correct method is: **constitution injection + impact
identification + selective rerun**.

Do not use it in these situations:

- A new project that has not run Spec-Kit: put `DESIGN.md` in the project root first, then run
  Spec-Kit normally.
- No design artefact exists yet: this Skill injects a design; it does not create one.
- A backend-only project: there is no interface design system to inject.
- Only one or two colours or tokens change: update `DESIGN.md` directly.

## Pre-flight Check

Confirm before starting:

| Requirement | What to check |
|---|---|
| Spec-Kit is initialised | `.specify/` exists in the project root |
| At least one feature has a plan and tasks | `specs/00X-*/plan.md` and `tasks.md` exist |
| A design artefact exists | One of DESIGN.md, a Stitch/Figma export, Claude Design, HTML, or an image prototype |
| The project root is clear | It resolves to a concrete absolute path |

If any requirement is missing, pause and ask the user. Do not guess or fabricate it.

## Four-step Workflow

```text
Step 1: Place materials       → put design artefacts in stable, referenceable locations
Step 2: Inject constitution   → write abstract design principles into constitution.md
Step 3: Identify impact       → find the features that genuinely touch UI
Step 4: Selectively rerun     → rerun plan + tasks only for affected features
```

Hard boundary: do not modify `spec.md` or the specification after clarify. Adding a design
system does not change business requirements.

### Step 1: Place Materials

Target structure:

```text
<project-root>/
├── DESIGN.md
├── design-reference/
│   └── <source>-export/
│       ├── <page-1>/
│       │   ├── code.html
│       │   └── screen.png
│       └── ...
└── .specify/memory/constitution.md
```

Execution requirements:

1. Read `references/design-source-adapters.md` for the design source and select its mapping
   rules.
2. Rename page directories with semantic names corresponding to features under `specs/`, for
   example `_7` → `cart-en`.
3. If `DESIGN.md` already exists in the project root, compare it and wait for user confirmation;
   do not overwrite it.
4. If `design-reference/` already exists, present a merge proposal and wait for confirmation.
5. If the design artefact includes a duplicate `prd.md`, do not copy it; report differences
   when the contents do not agree.
6. Use the current platform's native non-destructive copy operation. Before recursively
   copying, resolve and verify the absolute source and destination paths. Retain the source as
   a backup; do not move the source directory.

### Step 2: Inject the Constitution

Goal: write stable design direction into `.specify/memory/constitution.md` so later
`/speckit.plan` and `/speckit.tasks` runs inherit it automatically.

Core rule: **the constitution stores direction; DESIGN.md stores concrete values.**

- Allowed: the sole source of visual specifications is root `DESIGN.md`; colours, type sizes,
  and spacing must use what it defines.
- Not allowed: concrete hex values, token names, font names, or component names.

Read before execution:

- Root `DESIGN.md`
- `specs/prd.md`
- Two or three representative pages under `design-reference/<source>-export/`

Append a “Frontend Design System” section. Write each principle as: principle name → why it
cannot be violated → source-of-truth file. Cover at least: source of visual specifications,
how samples are referenced, target user/market conventions, component-library baseline,
information density, multilingual strategy (if applicable), and light/dark theme (if
applicable). Put anything the material does not clearly specify into Open Questions; do not
decide for the user.

Show the diff before writing. After writing, report the changed files and the source paragraph
for each principle.

### Step 3: Identify Impact

Scan every feature's `plan.md` and `tasks.md` under `specs/`, and output:

| Feature directory | Touches UI? | Rerun plan/tasks? | Matching reference page | Basis |
|---|---|---|---|---|

- Interface work such as React/Vue components, pages, forms, tables, charts, and dashboards:
  rerun.
- Pure backend, algorithm, scheduling, or database work: do not modify.
- No matching design page: mark it as a gap; do not design it unilaterally.

After outputting the list, pause and wait for the user to confirm the rerun scope.

### Step 4: Selectively Rerun

Handle one confirmed feature at a time:

1. Run only `/speckit.plan` and `/speckit.tasks`; do not run `/specify` or `/clarify`.
2. Before plan, read root `DESIGN.md` and the matching reference page.
3. In plan's frontend section, list the components, matching DESIGN.md sections, and reference
   sample paths.
4. Preserve all existing backend, data-flow, integration, dependency, and risk content.
5. Retain the project's existing task-label system; use `[FE]`, `[BE]`, and `[INT]` only when
   no labels exist.
6. Each `[FE]` task must cite the DESIGN.md section, HTML/image sample path, and component used.
7. Re-evaluate parallel groups from actual dependencies; do not presume frontend and backend
   can always run in parallel.
8. Pause after each feature and let the user review it before continuing.

## Anti-patterns

| Anti-pattern | Correct approach |
|---|---|
| Copy hex values and tokens into the constitution | The constitution only references DESIGN.md as the source of truth |
| Rerun specify after adding design | Business requirements did not change; rerun only plan + tasks |
| Rerun every feature without separating frontend and backend | Identify impact first; update only UI features |
| Decide unclear design direction independently | List an Open Question and wait for user confirmation |
| Copy all of DESIGN.md into every plan | Enforce it through the constitution and reference it from plan |
| Skip the constitution and rerun directly | Establish consistent constraints first so features do not interpret them differently |

## Completion Criteria

- `DESIGN.md` is in the project root.
- `design-reference/<source>-export/` uses semantic page directories.
- The constitution contains only abstract design principles, not concrete token values.
- Only UI-related features have updated plan/tasks.
- Backend-only features remain unchanged.
- All newly added explanatory content and reports use English.

## References

- `references/design-source-adapters.md`: placement mappings for different design sources.
- `references/prompts.md`: copyable prompts for the four-step flow; this English version uses
  only the English blocks.
- `references/examples.md`: complete cases across project types.

Read a reference only when its source-specific details, prompt, or complete case is needed. Do
not load all references at once.

## First Response

Explain in English first: there is no need to redo spec/clarify; only plan/tasks for
frontend-related features are updated, and the Spec-Kit constitution enforces the design system
across the project. Then follow the four-step workflow, with confirmation gates before
overwriting materials, writing the constitution, accepting the impact list, and after rerunning
each feature.


## Upstream Artifacts

| Artifact | Level | When missing |
|---|:---:|---|
| `DESIGN.md` or an equivalent design source of truth | **required** | Stop — without design material, this Skill has no input |
| Visual and interaction reference sample directory | orchestration | Inject from DESIGN.md alone; mark sample-related constraints as not covered |
| Feature directories that completed specify and clarify | orchestration | Ask the user to specify them; with none, perform only the constitution injection |
| Specification toolchain | optional | Use the equivalent rewrite flow |

## Downstream Consumers

| Consumer | What it reads |
|---|---|
| Implementation executor | Design principles in the constitution and the rerun plan/tasks |

## Standalone Use

**What you provide**: a DESIGN.md or equivalent design source of truth. A reference sample
directory is helpful.

**What you get**: a new design-principles section in the constitution and a targeted rerun of
plan/tasks for the affected features.

**What you don't get**:

- **Design material is required** — it is the sole required dependency; without it this Skill
  has no input.
- **It does not modify spec or clarify artefacts**; it changes only plan and tasks.
- It does not produce the design itself; DESIGN.md comes from the design stage.

**Gate**: output the affected-feature list and wait for user confirmation, then rerun features
one at a time; stop after each for review.
