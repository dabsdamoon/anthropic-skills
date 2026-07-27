---
name: capture-customer-outcomes
description: Capture a traceable customer outcome and contract baseline from naive requirements, emails, messages, interviews, proposals, statements of work, and contracts. Use when a user needs to preserve what a customer originally asked for, distinguish requested outcomes from detailed solution assumptions, reconstruct initial included and excluded scope, or prepare the first canonical input for an FDE estimate or change-scope analysis.
---

# Capture Customer Outcomes

Create a factual baseline without improving the customer's original request into
a requirement they never approved.

## Workflow

1. Read `../../references/interactive-review-protocol.md` completely.
2. Run GATE-0. Ask what decision the estimate should support and what product
   boundary it covers, explain relevant scenarios in plain language, and wait
   for the user's response.
3. Run GATE-1. Ask for the source boundary: files, messages, interviews, quote,
   contract, dates, intended users, outcomes, and authorized stakeholders.
4. Read `../../references/evidence-and-claim-rules.md` completely.
5. Read `references/output-contract.md` completely.
6. Preserve the customer's original wording in source records. Write editorial
   summaries separately.
7. Extract:
   - problems and desired outcomes;
   - users and decisions the product should support;
   - explicit included and excluded scope;
   - constraints, customer-provided items, assumptions, and approvals;
   - measurable success criteria when the source provides them.
8. Mark missing detail as an assumption or open issue. Do not fill it from the
   implemented product.
9. Create `customer-baseline.json` and `customer-baseline.md` with
   `status: draft` and `review.status: pending`.
10. Present the baseline, assumptions, and missing decisions. Wait for the user
    or identified stakeholder to approve or correct it. Record the real review
    reference; never fabricate approval metadata.
11. Set both document and review status to final/approved only after that
    response, then validate:

```bash
python3 "$PLUGIN_DIR/scripts/validate_input_package.py" \
  --customer-baseline "$OUTPUT_DIR/customer-baseline.json" \
  --final \
  --output "$OUTPUT_DIR/customer-baseline-verification.json"
```

Set `PLUGIN_DIR` to the plugin root and `OUTPUT_DIR` to the task output
directory before running the command.

## Completion gate

- Keep original request, editorial interpretation, and later discovery distinct.
- Record source dates and references.
- Do not claim contractual inclusion without a scope, quote, contract, or
  approval source.
- Disclose when the contract baseline is absent; a product-value estimate may
  still be possible, but an additional-payment claim will be weaker.
- Stop finalization when no customer source exists. Deliver a clearly labeled
  reconstruction draft instead.
- If the user cannot review the baseline, stop with a readiness summary. Do not
  continue into priced policy, effort allocation, or calculation.
