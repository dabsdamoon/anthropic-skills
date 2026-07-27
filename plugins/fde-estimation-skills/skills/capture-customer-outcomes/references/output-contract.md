# Customer baseline output contract

Write two files from the same source set.

## `customer-baseline.json`

Follow `../../../schemas/customer-baseline.schema.json`.

Initialize `review.status` as `pending`. Set it to `approved` and record
`reviewed_by`, `reviewed_at`, and `reference` only after the reviewer has seen
the summarized baseline and responded.

Use these identifier prefixes:

- source document: `SRC-`
- outcome: `OUT-`
- explicit scope: `SCP-`
- constraint: `CON-`
- assumption: `ASM-`
- approval: `APR-`

Every outcome, scope item, constraint, and assumption requires `provenance`.
An explicit source document entry records `id`, `title`, `kind`, `location`,
and `source_date`.

## `customer-baseline.md`

Use this order:

1. Evidence boundary and document status
2. Customer's original wording
3. Problems and desired outcomes
4. Users and supported decisions
5. Explicit included scope
6. Explicit excluded scope
7. Constraints and customer-provided items
8. Assumptions and missing detail
9. Approvals and unresolved confirmation

Keep verbatim excerpts short. Link or point to the retained source rather than
copying long copyrighted or confidential material.
