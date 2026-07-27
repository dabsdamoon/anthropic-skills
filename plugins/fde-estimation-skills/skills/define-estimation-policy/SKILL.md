---
name: define-estimation-policy
description: Interactively define a reproducible software estimation policy with user-reviewed job families and entry, junior, or senior staffing; KOSA or level-specific web rate evidence; effort units; overhead; technical fee; profit; risk; discount; tax; rounding; confidence; and validity. Use when a user needs the staffing, pricing, and arithmetic rules for an FDE budgetary estimate, basis of estimate, replacement valuation, remaining-work quote, or change-adjustment proposal.
---

# Define Estimation Policy

Create the reusable commercial calculation policy separately from project scope.
Never hardcode a current market rate without its source and date.

## Workflow

1. Read `../../references/interactive-review-protocol.md` completely.
2. Confirm GATE-0 is complete. If the value question or product boundary is
   unclear, ask the user and wait before choosing a policy.
3. Read `../../references/scenario-and-calculation-rules.md` completely.
4. Read `../../references/workforce-rate-source-rules.md` completely.
5. Read `references/policy-contract.md` completely.
6. Run GATE-3. Derive and present the necessary job families with the reason
   each is needed. Ask the user to confirm `entry`, `junior`, or `senior` for
   every role-level combination and wait.
7. After staffing confirmation, ask for jurisdiction, currency, locale,
   effective period, estimate maturity, commercial model, and every user-owned
   cost rule. Do not infer a default from the repository.
8. Check the latest applicable KOSA publication. Use it as the selected rate
   only when it explicitly covers the confirmed seniority. Otherwise collect
   current level-specific web evidence according to the workforce source rules.
9. Record every observed value, normalization, compensation scope, selected
   monthly rate, and rationale. Keep an aggregate KOSA value as a cross-check,
   never as a silent proxy for seniority.
10. Set every cost component explicitly, including zero values:
   - overhead;
   - technical fee;
   - profit;
   - risk;
   - discount;
   - tax;
   - rounding.
11. Define confidence range, re-estimation triggers, and validity period.
12. Create draft `estimation-policy.yaml` using JSON-compatible YAML and
    `estimation-policy.md` with `review.status: pending`.
13. Present the staffing matrix, raw and normalized rate evidence, selected
    rates, cost rules, and arithmetic order. Wait for the user or identified
    estimate owner to approve or correct them and record the real review.
14. Validate only after the review is approved:

```bash
python3 "$PLUGIN_DIR/scripts/validate_input_package.py" \
  --estimation-policy "$OUTPUT_DIR/estimation-policy.yaml" \
  --final \
  --output "$OUTPUT_DIR/estimation-policy-verification.json"
```

## Judgment rules

- Distinguish employee average wages, supplier cost, and customer billing rate.
- Do not treat a KOSA occupation mean or wage percentile as a seniority band
  unless the publication explicitly defines it that way.
- Explain whether statutory benefits, tools, travel, infrastructure, and
  support are included.
- Use company policy, not the implemented product, to choose margin.
- Do not add a risk percentage when the same uncertainty is already priced as
  explicit effort.
- Preserve a conservative zero-cost component as an intentional policy
  decision, not an omission.

## Completion gate

Stop finalization when a priced role lacks a dated source or when the arithmetic
order is ambiguous. If a user-owned value is unanswered, keep the policy in
draft; zero is valid only when explicitly selected. Also stop when any role
lacks user-confirmed seniority or auditable normalized rate evidence.
