# 14 Chapters in Detail - Chapters 8-14

> Split out of `14-chapters-detailed.md` (400-line ceiling).
> Chapters 1-7 are in that file; the two together are the complete fourteen.

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
