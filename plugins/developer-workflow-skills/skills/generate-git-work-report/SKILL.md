---
name: generate-git-work-report
description: Generate repeatable, timestamped, evidence-backed project execution histories and detailed work logs from a local Git repository, including conservative humanize-korean editing for Korean narrative and polished reference-matched DOCX/PDF deliverables. Use when a user asks for a Git-based 수행이력, 업무일지, work log, project history, delivery report, audit trail, external project summary, internal evidence report, or professionally formatted office report derived from commit, merge, tag, author, date, and file-change history.
---

# Generate Git Work Report

Create two reports from one immutable Git evidence snapshot:

- An external summary that explains scope, milestones, outcomes, and validation
  without exposing unnecessary internal detail.
- An internal work log that preserves chronological commit-level traceability.

Treat Git as evidence of recorded change, not proof of hours worked, effort,
individual productivity, business value, or work performed outside the
repository.

Keep the evidence workflow deterministic. Treat editorial interpretation and
office-document design as separate, explicit stages with their own gates.

## Workflow

### 1. Define the evidence boundary

Determine or state these inputs before collecting evidence:

- Repository path.
- Revision scope. Default to the current `HEAD`; use `--all-refs` only when the
  user explicitly wants unmerged or orphaned branch activity included.
- Optional date and author filters.
- Reporting timezone. Default to `UTC` when the user gives no locale.
- Output root, project name, filename-safe project slug, and language.
- Report creation time captured once in the reporting timezone.
- Whether author email addresses may be retained. Keep them redacted by
  default.

Do not silently combine `HEAD`, all refs, the working tree, GitHub activity, or
chat history. Report each evidence source separately.

#### Output naming contract

Capture the report creation time once when the report run begins. Keep the same
timestamp for every file in that report package, including later DOCX and PDF
artifacts. Treat it as the report's authored/saved time; do not recalculate it
per file.

- Human-readable value: ISO 8601 with seconds and UTC offset, such as
  `2026-07-27T10:45:12+09:00`.
- Filename stamp: `YYYYMMDDTHHMMSS±HHMM`, such as
  `20260727T104512+0900`.
- Project slug: lowercase ASCII letters, digits, and hyphens only.
- Timestamp source: current time in the reporting timezone. Do not substitute
  the last commit time, evidence-period end, or filesystem modification time.

Use this package layout:

```text
<output-root>/<project-slug>-work-report-<stamp>/
  <project-slug>-git-evidence-<stamp>.json
  <project-slug>-external-project-history-<stamp>.md
  <project-slug>-internal-work-log-<stamp>.md
  <project-slug>-verification-<stamp>.json
```

Use the same stamped Markdown stems for DOCX and PDF. Name supporting office
files `<project-slug>-template-audit-<stamp>.md` and
`<project-slug>-office-verification-<stamp>.json`.

Set the path variables from the same immutable values:

```text
OUTPUT_DIR=<output-root>/<project-slug>-work-report-<stamp>
EVIDENCE_PATH=<output-dir>/<project-slug>-git-evidence-<stamp>.json
EXTERNAL_NAME=<project-slug>-external-project-history-<stamp>.md
INTERNAL_NAME=<project-slug>-internal-work-log-<stamp>.md
EXTERNAL_PATH=<output-dir>/<external-name>
INTERNAL_PATH=<output-dir>/<internal-name>
VERIFICATION_PATH=<output-dir>/<project-slug>-verification-<stamp>.json
EXTERNAL_STEM=<external-name without .md>
INTERNAL_STEM=<internal-name without .md>
TEMPLATE_AUDIT_PATH=<output-dir>/<project-slug>-template-audit-<stamp>.md
OFFICE_VERIFICATION_PATH=<output-dir>/<project-slug>-office-verification-<stamp>.json
```

Set and reuse `REPORT_CREATED_AT`, `REPORT_STAMP`, `PROJECT_SLUG`, and every
path above before collection.
Include the human-readable report creation time in the identity block of both
reports and on each office cover. If a delivered report is revised, create a
new timestamped package instead of overwriting the previous package. When a
required submission template forbids timestamped filenames, preserve the
timestamp in the containing directory and document identity, and disclose the
exception.

