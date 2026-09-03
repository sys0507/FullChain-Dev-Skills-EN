# FullChain-Dev-Skills-EN · CLAUDE.md

> The English edition of the full-chain development skill set.

## 1 · What this project is (WHAT)

Twenty reusable Agent Skills covering the eleven stages of full-chain development, from a
project idea through research, requirements, specification, design, implementation, testing
and retrospective to release. Each skill works **both** as part of the chain and **on its
own**; standalone is not a degraded mode.

This tree is the English edition. The Chinese edition lives in the sibling
`全链路开发汇总/`, and it is where this one was ported from.

## 2 · Why this project exists (WHY)

A 793-line prompt template covering eleven stages meant copying and pasting by hand for every
new project, with no way for improvements to flow back into projects already under way. The
skills turn that template into assets: version-controlled, checkable, and reusable one at a
time.

The English edition exists because an English workflow that emits Chinese-named artifacts is
exactly the kind of pollution hard language isolation forbids.

## 3 · Workflow (HOW)

**Starting work on a skill**

1. Read `docs/EN-PORT-SPEC.md` — the fixed vocabulary, the path map, and the rules that
   outrank fluency
2. Read the Chinese counterpart in `../全链路开发汇总/Assets/skills/<name>/`
3. Check what the checks currently say before changing anything

**While working**

- The three contract sections, the three standalone questions and the dependency level enum
  are matched **literally** by the checks. Do not invent alternative wording.
- Never read across languages. An English skill that cannot find its English input reports
  the miss; it MUST NOT fall back to the Chinese file.
- Every honest label in the Chinese version comes across. If it says something is unverified,
  so does the English.

**Before finishing**

```
python tools/skill_checks/run_all.py --scope en --phase 3
python tools/skill_checks/run_all.py --check C2 --phase 3 \
  --skills-root ../全链路开发汇总/Assets/skills --en-root Assets/skills
```

Both must be clean. C2 is the drift detector between the two trees, and it is the only thing
that will notice a change landing on one side only.

**Rhythm**

One skill at a time; run the checks; commit. Do not batch several skills into one unchecked
commit.

## 4 · Tech stack

The deliverables are Markdown and Agent Skills. Two skills carry Python scripts
(`fullchain-toolchain-setup-en` and `release-packaging-router-en`), plus the checker under
`tools/`. All of it is **standard library only** — there is no dependency manifest, and none
should be invented.

## 5 · Commands

```bash
# Every check, English scope
python tools/skill_checks/run_all.py --scope en --phase 3

# Cross-tree pairing check
python tools/skill_checks/run_all.py --check C2 --phase 3 \
  --skills-root ../全链路开发汇总/Assets/skills --en-root Assets/skills

# The checker's own tests
python tools/skill_checks/tests/test_checks.py

# The two scripted skills' tests
python Assets/skills/fullchain-toolchain-setup-en/tests/test_toolchain_setup.py
python Assets/skills/release-packaging-router-en/tests/test_route_release.py
python Assets/skills/full-chain-testing-en/tests/test_pathinv.py
```

## 6 · Governing rules

This tree is governed by the Chinese edition's constitution, in
`../全链路开发汇总/.specify/memory/constitution.md`. Four of its seven principles are
non-negotiable; the two that bite hardest here are hard language isolation and dual-mode
parity.

## 7 · Visual system

**Not applicable.** The deliverables are Markdown and scripts, with no graphical interface
and no `DESIGN.md`.

## 8 · Anti-patterns

| # | Forbidden | Source |
|:-:|---|---|
| 1 | Reading across languages, or substituting the other language version when one is missing | Constitution II |
| 2 | Inferring the language parameter from the environment or the locale | Constitution II |
| 3 | Deriving the English directory name by concatenating "Chinese name + -en" | The first four carry -universal; concatenation gets them wrong |
| 4 | Chinese characters anywhere in this tree, including .py and .json | Check C3 (which currently scans only .md — a known blind spot) |
| 5 | Inventing wording for the three sections, the three questions or the dependency enum | The checks match literally; unenumerable rules cannot be enforced |
| 6 | Softening a MUST into a suggestion for the sake of fluent English | A constraint translated as advice is a mistranslation |
| 7 | Claiming something was verified when it was not | Constitution IV |
| 8 | A cross-skill file path inside a skill directory | Constitution III (by-name references are fine) |

## 9 · Behavioral Guidelines (Karpathy-Inspired)

These four principles apply during every task's implementation phase.

**Think before coding.** State your assumptions; if uncertain, ask. Where several readings
exist, present them rather than picking silently. Where a simpler approach exists, say so.

**Simplicity first.** The minimum that solves the problem. No speculative features, no
abstractions for single-use code, no configurability nobody asked for.

**Surgical changes.** Touch only what you must. Do not improve adjacent code, comments or
formatting. Match the existing style even where you would do it differently. Clean up only
the orphans your own change created.

**Goal-driven execution.** Turn tasks into verifiable goals, and loop until verified.
"Add validation" becomes "write tests for invalid inputs, then make them pass".

## 10 · Key file navigation

| File | When to read it |
|---|---|
| `docs/EN-PORT-SPEC.md` | Before touching any skill — the fixed vocabulary and the path map |
| `docs/PHASE3-STATE.md` | To find out what is done and what remains |
| `Full-Chain-Development-Skill-Execution-Index.md` | To drive the chain: what to call, when to stop |
| `Full-Chain-Development-Prompt-Template.md` | To look up why a stage is designed the way it is |
| `Full-Chain-Development-Prompt-Template-Skills-Edition.md` | The skill-driven execution edition of the same template |
| `Assets/skills/<name>/SKILL.md` | When calling or changing a skill |
| `../全链路开发汇总/docs/stage-artifact-contract.md` | The single source of truth for paths and gates; section 3.5 holds the English path map |
| `../全链路开发汇总/.specify/memory/constitution.md` | The seven principles governing both trees |
