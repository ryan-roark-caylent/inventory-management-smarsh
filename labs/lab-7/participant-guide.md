# Lab 7: Sub-Agents, MCP, and Scoped Agentic Automation

**Track 3 — AI Teammate | Theme 7**

Your completion and mastery quizzes are in the LMS.

---

## What you'll build

By the end of this lab you'll have:

- A `structured-handoff.md` (Findings / Decisions / Constraints) that Claude drafts and you scope, derived from a read-only sub-agent review
- A `permission-scope.md` encoding a least-privilege MCP scope for Jira (read allowed, all writes blocked)
- First-hand proof that the scope — not your click — is the safety: a Jira write DENIED under auto mode while the scoped read still works

Both files stay local in your worktree. Nothing gets committed or pushed.

**The point:** an MCP connection is a privilege grant, not a convenience. You scope it to exactly the calls the workflow needs, and the guard — not your click — is what stops the rest. When a write is scoped off, even auto mode can't perform it.

---

## Core path

Steps 0-8 are the core path. Work at your own pace.

---

### Step 0 — Pre-flight check

You should already be on `lab-7-work` (in your per-lab worktree) from the MindTickle pre-work module. If you are not, check it out now:

```
git fetch origin
git worktree add ../lab-7-work lab-7-start
```

(Your pre-work module has the exact worktree setup; this is the fallback.)

Do the following before you begin:

1. **Switch to Sonnet.** Smarsh defaults to Haiku; this lab is tuned for Sonnet. Run `/model sonnet` (or `/model` and pick Sonnet). The point-step behaviors assume Sonnet.

2. **Relaunch Claude Code** so the project `.mcp.json` and `CLAUDE.md` load fresh.

3. **Confirm Jira is connected.** Run `/mcp` and confirm **jira** (Atlassian) shows connected. If it shows disconnected, your credential environment variables aren't set — fix them per the MindTickle pre-work module, then relaunch. (There is no GitHub MCP in this lab — Jira only.)

4. **Note the exact Jira tool names.** In the `/mcp` view, look at the Jira server's tool list and note the exact names for "get an issue," "search issues," and "add a comment." You'll need the exact names in Step 5 — a guessed name silently mis-scopes.

**Success signal:** `git branch --show-current` (or `git worktree list`) shows you on `lab-7-work`; `/model` shows Sonnet; `/mcp` lists jira as connected and you can see its tool names.

> **Windows / macOS (identical):** after any `.mcp.json` or settings change, relaunch Claude Code before testing MCP or permissions. MCP is configured at project scope (root `.mcp.json`), never user-global. If MCP auth opens a browser, on Windows add `--browser msedge` to that step; on macOS your default browser opens with no flag.

> **Docs pointer:** anything this card references as "see the pre-work" lives in your **MindTickle pre-work module**, not in this repo.

---

### Step 1 — Read the trigger (local, read-only)

Ask Claude (single agent, read-only) to run the backend test suite and explain which test fails and why. Do not ask it to fix anything.

```
uv run --project server pytest tests/backend/ -v
```

Ask Claude to name the failing test and identify the specific line of code responsible.

**Expected output shape:**

```
tests/backend/test_dashboard_filter.py::test_inventory_count_respects_filter FAILED
...
=================== 1 failed, 40 passed in 0.5s ===================
E   assert <filtered count> < <global count>   # the counts are equal because the field ignores the filter
```

**Success signal:** Claude names the failing test and points at the specific line in `server/main.py` (`get_dashboard_summary`).

---

### Step 2 — Delegation topology (open-ended judgment)

You have four tasks for this repo:

- (a) Scan all API routes for missing auth and authorization gaps
- (b) Rename one local variable in `main.py`
- (c) Generate pytest tests for 5 independent endpoints
- (d) Apply a one-line CORS config change

Sort each into **delegate to a sub-agent** vs **keep in a single agent**. Write one line defending each decision. Then name the delegation topology for any task you delegate: which sub-agent does what, in what order.

Decide and defend: which tasks earn a sub-agent's coordination overhead?

**Success signal:** a 4-row sort with a one-line reason per task, plus a named topology for any delegated work.

> **Note:** this is judgment, not a code change — there's nothing to run here. Step 3 dispatches the reviewer that this sort tells you is worth delegating.

---

### Step 3 — Dispatch the read-only reviewer

Ask Claude to dispatch the `code-reviewer` sub-agent on the failing dashboard-summary code in `server/main.py`. Ask it to return the reviewer's findings and confirm whether any files were changed.

> **Refresher:** the `code-reviewer` sub-agent runs in its **own context window**. Its investigation — reading files, grepping, reasoning — does not pile into your main session's context. That isolation is the point: you get the findings back without clogging your window with everything it looked at. It also has read-only tools (Read, Grep, Glob) and cannot write files even if asked.

**Expected output shape:**

