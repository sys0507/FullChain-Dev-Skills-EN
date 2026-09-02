# Ready-to-Copy Prompts

Copy-paste prompts for each of the 4 steps.
Adapt the placeholders (in `<angle brackets>`) to your project.

---

## Step 1 · Material Placement (Stitch source example)

```
Help me organize the Stitch download artifacts into my current project,
following these rules:

Source directory: <absolute path to your Stitch download>
Target: current project root

Tasks:
1. Copy <design-system-name>/DESIGN.md from source to project root
   (this becomes the project's frontend design constitution)
2. Create design-reference/stitch-export/ at project root
3. Copy all _1 ~ _N page directories from source into
   design-reference/stitch-export/, renaming each to a semantic name based on
   the <title> tag in its code.html
   (example: _3 has title "Shopping Cart" → rename to cart-en; _5 has title "购物车" → rename to cart-zh)
4. Do NOT copy prd.md from source — project already has specs/prd.md.
   If contents differ, stop and ask me
5. App shell directory (if present) → design-reference/stitch-export/_app-shell/
6. Skip .DS_Store and system files

Output after completion:
- Project tree (depth 3)
- ls -la verifying DESIGN.md is at root
- File listing per design-reference/stitch-export/<page>/
- Rename mapping table (original number → semantic name)

Constraints:
- Use the platform-native non-destructive copy operation, never move sources; resolve and verify source and destination paths before recursive copies
- If DESIGN.md or design-reference/ already exists at project root, stop and ask
```

---

## Step 2 · Constitution Injection

```
/speckit.constitution

I've placed design artifacts in this project:
- DESIGN.md at project root
- Visual reference samples in design-reference/<source>-export/

Update .specify/memory/constitution.md by appending a "Frontend Design System"
section, based on these materials.

Step 1: Read these files to understand the design context
- DESIGN.md (the full design system)
- specs/prd.md (business context, target users, market conventions)
- 2-3 sample pages from design-reference/<source>-export/ (visual style)

Step 2: Extract "non-negotiable design principles" — direction, not values
Format each principle as: Name → Why it's non-negotiable → Source-of-truth file

Step 3: Constitution holds direction, DESIGN.md holds values
✅ Write: "Visual specs come from root DESIGN.md, all colors/fonts/spacing
   must use its tokens"
❌ Do NOT write: specific hex values, token names, font names, or component names

Required directions to cover (extract from the materials, don't ask me to fill):
1. Single source of truth for visual specs
2. How to reference visual prototype samples
3. Target market / user conventions that cannot be compromised
   (from prd.md; if unclear, Open Question)
4. Component library baseline (infer from DESIGN.md; if unclear, Open Question)
5. Information density / design philosophy (from DESIGN.md design principles)
6. Multi-language strategy (only if multiple shown in design-reference)
7. Theme mode — exactly what DESIGN.md says, no more

Hard constraints:
- Do NOT copy hex values, token names, font names, or component names
- Do NOT make decisions for me — anything unclear goes under
  "Open Questions" at the end
- After writing, report: (a) files changed (b) source paragraphs for each principle
```

---

## Step 3 · Impact Identification

```
Scan all feature directories under specs/. For each, classify whether its
plan.md or tasks.md involves frontend UI (React/Vue components, pages, forms,
tables, charts, dashboards) versus pure backend/algorithm/scheduling/DB work.

Output table:
| Feature dir | Has FE? | Needs re-run? | Best matching design-reference/ page |

Criteria:
- Has FE = true → needs /plan + /tasks re-run
- Has FE = false → no action

Do NOT decide for me. After the table, STOP and wait for my confirmation.
```

---

## Step 4 · Selective Re-run (per feature)

```
For specs/<NNN>-<feature-name>/, re-run plan + tasks ONLY.
Do NOT touch spec.md or any clarify outputs — business requirements unchanged.

/speckit.plan
- Read root DESIGN.md and design-reference/<source>-export/<matched-page>/ first
- Add a "Frontend section" to plan.md listing:
  (a) Components used (per DESIGN.md §Components)
  (b) Which DESIGN.md section each component maps to
  (c) Visual reference sample path
- Preserve all existing backend / integration / data flow / dependencies / risks

/speckit.tasks
- Follow the project's existing task labels; only default to [FE] / [BE] / [INT] when no label system exists
- [FE] tasks must cite:
  (a) DESIGN.md section
  (b) Reference HTML/image sample path
  (c) shadcn (or equivalent) component used
- Preserve backend/core tasks; use [BE] for them and [FE] for interface tasks only under the default vocabulary
- Re-evaluate parallel groups from the actual dependency graph; do not assume frontend and backend are always parallelizable

After this feature, STOP and let me review before the next.
```
