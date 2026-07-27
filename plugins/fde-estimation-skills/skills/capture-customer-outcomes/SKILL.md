---
name: capture-customer-outcomes
description: Capture a traceable customer outcome and contract baseline from naive requirements, emails, messages, interviews, proposals, statements of work, and contracts. Use when a user needs to preserve what a customer originally asked for, distinguish requested outcomes from detailed solution assumptions, reconstruct initial included and excluded scope, or prepare the first canonical input for an FDE estimate or change-scope analysis.
---

# Capture Customer Outcomes

Create a factual baseline without improving the customer's original request into
a requirement they never approved.

## Workflow

1. Define the source boundary: files, messages, interviews, quote, contract,
   dates, and authorized stakeholders.
2. Read `../../references/evidence-and-claim-rules.md` completely.
3. Read `references/output-contract.md` completely.
4. Preserve the customer's original wording in source records. Write editorial
   summaries separately.
5. Extract:
   - problems and desired outcomes;
   - users and decisions the product should support;
   - explicit included and excluded scope;
   - constraints, customer-provided items, assumptions, and approvals;
   - measurable success criteria when the source provides them.
6. Mark missing detail as an assumption or open issue. Do not fill it from the
   implemented product.
7. Create `customer-baseline.json` and `customer-baseline.md`.
8. Set `status` to `draft` until every material claim has provenance and the
   baseline has been reviewed. Set it to `final` only when ready for downstream
   reconciliation.
9. Validate the artifact:

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
