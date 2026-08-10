# Delivery PR body

Use this structure for production-quality implementation after an evidence handoff. Omit empty administrative sections, but never omit the handoff decision, acceptance trace, remaining product risk, or out-of-scope work.

```markdown
# PR: [delivery title]

**Track:** Delivery
**Evidence handoff:** validated | provisional | missing
**Branch:** `[source]` → `[target]`
**Primary review question:** Does this implementation trace to an accepted handoff and satisfy its contract safely?

## Summary

[What accepted behavior is delivered, why it is ready for Delivery, and the thinnest vertical slice implemented.]

## Evidence handoff

- **Source:** [link or repository path]
- **Decision:** [validated/provisional/missing]
- **Accepted learning:** [interaction, terminology, or verified constraint]
- **Remaining product risk:** [customer/value/usability evidence still missing]

If the source is missing, say why implementation proceeded and whether this blocks merge.

## Acceptance traceability

| Observable criterion | Source | Test or verification | Status |
|---|---|---|---|
| [criterion] | [handoff/safety constraint] | [test/command/manual evidence] | PASS/FAIL/MISSING |

## TDD evidence

| Slice | Red evidence | Green evidence | Refactor/broader checks |
|---|---|---|---|
| [behavior] | [observed failure] | [focused pass] | [suite/build/browser] |

If red evidence was not preserved, state `not recorded`; do not infer it from test files or commit order.

## Major changes

### [Change category]
- **Files:** [paths]
- **Why:** [accepted behavior or fixed constraint]
- **Impact:** [consumers and operational effect]

## Blast radius

| File/area | Dependents | Radius | Notes |
|---|---:|---|---|

**Overall:** LOW | MEDIUM | HIGH | CRITICAL

## Security analysis

**Rating:** CLEAR | NOTE | CONCERN

[Findings and required action.]

## Deviations from handoff/spec

| Type | Item | Source said | PR does | Why/impact |
|---|---|---|---|---|

## Delivery discoveries

- **Returned to Discovery:** [implementation finding that changes or extends the product assumption]
- **No feedback required:** [state explicitly when none]

## Verification

- [x] [Focused behavior test]
- [x] [Broader suite, typecheck, build, browser, migration, or operational check]
- [ ] [Unverified item with reason; mark automatable gaps]

## Not included / out of scope

- [Deferred behavior, missing customer evidence, non-goal, or follow-up a reader may assume is complete.]

## Notes for reviewers

Review acceptance traceability and remaining product risk separately from implementation quality.
```

## Delivery-specific checks

- Do not use passing tests as the evidence-gate decision.
- A `provisional` handoff must constrain the scope and claims of Delivery.
- A missing handoff is a review finding even when the implementation is high quality.
- Report tests against observable behavior and public boundaries; flag tests coupled to private implementation details.
- Feed implementation discoveries back to Discovery rather than silently expanding the handoff.
