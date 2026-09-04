---
name: release-packaging-router-en
description: >-
  Decide whether a project needs packaging and release, then route each artifact to the right
  channel: container, package registry, app store, installer, firmware, hosting platform or
  private artifact repository, singly or in combination. Produce a release-channel decision
  report with reasons for rejected options, then turn the packaging work into a proper feature
  for the existing four-step pipeline. A container is only one of seven choices, never the
  default. Triggers: package / deploy / release / launch / distribute / artifact / image /
  publish a version / release / stage 11. Do not use to write Dockerfile or CI workflow contents
  (implementation stage), run the four-step documents (speckit-feature-pipeline-en), release on
  the user's behalf, register publishing-platform accounts, or invent packaging for a project
  that needs no distribution. Invoke whenever the task concerns how the product will be released,
  even if the user does not mention a Skill.
license: MIT
metadata:
  version: "1.0"
  lang: en
  kind: behavioural
  stage: "11"
  standalone: true
  produces:
    - "specs/<id>-<slug>/release-channel-decision.md"
    - "the packaging feature's directory and spec skeleton"
  requires:
    - name: "project manifest file"
      level: required
      fallback: "Ask the user what the project produces and who consumes it; label the report 'project manifest not read, shape judgement not cross-checked'"
    - name: "specs/prd.md"
      level: optional
      fallback: "Ask about the target environment directly; label the report 'PRD not read'"
    - name: "specs/research/05-decision-summary.md"
      level: optional
      fallback: "Report the skip reason in the session, labelled 'not written to the decision summary'"
    - name: "speckit-feature-pipeline-en"
      level: orchestration
      fallback: "The skeleton is still produced; tell the user the four-step documents need handling separately"
---

# Release Packaging Router (Stage 11)

## What this skill is guarding against

**Writing a Dockerfile for an npm library.**

The frozen template's stage 11 says it plainly in its first paragraph: containers "MUST NOT
be forced on mobile, desktop, SDK, library, plugin or embedded projects". And then the
execution prompt that follows is entirely about base images, multi-stage builds,
`docker compose up -d` and health checks — **the warning is in paragraph one and the
counterexample is in paragraph two**.

An agent reads it, follows it, and produces a container solution for a project that needs no
container.

This skill turns that warning into **a step you cannot skip**.

## Step 1: does it need distributing

| Criterion | Conclusion |
|---|---|
| The artifact is only ever used by you on your own machine | **Not applicable** |
| The artifact goes to someone else (a colleague, a user, another machine) | Applicable |
| The artifact is depended on by another project | Applicable |

When not applicable: **record the reason** in `specs/research/05-decision-summary.md`, and
**produce no feature skeleton at all**. That is a normal exit, not a failure.

## Step 2: detect the artifact shape

```
python scripts/route_release.py --root .
```

The script reads the manifests and emits **candidate channels**. Three disciplines:

| # | Discipline |
|:-:|---|
| 1 | **An unclear shape is marked unknown, never guessed** — a wrong guess travels all the way to tasks before anyone notices |
| 2 | **A conflict is reported, never chosen** — a judgement a tool makes goes unquestioned precisely because it came from a tool |
| 3 | **Several artifacts are not merged** — a service plus a CLI needs two channels, or the CLI's users get no package |

**Installer and private registry have no automatic signal** and can only come from the user.
That is not an omission — no manifest field can express "produce an .msi for machines on the
internal network".

See `references/artifact-detection.md` for the signal table and the detection disciplines.

## Step 3: supply the reasoning

**The script gives candidates, the agent gives reasons, the user rules.** None of the three
substitutes for another.

The decision report MUST contain:

| # | Content |
|:-:|---|
| 1 | Which channel or channels were chosen |
| 2 | **Why this one** — grounded in this project's artifact shape and its consumers |
| 3 | **Which were rejected and why** — writing only what was chosen is not a decision, and the user cannot review it |
| 4 | The labelling for any fallback path taken |

Written to `specs/<id>-<slug>/release-channel-decision.md`. **Do not overwrite an existing one.**

## Step 4: the gate

**Stop. Wait for the user to confirm the release channel.**

The channel determines the shape of every packaging task that follows, and changing it later
is expensive. This confirmation cannot be skipped.

## Step 5: turn it into a feature

Once confirmed, create the feature directory and a **spec skeleton**, then hand it to
`speckit-feature-pipeline-en` for specify -> clarify -> plan -> tasks.

**This skill does not run the four steps.** Their quality constraints (clarify's four
boundary classes, plan's five elements, tasks at 12-18) belong to that skill, and a copy here
would inevitably drift.

For what clarify should ask, look up the playbook for the confirmed channel — **read that
section only, not the whole file**.

See `references/channel-playbooks.md` for the clarify checklist per channel.

## Upstream Artifacts

| Artifact | Level | When missing |
|---|:---:|---|
| Project manifest file | **required** | Ask what the project produces and who consumes it; label "project manifest not read" |
| `specs/prd.md` | optional | Ask about the target environment directly; label "PRD not read" |
| `specs/research/05-decision-summary.md` | optional | Skip reason to session output, labelled "not written to the decision summary" |
| `speckit-feature-pipeline-en` | orchestration | The skeleton is still produced; note the four steps need handling separately |

## Downstream Consumers

| Consumer | What it takes |
|---|---|
| `speckit-feature-pipeline-en` | The feature directory and spec skeleton, to run the four steps |
| `run-feature-en` | Implements the packaging feature once the four steps are done |
| The user | The release channel decision report — telling them whether to go register accounts or apply for certificates first |

## Standalone Use

**What you provide**: a project directory. Even with no manifest file it works — answer two
questions: what does this project produce, and who consumes it.

**What you get**: a release channel decision report — which channel, why, what was rejected —
plus that channel's checklist of what clarify must settle.

**What you don't get**: it will not write your Dockerfile, CI workflow or any packaging
script; it will not run the four-step documents for you; it will not register release
platform accounts or apply for certificates on your behalf; and where the shape is unclear or
conflicting **it will not choose for you** — that is your decision.
