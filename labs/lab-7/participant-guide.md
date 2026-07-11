# Lab 7: Sub-Agents, MCP, and Scoped Agentic Automation

**Track 3 — AI Teammate | Theme 7**

Your completion and mastery quizzes are in the LMS.

---

## What you'll build

By the end of this lab you'll have:

- A `structured-handoff.md` (Findings / Decisions / Constraints) derived from a read-only sub-agent review
- A `permission-scope.md` encoding the 3-part MCP permission model (Explicit Read / Explicit Write / Explicit Blocks) for a real GitHub + Jira round-trip
- A worktree (`../inv-lab7`) proving agentic isolation holds

These three files are your share-back, plus the Jira issue key the live round-trip produces.

**The point:** a sub-agent or an MCP connection is a privilege grant, not a convenience. You right-size the delegation, scope the permissions to exactly the calls the workflow makes, and run automation inside a worktree it can't escape.

---

## Core path

Steps 0-7 are required for done-criteria. Work at your own pace.

---

### Step 0 — Pre-flight check

Prerequisites for this lab (fork, clone, branch push, PR open, CI trigger, and MCP credential provisioning) were completed before you started. See `25-lab-prerequisites.md` if you need to revisit any of them.

Do the following checks before you begin:

1. Relaunch Claude Code so the project `.mcp.json` (GitHub + Jira servers) and `CLAUDE.md` load fresh.

2. Run `/mcp` and confirm **github** and **jira** both show as connected. If either shows disconnected, your credential environment variables are not set. Stop and fix them using `25-lab-prerequisites.md` before continuing.

3. Confirm the PR's CI check is red. Run this command:

   ```
   gh pr checks --repo ryan-roark-caylent/inventory-management-smarsh
   ```

   `backend-tests` must show `fail`. If it still shows `pending`, wait one minute and run the command again. If `backend-tests` never appears, Actions may not be enabled on the fork. See `25-lab-prerequisites.md` for the Actions-enable step.

4. Confirm you are on the right branch:

   ```
   git branch --show-current
   ```

   Must print `lab-7-work`.

**Success signal:** `git branch --show-current` prints `lab-7-work`; the `gh pr checks` output shows `backend-tests` as `fail`; `/mcp` lists github and jira as connected.

> **Windows:** after any `.mcp.json` or settings change, relaunch Claude Code before testing MCP or permissions. MCP is configured at project scope (root `.mcp.json`), not user-global. If MCP authentication opens a browser, add `--browser msedge` to that step.
>
> **macOS:** same relaunch rule applies after `.mcp.json` or settings changes. MCP is configured at project scope (root `.mcp.json`), not user-global. If MCP authentication opens a browser, your default browser opens automatically with no extra flag.

---

### Step 1 — Read the trigger

Ask Claude (single agent, read-only) to run the backend test suite and explain which test fails and why. Point it at the backend tests:

```
uv run --project server pytest tests/backend/ -v
```

Ask Claude to name the failing test and identify the specific line of code responsible. Do not ask it to fix anything yet.

**Expected output shape:**

```
tests/backend/test_dashboard_filter.py::test_inventory_count_respects_filter FAILED
tests/backend/test_dashboard.py::TestDashboardEndpoints::test_get_dashboard_summary PASSED
...
=================== 1 failed, 40 passed in 0.58s ===================
E   assert 32 < 32   # total_inventory_items returned the global count (32), not the filtered count (12)
```

**Success signal:** Claude names the failing test and points at the specific line in `server/main.py` the test targets.

---

### Step 2 — Delegation topology (open-ended judgment)

You have four tasks for this repo:

- (a) Scan all API routes for missing auth and authorization gaps
- (b) Rename one local variable in `main.py`
- (c) Generate pytest tests for 5 independent endpoints
- (d) Apply a one-line CORS config change

Sort each into **delegate to a sub-agent** vs **keep in a single agent**. Write one line defending each decision. Then name the delegation topology for any task you delegate: which sub-agent does what, in what order.

You must decide and defend: which tasks earn a sub-agent's coordination overhead, and which don't?

**Success signal:** a 4-row sort with a one-line reason per task, plus a named topology for any delegated work.

---

### Step 3 — Dispatch the read-only reviewer

Ask Claude to dispatch the `code-reviewer` sub-agent on the failing dashboard-summary code in `server/main.py`. Ask it to return the reviewer's findings and confirm whether any files were changed.

Note: the `code-reviewer` agent runs in its own context window. It has read-only tools (Read, Grep, Glob) and cannot write files even if asked.

**Expected output shape:**

