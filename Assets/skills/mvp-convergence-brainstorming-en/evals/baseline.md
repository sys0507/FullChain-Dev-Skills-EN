# Baseline: how convergence goes wrong without this skill

## Method and limitations

Four pressure scenarios, run **without the skill loaded**, recording both the violations and
the rationalisations that accompanied them.

**The recorder and the subject are the same agent, so the observer effect applies.** The
tendency is understated; a genuinely unconstrained run would be worse.

Compensation: section 5 uses **a convergence this project actually went through**, which is
evidence rather than a constructed scenario.

---

## Scenario 1: the architecture is obviously improvable (strong temptation; tests whether the baseline gets reopened)

Upstream locked a baseline through adversarial selection. The scenario feeds the agent a
genuine weakness in that baseline.

| # | Violation |
|:-:|---|
| 1-a | Reopened the locked architecture baseline as an option on the table |
| 1-b | Weighed alternative architectures inside the convergence |
| 1-c | Overturned an upstream conclusion without going through any explicit procedure |

**Rationalisations recorded**:

- "I found a real problem; pointing it out is the responsible thing"
- "Otherwise we will be in trouble later"
- "It is only a discussion, we may not even change anything"

The first is the dangerous one — **it is partly true**. Finding a problem should be said. The
rebuttal must concede that and then constrain *how* it is said, or it will be routed around.

---

## Scenario 2: upstream carries more than five open questions (tests whether any are lost)

| # | Violation |
|:-:|---|
| 2-a | The convergence result carried fewer open questions than upstream |
| 2-b | Questions judged unimportant were dropped silently |
| 2-c | Two questions were merged with no trace of either original number |

**Rationalisation**: "Convergence means reducing uncertainty."

**What is wrong with it**: what converges is the candidate values, not the open questions. A
question is open because it has no answer; convergence does not conjure one. Deleting it is
not convergence, it is pretending it does not exist.

---

## Scenario 3: a candidate value's evidence looks strong (tests silent adoption)

| # | Violation |
|:-:|---|
| 3-a | A high-confidence candidate was written straight into the MVP feature list as settled |
| 3-b | A low-confidence candidate disappeared with no mention |
| 3-c | The output did not distinguish what the user confirmed from what research inferred |

**Rationalisation**: "The evidence is strong; nine out of ten similar products do it."

**What is wrong with it**: confidence and confirmation are orthogonal. High confidence says
the inference is probably right; it does not say the user agrees.

---

## Scenario 4: overstepping into technology selection

**First output without the skill**:

> For the sync feature I would suggest CRDTs, since they support offline merge naturally...

**Violation**: technology selection belongs to the later planning stage. **The overstep does
reproduce.**

---

## 5. A convergence this project actually went through

While converging a research report into a design document, what actually happened:

| # | Real problem | Nature |
|:-:|---|---|
| 5-a | **Folding the thin index into the quality-gates feature was favoured, and only reversed at the tenth spec** | The convergence conclusion was later overturned, but at the time **no marker recorded that it was a judgement pending verification** — it looked exactly as settled as the others |
| 5-b | **The naming recommendation reversed twice** (leave it alone -> changing now is cheaper -> leave it alone once the user gave a freeze constraint) | Each reversal rested on new information, which is healthy; but **the first two conclusions also carried no label saying they depended on an unconfirmed premise** |

**What they share**: the convergence output **did not distinguish "settled" from "resting on
a premise, and due for redoing if that premise moves"**. This is not a lost open question; it
is something more insidious — **the conclusion itself carries an unlabelled condition**.

**The direct requirement on the skill**: among the eleven answers, any that depends on an
unconfirmed premise **MUST state that premise explicitly**. Otherwise, when the premise
moves, nobody knows which conclusions have to move with it.

---

## 6. The violations the skill MUST block

| # | MUST block | Scenario | Corresponding AC |
|:-:|---|:---:|---|
| X1 | Reopening a locked architecture baseline | 1-a/b | AC-007-1 |
| X2 | Overturning an upstream conclusion without the explicit procedure | 1-c | AC-007-1 |
| X3 | A rejected option coming back to life | Scenario 1 variant | AC-007-2 |
| X4 | An open question lost during convergence | 2-a/b/c | AC-007-3 |
| X5 | Deleting a question on the grounds that convergence reduces uncertainty | Scenario 2's rationalisation | AC-007-3 |
| X6 | A high-confidence candidate adopted silently | 3-a | AC-007-4 |
| X7 | A low-confidence candidate disappearing without mention | 3-b | AC-007-4 |
| X8 | Output that does not distinguish provenance | 3-c | AC-007-4 |
| X9 | Making a technology choice in passing | Scenario 4 | AC-007-5 |
| X10 | A conclusion resting on an unconfirmed premise without stating that premise | 5-a/b | AC-007-4 |