```
# Code Review: dashboard summary
**Files Reviewed**: server/main.py
## Critical Issues
1. <primary finding — a count that ignores the active filters>
2. <a secondary finding, noted as a separate known issue>
## Suggestions
- <a broad CORS setting flagged as demo-only>
(No files were modified — reviewer has Read/Grep/Glob only.)
```

**Success signal:** the sub-agent returns findings and `git status` is clean (no files changed).

---

### Step 4 — Claude drafts the handoff, then quizzes you

Instead of writing the handoff from scratch (or passing the reviewer's raw transcript downstream), **ask Claude to draft `structured-handoff.md`** with three sections — **Findings / Decisions / Constraints** — and then to **quiz you** on the scoping calls it can't make for you:

- Which finding is the one the failing test targets (the primary), and which are separate known issues to defer?
- What is the minimal fix, and what should it deliberately NOT touch?
- What constraints bound it (in-memory only, no new deps, don't touch other endpoints)?

Answer Claude's questions to lock the Decisions and Constraints yourself. The finished handoff should be shorter than the raw transcript and carry no chat noise. **This stays a local file in your worktree — it does not get sent anywhere.**

**Success signal:** `structured-handoff.md` exists with all three sections filled; Decisions is scoped to the test-targeted field and explicitly defers the out-of-scope finding; it reads as signal, not transcript.

---

### Step 5 — Scope Jira to read-only (`permission-scope.md`) ★ Point step

You're about to let an agent touch Jira. Before you do, decide exactly what it may and may not do, and write it down. For the workflow "read my most-recent Jira ticket; do nothing else to Jira," write the three scopes and defend each:

- **Explicit Read** — Jira: read issues (get one issue / search my issues). Read-only.
- **Explicit Write** — Jira: **BLOCKED.** No comment, no create, no transition, no edit.
- **Explicit Blocks** — everything else: no other MCP server, no Jira admin, no deletes, no project changes.

Then encode it in `.claude/settings.local.json`: **allow** only the Jira read call(s); **deny** the Jira write calls and everything else.

The shape your `permission-scope.md` should take:

```markdown
## Explicit Read
- jira: <the specific read call(s)>   (my issues / one issue — read only)

## Explicit Write
- jira: BLOCKED — no comment, no create, no transition, no edit

## Explicit Blocks
- jira: <write/admin/delete calls you are blocking>
- everything else: no other MCP server, no other project, no admin
```

> **Verify tool names:** open `/mcp`, find the Jira server's tool list, and confirm your allow/deny entries use the **exact** tool names it exposes. A guessed name (`get_issue` vs `jira_get_issue`) silently mis-scopes — the guard won't match and the block won't fire where you think it does.

Ask Claude to help you enumerate the minimal read calls the workflow needs, but you fill in and defend the three sections and the allow/deny list yourself.

**Success signal:** `permission-scope.md` has all three sections as checkable lines; your allow list names only the Jira read call(s); your deny list names the Jira write calls plus everything outside the workflow. The `/mcp` tool names match your entries exactly.

---

### Step 6 — Run it under auto mode and watch the write get DENIED ★ Point step

Now prove the scope is the safety — not your click.

1. **Enable auto mode** (you learned this earlier in the program; via `/permissions`, not Shift+Tab). With auto mode on, Claude does not stop to ask you to approve tool calls.
2. Ask Claude to: **(a) read your most-recent Jira ticket** (fetch the single latest issue assigned to or reported by you — content doesn't matter), then **(b) add a short comment to that same ticket** (any nonsense text).
3. Watch what happens: the **read succeeds** (it's in your Explicit Read). The **comment write is DENIED by your Explicit Block** — even though auto mode would have auto-approved anything you allowed. No human said no. The scope said no.
4. **Then review locally with git.** Run `git status` / `git diff` in your worktree and confirm nothing changed and no local files were written by the blocked call. This is the review-after-autonomy habit: let it run, then check.

**Expected output shape:**

```
jira ▸ get_issue(<your-latest-key>)         → returns the ticket (summary, status)   ✓ allowed
jira ▸ add_comment(<your-latest-key>, ...)  → DENIED by permission rule (deny: jira add_comment)
                                              (no approval prompt — auto mode was on)
Result: read completed; comment was NOT created. Scope held with no human in the loop.
```

**Success signal:** Claude reports the content (or key) of your most-recent ticket from the read; the comment attempt returns a permission-denied / blocked result, not a created comment; auto mode never prompted you to approve; `git`-review shows a clean local tree.

> **Note:** the whole point is that this is lab-agnostic — it works against whatever real Jira project you were provisioned. The ticket content is irrelevant; the connection working (read) and the block firing (write) are the lesson.

---

### Step 7 — Worktree isolation (you've been in one all along)

You didn't just run an autonomous agent — you ran it inside a **git worktree** (`lab-7-work`) the whole lab. Confirm it:

```
git worktree list
```

You'll see `lab-7-work` as its own working directory, separate from any other checkout. That's why the auto-mode run in Step 6 could never have escaped into another branch's files or your main checkout.

Write one sentence on why running an autonomous, MCP-connected agent inside a worktree matters (blast radius: the worst case is contained to this working tree). Then note a **qualitative** token-cost estimate for the workflow you ran — relative cost vs a single-agent task, and the biggest cost driver. No absolute number.

**Expected output shape:**

```
$ git worktree list
/path/to/inventory-management-smarsh   <sha> [main]
/path/to/lab-7-work                    <sha> [lab-7-work]
```

**Success signal:** `git worktree list` shows `lab-7-work` as an isolated worktree; you can state in one sentence why isolation bounded the autonomous run.

---

### Step 8 — Keep your takeaway (no commit)

Your two local artifacts — `permission-scope.md` and `structured-handoff.md` — stay in your worktree as a personal takeaway. **Do not commit or push anything.**

Think through (no need to write it down): if you scoped this Jira workflow for your own team, what's the one call you'd allow and the one you'd hardest-block?

**Success signal:** both files exist in your worktree; you can point to the Explicit Block line that denied the write in Step 6.

---

## Done criteria

You have completed the core path when all four are true:

1. `structured-handoff.md` exists in your worktree with Findings, Decisions, and Constraints filled; Decisions scoped to the test-targeted field.
2. `permission-scope.md` exists with all three parts (Explicit Read, Explicit Write blocked, Explicit Blocks) as checkable lines; the allow list names only the Jira read call(s).
3. Under auto mode, the scoped Jira read succeeded and the comment write was DENIED by your deny rule with no approval prompt.
4. `git worktree list` shows you ran the whole lab inside `lab-7-work`; a `git`-review shows a clean local tree.

---

## Extra credit

These are not required for done-criteria or the completion quiz. Work on them if you finish early or want to go deeper.

1. **Raw transcript vs structured handoff comparison.** Pass the reviewer's full raw transcript to a fresh implementer session, then pass your `structured-handoff.md` to another. Compare which produces the cleaner, more targeted fix.

2. **Fix the bug locally.** In your worktree, apply the fix you scoped in your structured handoff, run pytest green, and confirm nothing else changed. (Do not commit.)

3. **Second sub-agent, real topology.** Dispatch `security-auditor` (haiku, read-only) on the same code and compare its findings to `code-reviewer`'s. Did the two-reviewer fan-out earn its cost?

4. **Tighten the scope further.** Add a second Jira write to your deny list (a transition or an update) and re-run Step 6's write attempt against it. Confirm each named write is blocked independently.

---

## Stuck path

**Jira won't connect (Step 0 / 6).** Run `/mcp` to see current status. If jira shows disconnected, confirm your read-only Jira token environment variable is set (see the MindTickle pre-work module), then relaunch Claude Code. If you still can't connect, you can still complete the scoping half of the lab: ask Claude to read `.mcp.json` and help you think through which specific Jira calls a workflow that only reads your most-recent ticket would need, and which it must be blocked from, without calling any tool. You'll produce a valid `permission-scope.md` and still hit the scoping done-criteria.

**Sub-agent dispatch confuses you (Step 3).** Ask Claude to dispatch the `code-reviewer` sub-agent to review the dashboard summary function in `server/main.py`, report its findings, and confirm it made no file changes. If Claude seems confused about sub-agents, confirm `.claude/agents/code-reviewer.md` exists in the repo.

**Stuck on the handoff (Step 4).** Ask Claude to draft the three sections and quiz you on the scoping calls — the primary finding (the one the failing test targets), any secondary findings worth deferring, and what the minimal fix must avoid touching. You make the scoping calls; Claude drafts from your answers.

**Stuck on permission scoping (Step 5).** Ask Claude to list the minimal set of Jira tool calls a workflow that only reads your most-recent ticket would need, and every Jira write/admin call that should be explicitly blocked, without calling any tool. Use that list to fill in your three sections yourself.

**Fully stuck or out of time.** Check out the reference artifacts from the solution branch to see finished examples. First confirm your remote points at the fork:

```
git remote -v
git fetch origin
git checkout origin/lab-7-solution -- permission-scope.md structured-handoff.md
```

Open both files. You'll see what a complete least-privilege scope and a signal-preserving handoff look like. You still leave having seen the 3-part model applied.

**Reset everything.** Run the `/reset-branch` command (not a skill). It does `branch -D` + `reset --hard` + `clean -fd` with no confirmation, so save anything you want to keep first. With worktree-per-lab you mostly just move to the next lab's worktree. Delete `.claude/settings.local.json` before your next lab so the allow/deny list doesn't carry over.

---

## Sources

- [31-lab-7-remediation-design.md](../../lab-build/31-lab-7-remediation-design.md) — authoritative design (Sections 1-8)
