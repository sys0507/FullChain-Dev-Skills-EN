# PRD 14-Chapter Detailed Template & Filling Guide

> 14 core chapters, each containing: **purpose + template snippet + anti-patterns**

---

## Table of Contents

| Chapter | Required/Recommended/Optional | Jump to |
|------|:-:|------|
| Chapter 1 · Document Info | ★ Required | [↓](#chapter-1--document-info-required-) |
| Chapter 2 · Project Background & Goals | ★ Required | [↓](#chapter-2--project-background--goals-required-) |
| Chapter 3 · Target Users & Personas | ★ Required | [↓](#chapter-3--target-users--personas-required-) |
| Chapter 4 · User Stories / Use Cases | ★ Required | [↓](#chapter-4--user-stories--use-cases-required-) |
| Chapter 5 · Feature List & Scope | ★ Required | [↓](#chapter-5--feature-list--scope-required-) |
| Chapter 6 · Detailed Feature Descriptions | ★ Required | [↓](#chapter-6--detailed-feature-descriptions-required-) |
| Chapter 7 · Non-Functional Requirements | ★ Required | [↓](#chapter-7--non-functional-requirements-required-) |
| Chapter 8 · UI / Interaction Notes | ☆ Recommended | [↓](#chapter-8--ui--interaction-notes-recommended-) |
| Chapter 9 · Acceptance Criteria | ★ Required | [↓](#chapter-9--acceptance-criteria-required-) |
| Chapter 10 · Priority / MVP Scope | ★ Required | [↓](#chapter-10--priority--mvp-scope-required-) |
| Chapter 11 · Metrics | ★ Required | [↓](#chapter-11--metrics-required-) |
| Chapter 12 · Dependencies & Constraints | ☆ Recommended | [↓](#chapter-12--dependencies--constraints-recommended-) |
| Chapter 13 · Risks & Open Questions | ★ Required | [↓](#chapter-13--risks--open-questions-required-) |
| Chapter 14 · Milestones / Timeline | ☆ Recommended | [↓](#chapter-14--milestones--timeline-recommended-) |
| **Chapter Usage Recommendations** (full / slim / minimal versions) | — | [↓](#chapter-usage-recommendations) |

---

## Chapter 1 · Document Info (Required ★)

**Purpose**: Let the reader immediately know "am I looking at the latest version".

**Template snippet**:

```markdown
## 1. Document Info

| Field | Value |
|---|---|
| Document Name | <Project Name> · Product Requirements Document |
| Version | v0.3 |
| Status | Draft / Review / Approved / Deprecated |
| Author | <PM Name> |
| Created Date | YYYY-MM-DD |
| Last Updated | YYYY-MM-DD |
| Reviewers | <Cross-functional review list> |

### Change Log
- v0.3 (YYYY-MM-DD) Added risk control module chapter
- v0.2 (YYYY-MM-DD) Supplemented non-functional requirements
- v0.1 (YYYY-MM-DD) Initial draft
```

**Anti-patterns**: No version number · Change log says "minor edits" · Status always stuck at Draft

---

## Chapter 2 · Project Background & Goals (Required ★)

**Purpose**: Answer "why is this worth doing right now".

**Template snippet**:

```markdown
## 2. Project Background & Goals

### 2.1 Background
<2-3 paragraphs clearly explaining:
- What does the current world look like?
- How do users currently solve this problem?
- What is lacking in the current situation?>

### 2.2 Goals
- **Business Goal**: <X users / Y retention / Z revenue within 6 months>
- **Product Goal**: <Reduce time for users to complete a task from X to Y>
- **Learning Goal** (for exploratory projects): <What hypothesis we want to validate>

### 2.3 Non-Goals (What We Are NOT Building)
- Not building <something>, because <reason>
- Not building <something else>, deferred to v2

### 2.4 Strategic Alignment
This project aligns with <company annual strategy / OKR / product portfolio>
```

**Anti-patterns**: Written as a KPI list · No "why now" · Missing Non-Goals

---

## Chapter 3 · Target Users & Personas (Required ★)

**Purpose**: Ensure all team members have the same user image in mind.

**Template snippet**:

```markdown
## 3. Target Users & Personas

### 3.1 Primary Persona P1: <Persona Name>
- **Background**: <Profession, age range, technical level>
- **Goals**: <What they come to our product to achieve>
- **Pain Points**: <Specific difficulties they currently face, 3-5 items>
- **Usage Frequency**: <How many times per day/week>
- **Devices**: <PC / mobile / tablet / multi-device>
- **Numeric Representative**: <How much money they're willing to spend monthly / time invested>

### 3.2 Secondary Persona P2: <Persona Name>
(Same structure as above)

### 3.3 Anti-Persona (Who We Are Explicitly NOT Serving)
- <A type of user>, reason: <...>
- <Another type of user>, reason: <...>
```

**Anti-patterns**: Written as "anyone who wants to do XX" (= wrote nothing) · Demographics only, no behavioral data

---

## Chapter 4 · User Stories / Use Cases (Required ★)

**Purpose**: Turn abstract goals into concrete scenarios so the team can empathize with users.

**Template snippet** (INVEST format):

```markdown
## 4. User Stories

### US-01 <Story Title>
As a <type of user>
I want to <do something> <in some context>
So that <I can achieve some goal>

**Trigger Context**: <When, where, in what mindset the user would use this>
**Expected Outcome**: <What state the user is in after completing the action>

### US-02 ...
```

**INVEST Self-Check**:
- **I**ndependent — independently deliverable
- **N**egotiable — can be negotiated
- **V**aluable — has user value
- **E**stimable — can be estimated
- **S**mall — small enough
- **T**estable — testable

**Anti-patterns**: Written as feature list ("system supports XX") · Missing Who/Why · One story spans multiple scenarios

---

## Chapter 5 · Feature List & Scope (Required ★)

**Purpose**: Tell the team in one sentence "what exactly are we building in this release".

**Template snippet**:

```markdown
## 5. Feature List & Scope

### 5.1 In-Scope (MVP v1.0 Must Have)
| ID | Feature Name | One-line Description | Related User Stories | Priority |
|---|---|---|---|:--:|
| F1 | <Core Feature A> | <One-line core value description> | US-01, US-03 | P0 |
| F2 | <Core Feature B> | <One-line core value description> | US-02 | P0 |
| F3 | <Supporting Feature C> | <One-line description> | US-04 | P1 |
| F4 | <Supporting Feature D> | <One-line description> | US-05 | P1 |

### 5.2 Out-of-Scope (Not in v1.0)
- ❌ <Feature E>, reason: <...> → Moved to v1.1
- ❌ <Feature F>, reason: <...> → Moved to v2.0
- ❌ Mobile APP → Not considered (validate needs with Web version first)
- ❌ Internationalization (multi-language) → Not considered

### 5.3 Priority Definitions
- P0 = Must have (product cannot launch without it)
- P1 = Should have (user experience significantly degraded without it)
- P2 = Nice to have (polish)
```

**Anti-patterns**: MVP scope > 8 features · No Out-of-Scope · All priorities are P0

---

## Chapter 6 · Detailed Feature Descriptions (Required ★)

**Purpose**: Inputs/outputs/flow/boundaries for every feature are explicit; engineers / AI don't need to "guess".

**Template snippet** (recommended "card style", one 4-tuple per feature):

```markdown
## 6. Detailed Feature Descriptions

### F1 <Core Feature A>

**Trigger**: <What action triggers this feature — user click / timer / API call>

**Inputs**:
- `param_name`: <type, meaning, constraints> (required/optional, default value)
- ...

**Core Flow**:
1. <Step 1>
2. <Step 2>
3. <...>

**Outputs**:
- `field_name`: <type, meaning>
- ...

**Boundary Conditions**:
- <Exception case 1> → <Handling method>
- <Exception case 2> → <Handling method>

**Error Handling**:
- <Error type> → <Error code / user message>

**Performance Requirements**: <Specific number, e.g. p95 < 200ms>

**Business Rules**:
- <Rule 1>
- <Rule 2>
```

**Anti-patterns**:
- ❌ Only feature name with no flow
- ❌ No boundary conditions / error handling
- ❌ Implementation details ("use Redis cache") written in
- ❌ Performance requirements written as "should be fairly fast"

---

## Chapter 7 · Non-Functional Requirements (Required ★)

**Purpose**: Quality baselines. NFRs must be in their own section, not buried in feature paragraphs.

**Template snippet**:

```markdown
## 7. Non-Functional Requirements (NFR)

### 7.1 Performance
- First-screen load p95 < 2 seconds
- API response p95 < 500ms
- Large list rendering (>1000 items) < 1 second
- Real-time data latency < 100ms (if real-time requirements exist)

### 7.2 Availability
- System monthly uptime ≥ 99.5% (i.e., downtime ≤ 3.6 hours/month)
- Availability ≥ 99.95% during critical business hours (specify if fixed peak periods apply)
- Failure recovery RTO < 5 minutes, RPO < 1 minute

### 7.3 Security
- User passwords encrypted at rest (bcrypt / argon2)
- API Keys encrypted at rest (AES-256)
- Sensitive operations require secondary confirmation (e.g., involving funds, data deletion)
- Audit log retention period (per industry compliance requirements, e.g., finance 7 years, healthcare 10 years)
- Do not store unnecessary sensitive user information

### 7.4 Compliance
- Comply with <relevant regulations (by industry and target market, e.g., finance: securities regulatory rules;
  global: GDPR; China: Personal Information Protection Law; healthcare: HIPAA, etc.)>
- Do not provide <industry red-line behaviors (fill in per compliance requirements)>

### 7.5 Data
- Key business data integrity: missing rate < 0.1%
- Data backup frequency: once per day
- Data retention: raw data ≥ <fill in per business and compliance requirements> years

### 7.6 Accessibility (A11y)
- Keyboard navigation support
- Color contrast ≥ WCAG AA standard
- Screen reader support

### 7.7 Internationalization (i18n)
- v1.0 only <target language>
- Character encoding UTF-8
```

**Anti-patterns**: NFR written as "system should be fast" · No specific numbers · Missing compliance section

---

## Chapter 8 · UI / Interaction Notes (Recommended ☆)

**Purpose**: Help design / frontend understand "what to present + how to interact".

**Template snippet**:

```markdown
## 8. UI / Interaction Notes

### 8.1 Information Architecture
(A Mermaid diagram showing main navigation / sub-page hierarchy)

### 8.2 Key Pages
- **Home / Dashboard**: <Key information cards + action buttons>
- **Core Feature Page**: <Input fields + result list>
- **Settings Page**: <...>

### 8.3 Key Interaction Flows
- Core action: User input → Loading state → Result display → Completion confirmation
- Notification receipt: Push notification → Click → Enter detail view

### 8.4 Design Links
- Figma: <link>
- Key Frame naming: <align with shared vocabulary>
```

**Anti-patterns**: Turning the PRD into a design review · Over-specifying colors / font sizes (that's the design team's job)

---

## Chapter 9 · Acceptance Criteria (Required ★)

**Purpose**: What does "done" mean — must be executable / machine-verifiable.

**Template snippet** (Given/When/Then format):

```markdown
## 9. Acceptance Criteria

### AC-F1-01: Core Feature A — Successful Operation
**Given** the user is logged in and <precondition>
**When** the user performs <target action>
**Then** the system <expected result>, and <quantifiable verification condition>

### AC-F1-02: Core Feature A — Boundary Condition
**Given** the user has reached <some limit>
**When** the user attempts <an action that triggers the boundary>
**Then** the system shows <a friendly error message>, and the action is not executed

### AC-F2-01: Core Feature B — Performance Acceptance
**Given** the system is in normal state
**When** the user <triggers the action>
**Then** results meeting the criteria are returned within <N seconds>

### AC-NFR-01: Performance Acceptance
**Given** <N> concurrent users
**When** users access the core page
**Then** p95 load time < <X seconds>
```

**Anti-patterns**: Written as "feature passes" · No quantifiable conditions · Missing acceptance criteria for error paths

---

## Chapter 10 · Priority / MVP Scope (Required ★)

**Purpose**: Clarify "what to build first" and prevent scope creep.

**Template snippet** (RICE / MoSCoW framework):

```markdown
## 10. Priority / MVP Scope

### 10.1 MVP Scope (v1.0)
**The 5 Core Things** (everything else is deferred):
1. <Core Feature A> (the primary path for users to complete the core task)
2. <Core Feature B> (key companion to the primary path)
3. <Supporting Feature C> (essential experience guarantee for MVP)
4. <Supporting Feature D> (required to validate the differentiating hypothesis)
5. <Base Feature E> (closes the product loop)

### 10.2 MVP Validation Hypotheses
Through the MVP we want to validate:
- Hypothesis 1: Target users are willing to replace <existing solution> with our tool
- Hypothesis 2: <Core feature> can address 80% of users' main scenarios

### 10.3 v1.1 Plan (After MVP)
- <Feature F>
- <Feature G>

### 10.4 Priority Scoring Method
Using RICE scoring: Reach × Impact × Confidence / Effort
| Feature | R | I | C | E | RICE |
|---|---|---|---|---|---|
| F1 | 100 | 3 | 0.9 | 2 | 135 |
```

**Anti-patterns**: MVP is a "complete product" · No validation hypotheses · No v1.1 / v2.0 breakdown

---

## Chapter 11 · Metrics (Required ★)

**Purpose**: What does "success" look like — what data do we look at post-launch to judge success.

**Template snippet** (North Star + AARRR):

```markdown
## 11. Metrics

### 11.1 North Star Metric
**<Frequency or depth of the product's core value behavior>** (DAU/WAU is not enough; measure depth of use)

### 11.2 Key Metrics
**Acquisition**
- Monthly new users ≥ X
- Channel conversion rate ≥ Y%

**Activation**
- Users completing a core action within 24h of registration ≥ 60%

**Retention**
- Day-1 retention ≥ 40%
- Day-7 retention ≥ 25%
- Day-30 retention ≥ 15%

**Revenue / Referral** (if applicable)

**Referral**
- Users voluntarily sharing N times

### 11.3 Counter-Metrics (Prevent "Metric Gaming")
- <Key depth-of-use metric> (prevent false activation from users who only complete onboarding)
- <For notification/push products> open rate ≥ 20% (skip if no push functionality)

### 11.4 Reporting Cadence
- Daily: DAU / key action conversion
- Weekly: retention / North Star
- Monthly: full AARRR
```

**Anti-patterns**: Only tracking DAU · No counter-metrics · No explanation of how to collect

---

## Chapter 12 · Dependencies & Constraints (Recommended ☆)

**Purpose**: Flag "what's blocking us / who we're waiting on".

**Template snippet**:

```markdown
## 12. Dependencies & Constraints

### 12.1 External Dependencies
| Dependency | Provider | Expected Ready Date | Risk Level |
|---|---|---|:--:|
| <Core data source/API> | <Provider type> | <Expected ready date> | <Risk level> |
| <Push/notification channel> | <Provider> | <Expected ready date> | <Risk level> |
| <Cloud/deployment resources> | <Cloud vendor> | <Expected ready date> | Low |

### 12.2 Internal Dependencies
- Design files by design team (deadline: day X)
- Data API by data team (deadline: day Y)

### 12.3 Constraints
- Budget: monthly server/SaaS costs ≤ <cap>
- Timeline: MVP must go live within <N> weeks
- Team: <team size> (e.g., 1 person solo + AI assistance)
- Legal: <relevant compliance constraints> (fill in by industry)
```

**Anti-patterns**: Missing this chapter (only discovering blockers at launch time) · No expected ready date / risk level

---

## Chapter 13 · Risks & Open Questions (Required ★)

**Purpose**: Flag "what's still uncertain + how to hedge known risks".

**Template snippet**:

```markdown
## 13. Risks & Open Questions

### 13.1 Risk Register
| ID | Risk | Severity | Probability | Mitigation |
|---|---|:--:|:--:|---|
| R-01 | Core data source/API changes or rate limiting | High | Medium | Prepare backup data source; monitor API status |
| R-02 | Push/notification frequency too high, causing user annoyance | Medium | High | Set push frequency cap + allow users to customize/disable |
| R-03 | Business involves regulatory red lines (by industry) | High | Low | Consult legal in advance; add disclaimers throughout |

### 13.2 Open Questions
- [ ] OQ-01: Can <key external dependency> meet <business requirement>? @PM to follow up
- [ ] OQ-02: Should <some feature> be included in MVP? Decision point: <date>
- [ ] OQ-03: <User experience/security/compliance> decision? @<owner> to decide
- [ ] OQ-04: How to define <important boundary condition>? @PM to convene discussion

### 13.3 Decision Log
(Once a decision is made, mark the corresponding OQ as closed)
- ✅ DR-01: <Decided item> → See ADR-001
```

**Anti-patterns**: Pretending everything is clear (no Open Questions) · Risks written as "there might be a problem" (not specific)

---

## Chapter 14 · Milestones / Timeline (Recommended ☆)

**Purpose**: When will it be done.

**Template snippet**:

```markdown
## 14. Milestones

### 14.1 Key Milestones
| Milestone | Target Date | Deliverable | Owner |
|---|---|---|---|
| M1 PRD Approved | YYYY-MM-DD | This document v1.0 | PM |
| M2 Technical Design Complete | YYYY-MM-DD | TRD + architecture diagram | Engineer |
| M3 Design Complete | YYYY-MM-DD | Figma | Designer |
| M4 Development Complete | YYYY-MM-DD | Demo-ready version | Engineer |
| M5 Testing Complete | YYYY-MM-DD | Test report | QA |
| M6 Launch | YYYY-MM-DD | Production environment | Engineer |

### 14.2 6-Week Cadence
- Week 1: Technical design + Figma
- Weeks 2-3: Frontend + backend parallel development (contract-first)
- Week 4: Integration + bug fixes
- Week 5: Testing + soft launch / gray release
- Week 6: Launch + observation period

### 14.3 Risk Buffer
Reserve 1 week buffer for unexpected delays
```

**Anti-patterns**: Timeline too rigid (no buffer) · No assigned owners · Milestones have no deliverables

---

## Chapter Usage Recommendations

### Full Version (for: medium/large projects / cross-team / B2B SaaS)
All 14 chapters

### Slim Version (for: personal projects / small teams / exploratory MVPs)
Keep #1, #2, #3, #5, #6, #9, #10, #11, #13 (9 chapters total)

### Minimal Version (for: solo projects / deliverable within 1 week)
Keep #2, #5, #6, #9, #13 (5 chapters total)

---

**Remember**: A longer PRD is not a better PRD. Write until it's clear, not a word more.
