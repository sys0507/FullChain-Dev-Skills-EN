# Configuring the optional capabilities

## When to read this

After installing the skills, when configuring the optional capabilities the project needs.

---

## The six capabilities

Each is judged **needed / not needed / pending**, and once configured, **verified as available
in the current session**.

| Capability | Purpose | Enable when | Needs credentials |
|---|---|---|:---:|
| **Research search** | Gives the research stage **a second independent search source** | The project needs external factual research | Yes |
| Development status display | A status line for cost, elapsed time, tokens and todos | The tool in use supports it | No |
| Engineering workflow enhancement | Divergence, TDD, code review, branch close-out, the four spec steps | Recommended whenever available | No |
| Visual implementation toolchain | Design to code | **Only when** the project has a compatible visual interface | Depends on the tool |
| Browser debugging and testing | Debugging and acceptance for browser scenarios | **Only when** the project has a web or browser surface | No |
| Parallel agents | Parallel execution of research and adversarial evaluation | **Only when** the tool supports it and the tasks parallelise safely | No |

---

## The three-way judgement

| State | When to use it | What the report MUST say |
|---|---|---|
| **Needed** | The project genuinely uses it | The configuration result and the verification result |
| **Not needed** | Judged not applicable | **The specific reason it is not applicable** |
| **Pending** | Cannot be judged alone (an account, a quota, a personal preference) | The specific question the user must decide |

**"Not needed" MUST carry a reason.** "Browser testing tool - this project has no web
surface, not applicable" is far more useful than letting it vanish from the report; the
latter leaves people asking "do we need to configure this?" over and over.

---

## Conditional capabilities are not pre-installed

Visual implementation, browser testing and parallel agents are **enabled only where the
project genuinely needs them**.

The judgement comes from the project scan, not from "installing it can't hurt".
Pre-installing costs the user an unused thing in their environment, and adds noise the next
time they debug something.

---

## Guided installation (for capabilities needing credentials)

For a capability needing credentials or having prerequisites:

> **Read its own documentation first, then follow its guided flow.
> MUST NOT run commands from impression.**

Why: the install steps, configuration file locations and environment variable names differ
for each of these, and running from impression typically fails as "half installed" — which is
harder to diagnose than not installed at all.

| Situation | Handling |
|---|---|
| The documentation is available | Read it and follow its guided flow |
| **The documentation is unavailable** | Mark that item pending and **do not act** |
| The documentation exists but looks out of date | Follow it anyway; on failure, record it and label it "documentation may be out of date" |

---

## Sensitive values

Keys for credentialed capabilities go **only into local files covered by the ignore rules, or
into a secret manager**.

The report records only the configuration item's name, its purpose and whether it is ready.
**It never records values.**

Where the configuration file that will hold a key does not exist yet, it is worth **adding it
to the ignore rules in advance** — adding it after it appears is too late, because it may
already have been committed by accident on first generation.

---

## Capabilities already installed globally

| Situation | Handling |
|---|---|
| The capability is already installed globally | **Report that it exists**; do not duplicate it into the project, and **do not modify the global configuration** |

"Do not modify the global" is a hard constraint. A user's global environment serves all their
projects; this skill is responsible only for the current one.

---

## Honest recording

| Situation | What the report says |
|---|---|
| Configuration failed | The failed item + its impact + whether it blocks |
| Verification failed | The verification method + the actual result |
| Unknown or not applicable | Marked explicitly; **never dressed up as installed** |

**MUST NOT fake success.** If something will not install, say so — downstream seeing "ready"
and then finding it unusable is worse than knowing from the start that it is not installed.

---

## How this connects to dual-route research

Once the research search capability is configured, the downstream research stage applies the
**dual-route cross-verification** standard. See `dual-route-research.md`.

That capability being **unconfigured does not block**, but the research conclusions are then
verified by one route only, and the output MUST say so.
