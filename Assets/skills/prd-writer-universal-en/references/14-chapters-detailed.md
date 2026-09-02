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

---

Chapters 8-14 are in `references/14-chapters-detailed-part2.md`.
