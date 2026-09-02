# Full-Chain Development Prompt Template (Skills Edition)

> This template covers the full development chain: project idea, research, requirements, specs, design, implementation, testing, retrospective, and deployment.
> Replace the placeholders below before use; a conditional stage that does not apply to the current project MUST be explicitly marked "skipped, with reason" — do not manufacture worthless artifacts just to complete the flow.
> Every "reusable asset" mentioned here is treated as an already-available, project-level Skill suitable for general-purpose projects.

## How to Use

1. **First launch of a project**: copy "Global Input Context", "Global Execution Constraints", and the "Stage 0 Execution Prompt" to the Agent, in that order. Template variables may be left blank; the minimum input can be a single sentence describing the project idea.
2. **Continuing later stages in the same session**: normally you only need to copy the current stage's content marked "Execution Prompt (copy to the Agent)"; stage narration, template examples, and reusable-asset notes do not need to be copied.
3. **Starting a new session or switching Agents**: if the Agent can read the project-level context files and `specs/research/00-project-input-and-assumptions.md` on its own, copy only the current stage's execution prompt; otherwise supply "Global Execution Constraints" first, and add the latest "Global Input Context" as needed.
4. **When project context is already persisted**: if the global rules are already written into `CLAUDE.md`, `AGENTS.md`, or the current tool's equivalent project-level file, do not re-paste them at every stage; the latest version in the project file governs.
5. Submit to the Agent only the content explicitly labeled global context, global constraints, or execution prompt; ordinary narration, collapsed-section indexes, and artifact examples are for human reading only.

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
8. This document is an **English execution template**: Agent interaction, research reports, requirement/design/test narration, and every other newly generated explanatory artifact default to English. Code, commands, APIs, file paths, dependency names, identifiers already present in the project, and technical principles explicitly required to stay verbatim are not translated. Reading material in another language does not mean switching output language.

# Stage 0: Project Initialization and Toolchain Configuration

### Execution Prompt (copy to the Agent)

- Create the project directory `<REPO_OR_WORKSPACE>`, initialize version control, and open it with the current AI coding tool.
- Scan the project type, existing files, and runtime environment, and produce a "needed / not needed / to be confirmed" toolchain configuration inventory.
- At project start, configure and verify in one pass all reusable-asset Skills that later stages of this template will invoke. The default source is `~/Assets/skills/<skill-name>/`; every Skill is installed at the **current project level** and MUST NOT pollute the global environment; when a Skill of the same name already exists, check its version and content first and do not overwrite it redundantly:
  - `product-research-kickoff-universal-en`
  - `adversarial-architecture-selection-universal-en`
  - `prd-writer-universal-en`
  - `speckit-design-injection-universal-en`
  - `claude-md-bootstrap-en`
  - `run-feature-en`
  - `test-routing-advisor-en`
  - `testing-system-blueprint-en`
  - `backend-testing-en`
  - `frontend-testing-en`
  - `fullstack-slice-testing-en`
  - `full-chain-testing-en`
- Skill versions MUST match the list above **exactly**; substituting a merely similar name is forbidden:
  - This document and the Chinese template use **template-level hard isolation**. This English template installs and invokes only the `-en` Skills listed above, and MUST NOT auto-switch to, fall back on, or mix in any non-`-en` directory.
  - The first four may appear in older course material as project-specific originals without `-universal`; the current asset directory now keeps only the universal Chinese and English versions. This template is fixed on the `*-universal-en` English universal version, and MUST NOT restore or mistakenly install a project-specific original from older external material.
  - The remaining eight carry no `-universal` segment — `<name>-en` is the universal main version, and you MUST NOT invent a nonexistent `*-universal-en`. Among them, `claude-md-bootstrap-en` is invoked only in Claude Code projects; other tools may still pre-configure it, but Stage 6 MUST use the equivalent project-level context approach.
  - The Chinese template installs and invokes only the Chinese versions that correspond one-to-one with these 12 Skills; the Chinese template's version-selection rules MUST NOT reach back into this English template.
