---
name: implementation-runway-setup-en
description: >-
  Finish the four deterministic preparation items before entering the implementation phase — the include list of files for isolated runs, the external services and credentials inventory, appending an implementation-discipline block to the project constitution, and adding progress and session handoff files to every feature directory. Every operation is idempotent: two runs produce byte-identical output. Trigger keywords: pre-implementation setup / environment preparation / worktree include list / credentials inventory / external service survey / add state session / task management system / discipline block append / configuration before multi-task runs. Do not use for: creating or switching a worktree (that belongs to the implementation executor), writing code, running TDD, producing a feature's spec/plan/tasks, or registering external accounts on the user's behalf. Even when the user does not say "use a Skill", invoke it whenever the task involves "what has to be prepared before implementation starts".
license: MIT
allowed-tools: Read Write Edit Bash
metadata:
  version: "1.0"
  lang: en
  stage: "7"
  standalone: true
  produces:
    - ".worktreeinclude"
    - "docs/external-services.md"
    - ".specify/memory/constitution.md"
    - "specs/00X-*/state.md"
    - "specs/00X-*/session.md"
    - "specs/research/09-runway-setup-report.md"
  requires:
    - name: "specs/00X-*/ feature directories"
      level: orchestration
      fallback: "Ask the user to name the directory; with none, run items A/B only and state explicitly why C/D were not run"
    - name: "Project constitution file"
      level: optional
      fallback: "Skip item C and report 'no constitution file, discipline block not injected'; never create a constitution"
    - name: "Local configuration files"
      level: optional
      fallback: "The include list stays empty and states 'no includable local configuration file was detected'"
    - name: "Isolation mechanism support"
      level: optional
      fallback: "Use an equivalent isolation configuration mechanism; if none is available, skip item A and say so"
---

# Pre-Implementation Environment Setup

## The Four Items

| Item | What it does | Idempotent |
|:---:|---|:---:|
| **A** | Include list of files for isolated runs — list **only files that already exist** | Idempotent |
| **B** | External services and credentials inventory (five columns) | Idempotent |
| **C** | **Append** an implementation-discipline block to the project constitution | WARNING **not idempotent** |
| **D** | Add a progress file and a session handoff file to every feature directory | Idempotent |

All four are deterministic file operations, yet this is **the segment most often skipped**
in the whole chain — because none of it produces "visible progress".
The cost of skipping only shows up during implementation.

## Primary Correctness Requirement: Rerun Safety

Item C is not idempotent. Repeated runs append the same discipline text over and over into the
constitution — polluting the project's most important constraint file.

> **Every write operation MUST sit after the "no" branch of a detection.**
> This is a structural requirement, not a suggestion about execution order.

**Acceptance criterion**: for the same input, two runs produce **byte-identical** output across all
four items, and the discipline block appears in the constitution **exactly once**.

## Flow

```
1. Probe: is the isolation mechanism available? does a constitution exist? which feature dirs exist?
2. A: scan candidate config files -> keep only the ones that exist -> write list -> check ignore rules
3. B: scan feature docs for external service needs -> guided five-column completion -> write inventory
4. C: detect whether the discipline block is already present
      |- present -> skip, report "already in place"
      |- absent  -> locate the version metadata line -> insert before it
5. D: walk feature directories -> add the missing files -> skip the existing ones
6. Report: each item's action, every skip reason, every external service that is not ready — also write to `specs/research/09-runway-setup-report.md` (create; skip if it already exists)
```

## Item A · Include List

**Never create a credential file that does not exist.**

List only files that **really exist** and are **already covered by the ignore rules** — both
conditions, neither optional. An include-list mechanism usually copies a file only when it
"matches a pattern AND is already ignored", so listing a file that is not ignored is a no-op.

Candidates that do not exist are **commented out**, not deleted — they are the hints for the day
they get enabled.

Check at the same time whether the ignore rules cover the sensitive files.
**When they do not, report and ask the user to confirm; MUST NOT edit the ignore rules unilaterally.**

Reference: candidate probing, list-only-what-exists, ignore-rule checks in `references/include-list-rules.md`

## Item B · External Services and Credentials Inventory

