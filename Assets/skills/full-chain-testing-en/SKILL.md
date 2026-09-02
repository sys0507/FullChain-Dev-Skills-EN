---
name: full-chain-testing-en
description: Excavate and protect a newly reachable P0 cross-feature journey using static structure, runtime traces, and spec contracts. Bring up the real system, stub only external boundaries, validate multi-feature and asynchronous paths without fixed sleeps, archive journey-level evidence, and backfill lower layers when a defect first appears here. Deliver isolated changes for human review. Use directly or when routed by test-routing-advisor-en; do not use for a single-feature seam.
license: MIT
metadata:
  version: "1.0"
  lang: en
  kind: process-executor
  stage: "9.2"
  standalone: true
  produces:
    - "end-to-end test code"
    - "path-inventory.json"
    - "evidence archive"
  requires:
    - name: "several closed-out features"
      level: required
      fallback: "Stop - a cross-feature journey needs several features to exist first"
    - name: "project manifest files"
      level: required
      fallback: "Stop - the stack cannot be identified and the system cannot be orchestrated"
    - name: "routing decision report"
      level: orchestration
      fallback: "Ask the user which journey to take"
    - name: "runtime tracing capability"
      level: optional
      fallback: "Excavate from the static graph and spec contracts only, and label which paths went un-excavated"
---

# full-chain-testing-en · Complete Functional Chain Test Executor

## What This Skill Solves

The first three quadrants each focus on a **given, clearly scoped** subject under test: `backend-testing-en` validates the backend's real behavior, `frontend-testing-en` validates the frontend's rendering and interaction contracts, `fullstack-slice-testing-en` within a **single feature** brings up a single consumer↔provider slice in real form for reconciliation. Their common prerequisite is — **the subject under test is known, with boundaries defined by that feature**.

**The complete functional chain is the fourth quadrant. It solves a different class of problem: when multiple features are successively completed, a "user going from feature A to feature B to feature C" end-to-end journey will [become traversable for the first time]. This journey crosses multiple features, often contains non-UI jumps (scheduled task triggers, async messages, cross-channel delivery), and no single quadrant has ever watched whether the entire journey can actually connect end-to-end.**
This quadrant is for weaving an end-to-end safety net for this class of **critical journeys across multiple features**.

> **The essence in one sentence**: Complete functional chain = **first excavate cross-feature end-to-end paths from system structure (path inventory) → select P0 critical journeys → validate end-to-end, as a safety net.** Covers chains that **cross multiple features** and **include non-UI jumps** (scheduled tasks / async / cross-channel). **Single-feature single slices belong to the third quadrant "partial frontend-backend," not here.**

Follows the `testing-system-blueprint-en` (reference by name as needed): risk-tiered ordering, traceable IDs, release gates, three-layer cadence (this quadrant lands at L3).

---

## Two Most Distinctive Points (Must Understand First — They Determine the Fundamental Differences from the First Three Quadrants)

### Distinctive Point ①: The Subject Under Test Must First Be [Excavated]

The subjects under test in the first three quadrants are **given** ("test this backend," "test this frontend," "test this slice"). This quadrant is not — **no one will directly tell you "how many complete chains there are."** A journey spanning multiple features is scattered across multiple features' code, configuration, and contracts; **as a whole it has never been explicitly declared anywhere**. So the first and most core task in this quadrant is **excavating paths from the system structure** (path inventory). The methodology for path excavation is shown below in the ⭐ Three-Source Model — this is the most core and empirically validated part of this skill.

### Distinctive Point ②: It Is the "Safety Net Layer" — Few and Precise, Only Covering P0

Chain E2E is slow and fragile (blueprint § three L3). This quadrant **does not chase coverage rate** — it only weaves a net for **the highest-risk P0 critical journeys among the excavated paths** — "the entire chain actually connects," which L1/L2/the first three quadrants cannot cover, is the only reason it exists. This gives rise to one iron rule:

> **If a bug is [first] discovered at this layer (chain E2E), that is a signal of lower-layer coverage gaps — it means it should have been caught more cheaply at backend-only / frontend-only / partial frontend-backend, but was missed. In addition to making the chain green, [back-fill the lower layer] — add it as a regression in the quadrant where it should have been caught, so it gets caught at the cheaper layer next time.** The chain layer is "patching the net," not "the trash can where bugs are first discovered" (blueprint § three L3 mindset).

