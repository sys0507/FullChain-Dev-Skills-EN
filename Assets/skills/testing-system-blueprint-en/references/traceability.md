# Requirements↔Test Traceability (Complete Rules)

> This document expands SKILL.md §II. Stack-agnostic, project-agnostic.
> Goal: make "was this requirement tested" a **mechanically answerable** question rather than a human judgment call.

## Why Traceability Is Needed

The larger the test suite, the harder it is to answer "did we actually test everything" by feel. Traceability turns that question into set arithmetic: compare the set of "all acceptance criterion IDs" against the set of "all IDs referenced by tests", and the difference immediately exposes the hole.
It is the prerequisite that makes the release gate's "no orphan requirements" criterion (release-gate.md) mechanically enforceable.

## Three Elements

### 1. One stable ID per acceptance criterion (AC)
- Shaped like `AC-<feature>.<index>` (example: `AC-007.3`). The naming rule is the project's choice; the blueprint only requires that it be **stable**.
- **Stable = once published, never renumbered, never reused**. When a requirement is deleted, its ID retires and is never taken over by a new requirement.
  Otherwise historical test references would "point at a different requirement" and silently go wrong.

### 2. Each test references the AC ID it covers
The reference mechanism is instantiated per stack / tool; three common carriers (pick one, stay consistent within the team):
- **ID embedded in the test name**: the test name / case title contains `AC-007.3`.
- **Annotation / tag / metadata**: use that stack's test annotation mechanism to attach a marker like `@covers AC-007.3`.
- **Structured manifest**: maintain a mapping file of `AC ID -> test identifier`.

One AC may be covered by several tests; one test may cover several ACs. Many-to-many is normal.

### 3. Bidirectional mechanical validation
- **No orphan requirement**: `{all AC IDs} - {referenced AC IDs} = the empty set`.
  A non-empty difference = a requirement nobody tests = a missed test.
- **No ghost requirement**: `{referenced AC IDs} - {all AC IDs} = the empty set`.
  A non-empty difference = a test references a non-existent AC = the requirement was deleted or the number was mistyped, and the test is running naked (it asserts a contract that no longer exists).

## Validation Approach (stack-agnostic pseudocode)

The concrete implementation is instantiated by the caller per stack (how to enumerate tests and how to extract referenced IDs are both stack-specific). The logic is constant:

```
ac_ids     = parse the requirements document -> collect the set of all AC IDs
referenced = scan the tests (names / annotations / mapping file) -> collect the set of referenced IDs

orphans = ac_ids - referenced     # requirement with no test
ghosts  = referenced - ac_ids     # test references a non-existent requirement

if orphans is non-empty: report the list of untested ACs, release gate no-go
if ghosts  is non-empty: report the list of naked tests, release gate no-go
```

Instantiate this logic as a script for that stack and hang it in CI (see release-gate.md), and traceability turns from "a documentation burden" into "an automatic guardrail".

## Common Anti-Patterns

- **Adding IDs after the fact**: writing a pile of tests and then stuffing IDs in afterwards -> the IDs do not match the actual assertions. Reference the AC while writing the test.
- **ID reuse**: giving a deleted requirement's number to a new requirement -> historical references silently point at a new meaning. Retire, never reuse.
- **Only one direction**: checking orphans but not ghosts -> tests for deleted requirements keep "running green and naked", giving false confidence. Check both directions.
- **Treating traceability as documentation**: written in a wiki that nobody reconciles -> it MUST be mechanically consumable by a script before it can enter a gate.

## Project-Agnostic Reminder

The content of an AC is project-specific, but the mechanism of "assign an ID + reference it from tests + validate bidirectionally" is entirely general and is not bound to any business domain.
