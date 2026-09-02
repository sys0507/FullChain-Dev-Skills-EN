# PRD vs TRD Boundary Decision Guide

> The core question: What goes into the PRD, and what must be left for the TRD (Technical Requirements Document)?

---

## The Simple Cut Rule

> **If an engineer can use a different implementation and still satisfy the requirement → keep it in the PRD**
> **If the engineer cannot use a different implementation → that's a technical decision, move it to the TRD**

---

## Boundary Comparison Table

| Content Type | Goes in PRD ✅ | Goes in TRD ❌ |
|---------|----------|----------|
| **Performance** | "First-screen ≤ 2s" | "Use Redis cache + CDN" |
| **Feature behavior** | "Core action returns results within 3 seconds" | "Use Claude API + Function Calling" |
| **Data requirements** | "Retain historical data ≥ 5 years" | "Use TimescaleDB with table partitioning" |
| **Interface contract** | "Need an event push interface with params: entity ID / event type / threshold" | "OpenAPI YAML + endpoint paths" |
| **Business rules** | "Item count limit: N" | "Use PostgreSQL CHECK constraint" |
| **Error handling** | "Return a clear error code when data is missing" | "Error code uses RFC 7807 format" |
| **Availability** | "99.5% availability" | "Use Kubernetes multi-replica + health checks" |
| **Security** | "Secondary confirmation required before sensitive operations" | "Use TOTP or SMS for 2FA" |
| **Compliance** | "Must not store unnecessary sensitive user information" | "Which encryption algorithm to use" |
| **UX** | "Key actions have a loading state" | "Use Suspense or useState" |

---

## Three Perspectives Compared

### Mainstream Perspective (Against Tech Details in PRD)
- **Core argument**: PRD writes What & Why; TRD writes How. Specifying "use React" in the PRD strips away the engineer's solution space.
- **Exception**: "Illustrative implementation" may be mentioned to clarify use cases, but no specific technology is mandated.

### Strict Perspective (Zero Tech in PRD)
- **Core argument**: PRD audiences include marketing/customer service/legal; technical details pollute the document.
- **In practice**: Technical constraints, APIs, data models, error codes → all go to TRD

### Spec-Driven / AI Perspective (Recommended by This Skill ⭐)
- **Core argument**: In the AI era, PRDs must be written to a "behavior-verifiable" precision, but **still do not specify the tech stack**.
- **Key insight**: PRD is not an implementation guide; it's the source for generating implementations — so it must reach the level of behavioral contracts.
- **In practice**: PRD writes behavioral contracts (input/output/boundary); does not write specific classes / libraries / frameworks.

---

## Handling Gray Areas

Some content doesn't cleanly fit into What or How. What to do?

### Gray Area 1: Database Schema
- ❌ Do NOT write: `CREATE TABLE users (id INT, ...)` — this is TRD
- ✅ Do write: "Need to store user's: basic info (name, registration date), favorites/follow list (≤ N items), notification preferences" — this is PRD (abstract data model)

### Gray Area 2: API Contract
- ❌ Do NOT write: Complete OpenAPI YAML — this is TRD
- ✅ Do write: "Need to provide an event push webhook interface containing: entity ID, event type, change magnitude, timestamp" — this is PRD (interface abstraction)

### Gray Area 3: Third-Party Dependencies
- ❌ Do NOT write: "Integrate ThirdPartyAPI (key in .env.API_TOKEN)" — this is TRD
- ✅ Do write: "Need a stable external data source supporting real-time + historical backfill, covering at least X years of history" — this is PRD (capability requirement)
- 🟡 May write in the PRD's "Constraints" chapter: "Data source must meet compliance requirements; commercially restricted data is not allowed"

### Gray Area 4: Performance Metrics
- ✅ Do write: "First-screen p95 < 2s" "API p95 < 200ms" — this is PRD (product requirement)
- ❌ Do NOT write: "Monitor with LCP metric + Lighthouse score ≥ 90" — this is TRD (implementation detail)

---

## Field Test: 5 Real Judgment Calls

Determine whether the following content belongs in the PRD or TRD:

| # | Description | Answer |
|:-:|------|:----:|
| 1 | "User can switch to advanced mode with one click" | PRD |
| 2 | "Use PostgreSQL as the primary database" | TRD |
| 3 | "Core action p95 < 500ms" | PRD |
| 4 | "Use WebSocket to push real-time updates" | TRD ("push real-time updates" is PRD; specific protocol is TRD) |
| 5 | "User password must be ≥ 8 characters and contain both letters and numbers" | PRD (business rule) |

---

## 3 Core Rules of Spec-Driven Development

Applies to "PRD consumed by AI Agents" scenarios:

### Rule 1: Do Not Describe Implementation Details
PRD is WHAT and WHY, not HOW.
- ✅ User can complete a search within 3 seconds
- ❌ Use Elasticsearch to implement search

### Rule 2: Include Enough Detail for AI Agents to Consume
Acceptance criteria, boundary conditions, and error handling must all be explicitly written out.

### Rule 3: Document Alternatives Considered
Put rejected alternatives into the PRD with reasons — this is critical context for AI reasoning.

---

## 3 Special Scenarios Where Tech Can Be Mentioned in a PRD

Although the general rule is no tech in PRD, the following 3 situations are exceptions:

### Scenario 1: Hard Technical Constraints
When external constraints mandate a specific technology, it may be written in the PRD's "Dependencies & Constraints" chapter:
- "Must use the company's unified SSO login"
- "Must be deployed on a specified cloud provider (compliance requirement)"

### Scenario 2: Technology Choice Is Itself the Product Differentiator
When a technology choice is itself the product's selling point:
- "Uses a local LLM to ensure data never leaves the country"
- "Blockchain records transaction logs for tamper-proof auditability"

### Scenario 3: Audience Needs Technical Context
When part of the PRD involves compliance / legal / user education:
- "We use AES-256 encryption for sensitive user data" (for compliance explanation)
- "We do not store user passwords in plaintext" (for user trust)

---

## Self-Check Checklist

Run through this after writing the PRD:

- [ ] No specific framework names (React/Vue/Django)
- [ ] No specific database names (PostgreSQL/MongoDB), except the 3 special scenarios above
- [ ] No concrete code examples (unless it's an abstract description of an API contract)
- [ ] No specific directory structure / file naming specified
- [ ] No specific design patterns specified ("use Repository pattern")
- [ ] Performance requirements are "product-level numbers" (p95 < 200ms), not "implementation-level numbers"
  (QPS / memory usage)

If the PRD contains anything that violates the above, ask yourself one question:
> **"If engineers implemented this with a completely different technology, would this requirement still hold?"**
>
> - Answer "Yes" → keep it in the PRD
> - Answer "No" → move it to the TRD
