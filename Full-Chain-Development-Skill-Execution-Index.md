# Full-Chain Development Skill Execution Index

> **This document answers three things only: what this step does, which skill to call, and
> when to stop and wait for a person.**
>
> It **explains no design reasoning**. To learn why a step is designed the way it is, read
> `Full-Chain-Development-Prompt-Template.md` — the lookup guide is in section 6.
>
> Paths and gates are **quoted from** the contract matrix (in the Chinese tree,
> `docs/stage-artifact-contract.md`, section 3.5 for the English path mapping).
> **This index defines no paths.** Where the two disagree, **the matrix wins**, and this file
> is corrected.

## 1. How to use it

**Running the full chain**: start at stage 0 and work down. Call the skill each row names,
and stop wherever a gate is marked.

**Using only one or two**: call that skill directly. Every skill supports standalone mode —
when an upstream artifact is missing it asks you for the equivalent, it does not refuse to
work, and it does not require you to create directories first. The "input" column is a
**convention default**, not a precondition.

**Judging the conditional stages**: see section 5. **A skip MUST be recorded with its
reason**; it MUST NOT be passed over silently.

## 2. Stage table

| Stage | Skill called | Input | Output | Gate |
|---|---|---|---|:---:|
| 0 Toolchain setup | `fullchain-toolchain-setup-en` | Language parameter + asset source | `.claude/skills/<name>/` | none |
| 1.1 Project ledger | `project-context-ledger-en` | Your project idea | `specs/research/00-project-input-and-assumptions.md` | conditional |
| 1.2 Kickoff research | `product-research-kickoff-universal-en` | `00-project-input-and-assumptions.md` | `specs/research/01-` to `05-*.md` | **stage end** |
| 1.3 Adversarial selection | `adversarial-architecture-selection-universal-en` | `03-open-source-candidates.md`, `04-implementation-options.md` | `06-architecture-baseline.md`, `debate/` | **stage end** |
| 2 MVP convergence | `mvp-convergence-brainstorming-en` | `00`, `05`, `06` | `specs/research/07-mvp-convergence.md` | **stage end** |
| 3 Write the PRD | `prd-writer-universal-en` | `00`, `05`, `06`, `01`-`05` | `specs/prd.md` | **stage end** |
| 4 Four-step documents | `speckit-feature-pipeline-en` | `specs/prd.md` | `specs/00X-<slug>/spec.md`, `plan.md`, `tasks.md` | **per feature** |
| 5.1 Interface design | `platform-design-kickoff-en` | `specs/prd.md` | `DESIGN.md`, `design-reference/<source>-export/` | **stage end** |
| 5.2-5.3 Design injection | `speckit-design-injection-universal-en` | `DESIGN.md`, `prd.md`, `plan.md` | Constitution (append), `plan.md`, `tasks.md` | **per feature** |
| 6 Project context | `claude-md-bootstrap-en` | `prd.md`, constitution, `DESIGN.md`, manifest | `CLAUDE.md` | **stage end** |
| 7 Implementation setup | `implementation-runway-setup-en` | `specs/00X-*/`, constitution | `.worktreeinclude`, credentials inventory, constitution discipline block, `state.md`, `session.md` | **stage end** (partial) |
| 8 TDD implementation | `run-feature-en` | `spec.md`, `plan.md`, `tasks.md`, constitution | Source code, `state.md`, `session.md`, git tag | **per feature** |
| 9.1 Test routing | `test-routing-advisor-en` | The feature's complete output, manifest | `specs/<id>-<feature>/test-routing-decision.md` | none |
| 9.2 Run the tests | `backend-testing-en` / `frontend-testing-en` /<br>`fullstack-slice-testing-en` / `full-chain-testing-en` | Routing decision report, manifest | Test code, evidence archive | **stage end** (human review) |
| 9.3 Finish branch | `run-feature-en` | As stage 8 | merge + tag | **per feature** |
| 10 Lessons retrospective | `learnings-retrospective-en` | Feature process records, `LEARNINGS.md` | `LEARNINGS.md` (prepended), injection signal | none |
| 11 Packaging and release | `release-packaging-router-en` | Project manifest file | `specs/<id>-<slug>/release-channel-decision.md`, packaging feature skeleton | **stage end** |

Stages 1.3, 5.1, 5.2 and 11 are conditional — clear section 5 before deciding to run them.

**`testing-system-blueprint-en` is not in the table**: it is a blueprint, referenced **by
name** by 9.2's four executors, and never executed as a step of its own.

