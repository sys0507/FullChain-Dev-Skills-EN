# Built-in fallback workflows

## When to read this

**When external workflow tooling is unavailable.** Where it is available, use it — this file
is the degraded path, not an alternative path.

## The priority MUST NOT invert

| Situation | Which path |
|---|---|
| External TDD or review capability is available | **Use it** |
| Unavailable | Run the built-in flow in this file, **and label it in the output** |

> Switching to the fallback because a fallback exists is a capability regression.
> The only reason the fallback exists is so that a user who installed nothing but this skill
> can still finish the work.

**Labelling format**:

> "External workflow tooling not used; the built-in equivalent flow was run.
> Therefore <capability> is not covered: <specifically what>."

---

## 1. Built-in TDD (red -> green -> refactor)

### RED: write the failing test first

1. Read the **decision criterion** from that task's output-verification field in `tasks.md`
2. Translate that criterion into **one assertion that will fail**
3. **Run it and confirm it genuinely fails**

> Step 3 MUST NOT be skipped. Writing "the test is in place" without running it is not RED.
> An assertion that is always true also looks green.

The failure message MUST explain what differs, not merely say `AssertionError`.

### GREEN: write the minimum implementation

Write only the code needed to **make this one test pass**.

| Wrong | Right |
|---|---|
| Implementing the related features while you are in there | Turning only the current assertion green |
| Adding a parameter that "might be useful later" | Writing nothing the current task does not need |
| Adding error handling ahead of any test for it | Error handling also gets a failing test first |

Run the tests and confirm they went **from red to green**. Once green, stop; do not carry on
"improving".

### REFACTOR: tidy up under a green light

Tidy the structure while the tests stay green.

**Touch only what your change introduced**:

- Remove unused imports and variables **your change made unused**
- Do not refactor code that was already there and is not broken
- Do not "improve" the style of adjacent code in passing

**Rerun the tests** after each tidy-up.

### Loop exit

A task exits when **its output verification holds** and the existing tests are still all green.

---

## 2. Built-in structured code review

Run this once every task is green. **Scan every class; skip none.**

### The five scan classes

| Class | What to scan for |
|:-:|---|
| **1. Resilience** | Missing retries, timeouts or circuit breakers; whether a failing external call can hang silently |
| **2. Cross-cutting consistency** | Whether authorisation, rate limiting and logging cover **every** entry point. "Three of the four endpoints have it, the fourth was missed" is the classic failure |
| **3. Defensiveness** | Unhandled nulls, missing input validation, missing idempotency keys; whether a repeat run produces duplicate data |
| **4. Data migration** (where applicable) | Whether there is a rollback path; whether it is batched |
| **5. Project rule compliance** | Whether it violates the project constitution; whether values that should come from configuration are hardcoded; whether a forbidden dependency was introduced |

Class 5 requires reading the project constitution. **With no constitution file, mark that
class as not covered** — do not invent a set of "general standards" from impression and
review against those.

### Output format

```
| # | Class | File:line | Description | Priority |
```

Three priorities: P0 must fix / P1 should fix / P2 can wait.

### Digesting and closing the loop

| Result | Action |
|---|---|
| Zero defects | Proceed to close-out |
| Defects found | Return to the relevant task and **fix via TDD** (write the reproducing failing test first), then **run the review again**, until zero defects |

**Do not simply edit the code until the problem disappears** — a fix with no reproducing test
cannot prove it actually worked, and does not stop the problem recurring.

### The limits of self-review (MUST be labelled honestly)

The built-in review is **the same agent reviewing code it just wrote**. It catches
checklist-shaped omissions (a missing timeout, one endpoint missing authorisation), but it
does not catch **blind spots** — what you did not think of while writing, you will most
likely not think of while reviewing.

So the output should state:

> "This was a built-in self-review, not checked by an independent perspective.
> Checklist-shaped defects were scanned for, but design-level blind spots may remain
> undiscovered."

---

## 3. Coverage comparison

| Capability | External tooling | Built-in fallback |
|---|:---:|:---:|
| Red-green-refactor loop | Yes | Yes |
| Five-class checklist review | Yes | Yes |
| Review results in a table | Yes | Yes |
| Defect loop closure (fix via TDD) | Yes | Yes |
| **Independent-perspective review** | Yes | **No — the same agent reviews itself** |
| **That toolchain's other integrations** | Yes | **No** |

The last two rows are the fallback's real losses. They **MUST appear in the output's
labelling** and MUST NOT be glossed over.
