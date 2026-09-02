---
name: adversarial-architecture-selection-universal-en
description: Evaluate multiple architecture, framework, library, open-source, SaaS, or vendor candidates through a five-role courtroom-style adversarial process and produce an evidence-backed architecture baseline decision. Use when a technical choice has multiple credible candidates and bias-resistant comparison is valuable. Do not use for single-candidate checks or purely product-level decisions.
license: MIT
metadata:
  version: "1.0"
  lang: en
  stage: "1.3"
  standalone: true
  produces:
    - "specs/research/06-architecture-baseline.md"
    - "specs/research/debate/*.md"
  requires:
    - name: "specs/research/03-open-source-candidates.md"
      level: orchestration
      fallback: "Ask the user to supply the candidate list and each candidate's sources directly"
    - name: "specs/research/04-implementation-options.md"
      level: orchestration
      fallback: "Same as above; when missing, fewer adversarial dimensions are covered but the process still holds"
    - name: "Parallel agent capability"
      level: optional
      fallback: "Play each role serially; output structure is unchanged but it takes longer"
---

# Adversarial Architecture Selection (Universal)

## Overview

Standardizes "multi-candidate technology architecture selection" into a **courtroom-style
5-role adversarial research** process. Prefer the current AI coding tool's multi-agent or team
mechanism so Advocates, Red Team, and Integration Assessor can challenge one another through
messages or shared artifacts, with the main agent acting as Lead Judge.

**This version (Universal) is domain-agnostic**: the core methodology is identical to the original, but all examples and references have been stripped of any domain-specific presets (e.g., A-share quant, financial toolchains), making it directly applicable to any technology selection scenario.

Its position in the Vibe Coding workflow (5-stage chain):

```
Project Research Kickoff (product-research-kickoff-universal-en)
   ↓
★ Adversarial Research (this Skill, optional — strongly recommended for multi-candidate)
   ↓
Brainstorming (product direction convergence)
   ↓
PRD (prd-writer-universal-en)
   ↓
Spec-Kit (/specify → /plan → /tasks → /implement)
```

**What it is not**: not a single-agent devil's advocate (too lightweight), not brainstorming (that's for divergent-convergent product direction), not a PRD writing tool.

**Why adversarial**: single-agent architecture evaluation has strong "advocate bias" — any project can be praised endlessly while flaws are glossed over. In multi-candidate selection, this bias distorts critical decisions. Multi-agent courtroom debate is the industry best practice (D3 / MAD-M² / AgentCourt) for countering this bias.

---

## Core Principles

### 1. Fixed 5-Role Team, Regardless of Candidate Count N

```
3 Advocates + 1 Red Team + 1 Integration Assessor = 5 teammates (officially recommended sweet spot)
```

When candidate count N > 3, Advocates **serially own** multiple projects internally (without breaking team size). When N=2, the 3rd Advocate degrades to a "backup Red Team" to strengthen the opposition.

### 2. Adversarial Happens at the Paper Level, Not the Teammate Level

Red Team and Integration Assessor **challenge each position paper individually** — total challenges = 3N, scaling linearly with N, but teammate count remains fixed. This is the key design that supports any N.

### 3. Anti-Bias is a Hard Constraint (Not a Suggestion)

- Every paper must include a "Fatal Flaw Disclosure" (mandatory self-attack)
- Papers are **shuffled in random order** when submitted in Phase 2 (prevents positional bias)
- Each challenge response is ≤ 200 words (prevents length bias)
- Lead is **prohibited from expressing opinions** during Phase 2 (prevents authority bias)
- See [references/anti-bias-guardrails.md](references/anti-bias-guardrails.md) for detailed academic justification

### 4. Lead Judge Only Delivers the Final Verdict, Does Not Participate in Debate

The main agent **only observes** throughout Phase 1/2, and only in Phase 3 synthesizes all
papers + debate transcripts to write the architecture baseline decision. This follows
LLM-as-Judge best practices — the evaluator does not participate in producing the evidence.

### 5. Three-Phase Process Cannot Be Skipped

