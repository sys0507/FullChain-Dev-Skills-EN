---
name: speckit-feature-pipeline-en
description: >-
  Split a project-level PRD into features and take each through all four steps: spec.md, clarify
  write-back, plan.md and tasks.md. Produce documents only—no code, worktree changes or TDD.
  Includes the split-order table, four-step output contracts, clarify's four boundary classes,
  plan's five-element check, and 12–18-task granularity control. Triggers: split features / turn
  the PRD into specs / generate spec plan tasks / four-step documents / feature split table /
  specify clarify plan tasks / break requirements into tasks / write feature documents. Do not
  use to implement a feature (implementation executor), write the PRD (PRD writing Skill), converge
  MVP scope, or rerun plan/tasks after a design-system change (design injection Skill). Invoke
  whenever the task involves turning requirements into executable feature documents, even if the
  user does not mention a Skill.
license: MIT
allowed-tools: Read Write Edit Bash
metadata:
  version: "1.0"
  lang: en
  stage: "4"
  standalone: true
  produces:
    - "specs/00X-<slug>/spec.md"
    - "specs/00X-<slug>/plan.md"
    - "specs/00X-<slug>/tasks.md"
  requires:
    - name: "specs/prd.md"
      level: orchestration
      fallback: "Ask the user to describe the requirement directly or paste the PRD content; do not refuse to work for want of a file"
    - name: "spec toolchain"
      level: optional
      fallback: "Produce the built-in equivalent four-step outputs, labelled 'no external toolchain used'"
    - name: "existing feature directories"
      level: optional
      fallback: "Start numbering at 001 where there are none"
---

# Feature Document Pipeline

## The boundary (what it does not do, stated first)

This skill **produces documents only**:

- It writes no code
- It creates and switches no worktree or branch
- It runs no TDD

When it finishes, the codebase MUST show **zero changes** apart from new documents under
`specs/`.
These four are the dividing line against the implementation executor, not a footnote.

## The flow

```
1. Read the PRD; select the Must-haves
2. Estimate each one's task count; split any estimated above 18 first
3. Emit the five-column split table with a dependency ordering, saved to `specs/feature-split-table.md`
4. Take each feature through the four steps in order
   specify -> clarify (mandatory) -> plan (five-element check) -> tasks (granularity check)
5. Pause or continue according to the rhythm
6. Report: feature count / task count each / any deviations / pending items
```

## The split table (five columns)

| # | Feature name | Which PRD section it comes from | Which features it depends on | Document output directory |
|---|---|---|---|---|

The directory format is **strictly** `specs/00X-<feature-slug>/`, with a three-digit number
and a kebab-case slug.

**Split only the Must-haves.** Where a Should item is depended on by a downstream acceptance
criterion, **report the dependency but do not include it unilaterally** — whether to include
it is the user's scope decision.

### The split table may be revised

The split table **is not fixed once**. Where any feature's clarify step reveals the split was
wrong (two features are really one, or one needs splitting again), **go back to the table,
correct it, and say why**.

> A real case: this project once folded a documentation output into the quality-gates
> feature, and only discovered the scope confusion (a Should mixed into a Must) while writing
> that feature's spec, at which point it became its own feature.
> Had the table been unrevisable, the error would have travelled all the way into
> implementation.

## The four steps

### 1. specify -> spec.md

**Write only What and Why.**

MUST contain: functional boundary / MVP constraints / runtime environment / business flow /
inputs and outputs / acceptance criteria / boundary conditions.

**MUST NOT contain** framework names, library names, database selection, or specific language
runtime versions — every technical decision defers to plan.

The one-cut test:
> An engineer could satisfy this with a different implementation -> it stays in the spec
> Change the implementation and it is no longer satisfied -> that is a technical decision;
> move it to plan

The most common mistake is not "wrote technology" but **wrote technology and omitted the
boundary**. "Use streaming parsing for large volumes" is How; "for a single file of N lines
or more, produce a result or an explicit refusal within M seconds" is What.

See `references/step-contracts.md` for each step's required and forbidden contents.

### 2. clarify -> write back into spec.md (mandatory)

**This step MUST NOT be skipped. Under any circumstances.**

What deserves the most suspicion is not "the requirement is vague" but "the requirement looks
perfectly clear" — a detailed PRD usually leaves gaps on what is not being built, what
happens on failure, and extreme scale.

**Scan all four boundary classes, at least one question each**:

| Class | What to scan |
|---|---|
| MVP boundary | What is explicitly not being built? **Are the priority labels consistent with the delivery scope?** |
| Interface boundary | Rate limits, failures, timeouts, quotas |
| Data boundary | Nulls, anomalous values, extreme scale |
| Integration boundary | Assumptions about interacting with existing systems |

Every question MUST be **traced to a specific passage of spec.md**, and its write-back
location recorded.
There is no such thing as "this feature needs no clarification" as a whole-step skip.

See `references/clarify-4-boundaries.md` for the question bank per class and the traceable
write-back rules.

