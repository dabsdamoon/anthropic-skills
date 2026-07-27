---
name: generate-estimate-package
description: Generate and verify an evidence-backed FDE estimate package from finalized customer baseline, field discovery, as-built evidence, estimation policy, and scope traceability artifacts. Use when a user asks for a budgetary estimate, 개산견적서, basis of estimate, 견적산정근거서, replacement valuation, remaining-work estimate, additional-work adjustment request, or a consistent Markdown, DOCX, and PDF estimate family.
---

# Generate Estimate Package

Generate every monetary document from one canonical calculation. Never edit
totals independently in prose.

## Workflow

1. Read `../../references/interactive-review-protocol.md` completely.
2. Read `../../references/evidence-and-claim-rules.md` completely.
3. Read `../../references/scenario-and-calculation-rules.md` completely.
4. Read `references/document-architecture.md` completely.
5. Run GATE-5. Require all five canonical inputs in final status and approved
   human review records for customer baseline, field discovery, estimation
   policy, and scope traceability.
6. If a review or material decision is missing, ask the responsible person and
   wait. Deliver a readiness summary and drafts when no answer is available; do
   not calculate or render monetary documents.
7. Validate the complete input package:

```bash
python3 "$PLUGIN_DIR/scripts/validate_input_package.py" \
  --customer-baseline "$INPUT_DIR/customer-baseline.json" \
  --field-discovery "$INPUT_DIR/field-discovery.json" \
  --as-built-evidence "$INPUT_DIR/as-built-evidence.json" \
  --estimation-policy "$INPUT_DIR/estimation-policy.yaml" \
  --scope-traceability "$INPUT_DIR/scope-traceability.json" \
  --final \
  --output "$OUTPUT_DIR/input-verification.json" \
  --manifest "$OUTPUT_DIR/project-estimate-manifest.yaml"
```

8. Stop on validation errors. Do not repair source claims in the final document.
9. Calculate all scenarios:

```bash
python3 "$PLUGIN_DIR/scripts/calculate_estimate.py" \
  --scope-traceability "$INPUT_DIR/scope-traceability.json" \
  --estimation-policy "$INPUT_DIR/estimation-policy.yaml" \
  --output "$OUTPUT_DIR/estimate-calculation.json" \
  --verification "$OUTPUT_DIR/calculation-verification.json"
```

10. Render the canonical Markdown family:

```bash
python3 "$PLUGIN_DIR/scripts/render_estimate_package.py" \
  --calculation "$OUTPUT_DIR/estimate-calculation.json" \
  --customer-baseline "$INPUT_DIR/customer-baseline.json" \
  --field-discovery "$INPUT_DIR/field-discovery.json" \
  --as-built-evidence "$INPUT_DIR/as-built-evidence.json" \
  --scope-traceability "$INPUT_DIR/scope-traceability.json" \
  --estimation-policy "$INPUT_DIR/estimation-policy.yaml" \
  --output-dir "$OUTPUT_DIR"
```

11. Improve narrative clarity without changing fingerprint markers, scenario
   names, amounts, evidence status, or the legal caution.
12. Verify the package:

```bash
python3 "$PLUGIN_DIR/scripts/verify_estimate_package.py" \
  --calculation "$OUTPUT_DIR/estimate-calculation.json" \
  --output-dir "$OUTPUT_DIR" \
  --output "$OUTPUT_DIR/estimate-package-verification.json"
```

## Office delivery

Treat Markdown and structured inputs as canonical. When DOCX or PDF is
requested:

- use available document and PDF skills;
- use reference-first design when the user supplies an example;
- otherwise apply `assets/neutral-report-theme.json`;
- use DOCX as the editable office source and create PDF from the latest DOCX;
- retain the scenario relationship and calculation fingerprint in document
  metadata or an audit note;
- render and visually inspect every page;
- re-run amount checks after office conversion.

Do not make another plugin a hard dependency. If office tools are unavailable,
deliver the verified Markdown package and state the limitation.

## Completion gate

- Never add independent scenarios into one amount due.
- Describe a proposed change-adjustment as a negotiation request.
- Keep unverified assumptions and re-estimation triggers visible.
- Do not use `draft` status as permission to invent missing commercial inputs.
- Require calculation and package verification to pass before delivery.
