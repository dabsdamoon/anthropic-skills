---
name: document-field-discovery
description: Document Forward Deployed Engineering field discoveries, observed workflows, data constraints, inferred needs, prototypes, solution alternatives, decisions, and customer validation. Use when a user needs to turn site notes, interviews, data profiling, demos, or implementation-time learning into a defensible field-discovery and solution-definition record without misrepresenting FDE inference as an original customer request.
---

# Document Field Discovery

Explain how an ambiguous customer objective became a concrete solution while
preserving the boundary between observation, inference, validation, and
implementation.

## Workflow

1. Define the discovery boundary: period, participants, sites, systems, data
   samples, demonstrations, and decisions.
2. Read `../../references/evidence-and-claim-rules.md` completely.
3. Read `references/output-contract.md` completely.
4. Read `customer-baseline.json` when available. Reference its outcome IDs
   instead of rewriting the baseline.
5. Record each finding as one of:
   - direct workflow or data observation;
   - customer statement made during delivery;
   - FDE inference;
   - stakeholder-validated finding.
6. For each solution decision, record the triggering discoveries, considered
   alternatives, selected approach, rationale, status, and provenance.
7. Record open questions with an owner and estimate impact.
8. Create `field-discovery.json` and `field-discovery.md`.
9. Validate with the customer baseline when available:

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
draft with explicit open questions instead.
