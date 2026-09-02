# Question Gate

## When to read this file

Read it when you cannot decide whether to ask the user now or record an open item
and continue.

---

## 1. The gate is two-directional

Most Skills fail in one direction: not asking when they should. This Skill **fails
in both directions**:

| Direction | How it shows up | Consequence |
|---|---|---|
| Should ask, does not | Infers key information itself and treats it as confirmed | Built on a false premise; the later it is found, the more it costs |
| **Should not ask, asks anyway** | Keeps re-confirming when the information is already sufficient | Breaks "one sentence is enough to start"; the user is interrupted until they give up |

The baseline **reproduced both directions** (scenarios 1-3 are the first, scenario 4
is the second). Writing only "ask the user when unsure" degrades this Skill into
scenario 4.

---

## 2. The three criteria

**Ask immediately if and only if any one of these holds. If none holds, record an
open item and continue.**

### Criterion 1 - The gap would make the research direction entirely different

The key words are "**entirely different**", not "more precise".

| Ask | Do not ask |
|---|---|
| "Is this for internal company use or public release?" -- it decides whether to research compliance and multi-tenancy, two completely different search paths | "Roughly what age range are the target users?" -- it does not change what you search for, only how detailed the conclusion is |
| "Is this replacing an existing system or greenfield?" -- it decides whether to research data migration | "What is the product called?" -- a temporary codename works for now |

**Self-check**: if the answer is A, what would I search for? And if it is B?
**Two search lists that barely differ -> do not ask.**

### Criterion 2 - The answer needs authorisation or private information

Information the Agent **cannot obtain on its own**.

| Ask | Do not ask |
|---|---|
| "Do you have an account we can use for X?" | "Roughly what budget do you have?" -- unless it is a hard constraint (see below) |
| "Can you provide the interface docs for the internal system?" | "How many people are on the team?" -- unless it affects a parallelism decision |
| "What is the hard budget ceiling?" (when option prices vary enough to drive selection) | "What is your company called?" |

**Note that "budget" appears in both columns.** The difference is whether it is
**currently driving an irreversible decision**. If it is not, record an open item.

### Criterion 3 - Continuing would waste substantial effort and be hard to reverse

| Ask | Do not ask |
|---|---|
| "Does it need to work offline?" -- it shapes the whole architecture; changing it later is enormously expensive | "What colour should the button be?" -- changeable at any time |
| "Must it stay compatible with that old version?" -- it decides the range of viable tech stacks | "Docs in which language?" -- can be unified later |

**Self-check**: if I guess wrong, is the rework **a few lines** or **a whole layer**?
A few lines -> do not ask.

---

## 3. Decision tree

```
A variable is missing
    |
    +- Without it, would my search list be entirely different?
    |     +- Yes -> [ASK NOW]
    |
    +- Is this something I cannot obtain myself (authorisation / private)?
    |     +- Yes -> [ASK NOW]
    |
    +- If I guess wrong, is the rework "a whole layer"?
    |     +- Yes -> [ASK NOW]
    |
    +- None of the above -> [RECORD AS OPEN ITEM, CONTINUE, DO NOT INTERRUPT]
```

---

## 4. One question at a time

When you do need to ask, **ask exactly one question**, and prefer A/B/C options over
an open-ended prompt.

Wrong -- the counter-example from baseline scenario 4: firing off four questions at
once.

Right: ask one, get the answer, then judge whether the next one is still needed --
**the previous answer often makes the later questions disappear by itself.**

---

## 5. Handling a vague answer

When the user answers "roughly, yeah / either is fine / your call / whatever":

**That is neither a confirmation nor an authorisation.** "Either is fine" carries at
least three meanings:

| Meaning | Correct response |
|---|---|
| Both really are acceptable | Record as confirmed "both acceptable" -- only if the user explicitly says that is what they mean |
| I have not thought it through | Record as an open item and flag the ambiguity |
| I do not want to discuss this now | Record as an open item and **do not follow up again**; leave it to the convergence stage |

**Default to the second reading** (open item plus a flag), because it is harmless
under the other two as well.

You may **follow up once**, and the follow-up MUST offer concrete options:

> "By 'either is fine', do you mean the two user groups need roughly the same thing,
> so one build covers both? Or that it is still undecided and you want to see the
> research first?"

Still vague after one follow-up -> record an open item, **stop following up**, and
move to the next item.

---

## 6. Two things you MUST do when you ask

1. **Say why you are asking now** -- which of the three criteria it hits. When the
   user knows this is not a casual question, they answer more carefully.
2. **Say what happens if they do not answer** -- "if you are unsure I will record X
   as a candidate and carry on; we settle it at the convergence stage". Give the
   user a legitimate exit from answering right now.