## 3. Gate list

A gate means **genuinely stopping and saying what you are waiting for** — not printing
"please confirm" and continuing.

| Stage | What it is waiting for |
|---|---|
| 1.1 | Stops only when one of three questioning criteria is met. The criteria are in that skill's `references/question-gating.md` |
| 1.2 | Your confirmation that the research conclusions may proceed; candidate values MUST NOT be written as settled requirements without your confirmation |
| 1.3 | Each debate round is adjudicated by the lead agent; it pauses to ask you where the material is insufficient |
| 2 | Your confirmation of the MVP scope and the frozen topics. Once the scope is frozen, reopening it requires an explicit change record |
| 3 | Your confirmation that the PRD is final |
| 4 | Each feature's four steps stop once each; `clarify` MUST NOT be skipped |
| 5.1 | Your confirmation that `DESIGN.md` is final |
| 5.2-5.3 | Stops before injecting, for each feature with an interface |
| 6 | With an existing `CLAUDE.md`, **shows a diff and waits** — never overwrites directly |
| 7 | Stops to tell you when the credentials inventory has items that are not ready; it registers no accounts and creates no credential files |
| 8 / 9.3 | One feature goes green, then **stop and wait for review** before the next |
| 9.2 | Test output counts as complete only after human review |
| 11 | Your confirmation of the release channel |

## 4. Running the whole chain in one command

If you would rather not track the order yourself, use the orchestrator:

| Skill | It knows | It does not know |
|---|---|---|
| `fullchain-dev-workflow` (Chinese tree only) | The order, the gates, the conditional criteria | **How each stage is done** |

It works out which skill is next and whether to stop, recording "where we are, what was
skipped and why" into the chain state file. It supports resuming from any stage.

**How each step is done still comes from that stage's own skill** — the orchestrator does not
restate it, because restating creates a second source of truth.

> **The orchestrator has no English version yet.** The project's own rule is Chinese-first: a
> skill must be stable and have run against a real project before its English version is
> made, and the orchestrator has not yet met that bar. Until it does, drive the English chain
> from this index.

**All eleven stages have a skill.** No row's second column says "no skill yet".
**The only remaining reason to open the frozen template is to look up design reasoning** —
see section 6.

## 5. Deciding whether a conditional stage runs

Each conditional stage has an **executable criterion** — not "it depends".

| Stage | Run it if and only if | When not running, you MUST |
|---|---|---|
| **1.3 Adversarial selection** | Research converged on **two or more candidates** | Record "fewer than two candidates, nothing to argue against" and the basis for the exclusions |
| **5.1 Interface design** | There is a graphical interface, **or** an interaction contract, **or** a developer-experience need | Record all three criteria failing |
| **5.2 Design injection** | Stage 5.1 produced a `DESIGN.md` | Skipping 5.1 makes this automatically not applicable |
| **11 Packaging and release** | The artifact **goes to someone else** or is depended on by another project | Record "only I consume it, no distribution needed" |

Skip reasons go into the skip record section of `specs/research/05-decision-summary.md`.

**A worked example** (a small CLI tool): only self-built remained after research, so 1.3 does
not apply; no interface, so 5 does not apply; a single file, so 11 does not apply. All three
reach a conclusion, and none needs "it depends".

## 6. Looking up the reasoning

To learn **why a step is designed the way it is**, look it up in
`Full-Chain-Development-Prompt-Template.md` — this index points, it does not excerpt.

| Stage | Section | Stage | Section |
|---|---|---|---|
| General execution rules | General execution rules | 6 Context | Stage 6 |
| 0 Toolchain | Stage 0 | 7 Setup | Stage 7 |
| 1 Research | Stage 1 | 8 TDD | Stage 8 |
| 1.3 Adversarial selection | Section 1.3 | 9 Testing and close-out | Stage 9 |
| 2 Convergence | Stage 2 | 10 Retrospective | Stage 10 |
| 3 PRD | Stage 3 | 11 Packaging | Stage 11 |
| 4 Four-step documents | Stage 4 | | |
| 5 Interface design | Stage 5 | | |

> There are two template editions. `Full-Chain-Development-Prompt-Template.md` keeps each
> stage's original full prompt, for reference, explanation and audit;
> `Full-Chain-Development-Prompt-Template-Skills-Edition.md` is the skill-driven execution
> edition. Both are translations of the Chinese frozen baseline, whose content is unchanged.
