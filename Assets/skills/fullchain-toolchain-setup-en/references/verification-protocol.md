# Verification and failure recording

## When to read this

When verifying after installation, and when a failure needs recording.

---

## Verification signals

The observable criteria for "verified as triggerable":

| Layer | Signal | Strength |
|:-:|---|---|
| 1 | The skill's directory structure is complete (`SKILL.md` exists and its frontmatter parses) | Weak - it only proves the files are right |
| 2 | The skill appears in the tool's available list | **Medium - the most practical signal** |
| 3 | A typical trigger phrase actually reaches the skill | Strong - but it really runs it, which is expensive |

**Use layer 2 by default.** It proves the tool genuinely recognises the skill, without
triggering a full execution just to verify.

Layer 3 is used only when the user explicitly asks for "verified to the point of running".

**Nothing below layer 2 may be written as "verified"** — files in the right place is not the
same as the tool knowing about them.

---

## Report format

The install report has five columns:

| Column | What goes in it |
|---|---|
| Skill name | The directory name |
| Source path | Where it was copied from |
| Install location | Where it landed |
| Verification result | Which signal layer was reached; on failure, the reason |
| How to trigger | How the user invokes it |

---

## Failure recording

**MUST NOT fake success.**

| Situation | What to record |
|---|---|
| Source does not exist | The missing item + **which stage it affects** + whether it blocks |
| Language mismatch | Requested language versus actual + why installation was refused |
| Same-name conflict | A summary of the difference + awaiting the user's ruling |
| Verification failed | Which layer was reached + where it stopped |
| Failure partway through installation | **What was already installed successfully** + the break point + what remains |

### A failure partway through does not roll back

What is already installed **stays**, and the report states the break point and what remains.

Rollback carries more risk than benefit: it may delete a same-named skill the user already
had, or destroy a half-installed but still usable state.

---

## "Not applicable" is recorded too

When something is judged not applicable, write **the specific reason**.

| Bad | Good |
|---|---|
| (it vanishes from the report) | "Browser testing tool - this project has no web surface, not applicable" |
| "Not configured" | "Parallel agents - the current tool does not support them, not applicable" |

Reason: without a stated reason people ask the same question repeatedly, and there is no way
to tell "judged unnecessary" from "forgotten".

---

## The report's three closing sections

The report MUST end with:

1. **The ready list** — what can be used right away
2. **The failed and not-applicable list** — each with its reason and impact
3. **The pending list** — the specific questions needing the user's decision

Section 3 is the user's action list. It should be short, specific and directly answerable —
not unactionable advice like "please check the configuration".
