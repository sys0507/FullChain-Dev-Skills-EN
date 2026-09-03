# Inheritance and adjudication rules

## When to read this

When handling upstream open questions and research candidate values.

---

## 1. Zero loss of open questions

### The rule

Upstream has **N** open questions -> the convergence result **still has N**. It may grow,
never shrink.

### The procedure

```
1. Collect: list every open question from the ledger and the architecture baseline decision, AND COUNT THEM
2. Handle each one; each has only three legitimate outcomes
3. Merge in the new questions
4. RECHECK THE COUNT: the inherited portion is at least N
```

**The count is the crux.** Without counting there is no way to prove nothing was lost — "they
all seem to be there" is not enough.

### The three legitimate outcomes

| Outcome | How to write it |
|---|---|
| **Still open** | Keep it as it is; you may add "new information from this round" |
| **Answered** | Keep the entry, annotated "answered: <answer> + <basis>" |
| **Obsolete** | Keep the entry, annotated "**obsolete**: <reason>" |

**All three keep the entry itself.** Once an obsolete question is deleted, the next person to
ask "what happened to that question" has no answer.

### Illegitimate reasons

| Reason | Rebuttal |
|---|---|
| "Convergence means reducing uncertainty" | What converges is the **candidate values**, not the open questions. Deleting one is not convergence, it is pretending it does not exist |
| "This question is not important" | Judging importance itself needs a basis; keep it and mark it low priority |
| "It duplicates another one" | Merging is fine, but **say explicitly which entry it merged into**, and keep both numbers traceable |
| "An answer will emerge later" | Then it is still open. Keep it |

---

## 2. Adjudicate every candidate value

### The rule

The ledger holds **M** research candidate values -> every one MUST reach a definite conclusion.

**There are only two exits**:

```
Promoted to "user confirmed"  --  MUST carry the USER'S BASIS
Kept as an open question      --  enters the open list
```

**There is no third exit.** A candidate that is neither confirmed nor listed as open is
silent adoption.

### What counts as a basis for promotion

| Legitimate basis | Illegitimate |
|---|---|
| The user's own words stating a position this round | "The evidence is strong" |
| A choice the user made among options | "Confidence is high" |
| The user's explicit approval of an option | "Nine out of ten similar projects do it" |
| - | "We cannot continue without confirming it" |

**Confidence and confirmation status are orthogonal.**
High confidence says "this inference is probably right"; confirmation says "the user agrees".
The first does not imply the second.

### The item-by-item reconciliation table

Produce this table once adjudication is done, with **all M rows, none missing**:

| Candidate | Original confidence | Adjudication | Basis |
|---|:---:|---|---|
| ... | High | Promoted | The user said "use this one" |
| ... | High | **Kept open** | The user took no position — high confidence is not confirmation |
| ... | Low | Kept open | Insufficient evidence |

The second row is the easiest case to get wrong: **high confidence with no user position is
still open.**

---

## 3. Labelling a conclusion's premises

Among the eleven answers, any that depends on an unconfirmed premise **MUST state that
premise**.

### How to write it

> "Must-have includes <feature X> —
> **premise**: <candidate Y> is not yet confirmed; if Y does not hold, X should leave the MVP."

### Why it is mandatory

A real lesson: this project's convergence conclusions were overturned twice by later work,
and each time it was because **the premise the conclusion rested on had changed**. But at the
time the conclusion looked exactly as settled as the others, with no marker showing it
carried a condition.

When the premise moved, **nobody knew which conclusions had to move with it** — the only
option was re-reading all of them.

### Self-check

After convergence, ask of each conclusion:

> If the answer to some pending item reversed, would this conclusion still hold?
> If not -> that premise MUST be labelled.

---

## 4. The output MUST distinguish provenance

Label every conclusion in the convergence result with its source:

| Marker | Meaning |
|---|---|
| [confirmed] | The user stated a position |
| [candidate] | Research inference; the user took no position |
| [premise: X] | Depends on an unconfirmed item |

Downstream — the PRD writing especially — **may write only [confirmed] items as settled
requirements**. Without the provenance labels, downstream cannot enforce that rule.
