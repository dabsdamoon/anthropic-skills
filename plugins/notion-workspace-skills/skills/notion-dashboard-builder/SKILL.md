---
name: notion-dashboard-builder
description: Build or reorganize operational Notion pages by creating real databases directly under a requested root page, migrating or classifying records, and adding situation-appropriate timeline, board, calendar, and approval views. Use this skill whenever a user asks for a Notion roadmap, project hub, task board, operating timeline, approval tracker, role/area-filtered dashboard, cleaner top-level display, or replacement of linked database views with independently owned databases—even if they only say the current Notion page is cluttered or hard to navigate.
---

# Notion Dashboard Builder

Build a usable operating surface rather than a collection of links. Make the requested root page directly own the final databases, choose views that fit each workflow, and verify the user-visible records before reporting completion.

## Before writing

Read these references:

- [patterns.md](references/patterns.md) for schemas, layout choices, filters, migration, and validation.
- [runtime-compatibility.md](references/runtime-compatibility.md) for tool differences across Codex/OpenAI, Claude, Claude Code, and Cowork.

Confirm that the active Notion connection can fetch pages, create databases and records, update database attributes, query records, and create or configure views. If it cannot create views, state that limitation before changing the workspace; a database without the requested display is not a completed dashboard.

## Core contract

- Create each final database with the requested root page as its direct parent.
- Display each single-source database inline on that root page.
- Add view tabs to the actual database. Do not satisfy an independent-database request by appending linked views of another source.
- Preserve source or backup databases unless the user explicitly authorizes deletion or archival.
- Preserve migration provenance in an `Original`/`원본` URL property.
- Validate the configured views themselves, not only equivalent ad hoc queries.

## Workflow

### 1. Resolve and inspect

1. Resolve the exact root page and all possible source databases by URL or stable ID.
2. Fetch the root page, its database blocks, and relevant data sources.
3. Record:
   - root page ID and existing database block IDs;
   - database IDs, data source IDs, schemas, views, and row counts;
   - direct ancestor paths;
   - deleted or trashed state;
   - representative records, including late milestones and collaboration-only work.
4. Ask only when the root page, source of truth, or destructive scope cannot be determined safely. Otherwise state the working assumptions and proceed.

### 2. Design around how people work

Split records by interaction model, not merely by category. A useful default is:

- **Roadmap:** projects, milestones, releases, and date ranges shown as a timeline.
- **Work:** actionable tasks grouped by status on a board.
- **Approvals/checks:** decisions, external reviews, and unresolved gates in compact filtered tables.

Use fewer databases when the workflows are truly identical. Add databases only when they reduce cognitive load or serve a distinct audience.

When several functions participate, model both:

- `Primary area`/`주관 영역`: one accountable area;
- `Collaborating areas`/`협업 영역`: zero or more participating areas.

Keep internal codes in a separate property and give human-facing approval records plain-language titles.

### 3. Create actual databases on the root page

1. Insert a section heading immediately before creating each database when visual order matters.
2. Create the roadmap first when other databases relate to milestones.
3. Create every final database with the root page as its parent.
4. Make the database inline.
5. Add relations only to the newly created data source IDs.
6. Create view tabs inside the actual database, using the runtime's “existing database” or `database_id` mode rather than a “linked view on page” or `parent_page_id` mode.

Do not replace the entire root-page content after child databases exist. Full replacement can remove or trash those databases. Use exact, targeted content updates.

### 4. Migrate records safely

1. Snapshot source rows and counts before writing.
2. Classify every row into exactly one destination and compare expected totals.
3. Add every distinct select option required by the source before inserting a batch.
4. Create roadmap rows first and build a mapping from source milestone identity to new page URL.
5. Create work and approval rows with relations pointing to the new roadmap pages.
6. Copy supported page content and properties in bounded batches.
7. Preserve each source page URL in `Original`/`원본`.
8. If an old database container is deleted and cannot be restored, create a fresh database and copy accessible rows. Never build the final dashboard on a deleted container.
9. Keep sources as backups until the destination counts, relations, and views pass validation.

### 5. Configure focused views

Create the smallest useful set of views:

- Roadmap: all-record timeline and area timelines.
- Work: all-record status board and area boards.
- Approvals/checks: an attention view and area-specific incomplete tables.

Area views should usually include accountable and collaborating records:

```text
FILTER ("주관 영역" = "개발" OR "협업 영역" CONTAINS "개발")
```

For incomplete approvals:

```text
FILTER "상태" != "완료" AND
  ("주관 영역" = "개발" OR "협업 영역" CONTAINS "개발")
```

Show only the properties needed to scan and act. Put verbose completion criteria, evidence, and provenance inside the record or a secondary table.

### 6. Remove obsolete linked blocks

After the new databases pass preliminary checks:

1. Fetch the root page again.
2. Identify old linked database blocks by exact IDs.
3. Remove only those blocks with a targeted update.
4. Leave their source databases intact unless deletion or archival was explicitly requested.

### 7. Verify the user-visible result

Treat these checks as required:

1. Fetch the root page and confirm the expected database blocks are present.
2. Confirm each block uses the new database's own ID, is inline, and is not deleted.
3. Confirm obsolete linked-view block IDs are absent.
4. Fetch each new database and confirm the root page is its direct parent.
5. Compare actual and expected row counts for every destination.
6. Query named key records, especially the latest milestones or releases.
7. Execute representative configured area views and confirm collaboration-only records appear.
8. Confirm boards group by the intended status property and timelines use the intended date property.
9. Confirm relations resolve to pages in the new destination databases.

If a check fails, fix it or report the exact blocker. Do not speculate when connector evidence can answer the question directly.

## Reporting

Lead with the completed structure and include:

- root page link;
- actual database names and row counts;
- main view types and filter behavior;
- key records used to verify visibility;
- whether obsolete linked blocks were removed;
- whether source backups remain.

Never describe a linked view as an independently owned database.
