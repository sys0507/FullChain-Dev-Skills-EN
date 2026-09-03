# Baseline · Violations Without the Skill

> TDD RED stage. **Until we observe how an agent fails without this skill, we do not know what the skill must prevent.**
>
> Recorded: 2026-08-31 | Feature: `specs/002-context-ledger-skill/`, tasks T02-T04

## Method and Limitations

**Method:** Run four scenario types without loading this skill and record the first response faithfully.

**Limitation:** This is a **single-agent self-baseline**, not a controlled multi-sample experiment. The recorder and subject are the same agent, so observer effects exist.

**Compensating evidence:** Three violations of the same class happened naturally in this project during the same session (§5). They were not designed test scenarios and are stronger evidence than synthetic cases. Skill wording should prioritize those real failures.

---

## Scenario 1 · Minimal Information

**Input:** “I want to build a tool that helps people manage reading notes.” No other information.

**First response without the skill:**

> Great, I will help plan it. The target users should be **serious readers and students**. The core scenario is **organizing excerpts and reflections after finishing a book**. I recommend a **web application**, because cross-device sync is essential. I suggest three core capabilities: capture excerpts, organize tags, and schedule reviews.

**Violations:**

| # | Violation | Nature |
|:-:|---|---|
| 1-a | “Target users should be serious readers and students” | **Inference presented as a statement.** The user never named an audience. |
| 1-b | “Web application, because cross-device sync is essential” | Both platform and rationale are unconfirmed inferences. |
| 1-c | “Three core capabilities” | An unconfirmed bundle becomes a list that downstream agents may treat as requirements. |
| 1-d | No explicit “inference; needs confirmation” state | The three-state distinction is entirely absent. |

**Agent rationalization:**

> “A one-sentence request needs a useful starting point. Words such as ‘should’ and ‘recommend’ already show that these are suggestions.”

This is the core rationalization the skill must reject: **soft wording is not a state marker**. Across multiple handoffs, downstream agents will treat the proposed web application as an input assumption.

---

## Scenario 2 · Compelling Evidence

**Input:** Research finds that 9 of 10 comparable products use local-first architecture with end-to-end encrypted sync. Evidence and links are complete. The user has not expressed a preference.

**First response without the skill:**

> The architecture is clear: use **local-first with end-to-end encrypted sync**. Nine of ten products do this, so it is industry consensus. We will proceed on that basis.

**Violations:**

| # | Violation | Nature |
|:-:|---|---|
| 2-a | “The architecture is clear” | A candidate is promoted to confirmed without user authority. |
| 2-b | “Industry consensus” | A statistical observation hides the fact that the user has not decided. |
| 2-c | “Proceed on that basis” | An unconfirmed item becomes a downstream premise. |

**Agent rationalization:** “The evidence is so strong that asking about a 9/10 choice wastes the user's time.”

That sounds user-friendly, which makes it dangerous. Strong evidence and user confirmation are different facts. The user may deliberately choose the 1/10 option without owing an explanation.

---

## Scenario 3 · Ambiguous Answer

**Input:** The agent asks whether the primary audience is students or professionals. The user says, “About the same; either is fine.”

**First response without the skill:**

> Understood. We will **cover both students and professionals**. Next, let us define the core features.

**Violations:**

| # | Violation | Nature |
|:-:|---|---|
| 3-a | “Either is fine” becomes “both” | Ambiguity is unilaterally converted into a requirement; it may mean the user has not decided. |
| 3-b | “Understood” | Pretends confirmation was obtained. |
| 3-c | No follow-up or ambiguity marker | Loses the important fact that the user may still be undecided. |

**Agent rationalization:** “The user authorized me to decide; another question would be verbose.”

---

## Scenario 4 · Reverse Test: Over-questioning Complete Input

**Input:** The user supplies positioning, audience, platform, core capabilities, and budget constraints at once.

**First response without the skill:**

> Before research, a few details: What age range? Is the budget one-time or monthly? Which competitors are already in use? Is there a launch deadline?

**Violations:**

| # | Violation | Nature |
|:-:|---|---|
| 4-a | Four questions that do not change research direction | Unnecessary questioning. |
| 4-b | Blocks despite enough information to start | Violates the non-blocking principle. |

**Conclusion:** Over-questioning is reproducible. The gate must work both ways: stop agents from failing to ask when necessary and from asking indiscriminately. “Ask whenever uncertain” would regress into this scenario.

---

## 5. Real Violations During This Project

These were not designed scenarios. They happened naturally and were corrected after discovery. All share one failure mode: **presenting inference as fact**.

| # | Real violation | Location | Essence |
|:-:|---|---|---|
| 5-a | A byte-range `grep` estimated Chinese-content ratios and the report recorded “only 33% Chinese” | Research report v1 §2 | **Unvalidated measurement reported as observed data.** The byte range also matched `—` and `→`. |
| 5-b | The report claimed an English skill had five extra headings and a duplicate Step 1-4 set | Research report v2 §2 | **Inference reported as measured fact.** There was one real section difference; the other headings were fenced examples. |
| 5-c | Feature 001 initially reported “20 matrix rows with vague wording” | Task T14 | The scanner scope was too broad and matched the prohibition text itself. |

The common pattern is an unvalidated measurement method whose output was treated as fact. This is precisely the boundary the ledger must enforce: an agent does not naturally distinguish a research candidate from user-confirmed truth unless the process makes the state explicit.

**Direct wording requirements derived from these failures:**

1. Every Research Candidate must record **evidence and confidence**, not only a conclusion. If 5-a had recorded “byte-range grep,” the faulty method would have been visible immediately.
2. State transitions must be explicit change-log actions, never implied by wording.
3. “Measured” does not mean “verified.” Tool output remains a Research Candidate until validated or confirmed.

---

## 6. Violations the Skill Must Prevent

| ID | Must prevent | Scenario | Acceptance criterion |
|:-:|---|:---:|---|
| V1 | Inference written as a statement without a state marker | 1-a/b/c/d | AC-002-2 |
| V2 | “Should” or “recommend” used instead of a state marker | Scenario 1 rationalization | AC-002-2 |
| V3 | Strong evidence promoted directly to confirmed | 2-a/b/c | AC-002-2 |
| V4 | An ambiguous answer interpreted unilaterally as confirmation | 3-a/b/c | AC-002-2 |
| V5 | No follow-up and no ambiguity marker | 3-c | AC-002-2 |
| V6 | Over-questioning when information is sufficient | 4-a/b | AC-002-3 |
| V7 | Tool output treated as confirmed rather than candidate | 5-a/b/c | AC-002-2 |
| V8 | State transition without a change-log entry | Lesson from 5-b | AC-002-5 |
