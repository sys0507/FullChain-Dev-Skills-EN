# Full-Chain Development Prompt Template (Pure Prompt Edition)

> This template covers the full development chain: project idea, research, requirements, specs, design, implementation, testing, retrospective, and deployment.
> Replace the placeholders below before use; a conditional stage that does not apply to the current project MUST be explicitly marked "skipped, with reason" — do not manufacture worthless artifacts just to complete the flow.
> Every "reusable asset" mentioned here is treated as an already-available, project-level Skill suitable for general-purpose projects.

## How to Use

1. This file preserves the original complete prompt of every stage; it exists mainly for consultation, explanation, and auditing. For actual execution, prefer [Full-Chain-Development-Prompt-Template-Skills-Edition.md](./Full-Chain-Development-Prompt-Template-Skills-Edition.md) in the same directory, which already marks the copy boundaries.
2. **First launch of a project**: copy "Global Input Context", "Global Execution Constraints", and the actual execution content of Stage 0 to the Agent, in that order. Template variables may be left blank; the minimum input can be a single sentence describing the project idea.
3. **Continuing later stages in the same session**: copy only the prompt that the current stage genuinely requires the Agent to execute; do not copy background narration, asset notes, or artifact examples. When the boundary is unclear, the "Execution Prompt (copy to the Agent)" marker in the copy template governs.
4. **Starting a new session or switching Agents**: if the Agent can read the project-level context files and `specs/research/00-project-input-and-assumptions.md`, supply only the current stage's prompt; otherwise supply "Global Execution Constraints" first, and add the latest "Global Input Context" as needed.
5. If the global rules are already written into `CLAUDE.md`, `AGENTS.md`, or the current tool's equivalent project-level file, do not re-paste them at every stage; the latest version in the project file governs.

## Template Variables (may be blank; filled in progressively by research)

### Global Input Context (copy to the Agent at first launch)

Copy this block at first launch. Afterwards, prefer letting the Agent read the continuously updated `specs/research/00-project-input-and-assumptions.md`; re-copy this block only when that file does not exist, cannot be read, or is clearly out of date.

You are **not required to fill in every variable at once** when the project begins. The minimum input can be a single `<PROJECT_IDEA>` sentence; the remaining variables are managed in one of three states:

- **User-confirmed**: explicitly provided by the user; may be used as the basis for later decisions.
- **Research candidate**: derived from market, user, technical, or source-code research; MUST carry evidence and a confidence level, and MUST NOT pose as user-confirmed fact.
- **To be confirmed**: evidence is currently insufficient; keep it as an Open Question and ask the user only when it actually affects scope, cost, or an irreversible decision.

If the user provides only one sentence of an idea, record it verbatim first; do not block the project because template variables are missing. Stage 1 is responsible for progressively discovering candidate answers, Stage 2 converges and confirms them through brainstorming, and Stage 3 writes the confirmed results into the PRD.

- `<PROJECT_NAME>`: project name
- `<PROJECT_IDEA>`: one-sentence project idea
- `<PROJECT_DESCRIPTION>`: background, pain points, target users, and expected value
- `<PROJECT_DEFINITION>`: one-sentence product/system positioning
- `<TARGET_USERS>`: target users or primary operators
- `<TARGET_PLATFORM>`: Web / mobile / desktop / CLI / API / SDK / data pipeline / embedded, etc.
- `<DOMAIN>`: business domain
- `<CORE_CAPABILITIES>`: 3-5 core capabilities
- `<KEY_RESOURCES>`: data, content, models, hardware, third-party APIs, or platform capabilities the project depends on
- `<BUDGET_AND_CONSTRAINTS>`: time, budget, compliance, team, and runtime-environment constraints
- `<REPO_OR_WORKSPACE>`: current project directory
- `<DESIGN_REFERENCE_DIR>`: directory of visual/interaction reference samples; when using Stitch it may be set to `design-reference/stitch-export`
- `<FEATURE_NAME>` / `<FEATURE_ID>`: current feature name and identifier

Maintain `00-project-input-and-assumptions.md` under `specs/research/`:

```markdown
# Project Input and Assumptions

## User-Confirmed
- PROJECT_IDEA: <the user's own words; rewriting their meaning is forbidden>

## Research Candidates
| Variable | Candidate | Evidence | Confidence | Awaiting user confirmation |
|------|--------|------|--------|------------|

## Open Questions
- <record only questions that cannot yet be answered reliably>

## Change Log
- <date>: <variable> moved from "candidate" to "confirmed", basis: <user confirmation / file path>
```

Rules for filling it in:

1. If a candidate answer can be obtained through research, research it first; do not throw every question back to the user.
2. When a single variable has several reasonable directions, give 2-3 candidates with evidence and impact, and let the user choose at the decision gate.
3. Ask immediately only when the missing information would block research, requires user authorization/private data, or would lead to a clearly different and hard-to-reverse path.
4. Candidates not confirmed by the user MUST NOT be written as settled fact; they may be used to form conditional option comparisons.
5. Update this file at the end of every stage so later stages know what is confirmed and what is still an assumption.

## General Execution Rules

### Global Execution Constraints (copy to the Agent at first launch or in a new session)

Copy this block at first launch. Copy it again in a new session, when switching Agents, or when the Agent cannot read the project-level rule files; if the rules are already persisted into `CLAUDE.md`, `AGENTS.md`, or similar files, re-pasting them at every stage is unnecessary.

1. Read the upstream files designated by the current stage and `specs/research/00-project-input-and-assumptions.md` (when it exists) before executing the task; when facts are insufficient, research the verifiable parts first, then list Open Questions — fabrication is forbidden.
2. Every recommendation MUST state "why X was chosen and why Y was not", and MUST distinguish fact, inference, and unverified assumption.
3. Whenever external facts, prices, versions, licenses, policies, or platform capabilities are involved, you MUST search and cross-verify the latest information.
4. Stages connect through file artifacts; confirmed decisions MUST NOT be reopened downstream without cause.
5. You MUST pause wherever a user confirmation gate exists; where there is no gate and the information is sufficient, continue.
6. Web/UI, data sources, open-source reuse, multi-Agent, Docker, and the like are conditional capabilities — enable them only when the project needs them.
7. Tools and Skills are installed with project-level configuration by default and MUST NOT pollute the global environment; sensitive information MUST NOT be committed to version control.

# Stage 0: Project Initialization and Toolchain Configuration

