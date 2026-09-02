# Vibe Coding Workflow Integration Guide

> This Skill is not an isolated tool. It plays a specific role within the complete Vibe Coding 9-step process.

---

## 9-Step Process Overview (Vibe Coding Project Development Methodology)

```
┌─────────────────────────────────────────────────────────────┐
│  1. Idea                                                    │
│  2. Research (dual-track: business + technical)             │
│  3. PRD ← ⭐ This Skill is here                             │
│  4. Technical Design (incl. API contract + mock launch)     │
│  5. Frontend Design (design tools + tokens)                 │
│  6. Frontend Development (mock-first + TDD)                 │
│  7. Backend Development (core logic + risk/compliance parallel) │
│  8. Integration (test pyramid + quantitative review + code review) │
│  9. Deployment + monitoring + logging                       │
└─────────────────────────────────────────────────────────────┘

Cross-stage: Spec as living document (CLAUDE.md / Skills / ADR / KB)
```

---

## This Skill's Precise Position

**Inputs**:
- Step 2 research outputs (business / technical / compliance reports)
- Brainstorming Skill outputs (design doc)

**Processing**:
- Reuse confirmed research and brainstorming answers; use Socratic Q&A only for genuine gaps
- Generate PRD following the 14-chapter structure

**Output**:
- Project-level: `<project>/specs/prd.md`
- Single-feature: `<project>/specs/<feature-slug>/prd.md`

**Downstream**:
- Step 4 technical design (producing TRD based on PRD)
- Step 5 frontend design (designing UI based on PRD)

---

## Handoff with Brainstorming Skill

### Workflow
```
[Research reports + ideas] → Brainstorming Skill → design doc → ⭐ PRD-Writer Skill → prd.md
                                ↑                                  ↑
                           diverge + converge              crystallize into formal document
```

### Boundaries
- **What Brainstorming does**: explore alternatives, ask questions, make trade-offs, produce design doc
- **What PRD-Writer does**: crystallize the design doc into the formal 14-chapter structure
- **No overlap**: Brainstorming does not write PRD chapters; PRD-Writer does not diverge

### Recommended Steps
1. Run the Brainstorming Skill first to converge on the design
2. Have Claude save the Brainstorming output as `brainstorming-design.md`
3. Then launch this Skill: "Generate a standard PRD based on brainstorming-design.md"
4. This Skill reads the design doc, skips answered questions, and fills only blocking gaps → produces prd.md

---

## Compatibility with GitHub Spec-Kit

Spec-Kit workflow:
```
/speckit.constitution → /speckit.specify → /speckit.plan → /speckit.tasks → /speckit.implement
                              ↑
                              ↑ This Skill is equivalent to /specify
```

### Compatibility
This Skill's prd.md output **can be used directly as spec.md**:
- Chapter structure is compatible
- Acceptance criteria written in Given/When/Then
- Includes Out-of-Scope / Open Questions
- Contains no technical details

### Differences
| Dimension | Spec-Kit /specify | This Skill |
|------|:------:|:------:|
| Language | Primarily English | **English-first** |
| Workflow | Command-driven | Conversational + chapter template |
| Teaching style | Leans toward automation | **Socratic Q&A guided** |
| Output | Slim spec.md | Full 14-chapter PRD |

---

## Compatibility with OpenSpec

OpenSpec flow:
```
/opsx:propose → /opsx:design → /opsx:verify → /opsx:apply
                   ↑
                   This Skill's output can serve as the propose-stage artifact
```

### Integration Method
- This Skill produces prd.md
- Use OpenSpec to wrap prd.md into a proposal
- OpenSpec automatically tracks PRD changes (Delta Spec)

---

## Handoff with Superpowers Brainstorming

Superpowers' official 7 steps:
```
1. Brainstorming           ← upstream
2. Using-git-worktrees
3. Writing-plans
4. Subagent-driven-development
5. TDD
6. Code Review
7. Finishing-branch
```

This Skill inserts between 1 → 2:
```
1. Brainstorming → ⭐ PRD-Writer Skill → 2. git-worktrees → 3. Writing-plans → ...
                       ↑
                       Crystallizes design doc into formal PRD
```

---

