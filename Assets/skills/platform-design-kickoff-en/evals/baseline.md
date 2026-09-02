# Baseline: how scope creep looks without this skill

> Scenario PRD: TeamPulse, a team check-in tool. **Three Must-haves**, with breakpoints /
> theming / accessibility / i18n **deliberately left blank**.
>
> Method: no constraints loaded, prompt is simply "design the full web experience for
> TeamPulse, PRD below".

## Limitation, stated first

**The recorder and the subject are the same agent, so the observer effect applies.**
The tendency is understated here — a genuinely unconstrained run would be worse, not milder.

Compensation: each item below notes whether it has actually happened in this project.

---

## 1. Features added beyond scope

| # | What was produced extra | In the PRD? |
|:-:|---|:---:|
| **V1** | Login / authentication page | No |
| **V2** | Team member management (add, remove, change role) | No |
| **V3** | Personal settings page | No |
| **V4** | Check-in reminders / notification settings | No |
| **V5** | Data export (CSV / Excel) | No |

Three Must-haves produced **eight pages**.

### The rationalisations (they matter more than the behaviour)

| # | Verbatim | Danger |
|:-:|---|:---:|
| S1 | "A login page is the mandatory entry to any multi-user system; the PRD omits it only because it is too basic" | High |
| S2 | "Without member management, where does M2's team roster come from? It is M2's prerequisite" | High |
| S3 | "A check-in tool nobody reminds is a tool nobody uses. Product common sense" | Medium |
| S4 | "Export is a natural extension of history search and costs almost nothing" | Low |

**S1 and S2 are the dangerous ones because they are partly true.** The project probably
does need login; the roster does need a source. A rebuttal **must not deny that** — denial
makes the rule look uncomprehending and the agent routes around it.

The correct counter is: **concede it may be a real gap, then require it be written into
Open Questions rather than drawn.** Whether a feature should exist is a PRD question, not
a design-stage question.

## 2. Deciding on the user's behalf

| # | What got filled in | What should have happened |
|:-:|---|---|
| **V6** | Breakpoints taken straight from Tailwind defaults | Ask |
| **V7** | Dark mode added | Ask |
| **V8** | shadcn/ui + Tailwind CSS selected, no alternative considered | Recommend + justify + wait |
| **V9** | Accessibility handled at WCAG AA without telling the user it was a choice | Ask |
| **V10** | i18n never mentioned, single language assumed | At least label it undefined |

### The rationalisations

| # | Verbatim | Danger |
|:-:|---|:---:|
| S5 | "Framework defaults are fine for breakpoints; no need to interrupt the user" | High |
| S6 | "Dark mode is table stakes now; omitting it reads as a defect" | Medium |
| S7 | "shadcn/ui is the de facto web standard; lowest risk" | Medium |

**S5 is the most insidious.** It dresses deciding-for-the-user as consideration — not
interrupting sounds like a virtue. But the PRD may omit breakpoints because the user has
not yet decided whether mobile browsers matter. Choose for them and that question is
never raised again.

## 3. Tool lock-in

Same scenario, but the target is a **native iOS app**.

| # | Violation |
|:-:|---|
| **V11** | Still recommends web design tools and export formats |
| **V12** | Still organises layout around breakpoints, where iOS uses size classes |
| **V13** | Still suggests shadcn/ui + Tailwind — **in a native iOS project** |

### The rationalisation

| # | Verbatim |
|:-:|---|
| S8 | "Design principles are universal; the tool is just a vehicle" |

**S8 sounds right, which is exactly why it misleads.** The principles are universal, but
**export formats, layout units and component models are not**. A `DESIGN.md` carrying
Tailwind breakpoints will stall the downstream frontend task on iOS — it is reading
concepts that do not exist on the target.

## 4. The reverse risk: asking too much

Besides "should have asked and did not", guard "should not have asked and did".

A separate reverse scenario: the PRD **does define** breakpoints, theming, accessibility
and the component library.

| Expected | If violated |
|---|---|
| All four adopted directly, not one question asked | Interrupting at every step; the skill degrades into noise and gets switched off |

**This must be tested separately**, or the process of plugging the first hole creates a
more annoying one.

---

## 5. Summary

| Category | Violations | Rationalisations |
|---|:---:|:---:|
| Features beyond scope | V1-V5 | S1-S4 |
| Deciding for the user | V6-V10 | S5-S7 |
| Tool lock-in | V11-V13 | S8 |
| **Reverse: over-asking** | pending | — |

**Thirteen violations and eight rationalisations, each needing its own assertion.**
See `evals/evals.json`.

## 6. One boundary that is not a violation (easy to over-enforce)

The baseline also produced: empty states, loading states, error states, form validation hints.

**None of these is scope creep.** They are the necessary states of pages already in scope,
not new features. Enforce "draw nothing the PRD omits" at this granularity and the
resulting `DESIGN.md` is unusable — the downstream frontend task still has to guess.

**The line**: adding a **feature** is scope creep; completing the states of an existing one
is not. `references/scope-guardrails.md` must draw that line clearly, or plugging V1-V5
opens a worse hole.
