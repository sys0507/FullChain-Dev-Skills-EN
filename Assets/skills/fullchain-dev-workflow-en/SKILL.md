---
name: fullchain-dev-workflow-en
description: >-
  Thin orchestrator that advances the eleven full-chain stages in order: determine which Skill to call next,
  actually stop at gates, decide whether conditional stages apply, and record where the chain is, what was
  skipped, and why so work can resume from any stage. When a stage Skill is not installed, report the missing
  Skill and provide the manual path instead of silently skipping it. Trigger keywords: full chain / run the
  workflow / develop from scratch / what comes next / chain state / resume from checkpoint / orchestration /
  orchestrator / run the complete process. Do not use it to perform any stage's work, restate stage execution
  rules, define file paths (the contract matrix owns them), pass a gate for the user, or run multiple features
  concurrently. Invoke it whenever the request means “follow this workflow from the beginning,” even when the
  user does not explicitly say “use a Skill.”
license: MIT
metadata:
  version: "1.0"
  lang: en
  kind: behavioural
  stage: "0-11"
  standalone: true
  produces:
    - "specs/research/chain-state.md"
  requires:
    - name: "docs/stage-artifact-contract.md"
      level: optional
      fallback: "Use the built-in table in references/stage-order.md; label the output: 'Contract matrix not read; paths and gates were not cross-validated'"
    - name: ".claude/skills/ directory"
      level: optional
      fallback: "Installed Skills cannot be detected; ask the user at each step whether that Skill is available"
    - name: "the 18 stage Skills"
      level: orchestration
      fallback: "Report each missing Skill and give the manual path (the matching section in the frozen template); never silently skip it"
---

# Full-Chain Orchestrator

## What This Skill Knows—and Does Not Know

| Knows | Does not know |
|---|---|
| Order—which stage comes next | **How to perform each stage** |
| Gates—where it MUST stop | What content each stage produces |
| Conditions—which stages may not run | What file paths look like |

**Other authorities own all three items on the right:** each stage's own SKILL.md explains how to work;
`docs/stage-artifact-contract.md` defines paths.

**Restating either here creates a second source of truth.** It will drift, and nobody will know which copy to
trust. This Skill deliberately stays within the 200-line limit even though its category permits 350, so growth
becomes visible as soon as it happens.

## Four Actions Per Turn

```
1. Find the next step   scripts/chain_state.py --root .
2. Conditional stage?  Give a conclusion for each criterion -> wait for user confirmation -> run, or record why skipped
3. Is the Skill present? If not, report it + the manual path; never silently skip
4. Invoke -> stop at a gate -> write back state
```

## 1. Find the Next Step

```
python scripts/chain_state.py --root .          # read-only; changes no file
python scripts/chain_state.py --root . --init   # create the state file; skip if it exists
```

**Read-only operations MUST NOT write files**—checking progress must have no side effect.

The four states are `not-started` / `completed` / `skipped` / `completed-without-skill`.
The last three are terminal and MUST NOT reappear as pending work.

**The fourth state records degraded execution.** Use it when a stage Skill is missing and the manual path is
used. Without it, the row could only say `completed`; the degradation would survive only in the change log,
while **people scan the table**.

Both `skipped` and `completed-without-skill` **MUST include a reason**. The script reports an empty reason as
an inconsistency.

**Report disagreement between state and real artifacts; do not fix it automatically.** If state says stage 3
is complete but `prd.md` is absent, that is a signal for human review, not noise to erase.

## 2. Conditional Stages

There are four: **1.3 adversarial selection, 5.1 interface design, 5.2 design injection, and 11 packaging/deployment**.

The criteria are executable and yield yes/no conclusions. If they cannot, information is missing—**ask the
user instead of deciding by yourself**.

A skip MUST include a reason. **The script reports an empty reason as an inconsistency.**

Read `references/stage-order.md` for the four criteria and the order of all 17 execution points.

## 3. Missing Skill

**Report the missing Skill and give the manual path; never silently skip it.**

A silent skip makes the user believe the whole chain ran even though two stage outputs are absent and downstream
work proceeded on top of those gaps.

The manual path is that stage's section number in the frozen template. **Say plainly that the Skill is absent;
do not recommend a substitute or pretend its output already exists.**

## 4. Gates

**Actually stop at every gate.** “Skip confirmation so the chain can finish” is this orchestrator's likeliest failure.

When stopping, state three things: **what you are waiting for** (specific enough to answer), **where the output
is**, and **which Skill comes next after confirmation**.

If the user explicitly asks to skip, **allow it but leave a trace**: record the reason, label “stage N was not
executed; its output was not generated,” and warn which downstream stages will lose input.

**After confirmation, write state before continuing.** Written state is the only reliable recovery point after
an interruption.

Read `references/gate-protocol.md` for gate wording, refusal wording, and recovery.

## Starting in the Middle

Allowed. Label “stages 1-N were not executed by this orchestrator; their artifact state is unknown.” **Do not
pretend they are complete, and do not force the user to rerun them.**

## Upstream Artifacts

| Artifact | Level | When missing |
|---|:---:|---|
| `docs/stage-artifact-contract.md` | optional | Use `references/stage-order.md`; label “contract matrix not read” |
| `.claude/skills/` directory | optional | Installed Skills cannot be detected; ask the user at each step |
| The 18 stage Skills | orchestration | Report each missing Skill + manual path; never silently skip |

There are **zero `required` dependencies**—the orchestrator can start in an empty directory, precisely where it
is most useful.

## Downstream Consumers

| Consumer | What it takes |
|---|---|
| Stage Skills | Invoked **by name**; the orchestrator neither reads their files nor changes their outputs |
| User | `specs/research/chain-state.md`—after days away, see immediately where work stopped and why anything was skipped |

## Standalone Use

**What you provide:** A project directory; it may be empty. Without a contract matrix, use the built-in order
table and label that fallback in the output.

**What you get:** At each step, the next Skill, whether to stop, and what is awaited, plus a human-readable state
file that supports resuming from any stage.

**What you don't get:** It does not perform any stage's work—it only identifies whom to invoke; it does not pass
gates for you; it does not run multiple features concurrently because stages have a dependency topology; and if
a Skill is missing, **it never pretends that step was completed normally**.
