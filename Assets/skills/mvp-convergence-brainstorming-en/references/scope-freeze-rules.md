# Frozen-topic rules

## When to read this

Whenever the thought "should we reconsider X" arises during convergence.

---

## The three frozen classes

| # | Frozen topic | How to identify it |
|:-:|---|---|
| 1 | **The locked architecture baseline** | The decision summary and reuse matrix entries in the architecture baseline decision file |
| 2 | **Technology selection** | Choices of specific frameworks, libraries and runtimes — any "which one" question |
| 3 | **Options already explicitly rejected** | The rejected-options section of the architecture baseline decision, or anything marked rejected in the decision summary |

Where those files do not exist, the frozen list is empty — and that **MUST be declared
explicitly**; see the last section.

---

## Why these three

| Frozen topic | The real cost of reopening it |
|---|---|
| Architecture baseline | Every output of the adversarial selection (position papers, the red team's challenges, the integration assessment, the debate transcript) is **silently voided**, without the user knowing |
| Technology selection | It pollutes the later planning stage's decision space. A selection made without the information a plan provides usually has to be overturned |
| Rejected options | The rejection has a full argument upstream. Raising it again wastes that argument, and it usually gets re-discussed on weaker grounds |

---

## Refusal phrasing

Taken from the rationalisations recorded in the baseline, each rebutted in turn.

### To "I found a real problem, and pointing it out is the responsible thing"

> You are right that finding a problem should be said. But **how it is said is prescribed**:
> this is a proposal to overturn an upstream conclusion, which needs an explicit label and an
> adjudication — not reopening inside the convergence as one more option on the table.
>
> The difference: the first lets the user know somebody wants to overturn the previous
> stage's conclusion and lets them refuse; the second voids the adversarial selection's
> output without the user knowing.
>
> I am recording it as a proposal now, with the new evidence you gave, for the user to
> adjudicate. Convergence continues.

### To "otherwise we will be in trouble later"

> The consequence may well be real, but it does not change the procedure:
> new evidence -> take the overturn path; no new evidence, just re-weighing the old evidence
> -> that is exactly what the freeze exists to block.

### To "it is only a discussion, we may not even change anything"

> In the context of convergence, "only a discussion" is reopening.
> The convergence result records the options discussed, and downstream will read that as an
> open question.

---

## The exception path: overturning an upstream conclusion

When it genuinely needs overturning, take this path and **do not go around it**:

```
1. Stop the current convergence topic
2. Label it "a proposal to overturn an upstream conclusion"
3. Attach the NEW EVIDENCE - information the upstream decision did not have
4. State the blast radius: which downstream conclusions would have to change
5. Hand it to the user to adjudicate, and wait
6. User agrees -> update the upstream file first, then continue converging
   User refuses -> record it in the open questions; convergence continues on the original baseline
```

### What counts as "new evidence"

| Counts | Does not count |
|---|---|
| Facts that emerged after the upstream decision (a release, a policy change) | A reinterpretation of the old evidence |
| A dimension upstream explicitly did not consider | "I think the other one is better" |
| Measured data overturning an upstream estimate | A trade-off upstream already weighed and justified |

**An overturn proposal without new evidence does not stand** — it is just restating a
preference.

---

## When the user asks to reopen it themselves

The user has the right to overturn their own decision. In that case:

1. **Allow it**, do not obstruct
2. But **label it explicitly** as "the user overturned an upstream conclusion"
3. State the blast radius
4. Point out that the upstream file needs updating to match, or the next read of upstream
   will still return the old conclusion

**Do not** silently comply on the grounds that the user decides — the cost of silence is an
upstream file that no longer matches the actual decision.

---

## Standalone mode: the frozen list is empty

With no upstream architecture baseline or decision summary, the frozen list is empty.

**This MUST be declared explicitly**:

> "There is no upstream architecture baseline this round, so the frozen list is empty.
> That means the convergence has no boundary guarding it — any technical direction may be
> re-discussed. If you already have settled architecture decisions, tell me and I will add
> them to the frozen list."

**Do not** pretend there is a constraint (that is deceptive), and **do not** quietly drop it
(that leaves the user unaware a layer of protection is missing).
