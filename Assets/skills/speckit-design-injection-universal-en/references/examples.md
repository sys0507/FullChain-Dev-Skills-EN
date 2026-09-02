# Worked Example: Team Task Tracker with Design System

A complete walkthrough using a React-based team task tracker project
that has already completed Spec-Kit's pipeline and now needs design system injection.

## The starting state

The user had a project `~/projects/taskflow/` with:

```
taskflow/
├── specs/
│   ├── prd.md                     (12-chapter PRD, Team Task Manager)
│   ├── 001-auth/                  (User authentication)
│   │   ├── spec.md, clarify.md, plan.md, tasks.md
│   ├── 002-project-board/         (Kanban/board view)
│   │   └── ... 4 files
│   ├── 003-task-detail/           (Task detail panel)
│   │   └── ... 4 files
│   ├── 004-team-members/          (Team & permissions)
│   │   └── ... 4 files
│   ├── 005-notifications/         (In-app & email notifications)
│   │   └── ... 4 files
│   ├── 006-search/                (Search & filters)
│   │   └── ... 4 files
│   ├── 007-reports/               (Reports & analytics dashboard)
│   │   └── ... 4 files
│   └── 008-settings/              (Settings & integrations)
│       └── ... 4 files
└── .specify/
    └── memory/
        └── constitution.md
```

The user then ran their PRD through Google Stitch and downloaded:

```
stitch_taskflow_design/
├── prd.md                                           (returned)
├── clean_minimal_productivity_system/
│   └── DESIGN.md                                    (the design system)
├── taskflow_app_shell/
│   └── code.html                                    (app shell)
└── _1/ _2/ ... _8/                                  (8 pages)
```

## Step 1 in action

The agent read each `_N/code.html`'s `<title>` tag to map numbers → semantic names:

```
_1  title="TaskFlow - Dashboard"          → dashboard
_2  title="TaskFlow | Project Board"      → project-board
_3  title="TaskFlow | Task Detail"        → task-detail
_4  title="TaskFlow - Team Members"       → team-members
_5  title="TaskFlow | Notifications"      → notifications
_6  title="TaskFlow - Search & Filter"    → search-filter
_7  title="TaskFlow | Reports"            → reports
_8  title="TaskFlow - Settings"           → settings
```

The agent then used the platform-native non-destructive copy operation to:

1. Copy `clean_minimal_productivity_system/DESIGN.md` to the project root.
2. Create `design-reference/stitch-export/`.
3. Copy each page directory into its semantic destination (`dashboard`,
   `project-board`, and so on).
4. Copy the app shell to `_app-shell/`.

Before recursive copies, it resolved and verified the exact source and
destination paths. The source export remained intact.

The agent verified that `specs/prd.md` already existed, compared first 200 chars
to the returned `prd.md`, confirmed they matched, and did not copy.

Result structure after Step 1:

```
taskflow/
├── DESIGN.md                              ← copied from stitch
├── design-reference/
│   └── stitch-export/
│       ├── _app-shell/
│       │   └── code.html
│       ├── dashboard/
│       │   ├── code.html
│       │   └── screen.png
│       ├── project-board/
│       │   ├── code.html
│       │   └── screen.png
│       ├── task-detail/
│       │   ├── code.html
│       │   └── screen.png
│       ├── team-members/
│       │   ├── code.html
│       │   └── screen.png
│       ├── notifications/
│       │   ├── code.html
│       │   └── screen.png
│       ├── search-filter/
│       │   ├── code.html
│       │   └── screen.png
│       ├── reports/
│       │   ├── code.html
│       │   └── screen.png
│       └── settings/
│           ├── code.html
│           └── screen.png
└── .specify/
    └── memory/
        └── constitution.md
```

## Step 2 in action

The agent ran `/speckit.constitution` with the trigger prompt from `references/prompts.md`.

It read DESIGN.md, specs/prd.md, and 2-3 sample pages (dashboard, project-board,
reports). It then proposed this addition to `.specify/memory/constitution.md`:

