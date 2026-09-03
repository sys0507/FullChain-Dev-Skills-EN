# Gate Protocol

## When to Read

Read this at any stage marked with a gate.

## A Gate Is Design, Not Obstruction

Gates sit where changing direction is **expensive**: after scope freezes, after a PRD is finalized, or after a
release channel is selected, reversal costs far more than confirming in place.

**“Skip confirmation so the chain can finish” is this orchestrator's likeliest failure.**

## Say Three Things When You Stop

| # | Say | Counterexample |
|:-:|---|---|
| 1 | **What you are waiting for**—specific enough to answer | “Please confirm” |
| 2 | **Where the output is**—where the user should review it | Say nothing and make the user search |
| 3 | **What follows confirmation**—which Skill comes next | Say nothing, hiding the consequence |

Good example:

> **Stage 3 gate.**
> Waiting for: whether all 14 chapters of `specs/prd.md` are final, especially chapter 5 scope and chapter 13 open questions.
> After confirmation: stage 4 begins; `speckit-feature-pipeline-en` splits Must-haves into features, then stops again for review of the split table.

## Refusal Wording

Baseline rationalizations and their counters:

> **“The user said ‘run everything and report at the end,’ so gates may pass continuously.”**
>
> Authorization to continue is not authorization to erase confirmation. The correct action is to **stop as
> usual, record what is awaited, then continue under the authorization**, and list every continuously passed
> gate in the final report.
>
> A skipped gate leaves no record, so the user cannot know what was missed. A recorded-then-continued gate
> leaves a trace the user can review later.
>
> **Phase 1 validation A did exactly this: gates were identified and recorded but did not truly stop execution.
> It therefore proved detection, not that a gate can block the agent. The acceptance report records that gap honestly.**

> **“This stage's output is obviously correct; stopping wastes time.”**
>
> “Obviously correct” is the executor's judgment. A gate requires the **decision-maker's** judgment. They often
> agree, but the few times they do not are why the gate exists.

> **“The user is away; proceed now and confirm later.”**
>
> Confirmation cannot be added later. Downstream stages will build on an unconfirmed output; when the user
> returns, a whole chain—not one step—must be undone. Stop here and write exactly what is awaited so work can
> resume immediately.

## User Explicitly Requests a Skip

**Allow it, but leave a trace:**

| # | Required action |
|:-:|---|
| 1 | Record the skipped stage and the user's reason |
| 2 | Write “**stage N was not executed; its output was not generated**” in the state file |
| 3 | Warn which downstream stages will fall back or lose input |

The third action is easiest to miss. Skipping stage 3 does not merely remove one PRD; stage 4 then has **no
Must-haves to split into features**.

## Degradation Also Leaves a Trace

When a stage Skill is missing, write `completed-without-skill`, not `completed`, and name the missing Skill and
manual path in the reason column.

**Why `completed` is wrong:** a person scanning an all-completed table assumes the chain followed every
constraint. In reality, that output **did not pass through the missing Skill's checks**, and downstream work
must know this.

## Recovery

After confirmation, **write state before continuing**. Written state is the only recovery basis after interruption.

Read `stage-order.md` for stage order and conditional criteria.