```
# Code Review: dashboard summary
**Files Reviewed**: server/main.py
## Critical Issues
1. total_inventory_items ignores filters - server/main.py (get_dashboard_summary)
   - Problem: len(inventory_items) counts the global list; filtered_inventory is already
     computed above but unused here
   - Fix: len(filtered_inventory)
2. total_backlog_items ignores filters - server/main.py line 200 (get_dashboard_summary)
   - Problem: len(backlog_items) counts the global backlog list with no warehouse/category filter
   - Note: backlog items carry no warehouse or category fields, so a filter here is
     non-trivial; separate issue, out of scope for the failing test
## Suggestions
- CORS allow_origins=["*"] (main.py) is broad for anything beyond a demo
(No files were modified — reviewer has Read/Grep/Glob only.)
```

**Success signal:** the sub-agent returns findings and `git status` is clean (no files changed).

---

### Step 4 — Author the structured handoff

Instead of passing the reviewer's raw transcript to an implementer, write a one-page `structured-handoff.md` with three sections:

- **Findings:** what the reviewer found (primary finding + any secondary findings noted as separate known issues)
- **Decisions:** what you will fix and why, scoped to exactly the test-targeted field; explicitly defer anything out of scope
- **Constraints:** what the fix must not do (no new dependencies, no touching other endpoints, keep it in-memory)

The handoff should be shorter than the raw transcript and contain no chat noise.

Ask Claude to help you think through what belongs in each section, but make the scoping decisions yourself. What is the minimal fix that makes the failing test pass?

**Success signal:** `structured-handoff.md` exists with all three sections filled; Decisions is scoped to the test-targeted field and explicitly defers anything out of scope.

---

### Step 5 — Write `permission-scope.md` (the 3-part model) ★ Point step

For the workflow "read the failing CI check on the PR, then open a Jira issue with the diagnosis," write the three permission scopes yourself and defend each:

- **Explicit Read:** what can the agent read, on which resource, and on which specific repo?
- **Explicit Write:** what can the agent create or modify, on which resource, on which specific project?
- **Explicit Blocks:** what is explicitly forbidden, even if the MCP server would allow it?

Strip anything broader than what the workflow actually needs. Each section should be a checklist of named, specific calls.

Then encode the two permitted calls (one read, one write) as an allow/deny list in `.claude/settings.local.json`. Block everything else.

The shape your `permission-scope.md` should take:

```markdown
## Explicit Read
- github: <the specific read call>  (repo: inventory-management-smarsh ONLY)

## Explicit Write
- jira: <the specific write call>  (project: <your project> ONLY)

## Explicit Blocks
- github: <calls you are blocking>
- jira: <calls you are blocking>
```

Ask Claude to think through what minimal set of calls the workflow requires, but you fill in and defend the three sections yourself.

**Success signal:** `permission-scope.md` has all three sections as checkable lines; your allow list names only the single read call and the single write call; your block list names merge, delete, and any call outside your workflow.

---

### Step 6 — Run the scoped round-trip

With auto mode **off**, ask Claude to run the full workflow under your scope: read the failing CI check on your open PR via the GitHub MCP, then create exactly one Jira issue titled after the failing test with the diagnosis from your `structured-handoff.md` in the body.

Tell Claude not to merge anything, not to touch any other repo or project, and to ask you before each MCP call.

Approve each call as it fires. Observe that only the two calls your scope names are ever requested.

**Expected output shape:**

```
github ▸ get_pull_request(#7)  → checks: "backend-tests" = FAILING
jira   ▸ create_issue(project=AEP, summary="test_inventory_count_respects_filter failing on PR #7")
       → { "key": "AEP-1234", "self": "https://.../browse/AEP-1234" }
```

(Your issue key and PR number will differ.)

**Success signal:** the GitHub MCP returns the red check name; the Jira MCP returns a new issue key; no other MCP call was attempted. Open the issue in Jira and confirm the diagnosis appears in the body.

> **Note:** if your Jira project key isn't `AEP`, the create call uses whatever project you were provisioned. The scope discipline (one project only) is what matters, not the specific key.

---

### Step 7 — Worktree isolation

From the repo root, run each command on its own line (no chaining):

```
git worktree add ../inv-lab7 -b inv-lab7
```

Then create a file in the new worktree:

```
touch ../inv-lab7/isolation-test.txt
```

Verify the file appears in the worktree:

```
git -C ../inv-lab7 status --short
```

Then verify the main checkout is unaffected:

```
git status --short
```

The file must not appear in the main checkout.

**Expected output shape:**

```
$ git -C ../inv-lab7 status --short
?? isolation-test.txt
$ git status --short
                            # (empty — the file does not leak in)
```

Write one sentence explaining why the isolation holds. Then note a qualitative token-cost estimate for the full workflow you ran (relative cost compared to a single-agent task, and what the biggest cost driver is). No absolute token count needed.