```markdown
## Frontend Design System

### Principle 1: Single Source of Truth for Visual Specs
DESIGN.md at project root is the authoritative source.
No colors, typography, or spacing values may be hard-coded in components —
all must reference tokens defined in DESIGN.md.
Why: Constitution holds direction across design iterations; DESIGN.md holds
the current values that will evolve. Conflating them makes the system unable
to absorb design changes.
Source of truth: `<project-root>/DESIGN.md`

### Principle 2: Visual Reference Samples
When implementing any UI-touching feature, read the corresponding page in
design-reference/stitch-export/<page-name>/ first. The HTML prototype is
the visual contract — match it closely.
Why: Token-level DESIGN.md leaves layout ambiguous; reference HTML anchors
the visual intent. Without it, AI agents drift toward generic dashboards.
Source of truth: `<project-root>/design-reference/stitch-export/`

### Principle 3: Target User Conventions
Product targets knowledge workers using browsers primarily on desktop (1280px+).
Mobile is secondary — responsive but not mobile-first. Keyboard shortcuts are
expected (power users).
Why: PRD §2.3 user profile explicitly lists "productivity-focused desktop users"
as the primary audience. Designing mobile-first would compromise information
density and keyboard workflow.
Source of truth: PRD §2.3 + DESIGN.md §Layout Principles

### Principle 4: Component Library Baseline
Components derive from the shadcn/ui library (as identified from DESIGN.md §Components).
Any new component must first check if a shadcn primitive exists before custom implementation.
Why: Consistency at the component level reduces visual drift and implementation time.
Source of truth: DESIGN.md §Components

### Principle 5: Information Density
Clean, minimal aesthetic with generous whitespace. Data-dense tables (reports page)
are acceptable exceptions — refer to design-reference/stitch-export/reports/ for
the dense-data pattern.
Why: DESIGN.md §Design Philosophy states "clarity over decoration". The reports
page is explicitly called out as the exception in DESIGN.md §Data Tables.
Source of truth: DESIGN.md §Design Philosophy + §Data Tables

### Principle 6: Color Modes
DESIGN.md specifies both light and dark mode tokens. All components must support
both modes via CSS custom properties, never hard-coded colors.
Why: prd.md §6.2 lists dark mode as a Must-have requirement.
Source of truth: DESIGN.md §Colors

Open Questions:
- [ ] Right-to-left (RTL) language support? prd.md doesn't specify. Assume no for v1.
- [ ] Accessibility floor: WCAG level not stated in prd.md or DESIGN.md. Set a
      baseline (e.g., WCAG 2.1 AA) or explicitly opt out?
```

