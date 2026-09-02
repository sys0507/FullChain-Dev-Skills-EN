# Sub-item A: include-list rules

## When to read this

When generating the file include list for isolated runs.

---

## Iron rule: list only files that exist

**Never create a credential file that does not exist in order to "complete" the list.**

Listing a non-existent `.env` does not mean "it will work once one appears". It means:

- The copy mechanism cannot find the source and either skips silently or errors
- Worse, someone reads the list, concludes the project needs a `.env`, and creates an empty one

---

## Two conditions, both required

The include list's copy mechanism usually requires **both**:

1. The file **matches a pattern in the list**
2. The file **is already covered by the ignore rules** (because the whole point is to carry
   across the files version control does not track)

**Listing a file that is not ignored is a no-op** — it is already in version control, so the
isolated environment gets it automatically.

### Verify before generating

For each candidate, verify in order:

```
Does the file actually exist? - No -> comment it out, noting "does not currently exist"
       | Yes
       v
Is it covered by the ignore rules? - No -> report: this file is not ignored,
       | Yes                              listing it will have no effect;
       v                                  ask whether it should be added to the ignore rules
   Write it into the list
```

---

## Candidate detection list

Ordered by how common they are. **These are candidates, not a list of files to create.**

| Category | Common files |
|---|---|
| Environment variables | `.env`, `.env.local`, `.env.development` |
| Credentials | `.credentials.yaml`, `.credentials.json`, `.netrc` |
| Local tool configuration | An editor's or agent's `settings.local.json` and similar |
| Package manager credentials | `.npmrc`, `.pypirc` |
| Service configuration | Service configuration files containing secrets |

**How to detect**: check the filesystem one by one. Do not infer what the project "should"
have.

---

## Non-existent candidates: comment them, do not delete them

```
# Permission approval record.
# (state why this file is worth carrying into the isolated environment)
.claude/settings.local.json

# --- Below: candidates to enable if they ever appear. None exists now, so all are commented ---
# Before enabling one, confirm the file actually exists and is covered by the ignore rules.
#
# .env
# .env.local
```

Commented lines serve two purposes:

1. They flag what to enable if it appears later
2. They **prove the candidate was considered and excluded**, rather than overlooked

---

## Ignore-rule check

Check the ignore rules while generating the list, focusing on two things:

| Check | Handling |
|---|---|
| Is every file in the list ignored | Not ignored -> **report and ask the user to confirm**; do not change the ignore rules unilaterally |
| Is the isolated workspace directory ignored | Not ignored -> suggest adding it, so the main checkout does not treat it as untracked files |

**Why not change the ignore rules unilaterally**: the ignore rules decide what enters version
control, which is a project-level decision. One wrong line can permanently keep a file that
should be committed out of the repository, and that is very hard to notice.

### Ignoring a sensitive file that does not exist yet

Where a class of configuration file **will certainly appear and will contain secrets** (an
MCP configuration, say), it is worth **adding it to the ignore rules now** — adding it after
it appears is too late, because it may already have been committed by accident on first
generation.

This is a suggestion, and still needs the user's confirmation.

---

## When the mechanism is unavailable

| Situation | Handling |
|---|---|
| The current tool has no include-list mechanism | Use the equivalent isolation configuration mechanism |
| None is available | **Skip sub-item A and say so**; do not emit a file that does nothing |

**MUST NOT** emit a list file when no mechanism exists to consume it — that leaves people
believing the configuration took effect.

---

## Self-check

- [ ] Every uncommented file in the list **actually exists**
- [ ] Each one **is covered by the ignore rules** (verified, not assumed)
- [ ] Non-existent candidates are commented with an explanation
- [ ] No new credential file was created
- [ ] Any change to the ignore rules was confirmed by the user
