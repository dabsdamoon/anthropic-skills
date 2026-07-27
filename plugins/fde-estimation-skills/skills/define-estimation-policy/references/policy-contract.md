# Estimation policy contract

Follow `../../../schemas/estimation-policy.schema.json`.

Initialize `review.status` as `pending`. An approved review must identify the
reviewer, time, and source response covering the complete policy and arithmetic
order.

Use identifier prefixes:

- rate source: `RATE-`
- role: `ROLE-`

Each rate source records its publisher, source type, location, retrieval date,
explicitly covered seniority levels, and compensation scope.

Each role represents one job-family and seniority combination. Record:

- `occupation`, `seniority`, and `seniority_confirmed`;
- final `monthly_rate` and `rate_method`;
- every `source_id` used in `source_ids`;
- one raw and normalized observation per cited source in `rate_evidence`;
- the selection and normalization logic in `rate_rationale`.

Do not set `seniority_confirmed: true` before the user or identified staffing
owner reviews the proposed staffing matrix.

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
3. Reviewed job-family and seniority matrix
4. Raw and normalized rate evidence with compensation scope
5. Selected role rates and selection rationale
6. Cost composition and calculation order
7. What is included and excluded
8. Confidence range and re-estimation triggers
9. Approval owner
