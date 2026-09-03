# The six-question protocol

## When to read this

Work through it question by question while running the retrospective.

---

## General requirement

**Every question gets a response**, and only two outcomes are acceptable:

| Outcome | How to write it |
|---|---|
| There is something | A specific entry (enters the filtering pool) |
| **None** | "None — <reason>" |

**An answer of "none" MUST carry a reason.** A reasonless "none" is the standard shape of
going through the motions: six questions all answered "none" looks like a retrospective
happened while nothing was actually thought about.

Make the reason specific: "this feature ran straight through the tasks in order with no
rework" carries information; "nothing" does not.

---

## Q1: Where did we hit a pitfall?

**Scope**: errors that stalled us, things that would not run, things that took several
attempts to get right.

**Follow up with**:

- How long were we stuck? More than one attempt is worth recording
- Was the stall an environment problem or an understanding problem? The responses differ
  completely
- Was there an earlier signal we could have caught?

**Easy to miss**: the places that "felt obvious at the time" but, thinking back, actually
cost half a day.

---

## Q2: Where did the AI stall or take a detour?

**Scope**: misreading the spec, producing code that was thrown away, going down a blind alley.

**Follow up with**:

- Was the misreading caused by an ambiguous spec, or by a correct spec being read wrongly?
  The first means changing how specs are written, the second means changing how they are
  prompted — **the two responses MUST NOT be conflated**
- Was any code or document produced and then discarded wholesale?
- Was the same thing explained repeatedly?

**This question is the easiest to skip**, because it requires admitting the process was
bumpy. It also has the highest retention value.

---

## Q3: Which decision looks wrong in hindsight?

**Scope**: technology choice, task splitting, abstraction boundaries.

**Follow up with**:

- Was there enough information at the time to make this decision correctly?
  - Enough, and still wrong -> a judgement problem; record it as `decision reflection`
  - **Not enough** -> that is not an error, it is missing information; what should be
    recorded is "how to obtain that information earlier"
- When was the decision discovered to be wrong? The later it was found, the more it is worth
  recording

**Note**: do not treat "circumstances changed later" as a wrong decision.

---

## Q4: Any "if only we had known"?

**Scope**: a faster or safer path we could have taken.

**Follow up with**:

- Was that better path **knowable at the time**?
  - Knowable -> worth recording; record "how to see it first next time"
  - Not knowable -> that is hindsight; do not record it
- Is it a tooling problem or a method problem?

---

## Q5: Any small reusable technique worth carrying to later features?

**Scope**: something worked out this time that can be applied directly next time.

**Follow up with**:

- Is it **specific to this project** or general? Project-specific ones are worth more
- Is it described concretely enough? "Watch out for idempotence" is not a technique;
  "put every write after the detection's negative branch, so the structure itself is
  checkable" is

**This is the only question that produces positive experience** — the other five all record
problems. Do not skip it.

---

## Q6: Any quirk hit in a tool, framework or third-party library?

**Scope**: behaviour that did not match expectations.

**Follow up with**:

- Is it a quirk or my misunderstanding? A misunderstanding belongs to Q2
- Is it version-dependent? If so, record the version
- Does the official documentation mention it? Undocumented quirks are the most worth
  recording

---

## When a question does not apply

Where the nature of the project makes a question inapplicable (Q6 for a documentation-only
feature, say), write "**not applicable — <reason>**". Do not leave it blank and do not force
an answer.

The difference between "not applicable" and "none":

| | Meaning |
|---|---|
| None | The question applies, but this time there genuinely was nothing |
| Not applicable | The question does not hold for this kind of feature |

---

## After the six questions

Move to filtering (see `anti-padding.md`):

```
0 candidate entries  -> record "this feature produced no lessons worth keeping"; a valid output
1-5 candidates       -> keep them all
More than 5          -> filter down to five or fewer, and explain what was filtered out and why
```
