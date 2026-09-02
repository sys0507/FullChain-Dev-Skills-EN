---
name: prd-writer-universal-en
description: Generate an industry-standard, domain-neutral Product Requirements Document from confirmed research and brainstorming outcomes. Supports project-level PRDs at specs/prd.md and feature-level PRDs at specs/feature-slug/prd.md, with verifiable acceptance criteria, scope boundaries, risks, and open questions. Use for PRD or product-spec writing; do not use for technical design, market research, or unconverged ideation.
license: MIT
metadata:
  version: "1.0"
  lang: en
  stage: "3"
  standalone: true
  produces:
    - "specs/prd.md"
    - "specs/<feature-slug>/prd.md"
  requires:
    - name: "Upstream research or brainstorming conclusions"
      level: orchestration
      fallback: "Extract them on the spot through Socratic Q&A; never refuse to work just because the file is missing"
    - name: "specs/research/00-project-input-and-assumptions.md"
      level: orchestration
      fallback: "Ask the user which items are confirmed; with no ledger, treat every item as unconfirmed"
    - name: "Spec toolchain"
      level: optional
      fallback: "The PRD produced is still directly usable as downstream input; it simply does not trigger that toolchain's handoff"
---

# PRD-Writer · Standard Product Requirements Document Generation Skill

## What This Skill Does

Transforms "ideas + research + brainstorming conclusions" into a **14-chapter PRD that meets industry standards**. The output can be fed directly to engineers / Claude Code / Spec-kit for subsequent technical design and implementation.

**What it is**:
- A **structured, verifiable, AI-friendly** product requirements document generator
- A 14-chapter PRD template that meets industry standards, covering all dimensions from background to risk
- **English-first**, with chapter names in English

**What it is not**:
- ❌ Not a Technical Requirements Document (TRD / Design Doc) — that's the next step
- ❌ Not market research / competitive analysis / business planning — those are upstream
- ❌ Not a replacement for brainstorming itself — it **crystallizes** brainstorming conclusions into a formal document

---

## Core Principles (Iron Rules)

### 1. PRD Comes **After** Brainstorming, Not Before

Correct flow:
```
Idea → Research → Brainstorming (diverge + converge) → PRD (write it down) → TRD (technical design) → Implementation
                                                        ↑
                                                   This Skill is here
```

⚠️ **Anti-pattern**: Using PRD for open-ended exploration. PRD is a "resolution document", not a "discussion draft".

### 2. PRD Describes "What to Build", Not "How to Build It"

**Simple cut rule**:
> If an engineer can use a different implementation and still satisfy the requirement → **keep it in the PRD**
> If the engineer cannot use a different implementation → **that's a technical decision, move it to the TRD**

✅ Goes in PRD: "Core feature first-screen load time ≤ 2 seconds"
❌ Does not go in PRD: "Implement the Dashboard with React + Vite"

See `references/prd-vs-trd-boundary.md` for details.

### 3. AI-Friendly Precision

"Specs are the new code": PRDs must be written to a precision that **AI Agents can directly consume** — inputs, outputs, boundary conditions, and acceptance criteria must all be explicit.

But still **do not specify**: tech stack / specific libraries / specific class names.

---

## 5-Step Workflow

### Step 1: Check Upstream Artifacts (Prerequisites)

Ask the user whether they have any of the following materials (any one is sufficient):

- 📁 Research report (Step 2 research output)
- 📝 Brainstorming design doc / meeting notes
- 💡 Idea card / MVP Scope statement
- 🎯 Competitive analysis / user interview notes

If there are **no upstream materials at all**:
- Do not force-write the PRD (the result will inevitably be hollow)
- Suggest the user first do brainstorming or research
- Or extract information on the spot via Q&A (suitable for simple projects)

First choose one output mode and generate only that mode:

- **Project-level PRD**: use when `specs/research/` contains project research and convergence decisions, or the user explicitly requests a PRD for the whole project. Output to `specs/prd.md`.
- **Single-feature PRD**: use when the user is defining one independent feature. Output to `specs/<feature-slug>/prd.md`.

In project-level mode, read these sources first:

1. `specs/research/00-project-input-and-assumptions.md`
2. `specs/research/06-architecture-baseline.md`; if absent, use `05-decision-summary.md`
3. Existing `specs/research/01-*.md` through `05-*.md`
4. Any existing brainstorming or design document

Only user-confirmed information may become settled requirements. Research candidates, inferences, and unresolved items belong under assumptions, risks, or Open Questions.

