# Examples · 3 End-to-End Examples

> This file contains 3 end-to-end examples across different domains, demonstrating
> the Skill's consistent applicability across different project types.
> Each example shows: skeleton variable extraction → theme filling → final prompt excerpt.
>
> **Note**: Examples are for methodology demonstration only — not domain constraints.
> The Skill applies to new product launch research in any domain and any market.

---

## Table of Contents

- [Example A: China-Market Software Product (A-stock monitoring assistant)](#example-a-china-market-software-product-a-stock-monitoring-assistant)
- [Example B: International SaaS Tool (Remote async meeting tool)](#example-b-international-saas-tool-remote-async-meeting-tool)
- [Example C: Hardware / IoT Product (Smart home energy monitoring system)](#example-c-hardware--iot-product-smart-home-energy-monitoring-system)

---

## Example A: China-Market Software Product (A-stock monitoring assistant)

### Skeleton Variables

| Variable | Value |
|----------|-------|
| Project definition | 7×24 AI assistant monitoring A-shares: watchlist Dashboard + natural-language stock screening + morning briefing + anomaly alerts |
| Target market | Mainland China primary |
| Benchmark competitors | Tonghuashun Wencai, Xueqiu, TradingView |
| Key resource type | A Data (A-share market data) |
| Open-source reuse intent | C — borrow modules |
| Module list | Data ingestion, storage layer, business logic, front-end UI, push channel, deployment/ops |
| Path B tool | muyu-search-mcp |

### Theme 2 Fill Example (Data Sources)

```markdown
## Research Theme 2: Data Sources

For "7×24 A-share AI monitoring assistant", how do we get A-share market data?

1. Full market inventory: open-source libraries, brokerage APIs, paid data vendor
   interfaces, scraping... all viable channels
2. Facts per channel:
   - Coverage (all A-shares / ETFs / HK and US stocks)
   - Frequency (real-time / minute-level / daily)
   - Latency (second-level / 15-minute delay / next-day)
   - Rate limits and quotas
   - Pricing tiers (free quota / paid tiers)
   - Registration requirements (real-name / brokerage account / business license)
   - Commercial / redistribution compliance boundaries
3. Most common choices for indie developers: which do people actually run in
   production? Why?
4. Recommended approach: top recommendation + fallback switching plan
```

### Push Channel Dimension Note

> This project targets Mainland China. Push channel research dimensions should cover:
> WeChat Official Account / WeCom bot / Feishu bot / DingTalk bot / SMS / App Push
> — not overseas channels (Slack / Email / Discord).

### Final Prompt Excerpt (dual-path spec paragraph)

```markdown
## 🔀 Dual-Path Research Spec

- Path A: Claude built-in WebSearch / WebFetch (English sources / GitHub)
- Path B: muyu-search-mcp web_search / web_fetch / web_map
  (Chinese sources / Zhihu / domestic regulatory compliance)

muyu invocation must follow the planning state machine:
plan_intent → plan_complexity → plan_sub_query → plan_search_term
→ plan_tool_mapping → plan_execution → web_search

Annotation: [WebSearch] / [muyu] / [✅ Both] / [⚠️ Single-source] / [⚠️ Conflict — see below]
```

---

## Example B: International SaaS Tool (Remote async meeting tool)

### Skeleton Variables

| Variable | Value |
|----------|-------|
| Project definition | Remote team AI meeting assistant: auto record + transcribe + extract action items + highlight decisions, for distributed software teams |
| Target market | Overseas market primary (English market) |
| Benchmark competitors | Loom, Otter.ai, Fireflies.ai |
| Key resource type | B APIs (speech-to-text API + LLM API) |
| Open-source reuse intent | B — fork and modify |
| Module list | Recording/ingestion layer, AI inference layer (transcription + summary), storage, web UI, notifications, deployment |
| Path B tool | WebSearch (English terms) + Reddit/HN/Product Hunt |

### Theme 2 Fill Example (API Sources)

```markdown
## Research Topic 2: API & Service Sources

For "Remote Team AI Meeting Assistant", what API vendors are available?

1. Vendor survey: at least 5 comparable options
   (Deepgram, AssemblyAI, OpenAI Whisper, Google Speech-to-Text,
    Rev AI, Gladia, and LLM vendors: OpenAI, Anthropic, Gemini, Mistral)
2. Facts per vendor:
   - Pricing tiers (free quota, per-minute or per-token cost)
   - SLA / uptime guarantee
   - Rate limits (concurrent requests / monthly quota)
   - Regional availability (EU data residency options?)
   - Compliance (GDPR, SOC 2, HIPAA readiness)
   - Switching cost (API compatibility)
3. What do indie developers most commonly use? Why?
4. Recommended plan: primary vendor + 1-2 fallbacks
```

### Push Channel Dimension Note

> This project targets the overseas English market. Push channel research dimensions
> should cover: Email (SendGrid / Resend) / Slack integration / Discord bot /
> Web Push (browser notifications) / Webhook
> — not Mainland China channels (WeChat / Feishu / DingTalk).

### Final Prompt Excerpt (dual-path spec paragraph)

```markdown
## 🔀 Dual-Path Research Spec

- Path A (Technical/Official): WebSearch + WebFetch
  Keywords: official docs, GitHub repos, technical blogs
- Path B (Community/Reviews): WebSearch with community-oriented terms
  Examples: "[product] reddit", "best [feature] tool site:news.ycombinator.com",
  "[product name] alternative", "[category] G2 reviews 2025"

Source tags: [Official] / [Community] / [✅ Both] / [⚠️ Single-source] / [⚠️ Conflict]
Do NOT resolve conflicts — mark them and list both sources.
```

---

## Example C: Hardware / IoT Product (Smart home energy monitoring system)

### Skeleton Variables

| Variable | Value |
|----------|-------|
| Project definition | Smart home energy monitoring system: hardware captures per-circuit power consumption + cloud AI anomaly detection + real-time App view + monthly report, for energy-conscious homeowners |
| Target market | Global, priority on Mainland China first |
| Benchmark competitors | Xiaomi Smart Home, Sense Home Energy Monitor, Shelly (Europe) |
| Key resource type | C Hardware (energy sensors / metering chips) |
| Open-source reuse intent | C — borrow modules |
| Module list | Hardware acquisition layer, firmware/communications layer, cloud data ingestion, AI analysis layer, App UI, deployment/ops |
| Path B tool | muyu-search-mcp (primary market: Mainland China) + WebSearch (global sources) |

### Theme 2 Fill Example (Hardware Supply)

```markdown
## Research Theme 2: Hardware / Compute Supply

For "smart home energy monitoring system", how do we select and procure the core
sensors and metering chips?

1. BOM inventory: core hardware list
   - Single-phase/three-phase energy metering chips (at least 3 option comparison)
   - Communication modules (Wi-Fi / Zigbee / Matter)
   - MCU selection
   - PCB prototype resources
2. Facts per SKU:
   - Unit price / MOQ
   - Delivery lead time (LCSC/Huaqiangbei vs overseas suppliers)
   - Compatibility (interface / protocol / electrical certification: CCC / CE / UL)
   - Supply chain stability (single-source risk)
   - Technical support and documentation quality
3. Most common choices for maker / indie hardware developers: what do people use?
   Why?
4. Recommended approach: primary choice + fallback + mass-production upgrade path
```

### Special Handling for "Global + China Priority" Target Market

> Skeleton variable 2 is "Global, priority on Mainland China first"; `<path B tool>`
> uses a dual-strategy approach:
> - Primary Path B: muyu-search-mcp (covers domestic suppliers, LCSC, Huaqiangbei,
>   domestic CCC compliance)
> - Secondary Path B: WebSearch English terms (covers DigiKey/Mouser, GitHub IoT
>   projects, Matter protocol community)

### Final Prompt Excerpt (dual-path spec paragraph)

```markdown
## 🔀 Dual-Path Research Spec

This project targets the global market with priority on Mainland China.
Uses an enhanced dual-path strategy:

- Path A: Claude built-in WebSearch / WebFetch
  (English sources / GitHub / international standards docs)
- Path B (primary): muyu-search-mcp
  (domestic suppliers / LCSC / Zhihu / domestic compliance info)
  Invocation must follow the planning state machine;
  see parallel-dispatch-spec.md for details
- Path B (secondary): WebSearch English terms
  (DigiKey / Mouser / Matter community / overseas IoT forums)

Run Chinese and English search terms in parallel to ensure dual coverage of domestic
supply chain and international technical standards.

Annotation: [muyu] / [WebSearch-EN] / [WebSearch-Official] / [✅ Both] /
[⚠️ Single-source] / [⚠️ Conflict]
```

---

## Cross-Example Pattern Summary

| Dimension | Example A (China software) | Example B (International SaaS) | Example C (IoT hardware) |
|-----------|---------------------------|-------------------------------|--------------------------|
| Target market | Mainland China | Overseas English market | Global + China priority |
| Path B tool | muyu-search-mcp | WebSearch community terms | Both combined |
| Theme 2 type | Data type (4A) | API type (4B) | Hardware type (4C) |
| Push channel dimensions | WeChat/Feishu/DingTalk | Slack/Email/Discord | App + panel (adjusted by market) |
| Open-source keywords | Mixed Chinese/English | English primary | English primary + LCSC open-source |

**Conclusion**: The 4 themes' skeleton is fixed; content is entirely driven by skeleton
variables with no domain assumptions.
