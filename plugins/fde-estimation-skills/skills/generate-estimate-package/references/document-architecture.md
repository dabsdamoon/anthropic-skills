# Estimate package document architecture

## Canonical documents

Always create:

- `budgetary-estimate.md`
- `basis-of-estimate.md`
- `estimate-calculation.json`
- `project-estimate-manifest.yaml`
- `input-verification.json`
- `calculation-verification.json`
- `estimate-package-verification.json`

Create when the scenario exists:

- `change-adjustment.md`
- `remaining-work-estimate.md`

## Audience split

Budgetary estimate:

- customer problem and outcome;
- scenario purpose;
- scope and deliverables;
- price, schedule, acceptance, payment, assumptions, exclusions;
- uncertainty and validity.

Basis of estimate:

- evidence boundary;
- traceability and classifications;
- WBS and role effort;
- rate sources and cost rules;
- arithmetic reconciliation;
- risks, assumptions, and limitations.

Change adjustment:

- original baseline;
- discovered and completed delta;
- benefit or necessity;
- evidence and approval state;
- proposed amount and written-change request.

## Language guardrails

Prefer:

- “협의를 요청한다”
- “현장 발견으로 구체화되었다”
- “고객 확인이 필요하다”
- “재조달 참고값이다”

Avoid:

- “만들었으니 지급해야 한다”
- “고객이 원했다” when the source is inference
- “확정 금액” for a budgetary estimate
- “총 청구액” as a sum of independent scenarios

## Narrative clarity rubric

Before delivery, confirm:

1. The customer problem and desired outcome appear before the feature or price.
2. Every major capability shows whether it was requested, discovered, inferred,
   validated, implemented, or optional.
3. Each scenario answers one commercial question in a single sentence.
4. The budgetary estimate explains what the customer receives, the assumptions,
   and the decision still required.
5. The basis report explains how evidence became scope, effort, rate, and price.
6. Proposed changes use negotiation language; approved changes cite approval.
7. Unknowns and re-estimation triggers remain visible.
8. No unsupported marketing claim or business value is inferred from effort.