### 2. Collect the canonical evidence

Set `SKILL_DIR` to this skill directory, then run:

```bash
python3 "$SKILL_DIR/scripts/collect_git_evidence.py" \
  --repo "$REPO_PATH" \
  --ref HEAD \
  --timezone +09:00 \
  --output "$EVIDENCE_PATH"
```

Use an IANA zone such as `Asia/Seoul` when timezone data is available, or a
fixed offset such as `+09:00` for a portable snapshot. Use `--since`,
`--until`, or `--author` only when requested. Use
`--include-author-email` only with an explicit need for personally identifiable
information.

Stop and disclose the limitation when the collector reports a shallow
repository, truncation, an unresolved revision, or an empty scope. Do not fill
history gaps with inference.

### 3. Read the evidence and repository context

Read:

- `references/interpretation-rules.md` before making narrative claims.
- `references/report-templates.md` before editing either report.
- `references/evidence-schema.md` when consuming fields beyond the summary
  metrics or when extending a script.

Inspect the repository's README, agent guidance, product state, ADRs, release
notes, and substantive merge messages. Use these sources to explain what the
work means. Keep every number, date, tag, and commit claim anchored to
`$EVIDENCE_PATH`.

### 4. Generate deterministic first drafts

Run:

```bash
python3 "$SKILL_DIR/scripts/render_work_reports.py" \
  --evidence "$EVIDENCE_PATH" \
  --output-dir "$OUTPUT_DIR" \
  --project-name "$PROJECT_NAME" \
  --language ko \
  --external-name "$EXTERNAL_NAME" \
  --internal-name "$INTERNAL_NAME"
```

This creates:

- `$EXTERNAL_PATH`
- `$INTERNAL_PATH`

The internal draft contains one machine-readable marker for every commit in
scope. Preserve these markers while editing so coverage remains verifiable.

### 5. Build the report story

Improve the deterministic draft without changing its evidence contract:

- External report: add the product purpose, delivery scope, major milestones,
  user or operational outcomes, validation, exclusions, and a concise evidence
  basis.
- Internal report: add decision context, verification details, incident or
  release links, and fact-versus-interpretation labels where useful.
- Prefer grouped milestones over a raw commit list in the external report.
- Keep exact commit hashes and chronological coverage in the internal report.
- Remove internal paths, author identities, security-sensitive messages, and
  customer data from the external version unless explicitly authorized.

Before office authoring, write a short story map for each report:

- External: cover decision, executive summary, milestone narrative,
  quantitative evidence, validation/handoff, limitations.
- Internal: evidence boundary, aggregate map, chronological phases,
  commit-complete appendix, warnings and supporting artifacts.
- Assign a page budget to each major section. Do not convert the Markdown
  linearly without deciding which content belongs in prose, callouts, tables,
  timelines, or appendices.
- Add `REPORT_CREATED_AT` to the visible identity block of both reports. Keep
  the filename stamp and visible timestamp equivalent.

Read `references/report-templates.md` for the required content architecture.

Do not claim elapsed effort, staffing level, completion percentage, cost, or
causality from commit counts alone.

### 6. Humanize Korean narrative

Run this gate only when the report language is Korean. English reports skip it.

1. Load and follow the `humanize-korean` skill. Use `장르: 리포트` and
   `강도: 보수`.
2. Run it from a task-local staging directory so its `_workspace` files do not
   pollute the source repository.
3. Give it only editorial narrative: the external purpose, scope, milestone,
   validation, handoff, and limitation prose; and the internal evidence
   boundary, phase summaries, decision context, validation notes, and
   interpretation prose.
4. Exclude the entire commit-complete appendix and protect all HTML evidence
   comments, hashes, commit subjects, author strings, tags, refs, dates,
   timestamps, metrics, table values, commands, paths, code, formulas, quotes,
   product names, and technical abbreviations.
5. Merge only the rewritten narrative spans back into the canonical Markdown.
   Keep `HUMANIZE-SUMMARY` outside the canonical reports as a supporting
   artifact.
6. Review the diff for changed facts or evidence language. Roll back any edit
   that adds, removes, strengthens, or weakens a claim.

