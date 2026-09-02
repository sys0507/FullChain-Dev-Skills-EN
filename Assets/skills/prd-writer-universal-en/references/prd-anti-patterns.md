# PRD Anti-Pattern Checklist

> Run through this checklist after writing every PRD. If any item appears, go back and fix it.

---

## Fatal Anti-Patterns (Send Back Immediately on Sight)

### ❌ 1. PRD Has No "Why" (Missing Background & Goals)
**Symptom**: Features listed directly, with no "why are we doing this"
**Why it's a problem**: The team has no basis for prioritization; work drifts without knowing it
**Fix**: Add §2 Project Background & Goals

### ❌ 2. No Out-of-Scope (Scope Will Explode)
**Symptom**: Only writes "what to build", not "what NOT to build"
**Why it's a problem**: Requirements get added mid-development; the original scope can't be protected
**Fix**: Every Scope section must be accompanied by 3-5 Out-of-Scope items

### ❌ 3. Acceptance Criteria Written as "The System Should Be User-Friendly"
**Symptom**: Acceptance criteria are vague ("friendly" / "efficient" / "fast")
**Why it's a problem**: Cannot be machine-verified; QA can't test it; AI can't understand it
**Fix**: Use Given/When/Then format + specific numbers

### ❌ 4. Tech Stack Written Into the PRD
**Symptom**: "Use React + PostgreSQL + Redis"
**Why it's a problem**: Strips away the engineer's solution space; pollutes document boundaries
**Fix**: Move to the TRD (Technical Requirements Document)

### ❌ 5. No Open Questions (Pretending Everything Is Clear)
**Symptom**: PRD looks "perfect" with no uncertainties listed
**Why it's a problem**: Nothing in a project is "fully clear"; pretending otherwise = digging a pit
**Fix**: Explicitly list 3-10 questions awaiting decisions

### ❌ 6. MVP Scope > 8 Features
**Symptom**: MVP lists 15 P0 features
**Why it's a problem**: That's not an MVP, it's a complete product. It won't get done.
**Fix**: Cut to 5 or fewer; move the rest to v1.1+

---

## Serious Anti-Patterns (Must Fix)

### ⚠️ 7. All Priorities Are P0
**Symptom**: "Everything is very important"
**Fix**: Use RICE / MoSCoW to force prioritization; no more than 5 P0 items

### ⚠️ 8. User Persona Written as "All Users"
**Symptom**: "Target users: everyone who wants to do XX"
**Fix**: Write a specific persona + anti-persona

### ⚠️ 9. User Stories Missing Who or Why
**Symptom**: "System supports XX management"
**Fix**: Rewrite as "As X user, I want to Y, so that Z"

### ⚠️ 10. No Detailed Feature Descriptions
**Symptom**: Feature list only has names, no inputs/outputs/flow
**Fix**: Add "trigger / input / flow / output / boundary conditions" for each feature

### ⚠️ 11. Missing Non-Functional Requirements
**Symptom**: Not a single word about performance / security / compliance
**Fix**: Write a dedicated §7, covering at minimum performance, availability, and security

### ⚠️ 12. NFRs Buried Inside Feature Paragraphs
**Symptom**: Performance requirements scattered under individual features
**Fix**: Extract them and consolidate into §7

### ⚠️ 13. No Metrics
**Symptom**: "We'll look at feedback after launch"
**Fix**: Define the North Star metric + key AARRR numbers

### ⚠️ 14. Milestones Written Too Rigidly
**Symptom**: Dates precise to the day with no buffer
**Fix**: Leave 20% buffer; explicitly state a risk contingency

---

## General Anti-Patterns (Recommended to Fix)

### 🟡 15. Missing Document Info
**Symptom**: No version number / status / author / change log
**Fix**: Add §1; update version on every major change

### 🟡 16. Version Number Stuck at v0.1
**Symptom**: From inception to launch, always v0.1
**Fix**: MVP launch version = v1.0; major changes = v1.1 / v2.0

