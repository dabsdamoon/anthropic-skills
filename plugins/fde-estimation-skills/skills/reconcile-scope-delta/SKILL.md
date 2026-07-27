---
name: reconcile-scope-delta
description: Reconcile customer outcomes, field discoveries, as-built implementation evidence, and estimation roles into a traceable scope delta with independent replacement-value, remaining-work, and change-adjustment allocations. Use when a user needs to distinguish original scope, necessary derived work, customer-validated discoveries, supplier-initiated work, future options, and unresolved items before generating an estimate or negotiating a change.
---

# Reconcile Scope Delta

Make the commercial classification an explicit, reviewable judgment. Do not
derive it automatically from code volume or the existence of a feature.

## Workflow

1. Read `../../references/interactive-review-protocol.md` completely.
2. Require the four canonical inputs or state which are missing:
   - `customer-baseline.json`;
   - `field-discovery.json`;
   - `as-built-evidence.json`;
   - `estimation-policy.yaml`.
3. Read `../../references/evidence-and-claim-rules.md` completely.
4. Read `../../references/scenario-and-calculation-rules.md` completely.
5. Read `references/reconciliation-contract.md` completely.
6. Run the input validator in final mode before classifying scope. Return to an
   earlier interaction gate when an input lacks its approved review.
7. Create one trace item for each commercially meaningful capability or work
   product. Map baseline, discovery, and implementation IDs.
8. Classify each item as exactly one of:
   - `explicit-baseline`;
   - `derived-necessary`;
   - `field-validated`;
   - `supplier-initiated`;
   - `future-option`;
   - `unresolved`.
9. Explain the rationale and customer-confirmation state.
10. Add scenario allocations by reviewed role-level ID and M/M. Do not collapse
    entry, junior, and senior contributors into one average-rate role. Keep
    replacement, remaining, and change-adjustment allocations independent.
11. Set unpriced or excluded allocations to `include_in_estimate: false`.
12. Keep a proposed change separate from an approved change.
13. Create draft `scope-traceability.json` with `review.status: pending`.
14. Run GATE-4. Present the classifications, role, seniority, M/M allocations,
    exclusions, assumptions, and unresolved price effects. Wait for the user or
    identified estimate owner to review them; apply corrections and record the
    real review.
15. After approval, render and verify:

```bash
python3 "$PLUGIN_DIR/scripts/build_scope_traceability.py" \
  --traceability "$OUTPUT_DIR/scope-traceability.json" \
  --customer-baseline "$INPUT_DIR/customer-baseline.json" \
  --field-discovery "$INPUT_DIR/field-discovery.json" \
  --as-built-evidence "$INPUT_DIR/as-built-evidence.json" \
  --estimation-policy "$INPUT_DIR/estimation-policy.yaml" \
  --final \
  --output-md "$OUTPUT_DIR/scope-traceability.md" \
  --verification "$OUTPUT_DIR/scope-traceability-verification.json"
```

## Completion gate

- Reject unknown cross-references and roles.
- Require an approval reference for a confirmed change-adjustment.
- Warn rather than silently bill when supplier-initiated or unresolved work is
  placed in change-adjustment.
- Stop when completed and remaining effort cannot be separated.
- Do not calculate money while scope or effort review is pending.
