# The four steps' output contracts

## When to read this

Before starting a step, to check that step's required and forbidden contents.

---

## 1. specify -> spec.md

### Required

| Item | Note |
|---|---|
| Functional boundary | **Both in-scope and out-of-scope.** Writing only what is built and not what is not guarantees the scope grows |
| MVP constraints | The minimum set that must hold this round |
| Runtime environment | The carrier, the platform, the volume constraints |
| Business flow | Trigger -> input -> processing -> output |
| Inputs / outputs | Each one's source, format, and behaviour when absent |
| Acceptance criteria | Given / When / Then, **machine-verifiable** |
| Boundary conditions | Nulls, anomalies, extreme scale, concurrency, failure |

### Forbidden

| Forbidden | Example |
|---|---|
| Framework or library names | "Render it with such-and-such charting library" |
| Database selection | "Store it in PostgreSQL" |
| Specific runtime versions | "Node 20" |
| Architectural layering decisions | "The frontend renders and the backend provides an aggregation endpoint" |
| Implementation approaches | "Streaming parsing", "add a cache", "paginate" |

### The test

> An engineer could satisfy this with a different implementation -> **it stays in the spec**
> Change the implementation and it is no longer satisfied -> **move it to plan**

### The most common real mistake

Not "wrote technology", but **wrote technology and omitted the boundary**:

| Written like this | Should be written like this |
|---|---|
| "Use streaming parsing for large volumes to avoid memory exhaustion" | "For a single file of 100,000 lines or more, the system MUST produce a usable result within 30 seconds, or refuse explicitly and state the ceiling" |
| "Paginate to reduce the load" | "Where the result set exceeds 1000 items, batched retrieval MUST be supported and the total MUST be knowable" |
| "Add a retry mechanism" | "When an external call fails, the user MUST see a clear reason within 5 seconds; it MUST NOT hang silently" |

The right-hand column **specifies no implementation**, yet every line is verifiable and
leaves plan the full decision space.

### Length

A complex business feature is usually 1500-2000 words. A simple one is judged by complete
coverage of boundaries and acceptance, **not padded to reach a word count**.

---

## 2. clarify -> write back into spec.md

### Mandatory

**MUST NOT be skipped under any circumstances.** See `clarify-4-boundaries.md`.

### Output shape

clarify **produces no new file**. Instead it:

1. Writes back into the corresponding passages of `spec.md`
2. Leaves a **Clarifications record** in `spec.md`: the question, the conclusion, and **which
   section it was written back into**

### Record format

```markdown
## Clarifications

### MVP boundary
| # | Question | Conclusion | Write-back location |
|:-:|---|---|---|
| C1 | ... | ... | Section 2.2 |
```

**The write-back location column is mandatory.** A clarification with no write-back location
may as well not have happened — that column is what proves the clarification genuinely
changed the spec rather than merely asking a question.

---

## 3. plan -> plan.md

See `plan-5-elements.md`. Missing any of the five means rework, and **it does not proceed to
tasks**.

### Reuse first

Element 4 of plan (integration points) MUST **distinguish reuse from new build explicitly**:

```markdown
### Reused (never rebuilt)
| What is reused | How |
### New
| What is new | Why |
```

Every row under "new" MUST be able to answer **why the existing one cannot be reused**.
Being unable to answer means it should be reused.

---

## 4. tasks -> tasks.md

See `task-granularity.md`.

### The fixed format of each task

```markdown
- [ ] **T01** `[label]` task description
  - [FR source] the specific section of spec or plan
  - [task dependencies] none / T0X, T0Y
  - [output verification] how it is judged done
```

**The checkbox is mandatory.** The implementation discipline is "update the checkbox after
each task completes", and with no checkbox that discipline cannot be executed.

### How to write "output verification"

| Bad | Good |
|---|---|
| "Done" | "A 12-row list is produced; anything undeclared is marked as such, and the entry count is counted" |
| "Tests pass" | "Contains the assertion 'two consecutive runs produce byte-identical output'" |
| "Documentation written" | "All three sections present; the standalone section missing any of the three questions fails" |

A good output verification **lets a third party judge independently whether it is done**,
without relying on the executor's self-assessment.

---

## The gates between the four steps

| From -> to | Gate |
|---|---|
| specify -> clarify | None (it always proceeds) |
| clarify -> plan | At least one question per boundary class, each with a write-back location |
| plan -> tasks | **All five elements present**; missing one means rework |
| tasks -> next feature | Granularity compliant; any deviation from 12-18 explained |
