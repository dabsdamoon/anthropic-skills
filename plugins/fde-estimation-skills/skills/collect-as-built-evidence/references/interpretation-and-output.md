# As-built interpretation and output

## Evidence priority

Prefer:

1. Accepted release or deployment evidence
2. Tests and domain documentation tied to code
3. Reviewed merge or pull-request context
4. Commit and file history
5. Uncommitted working-tree state, clearly separated

## Implementation item boundary

Group changes by delivered capability or technical work product, not by commit.
A useful item can be independently described, verified, and connected to a
customer outcome or FDE decision.

Use identifier prefix `IMP-`.

Follow `../../../schemas/as-built-evidence.schema.json`.

## Markdown order

1. Evidence boundary and fingerprint
2. Product purpose and architecture context
3. Delivered capabilities
4. Data and domain logic
5. Quality, deployment, and operations
6. Reused versus new work
7. Partial and remaining work
8. Evidence limitations

Keep hashes and internal paths in the evidence record. Redact them from a
customer-facing summary unless they add necessary auditability.