---

## Two Absolute Constraints (Read First — Apply Throughout)

1. **stack-agnostic**: All capabilities are expressed using "**capability description + per-stack/scenario instantiation lookup**" exclusively — never hardcode any tool as a dependency or the only answer. The **glia / OpenLore / Pathfinder / Tracetest / docker-compose / OpenTelemetry / AppMap / eBPF / gstack `/qa`** and other tools appearing in this document and in `references/gaps.md` are **all just "instance examples for a certain stack/scenario" — never the only solution, let alone hard dependencies**. If an environment doesn't have a certain tool, fall back to the generic equivalent for that capability.
   - **Special note (glia)**: glia has a **non-commercial license** — it can be mentioned as an example of "static code graph" capability, but **commercial products cannot use it**; more importantly **this skill is not bound to any single tool** — the static graph capability can be instantiated by any equivalent (OpenLore-style or that stack's built-in call graph / dependency analysis).
   - **gstack `/qa` is not a hard dependency** — it is just one instance of "diff-aware E2E" in a certain environment; without it, fall back to general-purpose E2E. This skill does not write any gstack installation steps.
2. **project-agnostic**: No business-specific terms appear here, and no specific framework or protocol is assumed. Everything **project-specific** — which specific crons / scheduled tasks exist, whether a jump is streaming (SSE / WebSocket / long-polling), specific interface shapes, token / auth / one-time login mechanism, what cross-channel uses, whether the project has gstack at all — is **always read at runtime, never written into the skill, never pre-assumed**. Always written as **conditionals**: "**if the journey contains scheduled triggers, use fake clock / manual trigger** …", "**if a certain jump is streaming, then** …".

---

## ⭐ Path Excavation = Three-Source Model (The Most Core and Empirically Validated Part of This Skill)

Path excavation cannot rely on a single information source — **no single source can excavate the entire graph**. The core methodology of this quadrant is **three-source complementarity**: each source **reliably excavates only one class of edges** — combining them is what lets you piece together a complete cross-feature path. This conclusion was validated by two real projects plus controlled experiments.

```
Static code graph (glia / OpenLore-style, instantiated by stack)   → Reliably excavates: backend routes / resources / call graphs / shared dependencies
                                                                       (edges with clear syntactic fingerprints)
Runtime trace (distributed tracing / AppMap-style)                 → Under modern frontend stacks, [the only reliable way] to complement:
                                                                       FE↔BE bridge edges + decoupled edges (HTTP / cron / async / cross-channel)
Spec contracts (project's own cross-feature contract table / AC)   → Covers semantics + when code is not yet landed, the [only source of truth]
```

**Each source's boundaries, capabilities, and known failure modes (written into the skill as "known failure modes" so they aren't stepped on again):**

### Source A · Static Code Graph (Instantiated by Stack; glia / OpenLore Are Examples, Not Dependencies)

**Can excavate**: Backend routes, resources, call graphs, shared dependencies — any **edge with a clear syntactic fingerprint** (one function explicitly calls another, one route explicitly mounts a handler, multiple features explicitly import the same shared module) is excavated accurately by the static graph.

**Known failure modes (validated by two real projects + controlled experiments — treat as established facts):**
- **Static graph only excavates "half the graph"** — only covers edges with syntactically clear fingerprints.
- **Cannot excavate "cross-service request edges wrapped by frameworks"**: Modern frontends **basically don't write bare `fetch`** — as long as requests go through **framework wrapping** (AI-SDK / custom client / template URL concatenation etc.), **the FE↔BE bridge edge breaks in the static graph**. This has been **reproduced independently in two separate projects**, and a **controlled experiment proved the resolver itself wasn't broken** (restoring the same call to a bare fetch made it excavatable) — meaning this is not a tool bug but a **structural boundary where "framework wrapping consumed the syntactic fingerprint."**
  → **Conclusion: FE↔BE bridge edges must be supplemented via source B (runtime trace) or source C (spec contracts) — don't count on the static graph.**
- **Decoupled edges like cron / queue**: The static resolver's corpus is sparse (corpus-sparse) for these — hit rate is not optimistic.
  → **Prioritize source B (trace) / source C (spec) to supplement; don't fight the static graph.**

### Source B · Runtime Trace (Distributed Tracing / AppMap Are Examples, Not Dependencies)

