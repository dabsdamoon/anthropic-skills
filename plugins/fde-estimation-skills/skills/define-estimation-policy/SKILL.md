---
name: define-estimation-policy
description: Define a reproducible software estimation policy with dated role rates, source references, effort units, overhead, technical fee, profit, risk, discount, tax, rounding, confidence range, and validity. Use when a user needs the pricing and arithmetic rules that support an FDE budgetary estimate, basis of estimate, replacement valuation, remaining-work quote, or change-adjustment proposal.
---

# Define Estimation Policy

Create the reusable commercial calculation policy separately from project scope.
Never hardcode a current market rate without its source and date.

## Workflow

1. Read `../../references/scenario-and-calculation-rules.md` completely.
2. Read `references/policy-contract.md` completely.
3. Determine jurisdiction, currency, locale, effective period, estimate
   maturity, and permitted commercial model.
4. Collect official or primary role-rate sources. When current rates matter,
   verify them from the source at execution time and record retrieval date.
5. Add market benchmarks only as cross-checks; do not present a market listing
   as a binding rate.
6. Define role IDs and monthly rates. Keep role mapping explicit.
7. Set every cost component explicitly, including zero values:
   - overhead;
   - technical fee;
   - profit;
   - risk;
   - discount;
   - tax;
   - rounding.
8. Define confidence range, re-estimation triggers, and validity period.
9. Create `estimation-policy.yaml` using JSON-compatible YAML and
   `estimation-policy.md` for human review.
10. Validate:

```bash
python3 "$PLUGIN_DIR/scripts/validate_input_package.py" \
  --estimation-policy "$OUTPUT_DIR/estimation-policy.yaml" \
  --final \
  --output "$OUTPUT_DIR/estimation-policy-verification.json"
```

## Judgment rules

- Distinguish employee average wages, supplier cost, and customer billing rate.
- Explain whether statutory benefits, tools, travel, infrastructure, and
  support are included.
- Use company policy, not the implemented product, to choose margin.
- Do not add a risk percentage when the same uncertainty is already priced as
  explicit effort.
- Preserve a conservative zero-cost component as an intentional policy
  decision, not an omission.

## Completion gate

Stop finalization when a priced role lacks a dated source or when the arithmetic
order is ambiguous.
