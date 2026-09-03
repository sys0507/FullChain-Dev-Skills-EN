# Adapting to a divergence method

## When to read this

When deciding whether to delegate to an external divergence method or run the built-in flow.

---

## The principle

> **Detect first, then use; on detection failure switch to built-in, do not force it.**

This skill does not reinvent divergence methods. Where an external method is available,
**delegate to it** — what this skill provides is the constraints, not the method.

---

## Detection

| # | What to detect | How it is judged |
|:-:|---|---|
| 1 | Whether a corresponding divergence/convergence capability is visible in the session | It appears in the available list |
| 2 | Whether the project documentation declares that method is used | The context file mentions it |

Both negative -> run the built-in flow. **The detection result MUST be recorded; it cannot be
decided silently.**

Where the command name is unstable, **do not brute-force through candidates** — read the
actual available list for the name; where that still fails, switch to built-in and label it
"the method exists but its invocation name could not be determined".

---

## The boundary when delegating

Delegating to an external method **is not handing over the constraints**. This skill still
guards all four:

| Constraint | Who guards it after delegation |
|---|---|
| Frozen topics (not reopening the architecture baseline, and so on) | **This skill** — filter before handing the topic over |
| Zero loss of open questions | **This skill** — reconcile the count on receiving the result |
| Adjudicating every candidate | **This skill** — the external method does not know the ledger exists |
| Premise labelling | **This skill** — add the labels on receiving the result |

**The external method is responsible for the quality of the divergence and the questioning;
this skill is responsible for the boundaries and the bookkeeping.**

---

## The built-in equivalent flow

Take this path when the external method is unavailable. The goal is to produce answers to the
eleven questions while holding all four constraints.

### Advance question by question, one at a time

```
1. State that question's goal and how it will be judged
2. Give a preliminary answer from the upstream material, with its evidence source
3. Point out where that answer is weak - challenge yourself
4. Where user input is needed, ask one question at a time with A/B/C options
5. Record the answer plus its provenance marker (confirmed / candidate / premise)
```

**Step 3 MUST NOT be skipped.** The built-in flow's biggest risk is asking yourself questions
and being very satisfied with your own answers — actively naming the weak spots is the only
hedge against it.

### Look back at the end of each group

Stop once at the end of each of the four groups and check:

- Does this group's answer contradict any earlier group?
- Did any answer actually touch a frozen topic?
- Does any answer depend on an unconfirmed premise without saying so?

### Labelling

The output MUST say:

> "No external divergence method was used this round; the built-in equivalent flow was run.
> All four constraints (frozen topics / zero loss of open questions / adjudicating every
> candidate / premise labelling) were applied.
> The built-in flow advances from one side only and lacks the external method's
> multi-perspective questioning."

**That last sentence is the built-in flow's real loss, and it MUST be written.**

---

## Coverage comparison

| Capability | External method | Built-in flow |
|---|:---:|:---:|
| All eleven questions covered | Yes | Yes |
| The four constraints | Yes (guarded by this skill) | Yes |
| One-question-at-a-time rhythm | Yes | Yes |
| **Multi-perspective questioning** | Yes | **No — one side advancing, with self-challenge** |
| That method's other integrations | Yes | **No** |
