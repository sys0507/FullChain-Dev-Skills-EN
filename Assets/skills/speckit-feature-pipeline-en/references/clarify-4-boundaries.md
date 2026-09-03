# The four boundary classes clarify scans

## When to read this

While running the clarify step. **This step MUST NOT be skipped.**

---

## Why it cannot be skipped

The most common reason given for skipping is "the requirement is already clear". That reason
**points precisely at the case that most needs clarifying**.

> **clarify is not a remedy for a vague requirement; it is the mirror you hold up when a
> requirement looks clear.**

A detailed PRD usually leaves three gaps, and all three detonate during implementation:

1. **What is not being built** — what to build is spelled out, where the boundary sits is not
2. **What happens on failure** — the happy path is described, the error path is not
3. **Extreme scale** — the typical case is described, the ceiling is not

A vague PRD, by contrast, puts people on guard and gets clarified properly.

---

## The four question banks

**At least one question per class**, and every question MUST trace to a specific passage of
`spec.md`.

### Class 1: MVP boundary

| Candidate questions |
|---|
| What is explicitly **not** being built? Is out-of-scope written? |
| **Are the priority labels consistent with the delivery scope?** (see the real case below) |
| Where is the boundary between this feature and its neighbours? Who owns the overlap? |
| Is there an implicit expectation that something will be "done while we are in there"? |
| Is a given capability this round or the next? On what basis? |

> **A real case**: this project's PRD marked a document as Should in section 5.1 while
> including it in the MVP deliverables in section 10. The contradiction only surfaced while
> writing the tenth feature's spec.
> **"Are the priority labels consistent with the delivery scope" MUST be a standing
> question**, because a contradiction of this kind is invisible when reading either section
> alone.

### Class 2: interface boundary

| Candidate questions |
|---|
| What happens when an external call fails? How many retries? What timeout? |
| Is there a rate limit or quota? How does it behave at the ceiling? |
| When a dependency is unavailable, degrade or stop? How is the user told about a degradation? |
| How is compatibility handled when the contract changes? |
| What happens when authentication credentials are missing? |

### Class 3: data boundary

| Candidate questions |
|---|
| How are nulls and missing fields handled? |
| How are anomalous values handled (negatives, over-length, invalid encoding)? |
| What is the scale ceiling? Above it, **refuse explicitly** or do the best it can? |
| What happens on concurrent writes to the same data? |
| Does a repeat run produce duplicate data? |

### Class 4: integration boundary

| Candidate questions |
|---|
| What assumptions does it make about interacting with existing systems? Which are guesses? |
| Will it change something someone else owns? If so, must their tests be rerun? |
| Who reads this feature's output? Will they break if the format changes? |
| Does it write to the same file as another feature? What is the ruling? |
| Can this feature still run when an upstream artifact is missing? |

---

## Traceable write-back rules

**Every clarify question MUST have a write-back location.** Record it like this:

```markdown
| # | Question | Conclusion | Write-back location |
|:-:|---|---|---|
| C1 | Refuse above the limit, or do the best it can? | Refuse explicitly and state the ceiling | Section 7, boundary conditions |
```

### Three legitimate outcomes

| Outcome | Handling |
|---|---|
| A definite answer | Write it into the conclusion and back into the corresponding spec passage |
| **The user is unsure too** | Record it as an open question; **do not decide for them** |
| Not applicable to this feature | Record "not applicable, with the reason"; **do not leave it blank** |

### Illegitimate outcomes

- "This feature needs no clarification" — skipping the step wholesale
- Asking a question and reaching no conclusion
- Reaching a conclusion without changing the spec (which means the conclusion never landed)

---

## Self-check

After clarify, ask yourself:

1. Did each of the four classes get **at least one question**?
2. Does every question have a **write-back location**?
3. Is any conclusion actually a guess I made on the user's behalf?
4. Compared with before clarify, **has the spec genuinely changed**? If not, this
   clarification went through the motions.
