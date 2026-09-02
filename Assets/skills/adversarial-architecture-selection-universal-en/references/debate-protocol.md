# 3-Phase Debate Protocol — Detailed Specification

> Detailed specification for the complete Phase 0 → 1 → 2 → 3 process of the 5-role Agent Team. Lead follows this specification during execution.

---

## Phase 0: Candidate Assignment

### Input
- `specs/research/03-open-source-projects.md (or relevant research artifact)` (or a candidate list provided directly by the user)
- Project definition (one sentence)

> **Note**: Path names vary by project; adjust according to the actual research file location. The candidate list may reside in different files under `specs/research/` (e.g., open-source project inventory, technical solution inventory, etc.). Use the actual file as the source of truth.

### Steps

#### 0.1 Determine Candidate Count N
Read the candidate list and count N.

#### 0.2 Assign According to Rules

| N | Assignment | Team Configuration |
|---|------------|--------------------|
| **0** | No candidates — terminate process, notify user | — |
| **1** | Single candidate — no adversarial needed, go directly to a simplified Phase 3 (Lead self-evaluates) | — |
| **2** | Advocate 1 owns project A; Advocate 2 owns project B; **Advocate 3 becomes "Backup Red Team"** (strengthens opposition) | 2 Advocates + 2 Red Teams + 1 Integration Assessor |
| **3** | 1 Advocate = 1 project (ideal state) | 3 Advocates + 1 Red Team + 1 Integration Assessor |
| **4** | 1 Advocate owns 2 projects, others own 1 each | Same as above |
| **5** | 2/2/1 split | Same as above |
| **6** | 2/2/2 split | Same as above |
| **7** | 3/2/2 split | Same as above |
| **8+** | Even distribution, but Lead should warn "too many candidates, recommend pre-screening first" | Same as above |

#### 0.3 Assignment Principles
- Projects with **similar** tech stacks/positioning → merge to the same Advocate (easier to compare from the same perspective)
- Projects with **large differences** in tech stacks/positioning → assign to different Advocates (maintains debate diversity)

Examples:
- 5 candidates all belong to the same technical category (e.g., all Python frameworks) → group by core feature differences (e.g., "whether distributed is supported")
- Candidates span different programming languages/tech stacks → group by language/runtime

#### 0.4 Write the Assignment Document
Path: `specs/research/debate/00-task-assignment.md`

Format:
```markdown
# Candidate Assignment (Phase 0)

Total candidates N = {N}
Project definition: {PROJECT_DEFINITION}

## Assignment Results

### Advocate 1 owns
- Project X ({URL})
- Project Y ({URL}) (if any)
Rationale: {Why these are merged}

### Advocate 2 owns
- Project Z ({URL})
Rationale: {Why separate}

### Advocate 3 owns
- Project W ({URL})
Rationale: {Why separate}

### Red Team
Fixed 1 (or 2 when N=2)

### Integration Assessor
Fixed 1

## Overall Strategy
{The overall strategy for this adversarial research, e.g., "We are focused on differences in the data ingestion layer, so..."}
```

---

## Phase 1: Independent Deep Dive

### Input
- Phase 0's `00-task-assignment.md`
- Source code or documentation for each candidate project

### Execution Rules

#### 1.1 Parallel Launch
All 5 teammates (when N=2: 5 = 2 Advocates + 2 Red Teams + 1 Integration Assessor) start **simultaneously**. Lead does not specify a launch order.

#### 1.2 No Inter-Communication
During Phase 1, **no** mailbox communication is allowed between any teammates. Reasons:
- Prevents "early consensus bias" — if a paper comes out first, later papers will reference it, losing independence
- Forces each paper to be an independently complete argument

If Lead detects inter-teammate communication, immediately stop.

#### 1.3 Time Budget
- Single-project Advocate: ≤ 30 minutes
- Multi-project Advocate (owns 2+ projects): +20 minutes per additional project, max 90 minutes
- Red Team: ≤ 30 minutes (no deep source code reading needed, skimming is sufficient)
- Integration Assessor: ≤ 30 minutes

