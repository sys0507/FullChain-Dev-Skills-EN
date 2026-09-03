# Baseline: how the four-step pipeline goes wrong without this skill

## Method and limitations

Four pressure scenarios run **without the skill loaded**, recording the violations and the
rationalisations that came with them.

**The recorder and the subject are the same agent, so the observer effect applies.** The
tendency is understated.

Compensation: section 5 uses **problems that actually occurred** while producing this
project's `specs/001` through `010` — evidence, not a constructed scenario.

---

## Scenario 1: the requirement looks clear (tempts skipping clarify)

**Input**: a well-written PRD extract with the feature description, inputs and outputs, and
acceptance criteria all present, asking to "split this feature into spec/plan/tasks".

**First output without the skill**:

> The requirement here is already clear, so I will produce the three documents directly:
> spec.md (extracted from the PRD), plan.md, tasks.md...

**Violations**:

| # | Violation | Nature |
|:-:|---|---|
| 1-a | "The requirement is already clear" -> skipped clarify | **The core violation.** clarify's value lies precisely in the case where the requirement looks clear |
| 1-b | Produced three documents directly | Four steps became three; the middle one vanished silently |
| 1-c | No trace of any four-class boundary scan | MVP, interface, data and integration boundaries all unscanned |

**Rationalisation**:

> "The PRD is detailed; nitpicking it wastes time. clarify is for when the requirement is
> vague."

> This rationalisation MUST be rebutted head-on: **clarify is not a remedy for a vague
> requirement; it is the mirror you hold up when a requirement looks clear.**
> A detailed PRD usually leaves gaps on what is not being built, what happens on failure and
> extreme scale — and those gaps detonate during implementation.

---

## Scenario 2: an obvious technical leaning (tempts putting selection into specify)

**Input**: "Build a feature where the user uploads a CSV and charts are generated
automatically. The data volume could be large."

**First spec.md output without the skill**:

> ## Technical approach
> Use streaming parsing for large files to avoid loading everything into memory.
> The frontend renders with a charting library; the backend provides an aggregation endpoint.
> Introduce pagination and caching at large volumes.

**Violations**:

| # | Violation | Nature |
|:-:|---|---|
| 2-a | "Streaming parsing", "pagination and caching" appear in the spec | **Technical decisions written into the What layer**, leaving plan no decision space |
| 2-b | "The frontend renders, the backend aggregates" | Architectural layering is also How |
| 2-c | What should have been written was not: how large is large? What happens above the limit? | The **boundary conditions** that genuinely belong in the spec are missing |

**Rationalisation**:

> "The user said the volume could be large; not mentioning streaming is dodging the problem."

> Rebuttal: **"how it behaves at large volumes" is What; "use streaming parsing" is How.**
> The spec should say "for a single file of N lines or more, the system MUST produce a usable
> result within M seconds or refuse explicitly"; how that is achieved is left to plan.

---

## Scenario 3: the feature is oversized (tempts exceeding 18 tasks)

**Input**: a feature covering user management, permissions and audit logging.

**First output without the skill**:

> tasks.md split into 27 tasks...

**Violations**:

| # | Violation | Nature |
|:-:|---|---|
| 3-a | 27 tasks, far above the ceiling, with no justification | Size out of control |
| 3-b | Never considered whether it should be several features | The correct response to an overrun is **splitting the feature**, not accepting a long list |
| 3-c | Some tasks cannot be tested alone (such as "implement the permissions system") | Single responsibility broken |

**The reverse observation**: given an atomic small feature, it produced only 5 tasks and
**never explained why fewer than 12**. Falling below the floor also needs explaining —
otherwise there is no way to tell "the feature is genuinely small" from "it was not split
finely enough".

---

## Scenario 4: no toolchain (tempts forcing a non-existent command)

**Input**: asked to run the four steps in an environment **with no spec toolchain installed**.

**First output without the skill**:

> Running `/speckit.specify`...
> (the command does not exist; after the error) let me try another spelling...

**Violations**:

| # | Violation | Nature |
|:-:|---|---|
| 4-a | Called without detecting first | Assumed the tool exists |
| 4-b | Trial-and-error after the failure rather than degrading | Should have switched to the built-in equivalent and labelled it |

**Conclusion**: **the forcing tendency does reproduce.**

---

## 5. Problems that actually occurred across this project's ten features

The following are not designed scenarios; they **actually happened** while producing
`specs/001` through `010` with this four-step process.

| # | Real problem | Nature | Requirement on the skill |
|:-:|---|---|---|
| 5-a | **A PRD contradiction went undetected**: section 5.1 marked the thin index as Should, while section 10's MVP deliverables included it. It only surfaced while writing 010's spec | Upstream material contradicted itself, and the four steps did not catch it early | clarify's MVP-boundary class MUST include the question **"are the priority labels consistent with the delivery scope"** |
| 5-b | **The split decision reversed midway**: the thin index was first folded into 009, and only became its own feature while writing 010 | The split table was finalised too early, with no re-check reserved | The split table MUST be revisable **after each feature's clarify**, rather than fixed once |
| 5-c | **009's task count landed exactly on 18** (the ceiling) | Approaching the ceiling triggered no active evaluation of splitting | At 17 or more tasks, the possibility of splitting MUST be evaluated explicitly and the conclusion recorded |

**What they share**: none of the three is "did it wrong". Each is **a missing revision or
self-check point in the four-step process itself**. The skill MUST hard-code those check
points, or they depend on the executor's alertness in the moment.

---

## 6. The violations the skill MUST block

| # | MUST block | Scenario | Corresponding AC |
|:-:|---|:---:|---|
| W1 | Skipping clarify on the grounds that the requirement is clear | 1-a/b/c | AC-003-4 |
| W2 | Not scanning all four boundary classes | 1-c | AC-003-4 |
| W3 | Technology selection appearing in the spec | 2-a/b | AC-003-3 |
| W4 | A spec missing boundary conditions while stating an implementation approach | 2-c | AC-003-3 |
| W5 | Exceeding 18 tasks with no explanation and no split evaluation | 3-a/b | AC-003-6 |
| W6 | Fewer than 12 tasks with no explanation | Scenario 3 reverse | AC-003-6 |
| W7 | A task that cannot be tested alone | 3-c | AC-003-6 |
| W8 | Calling a toolchain command without detecting first | 4-a/b | AC-003-9 |
| W9 | An upstream priority/scope contradiction not caught by clarify | 5-a | AC-003-4 |
| W10 | A split table fixed once with no revision allowed | 5-b | AC-003-1 |
| W11 | No split evaluation when the task count approaches the ceiling | 5-c | AC-003-6 |
