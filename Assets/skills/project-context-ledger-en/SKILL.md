---
name: project-context-ledger-en
description: >-
  Maintain the project's three-state context ledger: record and treat separately
  what the user confirmed in their own words, what research derived as a candidate,
  and what is still unknown, then keep it updated across every stage of the
  full-chain workflow. A single sentence of an idea is enough to start; no complete
  variable table is required up front. Trigger keywords: project input ledger /
  context ledger / confirmed or candidate / record project assumptions / did the
  user say this or did you infer it / project variable completion / open items list
  / starting a new project with very little information / write my idea down.
  Do not use for: dispatching parallel research (that is the research kickoff
  Skill), producing research file content, architecture selection rulings, MVP
  convergence, or writing a PRD. Even if the user never says "use a Skill", invoke
  it whenever the task involves separating what the user confirmed from what was
  inferred.
license: MIT
allowed-tools: Read Write Edit
metadata:
  version: "1.0"
  lang: en
  stage: "*"
  standalone: true
  produces:
    - "specs/research/00-project-input-and-assumptions.md"
  requires:
    - name: "The user's project idea"
      level: required
    - name: "specs/research/00-project-input-and-assumptions.md"
      level: orchestration
      fallback: "create it if it does not exist; never refuse to work because the file is missing, but the change log starts empty so no earlier state history is recoverable"
    - name: "Research artifacts from the other stages"
      level: orchestration
      fallback: "ask the user to supply them directly; with none, the candidate section stays empty and MUST be explicitly labelled 'no research artifacts connected', so nothing in it is backed by research evidence"
---

# Project Context Ledger

## What This Skill Solves

The most hidden and most expensive error in the full chain: **treating an inference
as a user requirement**. Once a candidate is treated as confirmed, the PRD, the spec
and the code that follow are all built on a false premise, and nobody notices --
because it reads exactly like a real requirement.

The value of this Skill is **not in doing more**. It is in **stopping when it should
stop and labelling when it should label**.

## The Three States

| State | Test | Usable as a basis for decisions |
|---|---|:---:|
| **User confirmed** | Traceable to the user's own words or an explicit approval | Yes -- may be written as a settled requirement |
| **Research candidate** | Derived from research or tool output, with evidence and confidence attached | Only as a conditional comparison of options |
| **Open item** | Current evidence is insufficient | Only as an Open Question |

**There is no fourth state.** Every piece of information MUST land in one of these
three cells. Nothing may be left floating.

## Iron Rules (Written Against Real Observed Violations)

### 1. "Suggest" and "Should" Are Not State Markers

Wrong: "The target users **should be** deep readers." That reads like a conclusion,
and downstream will consume it as a requirement.
Right: put it in the ledger's **research candidate** block, with evidence and
confidence.

Soft wording is lost as it is passed along. **State MUST be expressed by which block
of the ledger the item sits in, never by tone.**

### 2. No Amount of Evidence Equals User Confirmation

Nine out of ten comparable products do it this way -- that is a **very strong
candidate**, not a confirmation. The user may be exactly the one in ten, and they
have the right to be that one in ten without explaining why.

Wrong: "The architecture direction is already clear."
Right: "Candidate: local-first architecture | Evidence: 9 of 10 comparable products
adopt it (links attached) | Confidence: high | Awaiting user confirmation."

### 3. A Vague Answer MUST NOT Be Read One Way

The user says "roughly, yeah / either is fine / your call" -- **that is not a
confirmation**.

"Either is fine" carries at least three meanings: both really are acceptable / I
have not thought it through / I do not want to discuss this now. Defaulting to the
first reading throws away the important fact that the user has not thought it
through.

Right: record it as an **open item**, flag the ambiguity, and follow up once if
needed.

### 4. Tool Output Is Also a Candidate, Not a Confirmation

**The measurement itself may be wrong.** This project has been bitten twice already:
a byte-range `grep` distorted a character-ratio statistic, and an over-broad checker
scope produced a false report of structural drift.

Conclusions from scans, statistics and searches all go into **research candidates**,
and MUST state the measurement method -- write the method down and the flaw becomes
visible on the spot.

### 5. Every State Transition MUST Leave a Trace

