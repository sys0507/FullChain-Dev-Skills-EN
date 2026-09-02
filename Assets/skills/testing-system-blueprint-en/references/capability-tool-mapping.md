# Stack-agnostic tool mapping principles (full reference)

> This expands section 6 of SKILL.md. It is the place in the whole blueprint where the
> stack-agnostic constraint is most easily violated, so hold the line here.

## The core distinction: capability versus tool

- **Capability**: a generic primitive. It answers "what class of testing action do I need".
  For example: unit assertions, interface/HTTP contract validation, real-database
  integration, concurrency and races, E2E driving, property testing, mutation testing,
  coverage measurement. **Capabilities are constant across stacks** — every language needs
  "assert a function's return value".
- **Tool**: a capability's instance **in one concrete stack**. It answers "which library does
  this in this project's stack". **The tool is chosen by the caller after reading the
  project's actual stack**; the blueprint neither pins nor recommends a particular library.

## The single principle

> **Determine which capability is needed first, then instantiate that capability as a tool
> for the stack. The blueprint always stops at the capability layer.**

This principle is what lets the blueprint be reused by a project in any stack: a Python
backend, a Go microservice, a JVM monolith, a frontend application — their **capability
lists** overlap heavily, and only their **tool instances** differ.

## Capability -> multi-stack examples (illustrating only that one capability has different instances per stack; not a recommendation, not a lock-in)

The table below **deliberately names no concrete library**. Its purpose is to show what the
mapping looks like, while **the actual library names are filled in by
`test-routing-advisor-en` or a category skill (such as `backend-testing-en`) after reading
the project's stack**.

| Capability (generic primitive) | Python instance slot | Node instance slot | Go instance slot | JVM instance slot |
|---|---|---|---|---|
| Unit / assertions | That stack's mainstream unit framework | That stack's mainstream unit framework | The built-in testing facility | That stack's mainstream unit framework |
| Mocks / doubles | That stack's doubles mechanism | That stack's doubles mechanism | That stack's doubles mechanism | That stack's doubles mechanism |
| HTTP / interface contracts | A contract or schema validation library | A contract or schema validation library | A contract or schema validation library | A contract or schema validation library |
| Real-database integration (real DB + migrations) | An ephemeral real database instance | An ephemeral real database instance | An ephemeral real database instance | An ephemeral real database instance |
| Concurrency / races | That stack's concurrency testing approach | That stack's concurrency testing approach | The built-in race detection facility | That stack's concurrency testing approach |
| E2E driving | A browser or API driver | A browser or API driver | A browser or API driver | A browser or API driver |
| Coverage measurement | That stack's coverage tool | That stack's coverage tool | The built-in coverage facility | That stack's coverage tool |

> Note: "the built-in testing facility" and "the built-in race detection facility" are
> neutral descriptions of what some stacks ship with. They are still **instance slots**, not
> an anointed command; the project's own convention decides.

## The instantiation flow (for skills following this blueprint)

1. **Read the project's stack**: infer the language and testing infrastructure actually in
   use from the dependency manifest, the build configuration and the existing test directory.
2. **Land each capability on the list**: for every capability this task needs, pick a tool in
   that stack that is **already in use or agreed by the team**. Prefer reusing what the
   project already has over introducing a new dependency.
3. **Where the stack lacks a mature tool for a capability**: record the gap at the capability
   layer ("this stack has no ready contract validation"), and let the category skill decide
   the fallback. **Do not force in a tool from another stack.**

## Anti-patterns (violating stack-agnosticism)

- Hardcoding "use library X" in the blueprint or the routing layer — this binds the
  methodological skeleton to one stack, and other projects cannot reuse it.
- Assuming every project uses the same language, and presenting a single-stack command-line
  example as a universal instruction.
- Making the **tool choice** inside the blueprint rather than leaving it to the downstream
  skill that has read the project's stack.

Remember: **the blueprint owns "which capabilities are needed"; downstream owns "which tools
to use".** The two responsibilities do not mix.
