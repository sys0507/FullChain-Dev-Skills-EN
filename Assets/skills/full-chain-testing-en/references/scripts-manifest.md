# `scripts/` file manifest

> Moved down out of SKILL.md. This is a **lookup table** — consult the row you need when you
> need it. It is not a decision point to read through on every invocation.

| File | Knife | Language | Purpose |
|------|----|------|------|
| `scripts/pathinv.py` | shared | Python | path-inventory schema, status promotion, and the `validate()` anti-fabrication gate |
| `scripts/knife1_spec.py` | knife 1, source C | Python | Parse spec-kit `tasks.md` for dependency and scope labels and FR sources, yielding cross-feature candidate edges (candidate status, evidence being file:line) |
| `scripts/knife2_static.py` | knife 2, source A | Python | AST analysis (Python framework decorators, imports, cache keys, schedulers) plus regex (frontend routes, imports, fetch calls) yielding code-confirmed edges; **framework-wrapped frontend-to-backend calls are honestly left as candidate** |
| `scripts/knife3_trace.py` | knife 3, source B | Python | Read correlation-id structured event logs into trace-confirmed edges (evidence being a span or event) |
| `scripts/knife4_merge.py` | knife 4 | Python | Merge and deduplicate the three sources, promote status, mark spec-only gaps, derive journeys, and flag P0 by risk heuristic (noting that it needs human confirmation) |
| `scripts/knife5_e2e.py` | knife 5 | Python | Pick a journey and generate a RED E2E skeleton (condition-based waits, no sleep) |
| `scripts/knife6_viewer.html` | knife 6 | HTML/JS | Self-contained single file (plain DOM and CSS, no heavy dependencies); **a journey list for people to read** — one sentence of summary per journey plus step chips, coloured by status (candidate dashed grey, code blue, trace green), with provenance detail on click; the technical scatter view is demoted to a collapsible "technical detail" section |
| `scripts/view.sh` | one-command viewer | bash | `bash view.sh demo` / `bash view.sh alpha` / `bash view.sh out/xxx.json` — starts a local server, opens the browser and loads the data, **no drag-and-drop needed** |
| `scripts/run_pipeline.sh` | orchestration | bash | Start the demo, inject a correlation id and walk the journey, run knives 2 and 3, merge with knife 4, generate the skeleton with knife 5, output to `scripts/out/` |
| `demo-app/` | verification target | Python (stdlib) + HTML | A small but complete multi-feature demo (frontend button A -> endpoint B writes a key and queues async work -> cron C reads the key and pushes), containing every edge type and genuinely runnable |
