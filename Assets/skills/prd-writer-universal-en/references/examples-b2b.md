# PRD Example - B2B Internal Tool

> Split out of `examples.md` (400-line ceiling).
> Example A (SaaS tool) and Example B (consumer app) are in that file.

## Example C: B2B Internal Tool (Enterprise Knowledge Base)

**Project**: Internal enterprise knowledge base + AI Q&A system, for all employees at companies with 100–500 headcount
**Applicable PRD version**: Full 14 chapters

---

### C · Chapter 2: Project Background & Goals

#### 2.1 Background

As the company grew from 50 to 200 employees, knowledge silos and information fragmentation became acute: new hires rely on asking colleagues, and it takes an average of 2–3 weeks to fully onboard; experienced employees' core knowledge lives in personal laptops and heads — when they leave, it leaves with them; documents are scattered across multiple systems (internal wiki, Notion, file shares, email attachments), and finding a document takes longer than doing the actual work.

Current information retrieval methods: keyword search (low precision, requires knowing the document title), asking colleagues (consumes their time), asking managers (creates an information bottleneck). The company estimates each employee wastes 3–5 hours per week "looking for information" — roughly $2M in annual labor cost across the organization.

We are building an internal enterprise knowledge base + AI Q&A system that consolidates scattered documentation, allowing any employee to ask a question in natural language and receive an accurate, source-cited answer within 30 seconds — while creating a knowledge flywheel: the more it is used, the richer the knowledge base becomes.

#### 2.2 Goals

- **Business goal**: Within 6 months, reduce the frequency of employees asking colleagues "because they couldn't find the information" by 50% (validated via periodic surveys)
- **Product goal**: AI Q&A accuracy ≥ 85% (manual sampling evaluation); search result click-through rate ≥ 60%
- **Operational goal**: Cover core documents from 80% of company departments within 3 months of launch

#### 2.3 Non-Goals

- No external-facing knowledge base (customer-facing FAQ) — that is a separate product
- Not replacing existing wiki / Notion as the primary editing tool — integrate for discovery, don't migrate storage
- No real-time collaborative editing — users edit in their existing tools; the knowledge base handles "find" and "ask"

---

### C · Chapter 3: Target Users & Personas

#### 3.1 Primary Persona P1: General Employee "Jamie" (Content Consumer)

- **Background**: 25 years old, customer support specialist, 6 months on the job, handles many customer inquiries daily
- **Goal**: Find standard answers quickly without asking a manager every time
- **Pain points**: Doesn't know which document contains the canonical answer to a given question; too many document versions — unclear which is current; search returns too many results but none are accurate
- **Usage frequency**: 10–20 queries per day
- **Devices**: Company Windows PC, Chrome browser

#### 3.2 Secondary Persona P2: IT Admin "Chris" (System Administrator)

- **Background**: 32 years old, IT operations, responsible for company system security and access management
- **Goal**: Ensure knowledge base data is not accessed without authorization; manage document sources and permissions efficiently
- **Pain points**: Concerned that sensitive documents (finance, HR data) may be accessed by unauthorized employees; cross-system SSO integration is complex
- **Usage frequency**: Ongoing monitoring; monthly audits

#### 3.3 Anti-Personas (explicitly not served)

- **Scenarios requiring external collaboration (vendors / customers)**: External parties cannot access the internal knowledge base; external collaboration uses separate tooling
- **Developers who need the knowledge base to expose a public API**: v1.0 is internal-only; API access is considered for v2.0
- **Cases requiring a multi-tenant SaaS deployment**: v1.0 is single-tenant, internally deployed

---

### C · Chapter 7: Non-Functional Requirements (Enterprise Focus)

#### 7.1 Performance

- Keyword search p95 < 1 second
- AI Q&A first-token response < 3 seconds; full response complete < 15 seconds
- Supports 200 concurrent users with no degradation in p95 response time

#### 7.2 Availability

- Business hours (9 AM–8 PM on workdays) uptime ≥ 99.9%
- Off-hours ≥ 99.0%
- Planned maintenance window: every Sunday 2:00–4:00 AM

#### 7.3 Security & Access Control (Enterprise Core)

- **Access control**: Department/role-based document permissions (RBAC); employees can only access documents within their permission scope
- **SSO integration**: Must integrate with the company's existing Identity Provider (Okta / Azure AD / LDAP); no standalone account system permitted
- **Data isolation**: Finance, HR, and other sensitive department documents must have separate permission groups; not visible to other departments by default
- **Audit log**: Record all document access, AI Q&A queries, and permission change events; retain for 1 year (compliance requirement)
- **Data residency**: All AI model calls must use on-premises or in-region services; internal documents must not be transmitted to external servers without explicit authorization

#### 7.4 Compliance

