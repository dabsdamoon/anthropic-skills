# Interactive Review Protocol

Estimation is a joint decision process. Repository evidence can describe a
product, but it cannot choose the customer's value question, commercial policy,
scope classification, or effort on the user's behalf.

Follow every gate in order. A gate is blocking when the required decision is
missing. Do not treat `draft` status, an ignored output file, or a reversible
write as permission to invent user-owned inputs.

## GATE-0: Confirm the estimation intent

Before choosing a scenario or creating a priced artifact:

1. Ask what decision the estimate should support and what product boundary it
   covers.
2. Explain scenario choices in plain language before using internal identifiers:
   - cost to build the same product now (`replacement-value`);
   - cost to finish agreed remaining work (`remaining-work`);
   - proposed adjustment for changed or additional work
     (`change-adjustment`).
3. Wait for the user's response. Do not assume that a repository review means
   the user wants a rebuild or replacement valuation.

Read-only repository inspection may begin before this response when it only
collects evidence. It must not select a scenario, M/M, rate, margin, risk, or
commercial entitlement.

## GATE-1: Review the customer baseline

Ask for the smallest useful set of missing facts: the original request or source,
intended users, desired outcomes, included and excluded boundaries, constraints,
success measures, and authorized approver.

Present a concise baseline draft with assumptions and missing decisions called
out. Wait for review. Record approval in `customer-baseline.review`; otherwise
keep the artifact in `draft` with `review.status: pending`.

## GATE-2: Review discoveries and solution decisions

Separate observed facts, customer statements, FDE inferences, validated findings,
and implementation facts. Present material discoveries, solution choices,
alternatives, and price-affecting open questions in plain language.

Wait for the user or an identified stakeholder to confirm or correct the
material judgments. Record the result in `field-discovery.review`. Repository
implementation is not evidence that the customer approved a need.

## GATE-3: Review the estimation policy

Ask the user to choose or provide every commercial input that is not fixed by a
cited source:

- jurisdiction, currency, rate basis, and effective period;
- estimation method and effort unit;
- overhead, technical fee, profit, risk, discount, and tax;
- rounding, confidence range, estimate validity, and re-estimation triggers.

Zero is a valid explicit choice. Silence is not. Present the complete policy and
its arithmetic order, then wait for review. Record approval in
`estimation-policy.review`.

## GATE-4: Review scope classification and effort

Present the traceable work breakdown before calculating money. For every
material item show:

- plain-language capability or work product;
- scope classification and rationale;
- scenario, role, M/M, and included or excluded state;
- customer-confirmation and approval reference;
- assumptions or unresolved questions that could change price.

Wait for the user or identified estimate owner to review the classifications
and effort. Apply corrections and present the changed portion again. Record
approval in `scope-traceability.review`.

## GATE-5: Calculate and deliver

Calculate monetary scenarios only after Gates 0–4 are complete and every
human-owned final artifact contains an approved review record. A valid approval
record has:

```json
{
  "review": {
    "status": "approved",
    "reviewed_by": "identified person or accountable role",
    "reviewed_at": "ISO-8601 timestamp",
    "reference": "chat, meeting, email, ticket, or approval record"
  }
}
```

Do not fabricate approval metadata. A single user reply may approve a complete
artifact when the reviewed contents are clear; record that reply as the
reference. Editorial verification of `as-built-evidence` does not replace any
of the four human review records.

If the reviewer is unavailable or a material decision remains unanswered,
deliver a readiness summary and draft artifacts. List the exact decisions still
needed. Do not calculate or render monetary estimate documents.

## Conversation rules

- Ask before estimating whenever the answer belongs to the user or stakeholder.
- Ask a small, coherent batch of questions and explain why each affects the
  estimate.
- Use the user's product language first; introduce internal scenario names only
  as traceability labels.
- Clearly label evidence, assumptions, recommendations, and decisions.
- When the user corrects a premise, stop that line of estimation and return to
  the affected gate.
