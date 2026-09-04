---
name: product-research-kickoff-universal-en
description: Guide pre-launch research for a 0-to-1 product through Socratic intake, four parallel research tracks, dual-source verification, and one convergence report. Use for new-product fact finding, competitor scans, resource discovery, open-source landscape review, and implementation-option research. Do not use for post-selection implementation work, pure academic research, or routine iteration of an existing product.
metadata:
  version: "1.0"
  lang: en
  stage: "1"
  standalone: true
  produces:
    - "specs/research/01-product-shape.md"
    - "specs/research/02-key-resources-and-dependencies.md"
    - "specs/research/03-open-source-candidates.md"
    - "specs/research/04-implementation-options.md"
    - "specs/research/05-decision-summary.md"
  requires:
    - name: "The user's project idea or rough direction"
      level: required
    - name: "specs/research/00-project-input-and-assumptions.md"
      level: orchestration
      fallback: "Ask the user to supply the confirmed information directly; with none, leave the candidate section empty"
    - name: "Parallel agent capability"
      level: optional
      fallback: "Run the same task boundaries serially instead; output requirements are not lowered"
    - name: "Research retrieval MCP"
      level: optional
      fallback: "Degrade to single-path retrieval and label the artifacts 'single-path retrieval only, not cross-verified'"
---

# Product Research Kickoff (Universal)

## Overview

Standardizes "pre-launch research for a new product" into a **reusable meta-methodology**:
4 independent research themes running in parallel + dual search engine cross-verification +
1 convergence summary. Input is the user's rough idea; output is 5 research documents +
prompts that drive the current AI coding tool to complete them through parallel agents/tasks,
or an equivalent isolated serial fallback.

**Design principle: domain-neutral, market-neutral.**
- The research skeleton (4 themes) applies to all product types
- Search tools are determined dynamically in Step 2 based on the target market — not hardcoded
- Examples are for guidance only, not constraints

Its position in the Vibe Coding workflow (5-stage pipeline):

```
Idea → [This Skill: Launch Research]
       → ★ Adversarial Research (adversarial-architecture-selection-universal-en,
            strongly recommended when multiple candidates exist)
       → Brainstorming (direction convergence)
       → PRD (prd-writer-universal-en)
       → Spec-Kit (/specify → /plan → /tasks → /implement)
```

⚠️ When `03-open-source.md` recommends multiple candidates (N ≥ 2), or research reveals
a need to choose among multiple technical approaches, it is **strongly recommended** to
run the `adversarial-architecture-selection-universal-en` Skill before brainstorming to produce an
architecture baseline decision.

**What this Skill is NOT**: not a PRD writer (use `prd-writer-universal-en`), not a technical design
tool (that is the spec-kit `/plan` phase), not brainstorming (brainstorming diverges and
converges directions; this Skill does factual groundwork).

**Why brainstorming must come in between**: Research only answers "what can be built and
what resources exist" — **it does not answer "which version should I actually build"**.
Jumping from research directly to PRD = picking blindly from all possibilities.
Brainstorming uses Socratic follow-up questions to converge the direction into a clear MVP,
only then can the PRD be written without diverging.

---

## Core Principles

### 1. 4 parallel tracks + 1 convergence track is the fixed skeleton

All new product launch research uses:

```
Theme 1: Product Form      → competing products / IA / interaction patterns / AI features / delivery form → save to 01-product-shape.md
Theme 2: Key Resources     → channel inventory / per-channel facts / mainstream choices / recommendation + backup → save to 02-key-resources-and-dependencies.md
Theme 3: Open-Source Ecosystem → project inventory / project facts / puzzle pieces / reuse combinations → save to 03-open-source-candidates.md
Theme 4: Implementation Plan   → module breakdown / per-module option comparison / recommended tech stack → save to 04-implementation-options.md
──────────────────────────────────────────────────────────────────────────────────────────
Summary: 05-decision-summary.md (depends on all 4 prior docs, runs serially at the end)
```

The 4 themes have **no dependencies** on each other — 4 sub-agents can run simultaneously.

### 2. Use Socratic Q&A to extract the project skeleton — don't make the user write it

When users face a new topic, the hardest part is not searching but "knowing which 4 angles
to search from". The core value of this Skill is **helping users articulate the skeleton
through guided questioning**.

### 3. Dual-path research spec: select tools dynamically based on target market

Each sub-agent must use two search paths simultaneously for cross-verification:

- **Path A (General)**: Claude built-in `WebSearch` / `WebFetch`
  → covers English sources, GitHub, international official docs, overseas communities
- **Path B (Specialized)**: choose the appropriate tool based on the target market
  established in Step 2:

| Target Market | Path B Recommended Tool | Coverage Focus |
|---------------|------------------------|----------------|
| Mainland China primary | muyu-search-mcp | Chinese sources, domestic products, Zhihu, domestic compliance |
| Overseas market primary | WebSearch (with English search terms) + Reddit/HN | English communities, Product Hunt, G2 |
| Global / mixed | Both paths use general WebSearch with separate Chinese/English search terms | Bilingual coverage |
| Internal tool / personal use | Single path (Path A) only, no Path B needed | — |

⚠️ The Path B tool is not hardcoded — it is determined by the target market and explicitly
written out when generating the final prompt.

### 4. The 4 themes are "slots", not "hardcoded content"

The skeleton is fixed; what fills each theme is determined by the user's answers. Some
themes may not apply to certain projects (a purely front-end tool does not need a
"data sources" theme) — replacement is allowed, but the user must be informed first.

---

## 5-Step Workflow

### Step 1: Determine whether to trigger this Skill

Applicable: the user describes a **new product idea** and has not yet done systematic research.

Not applicable:
- The idea is too vague ("I want to build an app") → do brainstorming first to diverge
- Research output already exists → go to brainstorming (do not jump straight to PRD)
- This is a minor iteration on an existing product → use brainstorming

### Step 2: Socratic Q&A to extract the skeleton

📖 **When to read [references/socratic-questions.md](references/socratic-questions.md)**:
Read at the start of every Skill invocation; guide the user through 6 core questions.

Key principles:
- **Ask only 2-3 questions at a time**; wait for the user's answers before asking the next batch
- **Multiple-choice A/B/C questions are preferred** over open-ended questions — less effort for the user
- **If the user answers vaguely, follow up** — do not fill in the blanks yourself
- Key output: 7 skeleton variables (see table below)

| # | Variable Name | Used In |
|---|---------------|---------|
| 1 | `<project one-liner>` | "Project positioning" section of all themes |
| 2 | `<target market>` | **Determines which Path B tool to use** |
| 3 | `<benchmark competitor list>` | Starting point for Theme 1 (Product Form) inventory |
| 4 | `<key resource type>` | Specific dimensions for Theme 2 (Key Resources) |
| 5 | `<open-source reuse intent>` | Whether to activate Theme 3 (Open-Source Ecosystem) |
| 6 | `<6-module list>` | Breakdown basis for Theme 4 (Implementation Plan) |
| 7 | `<path B tool>` | Derived from variable 2; written into the dual-path spec in the final prompt |

### Step 3: Fill the 4-theme template based on the skeleton

📖 **When to read [references/4-themes-template.md](references/4-themes-template.md)**:
Read after obtaining the user's skeleton; substitute skeleton variables into the
fillable placeholders for each of the 4 themes.

Fill order:
1. Theme 1 (Product Form) — filled with "benchmark competitors" and "target market"
2. Theme 2 (Key Resources) — "key resource type" determines the specific dimensions
3. Theme 3 (Open-Source Ecosystem) — "open-source intent" determines whether to activate
4. Theme 4 (Implementation Plan) — expand using "6-module list"

If a theme does not apply, tell the user explicitly and ask whether to replace it.

### Step 4: Generate the parallel research prompt

📖 **When to read [references/parallel-dispatch-spec.md](references/parallel-dispatch-spec.md)**:
Read when generating the final prompt; apply the dual-path research spec + Task
parallel dispatch spec.

Fixed structure of the final prompt:

```
# Research Task: <Project Name> · Product Launch Research

## Project Positioning
<One-liner definition given by the user in Step 2>

## 📁 Output Paths
<project directory>/specs/research/{01-product-shape,02-key-resources-and-dependencies,03-open-source-candidates,04-implementation-options,05-decision-summary}.md

## Research Theme 1: ... (filled from template)
## Research Theme 2: ...
## Research Theme 3: ...
## Research Theme 4: ...
## Final Decision Summary: ...

## 🔑 Output Quality Requirements (fixed)
## 🔀 Dual-Path Research Spec (dynamically filled based on <path B tool>)
## Parallel Execution Instructions (fixed)

## Next Steps (3-stage pipeline — do not skip steps)
```

### Step 5: Self-check + hand off to next stage

Self-check (5 items):
- [ ] Are the 4 themes truly independent of each other?
- [ ] Is the dual-path research spec written into the prompt, and does the Path B tool
      match the target market?
- [ ] Does the output use the standard `specs/research/` location?
- [ ] Does the prompt include the complete 3-stage pipeline
      (brainstorming → PRD → Spec-Kit) without jumping straight to PRD?
- [ ] Are all 3 trigger prompts provided so the user can copy and proceed?

📖 **When to read [references/handoff-to-prd.md](references/handoff-to-prd.md)**:
Read when the user asks "what comes after the research", "what goes into the PRD",
or "how to turn a PRD into a spec-kit".