### 3. plan -> plan.md (five elements; missing one means rework)

| # | Element |
|:-:|---|
| 1 | Project file structure (paths plus each file's core responsibility) |
| 2 | Data flow (as a diagram) |
| 3 | Dependency list (versions/ranges/levels) |
| 4 | Integration points with existing systems (**state explicitly what is reused and what is new**) |
| 5 | Risk list (risk plus mitigation) |

**Missing any one means rework; do not proceed to tasks.**
The two most often missing are 4 and 5 — they carry no immediate output pressure and are the
easiest to skip, and they are precisely the two that prevent reinventing wheels and prevent
blowups.

**Reuse first**: where an existing asset can be reused, do not build a new one.

See `references/plan-5-elements.md` for how each element is judged, with counter-examples.

### 4. tasks -> tasks.md (12-18 items)

Every task MUST satisfy:

1. **Single responsibility** — one task does one thing
2. **Independently testable** — its inputs and outputs are explicit
3. **Completable within one context-bounded implementation cycle**

Each is labelled with its FR source, its task dependencies and its output verification
method, and marked with a **parallel group**.

**Size rules**:

| Situation | Handling |
|---|---|
| More than 18 | **First judge whether it should be several features**, rather than accepting an overlong list |
| 17 or more | Explicitly evaluate whether to split and **record the conclusion** (even when the conclusion is not to) |
| Fewer than 12 | Allowed, but you MUST **show they remain independently testable** |

**MUST NOT pad to reach a number.** Not reaching twelve means the feature is small; write it
clearly and move on.

See `references/task-granularity.md` for the granularity rules, the three-label format and
parallel group marking.

## Hard constraints

1. The specify step **never** makes technology choices
2. clarify is **mandatory** and MUST NOT be skipped
3. plan missing any of the five elements means rework
4. Deviating from 12-18 tasks MUST be justified
5. The directory is strictly `specs/00X-<feature-slug>/`
6. The codebase shows zero changes when the run ends

## What to do when something goes wrong

| Situation | Handling |
|---|---|
| The PRD lacks acceptance criteria, boundaries or data samples | **Stop and ask the user; do not invent them** |
| The user is unsure about a clarify question too | Record it as an open question; do not decide for them |
| An integration point is unclear | Stop and ask the user for the existing system's path or documentation; **do not guess** |
| Circular dependency between features | Stop, report the cycle and ask for adjudication; do not break it yourself |
| The PRD contradicts itself | Report the contradiction and ask for adjudication; **do not silently pick a side** |
| A feature directory of the same name exists | Do not overwrite; report the conflict and ask whether this is a continuation or a new number |

## Toolchain adaptation

**Detect first, then use; on detection failure switch to built-in, do not force it.**

| Situation | Approach |
|---|---|
| A spec toolchain is available | Call its four-step commands |
| Unavailable | Produce the built-in equivalent four-step outputs, **labelled "no external toolchain used"** |

See `references/toolchain-adapters.md` for the detection mechanism and the three ways it can
land.

## Upstream Artifacts

| Artifact | Level | When missing |
|---|:---:|---|
| `specs/prd.md` | orchestration | Ask the user to provide or paste the requirement content |
| Spec toolchain | optional | Built-in equivalent outputs, labelled |
| Existing feature directories | optional | Start numbering at 001 |

## Downstream Consumers

| Consumer | What it reads |
|---|---|
| The implementation runway setup skill | The `specs/00X-*/` directory structure |
| The implementation executor | `spec.md`, `plan.md`, `tasks.md` |
| The design injection skill | `plan.md` and `tasks.md` (rerun on a design change) |

## Standalone Use

**What you provide**: a description of the requirement — pasted or spoken is fine.
No `specs/prd.md` is needed, and no spec toolchain is needed.

**What you get**: the complete split table and three documents per feature, with the four-step
contracts, the four-class boundary scan, the five-element check and the granularity control
all in force — those rules are built into this skill and depend on no external tool.

**What you don't get**:

- **It implements nothing.** The output is documents; writing code needs the implementation
  executor.
- **It does not write your PRD.** If you give a single sentence rather than a formed
  requirement, I will still split out features, but the completeness of the What and Why
  depends on how much you provided.
- **With no external toolchain**, the command-level integration of the four steps is
  unavailable; the built-in equivalents produce the same structure but trigger none of that
  toolchain's other integrations.

## Anti-patterns

- "The requirement is already clear" -> skipping clarify
- Naming frameworks, libraries or a database in the spec
- Writing the implementation approach while omitting the boundary conditions
- Exceeding 18 tasks with no explanation and no evaluation of splitting the feature
- Padding to reach twelve
- Tasks at a granularity like "implement the permissions system", which cannot be tested alone
- Calling toolchain commands without detecting first, then trial-and-erroring after a failure
- Fixing the split table once and refusing to revise it when the split proves wrong
- Silently picking a side when upstream contradicts itself
