# Anti-Bias Hard Constraints and Academic Justification

> The greatest threat to a multi-agent debate framework is "looking like a debate while actually conforming." This document consolidates anti-bias hard constraints along with supporting academic literature.

---

## I. 6 Anti-Bias Hard Constraints (Must Be Followed)

| # | Constraint | What Bias It Counters | Academic Basis |
|---|------------|-----------------------|----------------|
| 1 | Every paper must include a "Fatal Flaw Disclosure" | Self-advocacy bias | D3 SAMRE / Anthropic Constitutional AI |
| 2 | Phase 2 papers submitted in randomly shuffled order | Positional bias | LLM-as-Judge survey 2024-2026 |
| 3 | Each challenge response ≤ 200 words | Length bias | LLM-as-Judge survey |
| 4 | Lead prohibited from expressing opinions in Phase 2 | Authority bias | MAD-M² ICLR 2026 |
| 5 | Phase 1 prohibits teammates from communicating with each other | Anchoring bias | Claude Code Agent Teams official documentation |
| 6 | Red Team / Advocate positions are fixed and cannot switch sides | Conformity bias | Nature 2026 "When collaboration fails" |

---

## II. Detailed Explanation of 6 Biases

### Bias 1: Self-Advocacy Bias

**Symptom**: Advocates naturally tend to emphasize a project's strengths while downplaying its weaknesses.

**Why it happens**: After being assigned the role of "arguing for X," an LLM enters "lawyer mode" and instinctively suppresses counter-evidence.

**Damage to decision-making**: All Advocates say "my project is the best," leaving the Lead with no negative information to weigh.

**Constraint 1: Fatal Flaw Disclosure (mandatory self-attack)**

The logic behind making Advocates **self-report** flaws:
- Fatal Flaw Disclosure is designed as a mandatory field in the paper; its absence is treated as negligence
- Self-reporting is always better than being exposed by the opposition — at least you control the narrative
- Mandatory self-attack is an extension of the "self-criticism" mechanism in Constitutional AI

Implementation details:
- Must list 3 flaws (not 0, not "no significant flaws found")
- Each flaw must have verifiable evidence (source code line / commit / issue)
- The severity of the flaws cannot all be trivial — the Lead Judge will see through it

**Academic basis**:
- D3 Framework (arXiv 2410.04663) SAMRE protocol requires each advocate to self-revise (self-critique) in round N
- Anthropic Constitutional AI (arXiv 2212.08073) uses a "critique → revise" loop to make LLMs self-correct

---

### Bias 2: Positional Bias

**Symptom**: Evaluators (Lead or teammates) tend to favor the **first-presented** option.

**Why it happens**: Attention decay + primacy effect in working memory. The first paper occupies the "head of context" when an LLM evaluates, making it most memorable.

**Damage to decision-making**: Two papers of equal quality, but the one seen first gets unconsciously overrated.

**Constraint 2: Phase 2 papers submitted in randomly shuffled order**

Implementation details:
- Lead calls a pseudo-random algorithm to shuffle paper order before Phase 2 begins
- The shuffled order is recorded in an internal log (for post-audit traceability)
- When broadcasting to all teammates, use the shuffled order — **not** the Phase 1 completion order, not alphabetical order

Advanced approach (for future consideration):
- The same paper could appear in different positions in different teammates' mailboxes (per-teammate shuffling)
- But implementation complexity is high; this Skill uses global shuffling for now

**Academic basis**:
- "Judging LLM-as-a-Judge" (arXiv 2306.05685) explicitly reports positional bias can reach 30%+
- LLM-as-Judge survey recommends "balanced prompt ordering"

---

### Bias 3: Length Bias

**Symptom**: Evaluators prefer **longer** arguments, even when content quality is equal.

**Why it happens**: Long = detailed = effort = more credible — a human bias that LLMs have learned.

**Damage to decision-making**: Advocates who can write at length have an inherent advantage; argument quality is overwhelmed by word count.

**Constraint 3: Each challenge response ≤ 200 words**

Implementation details:
- 200-word hard cap; responses exceeding this are treated as "violations"
- Lead detects over-length responses and asks the teammate to rewrite
- 200 words is enough to make one point clearly without padding

Why 200 words and not 300/500:
- D3 SAMRE protocol recommends ≤ 250 tokens per item (approximately 150 Chinese characters + 50 English)
- 200 words is slightly more generous, allowing for English expression
- Testing shows 200 words is sufficient to clearly convey 1-2 core counter-arguments

**Academic basis**:
- LLM-as-Judge survey (arXiv 2308.10142) reports length bias exists in most judge LLMs
- Recommends "length-normalized scoring" — this Skill uses the simpler "hard cap" approach

---

### Bias 4: Authority Bias

**Symptom**: After the Lead (the "authority") expresses an opinion, teammates tend to conform.

**Why it happens**: LLMs trained with RLHF tend to please the "authoritative instruction issuer."

**Damage to decision-making**: Debate becomes "guessing what the Lead wants," and independence is lost.

**Constraint 4: Lead prohibited from expressing opinions in Phase 2**

Implementation details:
- Lead **only coordinates, does not evaluate** during Phase 2
- Allowed Lead behaviors: broadcasting papers, relaying challenges, prompting "there are still N challenges without a response," announcing the next round
- Prohibited Lead behaviors: saying "Advocate A's argument is more reasonable," saying "I think project X is better," implying a preference (e.g., "Project Y looks pretty reliable?")

