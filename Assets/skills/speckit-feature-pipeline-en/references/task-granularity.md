# Task granularity control

## When to read this

While splitting tasks, and whenever the task count deviates from 12-18.

---

## 1. Three hard requirements

Every task MUST satisfy all three:

| # | Requirement | Self-check |
|:-:|---|---|
| 1 | **Single responsibility** | Can this task be stated in one sentence? Needing an "and" means it should be split |
| 2 | **Independently testable** | Are the inputs and outputs explicit? Can a third party judge independently whether it is done? |
| 3 | **Completable within one context-bounded cycle** | Do not sacrifice quality to an unrealistic duration |

### Examples that fail

| Fails | The problem | Split into |
|---|---|---|
| "Implement the permissions system" | Cannot be tested alone; far too coarse | "Define the role-to-permission mapping" / "Implement the permission decision function" / "Add boundary cases for the decision function" |
| "Write the docs and test them" | Two things | Split into two |
| "Optimise performance" | No output verification | "Reduce operation X's latency from A to B, measured by C" |

---

## 2. Size rules

| Situation | Handling |
|---|---|
| 12-18 | Normal |
| **17 or more** | **Explicitly evaluate whether it should be split into several features, and record the conclusion** (even when the conclusion is not to) |
| **More than 18** | **Split the feature first**, rather than accepting an overlong list. Where it cannot be split, the size MUST be justified |
| **Fewer than 12** | Allowed, but you MUST **show they remain independently testable** (explain why this feature is genuinely small) |

### Why 17 triggers an evaluation

> **A real case**: this project's quality-gates feature landed on exactly 18 tasks, right at
> the ceiling. Nobody actively evaluated whether it should be split; it simply happened not
> to exceed.
> Silence while approaching a ceiling is dangerous — the next small requirement addition
> crosses it, and by then the spec and plan are written, making the split far more expensive
> than it would have been.

Write the evaluation's conclusion into a "size note" section of tasks.md. Both outcomes are
legitimate:

- "Evaluated splitting into features A and B; rejected — they share one fixture and are bound
  by the same gate, and splitting leaves the gate with no subject to act on"
- "Evaluated; it should indeed be split" -> go back and correct the split table

### Padding is forbidden

Not reaching twelve means the feature is genuinely small, and **writing it clearly is enough**.
The classic sign of padding: splitting one task into "prepare", "execute" and "check" where
the three have no independent output verification of their own.

---

## 3. The three-label format

```markdown
- [ ] **T01** `[label]` task description
  - [FR source] spec section X or plan section Y
  - [task dependencies] none / T0X, T0Y
  - [output verification] how it is judged done
```

### `[FR source]`

Points at **a specific section of the spec or plan**, not a vague "the requirements document".
Its purpose: during implementation, being able to trace why this task exists.

### `[task dependencies]`

List only **direct dependencies**, not transitive ones.
A task depending on five or more usually means it should be split or moved later.

### `[output verification]`

**The most important field.** It MUST let a third party judge independently, without relying
on the executor's self-assessment.

| Bad | Good |
|---|---|
| "Done" | "A 12-row list is produced; anything undeclared is marked as such, and the entry count is counted" |
| "Tests pass" | "Contains the assertion 'two consecutive runs produce byte-identical output'" |
| "Meets the standard" | "All three sections present; the standalone section missing any of the three questions fails" |

**A heuristic**: an output verification containing specific numbers, specific file names or
specific assertions is usually good; one containing only adjectives usually is not.

---

## 4. Parallel groups

Mark which tasks can run concurrently and which MUST be serial.

```markdown
| Group | Tasks | Note |
|:-:|---|---|
| **P1** | T02, T03, T04 | Three scans, mutually independent |

**MUST be serial**: T05 -> T06 (the schema must exist before the table can be filled)
```

### Two reasons for serialisation, and they MUST be distinguished

| Reason | Example | Note |
|---|---|---|
| **Order dependency** | T06 needs T05's output | Common |
| **Structural guarantee** | Idempotence detection MUST precede the write | Not merely order but a **correctness requirement** — write it into the output verification so it can be checked |

The second kind MUST be called out in the note, or an implementer may parallelise it "for
efficiency" and break the structural constraint.

---

## 5. The checkbox is mandatory

Every task begins with `- [ ]`.

The implementation discipline is "update the checkbox after each task completes", and
**without a checkbox that discipline cannot be executed**.

> A real case: the first ten tasks.md files this project produced had no checkboxes at all,
> while the constitution said "Always update tasks.md checkbox after EACH task".
> The rule and the artifact did not match, and it went unnoticed until the implementation
> preparation stage, when 150 of them had to be added.