- Once the one-time configuration is complete, output the Skill inventory, source paths, install locations, verification results, and trigger conditions. Later stages only invoke them and never reinstall; a conditional stage that is ultimately skipped MUST still be marked in the inventory as "not invoked, with reason". If a Skill is missing or fails verification, record only the failed item and its impact — fabricating success is forbidden.
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

### Execution Prompt (copy to the Agent)

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

### Execution Prompt (copy to the Agent)

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

Stage 0 should already have configured the project-level `~/Assets/skills/product-research-kickoff-universal-en`. It may serve as a supporting asset for this stage, generating a research kickoff prompt, but it **MUST NOT replace the execution prompts of 1.1-1.2**. The reason is that this template allows the user to provide only one sentence and requires an ongoing "confirmed / research candidate / to be confirmed" ledger; that Skill does not fully cover this state management and research artifact structure.

If you use it, let it only generate supplementary research questions or a retrieval plan from `00-project-input-and-assumptions.md`; you MUST NOT let it override this stage's file structure, variable-default rules, or convergence logic.

## 1.3 Technology Selection via Adversarial Architecture

### Execution Prompt (copy to the Agent)

Use the project-level `adversarial-architecture-selection-universal-en` Skill to run adversarial architecture selection over the candidate options in `specs/research/01` through `05`. Follow that Skill's pre-checks, candidate advocacy, cross-examination, adjudication, and write-back flow strictly; produce `specs/research/06-architecture-baseline.md`, and update `05-decision-summary.md` according to its rules. Whenever material is insufficient, a candidate does not hold up, or a user ruling is required, pause explicitly — do not guess.

<details>
<summary>Index of the original stage prompt (not an execution prompt)</summary>

> To keep this document from growing unwieldy, the original prompt is not duplicated here. To consult it, open [Full-Chain-Development-Prompt-Template.md](./Full-Chain-Development-Prompt-Template.md) and look for "Stage 1.3 'Technology Selection via Adversarial Architecture'". The baseline document exists for explanation, auditing, and manual cross-checking only; do not feed its older prompt and this stage's Skill invocation to an Agent / LLM at the same time.

</details>

## *Reusable Assets for 1.3*

Stage 0 should already have configured the project-level `~/Assets/skills/adversarial-architecture-selection-universal-en`; this stage only invokes it and does not reinstall it.

# Stage 2: Trigger Brainstorming for Requirements Analysis and Converge the Research Documents

### Execution Prompt (copy to the Agent)

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

### Execution Prompt (copy to the Agent)

Use the project-level `prd-writer-universal-en` Skill to read the Stage 2 brainstorming convergence results and every research file under `specs/research/`, and generate a **project-level PRD** at `specs/prd.md`. You MUST read `00-project-input-and-assumptions.md` first: only "user-confirmed" content may be written as a settled requirement; unconfirmed content may only enter Open Questions, risks, or assumptions to be verified. If upstream artifacts already answer the Skill's core questions, do not ask them again — fill in only the information that genuinely blocks finalization.

<details>
<summary>Index of the original stage prompt (not an execution prompt)</summary>

> To keep this document from growing unwieldy, the original prompt is not duplicated here. To consult it, open [Full-Chain-Development-Prompt-Template.md](./Full-Chain-Development-Prompt-Template.md) and look for "Stage 3 'Write the Final Requirements Document'". The baseline document exists for explanation, auditing, and manual cross-checking only; do not feed its older prompt and this stage's Skill invocation to an Agent / LLM at the same time.

</details>

## *Reusable Assets for Stage 3*

Stage 0 should already have configured the project-level `~/Assets/skills/prd-writer-universal-en`; this stage only invokes it and does not reinstall it.

# Stage 4: Run Spec-Kit to Generate the Spec Documents

### Execution Prompt (copy to the Agent)

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