### Step 2: Fill In 6 Core Information Items

Fill in via Socratic Q&A (one question at a time, multiple-choice A/B/C format preferred):

If upstream research or brainstorming already answers an item clearly, reuse it and cite the source. Ask only about information that is genuinely missing, contradictory, or blocks finalization.

1. **One-sentence project definition**: "___ is a ___ tool for ___ used by ___"
2. **Core target user**: Primary persona / Anti-persona
3. **MVP scope**: 3-5 must-have features + explicit won't-do list
4. **Success metrics**: What counts as success? (Specific numbers, not "better")
5. **Key non-functional requirements**: Performance / security / compliance baselines
6. **Current uncertainties**: 3-5 Open Questions

⚠️ If the user gives a vague answer to any question, **follow up** until it is clear. Do not fill in the blanks yourself.

### Step 3: Generate PRD Using the 14-Chapter Structure

When to read `references/14-chapters-detailed.md`: read it when starting to generate PRD chapters; consult that chapter's "template snippet + anti-patterns" before writing each chapter. Chapters 1-7 are in that file; **chapters 8-14 are in `references/14-chapters-detailed-part2.md`**.

**Quick reference**:

| # | Chapter | Required/Recommended/Optional | One-line purpose |
|:-:|------|:-:|----------|
| 1 | Document Info (version/author/status) | ★ | Who, when, what changed |
| 2 | Project Background & Goals (Why) | ★ | Why do it, what to achieve |
| 3 | Target Users & Personas | ★ | Who it's for |
| 4 | User Stories / Use Cases | ★ | In what context users use it |
| 5 | Feature List & Scope (Scope / Out-of-Scope) | ★ | What to build, what not to build |
| 6 | Detailed Feature Descriptions (input/output/flow/boundary) | ★ | How each feature behaves |
| 7 | Non-Functional Requirements (performance/security/compliance) | ★ | Quality baselines |
| 8 | UI / Interaction Notes | ☆ | What it looks like |
| 9 | Acceptance Criteria (Given/When/Then) | ★ | What "done" means |
| 10 | Priority / MVP Scope | ★ | What to build first |
| 11 | Metrics (Success Criteria) | ★ | What counts as success |
| 12 | Dependencies & Constraints | ☆ | Blockers, waiting on whom |
| 13 | Risks & Mitigations / Open Questions | ★ | What's still uncertain |
| 14 | Milestones / Timeline | ☆ | When it will be done |

★ Required · ☆ Recommended · ○ Optional

**Slim version** (for small / personal projects): keep #1, #2, #3, #5, #6, #9, #10, #11, #13 (9 chapters).

### Step 4: Self-Check 4 Key Boundaries

After writing, self-check:

- [ ] **What/How boundary**: No tech stack / framework / library selections written
- [ ] **Verifiability**: Every feature has executable acceptance criteria (Given/When/Then format)
- [ ] **Scope clarity**: Both Scope and Out-of-Scope are written
- [ ] **AI-friendly**: Boundary conditions, error handling, and performance requirements are all explicit; AI does not need to "guess"

When to read `references/prd-anti-patterns.md`: mandatory during the self-check phase; go through the 24-item anti-pattern checklist item by item.
When to read `references/prd-vs-trd-boundary.md`: whenever you encounter a gray-area judgment of "does this count as What or How".

### Step 5: Output + Handoff to Next Step

**Output location** (choose one; do not generate both):

- Project-level PRD: `<project>/specs/prd.md`
- Single-feature PRD: `<project>/specs/<feature-slug>/prd.md`

**Handoff suggestion** (write at the end of the PRD):

```markdown
## Next Steps

This PRD has completed Step 3. To continue with Step 4 technical design:
- Use Spec-kit `/speckit.plan` command to generate plan.md based on this PRD
- Or launch the Brainstorming Skill again for technology selection
- Focus areas: architecture / data model / API contract / deployment plan
```

---

## Position in the Vibe Coding 9-Step Process

```
1.Idea → 2.Research → [Brainstorming diverge] → 3.PRD ← This Skill → 4.Technical Design → 5.Frontend Design → ...
                                                  ↑
                                                  Output: specs/prd.md or specs/<feature>/prd.md
```

When to read `references/workflow-integration.md`: when the user asks "how does this Skill work with Spec-Kit / OpenSpec / Superpowers".

---

## Complete PRD Examples (Cross-Domain)

