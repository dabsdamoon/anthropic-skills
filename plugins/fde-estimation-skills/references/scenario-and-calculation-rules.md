# Scenario and calculation rules

## Keep estimate scenarios independent

- `replacement-value`: reference value to rebuild the described product or
  capability from the stated starting point.
- `remaining-work`: future work that has not been completed.
- `change-adjustment`: completed work asserted to be outside the original
  baseline and submitted for written change negotiation.

Never present the arithmetic sum of these scenarios as an amount due. A scope
item may inform more than one scenario only when each allocation represents a
different commercial question and the document explains that relationship.

## Cost order

Apply rates with decimal arithmetic in this order:

1. Direct labor = role monthly rate × effort M/M.
2. Overhead = direct labor × `overhead_rate_on_direct`.
3. Technical fee = (direct labor + overhead) ×
   `technical_fee_rate_on_direct_plus_overhead`.
4. Cost subtotal = direct labor + overhead + technical fee.
5. Profit = cost subtotal × `profit_rate_on_cost`.
6. Risk = (cost subtotal + profit) × `risk_rate_on_cost`.
7. Pre-discount supply = cost subtotal + profit + risk.
8. Discount = pre-discount supply × `discount_rate`.
9. Supply amount = pre-discount supply - discount.
10. Tax = supply amount × `tax_rate`.
11. Total = supply amount + tax.

Round monetary outputs with the policy's `rounding_unit` and `rounding_mode`.
The deterministic calculator supports `HALF_UP`, `DOWN`, and `UP`.

## Evidence gates

- A role must exist in the estimation policy before it can be priced.
- Every priced role must have user-confirmed seniority and auditable normalized
  rate evidence for its cited sources.
- An aggregate KOSA occupation average or percentile is not a seniority rate.
- Every priced allocation must point to a scope item.
- A confirmed change-adjustment must include an approval reference.
- A proposed change-adjustment must be described as a request for discussion,
  not an established legal right.
- Excluded allocations must not enter a scenario total.
- Rate sources must record an effective or retrieval date.

## Uncertainty

Keep uncertainty separate from arithmetic contingency. State:

- estimate class or maturity;
- confidence range;
- unresolved assumptions;
- conditions that trigger re-estimation;
- validity period.

Do not hide uncertainty by lowering scope, deleting reserves, or presenting a
single precise total without its assumptions.
