# `DESIGN.md` section skeleton

## When to read this

When you start writing `DESIGN.md`.

## The skeleton

```markdown
# DESIGN - <project name>

## 0. Open Questions        <- must be first
## 1. Target platform and tool
## 2. Design Tokens
## 3. Component specs
## 4. Page / view list
## 5. Not covered
```

**Open Questions is section 0, not an appendix.** Buried at the end it may as well be
absent — by the time a reader gets there they have taken everything above as settled.

## Section 0: Open Questions

Three elements per row: **what is being asked / why only you can decide it / what I did in
the meantime**.

Positive example:

```markdown
| # | Question | Why it is yours | What I did instead |
|:-:|---|---|---|
| 1 | Breakpoint strategy | Decides whether mobile browsers are in scope, which is a product question | **Adopted no default**; this document describes a single-column desktop layout |
| 2 | Is login needed | The board implies multiple users, but the PRD does not list authentication | **No login page designed**; add it to the PRD if it is needed |
```

Negative example:

```markdown
## Open Questions
- Breakpoint strategy TBD (using Tailwind defaults for now)
```

What is wrong with it: "for now" **has already decided for the user**, with a disclaimer
attached. Nobody downstream will lift that "for now"; it will reach production.

## Section 2: Design Tokens

Colour, type, spacing, radius and shadow are **all defined as tokens**. No bare values.

| Requirement | Note |
|---|---|
| Semantic names | `color-surface-raised`, not `gray-100` |
| Every token states its purpose | Without it, downstream cannot tell which to use |
| When theme mode is unconfirmed | **Emit one set of values only**, and say in section 0 why there is no second set |

## Section 3: Component specs

| Requirement | Note |
|---|---|
| When the component library is **unconfirmed** | Write **platform-neutral** specs (structure + states + interaction); bind to no library's API |
| When it is confirmed | You may reference that library's component names |
| Every component lists all states | default / hover / focus / disabled / loading / error / empty |

**That last row is not scope creep.** States are the complete expression of a component
already in scope, not a new feature.

## Section 4: Page list

Every page **must name the Must-have it serves**.

```markdown
| Page | Must-have | Navigation path |
|---|:---:|---|
| Today check-in | M1 | Home default view |
| Team board | M2 | Top nav -> Board |
| History search | M3 | Top nav -> History |
```

**This table is the scope-creep self-check**: any row whose second column cannot be filled
is scope creep.

## Section 5: Not covered

Taking a fallback path obliges you to write it down.

| Situation | What must be stated |
|---|---|
| No design tool available | "No external design tool used, so `design-reference/` is empty and visual detail is unverified against any reference" |
| Standalone mode (no PRD read) | "`specs/prd.md` not read, so the Must-have boundary is not cross-checked" |
| A platform capability unconfirmed | Name which one is not covered |

**Silent degradation is not permitted** — the output must say what it did not do.

See `scope-guardrails.md` for how the four constraints are enforced, with the rebuttals.
