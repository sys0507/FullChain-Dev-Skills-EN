# The eleven questions

## When to read this

Work through it question by question while converging.

**Every question gets an answer.** Where the nature of the project makes one inapplicable,
label it "not applicable, with the reason"; do not leave it blank and do not force an answer.

---

## Group 1: why / what / what not (pure product decisions)

### Q1 Business goals + product goals + non-goals

| Good | Bad |
|---|---|
| Goals are verifiable; **non-goals are listed explicitly** | Goals with no non-goals — the scope will certainly grow |
| "A user completes one entry within three minutes" | "Improve the user experience" |

**Non-goals are the point of this question.** Without them, every later question drifts.

### Q2 Primary persona + anti-persona

| Good | Bad |
|---|---|
| One or two primary personas, each with a context, a pain point and a definition of success | "Anyone who needs X" |
| **The anti-persona explicitly states who is not served** | Only stating who is served |

What the anti-persona is for: it blocks scope growth better than the primary persona does.

### Q3 Three to five core user stories

INVEST format: as a <role>, I want <capability>, so that <value>.

**The "so that" MUST NOT be dropped** — without it there is no way to judge whether the story
should be built.

---

## Group 2: functional decisions shaped by the architecture baseline

### Q4 MVP feature list + out-of-scope

**Must-haves favour capabilities with a low reuse cost.**

| Criterion | Handling |
|---|---|
| Marked "reuse directly" in the upstream reuse matrix | Prefer including it in the MVP — it is nearly free |
| Needs building from scratch | **Include with caution**, unless it is the core value itself |
| A capability implicated in an upstream position paper's self-declared fatal flaw | Consider putting it out of scope first |

This question **most easily touches a frozen topic**. Discussing which features enter the MVP
slides very easily into "then we may as well change the architecture" — that is frozen; take
the overturn path.

### Q5 Key boundary conditions for each core feature

What happens on missing data, on concurrency, on failure.

**Boundaries MUST fall within what the confirmed architecture baseline can support** —
writing a boundary the baseline cannot deliver plants a landmine for implementation.

---

## Group 3: what counts as done well

### Q6 Non-functional requirements (**numbers are mandatory**)

| Good | Bad |
|---|---|
| "First screen within 2 seconds" | "It should respond quickly" |
| "For a single file of 100,000 lines or more, produce a result or an explicit refusal within 30 seconds" | "Supports large files" |

**Performance ceilings MUST reference what the confirmed architecture baseline can actually
do**; do not promise from thin air.

### Q7 Acceptance criteria for each user story

Given / When / Then, **machine-verifiable**.

### Q8 Priorities (MoSCoW)

Must / Should / Could / Won't.

**Order with reference to the cost of change**: lower cost means higher priority.

**Self-check**: are the priority labels consistent with the delivery scope stated later?
This project's PRD once contained the contradiction "the priority table says Should, but the
MVP deliverables list includes it", and it went unnoticed until the tenth spec.

### Q9 North-star metric + abandonment line

| Item | Requirement |
|---|---|
| North-star metric | One, measurable, directly related to the business goal |
| Abandonment line | Under what circumstances we should stop and re-evaluate |

**The abandonment line MUST account for the confirmed architecture baseline's scaling ceiling.**

---

## Group 4: what is still uncertain

### Q10 Open questions

**MUST contain every one inherited from upstream** (see `inheritance-rules.md`); new ones may
be added.

At least three. **Having none means the convergence was shallow** — no convergence ever
resolves all uncertainty.

### Q11 Dependencies and constraints (product level)

External interfaces, compliance approvals, platform policies.

**Do not repeat the technical dependencies upstream already settled** — those belong to the
architecture baseline.

---

## Common failure patterns

| Pattern | Why it fails |
|---|---|
| The answer is a pile of adjectives | Unverifiable |
| The answer depends on an unconfirmed premise **without stating that premise** | When the premise moves, nobody knows what must be redone |
| "It depends" | The same as not answering |
| Writing a candidate value as confirmed | Silent adoption |
| Leaving a question blank | Even "not applicable" needs "not applicable, with the reason" |

---

## Self-check before convergence ends

```
[ ] All eleven questions answered (including any "not applicable, with the reason")
[ ] Both non-goals and out-of-scope are written
[ ] Every non-functional requirement has a number
[ ] The priority labels are consistent with the delivery scope
[ ] The open-question count is at least the number inherited from upstream
[ ] All M candidate values have an adjudication
[ ] Every conclusion resting on an unconfirmed premise states that premise
[ ] No frozen topic was touched at any point
```
