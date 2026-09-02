# Ledger File Structure

## When to read this file

Read it when you need the exact block structure, the table column definitions or the
change-log format. For day-to-day three-state classification, `SKILL.md` is enough.

---

## 1. Overall file structure

```markdown
# Project Input and Assumptions

## User Confirmed
## Research Candidates
## Open Items
## Change Log
```

Four blocks, **fixed order, headings fixed verbatim**. The order is the priority: the
reader sees what is settled before what is not.

---

## 2. The "User Confirmed" block

Every entry MUST be traceable to the user's own words or an explicit approval.

```markdown
## User Confirmed

- **PROJECT_IDEA**: <the user's own words; changing their meaning is forbidden>
- **TARGET_PLATFORM**: CLI tool (user answered on 2026-08-31: "just make it command line")
```

**Format requirements**:

| Requirement | Note |
|---|---|
| Bold the variable name | So downstream can search by name |
| Keep the user's words **verbatim** | No "polishing" -- polishing shifts the semantic boundary |
| A confirmation that is not a direct quote MUST cite its source | For example: user answered on <date>: "..." |

**Forbidden**: treating the Agent's paraphrase as the user's words. If the user said
"a little tool", it MUST NOT be recorded as "a lightweight CLI application".

---

## 3. The "Research Candidates" block

A five-column table. **Evidence and confidence are mandatory columns**, not optional
commentary.

```markdown
## Research Candidates

| Variable | Candidate | Evidence | Confidence | Awaiting user confirmation |
|------|--------|------|--------|------------|
| TARGET_USERS | Deep readers + students | 8 of 10 comparable products target these two groups (links attached) | High | Yes |
| Storage approach | Local-first | 9 of 10 comparable products adopt it; method: manual reading of product sites | Medium | Yes |
```

### 3.1 What the "Evidence" column must contain

| Evidence type | Must include |
|---|---|
| From a search | Link / product name / search date |
| From tool output | **The measurement method** (which command, which scope) |
| From reasoning | The key step of the reasoning chain -- "obviously" is not enough |

> **Why tool output MUST state its method**: this project has had two distorted
> measurements -- a byte-range `grep` counted `--` and `->` as in-range characters,
> and a full-text checker scan matched the text of the prohibition itself.
> **Write the method down and the flaw is exposed on the spot**; write only the
> conclusion and it propagates all the way down.

### 3.2 Three confidence levels

| Level | Test |
|---|---|
| High | Several independent sources agree, and the sources are authoritative (official docs, source code, official pricing) |
| Medium | A single source, or several sources that are all second-hand |
| Low | Mostly reasoning, with no direct evidence |

**High confidence does not license promotion to confirmed.** The two are orthogonal:
high confidence only says "this inference is probably right"; it does not say "the
user agrees".

### 3.3 Several candidates for one variable

List them all, one row each, and **do not pick one yourself**:

```markdown
| Storage approach | Local-first | 9 of 10 comparable products adopt it | High | Yes (one of two, see below) |
| Storage approach | Cloud sync | Easier to operate at large user counts | Medium | Yes (one of two, see above) |
```

Hand the choice to the user at the decision gate. **When evidence conflicts, record
both side by side; do not force them into agreement.**

---

## 4. The "Open Items" block

```markdown
## Open Items

- Are the target users students or working professionals? (User answered "either is fine" on 2026-08-31 -- ambiguous, needs a follow-up)
- Is there a hard budget ceiling? (Private information; the user must volunteer it)
```

**Record only questions that currently cannot be answered reliably.** Anything
research can already turn into a candidate belongs in "Research Candidates" instead
of piling up here -- **this block is not a to-do list**.

A vague answer MUST have **the ambiguity flagged**, not just the question restated.

---

## 5. The "Change Log" block

**The only legitimate evidence of a state transition.** A promotion with no
change-log entry is invalid.

```markdown
## Change Log

- 2026-08-31: TARGET_PLATFORM promoted from research candidate to user confirmed,
  basis: user answered "just make it command line"
- 2026-08-31: Storage approach demoted from user confirmed back to open item,
  basis: user introduced a new constraint (must work offline); the earlier confirmation lapsed
```

**Three mandatory fields**: date, variable plus direction of the transition, basis.

### 5.1 Legitimate forms of a basis

| Legitimate | Not legitimate |
|---|---|
| A quote of the user's own words | "The user probably agrees" |
| A file path plus section | "The research supports this conclusion" |
| A description of the user's confirming action (for example "user chose A between options A and B") | "The evidence is sufficient" |

### 5.2 Demotions are logged too

When the user overturns a confirmed item, **the old value moves into the change log**,
the new value goes into the confirmed block, and the reason for the change is stated.
You MUST NOT rewrite the confirmed block without leaving a trace -- that permanently
loses "when did the user change their mind".

---

## 6. Handling an existing file

| Situation | Handling |
|---|---|
| The file already exists | **Append and update**; preserve all existing content and change-log entries |
| It contains user-written passages | Keep them verbatim; do not reorder, do not rewrite |
| Its format does not match this schema | Do not reorder existing content; write new entries per this schema and flag the format difference |
| One of the four blocks is missing | Add the missing block; leave the existing ones untouched |

**Never overwrite the file wholesale.**
