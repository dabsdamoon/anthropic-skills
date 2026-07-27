# Office delivery quality

Use this reference only when creating DOCX or PDF work reports.

## Contents

- [1. Select the design authority](#1-select-the-design-authority)
- [2. Distill the retained reference](#2-distill-the-retained-reference)
- [3. Author from a story map](#3-author-from-a-story-map)
- [4. Build and render](#4-build-and-render)
- [5. Reject these defects](#5-reject-these-defects)
- [6. Complete the two quality gates](#6-complete-the-two-quality-gates)

## 1. Select the design authority

### Reference-first mode

Use whenever the user supplies or points to a DOCX, PDF, report family, or
visual example. The reference wins over the neutral fallback for:

- Page size, orientation, and margins.
- Font family, scale, color, and heading ladder.
- Cover composition and metadata treatment.
- Table borders, fills, padding, alignment, and width ratios.
- Callouts, headers, footers, page numbers, and whitespace rhythm.
- Section sequencing and density.

Reuse the visual system, not the source identity or commercial content. Replace
logos, product names, customers, prices, confidential text, and project facts
with the target project's approved material.

### Neutral fallback mode

Use only when no reference exists. Read `assets/neutral-report-theme.json` and
resolve every token before authoring. Do not mix the fallback palette or A4
geometry into a reference-first document.

## 2. Distill the retained reference

Keep the reference unchanged. Render and inspect every page, then write the
task-local stamped template audit at `$TEMPLATE_AUDIT_PATH` containing:

- Absolute reference path, SHA-256, format, and page count.
- Page geometry and section behavior.
- Fonts, sizes, colors, and emphasis rules.
- Cover, metadata, tables, callouts, header, and footer.
- Content flow and typical page density.
- Mapping from reference components to external and internal reports.
- Intentional deviations for branding, privacy, or unavailable assets.

Prefer a sibling DOCX when a PDF and DOCX share the same report version. Use
the DOCX package for implementation and the PDF for visual comparison.

## 3. Author from a story map

Do not perform a linear Markdown-to-office conversion.

- Preserve Markdown and evidence JSON as canonical sources.
- Convert purpose and rationale to prose, decisions to callouts, repeated
  records to tables, and chronology to dated groups or timelines.
- Keep the external report outcome-oriented and concise.
- Put commit-complete traceability in the internal report after explanatory
  phase summaries.
- Reserve wide table columns for subjects and paths; keep dates, hashes,
  counts, and statuses compact.
- Assign a page budget before building. Adjust it when actual rendering shows
  a sparse or overloaded page.

Use versioned, aligned basenames such as:

```text
project-external-project-history-20260727T104512+0900.md
project-external-project-history-20260727T104512+0900.docx
project-external-project-history-20260727T104512+0900.pdf
```

The timestamp is the package-wide `REPORT_STAMP` captured in the reporting
timezone. Do not derive separate timestamps from DOCX conversion or PDF export
times.

## 4. Build and render

Use the document skill for DOCX authoring and the PDF skill for PDF inspection.
The latest DOCX is the editable office source. Generate the PDF from that
DOCX, not from an unrelated renderer.

After every meaningful layout change:

1. Render the DOCX to page PNGs and PDF.
2. Inspect every PNG at 100% zoom.
3. Compare cover, component rhythm, table treatment, and page furniture with
   the retained reference.
4. Fix the source and repeat.

Contact sheets help navigate but do not satisfy full-page inspection.

## 5. Reject these defects

- An accidental blank page or a page containing only an orphaned callout.
- A continuation-only page created by splitting a short table.
- A heading stranded at the bottom without meaningful following content.
- Clipped text, missing glyphs, overlapping content, or raw Markdown syntax.
- Narrow narrative columns, boundary-hugging cells, or unreadably small type.
- Inconsistent headers, footers, document IDs, versions, or page numbers.
- Reference branding, prices, customer data, internal paths, or author identity
  leaking into the external report.
- Different facts, evidence fingerprints, or version labels across Markdown,
  DOCX, and PDF.

When a short table would leave a mostly empty continuation page, move the table
as a unit, shorten it, reduce surrounding content, or move detail to an
appendix. Do not accept the split merely because the renderer allows it.

## 6. Complete the two quality gates

1. Run `verify_work_reports.py` against the canonical Markdown and evidence.
2. Run `verify_office_delivery.py` after visual QA.

The office preflight checks packaging, placeholders, PDF page readability,
sparse/blank-page signals, template-audit presence, and explicit visual-QA
confirmation. It does not replace human visual inspection.
