# Toolchain adaptation

## When to read this

When deciding whether to use an external spec toolchain or the built-in equivalent outputs.

---

## The core principle

> **Detect first, then use; on detection failure switch to built-in, do not force it.**

MUST NOT assume any external command exists. Command names change with tool versions, and
forcing produces "error -> try another spelling -> error again", wasting turns and polluting
the context.

---

## Detection

Detect in order; any hit is enough:

| # | What to detect | How it is judged |
|:-:|---|---|
| 1 | Whether the project contains that toolchain's configuration directory and templates | The directory exists and contains template files |
| 2 | Whether the corresponding command or skill is visible in the session | It appears in the available list |
| 3 | Whether the project documentation declares that toolchain is used | The context file or README mentions it |

**All three negative -> use the built-in equivalent outputs.**

The detection result **MUST be recorded**; it cannot be decided silently.

---

## Three ways it lands

### A: the external spec toolchain is available

Call its four-step commands. The output locations and naming follow that toolchain's
conventions, but **the four-step contracts, the four boundary classes, the five elements and
the granularity rules remain this skill's** — the toolchain provides the execution vehicle,
not the quality standard.

### B: a different spec tool is available

Map the four steps onto that tool's equivalent actions. **Write the mapping into the output**
so it can be traced later.

### C: no toolchain (built-in equivalent outputs)

Produce the three documents yourself, in a structure identical to A:

```
specs/00X-<slug>/
├── spec.md      (including the Clarifications record)
├── plan.md
└── tasks.md
```

**The output MUST be labelled**:

> "No external toolchain was used this time; the built-in equivalent outputs were produced.
> The four-step contracts, the four-class boundary scan, the five-element check and the
> granularity rules were all applied."

---

## Output equivalence

The three routes **MUST produce equivalent output**; only the generation process differs:

| Dimension | A / B | C |
|---|:---:|:---:|
| All three documents present | Yes | Yes |
| At least one question per boundary class | Yes | Yes |
| clarify has write-back locations | Yes | Yes |
| plan has all five elements | Yes | Yes |
| tasks have three labels, parallel groups and checkboxes | Yes | Yes |
| Triggering that toolchain's other integrations | Yes | **No** |

The last row is route C's real loss, and it **MUST be stated in the "what you don't get" part
of the Standalone Use section**. It MUST NOT be glossed over.

---

## When the command name is unstable

Where the toolchain is detected but the command name does not match expectations:

1. **Do not guess.** Do not brute-force through `/xxx.specify`, `/xxx-specify`, `/specify`
2. Read the toolchain's own documentation or command list and take the actual name
3. Still unobtainable -> switch to C, labelled "the toolchain exists but its command name
   could not be determined"

**Brute-forcing is explicitly forbidden** — it produces a stream of failed calls and may
mis-trigger a different command that happens to share a name.
