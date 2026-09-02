---
name: run-feature-en
description: Implement one ready Spec-Kit feature directory containing spec.md, plan.md, and tasks.md through worktree isolation, project-rule loading, task-by-task TDD, label-aware execution, structured review, and merge/tag handoff. Use when starting or continuing a single prepared feature. Project-specific stack, design, naming, and constitution rules are read at runtime. Do not use for project bootstrap, writing specs, or concurrent multi-feature execution.
---

# run-feature-en · Single Feature Implementation Standard Process (General)

When invoked, implements **one** feature (default convention directory `specs/<id>-<name>/`, containing spec/plan/tasks).
The target feature comes from the call argument (e.g., `/run-feature-en 001` or `/run-feature-en 003-push-channels`).
**Run only one feature at a time**; stop after completion and wait for user review.

> This skill defines only the **process skeleton**. All project-specific values — tech stack, constitution/principle clauses, design system, what the initialization phase is called — are **read from the project's own files**, not hardcoded here. Steps marked "if present" below are skipped if the project doesn't have them.

## Step 0 · Pre-flight checks (stop and ask if not satisfied — don't force ahead)

- **Infrastructure ready**: The project's dependency/build file exists and the test framework can run (per project tech stack, e.g., `package.json` / `pyproject.toml` / `go.mod` / `Cargo.toml` etc.).
  If not yet initialized, complete the project's initialization phase first (**whatever it is called: M1 / Phase 0 / bootstrap / setup**); **do not** apply this process to that step.
- **Upstream dependencies ready**: Other features that the target feature depends on have been completed (see that feature's progress record and the spec's dependency section).

## Step 1 · Worktree isolation

Use the current tool's isolated worktree or branch mechanism. Claude Code example:

```
claude --worktree feat-<id>-<feature>
```
If the project uses `.worktreeinclude` (or equivalent mechanism) to declare local credentials/environment files to bring into the worktree, they will be auto-copied; otherwise ignored.

## Step 2 · Four startup actions

① **Read the project constitution/conventions** (if present, common path: `.specify/memory/constitution.md`): read through and comply with **all** its principles — these are the project's non-negotiable baselines (visual, business, naming, etc.). This skill does not pre-define clause numbers or content.
② Open `specs/<id>-<feature>/tasks.md`, pick the uncompleted task with the minimum dependencies.
③ Use `superpowers:test-driven-development` for each task (RED → GREEN → REFACTOR).
④ After each task completes: update the project's progress record (if present, e.g., `state.md`) → commit → **automatically continue to the next task**; only STOP after all tasks are green, then wait for user review.

## Step 3 · Execute by task tags

The tag on each task in tasks.md determines the approach. Common tags: `[BE]` backend / `[FE]` frontend / `[INT]` integration; if the project uses a different tagging system, map according to its conventions.

**[FE] (Frontend)**
- Before writing tests, read the **project's design system/visual conventions** (if present, e.g., `DESIGN.md` + design reference sample directory), as well as the visual alignment section in that feature's plan (if present).
- Implement using **the component library/technology specified by the project**; reconstruct against the design reference, do not copy line-by-line.
- Before completion, go through the **project's frontend spec checklist** item by item (if present).

**[BE] (Backend)**
- Write test stubs per the plan's contract spec (e.g., API contract OpenAPI / JSON Schema); ignore if not applicable.
- Output validation uses the "output validation" column for that task in tasks.md + the input/output definitions in spec.

**[INT] (Integration)** — route by sub-type; **do not** treat all as "run last":
- Infrastructure type (config / migration / cross-feature contract / documentation): sort normally by the tasks.md dependency graph, **usually runs first**, does not depend on [FE]/[BE].
- E2E type: run real end-to-end (no mocks) after all [FE]/[BE] for this feature have passed.
- Cross-feature patch type (modifying source code of other features): after changes, **must re-run the existing tests of the modified feature**; only passes when green.

## Step 4 · Code review

After all tasks are green, use `superpowers:requesting-code-review`, scanning to cover at least:
① Resilience: missing retry / timeout / circuit breaker
② Cross-cutting consistency: whether auth / rate limiting / logging covers **all** endpoints
③ Defensive: unhandled null / missing input validation / missing idempotency key
④ DB migration (if involved): rollback script + batch operations
⑤ Project constitution/design system compliance (**only when the feature contains [FE] and the project has a design system**): whether visual values that should use tokens are hardcoded, whether the visual/business rules in the project constitution are violated, whether dependencies the project prohibits are introduced

Use `superpowers:receiving-code-review` to process, output table: `| # | Category | File:Line | Description | Priority |`
0 defects → Step 5; defects found → return to the corresponding task for TDD fix, re-run review, until 0 defects.

## Step 5 · Wrap-up

1. Final commit, message containing `Closes <id>-<feature>`
2. Merge back to main branch
3. Tag (e.g., `v0.1.0-<feature>`, per project tag conventions)
4. Update the feature's session/handoff record (if present, e.g., `session.md`) marking completion
5. **The feature's spec directory is never deleted** (CI seed + context for the next feature)
6. Report: this feature had N tasks / M [FE] / K [BE] / review found X defects, all fixed

## Rhythm rules

- After one feature completes, **stop and wait for review**, then the next.
- **Strictly prohibit multi-agent concurrent** runs across multiple features (features often have dependency topology).
