---
name: mvp-convergence-brainstorming-en
description: >-
  Converge the direction into an MVP resolution once the research outputs are read - answer
  eleven questions, adjudicate every research candidate value one by one, and carry every
  upstream open question forward without loss. Frozen topics (the locked architecture
  baseline, technology selection, already-rejected options) are guarded throughout, not
  reviewed at the end.
  Trigger keywords: MVP convergence / scope convergence / brainstorming convergence /
  what goes in the MVP / decide the scope / eleven questions / stage 2.
  Do not use for: reopening a locked architecture baseline, making technology choices
  (those belong to the planning stage), writing the PRD, or doing the research itself.
  Invoke it whenever the task involves settling what this project's first version contains,
  even if the user never says the word "skill".
license: MIT
allowed-tools: Read Write Edit
metadata:
  version: "1.0"
  lang: en
  kind: behavioural
  stage: "2"
  standalone: true
  produces:
    - "specs/research/07-mvp-convergence.md"
    - "specs/research/00-project-input-and-assumptions.md"
  requires:
    - name: "specs/research/00-project-input-and-assumptions.md"
      level: orchestration
      fallback: "Ask the user directly for what is already confirmed; with no ledger, treat everything as pending"
    - name: "specs/research/06-architecture-baseline.md"
      level: orchestration
      fallback: "Use the decision summary as the boundary; with neither, **declare explicitly that the frozen list is empty**"
    - name: "specs/research/05-decision-summary.md"
      level: orchestration
      fallback: "As above"
    - name: "specs/research/01-*.md through 04-*.md"
      level: optional
      fallback: "Mark the corresponding answers 'no research support'"
    - name: "external divergence method"
      level: optional
      fallback: "Run the built-in equivalent Socratic flow and label it as not having used an external method"
---

# MVP Convergence

## It is a constraint wrapper, not a new divergence method

General divergence and convergence methods are mature, and **this skill does not reinvent
them**. Its entire value is wrapping four classes of project-specific constraint around them.

Where an external divergence method is available, **delegate to it**; where it is not, run
the built-in equivalent.

**Delegating is not handing over the constraints** — this skill still guards all four:
clear the frozen topics before handing the discussion over, and on getting the result back,
reconcile the open-question count, adjudicate the candidate values, and add the premise
labels.

See `references/method-adapters.md` for detection, the delegation boundary, and the built-in
equivalent flow.

## The four classes of constraint

### 1. Frozen topics (guarded throughout, not reviewed afterwards)

**Three classes of topic are not reopened**:

| Frozen topic | Why |
|---|---|
| The locked architecture baseline | The previous stage locked it through an adversarial process at considerable cost. Reopening it here silently voids every position paper, red-team challenge and integration assessment |
| Technology selection (which framework or library) | It belongs to the later planning stage. Deciding it here pollutes that stage's decision space |
| Options already explicitly rejected | The reasons are recorded upstream; raising them again wastes that argument |

**The frozen check MUST run throughout convergence**, not as a final review.
By review time the architecture has already been re-discussed — the freeze was decorative.

#### What to do when you genuinely find a problem

Finding a real problem with an upstream conclusion **should be said**, but **how it is said
is prescribed**:

> Right: label it explicitly as a **proposal to overturn an upstream conclusion**, attach
> **new evidence**, and hand it to the user to adjudicate
> Wrong: reopen it inside the convergence as one more option on the table

The difference: the first lets the user know somebody wants to overturn the previous stage's
conclusion, and lets them refuse; the second **voids the adversarial selection's output
without the user knowing**.

See `references/scope-freeze-rules.md` for how to judge each frozen class, the refusal
phrasing, and the exception path.

### 2. Zero loss of open questions

Where upstream has N open questions, the convergence result MUST **still have N** (it may
grow, never shrink).

**"Convergence means reducing uncertainty" is not a reason to delete one.**
What converges is the **candidate values**, not the open questions. A question is open
precisely because it has no answer — convergence does not conjure one. Deleting it is not
convergence, it is pretending it does not exist.

Where one is judged obsolete, **label it explicitly as obsolete with the reason**; do not
remove it from the list.

### 3. Adjudicate every candidate value

Where the ledger holds M research candidate values, each MUST reach a definite conclusion:

