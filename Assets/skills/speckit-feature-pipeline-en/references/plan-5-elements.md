# The five elements of plan

## When to read this

Before writing plan.md, and when deciding whether a plan may proceed to the tasks step.

**Missing any of the five means rework; do not proceed to tasks.**

---

## 1. Project file structure

**Paths plus each file's core responsibility.**

| Good | Bad |
|---|---|
| A table: path / new-modify-readonly / core responsibility | Just a directory tree |
| **Read-only** files marked explicitly (MUST NOT be modified) | No distinction between new and modified |

Marking read-only matters — it is the first line of defence against accidental edits.

---

## 2. Data flow

**A diagram is mandatory.** A data flow described in prose becomes uncheckable past three
nodes.

The diagram MUST show:

| Element | Note |
|---|---|
| Input sources | Including optional inputs (dashed) |
| Decision nodes | Especially **rework decisions with a back edge** |
| Output destinations | Who consumes it |
| Forbidden paths | Where an edge must never be taken, draw it and label it |

> **A structural guarantee beats a written constraint**: where a rule requires "A must come
> before B", making the diagram show that order is far more reliable than a sentence saying
> "mind the order".
> Example: idempotence requires detection before writing, so on the diagram every write sits
> after the detection's negative branch — that is a checkable structure, not a reminder.

---

## 3. Dependency list

Each dependency lists **name / level / fallback**.

| Level | Fallback requirement |
|---|---|
| `required` | The fallback may be omitted, but you MUST say **why it cannot degrade** |
| `optional` | The fallback is **mandatory** |
| `orchestration` | The **standalone-mode equivalent entry point** is mandatory |

Where the project has language runtime dependencies, list the versions or ranges too.
**Where there are none, write "no runtime dependencies"; do not invent version numbers.**

---

## 4. Integration points with existing systems

**The most frequently skipped element.** It carries no immediate output pressure, and
skipping it reinvents wheels.

It MUST be split into two parts:

```markdown
### Reused (never rebuilt)
| What is reused | How |

### New
| What is new | Why |
```

**Every row under "new" MUST be able to answer: why can the existing one not be reused?**
Being unable to answer means it should be reused.

A third part is also needed:

```markdown
### Explicitly not touched
- List what this feature MUST NOT modify
```

"Explicitly not touched" is a guardrail for the implementation phase — especially in features
that modify existing assets.

---

## 5. Risk list

**The second most frequently skipped element.**

Each risk carries: **risk / type / impact / mitigation**.

| Type | Meaning |
|---|---|
| Technical | The approach itself may not hold |
| Data | The input does not match the assumption |
| Process | Execution order or collaboration goes wrong |
| Security | Credentials, permissions, escalation |

### What a good risk entry looks like

| Bad | Good |
|---|---|
| "There may be compatibility problems" | "The naming suffixes are inconsistent, so deriving English names by concatenating 'Chinese name + -en' produces the wrong name for the first four -> mitigation: two independent lists, no concatenation" |
| "There may not be enough time" | "The work for 12 skills x 2 items was underestimated -> mitigation: batch into four groups by dependency structure, deciding once per group" |

A good risk **points at a specific mechanism**, and the mitigation is **executable**.
"Test more thoroughly" and "be careful" are not mitigations.

### Three risks that MUST be registered

1. **The single most likely way this feature fails** — if you write only one, write this
2. **The risk of an upstream dependency not being finished**
3. **Mis-trigger and overreach risk** (might this feature do something it should not)

---

## The rework decision

Tick each item before proceeding to tasks:

```
[ ] 1 File structure: paths + responsibilities + read-only marked
[ ] 2 Data flow: a diagram showing decision nodes and rework back edges
[ ] 3 Dependency list: every item has a level; non-required items have a fallback
[ ] 4 Integration points: reused / new / explicitly-not-touched, all three present
[ ] 5 Risk list: every entry names a specific mechanism and an executable mitigation
```

**Any box unticked -> rework; do not proceed to tasks.**
