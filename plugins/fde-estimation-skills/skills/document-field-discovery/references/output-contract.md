# Field discovery output contract

## `field-discovery.json`

Follow `../../../schemas/field-discovery.schema.json`.

Use these identifier prefixes:

- discovery: `DSC-`
- solution decision: `DEC-`
- open question: `QUE-`

Each discovery references zero or more customer outcome IDs. Zero is valid only
when the finding exposes a new potential need; explain the missing link.

Use `validation_status`:

- `unverified`
- `customer-reviewed`
- `customer-confirmed`

Do not set `customer_confirmed: true` in provenance unless
`validation_status` is `customer-confirmed`.

## `field-discovery.md`

Use this order:

1. Discovery purpose and evidence boundary
2. Observed workflow and data constraints
3. Customer statements during delivery
4. FDE inferences and confidence
5. Solution alternatives and decisions
6. Prototype or demo feedback
7. Customer-confirmed findings
8. Open questions and estimate impact
