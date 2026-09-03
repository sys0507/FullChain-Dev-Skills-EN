# The skill catalogues (two independent language tables)

## When to read this

When taking the catalogue before installing.

---

## Why two tables rather than one concatenation rule

The twelve existing logical skills have **inconsistent naming suffixes**:

| Logical skill | Chinese directory | English directory |
|---|---|---|
| The first four | `<name>-universal` | `<name>-universal-en` |
| The other eight | `<name>` | `<name>-en` |

Deriving the English name by concatenating "Chinese name + `-en`" **produces the wrong name
for the first four** — it either yields something other than `<name>-universal-en`, or gets
the eight right while getting the four wrong.

**Two independent tables are the direct response to that inconsistency**, not redundancy.
They are also a direct consequence of the constraint not to rename the existing skills — a
suffix inconsistency cannot be removed by renaming, so it has to be enumerated.

> **Deriving names by concatenation is forbidden, in code and in process.** Look them up.

---

## The Chinese catalogue (zh)

| # | Directory | Purpose | Stage called |
|:-:|---|---|:---:|
| 1 | `fullchain-dev-workflow` | Full-chain orchestration | 0-11 |
| 2 | `project-context-ledger` | Three-state context ledger | throughout |
| 3 | `product-research-kickoff-universal` | Four-way parallel kickoff research | 1.1-1.2 |
| 4 | `adversarial-architecture-selection-universal` | Adversarial architecture selection | 1.3 |
| 5 | `mvp-convergence-brainstorming` | MVP convergence | 2 |
| 6 | `prd-writer-universal` | The 14-chapter PRD | 3 |
| 7 | `speckit-feature-pipeline` | Feature four-step documents | 4 |
| 8 | `platform-design-kickoff` | Platform design kickoff | 5.1 |
| 9 | `speckit-design-injection-universal` | Design system injection | 5.2-5.3 |
| 10 | `claude-md-bootstrap` | Project context file | 6 |
| 11 | `implementation-runway-setup` | Pre-implementation setup | 7 |
| 12 | `run-feature` | Single-feature TDD implementation | 8 |
| 13 | `testing-system-blueprint` | Testing system blueprint | 9 |
| 14 | `test-routing-advisor` | Test routing decision | 9.1 |
| 15 | `backend-testing` | Backend gap backfill | 9.2 |
| 16 | `frontend-testing` | Frontend gap backfill | 9.2 |
| 17 | `fullstack-slice-testing` | Local seam reconciliation | 9.2 |
| 18 | `full-chain-testing` | Cross-feature end-to-end | 9.2 |
| 19 | `learnings-retrospective` | Lessons retrospective | 10 |
| 20 | `release-packaging-router` | Release packaging router | 11 |

## The English catalogue (en)

| # | Directory |
|:-:|---|
| 1 | `fullchain-dev-workflow-en` |
| 2 | `project-context-ledger-en` |
| 3 | `product-research-kickoff-universal-en` |
| 4 | `adversarial-architecture-selection-universal-en` |
| 5 | `mvp-convergence-brainstorming-en` |
| 6 | `prd-writer-universal-en` |
| 7 | `speckit-feature-pipeline-en` |
| 8 | `platform-design-kickoff-en` |
| 9 | `speckit-design-injection-universal-en` |
| 10 | `claude-md-bootstrap-en` |
| 11 | `implementation-runway-setup-en` |
| 12 | `run-feature-en` |
| 13 | `testing-system-blueprint-en` |
| 14 | `test-routing-advisor-en` |
| 15 | `backend-testing-en` |
| 16 | `frontend-testing-en` |
| 17 | `fullstack-slice-testing-en` |
| 18 | `full-chain-testing-en` |
| 19 | `learnings-retrospective-en` |
| 20 | `release-packaging-router-en` |

---

## The source directory

Passed in by the caller as a **parameter** (the script's `--source`).

**No concrete path may be hardcoded** — including writing a "default" here as an example.
Where a user keeps their assets is their business, and pinning a location makes people
believe it is a requirement.

This document deliberately gives no example path, precisely so that an example does not
become a de facto convention.

## Install location

Project-scoped: `<project>/.claude/skills/<directory>/`.

**Never install globally, and never modify another project.**

---

## Subset installs

A user may install only some of them. In that case:

1. Install exactly what was named
2. **Report the impact of what was not installed** — which stages will lack a capability

MUST NOT refuse a subset for being "incomplete".
Wanting only two skills is an entirely legitimate use.