```
Promoted to "user confirmed" (with the basis)  or  kept as an open question
```

**There are only these two exits, and no middle state.**
There is no such thing as a candidate that is neither confirmed nor listed as open — that is
silent adoption.

**High confidence does not mean it may be confirmed.** The two are orthogonal: high
confidence says "this inference is probably right", not "the user agrees".

See `references/inheritance-rules.md` for the inheritance and adjudication rules.

### 4. A conclusion MUST state the premises it rests on

Among the eleven answers, **any that depends on an unconfirmed premise MUST state that
premise explicitly**.

> A real lesson: this project's convergence conclusions were overturned twice by later work,
> and each time it was because **the premise the conclusion rested on had changed** — but at
> the time the conclusion looked exactly as settled as the others, and nobody knew it carried
> a condition. When the premise moved, nobody knew which conclusions had to move with it.

How to write it:

> "Must-have includes X — **premise**: Y is not yet confirmed; if Y does not hold, X should
> leave the MVP."

## The flow

```
1. Read upstream by priority; record what exists and what is missing
2. Build the frozen list (locked and rejected items from the architecture baseline and decision summary)
3. Build the inheritance list (every upstream open question, counted)
4. Build the to-converge list (every research candidate value, counted)
5. Run the eleven-question convergence - guarded throughout by the frozen list
6. Adjudicate each candidate: promote to confirmed (with the basis) or keep open
7. Merge the open questions: N inherited plus any new ones
8. Write back to the ledger; emit the convergence result
```

## The eleven questions

In four groups:

| Group | Questions |
|---|---|
| **Why / what / what not** | Business and product goals plus non-goals; primary and anti-persona; core user stories |
| **Functional decisions shaped by the architecture baseline** | The MVP feature list plus out-of-scope; the key boundary conditions of each core feature |
| **What counts as done well** | Non-functional requirements (in numbers); acceptance criteria; priorities; the north-star metric plus the abandonment line |
| **What is still uncertain** | Open questions (including every inherited one); product-level dependencies and constraints |

**Every question gets an answer.** Where the nature of the project makes one inapplicable,
label it "not applicable, with the reason"; do not leave it blank and do not force an answer.

See `references/11-questions.md` for the full definitions, what a good answer looks like, and
counter-examples.

## Upstream Artifacts

| Artifact | Level | When missing |
|---|:---:|---|
| Project input ledger | orchestration | Ask the user directly for what is confirmed |
| Architecture baseline decision | orchestration | Use the decision summary as the boundary |
| Decision summary | orchestration | With neither, **the frozen list is empty and that is declared explicitly** |
| Research files 01-04 | optional | Mark the corresponding answers "no research support" |
| External divergence method | optional | Built-in equivalent flow, labelled |

## Downstream Consumers

| Consumer | What it reads |
|---|---|
| The PRD writing skill | The eleven answers, as direct input to the PRD |
| The project context ledger | The status transitions and the change record |

## Standalone Use

**What you provide**: the project background and what you already know — say it or paste it.
Research outputs help; without them the eleven questions still run.

**What you get**: complete answers to the eleven questions, every candidate value
adjudicated, and a merged list of open questions. Of the four constraints, three — zero loss
of open questions, adjudicating every candidate, and labelling premises — **depend on nothing
upstream** and apply identically in standalone mode.

**What you don't get**:

- **No upstream means no frozen topics.** In that case I **declare explicitly that there is
  no upstream architecture baseline and nothing is locked this round** — rather than
  pretending there is a constraint, or quietly dropping it. You need to know this round's
  convergence has no boundary guarding it.
- **It does not do the research for you.** Questions with no research behind them are
  answered and labelled "no research support".
- **It does not write the PRD, adjudicate architecture, or make technology choices.**

## Anti-patterns

- Reopening a locked architecture baseline during convergence
- Using "I found a real problem" to bypass the overturn procedure
- Deleting open questions on the grounds that "convergence reduces uncertainty"
- Writing a high-confidence candidate straight into the MVP feature list
- Letting a low-confidence candidate disappear silently
- Output that does not distinguish what the user confirmed from what research inferred
- Making technology choices in passing
- A conclusion resting on an unconfirmed premise without stating that premise
- Pretending there is frozen-topic guarding in standalone mode
