# The dual-route cross-verification standard

## When to read this

When performing any research task during the research stage.

---

## The requirement

Every research task **MUST cross-verify using at least two mutually independent search
sources**:

| Route | Source |
|:-:|---|
| 1 | The current AI tool's built-in web search and page reading |
| 2 | The configured research search capability, **or** another independent search source |

How "independent" is judged: the two routes have **different underlying data sources**. The
same search engine with a different query is not two routes.

---

## Evidence priority

| Question type | Trust first |
|---|---|
| **Technical questions** | Official documentation -> source code -> release notes -> issues -> the licence text |
| **Market information** | The product's own site -> the official pricing page -> authoritative third-party material |

Second-hand summaries, aggregator sites and unattributed blogs **MUST NOT be the only source**.

**The search date MUST be recorded** — versions, prices and policies have very short shelf
lives.

---

## Degradation: when the second route is unavailable

The research search capability is `optional`. When it is unavailable:

1. **Degrade to a single route and carry on** — research is not blocked
2. **Label it explicitly in the research output**:

> "This conclusion rests on a single search route and was not cross-verified."

**MUST NOT present it silently as a dual-route conclusion.**

What that label does is tell downstream which confidence tier the conclusion sits in. A
conclusion that was not cross-verified is still useful, but it should not look as reliable as
one that was.

---

## Handling conflicts

When the two routes disagree:

| Situation | Handling |
|---|---|
| One is clearly more authoritative (official versus second-hand) | Trust the authoritative one, and **record the other and the fact they disagree** |
| Both carry comparable authority | **Record both side by side, marked pending**; do not force a reconciliation |
| They differ in recency | Trust the newer one, and record both dates |

**MUST NOT** erase the minority view because "most sources say otherwise" — the minority may
be the only one that read the original.

---

## The relationship with the ledger

When a research conclusion enters the project context ledger, it is always a **research
candidate value**, never "user confirmed".

Even a conclusion that passed dual-route cross-verification only shows "this inference is
probably right"; it does not show "the user agrees". The two are orthogonal.

The ledger's evidence column MUST record: **the source + the search date + whether it was
cross-verified**.