**The only reliable way to supplement the two classes of edges the static graph cannot excavate**: ① **FE↔BE bridge edges** (when framework wrapping consumes the syntactic fingerprint, only by actually running once and looking at the trace can you know which backend endpoint a given frontend interaction hit); ② **decoupled edges** (HTTP / cron / async messages / cross-channel delivery — these edges in code are "fire and forget, the other end starts fresh"; they can't be connected statically, but trace can string them together via the same trace-id / correlation-id).

**Instantiation lookup (not the only solution)**: Distributed tracing (OpenTelemetry-style) / execution trace recording (AppMap-style) / kernel-level observation (eBPF-style) — read and select based on the stack and observability infrastructure available; if the environment has none, fall back to "add temporary log instrumentation + manually run once to string edges together."

### Source C · Spec Contracts (Project's Own Cross-Feature Contract Table / AC — No Tool Dependency)

**Covers two things**: ① **Semantics** — a trace can tell you "A truly called B afterward," but **why it called, which business journey this edge belongs to, what the P0 acceptance criteria of that journey are** — those must be read from the project's own spec / cross-feature contract table / AC. ② **The only source of truth when code is not yet landed** — see the timing section below.

**Known failure modes**: **When code is not yet landed (the chain only exists in the spec)**, static tools and traces are both blind (no code to analyze, no runtime to trace). → **Spec contracts are then the only source of truth** — you can still "excavate candidate paths + write RED E2E" based on them (assertions written and tagged with traceability, but red / pending because the code isn't there yet — can't run green).

> **Discipline for using all three sources together**: Use source A to excavate the backend skeleton (half the graph), use source B to fill in the FE↔BE bridge edges and decoupled edges to complete the full graph, and use source C throughout to cover semantics, define P0, and serve as the only source of truth when code is not yet landed. **A complete cross-feature path cannot be pieced together if any one source is absent.**

---

## Workflow (Six-Step Closed Loop)

> The skeleton is the same structure as the first three quadrants; **differences are concentrated in step 0 "excavate paths" (distinctive point ①) and the "safety net layer" mindset (distinctive point ②)**.

### Step 0 · Excavate Paths (Three Sources) + Select P0

1. **Three-source path excavation** (see ⭐ Three-Source Model above): source A excavates backend skeleton → source B fills in FE↔BE bridge edges + decoupled edges → source C covers semantics. Output a **cross-feature path inventory**: each path records **which features it traverses and which jumps it contains** (UI-traversable segments / scheduled / async / cross-channel).
2. **Select P0 critical journeys** (P0 = the **highest tier** in the four-tier risk/priority scale P0–P3, where P0 is highest and P3 is lowest; complete criteria in blueprint `risk-tiers.md`): per blueprint § one risk tiers, **select only P0** from the path inventory (data corruption / authorization bypass / financial amount miscalculation / core main-flow unavailable / irreversible outbound delivery — journeys that are "irreversible if it goes wrong + high frequency"). **The safety net is few and precise — don't weave an E2E for every path in the inventory.**
3. **Confirm "cross-feature"**: Each selected journey must **truly cross multiple features**. If one is actually within a single feature (even if it has both frontend and backend), it belongs to the third quadrant "partial frontend-backend" — **remove it from this quadrant** and return it to `fullstack-slice-testing-en`.

> If no clear cross-feature paths can be excavated, or no source at all is available (stack not analyzable + no observability + no spec), stop and ask — don't assume.

### Step 1 · Full-System Orchestration + External Boundary Stubs (This Quadrant's "Lay the Foundation")

Chain E2E needs to bring up **all features the entire journey traverses + the middleware they depend on** together and reproducibly — a larger scope than the third quadrant's "bring up two sides." This step does only one thing: **make the entire P0 journey bring up in real form, one-command, reproducibly, with health checks passing**.

- **Everything internal is real**: All internal features / services / middleware (DB / cache / queue / scheduler …, **which ones exist, read at runtime**) that the journey traverses must participate in real form — this is precisely the value of chain testing; **it is forbidden to stub out the internal features being tested** (stubbing them out means degrading and losing value — see guardrails).
- **Only stub external third-party boundaries**: Only stub out **third-party dependencies that are outside the system boundary, uncontrollable, expensive, or slow** — **typically LLMs / push channels / payments**. Which are "external boundaries" must be read at runtime — don't pre-assume.
- Reuse **existing orchestration definitions in the project** (compose / startup scripts / CI service sections — read at runtime); only instantiate minimal orchestration by stack if none exists.
- **Smoke-test to confirm the foundation is usable**: After bringing up the stack, first push through one simple real journey to prove the entire chain can move, then proceed to layered assertions. **Before this step is green, don't write any chain assertions.**

### Step 2 · Conditional Hit (What Jump Types Each P0 Journey Contains)

For each selected journey, **confirm at runtime which jump types it actually contains** to determine how to drive and assert downstream:

| Jump type | Meaning | Landing approach (selected in steps 3/4) |
|---|---|---|
| **UI-traversable segment** | The journey has a segment where a user truly clicks / inputs in the interface | Can use diff-aware E2E (gstack `/qa` is one) or general-purpose E2E driver; **not a dependency, fall back if unavailable** |
| **Scheduled trigger** | Journey advances via cron / scheduler (non-UI jump) | **Orchestration-driven**: control time with fake clock / manually trigger the scheduled task — **never truly wait until the clock time** |
| **Async** | Journey advances via message / queue / background task | **Orchestration-driven** + poll-retry for eventual state (bounded retries — no fixed sleep) |
| **Cross-channel** | Journey crosses in/outbound channels (e.g., through a third-party channel and back) | **Orchestration-driven** + observe delivery at the external boundary stub, assert the real landing point |

> **"Containing non-UI jumps" is what distinguishes this quadrant from pure frontend E2E**: A complete chain is often "user clicks once → scheduled task generates overnight → async push to a channel → user receives on the other end." **Non-UI jumps use orchestration-driven** (manual trigger / fake clock / observe async eventual state) — **cannot wait idly in the UI**.

### Step 3 · Two-Layer Landing

For each P0 journey, land in two layers — "blackbox traversal first, then structured assertions":

1. **First layer · Blackbox traversal**: On the already-brought-up full-system real stack, **run the entire journey end-to-end**, confirming "A→B→C actually connects."
   - **UI-traversable segments**: If a diff-aware E2E tool **already exists** in the environment (gstack `/qa` is one), use it preferentially (focuses on change-related journeys, saves time); **otherwise fall back to general-purpose E2E** (Playwright / Cypress or the stack equivalent). This skill does not write installation steps for these.
   - **Non-UI jumps**: Use **orchestration-driven** to push the journey forward (manually trigger scheduled task / advance time with fake clock / send a real message / observe delivery at the stub boundary).
   - Again: E2E tools **only probe running localhost — they don't bring up the stack** — so **step 1 must have already been completed**.
2. **Second layer · Structured chain assertions**: Assert at each **critical handoff point** along the journey (A's output truly became B's input, B's artifact truly triggered C, cross-channel delivery truly landed at the correct endpoint, the final state was truly reached and is consistent). Blackbox traversal only proves "it works"; structured assertions prove "**each handoff point matches one by one**" — that is what solidifies the safety net into regressions.

> See `references/gaps.md` for specific tools and assertion patterns; take the row corresponding to the stack / jump types identified while excavating paths in Step 0.

### Step 4 · RED→GREEN (No sleep) + Data Isolation

1. **Data isolation first**: Chain E2E runs on the full-system real stack traversing data across multiple features — **seed / teardown fixtures are required** to ensure the entire journey's data is controlled, non-polluting, and repeatable (start with known data → run entire journey → clean up).
2. **Iron rules for time control and waiting (most common pitfall — guardrail-level)**:
   - **Forbid `sleep` / `waitForTimeout` pretending to be ready or pretending it's time** — when the chain contains scheduled/async jumps, fixed sleep is slow, fragile, and deceptive.
   - **Scheduled jumps**: Use **fake clock to control time** or **manually trigger the scheduled task** to "fast-forward" the journey to the target time.
   - **Async / cross-channel jumps**: Use **poll-retry for eventual state** (bounded retry polling until the target state is reached) — not sleeping a fixed number of seconds.
3. **RED**: First write failing chain assertions, confirm they are red **because of real chain defects** (a handoff point doesn't align, a decoupled edge isn't connected, the final state wasn't reached) — not because the stack didn't come up / the test is written incorrectly / insufficient sleep. **Red for a good reason**, then proceed.
4. **GREEN**: Make assertions go green.
   - If red exposes a **real chain bug** — **HALT, don't modify product code yourself** (see guardrails), return to `superpowers:test-driven-development` / `superpowers:systematic-debugging` for fix, then return to this skill to solidify the regression.
   - **And** (distinctive point ②): **Judge whether this bug was [first] discovered at the chain layer** — if so, it means lower layers had coverage gaps; **simultaneously prompt to back-fill the lower layer** (add it as a regression in the backend-only / frontend-only / partial frontend-backend quadrant, so it gets caught at the cheaper layer next time).
5. **Assertions must not be weakened**: It is forbidden to relax assertions to make things go green (delete handoff-point assertions, broaden final-state validation, comment out timing assertions, secretly add back the forbidden sleep).

### Step 5 · Archive (Release Gate, Journey-Level Traceability) + Teardown + Isolated Changes for Human Review

For each newly added chain safety net test:

- Per `testing-system-blueprint-en` **risk tiers** into release gates — **P0 critical journeys are hard-blocked in release gates** (chain broken = core business journey unavailable). The safety net only covers P0, so virtually everything selected is a hard release gate item.
- Attach **journey-level traceable IDs** — associated with the **multiple features / multiple ACs this journey traverses + which jump types it contains** (coarser traceability granularity than single-feature, but must mechanically answer "was this cross-feature journey tested").
- Aligned with **three-layer cadence**: chain E2E belongs to blueprint **L3** (slowest, most fragile) — put only the one thing L1/L2/first-three-quadrants can't cover ("confirm the entire chain actually connects") here; **don't stuff unit-level / single-feature-level assertions into chain E2E**.
- **Teardown**: Both CI and local cadences are **bring up full-system stack → run journey → teardown stack**; clean up the real stack and data together after testing.
- Keep supplemental tests in an **isolated branch or change set for human review**; the upper-level wrap-up stage decides merge versus PR. The delivery note lists the path inventory summary, selected P0 journeys and rationale, jump types, excavation sources, stubbed external boundaries, and any lower-layer backfill.

---

## Timing Guidance (Written Honestly into the Skill — Don't Pretend It Can Run Early)

full-chain naturally **requires the most code to run** — it needs to bring up all features that the entire cross-feature journey traverses. Therefore it is **the last quadrant to actually be executable**: must wait until the features the journey traverses have all landed.

- **When code is not yet landed** (the chain only exists in the spec): source A / source B are both blind (no code to analyze, no runtime to trace); **source C (spec contracts) is the only source of truth**. **What can and should be done at this stage**: use spec to excavate **candidate paths** + write **RED E2E** (assertions written and tagged with traceability, but red / pending because code isn't there — can't run green).
- **The methodology can be established before the code**: This skill is a **reusable asset** — the three-source model for excavating paths, the criteria for selecting P0 for the safety net, the orchestration and time-control discipline, can all be thought through and candidate paths + RED E2E landed before the code is complete. **Real validation (running green) follows the code.**

---

## Key Distinctions from the First Three Quadrants (Must Be Clear)

| | First three quadrants (backend / frontend / partial frontend-backend) | This quadrant (complete functional chain) |
|---|---|---|
| Subject under test | **Given** (boundaries defined by that feature) | **Must first be excavated from three sources** (distinctive point ①) |
| Scope | Single feature (first two: single side; third: single slice within single feature) | **Cross multiple features + contains non-UI jumps** (scheduled / async / cross-channel) |
| Layer mindset | Each covers its own reality / seam | **Safety net layer** — few and precise, only covers P0; **bug first discovered here = lower layer gap, back-fill lower layer** (distinctive point ②) |
| Stack bring-up scope | One side / single feature both sides | **All features + middleware the entire journey traverses** — only stub external boundaries |
| Execution timing | Can run when feature wraps up | **Last** to run; when code is not yet landed can only excavate candidate paths + write RED E2E |

---

## Self-Healing Guardrails (Must Not Be Crossed)

The supplemental test process allows bounded automated iteration (excavate paths → bring up stack → RED → GREEN → teardown), but is constrained by the following guardrails (inherited from the blueprint):

- **Only write tests / orchestration config, don't change product code** — this is the default action. This skill is responsible for excavating paths, bringing up the full-system stack, configuring orchestration, and writing chain assertions — **not modifying business implementation**.
- **Assertions must not be weakened** — it is forbidden to relax assertions to make things go green (delete handoff-point assertions, broaden final-state validation, comment out timing assertions, shrink the contract comparison field set).
- **Fake fixes are forbidden** — it is not permitted to fake a pass using `skip`, **fixed `sleep` / `waitForTimeout` pretending to be ready or pretending it's time**, **secretly stubbing out the internal features being tested**, or bringing up fake services pretending to be the real stack. **Once this quadrant stubs out the internal features being tested, it degrades to a lower layer and loses all its value** (stubs are only permitted on external third-party boundaries).
- **Bounded retry escalation** — chain E2E is naturally fragile (port contention, health check jitter, async eventual state not yet reached, cross-channel delay); automated iteration has an upper limit; reaching it means stop and escalate to a human — **never use "one more run will fix it" or "sleep a few more seconds" to mask real chain instability**.
- **Isolated changes + human review** — keep the path inventory, orchestration config, and chain safety-net tests in an isolated branch or change set for review; the upper-level wrap-up stage decides merge versus PR.
- **Discovering a real bug requires HALT, return to superpowers for fix** — this skill **does not modify product code itself**. When RED exposes a real chain defect, **stop**, return to `superpowers:test-driven-development` / `superpowers:systematic-debugging` for a fix cycle, then return to this skill to solidify the regression. **And: if this bug was first discovered at the chain layer, simultaneously prompt to back-fill the lower layer** (distinctive point ②) — add it as a regression in the quadrant where it should have been caught cheaply.

The purpose of these guardrails: allow the chain safety net to be woven automatically, but block any shortcut of "stubbing back the internal features being tested," "pretending to pass without the real stack up," "using sleep to mask timing," or "crossing the line to modify product code."

---

## Relationship to Upstream and Downstream

- Upstream: `test-routing-advisor-en` calls this skill when it determines "complete functional chain" (can also be triggered directly by the user). **Killer integration**: the router derives from the dependency graph that "after completing a certain feature, a cross-feature journey A→B→C becomes traversable for the first time" and prompts "this chain can now be end-to-end tested" — this skill is exactly the executor that receives this prompt, excavates that journey into substance, and weaves it into a safety net.
- Blueprint: all post-excavation tiering / traceability / release gates / cadence follow `testing-system-blueprint-en` (reference by name; its content is not replicated here); this quadrant lands at **L3**.
- Siblings: `backend-testing-en` (backend-only) / `frontend-testing-en` (frontend-only) / `fullstack-slice-testing-en` (partial frontend-backend, single slice within single feature) — these three are "lower layers"; **when a bug first appears in this quadrant, the back-fill goes to them**.
- For reference (**not dependencies**): **Pathfinder**'s journey→E2E skeleton generation approach, **Tracetest**'s trace→assertion approach — referenced as instances of "how to generate E2E from excavated paths / how to convert traces into chain assertions" — **not bound to them; if the environment doesn't have them, use generic equivalents**.
- Methodology reuse: Fix and debug of discovered real chain defects reuses `superpowers:test-driven-development` and `superpowers:systematic-debugging` (this skill HALTs and returns to them).
- Boundary: **Single-feature single slices** belong to the third quadrant `fullstack-slice-testing-en`, not here.

---

## Bundled Implementation: `scripts/` Path Excavation + Visualization Tools

This skill comes with a **clean-room in-house** reference implementation (MIT, owned by the user) that makes the flow "excavate paths → merge three sources → derive journeys → generate RED E2E → visualize" into runnable tools. stack-agnostic / project-agnostic: processes after identifying stack by reading pyproject/package.json, without hardcoding any business names. **Anti-hallucination iron rule**: every edge has provenance (`file:line_number` or `trace span`); edges that cannot cite evidence are only marked `candidate` — never pretend they are confirmed.

Central artifact `path-inventory.json` (`scripts/pathinv.py` defines schema + validation gate):
features / nodes / edges (each with source+status+provenance) / journeys.

| File | Knife | Language | Purpose |
|------|----|------|------|
| `scripts/pathinv.py` | Shared | Python | path-inventory schema + status upgrade + `validate()` anti-hallucination gate |
| `scripts/knife1_spec.py` | Knife 1 Source C | Python | Parse spec-kit `tasks.md` `[dependency] Fn` / `[BE/FE/INT]` / `[FR source]` → cross-feature candidate edges (candidate, evidence=file:line_number) |
| `scripts/knife2_static.py` | Knife 2 Source A | Python | AST (Python FastAPI decorators/import/redis key/scheduler) + regex (Next route/import/fetch/redis) → code-confirmed; **framework-wrapped FE→BE (useObject/useChat) honestly marked candidate** |
| `scripts/knife3_trace.py` | Knife 3 Source B | Python | Read correlation-id structured event log → trace-confirmed edges (evidence=span/event) |
| `scripts/knife4_merge.py` | Knife 4 | Python | Three-source merge deduplication, status upgrade, mark spec-only gaps, derive journeys, heuristically mark P0 (noted "needs human confirmation") |
| `scripts/knife5_e2e.py` | Knife 5 | Python | Select one journey → generate pytest/Playwright RED E2E skeleton (condition-based wait, no sleep) |
| `scripts/knife6_viewer.html` | Knife 6 | HTML/JS | Single-file self-contained (pure DOM+CSS, no heavy dependencies); **"user journey list" for humans** — each journey has a one-sentence summary + step flow chips, color-coded by status (candidate=dashed gray / code=blue / trace=green), click step to see provenance details; technical scatter plot demoted to "view technical details" collapsible |
| `scripts/view.sh` | One-click open | bash | `bash view.sh demo` / `bash view.sh alpha` / `bash view.sh out/xxx.json` → automatically starts local server + opens browser + data already loaded, **no drag-and-drop needed** |
| `scripts/run_pipeline.sh` | Orchestration | bash | Start demo → inject cid, run journey → knife2+knife3 → knife4 merge → knife5 skeleton, output to `scripts/out/` |
| `demo-app/` | Validation target | Python(stdlib)+HTML | Small but complete multi-feature demo (A frontend button → B API writes kv+async → C cron reads kv+push), contains all edge types, actually runnable |

### Usage Flow (Trigger Timing + Automatic Output + Viewing)

1. **Trigger timing** — **Not triggered "when all features are done."** Triggered when **a cross-feature end-to-end journey becomes traversable for the first time** (per journey, not at project end). `test-routing-advisor-en`'s "killer feature" is proactively discovering this "first traversal" from the dependency graph and prompting — this is what people most easily forget.
2. **Automatic output** — After triggering, run spec parsing → static scan → trace collection → three-source merge per this skill's steps, **automatically produce `path-inventory.json`**. For the demo, `bash scripts/run_pipeline.sh` runs it end-to-end; for real projects, Claude reads the stack per skill, instantiates per stack, and produces equivalent output to `scripts/out/`.
3. **One-click view** — `bash scripts/view.sh demo` (or `alpha` / any inventory path) → automatically starts local server + opens browser + **data is already loaded**, goes directly to the cool "user journey list" page, **no drag-and-drop needed**. (Double-clicking `knife6_viewer.html` and dragging the json into the page drop zone is the `file://` fallback method; `view.sh` is recommended.)

Single-tool usage: run `knife1_spec.py <specs/>` against the spec tree, run `knife2_static.py <repo/>` against real code, then `knife4_merge.py` to merge, `knife4b_narrate.py` to add narration — this sequence is essentially the breakdown of step 2.

## Upstream Artifacts

| Artifact | Level | When missing |
|---|:---:|---|
| Several closed-out features | **required** | Stop - a cross-feature journey needs several features first |
| Project manifest files | **required** | Stop - the stack cannot be identified |
| Routing decision report | orchestration | Ask the user which journey to take |
| Runtime tracing capability | optional | Excavate from the static graph and spec contracts only; label which paths went un-excavated |

## Downstream Consumers

| Consumer | What it reads |
|---|---|
| Branch close-out | The end-to-end safety net's result |
| The retrospective skill | Which defects surfaced first at this layer, and therefore which lower layer under-tested |

## Standalone Use

**What you provide**: several closed-out features and the project's dependency manifests;
use whichever of the three excavation sources you have.

**What you get**: an excavated inventory of cross-feature paths, a P0 journey selection, and
an end-to-end safety net.

**What you don't get**: it does not cover slices within a single feature (those belong to
the local seam skill); with fewer than three sources it labels which paths went
un-excavated; and **when a defect surfaces here first, that means a lower layer
under-tested it, so backfill that layer** rather than adding tests here.
