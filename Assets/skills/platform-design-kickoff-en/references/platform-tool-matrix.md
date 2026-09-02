# Target Platform x Design Tool x Export Format

## When to read this

When choosing a design tool. **Settle the platform first, then the tool** — reverse the
order and you end up applying the web toolkit to a native project.

## What is preserved is the logic, not the tool name

From the frozen template:

> If you use a different design tool, substitute that tool's equivalent artifacts for the
> names, export formats and paths below, **but preserve the logic of design source of
> truth -> reference samples -> spec injection**.

**That logic is the invariant**:

| Link | Invariant | Variable |
|---|---|---|
| Design source of truth | There is exactly one `DESIGN.md` | Which tool generates it |
| Reference samples | They land in `design-reference/<source>-export/` | Which format is exported |
| Spec injection | Stage 5.2 injects into the constitution and reruns affected features | — |

**Any tool that can produce those three is a valid substitute.**

## Six platform families

| Platform | Tools (suggestions, not the only option) | Export format | Layout unit |
|---|---|---|---|
| **Web** | Google Stitch, Figma, Penpot | HTML/CSS, Figma file, SVG | Breakpoints (px / rem) |
| **Mobile native** | Figma (with iOS/Android kits), Sketch | Figma file, slices + redlines | **Size class / dp**, not breakpoints |
| **Desktop** | Figma, Penpot with a platform control kit | As above | Window size ranges + minimum size |
| **CLI / TUI** | No graphical tool — write an **interaction script** | Markdown interaction flow + sample output | Terminal columns (80 / 120) |
| **SDK / library** | No graphical tool — write an **API feel document** | Markdown: typical call sequences + error shapes | Not applicable |
| **Hardware / embedded** | Figma (panel layout), vendor HMI tools | Panel drawings + state machine | Physical dimensions / button count |

**Stitch appears only in the Web row, beside two others.** It is an option, not a default.

## A note on the last three families

CLI, SDK and hardware **have no graphical interface, yet may still fall in scope** — the
criterion is whether there is an interaction contract or a developer experience worth
designing.

| Situation | Applies? |
|---|:---:|
| The CLI has an interactive wizard (multi-step, can go back) | Yes — write an interaction script |
| The CLI is only `tool input.csv > out.md` | No |
| The SDK's API feel needs work (naming, error shapes, defaults) | Yes — write an API feel document |
| The SDK is a bag of internal helper functions | No |

**"No GUI" does not imply "does not apply."** The criterion is the contract, not pixels.

## State this once the tool is chosen

| Item | Requirement |
|---|---|
| Why this one | One sentence, grounded in this project's platform and constraints |
| Why not the alternative | Name at least one and say why it lost |
| If no tool is available | Still produce `DESIGN.md` (tokens + component specs), **labelled "no reference exports, design-reference/ empty"** |

That last row is the fallback path. Taking it obliges you to label it — **silent
degradation is not permitted**.
