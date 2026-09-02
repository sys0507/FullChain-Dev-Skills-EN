# Handoff to PRD · Downstream Pipeline Standard Interface Document

> This document is the downstream handoff specification for the
> `product-research-kickoff-universal-en` Skill, providing a clear answer to
> "how to go all the way from completed research to Spec-Kit".
> SKILL.md's main body contains ready-to-use trigger prompts; this document
> contains the methodology (understanding why the handoff is structured this way).
>
> **When to read**: when the user asks "what's the next step after research",
> "what goes into the PRD", or "how to turn a PRD into a spec-kit".

---

## Table of Contents

- [I. 5-Stage Pipeline Overview](#i-5-stage-pipeline-overview)
- [II. 11 Questions Brainstorming Must Answer](#ii-11-questions-brainstorming-must-answer)
- [III. PRD 12-Chapter Standard Structure](#iii-prd-12-chapter-standard-structure)
- [IV. 7 Rules for Converting PRD → Spec-Kit](#iv-7-rules-for-converting-prd--spec-kit)
- [V. Three Common Anti-Patterns](#v-three-common-anti-patterns)
- [VI. Sources](#vi-sources)

---

## I. 5-Stage Pipeline Overview (including optional adversarial research)

```
Launch Research (this Skill)
  Output: specs/research/01~05.md
  Answers: what can be built? what resources are available? is it technically feasible?
       ↓
★ Adversarial Research (adversarial-architecture-selection-universal-en Skill, optional)
  Trigger condition: 03-open-source.md has ≥ 2 candidates, or there is a clear
                     technical approach selection conflict
  Output: specs/research/06-architecture-baseline.md + 05-decision-summary.md (v2)
  Answers: making a traceable architecture baseline decision among multiple
           technical candidates
       ↓
Brainstorming (brainstorming Skill)
  Output: direction convergence notes (covering the 11 questions below)
  Answers: picking the right direction from the "possibility space" revealed by research
       ↓
PRD (prd-writer-universal-en Skill)
  Output: specs/prd.md (12 chapters, AI-friendly precision)
  Answers: putting "what to build + why + how to know it's done" into a written contract
       ↓
Spec-Kit (/specify → /plan → /tasks → /implement)
  Output: specs/00X-feature/{spec, plan, tasks}.md + code
  Answers: converting PRD Must-have features into executable spec → technical plan
           → tasks → implementation
```

**The nature of the four boundaries**:

| Boundary | Nature |
|----------|--------|
| Research → Adversarial Research | Information gathering → multi-candidate adversarial decision (only when N ≥ 2) |
| Adversarial Research → Brainstorming | Technical baseline → product direction decision |
| Brainstorming → PRD | Verbal consensus → written contract |
| PRD → Spec-Kit | Product language → engineering language |

**When to skip adversarial research**:
- 03-open-source.md recommends 0 or 1 candidates → skip; go directly to brainstorming
- Technical selection is already done with no architecture conflict → skip
- Candidate differences are minimal (e.g., different versions of the same library) →
  skip; consult the official docs directly

**When adversarial research is required** (strongly recommended not to skip):
- Multiple open-source project fork candidates (classic fork selection scenario)
- Multiple cloud vendors / SaaS comparison (Vercel vs Netlify vs Cloudflare)
- Multiple tech stack face-offs (React vs Vue vs Svelte)
- Multiple library selections (LangChain vs LlamaIndex vs Haystack)
- Multiple architecture approaches (Monolith vs Microservices vs Serverless)

---

## II. 11 Questions Brainstorming Must Answer

After research output is in place, the brainstorming phase must help the user answer
all 11 questions below — **these 11 answers are the input checklist for the PRD**.
If any question cannot be answered, brainstorming has not converged enough;
do not rush to write the PRD.

### ⚠️ If adversarial research was run (06-architecture-baseline.md exists), the following questions are constrained by 06

| Question | Impact from 06 | How it affects |
|----------|:--------------:|----------------|
| Q1–3, Q7 | ❌ No impact | Pure product decisions |
| Q4 MVP features / Out-of-Scope | ✅ Strong impact | Must-haves should prioritize modules marked "direct reuse" in 06; Out-of-Scope must include capabilities involving "fatal flaws" in 06 |
| Q5 Boundary conditions | ✅ Strong impact | Boundaries must be within what the 06 architecture baseline supports |
| Q6 Non-functional requirements | 🟡 Partial impact | Performance ceiling is constrained by the architecture baseline |
| Q8 Priority MoSCoW | ✅ Strong impact | Ordering references modification cost from 06 (lower cost = higher priority) |
| Q9 Kill switch | 🟡 Partial impact | Consider the scaling ceiling of the 06 architecture baseline |
| Q10 Open Questions | ✅ Strong impact | **Must include all Open Questions remaining from 06**; may add new product-level ones |
| Q11 Dependencies and constraints | ✅ Strong impact | Write only product-level dependencies (external APIs / compliance / approvals); do not repeat 06's technical dependencies |

**Brainstorming must not re-open**: architecture baseline, tech stack decisions, and
approaches already rejected in 06 — these are 06's outputs and must not be re-debated.

### [Why / What / What Not] (5 questions)

1. **Business objective + product objective + Non-Goals**
   - Business objective example: serve 1,000 users within 6 months of launch
   - Product objective example: reduce "idea → launch" time from 2 weeks to 2 days
   - Non-Goals example: not building feature X; not serving scenario Y

2. **1–2 primary personas + anti-personas**
   - Primary persona should be specific: background, goals, pain points, frequency,
     device
   - Anti-persona: explicitly state "who we are not serving"

3. **3–5 core user stories** (INVEST format)
   - As X, I want Y, so that Z
   - Must reflect real scenarios, not just paraphrased features

4. **MVP feature list + Out-of-Scope list**
   - Must-haves: keep to 5–8
   - Out-of-Scope: list at least 3 (AI cannot infer from omission)
   - ⚠️ With 06: Must-haves should prioritize capabilities marked "direct reuse" in the
     reuse matrix; Out-of-Scope must include capabilities involving "fatal flaws" in 06

5. **Key boundary conditions for each core feature**
   - What happens with missing data? Concurrent conflicts? External service failure?
   - This item is most commonly overlooked but directly determines whether AI will fill
     in incorrect assumptions during coding
   - ⚠️ With 06: boundary conditions must fall within what the 06 architecture baseline
     supports

### [How to Know It's Done] (4 questions)

6. **Non-functional requirements** — must use numbers; adjectives are prohibited
   - ❌ "Fast", "user-friendly", "stable"
   - ✅ p95 < 3s, monthly availability ≥ 99.5%, error rate < 0.1%
   - 🟡 With 06: performance ceiling references the real capability of the 06
     architecture baseline

7. **Acceptance criteria for each user story (Given/When/Then)**
   - Can be directly converted to test cases
   - Must cover at least one normal path + one error path

8. **Priority (MoSCoW)**
   - Must / Should / Could / Won't
   - Enforce 80/20 — if everything is "Must" it's the same as having no priority
   - ⚠️ With 06: ordering references modification cost from 06 (lower cost = higher
     priority)

9. **North Star metric + kill switch**
   - North Star: 1 core metric (e.g., monthly active users ≥ N)
   - Kill switch: when to start over (e.g., MAU < X after 3 months)
   - 🟡 With 06: kill switch should consider the scaling ceiling of the 06 architecture
     baseline

### [Still Uncertain] (2 questions)

10. **At least 3 Open Questions**
    - List unresolved items + Owner + Due Date
    - Fewer than 3 usually means the thinking isn't thorough enough
      (Aakash Gupta principle)
    - ⚠️ With 06: **must include all Open Questions remaining from 06**; may add new
      product-level Open Questions

11. **Key dependencies and constraints**
    - External APIs / data sources / compliance approvals / platform policies
    - What is in someone else's hands; what has a deadline
    - ⚠️ With 06: write only **product-level** dependencies; technical dependencies are
      already captured in 06 and should not be repeated

### Brainstorming Trigger Prompt (recommended version)

```
Please read the research files under specs/research/ carefully,
then use the brainstorming Skill to help me converge the MVP direction.
You must help me determine all 11 questions listed above.

⚠️ Do not ask me to make tech stack decisions (which framework / library /
   database to use) — leave tech stack decisions to the spec-kit /plan phase.
```

---

## III. PRD 12-Chapter Standard Structure

Based on a synthesis of templates from Atlassian / ProductSchool / Spec-Kit / Lenny /
Amazon PR-FAQ, 12 chapters are identified (streamlined for the AI era).

| # | Chapter | Required | One-line Purpose | Corresponding Brainstorming Question |
|---|---------|:--------:|-----------------|--------------------------------------|
| 1 | Document info | ★ | Who, when, what changed | — |
| 2 | Background and objectives (Why) | ★ | Why build it; what to achieve | Q1 |
| 3 | Target user personas | ★ | Who it's for | Q2 |
| 4 | User stories | ★ | In what context users engage | Q3 |
| 5 | Feature scope / Out-of-Scope | ★ | What to build; what not to build | Q4 |
| 6 | Detailed feature description (input/output/boundaries) | ★ | How each feature behaves | Q5 |
| 7 | Non-functional requirements (quantified) | ★ | Quality floor | Q6 |
| 8 | UI links (Figma + key screens) | ☆ | What it looks like | — |
| 9 | Acceptance criteria (Given/When/Then) | ★ | How to know it's done | Q7 |
| 10 | Priority / MVP (MoSCoW) | ★ | What to build first | Q8 |
| 11 | Metrics (North Star + kill switch) | ★ | How to know it succeeded | Q9 |
| 12 | Risks + Open Questions + dependencies | ★ | What is still uncertain | Q10, Q11 |

### AI-Friendly PRD Writing Tips

1. **Do not specify tech stack** (which framework / library / database) → that is for
   spec-kit `/plan`
2. **Write to AI-consumable precision**: exhaustively enumerate each feature's
   input / output / boundaries
3. **AC in Given/When/Then** → can be directly converted to test cases
4. **NFR must be quantified** → only then can AI generate testable code
5. **Explicit glossary** → list domain terms in a separate section; AI must not guess
6. **Append a self-check instruction at the end** → "After completion, please verify
   each AC in this PRD line by line"

### PRD Trigger Prompt (minimal version)

```
Based on the brainstorming convergence results and the research files under
specs/research/, use the prd-writer-universal-en Skill to write the PRD
(output to specs/prd.md).

⚠️ If specs/research/06-architecture-baseline.md exists:
The PRD should add an "Architecture Baseline" section that carries over the
reuse matrix from 06.
```

---

## IV. 7 Rules for Converting PRD → Spec-Kit

### Key Facts

- **`/speckit.specify` is designed at the feature level** — it processes one feature
  at a time, not an entire PRD
- **`/speckit.specify` input requirement**: a high-level prompt focused on What & Why;
  do not include technical details

### Three Main Conversion Modes

| Mode | How | Best for |
|------|-----|----------|
| A. Feed entirely | Give the full PRD to `/specify` | Small MVP projects (< 5 core features) |
| **B. Split by feature** (recommended) | Run each Must-have through `/specify` separately | Medium to large projects |
| C. PRD as context | Place PRD under `.specify/memory/`; each specify run references it | Multi-person collaboration, frequently changing requirements |

### 7 Rules to Follow When Writing the PRD (to prepare for Spec-Kit)

1. **Write each Must-have feature as a self-contained `/specify`-ready unit**
   - One feature per section; input / output / boundaries / AC all self-contained
   - Do not cross-reference other feature sections with "see above"

2. **AC in Given/When/Then**
   - Can be directly converted to test cases by `/specify`
   - At least 1 normal path + 1 error path

3. **Exhaustively enumerate boundary conditions**
   - AI will not infer from omission
   - If you don't say a feature is out of scope, AI may add it anyway

4. **Tag each feature with a Phase (sweet spot: 5–15 minutes of work)**
   - Too large → split; too small → merge

5. **Explicit glossary**
   - List domain terms in a separate section
   - All domain-specific terminology must be defined

6. **Data examples**
   - Provide JSON or table examples for inputs/outputs
   - AI aligns directly; no guessing required

7. **Append a self-check instruction at the end**
   - "After completion, please verify each AC in this PRD line by line and report
     any uncovered items"

### Spec-Kit Trigger Prompt (run once per Must-have)

```
Implement <feature name> from specs/prd.md; run the full spec-kit workflow:
/speckit.specify → /speckit.plan → /speckit.tasks → /speckit.implement
```

⚠️ **Critical workflow constraint**:
- Run separately per Must-have — do NOT feed the entire PRD to /speckit.specify
  (context will overflow)
- /speckit.specify will pull material from specs/prd.md itself; do not copy PRD
  content into the prompt

---

## V. Three Common Anti-Patterns

| # | Anti-Pattern | Consequence | Remedy |
|---|--------------|-------------|--------|
| 1 | Skipping brainstorming and writing PRD directly | PRD will inevitably diverge (research only answers "what can be built", not "what should be built") | Enforce brainstorming to converge the 11 questions |
| 2 | Skipping PRD and running `/speckit.specify` directly | Spec lacks business context; AI will fill in incorrect default assumptions | Write PRD first, then specify |
| 3 | Feeding the entire PRD to `/speckit.specify` | Context overflow; spec loses focus | Split by feature; run each Must-have separately |

---

## VI. Sources

1. Sean Grove (OpenAI) — The New Code: "Specifications are the source, code is the output"
2. GitHub Spec-Kit repository https://github.com/github/spec-kit
3. Addy Osmani — How to write a good spec for AI agents
4. David Haberlah — How to write PRDs for AI Coding Agents
5. Atlassian — Product Requirements Document Guide
6. Aakash Gupta — PRDs: A Modern Guide
7. Lenny Rachitsky — Examples and templates of 1-Pagers and PRDs
8. Amazon PR-FAQ format
9. ProductSchool PRD templates
