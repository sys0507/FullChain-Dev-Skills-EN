# Anti-padding rules

## When to read this

While filtering the candidate entries, and whenever you are unsure whether an entry is worth
keeping.

---

## The core test

> **Next time I hit something similar, will I genuinely come back and read this entry?**

If no -> **do not record it**.

This test is more useful than "is this entry correct". A correct lesson nobody will revisit
has a net effect of **dilution** — it crowds out attention from the few that matter.

---

## Zero entries is a valid output

**Where a feature genuinely produced nothing worth recording, writing "none" is a valid
retrospective result.**

### Why this has to be stated as a rule

Forbidding zero entries manufactures a motive to pad. Faced with "you must produce at least
one", an executor writes down things that were always going to be true:

| Padding | Why it is padding |
|---|---|
| "Read the requirements carefully" | Always true, never useful |
| "Testing matters" | Not a lesson, common sense |
| "Diagnose before fixing" | The same |
| "This one went according to plan" | Not a lesson |

Once twenty or thirty entries of this kind accumulate, nobody opens the learnings file any
more — and by then it may genuinely contain five extremely valuable ones.

### What a valid zero-entry result looks like

> "This feature produced no lessons worth keeping.
> All six questions were worked through: Q1-Q4 none (ran straight through the tasks in
> order, no rework, no reversed decisions); Q5 none (used existing techniques, nothing new);
> Q6 not applicable (documentation-only feature, no tools involved)."

**It MUST show that the six questions were genuinely worked through**, rather than simply
saying "none".

---

## The ceiling of five

More than five means **the filtering was not done**, not that this feature was unusually rich.

### Why it is a ceiling and not a target

A retrospective's value is in the **filtering**, not the recording.
Writing all eight candidates in as they are hands the filtering job to whoever reads it next
— and that person has no context and cannot do it.

### Filtered-out items MUST be explained

Explain **in the session** why each filtered-out item was dropped; do not discard silently.

> "Eight candidates, four written in. The four dropped, with reasons:
> 1. 'Read requirements carefully' — always true, gives no guidance;
> 2. 'This library's API is a bit odd' — too vague to find by search next time;
> 3 and 4 duplicated entry 2 and were merged into it."

The point of explaining: it lets the user overrule your filtering. They may consider one of
them important.

---

## Merging beats listing

When the same lesson recurs across several features:

**Merge it into one entry** annotated "**recurs across features**", rather than recording
several.

The recurrence is itself the signal — it says this is not incidental but **systemic**, so it
deserves more weight, not more lines.

---

## What makes an entry worth keeping

| Property | Note |
|---|---|
| **Not obvious at the time** | If it had been obvious to you then, you would not have hit it |
| **Findable** | Code-related entries carry a file path; tool-related ones carry a version |
| **Has a concrete response** | "What to do next time" can actually be written down |
| **Has a scope** | You know under what circumstances to come back to it |

An entry meeting all four is usually worth keeping; one meeting only one or two is usually
padding.

---

## A real counter-example

This project's checker scripts produced four problems in a row (scope too wide, byte ranges,
literals containing markdown markers, silently failing string replacement).

| Recorded as four entries | Recorded as one |
|---|---|
| Each of the four failures described separately | "**When checking documents automatically, the checkers have a higher false-positive rate than the subjects have defects.** All four self-check false alarms were the checker's own fault; zero were real defects. Response: every check MUST carry a negative sample that MUST NOT be reported." |

The single entry on the right is worth more than the four on the left — it **extracts what
they share** and gives an actionable response.