> Note: the Chinese template has a corresponding Skill for this stage (`platform-design-kickoff`), but its **English counterpart has not yet been ported**. Until it exists, run this stage from the execution prompt below — do not assume an `-en` Skill is available.

The following is the prompt for visual-interface projects:

### Execution Prompt (copy to the Agent)

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

### Execution Prompt (copy to the Agent)

Use the project-level `speckit-design-injection-universal-en` Skill to inject the already-generated `DESIGN.md` and the visual/interaction reference artifacts into the current Spec-Kit project. Execute that Skill's four-step flow in full: place the assets, inject the constitution, scan for impact, and — after I confirm — locally re-run plan and tasks for each affected feature one at a time. You MUST NOT modify the spec / clarify artifacts, MUST NOT overwrite existing design files, and MUST verify source and target paths before any recursive copy.

## 5.3 Update the Spec Documents Involving Interface/Interaction

5.3 continues within the same Skill invocation as 5.2. Output the impact list first and wait for my confirmation, then re-run feature by feature; stop after each feature so I can review it.

<details>
<summary>Index of the original stage prompt (not an execution prompt)</summary>

> To keep this document from growing unwieldy, the original prompt is not duplicated here. To consult it, open [Full-Chain-Development-Prompt-Template.md](./Full-Chain-Development-Prompt-Template.md) and look for "Stage 5.2-5.3 'Inject the Design System into the Constitution and Update the Affected Specs'". The baseline document exists for explanation, auditing, and manual cross-checking only; do not feed its older prompt and this stage's Skill invocation to an Agent / LLM at the same time.

</details>

## *Reusable Assets for Stage 5.2-5.3*

Stage 0 should already have configured the project-level `~/Assets/skills/speckit-design-injection-universal-en`; this stage only invokes it and does not reinstall it.

# Stage 6: Configure the Project-Level AI Development Context (CLAUDE.md as the example)

The default carrier below is Claude Code's `CLAUDE.md`. If you use a different AI coding tool, switch to its project-level context file (such as `AGENTS.md` or the tool's conventional file) and preserve the same information architecture, source tracing, and "do not copy the full upstream text" principle.

### Execution Prompt (copy to the Agent)

Use the project-level `claude-md-bootstrap-en` Skill to read the existing PRD, architecture decisions, constitution, design material, project manifests/lockfiles, and feature specs, and generate or refresh `CLAUDE.md` in the project root. Strictly enforce source mapping, real command and dependency verification, the 10-section structure, `@path` progressive disclosure, the four Karpathy principles, and the 200-line ceiling. If a `CLAUDE.md` already exists, show the diff first and preserve the user's hand-written content — direct overwriting is forbidden.

If the current project does not use Claude Code, this Skill does not apply; follow the source mapping and reduction principles in the supplementary notes below to create an equivalent project-level context file for the current tool.

<details>
<summary>Index of the original stage prompt (not an execution prompt)</summary>

> To keep this document from growing unwieldy, the original prompt is not duplicated here. To consult it, open [Full-Chain-Development-Prompt-Template.md](./Full-Chain-Development-Prompt-Template.md) and look for "Stage 6 'Configure the Project-Level AI Development Context'". The baseline document exists for explanation, auditing, and manual cross-checking only; do not feed its older prompt and this stage's Skill invocation to an Agent / LLM at the same time.

</details>

## *Reusable Assets for Stage 6*

Stage 0 should already have configured the project-level `~/Assets/skills/claude-md-bootstrap-en`; this stage only invokes it and does not reinstall it.

# Stage 7: Environment Preparation Before Multi-Task Execution

### Execution Prompt (copy to the Agent)

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

### Execution Prompt (copy to the Agent)

Use the project-level `run-feature-en` Skill to implement or continue `specs/00X-<feature>/`. Handle only one feature at a time, and only one that already has spec.md, plan.md, and tasks.md; create the isolated worktree/branch according to the project's actual rules, read the project constitution and design material, execute TDD task by task, complete a structured code review, and wrap up according to the Skill's rules. If infrastructure or an upstream dependency is not ready, stop and report first — forcing the run is forbidden.

