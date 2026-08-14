# Notion dashboard patterns

## Contents

- Ownership test
- Layout selection
- Reusable schemas
- View recipes
- Migration checklist
- Validation checklist
- Failure recovery

## Ownership test

An actual database used by the dashboard should satisfy all of these:

1. The requested root page is its direct parent.
2. Fetching the database shows that root page in its direct ancestor path.
3. The root page contains a database block using that database's own ID.
4. The database is inline and is not marked deleted.
5. Its tabs are views owned by that database.

A view appended to a page while referencing a separately owned data source is a linked view. Use one only when the user explicitly wants a reusable view of a central source database.

## Layout selection

| Work shape | Primary view | Useful secondary views |
| --- | --- | --- |
| Milestones or releases with dates/ranges | Timeline | All-record table, area timelines |
| Tasks moving through states | Board grouped by status | All-record table, area boards |
| Approvals, risks, external reviews | Filtered table | Area-specific incomplete tables |
| Events concentrated on calendar dates | Calendar | Table or timeline |
| Small reference catalog | Table or gallery | Category-specific tables |

Place the most frequently used database first. Keep background documents and source archives in a separate section rather than between operating views.

## Reusable schemas

Adapt property names and options to the user's language and organization.

### Roadmap

- Title
- Type: project, milestone, release
- Date range
- Status
- Project
- Primary area
- Collaborating areas
- Responsible roles or people
- Dependencies
- Completion criteria
- Verification result and evidence
- Completion date
- Blocked and block reason
- Related document
- Original URL

### Work

- Title
- Date range or due date
- Status
- Project
- Primary area
- Collaborating areas
- Responsible roles or people
- Related milestones
- Dependencies
- Completion criteria
- Verification result and evidence
- Blocked and block reason
- Original URL

### Approval/check

- Plain-language title
- Machine/internal code
- Date or decision deadline
- Status
- Project
- Primary area
- Collaborating areas
- Approval roles or people
- Related milestones
- Preconditions
- Approval condition
- Verification result and evidence
- Blocked and block reason
- Original URL

Create the roadmap first. Prefer one-way relations from work and approval databases unless the user needs reverse rollups.

## View recipes

Read the active connector's view-configuration documentation before using these examples. Translate the intent if the runtime uses structured arguments instead of a text DSL.

### Roadmap timeline

```text
TIMELINE BY "날짜";
SORT BY "날짜" ASC;
SHOW "이름", "상태", "주관 영역", "협업 영역", "구분"
```

### Area timeline

```text
TIMELINE BY "날짜";
FILTER ("주관 영역" = "개발" OR "협업 영역" CONTAINS "개발");
SORT BY "날짜" ASC;
SHOW "이름", "상태", "주관 영역", "협업 영역", "구분"
```

### Work board

```text
GROUP BY "상태";
SORT BY "날짜" ASC;
SHOW "이름", "날짜", "주관 영역", "협업 영역", "관련 마일스톤"
```

### Area work board

```text
GROUP BY "상태";
FILTER ("주관 영역" = "개발" OR "협업 영역" CONTAINS "개발");
SORT BY "날짜" ASC;
SHOW "이름", "날짜", "주관 영역", "협업 영역", "관련 마일스톤"
```

### Attention view

```text
FILTER "상태" != "완료" AND
  ("차단됨" = TRUE OR "검증 결과" IN ("검증 대기", "실패"));
SORT BY "날짜" ASC;
SHOW "이름", "코드", "날짜", "상태", "주관 영역", "검증 결과", "차단됨"
```

An empty attention view can be healthy. Also provide area-specific incomplete views so people can find upcoming approvals before they become blocked.

## Migration checklist

- Fetch the source schema and rows.
- Count rows by type before classifying.
- Record every source page ID and URL.
- Create destination schemas.
- Add missing select options before inserting rows.
- Insert roadmap records and build source-to-new-URL mappings.
- Insert work and approval records with new relations.
- Compare destination totals with classification totals.
- Inspect samples with empty dates, date ranges, multi-select values, completed dates, and URLs.
- Keep source databases as backups until cleanup is explicitly approved.

## Validation checklist

- Root fetch contains the expected final database blocks.
- Expected blocks have new database IDs, inline display, and no deleted marker.
- Old linked block IDs do not appear.
- Each database fetch shows the root page as direct parent.
- Destination counts match expected counts.
- Named late-stage milestones or releases exist.
- Representative area views return primary and collaboration-only records.
- Boards group by status.
- Timelines use the intended date property.
- Approval views omit completed items where intended.
- Relations resolve to new destination pages.

## Failure recovery

- If an insert fails on a select value, inspect distinct source values, add destination options, and retry only after verifying whether the failed batch wrote any rows.
- If a database is in trash and cannot be restored, create a new database and migrate accessible rows.
- If a root-page update would delete child databases, stop and use an exact targeted replacement.
- If a browser session is unavailable, fetch page/database structure and execute actual views through the connector. State what was verified without claiming screenshot inspection.
- If a filter is suspect, execute that exact saved view and inspect named records rather than relying only on an equivalent ad hoc query.
