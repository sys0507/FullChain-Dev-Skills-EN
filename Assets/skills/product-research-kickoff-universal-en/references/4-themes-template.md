# 4 Themes Template · Fillable Template for 4 Research Themes

## Table of Contents

- [Usage Instructions](#usage-instructions)
- [Theme 1: Product Form](#theme-1-product-form)
- [Theme 2: Key Resources](#theme-2-key-resources)
- [Theme 3: Open-Source Ecosystem](#theme-3-open-source-ecosystem)
- [Theme 4: Implementation Plan](#theme-4-implementation-plan)
- [Final Decision Summary](#final-decision-summary)
- [Theme Applicability Judgment](#theme-applicability-judgment)

---

## Usage Instructions

Substitute the variables extracted from [socratic-questions.md](socratic-questions.md)
into the placeholders below:

| Placeholder | Replace with |
|-------------|-------------|
| `<project definition>` | Skeleton variable 1 (project one-liner) |
| `<market>` | Skeleton variable 2 (target market) |
| `<benchmark 1>` `<benchmark 2>` `<benchmark 3>` | Skeleton variable 3 (benchmark competitors) |
| `<key resource>` | Skeleton variable 4 (key resource type) |
| `<open-source intent>` | Skeleton variable 5 |
| `<module 1>` ~ `<module N>` | Skeleton variable 6 (module list) |
| `<path B tool>` | Skeleton variable 7 (derived from target market) |

---

## Theme 1: Product Form

```markdown
## Research Theme 1: Product Form

For <project definition>, these questions must be answered. Each must have
verifiable evidence (screenshot description / link / real product name).

1. Competing product inventory: using <benchmark 1> / <benchmark 2> / <benchmark 3>
   as starting points, find at least 10 similar products in the <market> market.
2. Information architecture: what does their homepage look like? What are the main
   navigation items? How is each core feature organized?
3. Interaction patterns: what are the common interaction patterns for core operations
   (create / manage / trigger) in this industry?
4. AI integration examples: what AI-enhanced forms of similar products already exist?
   How far have they gone?
5. Delivery form: how does the industry deliver results to users?
   (Push notifications? Email? Cards? Rich reports? Embedded in a workflow?)

Output: `01-product-form.md` — product landscape + UI/interaction reference library
```

**Filling tips**:
- Question 1's "at least 10" is a hard requirement — prevents sub-agents from lazily
  finding only 3
- Question 5 should be adjusted based on the product type: B2B tools → "embedded in
  which workflow"; consumer products → "App push / email / notification center";
  IoT/hardware → "panel display / App / voice announcement" —
  **delivery method is not hardcoded; it is determined by the project's form**

---

## Theme 2: Key Resources

Choose the corresponding template based on skeleton variable 4 (key resource type):

### 4A: Data Type (public datasets / market data / UGC data)

```markdown
## Research Theme 2: Data Sources

For <project definition>, how is <key resource> obtained?
List all viable channels.

1. Full market inventory: open source, paid, official APIs, scraping...
   all viable channels
2. Facts per channel:
   - Coverage (full / partial / regional restrictions)
   - Frequency (real-time / daily / historical backfill)
   - Latency
   - Rate limits and quotas
   - Pricing tiers
   - Registration requirements (credentials / credit card / identity verification)
   - Commercial / redistribution compliance boundaries
3. Most common choices for indie / small-team developers: which do people actually use
   in production? Why?
4. Recommended approach: top recommendation + fallback / switching plan

Output: `02-data-sources.md` — data source comparison table + recommended approach
        + risk points
```

### 4B: API Type (third-party services / model APIs / SaaS)

```markdown
## Research Theme 2: API / Service Sources

For <project definition>, which vendors are available for <key resource>?

1. Vendor inventory: at least 5 comparable vendors
2. Facts per vendor:
   - Pricing tiers (including free quota)
   - SLA / uptime guarantee
   - Rate limits (QPS / monthly quota)
   - Regional availability (access restrictions, data residency)
   - Compliance (privacy policy / industry certifications / data transfer)
   - Switching cost (API compatibility / migration effort)
3. Most common choices for indie / small-team developers: which vendors do people
   typically use? Why?
4. Recommended approach: primary choice + 1–2 fallbacks

Output: `02-api-services.md` — vendor comparison table + recommendation + risk points
```

### 4C: Hardware Type (IoT / sensors / compute)

```markdown
## Research Theme 2: Hardware / Compute Supply

For <project definition>, how is <key resource> procured and integrated?

1. BOM inventory: core hardware list + at least 3 vendor comparisons
2. Facts per SKU:
   - Unit price / MOQ
   - Delivery lead time
   - Compatibility (interface / protocol / certification standards)
   - Supply chain stability (single-source risk)
   - After-sales support and technical documentation
3. Most common choices for maker / DIY developer communities: what do people commonly
   use? Why?
4. Recommended approach: primary choice + fallback + bulk-purchase upgrade path

Output: `02-hardware-supply.md` — BOM table + vendor comparison + risk points
```

### 4D: Model Type (self-trained / fine-tuned AI models)

```markdown
## Research Theme 2: Models and Training Resources

For <project definition>, where does the AI model come from?
Open-source base vs closed-source API vs self-trained.

1. Base model selection inventory: at least 5 comparable options
2. Facts per option:
   - Open-source vs commercial license
   - Model scale (parameter count / context window)
   - Inference latency (P95 latency for a typical task)
   - Inference cost (tokens/dollar or GPU-hours/dollar)
   - Fine-tuning complexity (official support available? data volume requirements?)
   - Hardware requirements (minimum VRAM)
   - Community activity (GitHub Stars / recent commits)
3. Most common choices for similar project developers: what do people building similar
   products typically use? Why?
4. Recommended approach: dev-phase recommendation + production-phase recommendation
   + cost-cap alternative

Output: `02-model-selection.md` — base model comparison table + recommendation
        + inference cost estimate
```

### 4E: Content Type (knowledge base / UGC / editorial content)

```markdown
## Research Theme 2: Content Resources

For <project definition>, where does <key resource> content come from?
How is it maintained?

1. Content source inventory: open data, licensed datasets, scraping, UGC,
   manual editorial
2. Facts per source:
   - Copyright ownership (CC / commercial license / copyright restrictions)
   - Data volume and quality level
   - Update frequency
   - Acquisition cost (licensing fees / scraping ops cost / editorial cost)
   - Compliance risks (privacy / copyright / platform terms)
3. Content strategy of similar products: how do others solve the "cold-start content"
   problem?
4. Recommended approach: initial content sources + content strategy at scale

Output: `02-content-resources.md` — content source comparison + recommendation
        + copyright risk points
```

---

## Theme 3: Open-Source Ecosystem

```markdown
## Research Theme 3: Open-Source Projects

For <project definition>, find at least 10 open-source projects on
GitHub / GitLab doing similar things.

1. Reference project inventory: at least 10 projects
   Suggested keywords: [fill in 3–5 Chinese/English keywords based on project domain]
2. Facts per project:
   - Stars / most recent commit / License
   - Tech stack used
   - What it does (core capabilities)
   - What it doesn't do (gaps)
   - Which modules I could reuse
   - Integration difficulty (direct fork / extract modules / reference only)
3. Ecosystem puzzle: which project excels at which piece
4. Recommended combination: based on <open-source intent>, which projects to fork /
   reference?

Output: `03-open-source.md` — project inventory + reuse matrix + initial code
        source recommendations
```

**Filling tips**:
- Keywords must include both English and Chinese (2–3 each) to prevent sub-agents from
  only searching in one language and missing projects
- If `<open-source intent>` is A (build from scratch), rephrase question 4 to
  "just get a sense of the ecosystem; no need to select a fork target"

---

## Theme 4: Implementation Plan

```markdown
## Research Theme 4: Implementation Plan

Break the system into the following modules; for each module provide industry-standard
approaches + a recommendation:

| Module | Research Dimensions |
|--------|-------------------|
| <module 1> | [expand to 2–3 research dimensions based on module name] |
| <module 2> | ... |
| <module 3> | ... |
| <module 4> | ... |
| <module 5> | ... |
| <module 6> | ... |

Per module output:
- 2–3 industry-standard approaches + pros and cons of each
- Recommendation + rationale (must include "why not use X")
- Rough effort estimate

Output: `04-implementation-plan.md` — option comparison + recommended tech stack
        + architecture diagram (Mermaid)
```

**Recommended research dimensions for common modules**:

| Module Name | Recommended Research Dimensions |
|-------------|--------------------------------|
| Data / resource ingestion | Mainstream approaches for receiving + cleaning + storing |
| Storage layer | Where to store historical data / real-time cache approach / user data |
| Business logic | Core algorithms / rules engine / task scheduling |
| AI / model inference layer | Inference framework / local vs API / latency optimization |
| Front-end UI | Web framework / component library / data visualization library / real-time comms |
| Push / notification channel | Channel options (based on target market) + integration complexity + cost |
| Deployment / ops | Local / cloud server / Serverless / containerized; monthly budget estimate |
| Auth / permissions | OAuth / JWT / RBAC; out-of-the-box solutions |
| Billing / subscription | Payment service comparison (based on target market); integration cost |
| Content management | CMS selection / editorial workflow / CDN |

> ⚠️ **Push/notification channel dimensions are NOT hardcoded**:
> - Mainland China market: WeChat Official Account / WeCom / Feishu / DingTalk / SMS
> - Overseas market: Email / Slack / Discord / Telegram / Web Push
> - Global: Email + instant messaging channel chosen by market
> Determined by `<target market>` — no single platform is hardcoded as "the default".

---

## Final Decision Summary

```markdown
## Final Decision Summary: `05-decision-summary.md`

1. Product form decision: what it looks like (homepage structure + feature form)
2. Key resource decision: what to use + fallback switching plan
3. Open-source reuse decision: which projects to fork / reference
   (if open-source intent = A, briefly summarize ecosystem findings)
4. Tech stack decision: what each module uses
5. Architecture overview: one end-to-end architecture diagram (Mermaid)
6. Cost estimate: monthly budget (development phase vs post-launch)
7. Risks: the most critical pitfalls to watch out for
```

---

## Theme Applicability Judgment

Not all projects need all 4 themes. Decision rules:

| Theme | Skip Scenario | Replacement Suggestion |
|-------|--------------|----------------------|
| Theme 1 Product Form | Internal tool with no reference products at all | Replace with "user scenario research" (interview 3 target users) |
| Theme 2 Key Resources | Project has no external resource dependencies at all | Replace with "core algorithm research" |
| Theme 3 Open-Source Ecosystem | Open-source intent = A and highly custom | Shrink to "ecosystem awareness"; merge with Theme 4 |
| Theme 4 Implementation Plan | Never skip | — |

**Important**: Always confirm with the user before skipping any theme, and state the
reason for skipping in the generated prompt.
