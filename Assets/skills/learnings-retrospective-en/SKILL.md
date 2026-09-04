---
name: learnings-retrospective-en
description: >-
  Run a pitfall-avoidance retrospective after each feature closes, working through six
  questions and writing the lessons worth keeping into the top of the learnings file in a
  uniform format. Zero entries are allowed - where a feature genuinely produced nothing worth
  recording, writing "none" is a valid output; five entries per feature is the ceiling,
  because a retrospective's value lies in the filtering, not the recording.
  Trigger keywords: retrospective / pitfall retrospective / lessons learned / LEARNINGS /
  what went wrong / what did we learn / feature close-out retrospective / cross-feature lessons.
  Do not use for: modifying the project context file (this skill only emits an injection
  signal; the injection itself belongs to the context bootstrap skill), changing code or
  tests, changing spec documents, or appraising people.
  Invoke it whenever the task involves summing up what was just finished, even if the user
  never says the word "skill".
license: MIT
allowed-tools: Read Write Edit
metadata:
  version: "1.0"
  lang: en
  stage: "10"
  standalone: true
  produces:
    - "LEARNINGS.md"
    - "injection signal (session output, never written to disk)"
  requires:
    - name: "the feature's process records"
      level: optional
      fallback: "Run the retrospective from the user's account, and label the output 'no process records, based on the user's account'"
    - name: "LEARNINGS.md"
      level: optional
      fallback: "Create it if it does not exist"
    - name: "project context file"
      level: optional
      fallback: "Read-only, used solely to decide whether to emit the injection signal; with none present, emit no signal and do not suggest creating one"
---

# Lessons Retrospective

## The one thing this skill never does

**It does not modify the project context file.**

Stage 10 originally asked for a reference to the learnings file to be injected into the
project context file. But that file is owned by the context bootstrap skill, and it carries
a size ceiling plus rules about preserving hand-written content and showing a diff first.
Two skills writing to the same file from both directions is the **only write conflict in
the whole chain**.

**The ruling**: this skill owns the learnings file only; **the injection is handed back to
the context bootstrap skill**, and this skill emits only a signal that injection is needed.

## Two ways to fail, equally bad

| Failure mode | Consequence |
|---|---|
| Simply not doing it | The same pitfall gets hit again in the next feature |
| **Padding to have something to show** | The learnings file is diluted by worthless entries, the few that matter get buried, and before long nobody reads it |

This skill's design centres on **guarding both ends at once**: genuinely do it, and allow
"this feature produced nothing worth recording".

## The six questions

| # | Question |
|:-:|---|
| 1 | Where did we hit a pitfall? (errors that stalled us, things that would not run, things that took several attempts) |
| 2 | Where did the AI stall or take a detour? (misread the spec, produced dead code, went down a blind alley) |
| 3 | Which decision looks wrong in hindsight? (a technology choice, a task split, an abstraction boundary) |
| 4 | Any "if only we had known"? (a faster or safer path we could have taken) |
| 5 | Any small reusable technique worth carrying to later features? |
| 6 | Any quirk hit in a tool, framework or third-party library? |

**Every question gets a response** — either a specific entry or an explicit "none".
An answer of "none" also needs a reason, to stop it degenerating into blanket empty answers.

See `references/six-question-protocol.md` for each question expanded, how to follow up, and
what an acceptable "none" looks like.

## Anti-padding

| Rule | Note |
|---|---|
| **Zero entries are allowed** | Where a feature genuinely produced nothing worth recording, write "none" — **that is a valid output** |
| **Five entries is the ceiling** | Going over means the filtering was not done; a retrospective's value is in the filtering, not the recording |
| Filtered-out items get explained | Say in the session why an item was filtered out; do not drop it silently |

**The filtering test**: next time I hit something similar, **will I genuinely come back and
read this entry?** If the answer is no, it should not be recorded.

See `references/anti-padding.md` for the filtering test and the argument for why zero
entries is a valid outcome.

## Entry format

```markdown
## <date> · <type> · <feature id-name>
**Symptom / decision**: state the problem in one sentence.
**What to do instead**: what to do next time.
**Scope**: which kinds of feature should come back to this entry (optional).
```

**Type is a closed set of six**: pitfall / decision reflection / reusable technique /
tool quirk / AI stall / architecture lesson.

**Any entry related to code MUST carry the file path** — so it can be found next time.
An entry recorded but unfindable may as well not exist.

See `references/entry-taxonomy.md` for how to judge each of the six types, with positive and
negative examples.

## Writing rules

| Rule | Note |
|---|---|
| **New entries go at the very top** | Newest first, so the most recent lessons are the easiest to see |
| **Existing content is left alone** | Content and order preserved verbatim |
| Existing content in a non-standard format | **Do not reformat it**; write the new entry at the top in the standard format and note the difference |

## The injection signal (it does not inject)

| Detection | Action |
|---|---|
| The context file already references the learnings file | **Emit no signal**; report "the reference already exists" |
| No reference | **Emit the signal**: recommend the context bootstrap skill inject it |
| The project has no context file | **Emit no signal**, and **do not suggest creating one** — that is a separate matter |

The signal is session output and is **never written to the context file**.

## Batch retrospectives

When several features are reviewed together:

1. **Group by feature first**
2. **Then add a section for system-level cross-feature lessons**

Step 2 MUST NOT be dropped. Grouped stacking alone loses exactly the class of lesson that
only becomes visible when those features are seen together.

## About the work, not the person

Entries involving an individual's mistake **are rewritten as descriptions of the work**.

A retrospective has to be sustainable; once it turns into appraising people, nobody will
take part.

## Upstream Artifacts

| Artifact | Level | When missing |
|---|:---:|---|
| The feature's process records | optional | Work from the user's account and label the source |
| `LEARNINGS.md` | optional | Create it if absent |
| Project context file | optional | **Read-only**, used to decide whether to signal; with none, emit no signal and suggest nothing |

> This skill has **no `required` external dependency** — that is what makes it usable alone.

## Downstream Consumers

| Consumer | What it reads |
|---|---|
| Later features' implementation | The learnings file — avoiding pitfalls when a type or scope matches |
| The context bootstrap skill | The injection signal |

## Standalone Use

**What you provide**: just tell me how this feature went. Progress records and commit
history help; without them it still works.

**What you get**: the six-question retrospective, filtered lesson entries, written to the top
of the learnings file. The anti-padding rules and the format standard depend on nothing
upstream and apply identically in standalone mode.

**What you don't get**:

- **It will not touch your project context file.** Where a learnings reference needs
  injecting, it emits a signal only; the context bootstrap skill performs the injection —
  this is the resolution of the chain's only write conflict, not a missing capability.
- **It does not change code, tests or spec documents.**
- With no process records, the retrospective rests entirely on your account, and the output
  says so; I cannot recall for you the parts you did not mention.

## Anti-patterns

- Modifying the project context file
- Inventing lessons to have something to show
- Going past five entries without filtering
- Answering "none" to all six questions with no reasons
- Overwriting or reordering existing entries
- A code-related entry with no file path
- A batch retrospective that only stacks groups and skips the system-level section
- Writing an entry as an appraisal of a person
- Suggesting the project create a context file when it has none
