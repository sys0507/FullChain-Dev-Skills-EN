# Full-Chain Development Skills

Twenty-one reusable Agent Skills covering the eleven stages of full-chain development — from a
project idea through research, requirements, specification, design, implementation, testing
and retrospective, to release.

**Each skill works both as part of the chain and on its own.** Standalone is not a degraded
mode: every upstream artifact has a "you provide it directly" equivalent, and no skill refuses
to work because a convention directory is missing.

---

## What is here

```
Assets/skills/          21 skills, project-scoped
Assets/mcp/             Shared research MCP servers referenced by the templates
Assets/configs/         Shared editor/status configuration referenced by the templates
tools/skill_checks/     10 structural checks, with their own tests
docs/                   The port spec and the current state
Full-Chain-Development-Skill-Execution-Index.md      What to call, when to stop
Full-Chain-Development-Prompt-Template.md            The full original prompts, for reference and audit
Full-Chain-Development-Prompt-Template-Skills-Edition.md   The skill-driven execution edition
```

## The eleven stages and their skills

| Stage | Skill |
|---|---|
| 0-11 Orchestration | `fullchain-dev-workflow-en` |
| 0 Toolchain setup | `fullchain-toolchain-setup-en` |
| 1.1 Project ledger | `project-context-ledger-en` |
| 1.2 Kickoff research | `product-research-kickoff-universal-en` |
| 1.3 Adversarial selection | `adversarial-architecture-selection-universal-en` |
| 2 MVP convergence | `mvp-convergence-brainstorming-en` |
| 3 The PRD | `prd-writer-universal-en` |
| 4 Four-step documents | `speckit-feature-pipeline-en` |
| 5.1 Interface design | `platform-design-kickoff-en` |
| 5.2 Design injection | `speckit-design-injection-universal-en` |
| 6 Project context | `claude-md-bootstrap-en` |
| 7 Implementation setup | `implementation-runway-setup-en` |
| 8 TDD implementation | `run-feature-en` |
| 9 Testing | `testing-system-blueprint-en`, `test-routing-advisor-en`, and four executors |
| 10 Retrospective | `learnings-retrospective-en` |
| 11 Packaging and release | `release-packaging-router-en` |

## Getting started

**Install everything**:

```bash
python Assets/skills/fullchain-toolchain-setup-en/scripts/toolchain_setup.py \
  --source Assets/skills --project-root /path/to/your/project --lang en
```

**Install only what you want** — this is a supported use, not a compromise:

```bash
python Assets/skills/fullchain-toolchain-setup-en/scripts/toolchain_setup.py \
  --source Assets/skills --project-root /path/to/your/project --lang en \
  --only prd-writer-universal-en run-feature-en
```

The installer is idempotent: an existing skill with identical content is skipped, and one you
have customised is reported for your ruling rather than overwritten.

The two prompt templates also reference `Assets/mcp/ml-search-mcp` and
`Assets/configs/claude-hud-config.json`; both are included in this repository. The shared MCP
directory additionally retains `muyu-search-mcp` for China-oriented search workflows.

**Driving the chain**: read `Full-Chain-Development-Skill-Execution-Index.md`. It says what
each step does, which skill to call, and where to stop — and nothing about design reasoning,
which lives in the template.

## Three rules worth knowing before you start

**Hard language isolation.** An English workflow installs only the English skills. When one
is missing, the installer reports a failure rather than substituting the Chinese version.
Mixing produces artifacts nobody can attribute, and once the two editions drift, the result
of mixing them is unpredictable.

**Gates are real stops.** Where a stage is marked with a gate, the skill stops and says what
it is waiting for. This is deliberate: the gates sit where changing your mind later is
expensive.

**Honest labelling over a clean-looking report.** When a skill takes a fallback path, its
output says which capability was not used and what is therefore not covered. A report full of
"unverified" is worth more than one that looks entirely green and is not.

## Verifying this tree

```bash
python tools/skill_checks/run_all.py --scope en --phase 3 --messages en
```

Ten checks: broken and orphaned references, Chinese residue, English evals identity, scripts
having tests, directory self-containment, the three contract sections, dependency grading,
size budgets, and matrix path propagation.

Cross-tree drift against the Chinese edition:

```bash
python tools/skill_checks/run_all.py --check C2 C4 C5 --phase 3 --messages en \
  --skills-root ../全链路开发汇总/Assets/skills --en-root Assets/skills
```

## Orchestrating the Complete Chain

Use `fullchain-dev-workflow-en` to calculate the next stage, stop at gates, evaluate conditional
stages, and maintain `specs/research/chain-state.md`. It remains deliberately thin: each stage
Skill owns execution details, and the contract matrix owns artifact paths.

## Licence

MIT.
