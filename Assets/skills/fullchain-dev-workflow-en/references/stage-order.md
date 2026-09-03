# Built-in Stage Order

> **This table is the fallback when `docs/stage-artifact-contract.md` is missing.**
> The contract matrix is the single source of truth; **the matrix wins on conflict**, and this table must be reported for correction.
> Whenever this fallback is used, label the output: “Contract matrix not read; paths and gates were not cross-validated.”

## When to Read

Read only when the contract matrix cannot be found. **If the matrix is readable, do not read this table.**

## 17 Execution Points

| Stage | Name | Invoke | Gate | Conditional |
|:---:|---|---|:---:|:---:|
| 0 | Toolchain setup | `fullchain-toolchain-setup-en` | None | |
| 1.1 | Project ledger | `project-context-ledger-en` | Conditional trigger | |
| 1.2 | Project research | `product-research-kickoff-universal-en` | End of stage | |
| **1.3** | Adversarial selection | `adversarial-architecture-selection-universal-en` | End of stage | Yes |
| 2 | MVP convergence | `mvp-convergence-brainstorming-en` | End of stage | |
| 3 | Write PRD | `prd-writer-universal-en` | End of stage | |
| 4 | Four-step documents | `speckit-feature-pipeline-en` | Each feature | |
| **5.1** | Interface design | `platform-design-kickoff-en` | End of stage | Yes |
| **5.2** | Design injection | `speckit-design-injection-universal-en` | Each feature | Yes |
| 6 | Project context | `claude-md-bootstrap-en` | End of stage | |
| 7 | Runway setup | `implementation-runway-setup-en` | End of stage | |
| 8 | TDD implementation | `run-feature-en` | Each feature | |
| 9.1 | Test routing | `test-routing-advisor-en` | None | |
| 9.2 | Execute tests | Routed by 9.1 to one of four executors | End of stage | |
| 9.3 | Finish Branch | `run-feature-en` | Each feature | |
| 10 | Retrospective | `learnings-retrospective-en` | None | |
| **11** | Packaging/deployment | `release-packaging-router-en` | End of stage | Yes |

**`testing-system-blueprint-en` is not an execution point.** It is a blueprint referenced by name by stage 9.2 executors.

## Criteria for the Four Conditional Stages

| Stage | Run if and only if | When not run, MUST |
|:---:|---|---|
| **1.3** | Research converges with **at least two candidates** | Record “fewer than two candidates; nothing to compare” and the exclusion basis |
| **5.1** | There is a graphical interface, **or** an interaction contract, **or** a developer-experience design need | Record a conclusion for each of the three criteria |
| **5.2** | Stage 5.1 produced `DESIGN.md` | If 5.1 was skipped, this stage is automatically not applicable |
| **11** | The artifact **must be handed to someone else** or consumed by another project | Record “self-consumed only; distribution unnecessary” |

**These criteria are executable, not “as appropriate.”** Each yields yes or no. If a conclusion cannot be
given, information is missing—ask the user instead of deciding alone.

## How the Orchestrator Uses This Table

| What the orchestrator needs | What this table supplies |
|---|---|
| Whom to invoke next | Third column |
| Whether to stop | Fourth column |
| Whether to run | Criteria table |
| **How to perform each step** | **This table neither supplies nor should supply it** |

The last row is this table's boundary. **Each stage Skill owns how to work.** Writing those instructions here
would create a second source of truth.

Read `gate-protocol.md` for how to stop, what to say, and how to resume.
