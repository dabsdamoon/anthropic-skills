# Discovery PR body

Use this structure for a prototype, experiment, research, or evidence-handoff PR. Omit empty administrative sections, but never omit the evidence decision, limitations, or prototype disposition.

```markdown
# PR: [experiment/discovery title]

**Track:** Discovery
**Decision:** validated | rejected | insufficient | provisional | pending
**Branch:** `[source]` → `[target]`
**Primary review question:** Did this work test the stated assumption credibly, and does the evidence support the decision?

## Summary

[What uncertainty this PR investigates, why it matters, and what decision it enables.]

## Discovery contract

| Field | Definition |
|---|---|
| Outcome | [desired user or business outcome] |
| Target user and situation | [who, where, and when] |
| Riskiest assumption | [single assumption under test] |
| Discovery question | [question the experiment can answer] |
| Method | [interview, observation, prototype, spike, data query, production experiment] |
| Predeclared threshold | [success/failure threshold, or explicitly missing] |

## Evidence quality

| Source | Sample/context | What it supports | Limitation |
|---|---|---|---|
| [source] | [participants/environment] | [bounded claim] | [bias or missing representativeness] |

## Raw observations

- [Observed behavior, quote excerpt, measurement, or verified constraint without interpretation.]

## Interpretation and decision

**Decision:** [state and justify the gate outcome]

- **Accepted:** [interaction, terminology, constraint, or assumption]
- **Rejected:** [alternative or assumption]
- **Still unknown:** [unresolved risk]

## Prototype scope and disposition

- **Built to answer:** [question]
- **Not evidence of:** [claims the artifact cannot support]
- **Disposition:** delete | archive | retain as non-production reference
- **Code excluded from Delivery:** [prototype internals not to carry forward]

## Proposed Delivery handoff

1. [Observable acceptance criterion]
2. [Observable acceptance criterion]

## Engineering review

### Blast radius
[Dependents and overall rating.]

### Security analysis
**Rating:** CLEAR | NOTE | CONCERN

### Experiment verification
- [x] [Observed execution or artifact check]
- [ ] [Unverified item, with reason]

## Deviations and limitations

- [Deviation from experiment plan, sequence bias, proxy participants, missing timing, or instrumentation gap.]

## Not included / next question

- [What a reader could wrongly assume was validated.]
- **Next Discovery question:** [question]

## Notes for reviewers

Review the credibility of the method and decision before reviewing visual preference or production code quality.
```

## Discovery-specific checks

- Use `pending` only before the experiment has run; do not disguise it as `provisional`.
- Do not call stakeholder preference, heuristic inspection, or automated browser checks customer validation.
- Do not include a Delivery implementation checklist unless the PR genuinely contains accepted Delivery work.
- When raw notes cannot be shared, state the access restriction and provide a traceable bounded summary.
