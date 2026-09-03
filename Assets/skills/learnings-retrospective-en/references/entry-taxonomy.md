# Entry types

## When to read this

When classifying a lesson, or when unsure which type it belongs to.

---

## A closed set of six values

| Type | How to judge it | Corresponding question |
|---|---|:---:|
| `pitfall` | Stalled, would not run, took several attempts to get right | Q1 |
| `AI stall` | The AI misread the spec, produced dead code, went down a blind alley | Q2 |
| `decision reflection` | A choice that looks wrong in hindsight (enough information, wrong judgement) | Q3 |
| `reusable technique` | Something worked out here that can be used directly next time | Q4, Q5 |
| `tool quirk` | A tool, framework or library behaving contrary to expectation | Q6 |
| `architecture lesson` | A lesson at the level of abstraction boundaries or module division | Q3, Q5 |

**The set is closed.** When something will not classify, **do not invent a new type**.
Instead:

1. Re-examine it — is it actually a lesson, or a stray thought?
2. If it genuinely is a lesson but will not classify, record it as pending, as input to
   revising the type system

---

## Positive and negative examples per type

### `pitfall`

| Good | Bad |
|---|---|
| "On Windows, counting Chinese characters with a byte-range grep also matches em dashes and arrows, inflating the ratio. Response: use a Unicode code-point range." | "Be careful when counting." |

What is wrong on the right: **it cannot be found by search next time, and it says nothing
about what to do.**

### `AI stall`

| Good | Bad |
|---|---|
| "The spec said 'at least one question per each of the four boundaries'; during implementation it was read as 'ask about one of the four'. The root cause is that the word 'each' is easy to skim over in a long sentence. Response: put counting requirements on their own line, in bold." | "The AI misunderstood the requirement." |

The right-hand version says nothing about **what was wrong, why, or how to prevent it**.

### `decision reflection`

| Good | Bad |
|---|---|
| "Folding the thin index into the quality-gates feature was the wrong call — at the time nobody noticed the index was marked Should in the PRD while the quality gates were Must, and mixing them blurs the scope boundary. Response: check that priorities match before splitting." | "The split plan changed once." |

Note: **a decision failure caused by insufficient information does not belong to this type**;
that should be recorded as "how to obtain that information earlier".

### `reusable technique`

| Good | Bad |
|---|---|
| "Make idempotence a structural guarantee: put every write after the detection's negative branch, so the code structure itself is checkable — more reliable than a comment saying 'careful on rerun'." | "Watch out for idempotence." |

The right-hand version is not a technique, it is a reminder. **A technique has to be concrete
enough to follow.**

### `tool quirk`

| Good | Bad |
|---|---|
| "The include list's copy mechanism requires a file to both match a pattern and already be ignored; a file that matches but is not ignored is skipped silently, with no error." | "That mechanism is a bit awkward." |

Quirk entries **MUST state the specific behaviour**, or the same thing will be hit again.

### `architecture lesson`

| Good | Bad |
|---|---|
| "Putting the checker scripts inside any one skill's directory would constitute a cross-skill reference, violating the very rule they check. A shared `tools/` is the only self-consistent location." | "Plan the directory structure properly." |

---

## When classification is ambiguous

One lesson may look like two types at once. Decide in this order:

```
1. Is its core "something behaved unexpectedly"?      -> tool quirk
2. Is its core "I judged this wrongly at the time"?   -> decision reflection
3. Is its core "next time you can do this"?           -> reusable technique
4. Is its core "the AI's output was wrong"?           -> AI stall
5. Is its core "the structure or boundary was wrong"? -> architecture lesson
6. None of those is typical; mainly "we got stuck"    -> pitfall
```

**Classify it once; do not record it twice.** The type is a retrieval dimension, not a
complete description.

---

## Code-related entries

**They MUST carry the file path.**

```markdown
## 2026-08-31 · architecture lesson · 009-quality-gates
**Symptom / decision**: the checker scripts were originally planned to live inside a skill
directory, which would constitute a cross-skill reference.
**What to do instead**: put them in a shared `tools/skill_checks/`.
Files involved: `tools/skill_checks/run_all.py`
**Scope**: any tool shared by several skills.
```

A code-related lesson with no path cannot be found by grep next time, which is the same as
not having recorded it.
