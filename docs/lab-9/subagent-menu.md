# Subagent menu (Step 3)

Pick ONE to author as `.claude/agents/<name>.md`. Each option is
scoped to a real directory or role in this repo, and distinct from the three
subagents already on `main` (code-reviewer, security-auditor, vue-expert).

## Required frontmatter fields (all four)
```yaml
---
name: <kebab-case>
description: <one-line, when to invoke this agent>
tools: <comma-separated list>
model: sonnet
---
```

## Option 1 — test-writer
File: `.claude/agents/test-writer.md`
Tools: Read, Write, Edit, Bash, Glob, Grep
One job: Generate pytest tests for the endpoint or function I name.
Scope: `tests/backend/` only. Follow `tests/backend/conftest.py`.
Out of scope: anything outside `tests/backend/` — say so and stop.

## Option 2 — api-contract-reviewer
File: `.claude/agents/api-contract-reviewer.md`
Tools: Read, Grep
One job: Review the named endpoint in `server/main.py` for contract stability —
response shape, HTTP status codes, parameter validation. Report findings; do not edit.
Out of scope: any write or edit operation — this agent is read-only.

## Option 3 — vue-auditor
File: `.claude/agents/vue-auditor.md`
Tools: Read, Glob, Grep
One job: Audit the named Vue component in `client/src/` for Composition API
patterns, key usage in v-for, and date validation. Report findings; do not edit.
Out of scope: `server/`, `.claude/`, or any write/edit operation.

## Option 4 — propose your own
File: `.claude/agents/<your-name>.md`
Requirements: scoped to one directory or one task; tool allowlist narrower than
the full default; system prompt names the target path and states what is out of scope.