```
Phase 0: Candidate Assignment (task allocation, not elimination)
Phase 1: Independent Deep Dive (5 agents in parallel, no inter-communication)
Phase 2: Courtroom Debate (inter-agent messaging, 1-2 rounds)
Phase 3: Lead Final Verdict (write the decision document)
```

---

## 5-Step Workflow

### Step 1: Determine Whether to Trigger This Skill

Applicable when: the user faces **multiple technology candidates** and needs to make a selection decision. Common scenarios:
- Multiple open-source projects (≥ 2) to consider forking, unsure which to choose
- Multiple SaaS / cloud vendor comparisons (e.g., Vercel vs Netlify, Datadog vs Grafana)
- Tech stack showdowns (e.g., React vs Vue vs Svelte)
- Open-source library selection (e.g., LangChain vs LlamaIndex vs Haystack)
- Multiple architecture pattern comparisons (e.g., Celery vs RQ vs Dramatiq)
- Research is complete but technical decisions remain contested

Not applicable:
- Single candidate, no comparison → no adversarial needed
- Pure product decisions (features/users/priorities) → use brainstorming
- Already have a strong preference and just want confirmation → use the single-agent devil's advocate Skill (lighter weight)

📖 **When to read [references/debate-protocol.md](references/debate-protocol.md)**: read when more detailed scenario determination is needed for the trigger decision.

### Step 2: Confirm Prerequisites + Choose an Execution Mode

Confirm that the user can provide a candidate list, from research artifacts or directly.
Then choose the best mode supported by the current tool:

- **Native Team mode (preferred)**: multi-agent execution, role isolation, and inter-agent
  messaging are available; run the five-role process directly.
- **Independent-task compatibility mode**: sub-agents/tasks are available but messaging is not;
  produce Phase 1 papers in parallel, then have the main agent shuffle and relay Phase 2
  challenges and responses.
- **Serial role-simulation mode (fallback)**: no sub-agent support; run five isolated role
  contexts or files serially and never leak the Judge's opinion into role outputs.

Claude Code Agent Teams may be enabled when that environment is used, but it is not a universal
prerequisite for this Skill.

### Step 3: Phase 0 Candidate Assignment

Read the candidate list and assign to 3 Advocates according to the table below:

| N | Assignment | Notes |
|---|------------|-------|
| 0 or 1 | Terminate process (no adversarial needed) | — |
| 2 | Advocate 1/2 each own 1 project; Advocate 3 becomes "Backup Red Team" | Strengthens opposition |
| 3 | 1 Advocate = 1 project (ideal state) | — |
| 4 | 1 Advocate owns 2 projects, others own 1 each | Merge projects with similar stacks |
| 5 | 2/2/1 split | — |
| 6+ | Even distribution | Rare |

Assignment principle: merge projects with **similar tech stacks/positioning** to the same Advocate; assign projects with **large differences** to different Advocates.

Write to `specs/research/debate/00-task-assignment.md`.

### Step 4: Create 5 Isolated Roles

📖 **When to read [references/role-spawn-templates.md](references/role-spawn-templates.md)**:
read when creating roles. In Native Team mode, spawn them directly; in compatibility modes,
use the same templates for independent tasks or isolated role passes.