Candidate to confirmed happens **only through an explicit change-log entry**, and
that entry MUST carry its basis (the user's own words or a file path). A promotion
with no change-log entry is invalid.

## Question Gate (Two-Directional)

**This gate runs in both directions.** Writing only "ask the user when unsure"
degrades this Skill into interrupting at every step -- the baseline reproduced
exactly that tendency.

**Ask immediately if and only if** any one of the following holds:

1. The gap would make the **research direction entirely different** (not "more
   precise" -- a different road)
2. The answer needs the user's **authorisation or private information** (accounts,
   hard budget ceilings, internal material)
3. Continuing would **waste substantial effort** and be hard to reverse

**Otherwise record it as an open item and continue.** In particular, do not ask
about:

- Details whose answer would not change this round's search strategy
- Questions a later stage will converge anyway (leave them to MVP convergence)
- "Let me just double-check" when the user has already given enough

See `references/question-gating.md` for the three criteria expanded, worked positive
and negative examples, and the decision tree.

## Workflow

```
1. Decide the mode: ledger file exists -> chained; absent -> standalone
2. Classify each item into one of the three states
3. Key variable missing -> temporary codename / broad assumption, do not block
4. Pass the question gate: stop if it qualifies, else record an open item and go on
5. Write to the ledger (append and update; preserve existing content and change log)
6. Report three summaries: newly confirmed / newly candidate / still undecided
```

See `references/ledger-schema.md` for the ledger file structure, the candidate table
columns and the change-log format.
See `references/bootstrap-heuristics.md` for temporary codenames, broad research
assumptions and search keyword extraction.

## One Sentence Is Enough to Start

A single sentence from the user is a **normal starting point, not insufficient
information**.

- Project name undecided -> generate a temporary codename, marked "renameable"
- Positioning undecided -> write a broad research assumption, marked "bounds this
  round's search only; does not represent user confirmation"
- Users, platform, capabilities undecided -> fold them into later research,
  **do not lock them early**

You MUST NOT require the user to complete the variable table before starting.

## Search Keyword Rules

**An unfilled placeholder MUST NOT be used verbatim as a search term.**

Extract neutral keywords from the user's own words, search from broad to narrow, and
keep a record of **how the search converged**.

## Upstream Artifacts

| Artifact | Level | What happens when it is missing |
|---|:---:|---|
| The user's project idea | **required** | Stop and ask -- with no idea there is nothing to open a ledger on |
| `specs/research/00-project-input-and-assumptions.md` | orchestration | Create it; the change log starts empty, so no earlier state history is recoverable |
| Research artifacts from the other stages | orchestration | Ask the user to supply them; with none, the candidate section stays empty and is labelled "no research artifacts connected", so no candidate is backed by research evidence |

## Downstream Consumers

| Consumer | What it takes from this Skill |
|---|---|
| MVP convergence Skill | All three states; it adjudicates every candidate one by one |
| PRD writing Skill | Only "user confirmed" items may become settled requirements |
| Learnings retrospective Skill | The change log (which judgements were later overturned) |

## Standalone Use

**What you provide**: one sentence of a project idea is enough. If you already have
research conclusions, competitor notes or meeting minutes, paste them in and I will
classify them item by item into the three states. Without them you can still start.

**What you get**: a maintainable three-state ledger file carrying evidence,
confidence and a change log, plus a per-round summary of "newly confirmed / newly
candidate / still undecided". The three-state test, the question gate, and
temporary-codename and broad-assumption generation all work without any other Skill.

**What you don't get**:

- **I will not do the research for you.** This Skill only records and classifies; it
  does not dispatch parallel searches and does not produce research file content.
  For research, use the research kickoff Skill; in standalone mode the candidate
  block is labelled "no research artifacts connected".
- **I will not decide for you.** A candidate is never promoted just because the
  evidence is strong -- that takes your confirmation.
- **No PRD, no MVP convergence, no architecture ruling.**

## Anti-Patterns

- Using "suggest / should / it looks like" in place of a state marker
- Writing a candidate into "user confirmed" because the evidence is sufficient
- Treating "either is fine" as authorisation
- Treating scan or statistics output as confirmed fact, with no measurement method
- Promoting a state without writing a change-log entry
- Re-confirming repeatedly when the information is already sufficient
- Refusing to start because the variable table is incomplete
- Using an unfilled placeholder as a search keyword
