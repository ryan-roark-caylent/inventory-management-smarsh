# Permission Scope — CI-to-Jira Workflow

Workflow: read the failing CI check on a PR, then open one Jira issue with the diagnosis.

## Explicit Read

- github: `get_pull_request`, `list_check_runs_for_ref` (or equivalent CI check status tool)
  - Scope: repo `inventory-management-smarsh` ONLY
  - No other repos, no file contents, no branch list

## Explicit Write

- jira: `create_issue`
  - Scope: project `AEP` ONLY (one project, one create call)
  - No transitions, no updates, no deletes

## Explicit Blocks

- github: `merge_pull_request`, `delete_branch`, `create_branch`, any other repo
- jira: `transition_issue`, `delete_issue`, `update_issue`, any other project, admin operations
- All other MCP tools not listed above
