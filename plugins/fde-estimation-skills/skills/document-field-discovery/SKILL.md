---
name: document-field-discovery
description: Document Forward Deployed Engineering field discoveries, observed workflows, data constraints, inferred needs, prototypes, solution alternatives, decisions, and customer validation. Use when a user needs to turn site notes, interviews, data profiling, demos, or implementation-time learning into a defensible field-discovery and solution-definition record without misrepresenting FDE inference as an original customer request.
---

# Document Field Discovery

Explain how an ambiguous customer objective became a concrete solution while
preserving the boundary between observation, inference, validation, and
implementation.

## Workflow

1. Read `../../references/interactive-review-protocol.md` completely.
2. Confirm GATE-0 and GATE-1 are complete. If intent or baseline is still
   material to the discovery, return to the affected gate and ask the user.
3. Define the discovery boundary: period, participants, sites, systems, data
   samples, demonstrations, and decisions.
4. Read `../../references/evidence-and-claim-rules.md` completely.
5. Read `references/output-contract.md` completely.
6. Read `customer-baseline.json` when available. Reference its outcome IDs
   instead of rewriting the baseline.
7. Record each finding as one of:
   - direct workflow or data observation;
   - customer statement made during delivery;
   - FDE inference;
   - stakeholder-validated finding.
8. For each solution decision, record the triggering discoveries, considered
   alternatives, selected approach, rationale, status, and provenance.
9. Record open questions with an owner and estimate impact.
10. Create draft `field-discovery.json` and `field-discovery.md` with
    `review.status: pending`.
11. Run GATE-2. Present material discoveries, inferences, solution decisions,
    alternatives, and price-affecting questions in plain language. Wait for the
    user or identified stakeholder to review them, then record the real review.
12. Validate with the customer baseline when available:

```bash
python3 "$PLUGIN_DIR/scripts/validate_input_package.py" \
  --customer-baseline "$INPUT_DIR/customer-baseline.json" \
  --field-discovery "$OUTPUT_DIR/field-discovery.json" \
  --final \
  --output "$OUTPUT_DIR/field-discovery-verification.json"
```

## Judgment rules

- Use `inferred` until an identified stakeholder confirms the need.
- Do not treat a demo reaction as approval unless the source records approval.
- Explain why the solution is necessary for an outcome; do not merely list
  features.
- Preserve rejected and superseded alternatives when they explain cost or
  complexity.
- Do not infer customer value from implementation effort.

## Completion gate

Stop finalization when the artifact cannot distinguish observations from
inferences, or when material decisions have no source or rationale. Deliver a
draft with explicit open questions instead. Repository implementation cannot
substitute for stakeholder review.
