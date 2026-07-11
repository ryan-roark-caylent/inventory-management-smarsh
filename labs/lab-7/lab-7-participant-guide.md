# Lab 7 — Sub-Agents, MCP, and Scoped Agentic Automation

## Before you start

Prerequisites from `25-lab-prerequisites.md` must be complete:
- You have forked `ryan-roark-caylent/inventory-management-smarsh` into your own GitHub account.
- You have cloned your personal fork, added the shared fork as `upstream`, and checked out `lab-7-start` as `lab-7-work`.
- You have pushed `lab-7-work` to your personal fork and opened a cross-fork PR back to the shared fork.
- You have provisioned and connected GitHub and Jira MCP credentials (GitHub PAT scope: repo read + issues; Jira token scoped to one project).

---

## Step 0 — Pre-flight check

- Relaunch Claude Code so the project `.mcp.json` (GitHub + Jira) and `CLAUDE.md` load.
- Run `/mcp` and confirm **github** and **jira** show connected. If either shows disconnected, the credential env vars are not set — stop and fix in `25-lab-prerequisites.md` before continuing.
- Confirm the PR's CI check is red:
  ```
  gh pr checks --repo ryan-roark-caylent/inventory-management-smarsh
  ```
  `backend-tests` must show `fail`. If it still shows pending, wait a minute and re-poll.
- **Success signal:** `git branch --show-current` prints `lab-7-work`; `gh pr checks` shows `backend-tests` as `fail`; `/mcp` lists github + jira as connected.

> **Windows:** relaunch Claude Code after any `.mcp.json` or settings change. If MCP auth opens a browser, use `--browser msedge`.
> **macOS:** same relaunch rule. No `--browser` flag needed — your default browser opens automatically.

---

## Core path (Steps 1–8, all required for done-criteria)

### Step 1 — Read the trigger

Ask Claude (single agent, read-only) to run the backend tests and explain which test fails and why. It should find `tests/backend/test_dashboard_filter.py` failing.

- Test command: `uv run --project server pytest tests/backend/ -v`
- **Success signal:** Claude names the failing test and points at the responsible line in `server/main.py`.

### Step 2 — Delegation topology (open-ended judgment)

You have a task list for this repo:

- (a) scan all API routes for missing auth/authorization gaps
- (b) rename one local variable in `main.py`
- (c) generate pytest tests for 5 independent endpoints
- (d) apply a one-line CORS config change

Sort each into **delegate-to-sub-agent** vs **keep-in-single-agent** and write a one-line defense for each. Then choose the delegation topology for the genuine multi-agent case.

- **Success signal:** a 4-row sort with a one-line reason each, plus a named topology for the delegated work.

### Step 3 — Dispatch the read-only reviewer

Dispatch the repo's `code-reviewer` sub-agent (tools: Read, Grep, Glob only — no write) on the failing dashboard-summary code. Note that it runs in its own context window and returns a summary; it cannot edit files even if asked.

- **Success signal:** the sub-agent returns findings and `git status` is clean (no files changed).

### Step 4 — Author `structured-handoff.md`

Instead of passing the reviewer's raw transcript to an implementer, write a one-page handoff with three sections:
- **Findings** — what the reviewer found
- **Decisions** — the scoped fix (one field, one line — explicitly defer any other issues as out of scope)
- **Constraints** — in-memory only, no new deps, don't touch other endpoints

- **Success signal:** `structured-handoff.md` exists with the three sections filled; it is shorter than the raw transcript; Decisions names exactly the field to fix and defers any secondary issues.

### Step 5 — Write `permission-scope.md` (open-ended judgment, point step)

For the workflow "read the failing CI check on the PR → open a Jira issue with the diagnosis," write the three scopes and defend each:

- **Explicit Read** — GitHub: read PR + CI check status on this one repo. Nothing else.
- **Explicit Write** — Jira: create one issue on one project. No transitions, no deletes.
- **Explicit Blocks** — no merge, no branch/issue delete, no access to any other repo or project, no admin.

Then encode it as an allow/deny list in `.claude/settings.local.json` (allow only the two calls the workflow makes; deny the blocks).

- **Success signal:** `permission-scope.md` has all three parts as checkable lines; your allow list names only the read call + the single write call.

### Step 6 — Run the scoped round-trip (the aha)

With auto mode OFF, ask Claude to run the workflow under your scope: read the failing CI check via the GitHub MCP, then create ONE Jira issue titled after the failing test with the diagnosis from your handoff in the body. Approve each MCP call as it fires.

- **Success signal:** the GitHub MCP returns the red check name; the Jira MCP returns a new issue key; no other MCP call was attempted. You can open the issue in Jira and see the diagnosis.

### Step 7 — Worktree isolation

From the repo root:
- `git worktree add ../inv-lab7 -b inv-lab7`
- Create a file in `../inv-lab7` (e.g., `touch ../inv-lab7/isolation-test.txt`)
- Back in the main checkout, run `git status` — the file must NOT appear.
- Write one sentence on why the isolation holds. Note a qualitative token-cost estimate for the workflow (relative cost + the biggest cost driver).

- **Success signal:** `git status` in the main checkout is clean; `isolation-test.txt` exists only in `../inv-lab7`.

### Step 8 — Exit ticket + commit

Commit `permission-scope.md`, `structured-handoff.md`, and record your delegation topology decision. Push `lab-7-work`.

- **Success signal:** `git log --oneline -1` shows your commit; both artifacts are on `lab-7-work`.

---

## Extra credit (not required for done-criteria)

1. **Scoped `/loop` auto-mode.** Enable auto mode via `/permissions` (NOT Shift+Tab). On the PR run `/loop 10m check whether CI passed, summarize any review comments, tell me what is blocking merge`. Confirm it never attempts a merge (your Explicit Blocks holds).
2. **Raw-transcript vs structured-handoff A/B.** Pass the reviewer's full raw transcript to a fresh implementer session, then pass your `structured-handoff.md` to another. Compare which produces the cleaner fix.
3. **Idempotency.** Run the "open a Jira issue" workflow twice. Add a check-existing-before-create step so the second run is a no-op.
4. **Fix the bug in the worktree.** In `../inv-lab7`, apply the one-line fix, run pytest green, and confirm the main checkout is untouched.
5. **Second sub-agent.** Also dispatch `security-auditor` on the same diff and compare findings to `code-reviewer`'s.

---

## If you get stuck

**MCP won't connect (stuck at Step 0).** Run `/mcp` to see status. If github/jira show disconnected, confirm the credential env vars are set, then relaunch Claude Code. Fallback: skip the live round-trip and do the scoping on paper:
```
Read .mcp.json. For a workflow that reads a failing CI check and opens one Jira issue, tell me exactly which GitHub and Jira tool calls it needs, and which it must be blocked from. Do not call any tool.
```

**Sub-agent dispatch confuses you (Step 3).** Paste into Claude Code:
```
Dispatch the code-reviewer sub-agent to review server/main.py's dashboard summary function. Report its findings. Confirm it made no file changes.
```

**Fully stuck or out of time.** Check out the solution artifacts to see the finished scope + handoff:
```
git fetch origin
git checkout origin/lab-7-solution -- permission-scope.md structured-handoff.md
```
Open both files and read the reference 3-part scope and handoff.

**Reset everything:** run the `/reset-branch` skill, then redo Step 0. Remove any stray worktree with `git worktree remove ../inv-lab7 --force`. Delete `.claude/settings.local.json` before the next lab.
