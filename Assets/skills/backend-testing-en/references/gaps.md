# Four classes of backend structural gap: capabilities + per-stack instantiation

> How to use: identify the project's stack per step 0 of SKILL.md, then read that stack's
> row under the relevant gap to instantiate the tools.
> Each gap states the **capability** first (stack-agnostic, always true), then gives
> **multi-stack examples**. The examples are a lookup, not the only answer — the stack and
> the libraries are the project's own choice; this table only maps "capability -> a tool in
> that stack's ecosystem".

## Contents

1. [Real-database data layer / migrations / transactions / constraints](#1-real-database-data-layer--migrations--transactions--constraints)
2. [Authorisation / escalation, BOLA and BFLA](#2-authorisation--escalation-bola-and-bfla)
3. [Concurrency / races / rate-limit atomicity](#3-concurrency--races--rate-limit-atomicity)
4. [Resilience / fault injection](#4-resilience--fault-injection)

---

## 1. Real-database data layer / migrations / transactions / constraints

**Capability**: start a **real database container** (not an in-memory stand-in, not a mock),
run the migrations `up` and `down` as a round trip against it, and assert that:
- unique constraints, foreign keys, CHECK and NOT NULL really do block illegal writes on the
  real database;
- transactions roll back completely on the error path, leaving no dirty data;
- migrations are reversible (the schema after up -> down -> up matches), and no destructive
  data-losing migration slips through quietly.

**Why an in-memory stand-in will not do**: SQLite and similar in-memory databases behave
differently from production databases (Postgres, MySQL) on constraints, types and
concurrency isolation levels; testing constraints against a stand-in tests nothing. Only a
real database container exposes the real behaviour.

| Stack | Real database container | Migration round trip |
|---|---|---|
| Python | `testcontainers` or `pytest-postgresql` | `pytest-alembic` (asserts the up/down round trip and that no migration is ungenerated) |
| Node / TS | `testcontainers` (testcontainers-node) | The project's migration tool (Prisma Migrate, Knex, TypeORM, node-pg-migrate) run up and down |
| Go | `dockertest` (ory/dockertest) | `golang-migrate` (up/down) |
| JVM | `Testcontainers` (org.testcontainers) | `Flyway` (migrate / undo) or Liquibase |
| Other stacks | Look up that stack's "dockerised integration-test database" option | Look up that stack's mainstream migration tool's up/down commands |

**Typical assertion list**: inserting a duplicate unique key raises a constraint error; a
foreign key pointing at a non-existent parent row is refused; after an exception inside a
transaction the row count is unchanged; the schema after a migration down and up again
matches the original.

---

## 2. Authorisation / escalation, BOLA and BFLA

**Capability (a framework-agnostic build-it-yourself pattern — every stack does it this
way)**:

1. Prepare credential fixtures for **two distinct identities** — identity A and identity B
   (same privilege level, different object ownership) — plus one ordinary user and one
   privileged user.
2. **BOLA (broken object level authorisation)**: use identity A's token to access an object
   owned by identity B (parameterise across the resource endpoints by object id) and assert
   it is refused (`403` or `404`, per the project's disclosure policy).
3. **BFLA (broken function level authorisation)**: use an ordinary user's token to reach
   privileged or administrative endpoints (parameterise across the privileged actions) and
   assert it is refused.
4. Positive counter-cases: a user accessing their own object, and a privileged user reaching
   a privileged endpoint, MUST succeed — so that the refusals are not an artefact of
   refusing everything.

**Why this is built by default**: **there is no pip- or npm-installable escalation tester** —
escalation logic depends on business object ownership, which no generic tool can know.
Optional commercial or scanning options (StackHawk, hadrian and other DAST tools) can probe
the surface, but the precise object-level assertions still have to be built to the pattern
above. So this class is almost always marked "must be built" in the coverage breakdown, and
it is stack-agnostic — the only difference is which testing framework writes the token
fixtures and the parameterised sweep.

| Stack | Only "what writes the fixtures and the parameterisation" is instantiated (the pattern does not change) |
|---|---|
| Python | pytest fixtures (two clients, two token sets) plus `pytest.mark.parametrize` across endpoints |
| Node / TS | The test framework (Vitest/Jest) with supertest, parameterised via `describe.each` |
| Go | `testing` with table-driven tests, two HTTP clients carrying different tokens |
| JVM | JUnit5 `@ParameterizedTest` with MockMvc or RestAssured, two auth headers |
| Other stacks | Repeat the same pattern with that stack's parameterisation mechanism: two identities, sweep the objects and privileged endpoints, assert refusal |

**Typical assertion list**: A reads, modifies or deletes B's object -> refused; an ordinary
user calls an admin endpoint -> refused; a refusal does not leak whether the object exists
(a uniform 404 where that is the policy); the positive cases pass.

---

## 3. Concurrency / races / rate-limit atomicity

**Capability**: hit the same endpoint or resource with **several concurrent requests at
once** and assert the **invariants and atomicity** hold afterwards:
- stock or quota decrements neither oversell nor go negative;
- counters and balances suffer no lost updates;
- the rate-limit window counts accurately under concurrency (a race does not let excess
  requests through);
- a uniqueness-creating operation succeeds exactly once under concurrency (no duplicate rows).

**Why it matters**: sequential single-request tests are always green; races appear only when
operations interleave. Genuine concurrent pressure has to be created.

| Stack | Generating concurrency |
|---|---|
| Python | `pytest-run-parallel`; or `asyncio.gather([...])` inside the test to fire concurrent requests; `ThreadPoolExecutor` where synchronous |
| Node / TS | `Promise.all([...])` to fire concurrent requests, with the test framework (Vitest/Jest) asserting the invariants |
| Go | Several goroutines hitting the endpoint with `sync.WaitGroup`, asserted via `testing`; pair with `-race` to detect data races |
| JVM | `ExecutorService` with `CountDownLatch` for concurrency, asserted via JUnit; or `@RepeatedTest` |
| Other stacks | Use that stack's concurrency primitives to trigger the same resource operation concurrently and assert the invariants |

**Typical assertion list**: after N concurrent decrements the remainder equals the initial
minus the successes and is not negative; under a concurrent rate limit the number let
through equals the quota ceiling; concurrently "creating a unique resource" succeeds exactly
once and the rest are refused.

---

## 4. Resilience / fault injection

**Capability**: **intercept the service under test's calls to its external dependencies**
inside the test and inject timeouts, error responses or error sequences (two 500s then a
200), asserting that the service's **retry, timeout, degradation and circuit-breaking** logic
behaves as intended — rather than passing the failure straight up or hanging.

**Why it matters**: external dependencies will wobble in production. Resilience logic
(backoff retry, timeout ceiling, degraded fallback, breaker open) only executes when a fault
is injected; happy-path tests never reach those branches.

| Stack | HTTP-layer fault injection |
|---|---|
| Python | `respx` (intercepting httpx) or `pytest-httpx` — return timeout / error / success in call order |
| Node / TS | `nock` or `msw` — define the failure sequence and latency for the intercepted endpoint |
| Go | `httptest.Server` returning a scripted failure sequence; or inject a custom `RoundTripper` |
| JVM | WireMock (stubbed faults, latency, scenario state machine) |
| Generic network layer (any stack) | `toxiproxy` — inject latency, disconnects and timeouts at the TCP proxy layer, applicable across languages |

**Typical assertion list**: a dependency timeout triggers N retries then a degraded fallback
rather than hanging; a sequence of upstream 500s produces backoff retries and then either
success or a graceful failure; past the breaker threshold it fails fast without hitting the
dependency; while faults are injected the endpoint under test still returns a controlled
response rather than passing a 5xx straight through.

---

## Cross-gap reminders

- **Judge conditional hits before filling** (SKILL.md step 1): the four classes above are not
  a checklist to complete; fill only what this feature actually hits.
- **Coverage breakdown** (step 2): for each dimension hit, first check whether development
  TDD or contracts already cover it; where they do, skip it and avoid duplication.
- **RED must be meaningful**: confirm the test is red because of a genuine gap before going
  green, then harden it into the regression suite.
- **Guardrails**: write only under `tests/`, never weaken an assertion, no fabricated fixes,
  bounded retries, isolated changes delivered for human review (see the self-healing
  guardrails in SKILL.md).
- **Archiving**: give every new regression a traceable ID, grade it by risk, fold it into the
  release gate, and align it with the three-layer rhythm (per `testing-system-blueprint-en`).