<details>
<summary>Index of the original stage prompt (not an execution prompt)</summary>

> To keep this document from growing unwieldy, the original prompt is not duplicated here. To consult it, open [Full-Chain-Development-Prompt-Template.md](./Full-Chain-Development-Prompt-Template.md) and look for "Stage 8 'Run TDD Development'". The baseline document exists for explanation, auditing, and manual cross-checking only; do not feed its older prompt and this stage's Skill invocation to an Agent / LLM at the same time.

</details>

## *Reusable Assets for Stage 8*

Stage 0 should already have configured the project-level `~/Assets/skills/run-feature-en`; this stage only invokes it and does not reinstall it.

# Stage 9: Testing and Wrap-Up

## *Reusable Assets for Stage 9*

The following project-level Skills should already have been configured and verified once in Stage 0; this stage only invokes them according to the routing result and does not reinstall them:

- ~/Assets/skills/test-routing-advisor-en
- ~/Assets/skills/testing-system-blueprint-en
- ~/Assets/skills/backend-testing-en
- ~/Assets/skills/frontend-testing-en
- ~/Assets/skills/fullstack-slice-testing-en
- ~/Assets/skills/full-chain-testing-en

If Stage 0 recorded missing or failed items, report their impact on this round of testing first, then decide whether to fill the gap or adopt an equivalent approach; silent degradation is forbidden.

*Note: Stage 8's TDD proves that individual tasks work as expected; Stage 9 is responsible for identifying structural risk that is not yet covered — cross-layer integration, real dependencies, browser/device behavior, complete business chains, and non-functional requirements, for example. By default, run test-routing-advisor and wrap up after each feature is complete; a small MVP on a batch cadence may enter Stage 9 in one pass, but it MUST still output a routing decision, gaps, executors, and results per feature, and add the system-level P0 chain tests at the end. You MUST NOT skip the routing judgment just because the unit tests are all green.*

## 9.1 Determine the Test Mode via the Routing Skills

### Execution Prompt (copy to the Agent)

Use the project-level `test-routing-advisor-en` Skill to review the just-completed `<feature name/id>`: determine which test types are hit, separate what is already covered by TDD / contracts from the structural gaps that remain, and give each gap a unique or explicitly combined executor route. Read `testing-system-blueprint-en` as the global test blueprint, but at this step output only the routing decision and its rationale — do not run the supplementary tests.

## 9.2 Execute the Tests According to the Result

*Note: the 9.1 routing result governs; fill only the structural gaps and avoid repeating what TDD already covers. Any work that modifies tests, test infrastructure, or shared configuration MUST happen in an isolated worktree/branch; purely read-only checks need no new branch. When real third-party services are involved, use a dedicated test environment and least-privilege credentials; destroying production data is forbidden. Test executors deliver isolated changes and evidence only — they do not decide merge or PR on their own; that decision belongs entirely to 9.3. If supplementary testing uncovers a genuine product defect, the executor MUST stop and hand it back to the Stage 8 TDD / debugging flow for repair.*

### Execution Prompt (copy to the Agent)

Following the 9.1 routing result, invoke the corresponding project-level executors: `backend-testing-en`, `frontend-testing-en`, `fullstack-slice-testing-en`, `full-chain-testing-en`. One or more may be hit, but execute only the gaps the routing report confirmed. Every executor follows `testing-system-blueprint-en`, completing testing, evidence archiving, and human-review delivery in an isolated branch/changeset; when finished, summarize the executor, test result, residual risk, and change location for every gap, then proceed to 9.3.

<details>
<summary>Index of the original stage prompt (not an execution prompt)</summary>

> To keep this document from growing unwieldy, the original prompt is not duplicated here. To consult it, open [Full-Chain-Development-Prompt-Template.md](./Full-Chain-Development-Prompt-Template.md) and look for "Stage 9.1-9.2 'Test Routing and Test Execution'". The baseline document exists for explanation, auditing, and manual cross-checking only; do not feed its older prompt and this stage's Skill invocation to an Agent / LLM at the same time.

