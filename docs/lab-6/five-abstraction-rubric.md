# Five-Abstraction Rubric

Use this matrix to decide which customization layer fits a recurring workflow.

| Abstraction | When it loads | Who triggers it | Context cost | Best fit |
|---|---|---|---|---|
| **CLAUDE.md** | Every session, automatically | No one — always resident | Counts against context window every turn | Always-on guidance every teammate needs on every request (formatting rules, project conventions, coding standards) |
| **Skill** | Description loads at session start; body loads after skill fires | Claude (implicit, via description match) or you (explicit `/name`) | Body costs tokens only when invoked | An occasional, invocable procedure with a clear trigger phrase (generate tests, write a PR description, review a diff) |
| **Hook** | Session start; fires on a tool event | The tool event (PostToolUse, PreToolUse) — not a person | Runs outside the context window | Logic that must run automatically after an action, with no human effort, and should not consume context tokens |
| **Subagent** | On demand, spun up by Claude | Claude (orchestrator decides) | Own context window; returns a summary | Long-running or parallel work that benefits from isolation (crawl a repo, run a multi-step analysis, explore options in parallel) |
| **MCP** | Server process; called per tool invocation | Claude (tool call) | Linear cost per call | Connecting to an external system where you need live data or write access (GitHub, Jira, Salesforce, a database) |

## The deciding question

> Does this workflow need to run **automatically after an action**, with **zero human effort**, and stay **outside the context window**?

If yes: **hook**.

If it needs to run on every turn, for every teammate, without being asked: **CLAUDE.md**.

If it is an invocable procedure with a name and a trigger phrase: **skill**.

If it needs its own isolated context to do heavy work: **subagent**.

If it talks to an external system: **MCP**.

## Scale test

Ask: "If this repo had 10,000 files and 50 teammates, which abstraction would still work without blowing up the context window or requiring everyone to remember a slash command?"

- CLAUDE.md: survives at scale only if kept lean (every rule costs tokens every turn).
- Skill: scales well — body is lazy-loaded, only costs tokens when invoked.
- Hook: scales perfectly — runs outside the context window on every edit with no token cost.
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
