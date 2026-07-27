# Workforce and Rate Source Rules

Treat staffing composition as a user decision and rate research as evidence.
Never apply one occupation-wide average to every contributor.

## 1. Propose the staffing matrix

Derive a small list of necessary job families from the reviewed outcomes, scope,
discoveries, and implementation boundary. Present it before researching rates:

| Job family | Why it is needed | Proposed seniority | User decision |
|---|---|---|---|
| Application development | Build and integrate the service | junior | pending |

Use `entry`, `junior`, and `senior` as canonical labels. Explain the intended
responsibility or experience band when the label is ambiguous. One occupation
may appear more than once when the plan needs different levels.

Ask the user to confirm, change, add, or remove each role-level combination.
Keep `seniority_confirmed: false` and stop finalization until they respond.
Confirm M/M for the reviewed role IDs at GATE-4.

## 2. Select rate evidence

Use this default hierarchy after the staffing matrix is approved:

1. Check the latest applicable official KOSA publication.
2. Use `kosa-seniority` only when the publication explicitly reports the
   selected job family and seniority level.
3. Do not reinterpret an occupation average or 25th/75th wage percentile as
   entry, junior, or senior. Retain it only as an aggregate cross-check.
   Do not substitute an obsolete KOSA grade table from a different effective
   year when the current publication lacks a seniority breakdown.
4. When KOSA lacks the selected level, use `web-estimate`:
   - prefer official government wage statistics with occupation plus rank,
     career, or equivalent level;
   - otherwise require at least two independent publishers from dated salary
     surveys or current job postings.
5. Use `customer-provided` only when the user explicitly supplies and selects a
   company or contract rate for the matching role and level.

Search current sources at execution time. Prefer primary publications and record
publisher, title, URL or file location, retrieval date, covered seniority, and
compensation scope. Reject undated snippets, duplicated syndications, anonymous
single claims, and listings that do not identify the relevant level.

## 3. Normalize without hiding assumptions

For every role and source record:

- observed value and unit (`annual`, `monthly`, `daily`, or `hourly`);
- normalized monthly value and the conversion;
- currency, region, employment type, and company-size differences when material;
- whether the value is employee wage, employer labor cost, supplier cost, or
  customer billing rate.

KOSA employer-cost figures and web salary figures may include different
components. Do not compare or combine them until the compensation scopes are
made explicit. Do not add benefits, overhead, technical fee, or profit twice.

Choose the final monthly rate with a stated rule, such as the median of
comparable normalized level-specific observations. Explain exclusions and use a
confidence range when sources diverge. Store the result in `monthly_rate`,
source observations in `rate_evidence`, and the calculation in
`rate_rationale`.

## 4. Review and calculate

Present the user with:

- confirmed job family and seniority;
- each raw and normalized source value;
- why KOSA was used as the rate or only as a cross-check;
- selected monthly rate and selection rule;
- role M/M and resulting direct labor.

Wait for policy review before finalizing. Calculate direct labor from the
reviewed role-level rate multiplied by reviewed M/M, then apply the separately
approved cost rules. Keep the source and normalization tables in the basis of
estimate.
