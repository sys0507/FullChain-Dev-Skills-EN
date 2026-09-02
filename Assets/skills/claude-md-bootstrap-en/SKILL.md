---
name: claude-md-bootstrap-en
description: Generate or refresh a project-root CLAUDE.md from existing PRD, architecture decisions, constitution, design docs, project manifests, and feature specs. Produces a concise WHAT/WHY/HOW routing map with verified commands and dependencies, @path references, anti-patterns, and Karpathy's four coding principles. Use when Claude Code needs durable project context. Do not use for empty projects without documentation or for non-Claude agent context files.
license: MIT
metadata:
  version: "1.0"
  lang: en
  stage: "6"
  standalone: true
  produces:
    - "CLAUDE.md"
  requires:
    - name: "At least one kind of project material (PRD / architecture doc / specs / README)"
      level: required
    - name: "Project constitution file"
      level: optional
      fallback: "Skip the constitution-reference section and label the omission in the output"
    - name: "DESIGN.md and the design reference directory"
      level: optional
      fallback: "Label the visual section 'not applicable' with the reason; MUST NOT fabricate it"
    - name: "Project manifest files"
      level: optional
      fallback: "Handle the tech-stack and commands sections with the placeholder strategy; **MUST NOT invent version numbers**"
---

# CLAUDE.md Project Context Bootstrap (English)

## Language convention

- This Skill is the English execution version: user interaction, check reports, Open
  Questions, and project descriptions generated from English upstream material default
  to English.
- Code, commands, dependency names, file paths, APIs, framework names, and the
  project's existing identifiers stay verbatim.
- Karpathy's four principles must be kept as the verbatim English original from
  `references/karpathy-guidelines.md`. This is a content-integrity requirement.
- Chinese workflows call `claude-md-bootstrap`. The Chinese and English versions must
  not be mixed within one workflow.

## Goal

Generate a project-root `CLAUDE.md` from the project's existing material. It should be a
**routing map + behavioral contract**, not another copy of the PRD, constitution,
architecture doc, and DESIGN.md.

The final file must answer:

1. What the project is and why it exists (WHAT / WHY).
2. Where the detailed material lives (`@path`).
3. What actions the Agent takes when starting and finishing a task.
4. What the real runnable commands and real dependencies are.
5. Which behaviors are explicitly forbidden.

## When not to use

- A brand-new empty project with no PRD, README, spec, or architecture material: write
  the project documentation first.
- An existing, well-maintained `CLAUDE.md` under 200 lines: update only the relevant
  sections, do not regenerate.
- The current tool is not Claude Code: create that tool's equivalent project-level
  context file instead; this Skill does not apply directly.
- A backend-only project with no visual material: skip the visual sections, do not
  fabricate them.

## Prerequisites

Confirm before starting:

| Requirement | Purpose |
|---|---|
| Project root is identified | `CLAUDE.md` must sit at the real project root |
| A project manifest exists | `package.json`, `pyproject.toml`, `Cargo.toml`, `pom.xml`, etc. |
| At least one kind of project material | PRD, architecture doc, specs, or README |

Optional but recommended to read:

- `.specify/memory/constitution.md`
- `DESIGN.md`
- `design-reference/`
- An existing `CLAUDE.md`

If a requirement is missing, pause and explain it to the user. Do not guess.

## Four-step workflow

```text
Step 1: Source inventory     → confirm which input files really exist
Step 2: Section mapping      → map sources to CLAUDE.md sections
Step 3: Generate from source → extract and reference, never fabricate
Step 4: Verify and finalize  → check line count, paths, commands, deps, traceability
```

### Step 1: Source inventory

Read when present:

| File | What to extract |
|---|---|
| `specs/prd.md`, `PRD.md`, or `docs/prd.md` | WHAT and WHY |
| Architecture / tech-selection decision doc | Tech-stack intent, rationale, constraints |
| `.specify/memory/constitution.md` | Reference the principles only, do not copy in full |
| `DESIGN.md` | Confirm the visual system and reference it via `@path` |
| `design-reference/` | Add key files to the navigation table |
| Project manifest / lockfile | Real scripts, dependencies, versions |
| `README.md` | Existing project description |
| `specs/00X-*/` | Feature structure and task-label conventions |

Report item by item: what was found, what can be extracted from it, what does not exist.
If source coverage needs user confirmation, pause before entering Step 2.

### Step 2: Section mapping

Read `references/template.md` when you need the exact structure. Build the mapping for
the current project:

| CLAUDE.md section | Primary source | How it is included |
|---|---|---|
| 1. Project WHAT | PRD overview | Extract one paragraph |
| 2. Project WHY | PRD business goals / problem | Extract one paragraph |
| 3. Workflow HOW | constitution, rule files, task labels, workflow docs | Synthesize into action rules |
| 4. Tech Stack | Project manifest and architecture decision | Extract real versions / intent |
| 5. Commands | Project manifest scripts | Extract verbatim |
| 6. Constitution | `.specify/memory/constitution.md` | `@path` reference |
| 7. Visual System | DESIGN.md, design-reference | `@path` reference |
| 8. Anti-Patterns | Prohibitions in constitution, DESIGN.md | 6–8 items, each with its source |
| 9. Behavioral Guidelines | `references/karpathy-guidelines.md` | Verbatim English |
| 10. File Navigation | Key files confirmed to exist | Navigation table |

