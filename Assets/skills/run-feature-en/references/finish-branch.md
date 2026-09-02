# Branch close-out

## When to read this

Once every task in a feature is green and the code review has zero defects.

## Why this lives here rather than in its own skill

Close-out is in substance **one call to an existing capability plus four project
conventions**. As a separate skill it would overlap heavily with this skill's Step 5, and
with similar descriptions the odds of a mis-trigger outweigh the benefit.

---

## Delegate first

| Situation | Approach |
|---|---|
| External workflow tooling has a close-out capability | **Delegate to it**; the four conventions below still apply |
| Unavailable | Run the built-in flow below |

---

## 1. Merge or PR

| Condition | Choice |
|---|---|
| Solo project, no review requirement | Merge straight back to the main branch |
| There are collaborators or a review process | Open a PR |
| The change touches the project constitution, the contract matrix, or files shared across features | **Open a PR**, regardless of headcount |

The reason for the third: changes of that kind reach beyond a single feature, and even on a
solo project they are worth leaving a traceable review point for.

**When unsure, open a PR.** A merge is irreversible; a PR can still be merged.

---

## 2. Tagging

Convention: `v0.1.0-<id>-<feature-slug>`

| Requirement | Note |
|---|---|
| Annotated | Use an annotated tag stating what this feature delivered |
| After the merge | The tag points at the merged commit, not at the branch's last commit |
| One tag per feature | Do not bundle several together |

Where the project already has its own tag convention, **follow the project's** rather than
applying this one.

---

## 3. Update the progress and handoff records

| File | Update it to |
|---|---|
| Progress record | Current task cleared; completed lists everything; progress reads N/N; date updated |
| Handoff record | Status marked "completed and merged", naming the tag and listing the outputs |

The handoff record should also state **what is left for downstream**:

- Which open questions this feature closed
- Which it left open, and for whom
- The key constraints downstream must read

---

## 4. The spec directory is never deleted

`specs/<id>-<feature>/` is **frozen and kept permanently**.

Three reasons:

1. It is the next feature's context — the dependencies, the naming conventions and the
   reasoning behind the split all live there
2. It is the record for looking back — three months later, "why was it designed this way"
   is answered by the spec and the plan
3. It is the acceptance evidence — the tasks' checkboxes and output verifications record
   what was actually done

**When requirements change, open a new number**; do not edit a frozen directory.

---

## Close-out checklist

```
[ ] Every task's checkbox is ticked
[ ] Code review has zero defects (or defects were fixed and the re-review passed)
[ ] The final commit message contains Closes <id>-<feature>
[ ] The merge/PR decision is made, with a clear reason
[ ] The tag is applied and annotated
[ ] Progress record: N/N, date updated
[ ] Handoff record: status, tag, output list, open items
[ ] The specs directory has not been deleted or renamed
```

## Close-out report

Report, for this feature:

- The total task count and the distribution across labels
- How many defects the code review found and how they were resolved
- **Which steps took a built-in fallback** (if any) and what they left uncovered
- The open questions left behind and who picks them up