**What the agent flagged as a common failure mode avoided**: The AI initially tried
to copy the primary color hex value (#3B82F6) into constitution. The user rejected
this and asked the AI to rewrite — the constitution now only says "all colors must
use tokens from DESIGN.md", not the values themselves.

The agent asked the user to answer the Open Questions before proceeding.

User answered: "No RTL for v1. WCAG AA baseline." Agent incorporated answers,
finalized constitution.

## Step 3 in action

The agent scanned all 8 feature directories and produced:

| Feature dir | Has FE? | Needs re-run? | Best matching page |
|-------------|:-------:|:-------------:|-------------------|
| 001-auth | Yes (login/register forms) | ✅ Yes | (no dedicated page — use dashboard layout as reference) |
| 002-project-board | Yes (main UI) | ✅ Yes | project-board |
| 003-task-detail | Yes (detail panel) | ✅ Yes | task-detail |
| 004-team-members | Yes (list + forms) | ✅ Yes | team-members |
| 005-notifications | Yes (notification UI) | ✅ Yes | notifications |
| 006-search | Yes (search UI) | ✅ Yes | search-filter |
| 007-reports | Yes (charts + tables) | ✅ Yes | reports |
| 008-settings | Yes (forms) | ✅ Yes | settings |

**Note**: In this project, all 8 features touch the frontend. This is typical for
a UI-heavy product. In a project with backend services (data ingestion, batch jobs,
worker queues), those would show "Has FE = No" and be skipped.

The user confirmed the re-run list and the agent proceeded to Step 4.

## Step 4 in action

The agent re-ran plan + tasks for `002-project-board` first (most critical feature,
confirmed by user). The original `plan.md` had a frontend section that said:

```
Frontend:
- Implement Kanban board with React
- Support drag-and-drop between columns
- Show task card with title, assignee, priority badge
```

After re-run with design injection, the same section became:

```
## Frontend Section (added post-design-injection)

### Visual Reference
design-reference/stitch-export/project-board/code.html

### Components Used
1. KanbanBoard
   - DESIGN.md §Board Layout
   - shadcn/ui: custom layout (no direct primitive — use Card as column wrapper)
   - Visual reference: project-board/code.html (outer grid structure)

2. TaskCard
   - DESIGN.md §Task Cards
   - shadcn/ui: Card + Badge + Avatar
   - Visual reference: project-board/code.html (individual card elements)

3. ColumnHeader
   - DESIGN.md §Column Headers
   - shadcn/ui: Button variants for "add task" action
   - Visual reference: project-board/code.html (column header row)

4. PriorityBadge
   - DESIGN.md §Status & Priority Indicators
   - shadcn/ui: Badge (variant maps to priority level)
   - Visual reference: project-board/code.html (badge colors per column)

### DESIGN.md Sections Referenced
- §Color Tokens → status colors for task priority (critical/high/medium/low)
- §Typography → card title, metadata label styles
- §Spacing → card gap, column padding, board horizontal scroll
```

The original backend section (REST API contracts, DB schema, data flow) was
preserved verbatim. Only the frontend section was rewritten.

Similarly `/speckit.tasks` was re-run. The original 12 tasks became 17 tasks
with proper tags:

```
[BE] T01 — GET /api/projects/:id/tasks (preserved from original)
[BE] T02 — POST /api/tasks (preserved)
[BE] T03 — PATCH /api/tasks/:id/status (preserved)
[BE] T04 — POST /api/projects/:id/tasks/reorder (preserved)
[FE] T05 — Implement KanbanBoard layout component
           Read: design-reference/stitch-export/project-board/code.html
           Reference: DESIGN.md §Board Layout
           Component: shadcn Card as column wrapper
[FE] T06 — Implement TaskCard component
           Read: design-reference/stitch-export/project-board/code.html
           Reference: DESIGN.md §Task Cards
           Component: shadcn Card + Badge + Avatar
[FE] T07 — Implement PriorityBadge component
           Reference: DESIGN.md §Status & Priority Indicators
           Component: shadcn Badge (4 priority variants)
[FE] T08 — Implement drag-and-drop between columns
           Reference: DESIGN.md §Interaction Patterns (drag feedback states)
[FE] T09 — Implement dark/light mode support for board
           Reference: DESIGN.md §Colors (CSS custom properties)
[INT] T10 — Wire KanbanBoard to GET /api/projects/:id/tasks
[INT] T11 — Wire drag-and-drop to POST /api/projects/:id/tasks/reorder
            Optimistic update pattern
[INT] T12 — Wire TaskCard status change to PATCH /api/tasks/:id/status
... (remaining integration tasks)
```

The agent stopped after `002-project-board` and asked the user to review before
proceeding to `003-task-detail`. User reviewed, confirmed, agent continued through
all 8 features over the next ~35 minutes.

## What success looks like (end state)

After all 8 features are re-run:

1. `DESIGN.md` at project root — single visual spec source
2. `design-reference/stitch-export/` with 8 semantically named page directories
3. `.specify/memory/constitution.md` has abstract "Frontend Design System" section
   (6 principles + WCAG AA added from Open Question answer)
4. All 8 features have updated plan.md + tasks.md with [FE]/[BE]/[INT] tags
5. `/speckit.implement` can now generate code that matches the Stitch visual design

## Time estimate for this example

| Step | Time |
|------|:----:|
| Step 1 (material placement) | ~10 min |
| Step 2 (constitution injection) | ~15 min |
| Step 3 (impact identification) | ~5 min |
| Step 4 (8 features × ~5 min each) | ~40 min |
| **Total** | **~70 min** |

This confirms the "30-60 minutes" estimate in SKILL.md — slightly over for a large
project with 8 UI features. A smaller project (3-4 features) would be 30-40 min.

## Contrast with a mixed-domain project

To illustrate that this workflow is domain-agnostic, here is a compressed summary
of what Step 3 looks like for a SaaS analytics backend that has both UI and
non-UI features:

```
analytics-platform/
├── specs/
│   ├── 001-data-pipeline/     (ETL jobs, no UI)
│   ├── 002-event-ingestion/   (Kafka consumers, no UI)
│   ├── 003-dashboard/         (chart UI, definitely FE)
│   ├── 004-alert-rules/       (rule engine, no UI)
│   ├── 005-alert-notifications/ (email + Slack, no UI)
│   └── 006-user-settings/     (settings page, FE)
```

Step 3 output for this project:

| Feature dir | Has FE? | Needs re-run? | Matching page |
|-------------|:-------:|:-------------:|--------------|
| 001-data-pipeline | ❌ | No | (pure ETL) |
| 002-event-ingestion | ❌ | No | (pure backend) |
| 003-dashboard | ✅ | Yes | dashboard |
| 004-alert-rules | ❌ | No | (rule engine only) |
| 005-alert-notifications | ❌ | No | (push channel adapter) |
| 006-user-settings | ✅ | Yes | settings |

Net: only 2 of 6 features need re-run. This is the typical ratio for a
data-heavy SaaS: significant backend work that is completely unaffected by
design injection, and a small set of UI surfaces that get the full treatment.

## Key insight to communicate

**constitution.md is the long-lived contract, DESIGN.md is the current visual
snapshot.** The reason this skill exists is that Spec-Kit's natural flow assumes
you have the design first, but real projects often produce design after engineering.
This skill bridges that inversion cleanly — regardless of whether the project is
a task tracker, an analytics platform, an e-commerce site, or any other domain.
