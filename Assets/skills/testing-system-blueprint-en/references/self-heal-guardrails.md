# The five guardrails for self-healing backfill

> Reference document. Any process that "detects gaps automatically, generates tests
> automatically, or automatically repairs until tests go green" MUST read this and follow
> every guardrail before starting. Stack-agnostic and project-agnostic.

"Self-healing" means letting automation (including AI agents) take part in closed-loop
backfill (see `closed-loop-backfill.md`): finding gaps automatically, writing tests
automatically, attempting fixes automatically. It is powerful, and it **also makes it
extremely easy to turn a test suite quietly into a self-reassurance system**. The five
guardrails below are safety boundaries that MUST NOT be crossed.

## Guardrail 1: write only to tests/, never modify product code

A self-healing process's write permission is **limited to the test directory**. It may add
or adjust tests; it **MUST NOT modify product code on its own initiative**.

- Why: letting automation change both the product code and the tests is letting it set its
  own exam and mark its own paper — nobody can trust the result.
- Fixing the product code (step 4 of the closed loop) should be an **explicit, reviewable**
  change, not something the self-healing process does in passing.

## Guardrail 2: assertions MUST NOT be weakened (feature breaks -> test goes red)

During self-healing, **turning a test green by weakening its assertions is not permitted**.
The standard is constant: **when the feature under test genuinely breaks, the test MUST go
red.**

- Forbidden: loosening expected values, deleting a key assertion, downgrading a precise
  assertion to "passes as long as nothing throws", widening a tolerance until it means
  nothing.
- Why: after weakening, the test is "green" but no longer protects anything. A test that is
  always green is more dangerous than no test — it manufactures false confidence.
- Self-check: after the change, ask "if I broke this feature, would this test still go red?"
  The answer MUST be yes.

## Guardrail 3: no fabricated fixes at runtime

**Runtime patching, monkeypatching, interception or stubbing out the real logic to make a
test "look like it passes" is forbidden.**

- Forbidden: quietly replacing the function under test with one that always returns the
  right value; mocking out the very core logic being verified; catching and swallowing the
  error that should have caused the failure.
- Why: such a "fix" holds only inside the test process, while the defect remains untouched
  at runtime. A passing test is not a fixed defect.
- The distinction: mocking an **external dependency** (whose genuine purpose is isolating the
  unit under test) is legitimate; mocking **the subject under test itself** so it pretends to
  be correct is fabrication.

## Guardrail 4: bounded retries, then escalate to a human

A self-healing attempt MUST have a **bound on attempts or time**; on reaching that bound
without a genuine resolution (within guardrails 1-3), it **escalates to a human**.

- Forbidden: unbounded retries; cycling through strategies to "get to green" until something
  passes by chance (which usually slides into violating guardrail 2 or 3).
- Why: repeated automatic retries burn resources and readily conceal a problem that
  fundamentally needs human judgement (an ambiguous requirement, a defect at the product
  design level). **Stuck means escalate** — that is healthier than grinding to green.
- The escalation should carry: the reproducing failing test, the paths already tried, and
  why it could not be solved within the guardrails.

## Guardrail 5: produce a PR, reviewed by a human

A self-healing process's output (new tests, gap reports, fix suggestions) MUST be submitted
as a **PR or change request** and merged **only after human review**.

- Forbidden: pushing straight to the trunk, auto-merging, or landing changes around the
  review.
- Why: tests are a long-term project asset, and automatically generated tests vary in quality
  (they may overfit, they may misread the intent). Human review is the final gate that turns
  automated output into a trustworthy asset — mirroring the release gate, where a person
  makes the final go/no-go above CI.

## How the five relate

Guardrails 1-3 stop self-healing from cheating (changing what it should not, weakening
assertions, fabricating fixes); guardrail 4 stops it from grinding; guardrail 5 ensures a
person vets what finally lands. **Bypass any one of them and self-healing degrades from
"accelerating backfill" into "mass-producing false green lights".**