When to read `references/examples.md`: when the user needs a reference example / is unsure how to fill in a certain chapter. It contains PRD excerpt examples from three different domains — SaaS tools, consumer apps, and B2B internal tools — showing how the same 14-chapter framework is filled in for different product types. **Example C (B2B internal tool) and the three-way comparison are in `references/examples-b2b.md`.**

---

## Recommended PRD File Naming Convention

```
<project-root>/
├── specs/
│   ├── 0001-feature-name/
│   │   ├── prd.md                  ← This Skill's output
│   │   ├── plan.md                 ← Step 4 output (not this skill's responsibility)
│   │   ├── tasks.md                ← Step 4 output
│   │   └── README.md
│   ├── 0002-another-feature/
│   └── ...
```

**Naming rule**: `<4-digit-index>-<kebab-case-feature-slug>/`

---

## Output Format Requirements

1. **Markdown**, not Word / PDF
2. **Fixed chapter order**, following the 14-chapter template
3. **Each chapter uses a `##` second-level heading**
4. **Tables preferred**, minimize long paragraphs
5. **Each feature description uses a unified 4-tuple**: trigger / input / flow / output / boundary
6. **Acceptance criteria in Given/When/Then format** (machine-verifiable)
7. **Line length** ≤ 100 characters (for easy diff / review)

---

## Compatibility with Existing Tools

| Tool | Compatibility | Notes |
|------|:-----:|------|
| GitHub Spec-Kit `/specify` | ✅ Fully compatible | This Skill's output can be used as spec.md |
| OpenSpec | ✅ Compatible | Can serve as input for `/proposal` |
| Superpowers Brainstorming | ✅ Perfect handoff | This Skill is the next step after Brainstorming |
| Claude Code built-in | ✅ Native | Reads directly |
| Cursor / Codex | ✅ Markdown universal | Can be fed directly |

---

## Trigger Keywords Quick Reference

English: write a PRD / product requirements document / requirements doc / feature spec / product spec / write requirements / organize requirements / turn ideas into a PRD / turn brainstorming into a doc / PRD draft / spec doc / write a product spec / document brainstorming conclusions

Whenever a task **touches product requirements documents**, invoke this Skill immediately.

---

## Anti-Pattern Quick Review (Run After Writing PRD)

- ❌ Written as a feature list (missing Why / missing acceptance criteria)
- ❌ No Out-of-Scope (scope will explode)
- ❌ Tech stack written into the PRD (pollutes boundaries)
- ❌ Acceptance criteria written as "the system should be user-friendly" (not verifiable)
- ❌ No Open Questions (pretending everything is clear)
- ❌ Missing document info / version number stuck at v0.1

Full anti-pattern list in `references/prd-anti-patterns.md`

---

## When the User's Project Is Medium/Large Scale

Enable the following supplementary chapters as needed:
- **Business rules and exception branches** (required for e-commerce / finance / government)
- **Multi-language / internationalization requirements**
- **Data migration plan** (when replacing a legacy system)
- **Training and operations support** (B2B SaaS)

Expand as needed, but don't write for the sake of writing.

## Upstream Artifacts

| Artifact | Level | When missing |
|---|:---:|---|
| Upstream research or brainstorming conclusions | orchestration | Extract on the spot through Q&A |
| `specs/research/00-project-input-and-assumptions.md` | orchestration | Ask the user which items are confirmed; with no ledger, treat every item as unconfirmed |
| Spec toolchain | optional | The PRD is still directly usable as downstream input |

## Downstream Consumers

| Consumer | What it takes from this skill |
|---|---|
| Feature documentation pipeline Skill | The Must-have list and acceptance criteria in `specs/prd.md` |
| Design Skill | Target users, platforms, and non-functional requirements |

## Standalone Use

**What you provide**: one requirement description is enough — paste it or say it out loud. Research artifacts help, but without them I will fill in the 6 core information items through Q&A.

**What you get**: a 14-chapter structured PRD with Scope/Out-of-Scope, Given/When/Then acceptance criteria, and Open Questions.

**What you don't get**:

- **I will not do the research for you**. With no upstream material, the factual density of the PRD depends on how much you supply during Q&A.
- **No technical design** — technology selection belongs downstream.
- With no ledger I cannot tell which items you have confirmed from which you mentioned in passing, so **every item is treated as unconfirmed** and listed under Open Questions.

**Gate**: ask one question at a time during Q&A; when the user answers vaguely on an item, follow up — MUST NOT fill the gap by guessing.
