# Sub-item B: external services and credentials inventory

## When to read this

When taking stock of the external services, accounts, permissions and configuration that
development and testing require.

---

## Five columns (there is no sixth)

| Column | What goes in it |
|---|---|
| **Configuration item name** | The environment variable name or capability name |
| **Purpose** | What cannot be done without it |
| **Environment** | Where it lives (local config file / secret manager / session environment) |
| **How to obtain** | Where to register, what prerequisites exist, what the key looks like |
| **Ready** | Ready / not yet / pending / not applicable (see below) |

> **There is no "value" column, and there never will be.**
> Sensitive values go only into local files covered by the ignore rules, or into a secret
> manager.

## The four readiness states

| Marker | Meaning |
|---|---|
| Ready | Available and usable now |
| Not yet | Not prepared, but **does not block** the current stage |
| Pending | **Waiting on the user** — it involves an account, a quota or a personal preference the agent cannot decide |
| Not applicable | Judged irrelevant to this project |

**The difference between pending and not-yet matters**: "not yet" means "known to be needed,
not done"; "pending" means "unknown whether it should be done at all". The first can be
progressed alone; the second MUST be asked.

---

## Scan sources

Scan in order; each one supplements the last:

| # | Source | What it yields |
|:-:|---|---|
| 1 | The dependency lists in each feature's spec and plan | Dependencies the project declares itself |
| 2 | Documentation and sample configuration for services bundled in the project | Concrete variable names and formats |
| 3 | The project context file and README | Capabilities already enabled |
| 4 | Whether the actual configuration files exist | Readiness state |

**A sample configuration file is the best source** — it usually lists every variable name,
with placeholder values that are safe to quote.

---

## Guided collection

For items that need the user's answer:

1. **Ask one at a time**
2. Explain **why it is needed** (what cannot be done without it)
3. Offer **a way not to answer** ("mark it pending and decide when it is needed")

Anything uncertain is marked pending. **Do not guess and do not fill it in on their behalf.**

---

## Handling sensitive values

| Situation | Handling |
|---|---|
| The user supplies a real key in conversation | **Do not write it into the inventory**; tell them to put it in an ignored local file or a secret manager, and confirm that file is covered by the ignore rules |
| The file that will hold the key does not exist yet | Suggest adding it to the ignore rules in advance (see `include-list-rules.md`) |
| The key already exists in some file | Record only the **file name** and the readiness state, never the contents |

**The inventory itself MUST be safe to commit to version control.** That is why it has five
columns and no value column.

---

## Items that are not ready do not block

An item marked not-yet or pending **does not block this skill from completing**.

The inventory exists to **tell the user what is missing**, not to withhold progress until
everything is gathered. Treating "every account must be opened first" as a precondition
stalls the whole preparation stage behind the slowest registration flow.

**But the report MUST list** the items that are not ready and their impact — "does not block"
is not "does not matter".

---

## Organise it in sections

Group the inventory by nature rather than laying out one flat table:

```markdown
## 1. Toolchain (no account needed)
## 2. Services needing an account and a key
## 3. Test environment
## 4. Pending decisions
## 5. Judged not applicable
```

**Section 5 MUST NOT be dropped.** Writing "browser testing tool — this project has no web
surface, not applicable" is far more useful than letting it vanish from the inventory; the
latter leaves people repeatedly asking "do we need to configure this?"

---

## Section 4: pending decisions

Gather every pending item here, each with:

| Column | Note |
|---|---|
| The question | Specific enough to answer directly |
| The impact | What happens if it stays undecided |
| My recommendation | **Give a recommendation, but do not make the decision** |

And state explicitly **whether these items block the current stage** — usually they do not,
and saying so lets the user proceed with confidence.
