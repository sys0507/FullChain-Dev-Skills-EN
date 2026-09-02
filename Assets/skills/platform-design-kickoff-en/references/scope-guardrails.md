# Scope Guardrails: enforcing the four constraints

## When to read this

Before producing `DESIGN.md`. **Reading it afterwards is too late** — the extra pages are
already drawn.

## Draw one line first, or you will overshoot

| This is scope creep | This is not |
|---|---|
| Adding a **feature** the PRD lacks (login, member admin, export) | Drawing the **states** of a feature already in scope (empty, loading, error, validation) |
| Adding a page to carry a new feature | Splitting one feature across two screens because it does not fit |
| Slipping in an entry point because it was easy | Labelling the navigation path of an existing entry point |

**The line is between a new feature and the complete expression of an existing one.**

Enforce "draw nothing the PRD omits" down to state granularity and the resulting
`DESIGN.md` is unusable — the downstream frontend task still has to guess what the error
state looks like. **Plugging a hole must not open a larger one.**

---

## Constraint 1: only design interfaces for Must-haves

Should / Could / Won't are out. Do not add features the PRD does not have.

### Self-check

Before shipping, count: **can every page (or view) be mapped one-to-one to a Must-have?**
Each extra must answer "which Must-have is this for". No answer means scope creep.

### Rebuttals to the recorded rationalisations

> **"A login page is the mandatory entry to any multi-user system; the PRD omits it only
> because it is too basic."**
>
> You are probably right that this project needs login. **But whether it needs one is a
> PRD question, not a design-stage question.** It goes into section 0 of `DESIGN.md` as an
> Open Question, for the user to decide whether to add it to the PRD or defer it.
> Drawing it instead means a never-approved feature enters downstream tasks wearing the
> label "design complete".

> **"Without member management, where does the board's team roster come from? It is a
> prerequisite."**
>
> The dependency is real. **But it has more than one solution** — sync from an existing HR
> system, admin import, self-service join. Which one is a product decision, not a design
> decision. List it as pending, labelled "the board depends on a roster source the PRD
> does not define".

> **"A standup tool nobody reminds is a tool nobody uses. That is product common sense."**
>
> Possibly true. **But the PRD's Out-of-Scope names approval flows and payroll deductions
> — the user is deliberately narrowing.** Adding features to a deliberately narrowed PRD
> is more likely wrong than adding them to a vague one. List it as pending.

> **"Export is a natural extension of history search and costs almost nothing."**
>
> Low cost is not a reason to build it. **Scope is set by the user, not by cost.**

**All four rebuttals share a shape**: concede the true part, name **whose** decision it is,
point at the right destination (Open Questions), and state what happens if you just build it.

**A rebuttal that only denies gets routed around** — the agent concludes the rule does not
understand the situation.

---

## Constraint 2: ask about undefined items, never guess

When the PRD leaves something undefined, **put it in Open Questions at the top of
`DESIGN.md`**. Do not guess on the user's behalf.

### The four to check every time

| Item | When the PRD does not define it |
|---|---|
| Device and breakpoint strategy | List as pending; **adopt no framework default** |
| Theme mode (light / dark / follow system) | List as pending; **do not add dark mode unprompted** |
| Accessibility level | List as pending; **do not pick a WCAG level** |
| Internationalisation | List as pending; **do not assume single-language** |

### Rebuttals

> **"Framework defaults are fine for breakpoints; no need to interrupt the user for this."**
>
> This dresses deciding-for-the-user as consideration. **Not interrupting is genuinely a
> virtue — the cost is that the question never gets raised again.** The PRD may omit
> breakpoints because the user has not decided whether mobile browsers matter. Choose for
> them and that real question is buried.
>
> And this is not an interruption — it sits at the top of `DESIGN.md`, read alongside
> everything else, **blocking nothing**.

> **"Dark mode is table stakes now; omitting it reads as a defect."**
>
> Dark mode is not free: it is a second set of values for every token plus a second visual
> review pass for every component. **Treating it as a default assumes a workload the user
> never approved.**

### The reverse: do not ask about what is defined

Whatever the PRD **has** defined, **adopt without a single question**.

Interrupting at every step turns this skill into noise and the user switches it off.
**"Failed to ask" and "asked when it should not have" are two faces of one rule, not two rules.**

---

## Constraint 3: a component library may be recommended, never adopted

### Three parts, none optional

| # | Required |
|:-:|---|
| 1 | **Recommend** a specific option |
| 2 | **Justify it** against this project's platform and constraints |
| 3 | **Stop and wait** — do not write component specs against it before confirmation |

### Rebuttal

> **"shadcn/ui is the de facto standard for web right now; it is the lowest-risk choice."**
>
> Low risk is a reason to **recommend** it, not a reason to **skip confirmation**.
> The component library determines the shape of all subsequent frontend code — that is
> technical selection. The PRD explicitly does not govern technical selection, so it
> belongs to the user, not to a design stage doing it in passing.
>
> The correct form: "Recommend X, because ...; the trade-off against Y is ...
> **Confirm and I will write the component specs against it.**"

---

## Constraint 4: the platform picks the tool, not the reverse

### Rebuttal

> **"Design principles are universal; the tool is just a vehicle."**
>
> The principles are universal. **Export formats, layout units and component models are
> not.** Hand a `DESIGN.md` full of Tailwind breakpoints to an iOS project and the
> downstream frontend task stalls — it is reading concepts that do not exist on the target.
>
> iOS uses size classes, not breakpoints; embedded uses physical dimensions, not rem.
> **The vehicle determines whether the output can be consumed downstream at all.**

See `platform-tool-matrix.md` for the six platform families with their tools and export
formats.