Five columns: **config item name / purpose / environment / how to obtain / ready state**.

**The inventory has no "value" column.** Sensitive values go only into a local file covered by the
ignore rules, or into a secret manager.

Guided collection: confirm one item at a time; mark anything uncertain as "to be confirmed" rather
than guessing. Items that are not ready **do not block** this Skill from finishing — label them
honestly and leave the decision to the user.

Reference: the five column definitions, collection phrasing, sensitive-value handling in `references/service-inventory.md`

## Item C · Discipline Block Append

**Detect first, then write.**

| Detection result | Action |
|---|---|
| Present and identical | Skip, report "already in place" |
| **Present but different** | **MUST NOT rewrite automatically**; report the difference and ask the user to rule |
| Absent | Locate the version metadata line, insert **before** it |
| No version metadata line | Append at the end, and **report the position downgrade explicitly** |

The discipline block is **generic implementation discipline**. An external workflow tool is only its
default instance and MUST NOT be hardcoded as the only option — a project may use a different tool,
or none at all.

WARNING **`references/discipline-block.md` is an explanatory document, not the block itself** — the
block lives inside its code fence. The script extracts it from the fence; when the file contains no
fence starting with the marker, it **refuses to inject and reports**, never writing dozens of lines
of meta-commentary into the constitution.

Reference: the discipline text, insertion position rules, idempotence detection algorithm in `references/discipline-block.md`

## Item D · Progress and Handoff Files

Add two files to every feature directory:

| File | Purpose |
|---|---|
| `state.md` (progress file) | Which task is in flight, which are done, whether anything is blocked |
| `session.md` (session handoff file) | Cross-session resumption instructions; **its core job is preventing re-planning** |

**Existing files are skipped, never overwritten.** The user may already have written them by hand.

> The handoff file MUST state "no re-planning": the plan is final, the tasks are locked, execute
> directly. If the plan or tasks turn out to be genuinely wrong, **stop, report, and wait for a
> ruling** — do not rewrite them and carry on; that is silent re-planning.

## What This Skill Does Not Do

- Does not create or switch a worktree / branch (that belongs to the implementation executor)
- Does not write code, does not run TDD
- Does not produce a feature's spec/plan/tasks
- Does not register external accounts on the user's behalf
- **Does not write sensitive values into any file tracked by version control**
- Does not create a constitution file on its own

## Upstream Artifacts

| Artifact | Level | When missing |
|---|:---:|---|
| `specs/00X-*/` feature directories | orchestration | Run A/B only, state explicitly why C/D were not run |
| Project constitution file | optional | Skip C and report it; **never fabricate one** |
| Local configuration files | optional | The list stays empty, with an explanation |
| Isolation mechanism support | optional | Use an equivalent mechanism, or skip A and say so |

## Downstream Consumers

| Consumer | What it reads |
|---|---|
| Implementation executor | Constitution discipline block, progress file, handoff file, include list |
| The user | The external services inventory — to decide whether to go open accounts first |

## Standalone Use

**What you provide**: nothing at all is enough — I probe what the project actually contains first.
If your feature documents are not in the conventional location, just tell me the path.

**What you get**: of the four items, **those the current project conditions allow** are carried
through to completion, with each item's action and each skip reason in the report. The idempotence
guarantee holds in standalone mode too.

**What you don't get**:

- **I will not create your missing prerequisites for you**. With no constitution file the discipline
  block is not injected, and **I will not build you a constitution** — that is a separate job, and it
  needs you to decide the project's principles.
- **I will not open external accounts for you**. The inventory tells you what is missing and where to
  get it; it does not do it for you.
- With no feature directory, item D has nothing to act on; that is reported explicitly rather than
  skipped silently.

## Anti-Patterns

- Creating a credential file that does not exist in order to "complete" the include list
- Listing a file the ignore rules do not cover (the copy mechanism will not fire)
- Writing secret values into the credentials inventory
- Editing the ignore rules unilaterally
- Appending the discipline block without detecting first (a rerun pollutes the constitution)
- Automatically rewriting a discipline block that is present but different
- Overwriting a progress or handoff file the user wrote by hand
- Creating a constitution file when none exists
- Aborting the whole preparation flow because one external service is not ready
