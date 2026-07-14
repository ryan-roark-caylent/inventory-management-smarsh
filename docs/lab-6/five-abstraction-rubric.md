# Five-Abstraction Rubric

Use this matrix to decide which customization layer fits a recurring workflow.

| Abstraction | When it loads | Who triggers it | Context cost | Best fit |
|---|---|---|---|---|
| **CLAUDE.md** | Every session, automatically | No one — always resident | Counts against context window every turn | Always-on guidance every teammate needs on every request (formatting rules, project conventions, coding standards) |
| **Skill** | Description loads at session start; body loads after skill fires | Claude (implicit, via description match) or you (explicit `/name`) | Body costs tokens only when invoked | An occasional, invocable procedure with a clear trigger phrase (generate tests, write a PR description, review a diff) |
| **Hook** | Session start; fires on a tool event | The tool event (PostToolUse, PreToolUse) — not a person | Logic runs outside the context window; its output can be fed back in | Logic that must run automatically on a tool event, with no human effort, and where you want the runtime work off Claude's turn (only the result enters context) |
| **Subagent** | On demand, spun up by Claude | Claude (orchestrator decides) | Own context window; returns a summary | Long-running or parallel work that benefits from isolation (crawl a repo, run a multi-step analysis, explore options in parallel) |
| **MCP** | Server process; called per tool invocation | Claude (tool call) | Linear cost per call | Connecting to an external system where you need live data or write access (GitHub, Jira, Salesforce, a database) |

## The deciding question

> Does this workflow need to run **automatically on a tool event**, with **zero human effort**, keeping the runtime work **off Claude's turn** (only the result flows back into context)?

If yes: **hook**. The script executes outside the context window; when it has something Claude should act on (like a test failure), that output is fed back into the context window.

If it needs to run on every turn, for every teammate, without being asked: **CLAUDE.md**.

If it is an invocable procedure with a name and a trigger phrase: **skill**.

If it needs its own isolated context to do heavy work: **subagent**.

If it talks to an external system: **MCP**.

## Scale test

Ask: "If this repo had 10,000 files and 50 teammates, which abstraction would still work without blowing up the context window or requiring everyone to remember a slash command?"

- CLAUDE.md: survives at scale only if kept lean (every rule costs tokens every turn).
- Skill: scales well — body is lazy-loaded, only costs tokens when invoked.
- Hook: scales well — the script runs off Claude's turn on every edit; only its output (e.g. a failure message) costs tokens, and only when it has something to report.
- Subagent: scales for isolated tasks; overhead is per-invocation.
- MCP: scales for external integrations; cost is per tool call, not per turn.

## Examples

| Workflow | Abstraction | Deciding factor |
|---|---|---|
| "Always use snake_case in Python" | CLAUDE.md | Must apply every turn, every teammate, no invocation |
| "Generate pytest tests for this endpoint" | Skill | Invocable on demand, clear trigger phrase |
| "Run backend tests after every file edit" | Hook (PostToolUse) | Must run automatically, no human effort, outside context window |
| "Analyze all 200 endpoints for security issues" | Subagent | Long-running, benefits from isolated context |
| "Create a Jira ticket from this finding" | MCP | Writes to an external system |
