# Evidence and claim rules

Apply these rules to every artifact in the estimate package.

## Separate source types

Use exactly one source type for each material claim:

- `customer_request`: explicitly stated by an authorized customer source.
- `observed`: directly observed in a workflow, system, dataset, or artifact.
- `inferred`: professional interpretation that has not been confirmed as a customer request.
- `validated`: reviewed and confirmed by an identified stakeholder.
- `implemented`: demonstrated by implementation evidence.

Never rewrite an `inferred` need as a `customer_request`. A later confirmation may
create a separate `validated` record that points to the inference.

## Require provenance

Record:

- a stable source reference;
- capture time or source date;
- confidence as `confirmed`, `probable`, or `unverified`;
- whether the customer confirmed the claim;
- evidence identifiers or paths.

Prefer immutable evidence such as signed scope, dated messages, commit hashes,
test results, deployment records, and approved meeting minutes. Preserve the
customer's original wording separately from editorial summaries.

## Limit Git claims

Git proves recorded changes within the selected revision boundary. It does not
prove:

- hours or elapsed effort;
- individual productivity;
- business value;
- customer approval;
- work performed outside the repository;
- contractual entitlement to payment.

Use Git to support implementation scope and chronology. Use time records,
interviews, decisions, and contractual sources for the other claims.

## Separate evidence from commercial judgment

Label a scope item with one classification:

- `explicit-baseline`
- `derived-necessary`
- `field-validated`
- `supplier-initiated`
- `future-option`
- `unresolved`

Do not automatically bill `supplier-initiated` or `unresolved` work. A proposed
change-adjustment remains a negotiation request unless a written change approval
proves otherwise.

## Protect sensitive information

Redact personal data, customer secrets, production credentials, author email
addresses, and security-sensitive paths by default. Treat customer production
systems and datasets as read-only unless explicit authority says otherwise.