**Success signal:** `git status --short` in the main checkout is empty; `isolation-test.txt` exists only in `../inv-lab7`.

---

### Step 8 — Exit ticket and commit

Commit `permission-scope.md` and `structured-handoff.md` to `lab-7-work`. Record your delegation topology decision (from Step 2) in the commit message or in a brief note in one of the files. Push to your fork.

```
git add permission-scope.md structured-handoff.md
git commit -m "lab-7: structured handoff and permission scope"
git push origin lab-7-work
```

Your share-back is the two committed files plus the Jira issue key from Step 6 and the worktree branch name `inv-lab7`, with your one-line qualitative token-cost note.

**Success signal:** `git log --oneline -1` shows your commit; both artifacts are on `lab-7-work`.

---

## Done criteria

You have completed the core path when all four are true:

1. `structured-handoff.md` exists on `lab-7-work` with Findings, Decisions, and Constraints filled.
2. `permission-scope.md` exists with all three parts (Explicit Read, Explicit Write, Explicit Blocks) as checkable lines, and the allow list names only the single read call and the single write call.
3. The scoped round-trip ran: the GitHub MCP read the red CI check and the Jira MCP returned a new issue key, and no broader MCP call was attempted.
4. A worktree exists at `../inv-lab7` and `git status` in the main checkout is clean.

---

## Extra credit

These are not required for done-criteria or the completion quiz. Work on them if you finish early or want to go deeper.

1. **Scoped `/loop` (Part 4).** Enable auto mode via `/permissions` (not Shift+Tab, which cycles to plan mode). On your open PR, run `/loop 10m` and ask it to check whether CI passed, summarize any review comments, and tell you what is blocking merge. Set an iteration cap. Confirm it never attempts a merge (your Explicit Blocks holds). Map the task to the trust spectrum first: is it read-mostly? Is the worst-case action recoverable?

2. **Raw transcript vs structured handoff comparison.** Pass the reviewer's full raw transcript to a fresh implementer session, then pass your `structured-handoff.md` to another. Compare which produces the cleaner, more targeted fix.

3. **Idempotency.** Run the "open a Jira issue" workflow twice. Observe a duplicate issue. Add a check-before-create step (keyed on the failing test name) so the second run is a no-op.

4. **Fix the bug in the worktree.** In `../inv-lab7`, apply the fix you identified in your structured handoff, run pytest green, and confirm the main checkout is untouched until you merge.

5. **Second sub-agent, real topology.** Dispatch `security-auditor` (haiku, read-only) on the same diff and compare its findings to `code-reviewer`'s. Did the two-reviewer fan-out earn its cost?

---

## Stuck path

**MCP won't connect (stuck at Step 0).** Run `/mcp` to see current status. If github or jira show disconnected, confirm your credential environment variables are set (see `25-lab-prerequisites.md`), then relaunch Claude Code. If you still can't connect, you can still complete the scoping half of the lab. Ask Claude to read `.mcp.json` and help you think through which specific GitHub and Jira calls a workflow that reads a failing CI check and opens one Jira issue would need, and which calls it should be explicitly blocked from, without calling any tool. You'll produce a valid `permission-scope.md` and still hit done-criteria 1 and 2.

**Sub-agent dispatch confuses you (Step 3).** Ask Claude to dispatch the `code-reviewer` sub-agent to review the dashboard summary function in `server/main.py`, report its findings, and confirm it made no file changes. If Claude seems confused about sub-agents, confirm `.claude/agents/code-reviewer.md` exists in the repo.

**Stuck on the structured handoff structure (Step 4).** Ask Claude to look at the reviewer's output and help you identify the primary finding (the one the failing test targets), any secondary findings worth noting, and what the minimal fix would need to avoid touching. You fill in the three sections; Claude can help you think through the boundaries.

**Stuck on permission scoping (Step 5).** Ask Claude to list the minimal set of GitHub and Jira tool calls a workflow that reads a failing CI check and creates one Jira issue would need, without calling any tool. Use that list to fill in your three sections yourself.

**Fully stuck or out of time.** Check out the reference artifacts from the solution branch to see finished examples:

```
git fetch origin
git checkout origin/lab-7-solution -- permission-scope.md structured-handoff.md
```

Open both files. You'll see what a complete least-privilege scope and a signal-preserving handoff look like. You still leave having seen the 3-part model applied.

**Reset everything.** Run the `/reset-branch` skill, then redo Step 0. Remove any stray worktree with:

```
git worktree remove ../inv-lab7 --force
```

Delete `.claude/settings.local.json` before your next lab so the allow/deny list doesn't carry over.

---

## Sources

- [20-lab-7-design.md](../../lab-build/20-lab-7-design.md) — authoritative design (Sections 2, 3, 4, 5, 7, 9)

**Date generated:** 2026-07-11
