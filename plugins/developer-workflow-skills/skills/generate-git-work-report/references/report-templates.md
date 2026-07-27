# Report templates

## External project history

Use this order unless the user's submission format requires another:

1. Document identity, report creation time with UTC offset, filename stamp, and
   evidence baseline.
2. Project purpose and delivery scope.
3. Reporting period and explicit exclusions.
4. Major milestones grouped by user or operational outcome.
5. Quantitative activity summary with careful metric definitions.
6. Validation, release state, and handoff.
7. Evidence basis and limitations.

Keep commit hashes, contributor identities, internal paths, and raw commit
messages out of the body unless they are required by the recipient. A short
evidence fingerprint is normally sufficient.

### External office story map

Use this page architecture as a starting point, then adapt it to the retained
reference:

1. Cover and executive summary: product purpose, evidence period, revision,
   one clear outcome statement.
2. Delivery scope: what changed, what was excluded, and the user or operational
   boundary.
3. Milestone narrative: 3-7 outcome-oriented phases supported by repository
   evidence.
4. Validation and handoff: tests, release markers, deployment or operating
   documentation, and known limitations.
5. Evidence basis: concise metrics, fingerprint, caveats, and source list.

Use metrics as supporting evidence, not as the story. Do not let a category
count table or commit list dominate the external report. Prefer a milestone
table, timeline, or grouped narrative when it explains progression better.

## Internal detailed work log

Use this order:

1. Report creation time with UTC offset, filename stamp, evidence snapshot, and
   collection command.
2. Completeness and repository-state warnings.
3. Aggregate metrics and metric definitions.
4. Chronological entries grouped by reporting-zone date.
5. For every commit: full evidence marker, visible short hash, subject,
   category, author, changed-file count, numstat, and representative paths.
6. Release tags, branch/ref snapshot, and validation record.
7. Interpretation notes, unresolved gaps, and supporting artifact paths.

Preserve `<!-- commit:FULL_HASH -->`, `<!-- evidence-sha256:... -->`, and
`<!-- metric:key=value -->` comments. The verifier depends on them.

### Internal office story map

Use this architecture:

1. Cover, evidence boundary, warnings, and collection identity.
2. Aggregate map: period, revision, tags, contributors, activity days, churn
   definitions, and category distribution.
3. Chronological phase summaries with decision and validation context.
4. Commit-complete work log, grouped by reporting-zone date.
5. Release/ref snapshot, verification result, limitations, and supporting
   artifact paths.

Keep one visible row or entry per commit, but place the dense commit-level
material after the explanatory phase summaries. Repeat table headers across
pages and reserve wide columns for subjects and representative paths.

## Office component mapping

- Purpose, rationale, and limitations: short prose sections.
- Executive decision or outcome: lead callout.
- Repeated milestones or commits: tables with explicit column widths.
- Chronology: timeline or dated groups.
- Verification: compact matrix or checklist.
- Definitions and evidence boundary: key-value block.
- Long commit subjects, paths, or commands: appendix-scale tables, never a
  narrow multi-paragraph cell.

Before authoring, assign a page budget. During rendering, rebalance sections
when a page contains only a callout, only the tail of a short table, or less
than one meaningful content block.

## Writing rules

- For Korean reports, apply the narrative-only `humanize-korean` gate defined
  in `SKILL.md` before canonical verification.
- Label statements as fact, interpretation, or user-provided context when the
  distinction is material.
- Prefer exact dates and revision names over words such as "recently".
- Explain why a milestone mattered; do not merely restate a commit subject.
- Separate recorded delivery from planned or uncommitted work.
- Never equate commit frequency with effort, quality, or employee performance.
