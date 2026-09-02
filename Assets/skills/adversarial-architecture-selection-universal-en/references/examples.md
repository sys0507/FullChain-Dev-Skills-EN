# Examples · 3 End-to-End Adversarial Research Case Studies

> This file contains 3 complete examples across different domains, demonstrating the
> courtroom-style adversarial research methodology applied consistently across different selection scenarios.
> **Note**: examples are for method illustration only — not domain constraints.

## Table of Contents
- [Example A: Open-source fork selection (async task processing framework)](#example-a-open-source-fork-selection-async-task-processing-framework)
- [Example B: Library selection (AI/LLM framework comparison)](#example-b-library-selection-aillm-framework-comparison)
- [Example C: SaaS/cloud service selection (monitoring/observability platform)](#example-c-saascloud-service-selection-monitoringobservability-platform)
- [Cross-scenario methodology comparison](#cross-scenario-methodology-comparison)

---

## Example A: Open-source fork selection (async task processing framework)

### Scenario

**Target product**: Enterprise-internal task scheduling and message queue system — needs to support
scheduled tasks, delayed tasks, priority queues, task retries, and distributed Workers.

**Candidates (N=4)**:
1. **Celery** — Most popular distributed task queue in the Python ecosystem
2. **APScheduler** — Lightweight Python task scheduling library
3. **RQ (Redis Queue)** — Simple Redis-backed Python task queue
4. **Dramatiq** — Reliability-focused Python task processing framework

---

### Phase 0: Candidate Assignment

N=4; merge by "similar tech stack / complexity":

```markdown
# Candidate Assignment (Phase 0)

Total candidates N = 4
Project definition: Enterprise-internal task scheduling and message queue system

## Assignment

### Advocate 1 owns
- Celery (https://github.com/celery/celery)
Rationale: Most feature-rich, most complex ecosystem — needs a dedicated advocate to deep-dive

### Advocate 2 owns
- APScheduler (https://github.com/agronholm/apscheduler)
- RQ (https://github.com/rq/rq)
Rationale: Both are "lightweight scheduling" solutions, similar tech stack (both Python,
      both support Redis) — well-suited for comparison from the same perspective

### Advocate 3 owns
- Dramatiq (https://github.com/Bogdanp/dramatiq)
Rationale: Positioned as "reliability-first" — a direct Celery competitor, needs its own advocate

### Red Team
Fixed 1 agent

### Integration Assessor
Fixed 1 agent

## Overall Strategy
Core tradeoff is "feature richness vs. operational complexity".
Focus on broker dependencies, task persistence, and monitoring ecosystem.
```

---

### Phase 1: Position Paper Excerpt (Celery advocate)

#### Dimension 5: Adaptation cost estimate (excerpt)

```markdown
### 5. Adaptation Cost Estimate

Forking Celery and integrating it into the target product:

| Adaptation item | Estimated person-days | Risk |
|---|:---:|---|
| Connect to target data source (business DB adapter) | 2-3 | Low (Beat scheduler base class available) |
| Custom priority queue strategy | 3-5 | Medium (requires routing_key configuration) |
| Connect to internal notification/alert channel | 1-2 | Low |
| Set up Flower monitoring dashboard | 2-3 | Low (works out of the box) |
| Configure Redis Sentinel HA | 3-5 | ⚠️ High (single point of failure risk, needs testing) |

**Total estimate: 11-18 person-days**
```

#### Dimension 6: Fatal flaw self-report (excerpt)

```markdown
### 6. ⭐ Fatal Flaw Self-Report (Mandatory)

I (Advocate 1) must honestly self-report Celery's 3 biggest flaws:

**Flaw 1**: Default serialization uses pickle — a security vulnerability
- Evidence: celery/app/serialization.py — default CELERY_TASK_SERIALIZER="pickle"
- Impact: In distributed environments, attackers can execute arbitrary code via malicious payloads;
  must force-switch to JSON and update all task signatures — adds ~2 person-days adaptation cost

**Flaw 2**: Single-node Broker (Redis/RabbitMQ) is a single point of failure (SPF)
- Evidence: Official docs "High Availability" section explicitly labeled "Experimental";
  GitHub Issue #4878 (open for 2+ years)
- Impact: Broker outage causes all tasks to be lost; production requires Redis Sentinel or RabbitMQ cluster

**Flaw 3**: Task state persistence requires extra configuration — results not persisted by default
- Evidence: CELERY_RESULT_BACKEND defaults to "disabled" (celery/app/defaults.py L89)
- Impact: Task execution history requires separate Result Backend (Redis/DB) configuration,
  otherwise no audit trail
```

---

### Phase 2: Courtroom Debate Excerpt

#### Red Team challenges Celery (Round 1, Challenge 2)

> **Red Team → Advocate 1**:
>
> Celery's configuration complexity is a well-known pain point. The official docs have 200+
> configuration options (measured: `celery/app/defaults.py` contains 347 lines of config definitions),
> with a steep team learning curve. A typical production config file usually needs 50-100 lines of YAML.
> This conflicts with the "fast enterprise-internal deployment" goal — explain how you'd control the complexity.

#### Advocate 1 response (≤ 200 words)

> **Advocate 1 → Red Team**:
>
> The complexity is real — acknowledged. But three counter-points:
> 1. Complexity = feature coverage. Enterprise task systems ultimately need priority queues, retries, and
>    monitoring. Building those from scratch in RQ/APScheduler has higher total development cost.
> 2. Official packages like `django-celery-beat` and `celery[redis]` provide pre-configured setups;
>    minimum production config is ~20 lines.
> 3. We can wrap an internal `TaskFactory` base class that hides 90% of configuration details —
>    business layer only needs to inherit and define `run()`.
>
> Complexity is an engineering problem, not a disqualifier.

#### Integration Assessor challenges Advocate 1

> **Integration Assessor → Advocate 1**:
>
> My evaluation shows Celery + Dramatiq composite recommendation score (7.2) vs. single-fork Celery (7.5)
> is only a 0.3 gap. The composite lets simple scheduled tasks run on Dramatiq (zero dependencies,
> lightweight) while complex workflows run on Celery. Why insist on single-fork Celery over composite?

#### Advocate 1 response

> **Advocate 1 → Integration Assessor**:
>
> The composite approach is attractive, but has two engineering problems:
> 1. Dual-stack operations (maintaining both Celery+Redis and Dramatiq+RabbitMQ) — monitoring
>    needs to be unified across both.
> 2. Task routing logic (which tasks go to Celery vs. Dramatiq) requires explicit awareness at the
>    business layer, increasing cognitive overhead.
>
> If the Integration Assessor's evaluation shows both data models can route transparently via an
> adapter layer, I can accept the composite approach.

---

### Phase 3: Decision Summary

```markdown
# 06 Architecture Baseline Decision (Example A)

## 1. Decision Summary

**Architecture baseline**: Celery (primary) + Dramatiq (simple task overflow) composite

**One-sentence rationale**: Celery covers complex workflows; Dramatiq handles high-frequency simple
tasks; an adapter layer provides transparent routing; shared Redis broker reduces operational overhead.

## 2. Reuse Matrix

| Module | Source | Treatment | Adaptation |
|---|---|---|---|
| Complex task scheduling engine | Celery | Adapted | Wrap TaskFactory base class, hide config |
| High-frequency simple task queue | Dramatiq | Direct reuse | — |
| Broker | Redis (shared) | Self-hosted HA | Sentinel configuration |
| Task monitoring dashboard | Flower (Celery ecosystem) | Direct reuse | — |
| Task routing adapter | Custom | New build | Transparent simple/complex routing |

## 4. Open Questions

1. Does the Redis Sentinel HA solution meet the company's SLA requirements (99.9% uptime)?
2. After switching Celery serialization to JSON, how large is the existing codebase impact?
3. Can Dramatiq and Celery share the same Redis DB for their Result Backends?
```

---

## Example B: Library selection (AI/LLM framework comparison)

### Scenario

**Target product**: Enterprise-internal knowledge base RAG (Retrieval-Augmented Generation) system —
needs multi-format document parsing, vectorization, semantic retrieval, Agent tool calls, LLM chat.

**Candidate libraries (N=3)**:
1. **LangChain** — Broadest LLM application framework
2. **LlamaIndex** — LLM framework focused on data indexing and retrieval
3. **Haystack** — Enterprise search and Q&A NLP framework

N=3, ideal state: 1 Advocate = 1 library.

---

### Phase 0: 7-Dimension Adaptation (library selection)

In a library selection scenario, the 7 dimensions need adjusted meanings:

| Dimension | Original (fork scenario) | Adapted (library selection) |
|---|---|---|
| 1. Architecture overview | Project directory + Mermaid diagram | Library's core module diagram + typical usage flow |
| 2. Core capabilities | Feature list + maturity | API feature list + version stability (Stable/Beta/Deprecated) |
| 3. Data model | Key classes/tables | Core abstract classes/interfaces (e.g., `BaseRetriever`, `BaseLLM`) + data flow formats |
| 4. Extension points | Hooks/plugins | Custom component interfaces, 3rd-party integration ecosystem (provider count) |
| 5. Adaptation cost | Fork adaptation person-days | Learning curve (weeks) + integration work (person-days) + version upgrade maintenance cost |
| 6. Fatal flaw self-report | Project flaws | API stability issues / performance bottlenecks / dependency hell / community maintenance risk |
| 7. Integration feasibility | Compatibility with other fork projects | Co-existence potential with other libraries (multi-library overhead) |

> Lead documents the specific meaning of each dimension in `00-task-assignment.md`; Advocates fill
> papers according to the adjusted meanings.

---

### Phase 1: LangChain Advocate Position Paper Excerpt

#### Dimension 6: Fatal flaw self-report

```markdown
### 6. ⭐ Fatal Flaw Self-Report (Mandatory)

I (Advocate 1) must honestly self-report LangChain's 3 biggest flaws:

**Flaw 1**: Historically unstable API — many breaking changes across version upgrades
- Evidence: LangChain GitHub Releases — v0.1→v0.2 has 30+ breaking changes;
  Community Issue #12441: "Migration from 0.0.x is painful" (2024-03, 2000+ reactions)
- Impact: Pinning version blocks security updates; tracking upgrades requires a maintenance
  adapter layer — roughly 2-5 person-days per upgrade cycle

**Flaw 2**: Deep abstraction layers make debugging difficult — stack traces typically 15+ levels
- Evidence: Measured LangChain LCEL chain typical error stack trace at 18 levels
  (test code at examples/debug_test.py)
- Impact: High time cost to diagnose production issues; new team members need ~2-3 weeks to ramp up

**Flaw 3**: Large package footprint and heavy dependency chain (~50+ dependencies pulled on install)
- Evidence: `pip install langchain` pulls 52 packages totaling ~380MB
- Impact: Container image bloat; increased cold-start time (significant in Lambda/Serverless scenarios)
```

---

### Phase 2: Debate Excerpt

#### Red Team challenges LangChain

> **Red Team → Advocate 1**:
>
> LangChain's API instability is structural, not temporary. Looking at LangChain's CHANGELOG:
> in 2023-2024, the core abstractions `Chain`, `Agent`, and `Tool` were refactored 3 times
> (0.0.x → 0.1.x → LCEL). An enterprise RAG system typically has a 3-5 year lifetime — the
> cumulative engineering cost of tracking upgrades may exceed the cost of writing a lightweight
> custom implementation. Please respond to this directly.

#### Advocate 1 response

> **Advocate 1 → Red Team**:
>
> The API change risk is real. But two mitigation strategies:
> 1. Use the "Adapter Pattern" to isolate LangChain — business layer only depends on internal
>    abstract interfaces; LangChain changes only require updating the adapter layer (~200 lines),
>    leaving business code untouched.
> 2. LangChain committed to LTS versions starting v0.2 (see official blog, June 2024), reducing
>    the risk of major version jumps.
>
> Red Team's point is valid — the adapter pattern is necessary and should be written into the
> adaptation plan.

---

### Phase 3: Decision Summary

```markdown
# 06 Architecture Baseline Decision (Example B)

## 1. Decision Summary

**Architecture baseline**: LangChain (Agent orchestration layer) + LlamaIndex (Retrieval layer) composite

**One-sentence rationale**: LangChain excels at tool calls and Agent orchestration; LlamaIndex leads
in complex document indexing and hybrid retrieval; combining via standardized interfaces avoids
single-framework capability gaps.

## 2. Reuse Matrix

| Module | Source | Treatment | Adaptation |
|---|---|---|---|
| Agent tool calls | LangChain | Direct reuse | Wrap Tool interface to isolate version changes |
| Document parsing / chunking | LlamaIndex | Direct reuse | Connect to internal storage |
| Vector retrieval | LlamaIndex | Direct reuse | Configure internal vector database |
| Hybrid retrieval (BM25 + vector) | LlamaIndex | Direct reuse | — |
| LLM call layer | LangChain | Adapted | Adapter pattern to isolate version changes |
| Frontend Chat UI | Custom | New build | Neither framework has a suitable UI layer |

## 4. Open Questions

1. Is LangChain v0.2 LTS support lifecycle long enough to cover the project lifetime (3-5 years)?
2. When mixing LlamaIndex + LangChain, are the Document object serialization formats compatible?
3. If LangChain undergoes another major rewrite, what is the migration contingency plan to full LlamaIndex?
```

---

## Example C: SaaS/cloud service selection (monitoring/observability platform)

### Scenario

**Goal**: Select a monitoring/observability platform for a multi-team SaaS product (~20-person
engineering team, 50+ microservices) — needs to cover Metrics, Logs, Traces, and frontend error monitoring.

**Candidates (N=4)**:
1. **Datadog** — Commercial full-stack observability SaaS
2. **Grafana + Prometheus (self-hosted)** — Open-source metrics + visualization
3. **New Relic** — Commercial full-stack APM + observability
4. **Sentry** — Focused on error tracking and performance monitoring

---

### Phase 0: 7-Dimension Adaptation (SaaS selection)

| Dimension | Adapted (SaaS selection) |
|---|---|
| 1. Architecture overview | Product capability map + data flow (how data flows from user services to the platform) |
| 2. Core capabilities | Out-of-the-box features (Metrics/Logs/Traces/Alerts etc.) |
| 3. Data model | Data export formats / API contracts / data retention periods |
| 4. Extension points | Plugins / webhooks / custom dashboards / data export APIs |
| 5. Adaptation cost | Migration cost (from current solution) + integration work + SDK onboarding person-days |
| 6. Fatal flaw self-report | Lock-in risk / pricing traps / data sovereignty / compliance issues |
| 7. Integration with others | Can it be used alongside alternatives (e.g., Sentry + Datadog dual-stack)? |

---

### Phase 1: Datadog Advocate Position Paper Excerpt

#### Dimension 2: Core capabilities

```markdown
### 2. Core Capabilities

- ✅ Stable: Metrics collection — 500+ official integrations, Agent auto-discovery with zero config
- ✅ Stable: Distributed tracing (APM/Traces) — automatic instrumentation, non-invasive
- ✅ Stable: Log management — centralized collection + correlation with Traces
- ✅ Stable: Alerting — Multi-condition alerts, PagerDuty/Slack integration
- 🟡 Beta: Error tracking — basic functionality, not as specialized as Sentry
- 🟡 Beta: Synthetic Monitoring — full-featured but API not stable
- ❌ Weak: Frontend RUM (Real User Monitoring) — exists but community reports accuracy gaps
```

#### Dimension 6: Fatal flaw self-report

```markdown
### 6. ⭐ Fatal Flaw Self-Report (Mandatory)

I (Advocate 1) must honestly self-report Datadog's 3 biggest flaws:

**Flaw 1**: Pricing scales exponentially with Metrics volume — mid-size teams can hit $5k+/month
- Evidence: Datadog pricing page — Custom Metrics over 100 costs $0.05/metric/month;
  Estimate for 50 microservices: ~5000+ custom metrics, monthly cost ~$3,000-8,000
  (see Datadog pricing calculator screenshot, 2025-12)
- Impact: Cost grows non-linearly with business scale, hard to budget; community has documented
  multiple "bill shock" incidents

**Flaw 2**: Data cannot leave certain regions — may not meet data residency compliance requirements
- Evidence: Datadog data centers are in US/EU/AP regions (see official "Data Residency" docs)
- Impact: If the business has data localization requirements, Datadog may be non-compliant;
  data anonymization feasibility must be evaluated

**Flaw 3**: Proprietary query language (DDL/DQL) creates lock-in — migration out of Datadog is costly
- Evidence: Datadog Dashboard JSON format is proprietary, cannot be exported to Grafana/Prometheus;
  alert rules use DQL, not compatible with PromQL
- Impact: Once on Datadog, all historical Dashboards + alert rules must be fully rewritten to migrate
```

---

### Phase 2: Debate Excerpt

#### Red Team challenges Datadog (pricing lock-in)

> **Red Team → Advocate 1**:
>
> Datadog's pricing trap is well-known in the engineering community. Multiple Hacker News posts
> document teams whose bills jumped from $500/month to $15,000/month after a code change accidentally
> produced large volumes of custom metrics. For a 50-microservice system this is a structural risk —
> the DogStatsD client library by default produces independent-dimension metrics per service instance.
> How do you control this risk?

#### Advocate 1 response

> **Advocate 1 → Red Team**:
>
> The pricing risk is real — acknowledged. Mitigation plan:
> 1. Set Datadog billing alert threshold; trigger alert at $3k/month (Datadog supports budget alerts)
> 2. Add "metrics cardinality check" in CI/CD pipeline — detect new custom metrics count before PR merge
> 3. Use Datadog Agent metrics filter config — only report core metrics, reducing total custom metrics count
>
> Trade-off: requires 2-3 person-days to maintain a metrics governance toolchain.

#### Integration Assessor challenges Datadog Advocate

> **Integration Assessor → Advocate 1**:
>
> My evaluation shows Grafana + Prometheus (self-hosted) + Sentry (specialist) composite recommendation
> score (7.8) exceeds single Datadog (7.0). Main advantages: zero lock-in risk + full data sovereignty +
> predictable cost. Operational overhead is the primary downside. Explain why Datadog is still preferred.

#### Advocate 1 response

> **Advocate 1 → Integration Assessor**:
>
> The operational burden of self-hosting is underestimated. Grafana + Prometheus requires:
> 1. Prometheus HA (Thanos/Cortex) — ~3-5 person-days initial setup + ~1 person/week ongoing
> 2. Separate storage planning and scaling for Loki (logs) + Tempo (traces)
> 3. Prometheus/PromQL training for 2-4 engineers (~1 week each)
>
> For a 20-person team without a dedicated SRE, these operational burdens fall on product engineers.
> Datadog's value is "giving SRE time back to product work."

---

### Phase 3: Decision Summary

```markdown
# 06 Architecture Baseline Decision (Example C)

## 1. Decision Summary

**Architecture baseline**: Grafana + Prometheus (self-hosted, primary) + Sentry (error monitoring specialist)

**One-sentence rationale**: Self-hosted gives full data sovereignty, predictable cost, and zero lock-in;
Sentry is significantly better than self-built for error tracking — the combination covers full-stack
observability needs.

## 2. Reuse Matrix

| Module | Source | Treatment | Adaptation |
|---|---|---|---|
| Metrics collection and storage | Prometheus (self-hosted) | Direct deployment | Configure HA (Thanos) |
| Visualization dashboards | Grafana (self-hosted) | Direct deployment | Connect to Prometheus data source |
| Log management | Loki (Grafana ecosystem) | Direct deployment | Configure log retention policy |
| Distributed tracing | Tempo (Grafana ecosystem) | Direct deployment | Connect existing service SDKs |
| Error tracking / frontend monitoring | Sentry (SaaS) | Integrate Sentry SDK | ~0.5 person-days per service |
| Alerting routing | Alertmanager | Direct reuse | Configure PagerDuty/Slack routing |

## 3. Why Rejected Candidates Didn't Make It

### Why Datadog wasn't selected
- Advocate's self-reported flaw 1 (pricing risk) was fully substantiated by Red Team in Phase 2;
  the mitigation (metrics governance toolchain) requires extra person-days, confirming structural risk
- Data sovereignty issue (flaw 2) was not cleared in compliance evaluation
- Lock-in risk (flaw 3) conflicts with the team's principle of "maintaining technical flexibility"

### Why New Relic wasn't selected
- Integration Assessor score: 6.0 — high feature overlap with Datadog, similar lock-in risk,
  weaker open-source ecosystem support than Grafana; no sufficient differentiating advantage

## 4. Open Questions

1. Has the Thanos (Prometheus HA) storage cost estimate accounted for data growth curves?
2. If the team needs SLA reports within 6 months, does Grafana's SLA Dashboard meet requirements?
3. Does Sentry also have data sovereignty concerns? (Confirm Sentry SaaS data center locations)

## 5. Total Adaptation Cost Estimate

| Item | Person-days |
|---|:---:|
| Prometheus + Grafana deployment and configuration | 3-5 |
| Thanos HA setup | 3-5 |
| Loki + Tempo deployment | 2-3 |
| Sentry SDK integration across all microservices | 10-15 (50 services × 0.2-0.3 days) |
| Alert rules migration / creation | 3-5 |
| Team PromQL training | 4 (4 engineers × 1 week, part-time) |
| **Total** | **25-37** |

Monthly budget estimate: {X} (based on cloud storage cost + Sentry Team plan subscription, currency per target market)
```

---

## Cross-scenario Methodology Comparison

| Dimension | Example A (fork selection) | Example B (library selection) | Example C (SaaS selection) |
|---|---|---|---|
| **Fatal flaw focus** | Project activity / hardcoded core modules / test coverage | API stability / dependency hell / abstraction complexity | Lock-in risk / pricing traps / data sovereignty |
| **Integration assessment focus** | Can data models be joined / shared Broker | Multi-library co-existence overhead / interface format compatibility | Can they be used together (dual-stack) / data export interoperability |
| **Open Questions focus** | Core adaptation technical feasibility / test gap strategy | Version pinning strategy / multi-framework interface isolation | Migration contingency / compliance confirmation / ops headcount |
| **Decision pattern** | Composite (primary framework + lightweight supplement) | Composite (each library owns its best layer) | Primary solution + specialist tool mix |
| **7-dimension adaptation** | Original (no changes needed) | Dimension 5 → "learning curve + integration work" | Dimension 3 → "data export formats"; Dimension 6 → "lock-in / compliance" |

> **Core conclusion**: The courtroom adversarial research methodology (5 roles + 3 phases + 6 anti-bias
> constraints) remains consistent across all selection scenarios. What changes is only the specific meaning
> of the 7 dimensions, and the core dispute points in Phase 2. Lead adapts the 7-dimension definitions
> at Phase 0 based on the scenario type; the rest of the process is unchanged.