</details>

## 9.3 Use Superpowers to Finish the Branch

### Execution Prompt (copy to the Agent)

Now I want to do the final finish branch:
This feature is all green now; use superpowers:finishing-a-development-branch to wrap up: decide merge or PR, tag v0.1.0-<feature>, update specs/00X-<feature>/state.md to mark it complete, and write the final summary in session.md. The specs directory is frozen and never deleted; a requirement change opens a new number.

# Stage 10: Retrospective and Reflection (optional)

*Note: the retrospective cadence follows the execution cadence of Stages 8 and 9. In a per-feature closed loop, run the retrospective immediately after that feature is merged and tested — the information is most accurate then; a small MVP on a batch cadence may retrospect in one pass, but it MUST group by feature first and then add a section on system-level cross-feature lessons. Calling Stage 10 "optional" means it is acceptable to have nothing worth recording — it does not mean the retrospective judgment may be skipped. When there is no valid lesson, record "none" explicitly; do not manufacture hollow conclusions to hit a count.*

## 10.1 Capturing Project Lessons

### Execution Prompt (copy to the Agent)

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

### Execution Prompt (copy to the Agent)

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

### Execution Prompt (copy to the Agent)

Append a new section at the end of CLAUDE.md with this content:

```
##  Automatic LEARNINGS Loading
@LEARNINGS.md
At the start of every session, absorb the captured lessons below; when implementing a new feature, if a relevant type /
scope of application is hit, actively avoid the pitfall and state explicitly "this run avoided LEARNINGS entry N".
```

# Stage 11: Packaging and Deployment (optional, Docker as the default example)

*Note: enter this stage only when the project needs to become a deployable service or a distributable artifact. First choose the release form based on the target platform: container, installer, app store, package registry, firmware, or hosting platform. Docker is only the default example for service-type projects and MUST NOT be forced onto mobile, desktop, SDK, library, plugin, or embedded projects. Once the release form is decided, still follow the established chain of Spec → Clarify → Plan → Tasks → TDD → Review → Finish → Learnings.*

> Note: the Chinese template has a corresponding Skill for this stage (`release-packaging-router`), but its **English counterpart has not yet been ported**. Until it exists, run this stage from the execution prompts below — do not assume an `-en` Skill is available.

## 11.1 Generate the Packaging and Deployment Feature Spec

### Execution Prompt (copy to the Agent)

First judge from the target runtime environment whether Docker is appropriate; for a desktop, mobile, embedded, plugin, library, or hosting-platform project, switch to the corresponding packaging and release form. If it applies, open a new feature 00X-dockerize-and-deploy.

Start with /speckit.specify to produce spec.md, targeting production-grade Docker images for every runtime service in the current project and extending (or creating) docker-compose.yml so that after `docker compose up -d` all services are
healthy, each exposes its own port, and migration-type startup hooks run to completion in order. Then run /speckit.clarify and ask me about the undecided items: "base image choice / multi-stage build strategy / image size ceiling / deployment target (self-hosted VPS or PaaS) / whether to generate a CI build-push workflow / how production configuration is isolated from the development environment / health check endpoint convention". Once those are settled, run /speckit.plan + /speckit.tasks. When all three steps are done, stop and give it to me for review; do not write code yet.

## 11.2 Implement and Verify the Packaging and Deployment Feature

### Execution Prompt (copy to the Agent)

Now start implementing specs/00X-dockerize-and-deploy/. Open a worktree (claude --worktree
feat-00X-dockerize-and-deploy), execute each task in tasks.md in order, strictly following
superpowers:test-driven-development (RED→GREEN→REFACTOR); after each task completes, update state.md
to change the current task from [>] to [x] before moving to the next, and do not stop in between. Once every task is green, stop and wait for my review, then run the §11
wrap-up trio (code review → finishing → append to LEARNINGS).