Humanization is a conservative editing pass, not a different evidence source
and not permission to expand content. If `humanize-korean` is unavailable, do
not claim that the Korean report is final; disclose the missing dependency and
retain the deterministic drafts.

### 7. Verify the canonical reports

Run after all Markdown edits:

```bash
python3 "$SKILL_DIR/scripts/verify_work_reports.py" \
  --evidence "$EVIDENCE_PATH" \
  --external "$EXTERNAL_PATH" \
  --internal "$INTERNAL_PATH" \
  --output "$VERIFICATION_PATH"
```

The command must pass before office authoring. It checks:

- Evidence fingerprints in both reports.
- Metric consistency.
- One-to-one internal commit coverage.
- Duplicate or unknown commit markers.
- Placeholders.
- Shallow or truncated evidence.

If editorial changes intentionally alter a machine-generated number, recollect
or rerender instead of hand-editing the metric marker.

### 8. Create DOCX or PDF when requested

Treat the Markdown reports and `$EVIDENCE_PATH` as the canonical record.
Read `references/office-delivery.md` completely before creating an office
artifact. Select exactly one mode:

- **Reference-first mode:** mandatory when the user supplies or points to a
  DOCX, PDF, report family, or visual example. The retained reference controls
  page geometry, typography, colors, cover, tables, headers, footers, spacing,
  and component rhythm. Do not read or apply the neutral theme first.
- **Neutral fallback mode:** use only when there is no visual reference. Read
  `assets/neutral-report-theme.json` and apply it as a complete token set.

In reference-first mode:

1. Use the available document and PDF skills.
2. Retain the reference unchanged and render every reference page.
3. Create `$TEMPLATE_AUDIT_PATH` as a task-local record of reference hashes,
   page count, geometry, typography, palette, tables, page furniture, content
   flow, and intentional brand/content substitutions.
4. Reuse the reference style system faithfully. Replace its product identity,
   confidential data, quoted prices, and proprietary content with the target
   project's material; do not weaken template fidelity merely because the
   identity changes.
5. Prefer a sibling DOCX as the implementation authority when the user points
   to a PDF. If only a PDF exists, distill the rendered pages before authoring.

For both modes:

1. Keep Markdown, DOCX, and PDF basenames/version labels aligned. Preserve the
   exact `REPORT_STAMP` in every filename.
2. Use the DOCX as the editable office source and generate the PDF from the
   latest DOCX.
3. Render every final page. Iterate after each meaningful layout change.
4. Reject accidental blank pages, isolated callouts, continuation-only pages,
   short tables split across pages, clipped text, broken glyphs, inconsistent
   headers/footers, unresolved placeholders, and raw Markdown residue.
5. Inspect at 100% zoom. A contact sheet is navigation, not a substitute for
   per-page review.
6. Run the office preflight after visual inspection:

```bash
python3 "$SKILL_DIR/scripts/verify_office_delivery.py" \
  --pair "external=$OUTPUT_DIR/$EXTERNAL_STEM.docx,$OUTPUT_DIR/$EXTERNAL_STEM.pdf" \
  --pair "internal=$OUTPUT_DIR/$INTERNAL_STEM.docx,$OUTPUT_DIR/$INTERNAL_STEM.pdf" \
  --reference-mode \
  --template-audit "$TEMPLATE_AUDIT_PATH" \
  --visual-qa-confirmed \
  --output "$OFFICE_VERIFICATION_PATH"
```

Omit `--reference-mode` and `--template-audit` only for neutral fallback mode.
The preflight complements, but never replaces, visual inspection.

## Delivery checklist

- State the repository, revision scope, period, timezone, and evidence
  fingerprint.
- State the report creation time and confirm that every delivered filename uses
  the same reporting-zone timestamp.
- Distinguish external summary from internal evidence.
- Disclose shallow clones, filters, missing refs, squashes, rebases, and other
  known limitations.
- Confirm both Markdown evidence verification and office preflight results.
- Confirm final DOCX/PDF page counts and full-page visual QA.
- State whether reference-first or neutral fallback mode was used.
- For Korean reports, confirm that `humanize-korean` ran in conservative report
  mode on narrative spans only and that evidence verification passed afterward.
- Keep generated reports outside the source repository unless the user
  specifies a tracked documentation path.