### 🟡 17. Status Always Draft
**Symptom**: PRD is live in production but status still says Draft
**Fix**: Change to Approved after review; change to Deprecated when retired

### 🟡 18. No Counter-Metrics
**Symptom**: All metrics are positive indicators
**Fix**: Add counter-metrics to prevent "metric gaming" (e.g., "high retention but low depth-of-use rate")

### 🟡 19. Risks Written Too Abstractly
**Symptom**: "There may be compliance risk"
**Fix**: Be specific about What / Severity / Probability / Mitigation

### 🟡 20. No Dependency List
**Symptom**: Only discovering third-party blockers right before launch
**Fix**: List dependencies + expected ready date + risk level

---

## AI-Era Specific Anti-Patterns

### 🤖 21. PRD Written Too "Loosely" — AI Cannot Consume It
**Symptom**: Content scattered across the document; lacks structured fields
**Fix**: Use the standard 14-chapter structure; key fields in consistent format

### 🤖 22. Acceptance Criteria Not Machine-Verifiable
**Symptom**: "The system should intelligently handle user input"
**Fix**: Given/When/Then format; every item must be writable as an automated test

### 🤖 23. No "Alternatives Considered"
**Symptom**: Only the final solution is written; rejected alternatives not documented
**Fix**: Write the alternatives considered during Brainstorming + reasons they were rejected into the PRD
(This is a core Spec-kit recommendation)

### 🤖 24. Boundary Conditions Incomplete
**Symptom**: Only the happy path is written; no exceptions / edge cases
**Fix**: Each feature must have at least 3-5 boundary conditions

---

## Anti-Pattern Quick Reference Table

| Type | Anti-Pattern | Self-Check Method |
|------|--------|---------|
| Fatal | Missing Why | Go to §2 — does it say "why now"? |
| Fatal | Missing Out-of-Scope | Go to §5 — are there ❌ markers? |
| Fatal | Acceptance criteria too vague | Go to §9 — can an automated test be written? |
| Fatal | Contains tech stack | Search full document for React/Vue/Postgres etc. |
| Fatal | Pretending no OQs | Go to §13 — at least 3 OQs? |
| Fatal | MVP > 8 features | Go to §10 — count the P0s |
| Serious | All P0 | Go to §10 — what's the P0 ratio? |
| Serious | Target is "all users" | Go to §3 — is there an anti-persona? |
| Serious | Stories missing Who/Why | Go to §4 — does every item have "As... so that..."? |
| Serious | Missing detailed descriptions | Go to §6 — is there "trigger/input/output/boundary"? |
| Serious | Missing NFRs | Go to §7 — covers performance/security/compliance? |
| Serious | Missing metrics | Go to §11 — has North Star + AARRR? |
| AI | Missing alternatives record | Is there an "Alternatives Considered" section? |
| AI | Incomplete boundaries | Does every feature have ≥ 3 boundary conditions? |

---

## 5 Hallmarks of a Good PRD (Positive vs. Negative Contrast)

1. ✅ **Clear purpose**: Can describe the product's core value in 3 seconds
2. ✅ **Defined scope**: MVP has no more than 5 P0 items; Out-of-Scope is complete
3. ✅ **Verifiable**: Every feature has Given/When/Then acceptance criteria
4. ✅ **Stays in its lane**: Only writes What/Why, not How
5. ✅ **Honest**: Marks Open Questions / risks / decision log

---

## 3 Things You Must Do After Writing a PRD

1. **Run through the anti-pattern checklist** (this document)
2. **Have someone not on the project read it** — if they can explain the product clearly in 5 minutes, the PRD passes
3. **Archive the current version** (git commit); retain full traceability for subsequent changes

---

**Remember**: A PRD is a contract, not a manual. The core of a contract is "boundaries + acceptance criteria". A PRD without boundaries / without acceptance criteria is no contract at all.
