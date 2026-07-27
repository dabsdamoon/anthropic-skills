# Reconciliation contract

Follow `../../../schemas/scope-traceability.schema.json`.

Initialize `review.status` as `pending`. An approved review must identify the
reviewer, time, and source response covering scope classifications and M/M
allocations.

Use identifier prefix `TRC-`.

## Classification decision

- Use `explicit-baseline` only with baseline evidence.
- Use `derived-necessary` when the original outcome cannot work without the
  item and document that causal necessity.
- Use `field-validated` when a stakeholder confirmed a discovery or solution.
- Use `supplier-initiated` when the supplier chose the work without customer
  confirmation.
- Use `future-option` for unimplemented selectable scope.
- Use `unresolved` when evidence conflicts or is insufficient.

## Allocation decision

Each allocation records:

- scenario;
- role;
- effort M/M;
- commercial status;
- whether it enters the estimate;
- explanatory note.

Commercial status:

- `reference-only`
- `proposed`
- `confirmed`
- `excluded`

Scenario membership never proves entitlement. Keep the supporting rationale and
approval reference visible.
