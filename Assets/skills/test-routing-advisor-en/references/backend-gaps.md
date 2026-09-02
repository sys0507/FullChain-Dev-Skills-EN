# Backend-only structural gap list (stack-agnostic capabilities -> routed to `backend-testing-en`)

This list serves the "backend only" category: when a feature's backend tasks are all green
and it enters close-out, the TDD loop has covered only the units, while the genuinely
high-risk gaps sit where TDD does not usually reach. Below, those **structural gaps** are
listed one by one (all of them **stack-agnostic capabilities**), each judged either
"available (just pick the tool for the stack)" or "**must be built** (no stack has an
off-the-shelf answer)". **This skill hardcodes no single-stack tool** — once you have judged
which gaps are hit, **route them, with the reason each was hit, to the `backend-testing-en`
skill**, which reads the project's `package.json` / `pyproject.toml` / `go.mod` /
`Cargo.toml` to identify the stack and picks that stack's tools to close the gap.

> Methodology follows the `testing-system-blueprint-en` skill as its blueprint; defect
> hardening reuses the TDD / systematic-debugging practice it points at ("for a bug, first
> write a failing test that reproduces it, then fix it"). Tool names below are
> **multi-stack examples**, not fixed answers.

## The key insight: code review is not a test

Many close-out processes handle these gaps with "a look during code review". But **code
review only reads and finds problems; it produces no regression test** — even if a defect
is fixed on the spot, without being hardened into a test that will go red, it comes back.
So the table below separates "how the process treats this gap today" from "what capability
the test should cover": finding by reading is not regression protection.

## Gap list (stack-agnostic)

| Structural gap (capability) | How the process treats it today | Judgement | Routes to / approach |
|---|---|---|---|
| Real-database data layer / migrations / transactions / constraints | Only reviewed (reading code, not running a real database) | Available | `backend-testing-en` picks a real-database or containerised testing tool for the stack |
| Authorisation / privilege escalation (BOLA, BFLA) | **Not touched at all** (P0) | **Must be built** | `backend-testing-en` builds two-user assertions (no stack has an off-the-shelf answer, see below) |
| Concurrency / races / rate-limit atomicity | Zero coverage | Available | `backend-testing-en` picks a concurrency load approach for the stack |
| Resilience / retry / timeout / degradation | Only reviewed | Available | `backend-testing-en` picks an HTTP or dependency mocking library for the stack |

## Each gap in detail (capability definition + multi-stack examples)

### 1. Real-database data layer / migrations / transactions / constraints — available

**Capability definition:** run migrations up and down against a real database as a
round trip, and verify constraints and serialisation on that real database. Unit tests
that mock out the data layer conceal schema drift, dead constraints and irreversible
migrations — only a real database catches those.

- **Multi-stack examples (chosen by `backend-testing-en` per stack):** Python stacks often
  use `pytest-alembic` (migration round trip) plus `pytest-postgresql` (a real database
  without Docker); any stack can use `testcontainers` to start a real container; other
  stacks use their own ecosystem's real-database or container testing tools. **These are
  examples, not fixed answers.**

### 2. Authorisation / privilege escalation (BOLA, BFLA) — must be built (P0, stack-agnostic judgement)

This is the gap the process **does not touch at all**. It carries the highest risk, and
**no stack has a plug-and-play answer** — it is business semantics.

- **BOLA (broken object level authorisation):** can user A read or modify an object that
  belongs to user B (`/resource/{id}`)?
- **BFLA (broken function level authorisation):** can an ordinary user reach a privileged
  endpoint meant only for administrators?

**Why it must be built, in any stack:** generic "is authorisation enforced" scanners can
only check whether an endpoint lets through a request with no token. They **cannot test
object-level escalation** — an endpoint that demands a token but never verifies that the
token's subject may access that particular object looks fine to a scanner, because the
scanner has no way to know which object should belong to whom. That is business semantics,
and no stack has an off-the-shelf tool for it.

**How to build it (landed by `backend-testing-en` per stack; the logic is stack-agnostic):**

1. Prepare a **two-user credential fixture** (a valid credential set each for user_A and user_B).
2. As user_A, create or obtain an object and record its id.
3. **Parameterise across the id-addressed endpoints**, accessing user_A's object with
   user_B's credentials.
4. **Assert that cross-user access returns 403** (or 404, per the project's convention) and
   never 200 with someone else's data.
5. Do the same for privileged endpoints: call an admin endpoint with ordinary user
   credentials and assert it is refused.

### 3. Concurrency / races / rate-limit atomicity — available

**Capability definition:** fire N concurrent requests inside one test and assert that rate
limits, quotas and unique constraints are not broken under concurrency. Rate limits, quotas
and unique constraints are always green in serial tests; the defects appear only under
concurrency.

- **Multi-stack examples (chosen by `backend-testing-en` per stack):** Python stacks use
  `pytest-run-parallel` with `asyncio.gather`; Go stacks use goroutines with the race
  detector (`-race`); JS/TS stacks fire concurrent requests via `Promise.all`; other stacks
  use their own concurrency load approach.

### 4. Resilience / retry / timeout / degradation — available

**Capability definition:** inject timeouts and error sequences into external dependencies —
simulate "fails twice, succeeds on the third" to verify retry logic, or "keeps failing" to
verify that degradation or fallback actually happens. Unit tests rarely cover these paths
through external dependencies.

- **Multi-stack examples (chosen by `backend-testing-en` per stack):** Python httpx stacks
  use `respx` or `pytest-httpx`; Node stacks use `nock` or `msw`; other stacks use their
  ecosystem's HTTP or dependency mocking library.

## Working with conditional hits

Not every feature hits every gap — take the subset the feature actually touches (the hit
rules are in the "conditional hits" table in `tool-mapping.md`): mark the real-database gap
only when it writes to a database, the authorisation gap only when there are multiple users
or privileged endpoints, the concurrency gap only when there are rate limits or quotas, the
resilience gap only when it calls an external dependency. A simple backend that is pure
logic or read-only may hit none of them, where TDD plus contracts is enough — do not
over-test to fill the table. This skill marks only the capability gaps that are hit;
**the concrete tools are always instantiated by `backend-testing-en` for the stack, and
this skill does not decide them on its behalf.**
