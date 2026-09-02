# Socratic Questions · 6 Skeleton Variable Extraction Questions

## Table of Contents

- [Core Goal](#core-goal)
- [1. Project One-Liner](#1-project-one-liner)
- [2. Target Market](#2-target-market)
- [3. Benchmark Competitors](#3-benchmark-competitors)
- [4. Key Resource Type](#4-key-resource-type)
- [5. Open-Source Reuse Intent](#5-open-source-reuse-intent)
- [6. Module List](#6-module-list)
- [7. Questioning Rhythm Guidelines](#7-questioning-rhythm-guidelines)
- [8. Complete Conversation Examples](#8-complete-conversation-examples)

---

## Core Goal

Through 6 questions, extract the user's "rough idea" into **6 skeleton variables + 1 tool
variable**. These variables are later substituted into the placeholders in
[4-themes-template.md](4-themes-template.md) to generate a complete research prompt.

| # | Variable Name | Used In |
|---|---------------|---------|
| 1 | `<project one-liner>` | "Project positioning" section of all 4 themes |
| 2 | `<target market>` | Determines `<path B tool>` and dual-path research emphasis |
| 3 | `<benchmark competitor list>` | Starting point for Theme 1 (Product Form) inventory |
| 4 | `<key resource type>` | Specific dimensions for Theme 2 (Key Resources) |
| 5 | `<open-source reuse intent>` | Whether to activate Theme 3 (Open-Source Ecosystem) |
| 6 | `<module list>` | Breakdown basis for Theme 4 (Implementation Plan) |
| 7 | `<path B tool>` | Derived from variable 2; written into the dual-path spec in the final prompt |

---

## 1. Project One-Liner

> Tell me in one sentence: what are you building? Who is it for? What problem does it solve?
>
> Template: "\_\_\_\_ is a \_\_\_\_ tool / product / system for \_\_\_\_ that solves \_\_\_\_"

**Follow-up situations**:

- Answer lacks a subject → "Who is building this? An individual developer or a company?"
- Answer lacks a user → "Who will use it? Describe their profile."
- Answer lacks a scenario → "When will they open it? What specific pain point does it solve?"

**✅ Acceptable examples (cross-domain)**:
> - "A 7×24 AI assistant monitoring A-shares for me: watchlist Dashboard + natural-language
>   stock screening + morning briefing. For retail investors / part-time programmer traders.
>   Solves the problem of not being able to watch the market all day."
> - "Async meeting tool for remote teams: auto record + transcribe + highlight key decisions.
>   For distributed teams of 20–100 people. Solves the problem of scattered meeting notes
>   and unclear action items."
> - "Smart home energy monitoring system: real-time per-device consumption + AI anomaly
>   alerts + monthly report. For energy-conscious homeowners / property managers.
>   Solves the problem of delayed awareness when electricity bills spike."

**❌ Unacceptable examples**:
> "Build an AI app" / "Build a SaaS" / "Build a tool"

---

## 2. Target Market

> Which market will this product primarily run in?
> A. Mainland China primary (compliance / payment / language / ecosystem all localized)
> B. Overseas market primary (English / international payment / overseas vendors)
> C. Global, but with a clear primary market
> D. Internal tool / personal use — not going to market

**Why ask this**: It determines `<path B tool>` — for Mainland China, muyu-search-mcp
(Chinese path) is the primary tool; for overseas markets, WebSearch English path is
primary; for global, run both paths in parallel with bilingual search terms.

| User's Answer | Derived `<path B tool>` |
|---------------|------------------------|
| A | muyu-search-mcp (Chinese sources) |
| B | WebSearch (switched to English search terms) + Reddit/HN/Product Hunt |
| C | Both paths use general WebSearch with separate Chinese/English search terms |
| D | Single path (Path A) only; no Path B needed |

**Follow-up situations**:
- Chooses C → "What is your primary market? Why that one?"
- Chooses D → "If you later wanted to share it with people outside your team/company,
  would that more likely be A or B?"

---

## 3. Benchmark Competitors

> For your product, are there any "well-established reference points in the industry"?
> List 2–3.
>
> It's okay if you don't know — you can say "I just know there's roughly something like X."

**Why ask this**: This is the starting point for Theme 1 (Product Form) research.
Without any benchmarks, sub-agents tend to search aimlessly.

**Follow-up situations**:
- "Never heard of anything" → This is a red flag; the user may need brainstorming before
  launch research. Suggest: "You don't know of any benchmarks — you might not be ready
  for launch research yet. Want to do a competitor discovery session first?"
- Only one given → "Think a bit more about this space — 1–2 domestic and 1–2 international?"
- Gave a competitor you can't find → "I can't find X — could you share a link or screenshot?"

**✅ Acceptable examples (cross-domain)**:
> - Stock monitoring: Tonghuashun Wencai, Xueqiu, TradingView
> - Async meeting tool: Loom, Otter.ai, Notion AI
> - IoT energy monitoring: Xiaomi Smart Home, Sense Home Energy Monitor, TP-Link Kasa

---

## 4. Key Resource Type

> What is the primary "raw material" this product depends on?
> A. **Data** (market data / public datasets / user behavior / UGC data)
> B. **APIs** (third-party services / model APIs / SaaS)
> C. **Hardware** (IoT devices / sensors / compute)
> D. **Models** (self-trained or fine-tuned AI models)
> E. **Content** (manually edited knowledge bases / UGC content libraries)
> F. **Other** (please describe)

**Why ask this**: Determines the specific research dimensions for Theme 2 — for data,
research "channels / rate limits / compliance"; for APIs, research "pricing tiers / SLA /
quotas"; for hardware, research "BOM / supply chain"; for models, research "pre-trained
base / fine-tuning cost / inference cost"; for content, research "copyright / licensing /
editing cost".

**Research dimensions by type**:

| Type | Core Dimensions for Theme 2 |
|------|----------------------------|
| A Data | Coverage, frequency, latency, rate limits, pricing, registration requirements, commercial compliance |
| B APIs | Vendor comparison, pricing tiers, SLA, regional availability, switching cost, compliance |
| C Hardware | BOM, vendor comparison, unit price / MOQ, delivery lead time, interface compatibility |
| D Models | Base model selection (open vs closed), fine-tuning cost, inference latency / cost, hardware requirements |
| E Content | Copyright source, licensing type, update frequency, editorial cost, quality standards |

**Follow-up situations**:
- Multiple answers → pick **the single most critical one** as the main axis for Theme 2;
  treat the others as secondary lines
- Answers F → follow up until it can be categorized as one of A–E

---

## 5. Open-Source Reuse Intent

> Are you planning to build from scratch, or stand on the shoulders of giants?
> A. Build from scratch (for learning / control)
> B. Find an open-source project to fork and modify (saves time)
> C. Borrow modules from open-source projects (flexibility)
> D. Haven't decided yet

**Why ask this**: Determines whether Theme 3 (Open-Source Ecosystem) is activated.
If the user firmly chooses A, Theme 3 can be scaled down to "just get a sense of the ecosystem".

**Follow-up situations**:
- Chooses D → "If you finished research and found someone on GitHub already did 80% of it,
  would you fork it?" Help the user take a stance.

---

## 6. Module List

> Break your product into 5–7 core modules. A module is the smallest subsystem that is
> "independently functional and mutually replaceable".
>
> Not sure how to break it down? Here is a general candidate list — pick what applies:
>
> - Data / resource ingestion
> - Storage layer (database / cache)
> - Business logic (core algorithm / rules engine)
> - Front-end UI
> - Notification / push channel
> - Deployment / ops
> - Auth / permissions (optional)
> - Billing / subscription (optional)
> - Model / AI inference layer (if applicable)
> - Content management layer (if applicable)

**Why ask this**: The breakdown basis for Theme 4 (Implementation Plan).
Without a module list, Theme 4 is just empty talk.

**Follow-up situations**:
- Too many modules (> 8) → "Which ones are MVP-essential? Trim to 5–6."
- Too few modules (< 3) → "If this product has a front end and back end, what sub-modules
  does each side have?"
- Module names are unclear → "What does this '\_\_' module specifically do?
  Give a one-sentence description."

---

## 7. Questioning Rhythm Guidelines

**Round 1**: Ask questions 1 + 2 (project definition + target market)
→ These are the foundational anchors; everything else depends on them.
   The Path B tool is also determined here.

**Round 2**: Ask questions 3 + 4 (benchmark competitors + key resources)
→ Once anchors are set, these two determine the specific content of Themes 1 and 2.

**Round 3**: Ask questions 5 + 6 (open-source intent + module list)
→ Determines the fill for Themes 3 and 4.

**Prohibited**: Asking all 6 questions at once (users will be overwhelmed and
answer quality will drop sharply).

---

## 8. Complete Conversation Examples

Two examples from **different domains** demonstrate the consistency of the questioning approach.

### Example A: China-Market Software Product (A-stock monitoring assistant)

```
[Skill]: Let's start with the 2 most fundamental questions:

         1. Tell me in one sentence: what are you building? Who is it for?
            What problem does it solve?
            Template: "___ is a ___ for ___"

         2. Which market will this product primarily run in?
            A. Mainland China primary  B. Overseas primary
            C. Global (with a primary market)  D. Personal use

[User]:  A 7×24 AI assistant monitoring A-shares for me, for retail investors /
         part-time programmer traders. A.

[Skill]: Recorded:
         - Project definition: 7×24 AI assistant monitoring A-shares for retail
           investors / part-time programmer traders
         - Target market: Mainland China primary → <path B tool> = muyu-search-mcp

         Next 2 questions:

         3. Are there any "well-established reference points"? List 2–3.

         4. What "raw material" does this product primarily depend on?
            A. Data  B. APIs  C. Hardware  D. Models  E. Content  F. Other

[User]:  Tonghuashun Wencai, Xueqiu. A — data.

[Skill]: Recorded:
         - Benchmark competitors: Tonghuashun Wencai, Xueqiu
         - Key resource: A Data → Theme 2 research dimensions: data sources / rate limits /
           compliance

         Last 2 questions:

         5. Building from scratch or using open source?
            A. From scratch  B. Fork and modify  C. Borrow modules  D. Undecided

         6. Break the product into 5–7 core modules (see candidate list above).

[User]:  C — borrow modules. Data ingestion + storage layer + business logic +
         front-end UI + push channel + deployment/ops.

[Skill]: All 6 skeleton variables extracted. Starting to fill theme templates...
```

---

### Example B: International SaaS Tool (Remote async meeting tool)

```
[Skill]: Let's start with the 2 most fundamental questions:

         1. Tell me in one sentence: what are you building? Who is it for?
            What problem does it solve?

         2. Which market will this product primarily run in?
            A. Mainland China primary  B. Overseas primary
            C. Global (with a primary market)  D. Personal use

[User]:  An AI meeting assistant for remote teams — auto record + transcribe +
         extract action items. For distributed software teams. B.

[Skill]: Recorded:
         - Project definition: Remote team AI meeting assistant — auto record +
           transcribe + extract action items
         - Target market: Overseas primary → <path B tool> =
           WebSearch (English terms) + Reddit/HN

         Next 2 questions:

         3. Are there any "well-established reference points"? List 2–3.

         4. What "raw material" does this product primarily depend on?
            A. Data  B. APIs  C. Hardware  D. Models  E. Content  F. Other

[User]:  Loom, Otter.ai. B — depends on speech-to-text API and LLM.

[Skill]: Recorded:
         - Benchmark competitors: Loom, Otter.ai
         - Key resource: B APIs → Theme 2 research dimensions:
           transcription API comparison + LLM API comparison

         Last 2 questions:

         5. Building from scratch or using open source?

         6. Break the product into 5–7 core modules.

[User]:  D — undecided. Modules: recording/ingestion layer + AI inference layer +
         storage + web UI + notifications + deployment.

[Skill]: All 6 skeleton variables extracted. Starting to fill theme templates...
```

After extraction is complete, proceed to Step 3 — fill in the placeholders in
[4-themes-template.md](4-themes-template.md).