- Compliant with applicable data protection regulations in the company's operating jurisdictions
- Data classification: documents tagged by sensitivity level (Public / Internal / Confidential / Restricted) per company data security policy
- When an employee leaves, ownership of their uploaded documents is automatically transferred to their manager

#### 7.5 Data Integrity

- Document sync latency: knowledge base index updated within ≤ 15 minutes of source document changes
- Search results always display source document name and last-updated timestamp to prevent citing stale information

---

### C · Chapter 10: Prioritization / MVP Scope

#### 10.1 MVP Scope (v1.0 — recommended 3-month delivery)

**Core 5 deliverables** (everything else deferred):
1. Primary document source auto-sync and indexing (covering the company's most active doc repository)
2. Natural language AI Q&A (with source citations and confidence indicators)
3. SSO single sign-on (integrated with company IdP; no new registration required)
4. Basic RBAC permissions (department-level access isolation)
5. Full-text keyword search (fallback / degraded mode when AI Q&A is unavailable)

#### 10.2 MVP Validation Hypotheses

- Hypothesis 1: Employees will change their search habits — switching from "search in the existing wiki" to "ask the knowledge base AI"
- Hypothesis 2: AI Q&A accuracy ≥ 85% will build user trust, turning it into a daily habit rather than "tried once and abandoned"

#### 10.3 v1.1 Roadmap (post-MVP validation)

- Additional document source integrations (Notion, local file upload)
- Knowledge contribution leaderboard (incentivize employees to organize and contribute docs)
- AI Q&A quality feedback (users can mark whether an answer was helpful)

#### 10.4 Explicitly Out-of-Scope (prevent scope creep)

- ❌ Company-wide rollout from day one — MVP phase: 2–3 seed departments only (e.g., support + product) as pilot
- ❌ Full historical document migration — only sync documents from the past 2 years; older archives excluded
- ❌ Multi-language UI — v1.0 is single-language only

---

### C · Chapter 12: Dependencies & Constraints

#### 12.1 External Dependencies

| Dependency | Provider | Expected Ready | Risk Level |
|---|---|---|:--:|
| Document source API (for sync) | Primary doc platform (e.g., Confluence, Notion API) | Already available | Low |
| AI language model service (Q&A engine) | TBD (OpenAI / Azure OpenAI / self-hosted) | Finalize within 2 weeks | Medium |
| Company IdP / SSO interface | IT department | Requires IT approval, ~3 weeks | High |
| Server infrastructure (cloud or on-premises) | IT department | Confirm within 1 week | Medium |

#### 12.2 Internal Dependencies (Critical Path)

- **IT security review**: SSO integration and network access requests must go through the company IT security review process (~3–4 weeks) — the single most critical bottleneck
- **Data classification definition**: Each department must cooperate to label document sensitivity tiers (requires department content owners' participation)
- **Seed department cooperation**: Support and product teams must designate a document owner to lead initial document organization

#### 12.3 Constraints

- Budget: cloud services (including AI API) ≤ $2,000/month
- Timeline: seed department pilot complete within 3 months; company-wide rollout within 6 months
- Team: 1 engineer + 1 PM + external AI integration consultant
- Legal: AI model must not use services that transmit internal documents to unauthorized external servers; data residency requirements must be satisfied per company security policy

---

## Key Differences Across the Three Examples

| Dimension | Example A (SaaS Tool) | Example B (Consumer App) | Example C (B2B Internal) |
|---|---|---|---|
| PRD version | Full 14 chapters | Condensed 9 chapters | Full 14 chapters |
| Core NFR focus | Performance + Availability | Privacy + Health data compliance | Security + Permissions + Audit |
| North Star metric | Weekly active sessions | 7-day consecutive usage rate | Knowledge base search usage rate |
| Key risk | API stability + competitors | Medical advice red lines | Internal IT approvals + data access |
| Open Questions focus | Pricing strategy + GDPR | Device compatibility + template compliance | IT approval process + data residency |
| MVP scoping method | Limit feature count | Limit platform (iOS only initially) | Limit departments (seed pilot) |
| Persona characteristics | Primary (engineer) + secondary (TL) | Primary + medical-risk anti-persona | Dual personas (consumer + admin) |
| Compliance focus | GDPR + cross-border data | Medical advice lines + audio privacy | Data security law + SSO + data classification |

---

## How to Use These Examples Correctly

1. **Find the example closest to your product type** and use it as a reference for filling in your own PRD
2. **Do not copy the content verbatim** — the value of these examples lies in the "thinking approach," not the specific numbers or wording
3. **Focus on the differences table** to understand the fundamental differences in PRD emphasis across product types
4. **Use together with `14-chapters-detailed.md`** — examples show "what to fill in," the detailed template shows "how to write it"

> Full chapter templates and anti-pattern rules: `14-chapters-detailed.md`
> PRD vs TRD boundary judgment: `prd-vs-trd-boundary.md`
> Quality self-check after writing: `prd-anti-patterns.md`
