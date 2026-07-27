# Estimation policy contract

Follow `../../../schemas/estimation-policy.schema.json`.

Initialize `review.status` as `pending`. An approved review must identify the
reviewer, time, and source response covering the complete policy and arithmetic
order.

Use identifier prefixes:

- rate source: `RATE-`
- role: `ROLE-`

Write `estimation-policy.yaml` as JSON-compatible YAML so the plugin can parse it
without a third-party dependency. General YAML syntax is supported when PyYAML
is installed.

Required cost rules:

- `overhead_rate_on_direct`
- `technical_fee_rate_on_direct_plus_overhead`
- `profit_rate_on_cost`
- `risk_rate_on_cost`
- `discount_rate`
- `tax_rate`
- `rounding_unit`
- `rounding_mode`

Use decimal fractions: ten percent is `0.10`.

The Markdown review should state:

1. Purpose and applicable estimate types
2. Effective period and currency
3. Role-rate table with sources
4. Cost composition and calculation order
5. What is included and excluded
6. Confidence range and re-estimation triggers
7. Approval owner
