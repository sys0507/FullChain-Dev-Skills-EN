# Parallel Dispatch Spec · Dual-Path Research + Task Parallel Dispatch Spec

## Table of Contents

- [Dual-Path Research Spec](#dual-path-research-spec)
- [Path B Tool Selection and Invocation Constraints](#path-b-tool-selection-and-invocation-constraints)
- [Fact Source Annotation Spec](#fact-source-annotation-spec)
- [Task Parallel Dispatch Spec](#task-parallel-dispatch-spec)
- [Wrap-Up Summary Spec](#wrap-up-summary-spec)
- [Dual-Path Spec Paragraph Template to Insert into the Final Prompt](#dual-path-spec-paragraph-template-to-insert-into-the-final-prompt)

---

## Dual-Path Research Spec

When doing research, each sub-agent **must use two search paths simultaneously**
for cross-verification.

| Research Path | Tool | Emphasis |
|---------------|------|----------|
| **Path A**: Claude built-in | `WebSearch` + `WebFetch` | English sources / GitHub / official docs / international communities |
| **Path B**: chosen by target market | See table below | Covers sources relevant to the target market |

**Path B tool is determined by the `<path B tool>` variable (skeleton variable 7) —
not hardcoded:**

| Target Market | `<path B tool>` | Coverage Focus |
|---------------|----------------|----------------|
| Mainland China primary | muyu-search-mcp | Chinese sources, domestic products, Zhihu, domestic regulatory compliance |
| Overseas market primary | WebSearch (switched to English search terms) + Reddit/HN | English communities, Product Hunt, G2, overseas forums |
| Global / mixed | Both paths use general WebSearch with separate Chinese/English search terms | Bilingual coverage |
| Internal tool / personal use | No Path B needed; single path (Path A) | — |

**Core principles**:
- Same fact found consistently on both paths → mark ✅ dual-path verified
- Two paths conflict → **explicitly annotate the conflict + list each source** in the
  output document; leave the decision to the main Claude session
- Only one path found it → mark ⚠️ single-source; confidence is lower
- Sub-agents are strictly prohibited from resolving conflicts on the user's behalf

---

## Path B Tool Selection and Invocation Constraints

### When Path B = muyu-search-mcp (Mainland China market)

muyu-search-mcp has a **hard gate**: calling `web_search` directly will be rejected
by the tool. The planning workflow must be completed first:

```
plan_intent ─► plan_complexity ─► plan_sub_query (batch)
                                       │
                                       ▼
                                  plan_search_term (batch)
                                       │
                                       ▼
                                  plan_tool_mapping (batch)
                                       │
                                       ▼
                                  plan_execution ─► web_search
```

| Stage | Key Output |
|-------|-----------|
| `plan_intent` | Core question + query_type + **unverified_terms** |
| `plan_complexity` | Level 1/2/3 + estimated_tool_calls |
| `plan_sub_query` (batch) | Multiple sub-queries (with goal / boundary / depends_on) |
| `plan_search_term` (batch) | Search terms per sub-query (≤ 8 words) |
| `plan_tool_mapping` (batch) | sub-query → tool mapping |
| `plan_execution` | parallel groups + sequential list |

**Key constraints**:
- `unverified_terms` must appear in at least one sub-query's goal; otherwise the plan
  will always be incomplete
- For product launch research, recommend level = 2 or 3 (most facts involve
  unverified terminology)

### When Path B = WebSearch English path (overseas / global market)

Call Claude's built-in `WebSearch` directly, but adjust the search term strategy:
- Path A search terms: technical documentation, GitHub, official sites
- Path B search terms: community discussion terms
  ("[\product type] reddit alternatives",
  "[feature] site:news.ycombinator.com",
  "[product name] G2 review", etc.)

No additional gate; call directly.

### When Path B = None (internal tool / personal use)

Only run Path A; source annotation rules simplified to:
- `[WebSearch]` / `[WebFetch]` / `[Single-source ⚠️]`

---

## Fact Source Annotation Spec

When sub-agents write to output documents, each fact/data point must have a source tag:

| Tag | Meaning |
|-----|---------|
| `[WebSearch]` | Found via Path A (Claude built-in) only |
| `[Path B]` | Found via Path B tool only (write the actual tool name, e.g., `[muyu]`) |
| `[✅ Both]` | Both paths agree |
| `[⚠️ Single-source]` | Found on only one path; lower confidence |
| `[⚠️ Conflict — see below]` | The two paths disagree; sources listed below |

**Example (muyu as Path B)**:

```markdown
- AKShare supports full A-share daily price data. [✅ Both]
- As of 2025, a certain API added token verification for high-frequency calls.
  [⚠️ Conflict — see below]
  - [WebSearch] GitHub Issue says "all endpoints remain free"
  - [muyu] Zhihu answer says "high-frequency endpoints now have rate limiting"
```

**Example (WebSearch English Path B)**:

```markdown
- Otter.ai free tier limits transcription to 300 minutes per month. [✅ Both]
- Whether the enterprise plan includes unlimited recording storage.
  [⚠️ Single-source]
  - [WebSearch] Official pricing page does not explicitly state this
```

---

## Task Parallel Dispatch Spec

### Tool Selection

✅ Prefer the current AI coding tool's native sub-agent / task mechanism and launch N
independent tasks in the same turn. If parallel execution is unavailable, preserve the same
task boundaries and run them serially without reducing output requirements.
❌ Do not force a heavyweight team mechanism that requires inter-agent communication merely
for parallelism; this scenario only needs independent research and main-session synthesis.

### Dispatch Pattern

```
Main Claude session
   ├──[Task 1]──► sub-agent: research Theme 1 → write 01-product-form.md
   ├──[Task 2]──► sub-agent: research Theme 2 → write 02-key-resources.md   (parallel)
   ├──[Task 3]──► sub-agent: research Theme 3 → write 03-open-source.md
   └──[Task 4]──► sub-agent: research Theme 4 → write 04-implementation-plan.md
        ↓
   All 4 Tasks return
        ↓
   Main Claude serially writes 05-decision-summary.md
```

### Each Task prompt must contain four required elements

1. **Focused scope**: do only the assigned theme; clear boundaries
2. **Self-contained context**: project positioning, target market, benchmark competitors,
   and all necessary background
3. **Constraints**:
   - Must use dual-path research + source annotation (Path B tool determined by
     target market)
   - Must use the Write tool to write to the specified path
   - Must not modify files belonging to other themes
   - Say "I don't know" rather than fabricating information
4. **Expected output**: file path + document structure + quality requirements

### Task Count Guidelines

- Recommended: 4 Tasks in parallel (4 themes)
- Maximum: 6 (more than that inflates main session coordination overhead)
- If a project needs more than 6 themes, split into two batches

---

## Wrap-Up Summary Spec

`05-decision-summary.md` is written serially by the main Claude (not a sub-agent):

1. **Cannot be parallelized** — must read all 4 prior docs before writing
2. **Cannot be delegated to a sub-agent** — summarization requires global perspective
   and decision authority
3. **Must handle conflicts** — any `[⚠️ Conflict]` items from the 4 prior docs must be
   explicitly addressed with a rationale for the choice made
4. **Must give recommendations** — for every decision point (product form / resources /
   reuse / tech stack), provide a clear recommendation with reasoning

Summary document skeleton:

```markdown
# 05-Decision Summary

## 1. Product Form Decision
Recommendation: xxx
Rationale: xxx
(Based on 01-product-form.md)

## 2. Key Resource Decision
Primary: xxx | Fallback: xxx
Rationale: xxx

## 3. Open-Source Reuse Decision
Fork: xxx | Reference: xxx
Rationale: xxx

## 4. Tech Stack Decision
Module 1: xxx (rationale)
Module 2: xxx (rationale)
...

## 5. Architecture Overview
(Mermaid diagram)

## 6. Cost Estimate
Monthly budget: ~xxx (development phase / post-launch)

## 7. Risks and Mitigations
- Risk 1: xxx → Mitigation: xxx
- Risk 2: xxx → Mitigation: xxx

## 8. Conflict Resolution
(List all [⚠️ Conflict] fact points from the 4 prior docs + rationale for the choice made)
```

---

## Dual-Path Spec Paragraph Template to Insert into the Final Prompt

When generating the final prompt, dynamically insert one of the following paragraphs
based on `<path B tool>`:

### Template A: Path B = muyu-search-mcp (Mainland China market)

```markdown
## 🔀 Dual-Path Research Spec

Each sub-agent must use two search paths simultaneously for cross-verification:

- **Path A**: Claude built-in `WebSearch` / `WebFetch`
  (emphasis: English sources, GitHub, official docs)
- **Path B**: muyu-search-mcp `web_search` / `web_fetch` / `web_map`
  (emphasis: Chinese sources, domestic products, Zhihu, domestic regulatory compliance)

**muyu-search-mcp invocation constraint**: Hard planning gate — must complete
`plan_intent → plan_complexity → plan_sub_query → plan_search_term →
plan_tool_mapping → plan_execution` before calling `web_search`; direct calls
will be rejected.

**Fact annotation**: tag each fact/data point with a source:
`[WebSearch]` / `[muyu]` / `[✅ Both]` / `[⚠️ Single-source]` / `[⚠️ Conflict — see below]`

When paths conflict, **do not resolve on my behalf** — mark them as-is and list
both sources.

## ⚡ Parallel Execution

Prefer the current AI coding tool's native **sub-agent / task mechanism** and **launch 4
independent tasks in the same turn**. If parallel execution is unavailable, preserve the same
task boundaries and run them serially. After all 4 results return, the main session serially
writes `05-decision-summary.md`.
```

---

### Template B: Path B = WebSearch English path (overseas / global market)

```markdown
## 🔀 Dual-Path Research Spec

Each sub-agent must use two search strategies simultaneously for cross-verification:

- **Path A (Technical / Official)**: Claude built-in `WebSearch` / `WebFetch`
  Search terms: official docs, GitHub, technical blogs
- **Path B (Community / Reviews)**: Claude built-in `WebSearch` with community-oriented terms:
  Reddit, Hacker News, Product Hunt, G2, industry communities

**Path B search term examples**:
`[product category] reddit`, `[product name] review site:news.ycombinator.com`,
`best [feature] tool 2025`, `[product name] alternative`

**Fact annotation**: tag each fact/data point with a source:
`[WebSearch-Official]` / `[WebSearch-Community]` / `[✅ Both]` /
`[⚠️ Single-source]` / `[⚠️ Conflict — see below]`

When paths conflict, **do not resolve on my behalf** — mark them as-is and list
both sources.

## ⚡ Parallel Execution

Prefer the current AI coding tool's native **sub-agent / task mechanism** and **launch 4
independent tasks in the same turn**. If parallel execution is unavailable, preserve the same
task boundaries and run them serially. After all 4 results return, the main session serially
writes `05-decision-summary.md`.
```

---

### Template C: No Path B (internal tool / personal use)

```markdown
## 🔍 Single-Path Research Spec

This project is an internal tool / personal use; using single-path research:

- **Path A**: Claude built-in `WebSearch` / `WebFetch`

**Fact annotation**: tag each fact/data point with a source:
`[WebSearch]` / `[WebFetch]` / `[⚠️ Single-source]`

## ⚡ Parallel Execution

Prefer the current AI coding tool's native **sub-agent / task mechanism** and **launch 4
independent tasks in the same turn**. If parallel execution is unavailable, preserve the same
task boundaries and run them serially. After all 4 results return, the main session serially
writes `05-decision-summary.md`.
```
