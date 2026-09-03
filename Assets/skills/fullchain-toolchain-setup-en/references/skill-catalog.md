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
| 1 | `project-context-ledger` | Three-state context ledger | throughout |
| 2 | `product-research-kickoff-universal` | Four-way parallel kickoff research | 1.1-1.2 |
| 3 | `adversarial-architecture-selection-universal` | Adversarial architecture selection | 1.3 |
| 4 | `mvp-convergence-brainstorming` | MVP convergence | 2 |
| 5 | `prd-writer-universal` | The 14-chapter PRD | 3 |
| 6 | `speckit-feature-pipeline` | Feature four-step documents | 4 |
| 7 | `speckit-design-injection-universal` | Design system injection | 5.2-5.3 |
| 8 | `claude-md-bootstrap` | Project context file | 6 |
| 9 | `implementation-runway-setup` | Pre-implementation setup | 7 |
| 10 | `run-feature` | Single-feature TDD implementation | 8 |
| 11 | `testing-system-blueprint` | Testing system blueprint | 9 |
| 12 | `test-routing-advisor` | Test routing decision | 9.1 |
| 13 | `backend-testing` | Backend gap backfill | 9.2 |
| 14 | `frontend-testing` | Frontend gap backfill | 9.2 |
| 15 | `fullstack-slice-testing` | Local seam reconciliation | 9.2 |
| 16 | `full-chain-testing` | Cross-feature end-to-end | 9.2 |
| 17 | `learnings-retrospective` | Lessons retrospective | 10 |

## The English catalogue (en)

| # | Directory |
|:-:|---|
| 1 | `project-context-ledger-en` |
| 2 | `product-research-kickoff-universal-en` |
| 3 | `adversarial-architecture-selection-universal-en` |
| 4 | `mvp-convergence-brainstorming-en` |
| 5 | `prd-writer-universal-en` |
| 6 | `speckit-feature-pipeline-en` |
| 7 | `speckit-design-injection-universal-en` |
| 8 | `claude-md-bootstrap-en` |
| 9 | `implementation-runway-setup-en` |
| 10 | `run-feature-en` |
| 11 | `testing-system-blueprint-en` |
| 12 | `test-routing-advisor-en` |
| 13 | `backend-testing-en` |
| 14 | `frontend-testing-en` |
| 15 | `fullstack-slice-testing-en` |
| 16 | `full-chain-testing-en` |
| 17 | `learnings-retrospective-en` |

> **The orchestrator has no English counterpart yet.** The project's own rule is
> Chinese-first: a new skill must be stable and have run against a real project before its
> English version is made, and the orchestrator has not yet met that bar.
> When the en catalogue is requested, any missing entry is **reported as a failure and
> recorded** under hard language isolation, and **the Chinese version is never substituted**.

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