**Handoff note**: After the research output is in place, **do not jump straight to PRD**.
Append the following to the end of the generated prompt:

```markdown
## Next Steps (follow this 3-4 stage pipeline — do not skip steps)

After research is complete (all 5 .md files saved), proceed in the following order:

### ⓪ If there are multiple candidate technical approaches → run adversarial research first (strongly recommended)

If 03-open-source.md recommends ≥ 2 candidate fork projects, or you are torn between
multiple tech stacks:

> I have multiple candidate technical approaches: [list candidates]
> Please use the adversarial-architecture-selection-universal-en Skill to make an architecture
> baseline decision.

Output: specs/research/06-architecture-baseline.md + 05-decision-summary.md (v2)

If there are 0 or 1 candidates → skip ⓪ and proceed directly to ①.

### ① Use the brainstorming Skill to converge the MVP direction

(Depending on whether ⓪ was completed, choose version A or version B from handoff-to-prd.md)

### ② Use the prd-writer-universal-en Skill to write the PRD

> Based on the brainstorming convergence results and the research files under
> specs/research/, use the prd-writer-universal-en Skill to write the PRD
> (output to specs/prd.md).

### ③ Use Spec-Kit to convert the PRD into executable specs (run once per Must-have)

> Implement <feature name> from specs/prd.md; run the full spec-kit workflow:
> /speckit.specify → /speckit.plan → /speckit.tasks → /speckit.implement

⚠️ Run separately per Must-have — do NOT feed the entire PRD to /speckit.specify.
```

---

## Complete Examples

📖 **When to read [references/examples.md](references/examples.md)**:
Read when the user needs a complete example reference, or is unsure how to fill
a particular theme. The file contains 3 end-to-end examples across different domains,
covering three typical scenarios: China-market software product, international SaaS tool,
and hardware/IoT product.

---

## Things NOT to Do

- ❌ Do not hardcode search tools for a specific market — Path B is determined by the target market
- ❌ Do not hardcode domain-specific competitors / data sources / push channels as defaults
- ❌ Do not make decisions on the user's behalf. This Skill only generates research prompts;
     facts are obtained by the sub-agents doing the research
- ❌ Do not skip Q&A to save time. If the skeleton is not clarified, the generated prompts
     will inevitably be empty platitudes
- ❌ Do not blend all 4 research tracks into one main-session pass. Prefer the current tool's
     native sub-agent / task mechanism; if parallel execution is unavailable, run the same
     isolated task boundaries serially without reducing output requirements

---

## Output Format Requirements

1. The final deliverable is **one complete parallel research prompt** (Markdown)
2. The user copies and pastes this prompt into the current AI coding tool to launch 4-agent
   parallel research, or the equivalent isolated serial fallback when parallelism is unavailable
3. Must include: project positioning + output paths + 4 themes + summary + quality requirements
   + dual-path spec (including specific Path B tool) + parallel execution instructions
   + next steps handoff
4. Line length ≤ 100 characters (for easier review)

---

## Trigger Keywords

**English**: kickoff research / product research / 0 to 1 research / new product discovery /
competitive research / feasibility research / help me research a new idea /
turn idea into research plan / scout competing products / scout data sources /
scout open-source ecosystem

**Chinese (for reference)**: 新项目立项 / 立项调研 / 产品调研 / 项目可行性 / 帮我调研一个新想法 / 我想做个 X 怎么开始调研 / 把想法变成调研计划 / 调研同类竞品 / 摸底数据来源 / 摸底开源生态

## Upstream Artifacts

| Artifact | Level | When missing |
|---|:---:|---|
| The user's project idea | **required** | Stop and ask |
| `specs/research/00-project-input-and-assumptions.md` | orchestration | Ask the user to supply the confirmed information directly |
| Parallel agent capability | optional | Run serially; task boundaries stay the same |
| Research retrieval MCP | optional | Single-path retrieval, explicitly labelled as not cross-verified |

## Downstream Consumers

| Consumer | What it takes from this skill |
|---|---|
| Architecture selection Skill | `03-open-source-candidates.md`, `04-implementation-options.md` |
| MVP convergence Skill | `05-decision-summary.md` |
| PRD writing Skill | All of 01-05 |

## Standalone Use

**What you provide**: a rough idea is enough. Existing competitor notes or interview transcripts can be pasted in directly.

**What you get**: research artifacts for 4 themes plus 1 decision summary; dual-engine cross-verification applies whenever the second path is available.

**What you don't get**:

- **No ledger maintenance** — three-state status tracking belongs to the project context ledger Skill.
- **No architecture verdict**; this skill supplies candidates and evidence only.
- When the second retrieval path is unavailable, the conclusions are **verified through a single path only**, and the artifacts say so.
