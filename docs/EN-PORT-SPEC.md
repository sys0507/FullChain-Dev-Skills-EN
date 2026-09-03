# English Port Spec

> The single authority for how a Chinese skill becomes an English one.
> Every porter reads this **first**. Do not invent alternative wording —
> the checks match these strings literally.

## 1. Fixed vocabulary

### Three contract sections (exact headings, `##` level)

```
## Upstream Artifacts
## Downstream Consumers
## Standalone Use
```

### The three questions `## Standalone Use` must answer

```
What you provide
What you get
What you don't get
```

Note the apostrophe in `don't` — it is a plain ASCII `'`, not a curly quote.

### Dependency level enum (closed, three values)

| Chinese | English | Meaning |
|---|---|---|
| `必需` | `required` | Cannot work without it; must stop and say so |
| `可选增强` | `optional` | Degrades; **MUST** state the fallback |
| `编排级` | `orchestration` | Supplied upstream in the chain; ask the user directly when standalone |

**Every non-`required` entry MUST carry a `fallback:` line.**
Grading rule, same in both languages: **if it can be `optional`, it is not `required`.**

### `description` must state what the skill is NOT for

Include one of: `do not use`, `not for`, `does not`.

## 2. Frontmatter shape

```yaml
---
name: <directory-name>          # must end in -en
description: >-
  What it does. Trigger keywords: ... . Do not use for: ... .
license: MIT
metadata:
  version: "1.0"
  lang: en
  kind: <same value as the Chinese twin>
  stage: "<same as Chinese twin>"
  standalone: true
  produces:
    - "<exact output path, English filename per the path map below>"
  requires:
    - name: "<exact input path or resource>"
      level: required
    - name: "<...>"
      level: optional
      fallback: "what happens without it, and what is therefore not covered"
---
```

`lang: en` is mandatory. `requires:` is mandatory.

## 3. Path map — English outputs use English filenames

| Chinese | English |
|---|---|
| `specs/research/00-项目输入与假设.md` | `specs/research/00-project-input-and-assumptions.md` |
| `specs/research/01-产品形态.md` | `specs/research/01-product-shape.md` |
| `specs/research/02-关键资源与外部依赖.md` | `specs/research/02-key-resources-and-dependencies.md` |
| `specs/research/03-开源项目.md` | `specs/research/03-open-source-candidates.md` |
| `specs/research/04-实现方案.md` | `specs/research/04-implementation-options.md` |
| `specs/research/05-决策汇总.md` | `specs/research/05-decision-summary.md` |
| `specs/research/06-架构基线决策.md` | `specs/research/06-architecture-baseline.md` |
| `specs/research/07-MVP收敛结果.md` | `specs/research/07-mvp-convergence.md` |
| `specs/research/链路状态.md` | `specs/research/chain-state.md` |
| `specs/<id>-<feature>/测试路由判定.md` | `specs/<id>-<feature>/test-routing-decision.md` |

> **本表是复制件，不是定义处。** 英文版路径的唯一定义处是中文库的
> `docs/stage-artifact-contract.md` §3.5（宪法原则 VII）。冲突时以那张表为准。
> 本表若与之不一致，是本文件错了。

**Unchanged in both languages** (they come from the wider ecosystem, not from this template):
`spec.md` `plan.md` `tasks.md` `state.md` `session.md` `prd.md`
`CLAUDE.md` `LEARNINGS.md` `DESIGN.md` `.worktreeinclude`
and every directory name (`specs/`, `specs/research/`, `.claude/skills/`).

**Never read across languages.** An English skill that cannot find its English
input reports the miss — it must not fall back to the Chinese file.

## 4. What the three sections contain

### `## Upstream Artifacts`

A table: artifact | level | what happens when it is missing.
Every non-`required` row states the fallback **and what that fallback leaves uncovered**.

### `## Downstream Consumers`

A table: consumer | what it takes from this skill.
Reference other skills **by name only** — never by file path. A skill directory
must stay self-contained.

### `## Standalone Use`

Prose, answering the three questions in order. Be concrete about the third —
"What you don't get" is the honest part, and it is the reason the section exists.

## 5. Rules that outrank fluency

1. **Translate the intent, not the words.** These are instructions to an agent.
   If a literal rendering reads as a suggestion where the Chinese was an
   obligation, the translation is wrong.
2. **Keep MUST / MUST NOT force.** Chinese `MUST` / `不得` become `MUST` / `MUST NOT`.
3. **No Chinese characters anywhere in the English tree** — including in
   file paths, examples, and table cells. One check exists solely for this.
4. **Do not add content the Chinese version lacks**, and do not drop content it has.
   The heading count is compared between the two versions.
5. **Never claim something was verified when it was not.** If the Chinese text
   labels something unverified, the English text says so too.

## 6. Done means

Run from the English tree root:

```
python tools/skill_checks/run_all.py --scope en --phase 3 --messages en \n  --matrix ../全链路开发汇总/docs/stage-artifact-contract.md
```

C1, C3, C4, C5, C6, C7, C8, C9, C10 all clean for the skills you touched.
C2, C4, and C5 need the Chinese tree for paired Skill, eval, script, and test checks:

```
python tools/skill_checks/run_all.py --check C2 C4 C5 --phase 3 --messages en \
  --skills-root ../全链路开发汇总/Assets/skills \
  --en-root Assets/skills
```
