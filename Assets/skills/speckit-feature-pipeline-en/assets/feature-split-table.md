# Feature split table

> Split only what is marked Must-have.
> Where a Should or Could item is depended on by a downstream acceptance criterion,
> **report the dependency but do not include it unilaterally**.

## The split table

| # | Feature name | Which PRD section it comes from | Which features it depends on | Document output directory |
|:-:|---|---|---|---|
| 1 |  |  | none | `specs/001-<slug>/` |
| 2 |  |  |  | `specs/002-<slug>/` |
| 3 |  |  |  | `specs/003-<slug>/` |

**Directory format**: `specs/00X-<feature-slug>/`, a three-digit number and a kebab-case slug.

## Dependency ordering

```
<ordered by dependency topology, with the parallelisable groups marked>
```

**Serial segments**:
**Parallelisable**:

## Size estimates

| Feature | Estimated tasks | Split assessment when 17 or more |
|---|:---:|---|
|  |  |  |

Anything estimated above 18 is **split before entering the four steps**; do not discover the
overrun only after finishing tasks.

## Excluded items

| Item | Priority | Reason for exclusion | Depended on downstream? |
|---|:---:|---|:---:|

**When the last column is yes, it MUST be reported** — that means acceptance will have a gap,
and the user must decide whether to include it.

## Revision record

The split table **may be revised**. Where any feature's clarify step reveals the split was
wrong, come back to this table, correct it, and record:

| Date | Original split | Changed to | Reason |
|---|---|---|---|
