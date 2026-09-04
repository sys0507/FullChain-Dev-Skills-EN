---
name: fullchain-toolchain-setup-en
description: >-
  Install and verify, in one pass, every skill the later stages will call - project-scoped,
  with hard language isolation - and then selectively configure six optional capabilities as
  the project needs them. Idempotent: an existing skill with identical content is skipped, and
  one with different content is reported for a human ruling rather than overwritten. The
  language parameter MUST be passed explicitly and is never inferred from the environment.
  Trigger keywords: install skills / set up the toolchain / stage 0 / project initialisation /
  configure the environment / which skills do I need / install the assets.
  Do not use for: generating the project context file (that is claude-md-bootstrap-en),
  modifying global configuration or another project, registering external accounts on the
  user's behalf, or pre-installing conditional capabilities the project does not need.
  Invoke it whenever the task involves getting this project's skills in place, even if the
  user never says the word "skill".
license: MIT
allowed-tools: Read Write Edit Bash
metadata:
  version: "1.0"
  lang: en
  stage: "0"
  standalone: true
  produces:
    - ".claude/skills/<name>/"
    - "specs/research/toolchain-setup-report.md"
  requires:
    - name: "language parameter"
      level: required
    - name: "skill asset source directory"
      level: required
    - name: "documentation for the optional capabilities"
      level: optional
      fallback: "Mark that capability pending; do not install from impression"
---

# Full-chain Toolchain Setup (Stage 0)

## Two halves

| Half | Content |
|:-:|---|
| **The first** | Install and verify, in one pass, every skill the later stages will call (**project-scoped**), producing an install report |
| **The second** | Selectively configure six optional capabilities as the project needs, one of which gives the research stage a second independent source |

## Why it has to be built in

The open-source skill collections this draws on are distributed by an external command-line
installer; **this project has no equivalent toolchain**. Without this skill, a user has to
copy a dozen directories by hand and verify each one — which is exactly the step that puts
people off at the very start of the chain.

## Two red lines

### 1. Hard language isolation

A Chinese workflow **installs only the Chinese versions**; an English workflow installs only
the `-en` versions.

| Situation | Correct behaviour |
|---|---|
| The Chinese version is missing | **Report the failure and its impact.** The English version MUST NOT be installed in its place |
| The directory name matches but `metadata.lang` does not | **Refuse to install** and report the mismatch |
| The `lang` field cannot be read | **Refuse** — better not installed than mixed |
| No language parameter was passed | **Stop and ask.** MUST NOT be inferred from the environment or the locale |

> Mixing produces the kind of pollution that is very hard to attribute — English artifacts
> appearing inside a Chinese project — and once the two versions drift apart over time, the
> result of mixing them is unpredictable.

**The catalogues are two independent tables; names are never derived by concatenation.** The
existing naming suffixes are inconsistent (the first four carry `-universal`), so
concatenation produces the wrong name for those four.

See `references/skill-catalog.md` for both catalogues.

### 2. Idempotence

| Detection result | Action |
|---|---|
| The target does not exist | Install |
| Present with identical content | **Skip**, reporting "already present" |
| **Present with different content** | **Report the difference for a ruling** — do not overwrite and do not skip silently |

Comparison uses a **content digest**, not a version number — version numbers may not be
maintained.

The user may have customised a skill. Overwriting their change is worse than not installing.

## The flow

```
1. Receive the language parameter (explicit, never inferred)
2. Scan the project: type, existing files, runtime -> a needed/not-needed/pending list
3. Look up the skill catalogue for that language
4. For each: source exists? -> verify language -> compare content -> install / skip / report conflict / record failure
5. Verify each is triggerable; produce the five-column install report
6. Judge each optional capability three ways; for those needing credentials, read their documentation first and follow the guided flow
7. Emit the overall report: ready / failed and not applicable / pending
```

## Optional capabilities

Six of them, each judged **needed / not needed / pending**, and verified as available in the
current session once configured.

**"Not needed" MUST carry a reason** — "browser testing tool — this project has no web
surface, not applicable" is far more useful than letting it vanish from the report.

**Conditional capabilities are not pre-installed**: visual implementation, browser testing
and parallel agents are enabled only where the project genuinely needs them.

**Guided installation**: for capabilities needing credentials or having prerequisites, **read
their own documentation first and follow the guided flow**. Where that documentation is
unavailable, mark the capability pending and **do not act**.

See `references/optional-capabilities.md` for the six capabilities and the guidance rules.
See `references/dual-route-research.md` for the dual-route cross-verification standard.

## Scope

**Every installation is scoped to the current project. Global configuration and other
projects MUST NOT be modified.**

Where a capability is already installed globally: report that it exists, do not duplicate it
into the project, and **do not touch the global installation**.

## Honest recording

**MUST NOT fake success.** If it will not install, say it will not install; if verification
fails, say where it stopped.

A failure partway through **does not roll back** — what is already installed stays, and the
report states the break point and what remains.
A rollback could delete a same-named skill the user already had.

The overall report is both emitted in the session and created at
`specs/research/toolchain-setup-report.md`; if the file already exists, skip it rather than
overwriting the previous execution record.

See `references/verification-protocol.md` for the layered verification signals and the
failure record format.

## Subset installs

The user may install only a few. Install exactly what was named, and **report the impact of
the ones not installed on the full chain**.

**MUST NOT refuse a subset for being "incomplete"** — wanting only two skills is an entirely
legitimate use.

## Upstream Artifacts

| Artifact | Level | When missing |
|---|:---:|---|
| Language parameter | **required** | Stop and ask; never infer |
| Skill asset source directory | **required** | Stop - with no source there is nothing to install |
| Documentation for an optional capability | optional | Mark it pending; do not install from impression |

## Downstream Consumers

| Consumer | What it depends on |
|---|---|
| Every later stage | The installed and verified project-scoped skills |
| The research stage | The research search capability plus the dual-route cross-verification standard |
| The user | The pending list — deciding whether to go and open accounts first |

## Standalone Use

**What you provide**: the language parameter and the path to the asset source directory. If
you want only a few, say which.

**What you get**: project-scoped installation and verification of the skills in that range, a
five-column install report, and a three-way judgement on the six optional capabilities.
Idempotence and language isolation apply identically in standalone mode.

**What you don't get**:

- **It does not generate the project context file** — that belongs to the context bootstrap
  skill; the two are semantically adjacent but do different jobs.
- **It does not register external accounts for you.** For capabilities needing credentials it
  tells you where to sign up and what format the key takes; it does not do it for you.
- A capability whose documentation is unavailable **will not be installed**, only marked
  pending — installing from impression fails as "half installed", which is harder to
  diagnose than not installed at all.

## Anti-patterns

- Substituting the English version when the Chinese version is missing
- Inferring the language parameter from the environment or the locale
- Deriving English directory names by concatenating "Chinese name + -en"
- Automatically overwriting a same-named skill whose content differs
- Modifying global configuration or another project
- Running a credentialed capability's install command without reading its documentation
- Pre-installing conditional capabilities (visual / browser / parallel agents)
- Letting a failure vanish silently from the report
- Rolling back after a partway failure and deleting what the user already had
- Refusing because the user only wants to install two