- Create the project directory `<REPO_OR_WORKSPACE>`, initialize version control, and open it with the current AI coding tool.
- Scan the project type, existing files, and runtime environment, and produce a "needed / not needed / to be confirmed" toolchain configuration inventory.
- Selectively configure the following capabilities according to project need, and verify after configuration that they work in the current session:
  - Development status display: [claude-hud](https://github.com/jarrodwatts/claude-hud) (if using Claude Code), which can be personalized via `~/Assets/configs/claude-hud-config.json`.
  - Research retrieval: project-level `~/Assets/mcp/ml-search-mcp` or an equivalent research MCP; read its README and install it through the guided flow.
  - Engineering workflow: [Superpowers](https://github.com/obra/superpowers), [Spec-kit](https://github.com/github/spec-kit).
  - Visual implementation: [stitch-skills](https://github.com/google-labs-code/stitch-skills) (only when the project contains a compatible visual interface).
  - Browser debugging and testing: [gstack](https://github.com/garrytan/gstack) (only when the project involves Web/browser scenarios).
  - Agent Teams (only when the current tool supports it and the work can be parallelized safely).
- All installations are scoped to the current project by default; you MUST NOT modify other projects or global configuration.
- Record enabled capabilities, versions, verification commands, and failed items. Mark unknown or inapplicable capabilities explicitly — do not pretend they are in place.

# Stage 1: Project Kickoff Research and Architecture Baseline

## 1.1 Project Idea

Start by recording what the user has already provided. The user may give only one sentence; do not require them to complete the whole table before research begins.

Minimum launch input:

- One-sentence idea: `<PROJECT_IDEA>` (the only variable recommended to have at the start)

Optional input (record it when the user has provided it; otherwise mark it "to be researched" and do not block):

- Description: `<PROJECT_DESCRIPTION>`
- Positioning: `<PROJECT_DEFINITION>`
- Target users: `<TARGET_USERS>`
- Target platform: `<TARGET_PLATFORM>`
- Core capabilities: `<CORE_CAPABILITIES>`
- Key resources and constraints: `<KEY_RESOURCES>`, `<BUDGET_AND_CONSTRAINTS>`

Execution requirements:

1. Create or update `specs/research/00-project-input-and-assumptions.md`, separating the user's own words, research candidates, and open questions.
2. Distill an "initial research boundary" from the existing input; it may be broad, but conjecture MUST NOT be written up as user requirements.
3. For variables that can be discovered through competitor, user-scenario, technology-ecosystem, or constraint research, propose candidate answers in research files 01-04.
4. Ask me first only when the missing information would send research in a completely different direction, requires authorized access, or could waste substantial cost; leave the rest for consolidated convergence in Stage 2.

## 1.2 Entering the Project Research Stage

How to start when variables are missing:

- `<PROJECT_NAME>` unconfirmed: generate a **temporary project codename** from the user's one-sentence idea and mark it "renameable" in `00-project-input-and-assumptions.md`.
- `<PROJECT_DEFINITION>` unconfirmed: write a **broad research hypothesis** based on the original idea, explicitly marked "used only to scope this round of retrieval; does not represent user confirmation".
- `<TARGET_USERS>`, `<TARGET_PLATFORM>`, `<CORE_CAPABILITIES>` unconfirmed: fold "identify candidate users, platforms, and capability combinations" into the product-shape research; do not lock them in early.
- `<KEY_RESOURCES>`, `<BUDGET_AND_CONSTRAINTS>` unconfirmed: actively discover candidate constraints during key-resource and implementation-option research; ask only when private information, authorization, or a hard user budget is involved.

You MUST NOT use an unfilled placeholder verbatim as a search keyword. Extract neutral keywords from `<PROJECT_IDEA>`, use a broad-to-narrow retrieval strategy, and keep a record of how the retrieval converged.

### Research Task: `<PROJECT_NAME>` · Product and Technology Kickoff Research

#### Project Positioning

`<PROJECT_DEFINITION>`; if it is not yet confirmed, use the broad research hypothesis generated above and mark its status here.

#### 📁 Research File Output Path

`<current project directory>/specs/research/`

```
research/
├── 00-project-input-and-assumptions.md
├── 01-product-shape.md
├── 02-key-resources-and-dependencies.md
├── 03-open-source-candidates.md
├── 04-implementation-options.md
└── 05-decision-summary.md
```

#### Research Topic 1: Product Shape and User Experience

These questions MUST be answered, each with checkable evidence (screenshot description / link / real product name / public material):

1. Inventory of comparable products or alternatives: at least 5-10 representative products in the target market; if there are fewer, state the actual number.
2. Information architecture or usage structure: how are entry points, primary navigation, core tasks, and key objects organized?
3. Interaction and workflow: when users complete the core task, what are the common industry paths, feedback, and exception handling?
4. Intelligence or automation cases (if applicable): how far do mature solutions go, and where are the limits?
5. Reach and result presentation: how are interface, report, notification, API, CLI output, and similar forms chosen?
6. Non-visual projects (API, SDK, library, data pipeline, and so on) MUST NOT force UI research; study developer experience, interface shape, and integration flow instead.

Output: `01-product-shape.md` — panorama of products/alternatives + a reference library of user or developer experience

#### Research Topic 2: Key Resources and External Dependencies

1. Inventory the key resources the project needs: data, content, models, third-party APIs, identity/authentication, payments, messaging channels, hardware, or platform capabilities.
2. For each resource, record the applicable fields:
   - Coverage and quality
   - Update frequency, real-time behavior, or performance
   - Rate limits, quotas, and scaling ceilings
   - Pricing and billing model
   - Registration, qualification, or hardware thresholds
   - License, commercial use, privacy, security, and redistribution boundaries
   - Availability, lock-in risk, and exit path
3. Real-world adoption: which options do target users or comparable developers commonly use, and why?
4. Recommend a primary option plus a fallback, and state the switching cost explicitly.
5. If the project has no external key resources, state the basis and reduce this topic to "runtime environment and dependency constraints"; fabricating data sources is forbidden.

Output: `02-key-resources-and-dependencies.md` — resource/dependency comparison table + recommended option + risks and alternative paths

#### Research Topic 3: Open-Source Projects and Reusable Implementations

1. Search for open-source projects related to comparable products, core modules, and infrastructure, targeting at least 10; when objectively fewer exist, output the actual number.
2. Check for every project:
   - Stars / latest commit / releases / license
   - Tech stack and runtime environment
   - Core capabilities and explicit weaknesses
   - Reusable modules, interfaces, or designs
   - Security, maintenance, and supply-chain risk
   - Integration difficulty (direct fork / use as dependency / extract module / reference only)
3. Draw the ecosystem map: which projects suit core capability, interface, infrastructure, testing, or deployment respectively.
4. Give a recommended combination of fork / depend / borrow / build.
5. If reusing an open-source implementation is not appropriate, you MUST justify it with evidence and keep a "fully self-built / managed service / commercial component" comparison.

Output: `03-open-source-candidates.md` — project list + reuse matrix + initial code baseline recommendation

#### Research Topic 4: Implementation Options

First split the system into 4-8 real modules based on `<PROJECT_DEFINITION>` and `<TARGET_PLATFORM>`; do not force a fixed architecture. Consider, but do not limit yourself to:

| Optional module | Research dimension |
|------|---------|
| Input / data ingestion | Acquisition, validation, cleaning, synchronization, or collection approach |
| Core domain logic | Key business rules, algorithms, workflows, or automation |
| State and storage | Persistence, caching, files, indexes, or stateless design |
| Interfaces and integration | API, events, plugins, devices, or third-party system boundaries |
| Experience layer | Web / App / CLI / SDK / reports; delete if not applicable |
| Notification and jobs | Messaging channels, scheduling, queues; delete if not applicable |
| Security and compliance | Authentication, authorization, privacy, auditing, and domain regulation |
| Deployment and operations | Local, cloud, serverless, edge, or on-device execution |

For every actual module, produce:

- 2-3 mainstream industry options + the pros and cons of each
- Recommended option + rationale (including "why not X")
- Contracts with and dependencies on other modules
- Rough effort, cost, and principal risks

Output: `04-implementation-options.md` — module option comparison + recommended tech-stack combination + end-to-end architecture diagram (Mermaid)

#### Final Decision Summary

Write `05-decision-summary.md`:

1. Product/system shape decision: how users or callers will use it
2. Key resource decision: primary option, fallback, and exit path
3. Open-source reuse decision: which parts to fork / depend on / borrow / build
4. Tech-stack decision: the choice for each module
5. Overall architecture diagram and the key data/control flows
6. Effort and running-cost estimates
7. Risks, assumptions, and questions still to be verified
8. Conditional-stage judgment: whether the later stages for UI, data sources, multi-Agent, containerization, and so on apply
9. Template-variable completion table: mark each item "confirmed / research candidate / to be confirmed", referencing `00-project-input-and-assumptions.md`

#### Output Quality Requirements

1. Every conclusion MUST have factual support — link / project name / data / source location
2. Every recommendation MUST carry a rationale — "why X was chosen, why Y was not"
3. Mark the retrieval date; volatile information such as versions, prices, and policies MUST come from the latest sources
4. When you do not know, write "unknown / to be confirmed" explicitly — do not make things up
5. Do not include low-quality candidates just to hit a count; when the count falls short, state the retrieval boundary

#### Determining the Technical Research Plan

Action: dispatch 4 independent sub-agents to run in parallel, each responsible for one research topic, with no dependencies between them. Use the current AI coding tool's sub-agent / Task capability to launch 4 parallel tasks in one round; if the environment does not support it, execute serially under the same output requirements.

##### Agent Dispatch List

- Agent 1, product shape and user experience research, outputs `specs/research/01-product-shape.md`
- Agent 2, key resources and external dependency research, outputs `specs/research/02-key-resources-and-dependencies.md`
- Agent 3, open-source project and reuse research, outputs `specs/research/03-open-source-candidates.md`
- Agent 4, implementation option research, outputs `specs/research/04-implementation-options.md`

##### Dual-Track Research Standard (every Agent MUST follow it)

While researching, every sub-agent MUST cross-verify using at least two mutually independent retrieval sources:

1. The current AI tool's built-in web search and page-reading capability
2. A configured research MCP or another independent retrieval source

For technical questions, prefer official documentation, source code, releases, issues, and the license text itself; for market information, prefer product websites, official pricing, and authoritative material.

##### After All 4 Agents Return

The main session performs the wrap-up:

- Read the 4 research artifacts
- Check for evidence conflicts, gaps, and staleness
- Synthesize and write `05-decision-summary.md`
- Update the candidates in `00-project-input-and-assumptions.md` with the research evidence, but MUST NOT promote a candidate to "user-confirmed" on your own authority

This step is not parallelized — it depends on the previous 4 artifacts and requires a global view.

## *Reusable Assets for 1.1-1.2*

Please extract and install the `~/Assets/skills/product-research-kickoff-universal-en` skill from my desktop into the current project, configured as a project-level Skill. Verify it once installed, and tell me how to trigger it.

## 1.3 Technology Selection via Adversarial Architecture

### Launch the Source-Code Adversarial Research Agent Team

#### Background

We have finished 5 kickoff research documents (specs/research/01~05.md); among them 03-open-source-candidates.md
recommends N candidate open-source projects, and we must decide which one to fork / what to reuse / what to build ourselves.

#### Task

Create an Agent Team with a courtroom-style adversarial structure to help me make the architecture baseline decision.
You are the Team Lead, acting as the judge; you take no part in the debate yourself and only deliver the consolidated ruling at the end.

---

#### ⭐ Global Standard: the 7-Dimension Deep-Dive Framework

Every position paper MUST be filled in against these 7 dimensions (none may be missing):

| # | Dimension | Content |
|---|------|------|
| 1 | Architecture overview | Mermaid diagram + main directory structure |
| 2 | Core capability inventory | What the project actually does (listed by capability) |
| 3 | Data model | Key classes / tables / interfaces |
| 4 | Extension points | Hooks, plugin slots, and configuration entries the design reserves |
| 5 | Modification cost estimate | How much code must change to turn the fork into the target product (person-days + risk) |
| 6 | ⭐ **Fatal-flaw self-disclosure** (mandatory) | The 3 biggest flaws of my project — **self-reported; failing to report counts as dereliction of duty** |
| 7 | Integration feasibility with the other candidates | vs Other_1 / Other_2: can cooperate / mutually exclusive / partially integrable |

Dimension 6 is the core anti-bias design — it forces the paper's author to self-report flaws, because
the opposing red team will dig them out sooner or later, and self-reporting always beats being exposed.

---

#### ⭐ Phase 0: Candidate Project Assignment (you MUST do this first)

Read `specs/research/03-open-source-candidates.md`, determine the candidate count N, and assign the projects to advocates according to this table:

| N | Assignment | Notes |
|---|---------|-----|
| **N = 0 or 1** | No adversarial research is needed; terminate the flow | — |
| **N = 2** | Advocates 1 and 2 each own 1 project; advocate 3 becomes a "backup red team" (strengthening the opposition) | 2 red teams vs 2 papers, evenly matched |
| **N = 3** | 1 advocate = 1 project (the ideal case) | — |
| **N = 4** | 1 advocate owns 2 projects, the other 2 advocates own 1 each | Merge projects with a similar tech stack or positioning under the same advocate |
| **N = 5** | A 2/2/1 split | — |
| **N ≥ 6** | Split evenly (e.g. N=6 → 2/2/2, N=7 → 3/2/2) | Fairly rare |

**Assignment principle**: projects with a similar tech stack or positioning go to the same advocate (easier to compare and choose);
projects that differ widely go to different advocates (preserving debate diversity).

**Write the assignment result** into `specs/research/debate/00-task-assignment.md`:

- Advocate 1 owns: [project A, project D] (reason: similar tech stack or core architecture)
- Advocate 2 owns: [project B]
- Advocate 3 owns: [project C, project E] (reason: similar interaction or integration architecture)

Once the assignment is settled, spawn 5 teammates.

---

#### Team Composition (fixed at 5 members, whatever N is)

##### Teammates 1-3: Project Analysts (each owns 1+ project, deep-diving serially)

- Role: project analyst + forceful advocate
- Required reading: specs/research/03-open-source-candidates.md + the source code of the projects they own
- Stance: **hold the line for every project they own**, yielding only to the Lead's ruling
- Output (Phase 1): write an independent position paper for **every project** they own
   - `position-paper-{project-name}.md`
   - Filled in against the 7 dimensions above
   - Dimension 6, "fatal-flaw self-disclosure", is mandatory; omitting it counts as dereliction of duty
   - ⚠️ When writing several papers, you MUST NOT "hedge" — write each one as if it were the only project you own
- Behavior (Phase 2): respond fully to every challenge each of your papers receives; abandoning any one of them is forbidden

##### Teammate 4: Red Team (devil's advocate, fixed at 1; add 1 more when N=2)

- Role: oppose every existing option and argue for "build it all ourselves" or "change the approach"
- Required reading: 03-open-source-candidates.md + 04-implementation-options.md + a skim of the candidate projects
- Stance: **total negation** — you MUST NOT agree with any paper
- Output (Phase 1): `red-team-position.md`
   - List 3 fatal flaws for every candidate project (with source-code / issue / commit evidence)
   - An estimate for the "build it all ourselves" option (effort, risk, benefit)
   - A "change the approach" option (where applicable)
- Behavior (Phase 2): **send 3 challenges to each paper individually** (total = 3N, not 3 × the number of advocates)

##### Teammate 5: Integration Assessor (fixed at 1)

- Role: assess the engineering feasibility of composing several projects
- Required reading: 04-implementation-options.md + the architecture of the candidate projects
- Stance: **neutral but empirically grounded** — take no side; let the data speak
- Output (Phase 1): `integration-assessment.md`
   - For every pairing (A+B / A+C / B+C / A+B+C and so on), assess:
      integration boundary / data-flow conflicts / version conflicts / total modification cost / operational complexity / recommendation score (1-10)
   - Produce an overall ranking and list the top 3 combinations (including the "build it all ourselves" control)
- Behavior (Phase 2): raise a composition challenge against every "single-fork camp" paper (at most 1 per paper)

---

#### The Three-Phase Flow

##### Phase 1: Independent Deep Dive (5 teammates in parallel, no communication)

- All teammates start at the same time, write up their required output, and then go idle
- An advocate deep-dives the projects they own **serially**, writing an independent paper for each
- Communication between any teammates during Phase 1 is **forbidden**
- Budget: ≤ 30 minutes per teammate (an advocate owning several projects may extend to 60 minutes)

##### Phase 2: Courtroom Debate (1-2 rounds, inter-agent messaging)

**The adversarial contest happens at the paper level, not the teammate level** — this is what lets a fixed team size support any number of candidates N.

Debate flow:

1. You (the Lead) broadcast all papers (N in total) to the mailbox in randomly shuffled order (to prevent position bias)
2. Red team → **send 3 challenges to each paper** (total = 3N), each backed by source-code / commit / issue evidence
3. Integration assessor → send 1 composition challenge to each "single-fork camp" paper
4. Each advocate → respond **point by point** to the challenges raised against each paper for the projects they own (≤ 200 words each)
   - Conceding part of a challenge is allowed
   - Counter-challenges are allowed
   - Skipping any challenge is forbidden
5. After a round completes, you judge whether a second round is needed:
   - A clearly dominant option has emerged → move to Phase 3
   - Still deadlocked → start round 2 (at most 2 rounds)

##### Phase 3: Your Consolidated Ruling (no teammates involved)

After reading all papers + debate transcripts, write:

**`specs/research/06-architecture-baseline.md`**:

1. Decision summary: the chosen architecture baseline (single fork or multi-project composite)
2. Reuse matrix:
   | Module | Source | Treatment |
   |------|------|---------|
   | Core domain module | Project A | Reuse directly |
   | ... | ... | ... |
3. Rationale for rejected options:
   - Why project X was not chosen (which challenge defeated it; cite the line number in the debate transcript)
   - Why "build it all ourselves" was not chosen (which red-team argument was refuted)
4. Open Questions (for the brainstorming stage, at least 3)
5. Total modification cost estimate: person-days / monthly budget

**Update `specs/research/05-decision-summary.md` → v2**:

- Replace the "open-source reuse decision" section with this architecture baseline decision
- Adjust the "tech-stack decision" according to the reuse matrix
- Mark the v2 update time and reason at the top

---

#### ⚠️ Hard Anti-Bias Constraints

- Dimension 6, "fatal-flaw self-disclosure", is mandatory in every paper; omitting it counts as dereliction of duty
- Papers submitted to you in Phase 2 are **randomly shuffled** (to prevent position bias)
- Every challenge response is ≤ 200 words (to prevent length bias)
- You (the Lead) are **forbidden to take a position during Phase 2** — observe only, do not speak
- You (the Lead) may rule only on the basis of "surviving arguments", never on "which is longer / which spoke first"
- When an advocate owns several projects, **each paper is an independent, forceful argument** — you MUST NOT weaken any one of them
   in order to "hedge"

---

#### Team Cleanup

Once Phase 3 is complete, shut down all teammates and release the team's resources.

#### Start Now

1. Confirm that Agent Teams is enabled (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`)
2. Read 03-open-source-candidates.md and assign the candidate projects to advocates per the Phase 0 table
3. Write `specs/research/debate/00-task-assignment.md`
4. Spawn 5 teammates (attach the corresponding role definition when spawning; see the templates below)
5. Enter Phase 1

---

#### The 3 Companion Spawn Templates

##### Advocate Spawn Template

You are a project analyst and forceful advocate, assigned to deep-dive the following projects:

- Project 1: {PROJECT_1_NAME} ({PROJECT_1_LOCAL_PATH or GitHub link})
- Project 2: {PROJECT_2_NAME} (where applicable)
- ...

###### Required Reading

- specs/research/03-open-source-candidates.md
- The source code of every project you own

###### Stance

You **completely believe, for every project you own**, that it is the best option for building
<{PROJECT_DEFINITION}>. You do not yield unless the Lead judge rules otherwise.

⚠️ When you own several projects:

- Each paper is an independent, forceful argument
- You MUST NOT weaken any one of them in order to "hedge"
- Write each one as if "this is the only project I own"
- But you may be honest — if a project has a flaw, self-reporting always beats having the other side dig it out

###### Phase 1 Output: an independent paper for each project you own

- `specs/research/debate/position-paper-{project-name}.md`
- Filled in against the 7 dimensions (see the Lead's launch prompt)
- Dimension 6, "fatal-flaw self-disclosure", is mandatory

###### Phase 2 Behavior

- The red team and the integration assessor **will challenge each of your papers individually**
- You MUST respond fully to every challenge each paper receives
- Abandoning any paper is forbidden

###### After Phase 1 Is Complete

Go idle once all papers are written. Do **not** initiate communication with other teammates — Phase 2 is started by the Lead.

##### Red Team Spawn Template

You are the red team (devil's advocate). Your stance is **opposition to every candidate project**, arguing that "build it all ourselves"
or "change the approach" is the best choice.

###### Required Reading

- specs/research/03-open-source-candidates.md
- specs/research/04-implementation-options.md
- The README + main directory structure of every candidate project (skim)

###### Stance

You do not believe in any fork option at all. Your job is to keep the "build it all ourselves" and "switch tech stacks"
options alive for the team rather than letting the advocates obscure them.

###### Phase 1 Output: `specs/research/debate/red-team-position.md`

**1. Fatal challenges against each candidate project**

3 fatal flaws per project, each backed by source-code / issue / commit-history evidence.

**2. Estimate for the "build it all ourselves" option**

- Effort (person-days)
- Principal risks
- Benefit relative to the fork options (if any)

**3. "Change the approach" option (optional)**

If a third path exists that neither forks nor builds everything (switching to SaaS, using low-code, and so on), write it down.

###### Phase 2 Behavior

**Send the 3 sharpest challenges to each paper individually** (total = 3N, not 3 × the number of advocates).
Challenges MUST be fact-based; ad hominem criticism is forbidden.

###### Counter-Rules

- You are forbidden at any point to say "project X is actually pretty good" — you are not here to split the difference
- You are forbidden to echo other teammates — you are the opposition by construction

###### After Phase 1 Is Complete

Write red-team-position.md and go idle.

##### Integration Assessor Spawn Template

You are the integration assessor, neutral in stance, and your job is to **assess the engineering feasibility of composing several projects**.

###### Required Reading

- specs/research/04-implementation-options.md
- The architecture overview of every candidate project (README / main directory structure)

###### Stance

You **take no side** — you favor no advocate and you do not join the red team. You let the data speak.

###### Phase 1 Output: `specs/research/debate/integration-assessment.md`

**For every pairing (A+B / A+C / B+C / A+B+C and so on), assess:**

1. **Integration boundary**: where the connection happens (API / files / database / process)
2. **Data-flow conflicts**: whether the data models can be joined up, and how many adapter layers it takes
3. **Version/dependency conflicts**: Python version / dependency library versions / Node version
4. **Total modification cost**: the extra effort of integrating several projects
5. **Operational complexity**: whether the combined option needs more infrastructure
6. **Recommendation score**: 1-10 (higher is more recommended)

**Overall ranking**

List every combination (including the "build it all ourselves" control) ranked by recommendation score, and mark the top 3.

###### Phase 2 Behavior

Raise a "why not compose?" challenge against every "single-fork camp" paper (at most 1 per paper,
attaching your score as the basis).

###### Counter-Rules

- You MUST NOT raise a score because an advocate argued well — only engineering facts count
- You MUST NOT echo the red team's "build it all ourselves" stance unless the data supports it

###### After Phase 1 Is Complete

Write integration-assessment.md and go idle.

---

#### The Companion Phase 2 Debate Trigger Prompt (issued by the Lead once Phase 1 is complete)

All teammates' papers are in place (N papers + the red-team position + the integration assessment).
Phase 2, the courtroom debate, now begins.

##### Phase 2 Flow

1. I (the Lead) broadcast all N papers to the mailbox in randomly shuffled order
   (shuffled order: {randomized order list})
2. Red team: **send the 3 sharpest challenges to each paper individually** (3N in total), delivered through the mailbox
   to the corresponding advocate. Every challenge MUST carry source-code / commit / issue evidence.
3. Integration assessor: send 1 composition challenge to each "single-fork camp" paper (with the scoring basis attached)
4. Each advocate: respond in the mailbox, **point by point**, to the challenges against the papers for the projects they own,
   ≤ 200 words each.
   - Conceding part of a challenge is allowed (it is no disgrace)
   - Counter-challenges are allowed
   - Skipping any challenge is forbidden
5. Once a round completes, all teammates go idle and I (the Lead) judge whether a second round is needed:
   - A clear consensus / dominant option has emerged → move to Phase 3
   - Still deadlocked → start round 2 (at most 2 rounds)

##### Start Now

Red team, begin the first round of challenges.

---

#### Key Artifacts and the Downstream Handoff

Phase 0 artifact:

```
specs/research/debate/
   └── 00-task-assignment.md              ← advocate-to-project ownership map
```

Phase 1 artifacts (N + 2 documents):

```
specs/research/debate/
   ├── position-paper-{project-A}.md     (owned by advocate X)
   ├── position-paper-{project-B}.md     (owned by advocate Y)
   ├── ... (N in total, per the candidate count)
   ├── red-team-position.md              (red team)
   └── integration-assessment.md         (integration assessor)
```

Phase 2 artifact:

```
specs/research/debate/
   └── debate-transcript.md              (the complete debate record)
```

Phase 3 artifacts (consolidated by the Lead):

```
specs/research/
   ├── 06-architecture-baseline.md       ← new
   └── 05-decision-summary.md (v2)       ← updated
```

## *Reusable Assets for 1.3*

Please install the `~/Assets/skills/adversarial-architecture-selection-universal-en` folder from my desktop into the current project, configured as a project-level Skill. Verify it once installed, and tell me how to trigger it.

# Stage 2: Trigger Brainstorming for Requirements Analysis and Converge the Research Documents

Read every research file under specs/research/ carefully, then use the Superpowers brainstorming Skill to help me converge on the MVP direction:

📂 Required reading (in priority order):

1. specs/research/00-project-input-and-assumptions.md   ⭐ confirmed input, research candidates, and open items
2. specs/research/06-architecture-baseline.md     ⭐ the locked architecture baseline, if Stage 1.3 actually produced it
3. specs/research/05-decision-summary.md (v2)   ⭐ the synthesis; when 06 was not produced, it is the primary decision basis
4. specs/research/04-implementation-options.md
5. specs/research/03-open-source-candidates.md
6. specs/research/02-key-resources-and-dependencies.md (if applicable)
7. specs/research/01-product-shape.md

⚠️ Brainstorming boundaries:

- If 06 exists, the architecture baseline is locked. Its reuse matrix and modification decisions are **not up for discussion** —
  they were settled by adversarial research, and brainstorming does not reopen the case. If Stage 1.3 was skipped for lack of candidates, the confirmed decisions in 05 form the boundary.
- Every Open Question from 00 and from 06 (if present) MUST **all carry over** into Q10 (do not lose any); new ones may be added.
- Must-have priority MUST reference the reuse matrix in 06 or the reuse decisions in 05 — capabilities that are "almost free" (directly reusable modules)
  go into the MVP first, and capabilities that are "expensive" (must be built) enter the MVP only with care.
- Converge every "research candidate" in 00 item by item: those that can be confirmed become "user-confirmed"; those that still cannot be confirmed stay Open Questions and MUST NOT be silently adopted.

Help me settle the following 11 questions (they are the input for writing the PRD):

[Why / What / What Not] (pure product decisions)

1. Business goals + product goals + Non-Goals (state explicitly what will not be done)
2. 1-2 primary personas + anti-personas (state explicitly who is not served)
3. 3-5 core user stories (INVEST format)

[Feature decisions shaped by the architecture baseline] (reference 06; reference 05 when 06 was not produced)

4. MVP feature list + Out-of-Scope list
   - Must-have items prefer capabilities marked "directly reusable" in the 06/05 reuse matrix
   - If adversarial research was run, Out-of-Scope should account for the capabilities touched by the "fatal flaws" the advocates self-reported
5. The key boundary conditions of every core feature (missing data / concurrency / failure — what happens?)
   - Boundary conditions MUST land inside what the confirmed architecture baseline can support

[How We Know It Is Done]

6. Non-functional requirements (performance / availability / compliance — numbers are mandatory)
   - Performance ceilings MUST reference the real capability of the confirmed architecture baseline
7. Acceptance criteria for every user story (Given/When/Then)
8. Priority (MoSCoW: Must/Should/Could/Won't)
   - Ordering MUST reference the modification cost in 06/05 (lower cost = higher priority)
9. North Star metric + shutdown line
   - The shutdown line MUST account for the scaling ceiling of the confirmed architecture baseline

[Still uncertain]

10. Open Questions (at least 3)
    - MUST include every Open Question left over from 00 and from 06 (if present)
    - New product-level Open Questions may be added
11. Dependencies and constraints (product-level — technical dependencies are governed by the final decisions in 06 or 05)
    - External APIs, compliance approvals, platform policies
    - Do not repeat the technical dependencies already in 06

⚠️ Topics that MUST NOT be reopened:

- The confirmed architecture baseline (which fork / composite solution) — 06 or 05 already decided it
- Technology selection (which framework / library) — that is left to spec-kit /plan
- Options already explicitly rejected in 06 or 05 — do not bring them up again

After brainstorming is complete, update the status and change log in `00-project-input-and-assumptions.md`, then move to Stage 3. For anything still unconfirmed but not blocking the MVP, mark the assumption and its validation plan explicitly in the PRD.

# Stage 3: Write the Final Requirements Document

Based on the brainstorming convergence results and the research files under specs/research/,
use the prd-writer-universal-en Skill to help me write the PRD (output to specs/prd.md).

Read `00-project-input-and-assumptions.md` before writing the PRD: only "user-confirmed" variables may be written as settled requirements; "research candidates" MUST be confirmed during brainstorming, and unconfirmed items may only enter Open Questions, risks, or assumptions to be verified.

## *Reusable Assets for Stage 3*

Please extract and install the `~/Assets/skills/prd-writer-universal-en` skill from my desktop into the current project, configured as a project-level Skill. Verify it once installed, and tell me how to trigger it.

# Stage 4: Run Spec-Kit to Generate the Spec Documents

Based on specs/prd.md, break every Must-have feature into the complete 4-step document set (specify / clarify / plan / tasks). This round produces documents only: write no code, touch no worktree, run no TDD.

## Step One: Split + Order (do not start until I confirm)

1. Split only the features marked Must-have in the PRD
2. Output the split table:
   | # | feature name | which PRD section it comes from | which features it depends on | document output directory |
   Directory format: specs/00X-<feature-slug>/
3. Order by dependency, then wait for me to confirm the order

## Run the full 4 steps for every feature, with an explicit artifact per step

### ① /speckit.specify → spec.md

- **Write What & Why only**; technical detail is forbidden (database choice, framework choice, and the like are left to plan)
- MUST contain: feature boundary / MVP constraints / runtime environment / business flow
- Extract from PRD section X: inputs, outputs, AC (Given/When/Then format), boundary conditions
- Length guidance: a complex business feature is typically 1500-2000 words; a simple feature is judged by full coverage of boundaries and acceptance criteria, not padded to hit a word count

### ② /speckit.clarify → update spec.md  MUST run

- Automatically scan the spec.md just generated and raise every ambiguity
- The 4 categories that MUST be scanned hardest:
   ① MVP boundary (what will not be done must be written down)
   ② API boundary (rate limits, failures, timeouts, quotas)
   ③ Data boundary (nulls, outliers, extreme scale)
   ④ Integration boundary (interaction assumptions with existing systems)
- Every clarify question MUST be traced to a concrete paragraph update in spec.md

### ③ /speckit.plan → plan.md

- The 5 mandatory items (none may be missing):
   ① Project file structure (paths + the core responsibility of each file)
   ② Data flow (as a mermaid diagram)
   ③ Dependency list (language versions, third-party library versions)
   ④ Integration points with existing systems (state explicitly which existing modules are reused and which are new)
   ⑤ Risk list (technical risks + mitigations)
- Reuse-first principle: whatever can be reused from the PRD architecture baseline MUST NOT be rebuilt

### ④ /speckit.tasks → tasks.md

- Split into 12-18 tasks by default; an atomic feature may have fewer, and beyond 18 tasks judge first whether it should be split into several features
- Every task MUST satisfy:
   ① Single responsibility (one task does one thing)
   ② Independently testable (explicit inputs and outputs)
   ③ Completable within a single clear, context-controlled implementation cycle; do not sacrifice quality to an unrealistic minute count
- Mark parallel groups (which tasks can run concurrently and which MUST be serial)
- Label every task with: [FR-X source] [dependency tasks] [output verification method]

## Hard Constraints (MUST NOT be violated)

1. The /specify step MUST NOT contain technology selection — technology selection belongs to /plan
2. /clarify is mandatory and MUST NOT be skipped — it is the core mechanism for surfacing hidden requirements
3. /plan MUST contain the 5 elements; missing any one requires rework
4. /tasks defaults to 12-18 tasks; any deviation MUST justify the feature's size, > 18 means splitting the feature first, < 12 requires proving it is still independently testable
5. The document directory MUST strictly follow the specs/00X-<feature-slug>/ format
6. After running the 4 steps for a feature, stop and show me; only after I confirm may you run the next feature

## What to Do When You Hit a Problem

- PRD is missing AC / boundaries / data samples → stop and ask me, do not invent them
- If I am also unsure about a question raised by /clarify → stop and ask me, do not decide on my behalf
- Integration point unclear → stop and ask me for the code path or documentation of the existing system, do not guess

## Output Cadence

- One feature completes 4 steps → pause → I confirm → next feature
- Do not run every feature in one go; the volume of documents would be too large to review one by one

Go ahead — for step one, output the split list + the recommended execution order.

# Stage 5: Experience and Interface Design (conditional stage)

If the project has no user-facing interface, interaction contract, or developer-experience design need, skip this stage and record the reason in the decision summary. If a different design tool is used, replace the Stitch name, export format, and paths below with that tool's equivalent artifacts, but keep the "design source of truth → reference samples → Spec write-back" logic.

## 5.1 Use a Professional Design Tool Suited to the Target Platform

If the project includes a Web interface or a visual interface expressible in Stitch, use Google Stitch and upload the PRD; mobile, desktop, CLI, SDK, API, or hardware projects MUST switch to the corresponding design/prototyping tool. Pure backend projects with no interactive interface may skip this stage and record the reason.

The following is the prompt for visual-interface projects:

Prompt:

I want to design the complete user experience of `<TARGET_PLATFORM>` for `<PROJECT_NAME>`. The full PRD is below.

Based on this PRD:

1. Generate the complete target-platform UI/interaction (pages for every Must-have feature)
2. Automatically produce DESIGN.md (design system + component specs + tokens)
3. Output requirements:
   - Follow the device and breakpoint strategy in the PRD; if the PRD does not define one, raise a clarification question first
   - Every page, view, or interaction entry point MUST have an explicit navigation/invocation path
   - Every page block, view, or interaction unit MUST be independently identifiable
   - Colors/typography/spacing MUST all be defined as design tokens
   - Theme modes, accessibility, and internationalization requirements are governed by the PRD; when undefined, clarify first

[Hard constraints]

- Design interfaces or interactions only for the features marked Must-have in the PRD; Should/Could/Won't are out
- Do not add features the PRD does not describe
- If the interface or interaction intent of some feature described in the PRD is unclear, list "questions requiring clarification" at the top of DESIGN.md — do not guess on my behalf
- The component library or design system is governed by the PRD/technical constraints; for a Web project with nothing specified, you may propose shadcn/ui + Tailwind CSS, but you MUST state the rationale and wait for confirmation

## 5.2 Inject the Design System into the Spec Kit Constitution

"First do it by hand: create a `<DESIGN_REFERENCE_DIR>/` directory inside the project's Spec directory and use it as the repository of visual reference samples.
I have put the DESIGN.md produced by Stitch into the project root and the visual prototypes into
`<DESIGN_REFERENCE_DIR>/`" (this part is the manual operation)

prompt:

/speckit.constitution

I have just put the DESIGN.md produced by Stitch into the project root and the visual prototypes into
`<DESIGN_REFERENCE_DIR>/`.

Based on this material, update .specify/memory/constitution.md and
append a "Frontend Design System" section.

### What You Must Do

Step one: read the following files first to understand the project's design context

- DESIGN.md (the whole design system)
- specs/prd.md (business background, target users, market conventions)
- Any 2-3 representative samples under `<DESIGN_REFERENCE_DIR>/` (to understand the visual and interaction style)

Step two: extract from them the "skeleton of inviolable design principles" and write it into the constitution
The constraint skeleton should be an abstract direction, not concrete values. Write each principle as:
   principle name → why it is inviolable → which specific file it cites as the basis for enforcement

Step three: the constitution states directions only and MUST NOT copy concrete values

- Write: "DESIGN.md is the single source of truth for visual specifications; colors/font sizes/spacing MUST use the tokens defined there"
- Do not write: "use #EF4444 for a rising price" (that is DESIGN.md's job; the constitution does not copy it)
- Write: "visual expressions that carry business semantics, risk levels, states, or cultural conventions MUST follow the conventions of the target domain; concrete values are in DESIGN.md"
- Do not write: "success-green means success" (that is a concrete token or mapping, and it will change)

### Directions That MUST Be Covered (extract them from the material yourself; do not ask me to fill them in)

1. The source of truth for visual specifications (which file decides)
2. How visual reference samples are cited (when to read design-reference)
3. The non-negotiable conventions of the target market/user group (extract them from the PRD; do not ask me to judge for you)
4. The component library foundation (work out from DESIGN.md what is used; do not ask me to decide for you)
5. Information density / design philosophy (the design principles section of DESIGN.md)
6. Multi-language strategy (if design-reference contains two language sets)
7. Dark/light mode (write whatever DESIGN.md says)

### Hard Constraints

- Do not copy any hex value, token name, component name, or font name into the constitution
- Do not decide on my behalf — for anything the PRD/DESIGN.md does not state explicitly (for example "is light mode supported"),
   list it in an "Open Questions" section at the end of the constitution and wait for my answer; do not fill it in yourself
- When you are done, tell me: ① which files you changed ② which passages of the material each of your 6-7 extracted principles cites

Go ahead.

## *Reusable Assets for 5.2*

Please install the `~/Assets/skills/speckit-design-injection-universal-en` folder from my desktop into the current project, configured as a project-level Skill. Verify it once installed, and tell me how to trigger it.

## 5.3 Update the Spec Documents Involving Interface/Interaction

### 5.3.1 Scan and Confirm the Features Affected by the Design

Scan every feature directory under specs/ and identify which features have a plan.md or tasks.md involving the user interface or interaction layer (pages, components, forms, CLI interactions, mobile views, and so on).

Output a table:
| feature directory | contains interface/interaction | which step must be re-run | which design-reference sample it corresponds to |

Then wait for me to confirm the list to re-run before starting the local re-run.

### 5.3.2 Locally Re-Run Plan and Tasks for the Affected Features

For every feature containing interface/interaction:

For specs/00X-<feature-name>/, re-run plan + tasks (leave spec alone, leave clarify alone):

/speckit.plan

- You MUST first read the root DESIGN.md and `<DESIGN_REFERENCE_DIR>/<corresponding sample>/`; if an executable prototype or exported code exists, read it as well
- In the "frontend zone" section of plan.md, list explicitly:
  ① which components are used (<project component A> / <project component B> / <project component C> and so on, per DESIGN.md §Components)
  ② which section of DESIGN.md each component corresponds to
  ③ the visual reference sample path (`<DESIGN_REFERENCE_DIR>/<sample>/`)
- Preserve all of the original plan.md's domain logic, backend, and integration content (data flow, API, dependencies); update only the interface/interaction part

/speckit.tasks

- Interface tasks are labeled [FE] by default; if the project uses mobile/desktop/CLI labels, keep the project's confirmed labels. Label every task with:
  ① the DESIGN.md section it references
  ② the HTML file it refers to
  ③ the component-library components or base controls it uses (per DESIGN.md)
- Backend or core logic tasks are labeled [BE] by default; where that does not apply, use the project's confirmed labels and preserve the original content
- Integration tasks are labeled [INT]
- Re-evaluate the parallel groups (once the contracts are explicit, the interface layer and the backend/core logic can usually run in parallel)

Stop after each feature and show me; only after I confirm may you go on to the next.

# Stage 6: Configure the Project-Level AI Development Context (CLAUDE.md as the example)

The default carrier below is Claude Code's `CLAUDE.md`. If you use a different AI coding tool, switch to its project-level context file (such as `AGENTS.md` or the tool's conventional file) and preserve the same information architecture, source tracing, and "do not copy the full upstream text" principle.

## 6.1 Append the Karpathy-Inspired Behavioral Guidelines

Append the 4 principles (Think Before Coding / Simplicity First / Surgical Changes / Goal-Driven
Execution) from https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md
to the end of the CLAUDE.md in the current project root, as a new section
"## Behavioral Guidelines (Karpathy-Inspired)".

Requirements:

1. Preserve the titles and body text of the 4 principles verbatim; do not rewrite or localize them
   (Karpathy's original wording is precise, and rewriting may lose its feel)
2. Add a one-line lead-in at the start of the section:
   "The following 4 principles apply during the implementation phase of every task in the project; their purpose is to reduce common AI-coding mistakes."
3. Do not modify anything else already in CLAUDE.md
4. Show me the diff when you are done

If the file does not exist, create it first.

## 6.2 Generate or Merge a Standardized CLAUDE.md

Create CLAUDE.md in the current project root; if one already exists, read it directly.

### Step One · Read the Project's Existing Documents (the information sources)

Read and understand the following files as the raw material for what you generate:

1. specs/prd.md                          → business WHAT/WHY
2. specs/research/06-architecture-baseline.md       → tech stack / selection rationale
3. .specify/memory/constitution.md       → the 7 principles + Compliance Checklist
4. DESIGN.md                              → the visual system skeleton
5. Project manifest and build files (such as package.json / pyproject.toml / Cargo.toml / go.mod) → real commands + real dependency versions
6. Any 2-3 feature directories under specs/       → to learn the task label system

### Step Two · Generate the Document Strictly Against the Following Framework:

Mandatory sections:

1. Project WHAT (one paragraph, extracted from prd.md)
2. Project WHY (one paragraph, extracted from the business goals in prd.md)
3. Workflow HOW (MUST be action-oriented; absolutely do not list the 9 historical steps of the past.
   Extract from the "Implementation Discipline" section of constitution.md + the label system in tasks.md,
   organized into 4-5 action blocks:
   ① how to start a feature (one command)
   ② which @path files MUST be read when starting each task
   ③ test discipline (which skill to use)
   ④ feature completion actions
   ⑤ the cadence rules
   Each block uses only 1-2 lines. Target 20-30 lines.
   Historical markers such as "(done)" / "(locked)" / "(kicked off)" are forbidden)
4. Tech stack table (extract real dependencies and versions from the project's actual manifest/lockfiles; do not fabricate)
5. Command list (extract real commands from the project manifest, task files, Makefile, or scripts; do not fabricate)
6. Project constitution reference (use @.specify/memory/constitution.md; do not copy the content)
7. Visual specification reference (if Stage 5 applies, use @DESIGN.md + mention `<DESIGN_REFERENCE_DIR>/`)
8. Anti-Patterns (extract 6-8 entries from the prohibitions in constitution.md + its Anti-pattern section)
9. Behavioral Guidelines (the 4 Karpathy principles, preserved verbatim in English, with a lead-in line)
10. Key file navigation table (all the project's important documents + when to read them)

### Step Three · Hard Constraints

- Total length < 200 lines (compress if it goes over)
- "YOU MUST" / "IMPORTANT" may be used at most 2 times in the whole document
- Do not copy the content of the constitution, PRD, architecture baseline, or DESIGN.md into it — reference them with @path
- Commands, dependency versions, and the tech stack MUST be extracted from real project files; when you do not know, stop and ask me
- Do not make up content from your impressions; every fact MUST trace back to a source file

### Step Four · Completion Report

Output:

- Total line count / token estimate
- A source mapping table for each section (which section of which file this passage was extracted from)
- A list of missing/uncertain information (for me to fill in)

If CLAUDE.md already exists in the project root:

- Diff the existing content first
- Preserve the parts I wrote myself and merge in only the newly generated standardized sections
- Show me the diff and wait for my confirmation before overwriting

## *Reusable Assets for Stage 6*

Please install the `~/Assets/skills/claude-md-bootstrap-en` folder from my desktop into the current project, configured as a project-level Skill. Verify it once installed, and tell me how to trigger it.

# Stage 7: Environment Preparation Before Multi-Task Execution

## 7.1 Solving the Shared-Resource Problem for Isolated Tasks:

First confirm whether the current tool supports `.worktreeinclude`. If it does, create that file in the project root and list only the local configuration files that are required for the worktree to run and that already exist; if it does not, use the current tool's equivalent isolation configuration mechanism. Example:

```
.env
.env.local
.env.development
.credentials.yaml
```

Do not blindly create credential files that do not exist, and do not commit secrets to Git; check `.gitignore` at the same time.

## 7.2 Collect External Service Information Ahead of Development

Before development, scan every feature document and list the external services, accounts, permissions, and configuration that development and testing require — API keys, OAuth, payment/messaging platform accounts, cloud resources, test devices, or hardware credentials, for example. Collect the "configuration item name, purpose, environment, how to obtain it, and whether it is ready" first; sensitive values go only into git-ignored local environment files or a secrets manager, and the corresponding filenames are added to .worktreeinclude (where applicable). Use the Superpowers brainstorming Skill to run this collection as a guided flow, and for anything uncertain, do not decide on your own — stop and ask me.

## 7.3 Append the Superpowers Handoff Section to the End of constitution.md (this directly solves the problem that Superpowers does not automatically read Spec-Kit's constitution)

Append the following at the end of .specify/memory/constitution.md (before the Version metadata line):

```
### Implementation Discipline (for Superpowers handoff)

- Before executing any tasks.md, ALWAYS read .specify/memory/constitution.md FIRST.
- Always follow TDD: Red (failing test) → Green (minimum code) → Refactor.
- Always update tasks.md checkbox after EACH task completes.
- After each task: commit, then STOP and wait for "next".
- All interface tasks: when Stage 5 applies, MUST read root DESIGN.md and the matched
   <DESIGN_REFERENCE_DIR>/<sample>/ BEFORE writing any component code.
```

## 7.4 Build the Task Management System

Add 2 persistent files under every specs/00X-<feature>/, so each feature directory has:

```
specs/00X-<feature>/
├── spec.md       (existing, generated by Spec-Kit)
├── plan.md       (existing, generated by Spec-Kit)
├── tasks.md      (existing, contains [ ] checkboxes)
├── state.md      ⭐ new: current progress, which task is in flight ([>] marker)
└── session.md    ⭐ new: cross-session continuation instructions (prevents re-planning)
```

### state.md Template

```
# Implementation Progress · <feature-name>

## Current Task
[>] T05 · Implement <core component or module>

## Completed
- [x] T01 ~ T04

## Blockers
(none / list them)

## Last Updated
2026-05-20 14:30
```

### session.md Template

```
# Session Handoff · <feature-name>

## Where We Left Off
(brief description of the last action)

## What the Next Session Does
1. Read the constitution first (constitution.md)
2. Read state.md → the current task is T0X
3. Continue from T0X; re-planning is forbidden

## No Re-Planning
plan.md is final and tasks.md is locked.
Execute directly; do not re-plan.
```

# Stage 8: Run TDD Development

*Note: the default is a serial closed loop per feature: Stage 8 implements → Stage 9 completes testing and wrap-up → Stage 10 runs the retrospective, then the next feature begins. This makes regressions easier to isolate, keeps context under control, and absorbs lessons promptly. Only when the project is a small MVP with few features, clear dependencies, shared infrastructure that is not yet stable, and where batching would not widen the rework surface, may you complete Stage 8 for all features first and then run Stages 9 and 10 together. Whichever cadence you choose, you MUST maintain state.md, session.md, test evidence, and commit history per feature; merging several features into one untraceable implementation is forbidden.*

Now start implementing specs/001-<feature>/.

## Step 1 · Worktree Isolation

Use the current tool to create an isolated worktree/branch. Claude Code example:

`claude --worktree feat-00X-<feature>`

Copy the required local environment files only when the tool supports it and `.worktreeinclude` is already configured.

## Step 2 ·  The 4 Superpowers Launch Instructions

① Read .specify/memory/constitution.md first
② Execute specs/00X-<feature>/tasks.md
③ Run every task with the Superpowers test-driven-development skill (RED→GREEN→REFACTOR)
④ After each task finishes, automatically: update state.md → commit → move on to the next task
   STOP only after all tasks are complete, and wait for me to review the feature

## Step 3 · Task Label Execution Rules

- [FE] (or the current project's interface label): before writing tests you MUST first read DESIGN.md + `<DESIGN_REFERENCE_DIR>/<corresponding sample>/`.
  If the sample comes from Stitch and the target tech stack is compatible, prefer using stitch-skills to convert the exported code into target components and verify visual consistency; other platforms use their corresponding toolchain. You MUST NOT force a switch to React just to reuse a tool.
  The implementation obeys the constitution's Compliance Checklist; if Stage 5 does not apply, follow that feature's interaction contract.
- [BE] Write test stubs against the contract specification in plan.md — an API contract (OpenAPI / JSON Schema), for example; ignore where not applicable
- [INT] MUST start only after the corresponding [FE] and [BE] have passed, and runs the real end-to-end path (no mocks); two kinds of scenario are involved here
  - Only E2E-class [INT] runs the real chain at the very end; config/migration/contract-class [INT] is ordered normally per the dependency graph in tasks.md
- Cross-feature patch-class [INT]: after making the change you MUST re-run the existing unit tests of the feature you changed, and it counts as passing only when they are green.

## Step 4 · Code Review (using the Superpowers requesting-code-review skill)

Once all tasks are complete, trigger the review with the Superpowers requesting-code-review skill.
The scan MUST cover these 4 categories of critical defect:

① Resilience defects: missing retries / missing timeouts / missing circuit breakers
② Cross-cutting consistency defects: whether authentication / rate limiting / logging cover every interface
   ("3 of the 4 interfaces have an auth check and the 4th is missing one" is the classic failure scenario)
③ Defensive coding defects: unhandled nulls / missing input validation / missing idempotency keys
④ Database migration defects (where applicable): is there a rollback script + is the operation batched

Digest the review report with the Superpowers receiving-code-review skill,
output format: | # | category | file:line | description | fix priority |

0 defects → go to Step 5
Defects found → return to the corresponding task, fix it through TDD, and run requesting-code-review again,
         until there are 0 defects

## Step 5 · Wrap-Up

1. Final commit, with "Closes 00X-<feature>" in the message
2. Merge back to the main branch
3. git tag v0.1.0-<feature>
4. Update specs/00X-<feature>/session.md to mark it complete
5. specs/00X-<feature>/ is never deleted (CI seed + context for the next feature)
6. Report: this feature had N tasks / M [FE] / K [BE]; the review found X defects, all of which are now fixed

## Cadence Rules

- One feature completes, stop and wait for my review, then the next
- Running several features concurrently across multiple agents is strictly forbidden

## *Reusable Assets for Stage 8*

Please install the `~/Assets/skills/run-feature-en` folder from my desktop into the current project, configured as a project-level Skill. Verify it once installed, and tell me how to trigger it.

# Stage 9: Testing and Wrap-Up

## *Reusable Assets for Stage 9*

Please install these skills into the current project, all configured as project-level Skills, and verify after installation that they can be triggered:

- ~/Assets/skills/test-routing-advisor-en
- ~/Assets/skills/testing-system-blueprint-en
- ~/Assets/skills/backend-testing-en
- ~/Assets/skills/frontend-testing-en
- ~/Assets/skills/fullstack-slice-testing-en
- ~/Assets/skills/full-chain-testing-en

Note: project-level installation — do not install globally and do not affect my other projects.

*Note: Stage 8's TDD proves that individual tasks work as expected; Stage 9 is responsible for identifying structural risk that is not yet covered — cross-layer integration, real dependencies, browser/device behavior, complete business chains, and non-functional requirements, for example. By default, run test-routing-advisor-en and wrap up after each feature is complete; a small MVP on a batch cadence may enter Stage 9 in one pass, but it MUST still output a routing decision, gaps, executors, and results per feature, and add the system-level P0 chain tests at the end. You MUST NOT skip the routing judgment just because the unit tests are all green.*

## 9.1 Determine the Test Mode via the Routing Skills

This feature is wrapped up; run the test-routing-advisor-en Skill: determine which test categories it hits, mark what is already covered by TDD/contracts and what remains a structural gap, and tell me which executor each gap should be routed to.

## 9.2 Execute the Tests According to the Result

*Note: what follows are example prompts for choosing an executor by feature type, not a fixed test checklist. The 9.1 routing result governs: fill only the structural gaps and avoid repeating what TDD already covers. Any work that modifies product code, test infrastructure, or shared configuration should happen in an isolated worktree/branch; purely read-only checks need no new branch. When real third-party services are involved, use a dedicated test environment and least-privilege credentials; destroying production data directly is forbidden.*

Pure backend: run single-backend gap tests for <feature name/id>.

Pure interface/client: run interface, interaction, accessibility, and state gap tests for <FE feature> on the corresponding platform.
(Prerequisite: please install https://github.com/garrytan/gstack at the current project level for me; after installation it MUST be tested for availability!)

Local cross-layer: run joint tests between the interface/caller and the server or core module for <feature>, reducing mocks and starting controllable real-dependency tests.

Complete feature chain: use full-chain-testing-en to identify the complete business chains, pick the P0 chains, and weave a safety net; when a visual reporting capability is available, open the "user journey map" for my review, otherwise output a reviewable Markdown/Mermaid report.

## 9.3 Use Superpowers to Finish the Branch

Now I want to do the final finish branch:
This feature is all green now; use superpowers:finishing-a-development-branch to wrap up: decide merge or PR, tag v0.1.0-<feature>, update specs/00X-<feature>/state.md to mark it complete, and write the final summary in session.md. The specs directory is frozen and never deleted; a requirement change opens a new number.

# Stage 10: Retrospective and Reflection (optional)

*Note: the retrospective cadence follows the execution cadence of Stages 8 and 9. In a per-feature closed loop, run the retrospective immediately after that feature is merged and tested — the information is most accurate then; a small MVP on a batch cadence may retrospect in one pass, but it MUST group by feature first and then add a section on system-level cross-feature lessons. Calling Stage 10 "optional" means it is acceptable to have nothing worth recording — it does not mean the retrospective judgment may be skipped. When there is no valid lesson, record "none" explicitly; do not manufacture hollow conclusions to hit a count.*

## 10.1 Capturing Project Lessons

Create LEARNINGS.md in the project root, with this initial content:

At the end of every feature, manually append 1-5 entries, newest at the very top. Do not record what is not worth recording; leaving a feature empty is better than padding.

Entry template:

```
## <date> · <type> · <feature id-name>
**Symptom / Decision**: state the problem in one sentence.
**Response**: what to do next time.
**Scope of application**: which kinds of feature should look back at this entry (optional).
```

type values: pitfall / decision-rethink / pattern /
  tool-quirk / ai-stuck / arch.

## 10.2 Run the Pitfall-Focused Feature Retrospective

Run a "pitfall-focused retrospective" for this feature: think through each of the 6 questions below once, without padding — when nothing is worth recording, say "none" explicitly:

1. Where did we hit a pitfall? (errors that blocked us, things that would not run, places that took several attempts to get right)
2. Where did the AI get stuck or take a detour? (misread the spec, produced dead code, went down a blind alley)
3. Which decision looks wrong in hindsight? (tooling choice, task split, abstraction boundary)
4. Was there an "if only we had known..." moment? (a faster/more robust path that was available all along)
5. Is there a small reusable pattern worth carrying into later features?
6. Any quirks hit in a tool / framework / third-party library?

For each question you can answer, append an entry to the top of the file (newest on top) using the LEARNINGS.md template, 1-5
entries, no padding. For anything code-related, list the file paths so they are easy to grep next time.

## 10.3 Configure Automatic LEARNINGS Loading

Append a new section at the end of CLAUDE.md with this content:

```
##  Automatic LEARNINGS Loading
@LEARNINGS.md
At the start of every session, absorb the captured lessons below; when implementing a new feature, if a relevant type /
scope of application is hit, actively avoid the pitfall and state explicitly "this run avoided LEARNINGS entry N".
```

# Stage 11: Packaging and Deployment (optional, Docker as the default example)

*Note: enter this stage only when the project needs to become a deployable service or a distributable artifact. First choose the release form based on the target platform: container, installer, app store, package registry, firmware, or hosting platform. Docker is only the default example for service-type projects and MUST NOT be forced onto mobile, desktop, SDK, library, plugin, or embedded projects. Once the release form is decided, still follow the established chain of Spec → Clarify → Plan → Tasks → TDD → Review → Finish → Learnings.*

## 11.1 Generate the Packaging and Deployment Feature Spec

First judge from the target runtime environment whether Docker is appropriate; for a desktop, mobile, embedded, plugin, library, or hosting-platform project, switch to the corresponding packaging and release form. If it applies, open a new feature 00X-dockerize-and-deploy.

Start with /speckit.specify to produce spec.md, targeting production-grade Docker images for every runtime service in the current project and extending (or creating) docker-compose.yml so that after `docker compose up -d` all services are
healthy, each exposes its own port, and migration-type startup hooks run to completion in order. Then run /speckit.clarify and ask me about the undecided items: "base image choice / multi-stage build strategy / image size ceiling / deployment target (self-hosted VPS or PaaS) / whether to generate a CI build-push workflow / how production configuration is isolated from the development environment / health check endpoint convention". Once those are settled, run /speckit.plan + /speckit.tasks. When all three steps are done, stop and give it to me for review; do not write code yet.

## 11.2 Implement and Verify the Packaging and Deployment Feature

Now start implementing specs/00X-dockerize-and-deploy/. Open a worktree (claude --worktree
feat-00X-dockerize-and-deploy), execute each task in tasks.md in order, strictly following
superpowers:test-driven-development (RED→GREEN→REFACTOR); after each task completes, update state.md
to change the current task from [>] to [x] before moving to the next, and do not stop in between. Once every task is green, stop and wait for my review, then run the §11
wrap-up trio (code review → finishing → append to LEARNINGS).
