# Adversarial Selection Example - SaaS / Cloud Service

> Split out of `examples.md` (400-line ceiling).
> Example A (open-source fork) and Example B (library selection) are in that file.

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
