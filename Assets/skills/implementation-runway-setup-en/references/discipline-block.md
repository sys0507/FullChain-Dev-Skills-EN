# Sub-item C: the implementation discipline block

## When to read this

Before appending the discipline block to the project constitution. **This is the only one of
the four sub-items that is not idempotent.**

---

## 1. Why this block is needed

An implementation-phase agent does not read the project constitution on its own — it reads
`tasks.md`. However many principles the constitution states, without one explicit
instruction to read the constitution before executing tasks, those principles do not exist
during implementation.

This block is the **joint**: it hands the discipline agreed at the specification stage over
to the implementation stage.

---

## 2. The discipline block text

```markdown
### Implementation Discipline (for downstream handoff)

- Before executing any tasks.md, ALWAYS read the project constitution FIRST.
- Always follow TDD: Red (failing test) -> Green (minimum code) -> Refactor.
- Always update the tasks.md checkbox after EACH task completes.
- After each task: commit, then STOP and wait for "next".
- All interface tasks: when a design system applies, MUST read the project's
  design source of truth and the matched reference sample BEFORE writing any
  component code.
```

### 2.1 Why it is written generically

The original version named a particular workflow tool in the heading and the body. **The
generic version hardcodes no tool name**:

| Original | Generalised | Reason |
|---|---|---|
| `(for Superpowers handoff)` | `(for downstream handoff)` | The project may use a different tool, or none |
| A specific TDD skill name | `Always follow TDD: Red -> Green -> Refactor` | The discipline itself is tool-independent |
| `root DESIGN.md` plus a specific sample directory variable | `the project's design source of truth and the matched reference sample` | Different projects name their design source of truth differently |

**Generalising replaces only tool names and path variables; not one discipline item is
dropped.** Where a project does use a particular tool, its own constitution may replace the
generic wording with the specific name — that is the project's choice, not this skill's
default.

### 2.2 The last item is conditional

The last item, "All interface tasks", **carries its own condition** (`when a design system
applies`). Where a project has no design system, it simply does not fire.

**MUST NOT delete it for being temporarily inapplicable** — once deleted, nobody will
remember to restore it when a design system is introduced later. A project-side note may be
added after it, stating that it is currently inactive and why.

---

## 3. Where to insert it

**Insert before the version metadata line**, not at the end of the file.

The version metadata line is usually the constitution's last line, of the form:

```
**Version**: X.Y.Z | **Ratified**: ... | **Last Amended**: ...
```

It MUST stay last — it is the whole document's signature line. The discipline block goes
before it.

| Situation | Handling |
|---|---|
| A version metadata line is found | Insert **before** it |
| **No version metadata line** | Append at the end, and **report the placement degradation explicitly** |

"Report the placement degradation explicitly" means telling the user "your constitution has
no version line, so I put the discipline block at the end" — rather than placing it silently
and moving on.

---

## 4. Idempotence detection algorithm

**Every write MUST sit after the detection's negative branch.** This is a structural
requirement.

### 4.1 The detection marker

Use the heading line as the marker:

```
### Implementation Discipline
```

**Match only the heading prefix, never the qualifier in parentheses** — the qualifier may
have been changed by the project to a specific tool name (see 2.1), and matching the full
heading would miss it and append a duplicate.

### 4.2 Three-state decision

| Detection result | Action |
|---|---|
| **Absent** | Locate the version line and insert before it |
| **Present and identical** | Skip; report "already in place" |
| **Present but different** | **Do not rewrite it automatically**; report the difference and ask the user to adjudicate |

The third case calls for the most restraint. Different content may mean:

- The project changed it themselves (swapping the generic wording for a specific tool name)
- The user added items by hand
- It is text from an earlier version

**None of those should be overwritten automatically.**

### 4.3 How to compare content

**Normalise before comparing**:

- Strip inline markdown emphasis markers
- Ignore trailing whitespace and differences in blank-line count
- Ignore the qualifier inside the heading's parentheses

Reason: none of these differences changes the discipline's meaning, and a byte-for-byte
comparison would report "actually the same" as "content differs", interrupting the user for
nothing.

---

## 5. Acceptance

| Check | Expectation |
|---|---|
| After the first run | The discipline block appears exactly once, before the version metadata line |
| **After a repeat run** | It **still appears exactly once**; the rest of the file is byte-identical |
| Running when the content differs | The file is **not modified**; the report explains the difference |
| Running with no constitution file | No file is created; the report explains why it was skipped |

The second row is this sub-item's core acceptance criterion: **rerun safety**.