Any section whose source is unclear or missing must be marked as an Open Question. Do
not fill it in with plausible-sounding content.

### Step 3: Generate from sources

Execution rules:

- Copy the manifest's scripts verbatim, and verify each command really exists.
- Extract the tech stack from real dependencies and versions; the architecture decision
  only supplies rationale and constraints.
- Reference long content from constitution, PRD, architecture docs, and DESIGN.md via
  `@path`. Do not copy it in full.
- Every Anti-Pattern must be traceable to a specific source.
- File navigation lists only paths that really exist and have been verified.
- §3 Workflow must face future tasks — write "how to start, execute, test, and finish
  now", not a history log like "research done → PRD done → spec done".
- "YOU MUST" and "IMPORTANT" may appear at most 2 times in the whole file, reserved for
  genuinely critical rules.
- Total length must be under 200 lines.

For a greenfield project with no manifest yet:

- §4 writes "tech-stack intent: see `@<real path to architecture decision doc>`; after
  project initialization, `/init` syncs dependency versions from the real manifest".
- §5 writes "pending project initialization; `/init` will extract from the real scripts".
- Do not invent dependency names, versions, or commands ahead of time. If the user wants
  them settled immediately, have them complete project initialization first.

Language rule: project descriptions follow the English upstream material and stay in
English; frameworks, dependencies, commands, and Karpathy's principles keep their
original form. Do not switch the whole `CLAUDE.md` to another language just because a
referenced source document is in one.

### Step 4: Verify and finalize

Check item by item:

```text
□ CLAUDE.md is under 200 lines
□ Every @path resolves to a real file
□ Every command exists in the real project manifest
□ Every dependency and version matches the manifest
□ Every Anti-Pattern traces back to a source paragraph
□ YOU MUST / IMPORTANT total no more than 2 occurrences
□ Karpathy's four principles keep the verbatim English original
□ File navigation contains no non-existent paths
□ English project descriptions were not accidentally rewritten into another language
  by non-English reference material
```

The final report is written in English and contains:

- Total line count and token estimate.
- The source mapping for every section.
- `@path` completeness results.
- Command and dependency verification results.
- Missing items and Open Questions.

Never overwrite an existing `CLAUDE.md` directly: preserve user-authored sections, show
a diff first, and merge only after confirmation.

## Definition of done

1. A `CLAUDE.md` under 200 lines exists at the project root.
2. Detailed material is referenced via `@path`, with no upstream content pasted in full.
3. Tech stack, commands, and versions match the real project files.
4. Karpathy's four principles keep the verbatim English original.
5. Anti-Patterns have explicit sources and nothing is fabricated.
6. Descriptive content and the completion report for an English project are in English.

## Reference files

- `references/template.md`: the 10-section structure, positive/negative examples, and
  placeholder strategy.
- `references/karpathy-guidelines.md`: the verbatim English text of Karpathy's four
  principles and its usage boundaries.

Read the corresponding file only when you need the exact section structure or need to
embed the Karpathy text.

## First response

Explain in English first: we will not copy the PRD into `CLAUDE.md`; we will produce a
routing map under 200 lines that traces back to real files. Then run the source
inventory, pausing at source-coverage confirmation and at section-mapping confirmation.
Before the final write, show a diff against any existing file.

## Upstream Artifacts

| Artifact | Level | When missing |
|---|:---:|---|
| At least one kind of project material | **required** | Stop — an empty project has nothing to extract from |
| Project constitution file | optional | Skip the reference section and label the omission |
| `DESIGN.md` and the design reference directory | optional | Label the visual section as not applicable |
| Project manifest files | optional | Tech stack / commands follow the placeholder strategy; no invented versions |

## Downstream Consumers

| Consumer | What it takes from this skill |
|---|---|
| Every agent during implementation | `CLAUDE.md` as the project context routing map |

## Standalone Use

**What you provide**: any one kind of material the project already has: a PRD, an architecture doc, specs, or a README.

**What you get**: a routing map under 200 lines covering WHAT/WHY/workflow/anti-patterns/behavioral guidelines and a key-file navigation table.

**What you don't get**:

- **It will not work on an empty project** — with no project material at all it recommends writing documentation first rather than generating empty phrases.
- **It does not copy upstream text in full**, it only makes @path references.
- With no project manifest, the tech-stack and commands sections state honestly that there is currently no manifest, and **MUST NOT invent dependency versions**.

**Gate**: when a `CLAUDE.md` already exists, show the diff and wait for confirmation; pause once at source-coverage confirmation and once at section-mapping confirmation.

⚠️ **Write-conflict ruling**: this Skill is the only writer of `CLAUDE.md`.
When the learnings-retrospective Skill needs a reference to the learnings file injected, it **only raises a signal; this Skill performs the injection** (PRD §3.3, option B).
