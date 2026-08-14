# Runtime compatibility

## Portable capability contract

This skill follows the Agent Skills folder format and must not depend on one vendor's tool prefix. Map the workflow to the active runtime's Notion connector or MCP tools.

The connection must support:

- fetching pages, databases, data sources, and view definitions;
- creating a database under a specified page;
- changing inline/full-page display when necessary;
- creating and updating database records;
- creating or configuring database views;
- querying records and saved views;
- targeted page-content updates.

The skill does not provide Notion credentials or install a Notion connector.

## Codex and OpenAI runtimes

- Use the installed Notion app/connector tools.
- Read any connector-provided Markdown and view-DSL specifications before writes.
- When the connector distinguishes `database_id` from `parent_page_id`, use `database_id` to add tabs to the real database. `parent_page_id` creates a linked view block.
- Use data source IDs for schema and record operations and database IDs for database-owned views.

## Claude Code

- Use the configured Notion MCP server or plugin tools.
- Tool names and argument shapes may differ from Codex. Preserve the ownership and validation invariants instead of copying a vendor-specific call literally.
- Install the repository plugin for automatic discovery, or place the standalone skill folder in a configured Claude skills directory.

## Claude and Cowork

- Use the packaged `.skill` artifact when the product supports skill upload/import.
- Ensure the session also has an authorized Notion integration with write access to the requested root page.
- In headless Cowork sessions, verify through connector fetches and saved-view queries. Do not claim visual inspection unless the UI was actually rendered.

## Capability gaps

If the runtime can create records but cannot create or configure saved views, stop before presenting the result as finished. Explain which capability is missing and retain any already-created data safely. Do not compensate by silently creating linked views when the user requested root-owned databases.