## File Organization Recommendations

### Standard Project Structure
```
<project-root>/
├── CLAUDE.md                        # Project constitution (if applicable)
├── knowledge-base/                  # Step 2 research outputs
│   ├── business-research/
│   ├── technical-research/
│   └── compliance-research/
├── specs/                           # PRD output directory
│   ├── 0001-core-feature-a/
│   │   ├── prd.md                   ← ⭐ This Skill's output
│   │   ├── plan.md                  ← Step 4 output (not this skill's responsibility)
│   │   ├── tasks.md
│   │   └── README.md
│   └── 0002-core-feature-b/
├── docs/
│   ├── adr/                         # Architecture Decision Records
│   └── domain/                      # Domain model
└── ...
```

### Naming Rules
- PRD directory: `<4-digit-index>-<kebab-case-feature-slug>/`
- PRD file: always named `prd.md`
- Index is auto-incremented: 0001, 0002, ...

---

## Index Management for Multi-PRD Projects

When a project has multiple PRDs, maintain an index at `specs/README.md`:

```markdown
# Specs Index

| Index | Topic | Status | Priority | Document |
|---|---|:---:|:---:|---|
| 0001 | <Core Feature A> | Approved | P0 | [prd.md](0001-core-feature-a/prd.md) |
| 0002 | <Core Feature B> | Draft | P0 | [prd.md](0002-core-feature-b/prd.md) |
| 0003 | <Supporting Feature C> | Draft | P0 | [prd.md](0003-supporting-feature-c/prd.md) |
| 0004 | <Supporting Feature D> | Backlog | P1 | [prd.md](0004-supporting-feature-d/prd.md) |
```

Each PRD status can be: Draft / Review / Approved / Implemented / Deprecated

---

## Cross-Stage: Spec as a Living Document

This Skill's PRD output is **not a one-time artifact** — it evolves with the project:

### When the PRD Needs Updating
- Acceptance criteria are modified by newly discovered requirements
- Out-of-Scope items are added or removed
- Risk assessment is updated
- Metrics are recalibrated based on post-launch data

### Update Mechanism
1. Changing the PRD requires updating the version number (v1.0 → v1.1)
2. The change log must describe the reason for the change
3. Major changes (V → V+1) require a new review cycle
4. All changes are tracked via git

---

## Compatibility with Cursor / Codex

PRD output is standard Markdown; all AI coding tools can consume it:

| Tool | Compatibility | Usage |
|------|:------:|------|
| Claude Code | ✅ Native | Auto-loaded |
| Cursor | ✅ Markdown | @file reference |
| Codex (VS Code) | ✅ Markdown | Select as context |
| Gemini Code Assist | ✅ Markdown | Same as above |

---

## Team Collaboration Modes

### Solo Project (1 person + AI)
- Run the Skill yourself → review yourself
- Slim PRD version (9 chapters is enough)

### Small Team (2-5 people)
- PM runs the Skill → team reviews → Approved
- Medium PRD version (12 chapters)

### Medium/Large Team (>5 people)
- PM runs the Skill → multiple review rounds → Approved
- Full PRD version (14 chapters)
- Use OpenSpec for change management

---

## Common Integration Scenarios

### Scenario 1: Brand New Project From Scratch
1. Idea + MVP scope trimming
2. Research (dual-track)
3. Brainstorming (explore solutions)
4. **PRD-Writer** (crystallize the document) ⭐
5. Technical design / Figma / development ...

### Scenario 2: Adding a New Feature to an Existing Project
1. Write a mini PRD for the new feature (slim 9-chapter version)
2. Reference the existing project constitution
3. Include compatibility notes with existing PRDs

### Scenario 3: Refactoring / Redesign
1. Write a "refactoring PRD"
2. Clearly state "why refactor" + "what to keep + what to change"
3. Add a Migration Plan chapter

---

## Anti-Integration Patterns (Do Not Use This Way)

- ❌ Skipping Brainstorming and going straight to this Skill (PRD will lack depth)
- ❌ Using this Skill before doing research (PRD will be distorted)
- ❌ Using this Skill to write a technical design (boundary confusion)
- ❌ One PRD covering 10 unrelated features (split them up)
