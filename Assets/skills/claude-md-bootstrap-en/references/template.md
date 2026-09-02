# CLAUDE.md · 10-Section Standard Template

The reference structure for generated CLAUDE.md files. Adapt section content to
the specific project, but keep the section order and naming consistent.

Total target: < 200 lines.

---

## Section 1 · Project Identity (WHAT)

Open with a single-line title and a one-paragraph definition.

Pattern:
```markdown
# <project-name> · CLAUDE.md

> <one-line tagline, often from PRD title>

## 1 · What this project is (WHAT)

<2-4 sentences extracted/synthesized from the PRD's "product overview"
section, whatever it's actually named in your PRD>

Full business requirements: @specs/prd.md
```

---

## Section 2 · Why this project exists (WHY)

Pattern:
```markdown
## 2 · Why this project exists (WHY)

<2-3 sentences synthesized from the PRD's "business goals" portion,
whatever it's actually named>

Detailed business goals and success metrics: PRD §2 / §7.
```

---

## Section 3 · Workflow (HOW)

**Principle: action-oriented, never historical.**

CLAUDE.md is read by future development sessions. They don't care how the
project got here ("research -> debate -> PRD -> specify -> ... -> constitution").
They care about **what to do right now when starting a task**.

### Extract, don't hardcode

Section 3's content MUST be extracted from the sources below, not filled in from
this template:

- The "development discipline" passages in the project's constitution, discipline
  or agent-rules documents (the section names vary by project)
- The label system in `specs/00X-*/tasks.md` (`[FE]` / `[BE]` / `[INT]` and so on)
- The project's actual workflow documents (a README workflow section, files under
  `docs/`)
- Any development-rhythm conventions agreed in conversation with the user

### Required structure (4-5 action blocks)

Once extracted, organise it in this structure, **one or two lines per block**:

1. **How to start a feature** (one command)
2. **What context every task must read on starting** (a list of `@path`s)
3. **Testing discipline** (which skill, what rhythm)
4. **What to do when a feature completes** (review skill + tag + state.md)
5. **The rhythm rule** (where to stop and wait for review)

### Anti-pattern (MUST NOT generate)

- A list of the past nine steps and what is "done"
- Historical markers such as "(completed)" / "(locked)" / "(ratified)"
- Descriptions of "how the spec was written" or "how the constitution was ratified"

### Target length

20-30 lines. Where the source files hold little, go shorter — do not pad to length.

---

## Section 4 · Tech Stack

Extract from `package.json` (or equivalent). Real names, real versions.

Pattern:
```markdown
## 4 · Tech stack

| Layer | Technology | Version source |
|----|------|---------|
| Frontend | React + TypeScript + Tailwind + shadcn/ui | package.json |
| Backend | Node.js + Express (or the actual framework) | package.json |
| Database | <extracted from the architecture decision document> | <that document's real path> |
| Testing | Vitest + @testing-library/react | package.json |
| Deployment | <extracted from the PRD or deployment document> | - |

> Exact versions live in `package.json`. The reasoning behind the selection is in
> @<the architecture decision document's real path>.
```

If the project has no architecture decision document, just point to package.json
and PRD.

---

## Section 5 · Commands

Verbatim from `package.json` scripts. Do not invent.

Pattern:
```markdown
## 5 · Commands

\```bash
# Development
npm run dev          # <description extracted from scripts>
npm run dev:api      # ...

# Testing
npm test             # run every test
npm test -- <path>   # run a single test file

# Build
npm run build
npm run lint
npm run typecheck
\```
```

Only include commands that actually exist in package.json. Don't show
"npm run lint" if there's no lint script.

---

## Section 6 · Project Constitution Reference

If the project has `.specify/memory/constitution.md`, reference it; do not copy.

Pattern:
```markdown
## 6 · Project constitution

**YOU MUST** read the project constitution before implementing any task:

@.specify/memory/constitution.md

The constitution defines principles that MUST NOT be violated. A violation means
the implementation has failed.
```

If no constitution exists, skip this section.