5 teammates:
- Teammates 1-3: Project Analysts (Advocates)
- Teammate 4: Red Team (Devil's Advocate)
- Teammate 5: Integration Assessor

📖 **When to read [references/7-dimensions-framework.md](references/7-dimensions-framework.md)**: read when assembling the Advocate prompt, to inline the 7-dimension deep-dive framework into the spawn prompt.

### Step 5: Execute 3 Phases + Final Verdict

📖 **When to read [references/debate-protocol.md](references/debate-protocol.md)**: read when executing the 3 phases, to drive teammates according to the protocol.

**Phase 1** (Independent Deep Dive): 5 agents write papers in parallel, no inter-communication.
**Phase 2** (Courtroom Debate): papers enter the mailbox (randomly shuffled); Red Team issues 3 challenges per paper; Integration Assessor issues 1 challenge per single-fork paper; Advocates respond to each challenge (≤ 200 words per response); 1-2 rounds.
**Phase 3** (Lead Synthesis): write `specs/research/06-architecture-baseline.md`, update `05-decision-summary.md → v2`.

📖 **When to read [references/anti-bias-guardrails.md](references/anti-bias-guardrails.md)**: read before Phase 2 starts to confirm all anti-bias hard constraints are enforced.

---

## Complete Examples

📖 **When to read [references/examples.md](references/examples.md)**: contains 3 end-to-end examples from different domains (async task framework fork selection, AI/LLM library selection, SaaS monitoring platform selection), demonstrating the consistent applicability of the methodology across different scenarios. Read when: **The third (SaaS monitoring platform) and the cross-scenario comparison table are in [references/examples-saas.md](references/examples-saas.md).**
- User is doing open-source fork selection → refer to Example A
- User is doing pure library selection (no source code to read, purely documentation/community research comparison) → refer to Example B
- User is doing SaaS/cloud vendor selection → refer to Example C

---

## What Not to Do

- ❌ Do not skip Phase 0 and spawn directly — wrong candidate assignment corrupts everything downstream
- ❌ Do not let Lead express opinions in Phase 2 — authority bias causes teammates to follow the crowd
- ❌ Do not let Advocates write "hedged" papers — every paper should argue as if this is the only option
- ❌ Do not omit the "Fatal Flaw Disclosure" — this is the core mechanism for anti-bias
- ❌ Do not submit papers to Lead in their original order — must be randomly shuffled
- ❌ Do not exceed 2 rounds of debate — marginal returns drop sharply, token costs spike
- ❌ Do not reduce the team size when N=2 — add a backup Red Team to maintain balance

---

## Output Format Requirements

Final deliverables:
- `specs/research/debate/00-task-assignment.md`
- `specs/research/debate/position-paper-{name}.md` × N
- `specs/research/debate/red-team-position.md`
- `specs/research/debate/integration-assessment.md`
- `specs/research/debate/debate-transcript.md`
- `specs/research/06-architecture-baseline.md` ⭐ Final output
- `specs/research/05-decision-summary.md (v2)` ⭐ Synchronized update

---

## Trigger Keywords

**English**: architecture decision / tech selection / framework comparison / vendor evaluation / adversarial review / multi-candidate selection / fork decision / architecture selection / tech stack showdown / help me decide between X and Y / SaaS selection / library selection / adversarial research / multi-candidate evaluation / multi-project composite

---

## Relationship with Other Skills

- **`product-research-kickoff-universal-en`** (upstream): after completing research, if the candidate list has multiple candidates, trigger this Skill
- **`brainstorming`** (downstream): after this Skill produces the architecture baseline decision, brainstorming converges on MVP direction
- **`prd-writer-universal-en`** (further downstream): after brainstorming, the "Architecture Baseline" section of the PRD directly references this Skill's output
- **Single-agent devil's advocate Skill**: a lightweight alternative to this Skill; use it for single-candidate scenarios

## Upstream Artifacts

| Artifact | Level | When missing |
|---|:---:|---|
| `specs/research/03-open-source-candidates.md` | orchestration | Ask the user to supply the candidate list directly |
| `specs/research/04-implementation-options.md` | orchestration | Fewer adversarial dimensions are covered; the process still holds |
| Parallel agent capability | optional | Play each role serially |

## Downstream Consumers

| Consumer | What it takes from this skill |
|---|---|
| MVP convergence Skill | `06-architecture-baseline.md` as a boundary that MUST NOT be reopened |
| PRD writing Skill | The comparison matrix and the reasons the rejected options were rejected |

## Standalone Use

**What you provide**: at least 2 candidate options and their sources. With only 1 candidate this Skill does not apply — there is nothing to argue against.

**What you get**: a full record of the courtroom-style adversarial process plus one architecture baseline decision, including the refutations that defeated the rejected options.

**What you don't get**:

- **Does not apply with fewer than 2 candidates**; the Skill says so outright instead of forcing the process through.
- No product decisions, technology selection only.
- Without parallel capability it takes substantially longer, though the output structure is unchanged.

**Gate**: the main agent rules at the end of each debate round; when the material is insufficient or a candidate does not hold up, it **pauses explicitly** and MUST NOT guess.