#### 1.4 Completion Signal
Each teammate becomes idle after finishing their deliverable. Lead monitors the status of all teammates:
- All teammates idle → enter Phase 2
- A teammate remains active and exceeds time limit (e.g., > 90 minutes) → Lead intervenes to check (not to rush, but to ask if they've encountered blockers)

### Output
```
specs/research/debate/
├── position-paper-{project-1}.md       # Advocate 1 owns project 1
├── position-paper-{project-2}.md       # Advocate 1 owns project 2 (if any)
├── position-paper-{project-3}.md       # Advocate 2 owns project 3
├── position-paper-{project-4}.md       # Advocate 3 owns project 4
├── red-team-position.md                # Red Team
└── integration-assessment.md           # Integration Assessor
```

---

## Phase 2: Courtroom Debate

### Input
All documents produced in Phase 1.

### Execution Rules

#### 2.1 Pre-Start Preparation
What Lead must do:
1. Check that all papers contain Dimension 6 "Fatal Flaw Disclosure" — those missing it must be completed by the teammate before Phase 2 can begin
2. **Randomly shuffle** all N position papers — record the shuffled order in an internal log
3. Broadcast the shuffled paper list to all teammates via mailbox

Why shuffle? To prevent positional bias — the first paper a LLM sees during evaluation naturally has an advantage.

#### 2.2 First Round of Debate

**Step A: Red Team Issues Challenges**
- Issues 3 challenges **per position paper** individually
- Total challenges = 3N (N is the total number of papers, not the number of Advocates)
- Each challenge must include evidence (source code line / commit / issue / data)
- Send via mailbox to the corresponding Advocate

**Step B: Integration Assessor Challenges Single-Fork Advocates**
- Issues 1 composite challenge **per position paper**
- Content: based on the scoring from integration-assessment, questions "why not choose composite option X"
- Send via mailbox

**Step C: Advocates Respond**
- Respond **item by item** to every challenge received for each paper they own
- Each response ≤ 200 words
- May acknowledge / rebut / issue counter-challenges
- ⚠️ Prohibited from skipping any challenge
- ⚠️ Prohibited from proactively abandoning any paper they own

#### 2.3 Consensus Judgment
After all Advocates have responded, Lead assesses:

| State | Action |
|-------|--------|
| A clearly dominant option emerges (most papers have been refuted) | Enter Phase 3 |
| A clearly eliminated option emerges (Red Team's arguments fully prevail) | Enter Phase 3; decision may be "build from scratch" |
| Still deadlocked, no clear winner | Launch Round 2 |

#### 2.4 Second Round of Debate (if needed)

Round 2 focuses only on **unresolved points of contention** from Round 1:
- Lead lists a "remaining controversy points" checklist (≤ 5 items)
- Relevant teammates issue 1 additional challenge/response per controversy point
- After Round 2, **mandatory** transition to Phase 3; no Round 3

Why limit to 2 rounds? Research shows the marginal returns of MAD (Multi-Agent Debate) drop sharply after 2-3 rounds, and token costs spike.

#### 2.5 Anti-Bias Hard Constraints (Confirm During Execution)
- ⚠️ Lead **is prohibited from expressing opinions in Phase 2** — only observe, only coordinate, do not state which paper is superior
- ⚠️ Each challenge response ≤ 200 words (prevents length bias)
- ⚠️ The same teammate is not allowed to reply to the same challenge multiple times in one round
- ⚠️ Teammates are not allowed to modify their Phase 1 paper during Phase 2 (if modification is needed, must publicly declare "I am retracting section X of my paper")

### Output
`specs/research/debate/debate-transcript.md`: Complete debate record, arranged in chronological order, for easy reference in Phase 3.

---

## Phase 3: Lead Final Verdict

### Input
- All position papers (N papers)
- red-team-position.md
- integration-assessment.md
- debate-transcript.md

### Execution Rules

#### 3.1 Lead Works Alone
Phase 3 **does not call any teammates**. Lead reads all documents alone, synthesizes and weighs them, then writes the decision.

#### 3.2 Verdict Methodology

Weighting by "surviving arguments":
- An argument that is refuted by the opposition → invalidated (not counted in Lead's verdict basis)
- An argument that is challenged by the opposition but successfully defended → survives, normal weight
- An argument that is not challenged by anyone → survives, but Lead should be cautious about "why was it really not challenged?" (may have been overlooked)

Inadmissible bases for the verdict:
- ❌ "Advocate X's argument is longer / more detailed" (length bias)
- ❌ "Advocate X's argument appeared first" (positional bias)
- ❌ "Advocate X uses more professional language" (phrasing bias)
- ❌ "I personally prefer project Y" (self-preference bias)

Admissible bases:
- ✅ Quantifiable data from the 7 dimensions (transformation cost, number of flaws, number of extension points)
- ✅ Challenges that received no response or an empty response
- ✅ Objective scoring from the Integration Assessor
- ✅ Multiple independent sources pointing to the same conclusion

#### 3.3 Decision Document Format

Path: `specs/research/06-architecture-baseline-decision.md`

```markdown
# 06 Architecture Baseline Decision

> Final verdict based on source code adversarial research (5-role courtroom-style debate)
> Decision date: {DATE}
> Decision basis: all artifacts under specs/research/debate/

---

## 1. Decision Summary

**Architecture Baseline**: {single fork of project X / A+B composite / build from scratch / ...}

**One-line rationale**: {core rationale ≤ 50 words}

---

## 2. Reuse Matrix

| Module | Source | Handling | Transformation Points |
|--------|--------|----------|-----------------------|
| Core processing engine | Project A | Direct reuse | - |
| Task scheduling module | Project A | Transform | Add distributed support |
| Data ingestion layer | Build from scratch | New development | Project A does not support target data source |
| Push notification channel | Project B's notification module | Direct reuse | - |
| Frontend UI | Build from scratch | New development | Replace original project's outdated framework |
| ... | ... | ... | ... |

---

## 3. Rationale for Rejected Options

### Why project X was not chosen
Refuted by the following challenges from {Red Team / Integration Assessor / Advocate Y}:
- {Challenge 1} (citing debate-transcript.md L42-50)
- {Challenge 2} (citing ...)

### Why building from scratch was not chosen
The Red Team's "build from scratch" option was refuted by the following facts:
- {Fact 1}
- {Fact 2}

---

## 4. Open Questions (for the Brainstorming phase)

At least 3:

1. {Question 1}
2. {Question 2}
3. {Question 3}

---

## 5. Total Transformation Cost Estimate

| Item | Person-Days |
|------|:-----------:|
| Fork transformation (Project A) | 15-20 |
| Build-from-scratch modules (data layer + frontend) | 12-18 |
| Integration layer + adapters | 5-8 |
| Testing + deployment | 5 |
| **Total** | **37-51** |

Monthly budget estimate: {X} (based on hardware + services + external API subscriptions; currency unit depends on target market)
```

#### 3.4 Synchronize Update to 05-decision-summary

Path: `specs/research/05-decision-summary.md`

Operations:
1. Add v2 version marker at the top + update time + reason for update
2. "Open-source reuse decision" section: fully replace with the reuse matrix from 06
3. "Tech stack decision" section: adjust based on the reuse matrix (the fork source determines the tech stack direction)
4. "Cost estimate" section: replace with the total cost estimate from 06
5. "Risks and countermeasures" section: supplement with risks exposed during the debate (from Advocate self-reported flaws + Red Team challenges)

---

## Team Cleanup

After Phase 3 is complete:

```
1. Lead notifies all teammates via mailbox: "Debate concluded, prepare to shutdown"
2. Shut down teammates one by one (in reverse order of spawn sequence)
3. After confirming no active teammates, clean up team resources
4. Notify user that adversarial research is complete; next step is Brainstorming
```

---

## Exception Handling

| Exception | Action |
|-----------|--------|
| Teammate Phase 1 timeout (> 90 min) | Lead intervenes to ask, does not rush, checks if they've encountered blockers |
| A paper is missing Dimension 6 (Fatal Flaw Disclosure) | Return to the Advocate to complete it; cannot proceed to Phase 2 |
| Red Team "hedges" (says "project X is actually fine too") | Lead intervenes to correct; requires Red Team to return to a fully opposing position |
| Advocate wants to switch sides in Phase 2 and support another | Warning — Advocate position is fixed; the desire to switch can be referenced by Lead in Phase 3 synthesis |
| Still deadlocked after Round 2 | Force entry into Phase 3; Lead rules based on surviving arguments |
| Lead is uncertain | Write into the "Open Questions" section of `06-architecture-baseline-decision.md`; defer to the Brainstorming phase |
