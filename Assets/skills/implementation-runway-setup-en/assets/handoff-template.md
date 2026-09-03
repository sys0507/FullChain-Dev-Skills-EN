# Session Handoff · <feature-name>

## Last Known State

(Briefly describe the last operation. If implementation has not started, state which prerequisite documents are ready.)

## Next Session

1. Read the project constitution first.
2. Read the progress file; the current task is T0X.
3. Read this feature's acceptance criteria in `spec.md` and file structure in `plan.md`.
4. Continue from T0X. **Do not re-plan.**

## Feature Dependencies

(List dependent features, or write `None`.)

## Do Not Re-plan

The plan is finalized and tasks are locked. Execute them directly.

If the plan or tasks are genuinely wrong, **stop, report the problem, and wait for a ruling**. Do not silently rewrite them and continue.

## After Each Task

1. Change that task's `[ ]` to `[x]` in `tasks.md`.
2. Update Current Task, Completed, Progress, and Last Updated in the progress file.
3. Commit.
4. STOP and wait for `next`.

## Tasks Not Ready

(If the tasks file is missing or empty, state that here so the next session does not start implementation by mistake.)
