# Permission Scope — Jira Read-Only Workflow

Workflow: read my most-recent Jira ticket; do nothing else to Jira.

## Explicit Read

- jira: `get_issue`, `search_issues`   (read my most-recent ticket; read only)
  - No file contents outside the ticket, no other MCP server

## Explicit Write

- jira: BLOCKED — `add_comment`, `create_issue`, `transition_issue`, `update_issue` all denied
  - There is no write in this workflow. Every Jira mutation is off.

## Explicit Blocks

- jira: `add_comment`, `create_issue`, `transition_issue`, `update_issue`, delete, admin
- all other MCP servers and tools

---

> **TO-VERIFY (dry-run):** the tool names above are the LIKELY Atlassian remote-MCP names.
> Smarsh's config may prefix them (e.g. `jira_get_issue`). Confirm the exact names via `/mcp`
> before relying on the deny list — the block only fires if the deny entry matches the real
> tool name the agent would call. The `mcp__jira__<tool>` prefix in `.claude/settings.local.json`
> also depends on the exact server key in `.mcp.json` (here `jira`).
</content>