---

## Section 7 · Visual System Reference

If the project has `DESIGN.md` and/or `design-reference/`, reference them.

Pattern:
```markdown
## 7 · Visual system

During frontend implementation, **YOU MUST** first read:
- @DESIGN.md (the design system constitution: colour, type and spacing tokens)
- `design-reference/<source>-export/<the matching page>/` (visual reference samples)

Key conventions: <list briefly any market convention that applies, such as a
market's rise/fall colour convention, dark mode, or brand colours>
```

If the project has no visual system, skip this section.

---

## Section 8 · Anti-Patterns

What NOT to do. Each item must trace to a source paragraph (constitution,
PRD, architecture decision, or industry standard).

Pattern:
```markdown
## 8 · Anti-patterns (forbidden)

- Do not hardcode visual values in code (colour hex, font-size px) — they MUST go
  through DESIGN.md tokens
  *(source: constitution F-1)*
- Do not introduce a second UI component library — the project is on shadcn/ui
  *(source: constitution F-4)*
- Do not make technology choices during /speckit.specify — leave them to /plan
  *(source: Spec-Kit official guidance)*
- Do not "helpfully" add features the spec never asked for
  *(source: Karpathy principle #2, Simplicity First)*
- Do not let .env or .credentials.yaml into git
  *(source: general security practice)*
- Do not submit several features in one PR — branch per feature
  *(source: Spec-Kit + Superpowers convention)*
```

Aim for 6-8 items. Each item ≤ 2 lines.

---

## Section 9 · Behavioral Guidelines (Karpathy-Inspired)

Insert the contents of `references/karpathy-guidelines.md` verbatim, under a
one-line introduction:

```markdown
## 9 · Behavioral Guidelines (Karpathy-Inspired)

These four principles apply to every task's implementation phase across the whole
project, to reduce the common failure modes of AI coding.

[paste references/karpathy-guidelines.md verbatim here]
```

Do NOT reword the four principles. The original wording is precise.

---

## Section 10 · Key File Navigation

A table that lists every important project document and when to read it.

Pattern:
```markdown
## 10 · Key file navigation

| File | Purpose | When to read |
|------|------|--------|
| @.specify/memory/constitution.md | Project constitution | Before implementing every task |
| @specs/prd.md | Business requirements | When a business boundary is unclear |
| @<the architecture decision document's real path> | Technology selection | Before adding a dependency |
| @DESIGN.md | Visual system | Required for `[FE]` tasks |
| design-reference/<source>-export/ | Visual samples | Required for `[FE]` tasks |
| specs/00X-<feature>/spec.md | Feature requirements | Before starting the feature |
| specs/00X-<feature>/plan.md | Feature implementation plan | Before starting the feature |
| specs/00X-<feature>/tasks.md | Feature task list | While executing tasks |
| specs/00X-<feature>/state.md | Feature progress | Update after each task completes |
```

Only include files that actually exist. Verify each path before listing.

---

## Length budget

| Section | Target lines |
|---------|-------------|
| 1. WHAT | 5-8 |
| 2. WHY | 4-6 |
| 3. HOW | 8-12 |
| 4. Tech stack | 10-15 |
| 5. Commands | 15-25 |
| 6. Constitution ref | 5-7 |
| 7. Visual system ref | 5-8 |
| 8. Anti-patterns | 12-18 |
| 9. Karpathy | 30-35 |
| 10. File navigation | 12-18 |
| Headers + dividers | 10-15 |
| **Total** | **~115-167** |

This leaves a buffer under the 200-line ceiling for project-specific extensions.

---

## Section ordering rationale

Why this order:
1. **WHAT first** — Claude needs to know what this project IS before anything else
2. **WHY before HOW** — purpose before mechanics
3. **Tech stack before commands** — names before invocations
4. **Constitution + Visual before Anti-patterns** — positive rules before negatives
5. **Karpathy at the end** — universal behavior guidelines, the "always-true"
   layer underneath project specifics
6. **File navigation last** — readers who scroll to the end get the routing map