If Lead accidentally expresses an opinion:
- In Phase 3 synthesis, **downweight** arguments in that direction
- **Disclose** the Lead's Phase 2 opinion record in the 06 decision document

**Academic basis**:
- MAD-M² (ICLR 2026) memory masking mechanism is specifically designed to eliminate "authority priors"
- LLM-as-Judge best practice: "judge should not produce evidence, only evaluate"

---

### Bias 5: Anchoring Bias

**Symptom**: After one teammate publicly takes a position, other teammates' positions "converge toward the first one."

**Why it happens**: Instinct for human collaboration + "polite compromise" patterns learned by LLMs.

**Damage to decision-making**: Debate becomes "the first paper determines the outcome," and diverse perspectives are lost.

**Constraint 5: Phase 1 prohibits teammates from communicating with each other**

Implementation details:
- Mailbox is silent during Phase 1 — no teammate may send messages to others
- Lead monitors mailbox traffic; if inter-teammate communication is detected during Phase 1, immediately stop
- Every teammate must independently complete their own paper / position / assessment

Why not just prohibit "reading each other's papers":
- Even without reading papers, inter-communication leaks positions (e.g., "I don't think X will work" influences others)
- Complete silence is the cleanest approach

**Academic basis**:
- Claude Code Agent Teams official documentation states: "With multiple independent investigators actively trying to disprove each other, the theory that survives is much more likely to be the actual root cause."
- Independence is the prerequisite for the value of debate

---

### Bias 6: Conformity Bias ⚠️ Most Dangerous

**Symptom**: In multi-round debates, minority-position teammates tend to "abandon their position and join the majority."

**Why it happens**: LLMs' learned "harmony" patterns + the weight of "frequently appearing viewpoints" increases in long contexts.

**Damage to decision-making**: Debate ultimately converges to a "everyone is happy" solution, and true adversarial challenge fails.

**Constraint 6: Red Team / Advocate positions are fixed and cannot switch sides**

Implementation details:
- Red Team's spawn prompt explicitly states "prohibited from saying 'project X is actually pretty good'"
- Advocate spawn prompt states "do not yield unless the Lead Judge rules"
- Advocates cannot proactively abandon any paper they own in Phase 2 (may acknowledge partial challenges, but cannot withdraw the entire paper)
- The desire to switch sides is not expressed in Phase 2; it can be referenced by Lead in Phase 3 synthesis (Advocates express this by ultimately acknowledging some challenges)

**Academic basis**:
- Nature 2026 "When collaboration fails: persuasion driven adversarial influence in multi-agent LLM debate" directly reports conformity failure patterns
- Counter-measures: role lock-in + explicit anti-conformity instruction

---

## III. Other Common Biases (Already Mitigated by Default)

| Bias | Mitigation Method |
|------|-------------------|
| Self-preference | Lead is not a converted Advocate; teammates have independent contexts |
| Verbosity bias | 200-word hard cap + Phase 2 challenges must include evidence |
| Sycophancy | Red Team / Advocate positions are locked |
| Recency bias | In Phase 3 synthesis, Lead must **re-read** Phase 1 papers, not just Phase 2 transcripts |
| Overconfidence | Fatal Flaw Disclosure is mandatory; Open Questions must have at least 3 |

---

## IV. Lead Judge Self-Check Checklist

Before writing the decision in Phase 3, Lead must self-check:

```
□ Did I express any opinions in Phase 2? (If yes, downweight related arguments)
□ Do all papers include a Fatal Flaw Disclosure? (Papers missing it have discounted credibility)
□ Is my verdict based on "which one is longer"? (If yes, re-evaluate)
□ Is my verdict based on "my personal preference"? (If yes, go back and find objective evidence)
□ Are there at least 3 Open Questions? (Fewer than 3 indicates excessive confidence in the verdict)
□ Do the reasons for rejected options cite specific line numbers from the debate-transcript? (Cannot rely on impressions)
□ Does the overall verdict reflect a 7-dimension comprehensive weighing, not just Dimension 5 cost?
```

Any item that fails → go back and rewrite the decision.

---

## V. Academic References

1. **D3 Framework** — Debate, Deliberate, Decide: A Cost-Aware Adversarial Framework for Reliable and Interpretable LLM Evaluation. arXiv 2410.04663
2. **MAD-M²** — Multi-Agent Debate with Memory Masking. ICLR 2026
3. **When Collaboration Fails** — Persuasion driven adversarial influence in multi-agent LLM debate. Nature Scientific Reports 2026
4. **Judging LLM-as-a-Judge** — arXiv 2306.05685
5. **LLM-as-Judge Survey** — arXiv 2308.10142
6. **Anthropic Constitutional AI** — arXiv 2212.08073
7. **Claude Code Agent Teams** official documentation https://code.claude.com/docs/en/agent-teams.md
8. **Courtroom-Style Multi-Agent Debate (AgentCourt)** — arXiv 2603.28488
9. **MAD: Should we be going MAD? A Look at Multi-Agent Debate Strategies for LLMs** — arXiv 2311.17371
10. **Improving factuality and reasoning in language models through multiagent debate** — ICML 2024
