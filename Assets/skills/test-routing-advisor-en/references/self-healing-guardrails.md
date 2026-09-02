# Self-healing test agents: five guardrails

When this advisor recommends an **agent-driven** testing option (a self-healing E2E loop,
say, or an auto-repair agent), that agent MUST operate under these five guardrails. They
exist because an unconstrained agent whose only goal is "make the tests green" will
happily delete assertions or patch the product to mask a failure — which destroys exactly
the signal the tests were there to give. The advisor never runs an agent itself; it points
here so that whoever builds one does it safely.

## The five guardrails

1. **Write tests only; never touch product code.** The agent may add or edit files under
   the test directory (`tests/` or its equivalent) and nowhere else. A failing test means
   the product is wrong; the agent's job is to express that correctly in a test, not to
   "fix" production behaviour it was never asked to change.

2. **An assertion MUST NOT be weakened.** The invariant is: *if the feature breaks, the
   test MUST go red.* The agent MUST NOT loosen a comparison, widen a tolerance, delete an
   assertion, or replace a meaningful check with one that is always true in order to reach
   green. An assertion-strength diff in CI should reject any change that lowers the tests'
   discriminating power.

3. **No fabricated fixes at runtime.** The agent MUST NOT stub, monkeypatch or short-circuit
   the system under test to manufacture a pass — forcing a function to return the expected
   value, intercepting the very call that is failing. Tests MUST exercise the real code path.

4. **Bounded retries, then escalate to a human.** The agent gets a fixed, small retry
   budget. When it exhausts that budget without a legitimate green, it stops and escalates
   with the failure context — it does not keep changing things until something passes.

5. **Produce a PR for human review.** The agent's work product is a pull request, never a
   direct commit to a protected branch. A human reviews the diff before it lands, so
   guardrails 1-4 get a person as the final backstop.

## Why this matters to the advisor

These guardrails are part of the **deterministic verification layer** the advisor
explicitly does **not** replace. When the closing report marks a recommendation with a
check mark ("already covered by a CI gate"), what it relies on for real proof are
mechanisms like the assertion-strength diff (guardrail 2) and the breaking-change gate.
The advisor's recommendations set direction; these guardrails plus the CI gates are what
make the resulting tests worth trusting.
