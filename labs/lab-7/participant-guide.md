# Lab 7: Sub-Agents, MCP, and Scoped Agentic Automation

**Track 3 — AI Teammate | Theme 7**

Your completion and mastery quizzes are in the LMS.

---

## What you'll build

By the end of this lab you'll have:

- A `structured-handoff.md` (Findings / Decisions / Constraints) that Claude drafts and you scope, derived from a read-only sub-agent review
- A `.claude/settings.local.json` encoding a least-privilege MCP scope for Atlassian (Jira read allowed, all writes and everything else blocked)
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

3. **Confirm Atlassian is connected.** Run `/mcp` and confirm **claude_ai_Atlassian** shows connected (this one server covers Jira, Confluence, and cross-product tools together). If it shows disconnected, your credentials aren't set — fix them per the MindTickle pre-work module, then relaunch. (There is no GitHub MCP in this lab — Atlassian only.)

4. **Note the exact Atlassian tool names.** In the `/mcp` view, select the **claude_ai_Atlassian** server and read its tool list. Note the exact names for "get an issue," "search issues," and "add a comment" — they're camelCase with a prefix (e.g. `mcp__claude_ai_Atlassian__getJiraIssue`). You'll need the exact names in Step 6; a guessed name silently mis-scopes.

**Success signal:** `git branch --show-current` (or `git worktree list`) shows you on `lab-7-work`; `/model` shows Sonnet; `/mcp` lists **claude_ai_Atlassian** as connected and you can see its tool names.

> **Windows / macOS (identical):** after any `.mcp.json` or settings change, relaunch Claude Code before testing MCP or permissions. MCP is configured at project scope (root `.mcp.json`), never user-global. If MCP auth opens a browser, on Windows add `--browser msedge` to that step; on macOS your default browser opens with no flag.

> **Docs pointer:** anything this card references as "see the pre-work" lives in your **MindTickle pre-work module**, not in this repo.

---

### Step 1 — Delegation topology (open-ended judgment)

Before you touch anything, frame the work. You have four tasks for this repo:

- (a) Scan all API routes for missing auth and authorization gaps
- (b) Rename one local variable in `main.py`
- (c) Generate pytest tests for 5 independent endpoints
- (d) Apply a one-line CORS config change

Sort each into **delegate to a sub-agent** vs **keep in a single agent**, and think through which tasks earn a sub-agent's coordination overhead and why. Then decide the delegation topology for anything you'd delegate: which sub-agent does what, in what order.

You don't need to write this down — reason it through and move on. The sort is the mental model the rest of the lab runs on: in Step 3 you'll dispatch the reviewer this thinking tells you is worth delegating.

**Success signal:** you can say which of the four tasks earn a sub-agent and why, and name the topology for any you'd delegate.

---

### Step 2 — Read the trigger (local, read-only)

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

Answer Claude's questions to lock the Decisions and Constraints yourself. The finished handoff should be shorter than the raw transcript and carry no chat noise. It's a local file in your worktree — you'll hand it to an implementer next.

**Success signal:** `structured-handoff.md` exists with all three sections filled; Decisions is scoped to the test-targeted field and explicitly defers the out-of-scope finding; it reads as signal, not transcript.

---

### Step 5 — Execute the handoff (the payoff)

A handoff only earns its keep if someone acts on it. Now play the implementer: **hand `structured-handoff.md` to Claude and ask it to apply the scoped fix** — nothing more than the Decisions section allows.

```
uv run --project server pytest tests/backend/ -v
```

1. Ask Claude to read `structured-handoff.md` and implement **only** the fix its Decisions section scopes (the `total_inventory_items` count), honoring the Constraints (in-memory only, no new deps, don't touch the deferred `total_backlog_items` finding or any other endpoint).
2. Re-run the backend tests. The previously failing test now passes.
3. **Review the diff** (`git diff`): confirm Claude changed only the one scoped line and left the deferred finding alone. This is the signal-preserving handoff proving itself — the implementer did exactly what the handoff said, no scope creep, because the handoff carried decisions not chatter.

**Expected output shape:**

```
tests/backend/test_dashboard_filter.py::test_inventory_count_respects_filter PASSED
...
=================== 41 passed in 0.5s ===================
git diff → one line changed in server/main.py; total_backlog_items untouched (deferred, as scoped)
```

**Success signal:** the failing test now passes, the diff touches only the scoped line, and the deferred finding is still present (not "helpfully" fixed) — the handoff bounded the implementer exactly as written.

---

### Step 6 — Scope the connection in `settings.local.json` ★ Point step

You're about to let an agent touch Atlassian. Before you do, decide exactly what it may and may not do — then encode that decision where it's actually enforced.

Notice what you're scoping: the connected server is **one combined `claude_ai_Atlassian` server** — it exposes Jira *and* Confluence *and* cross-product tools (~32 calls, including Confluence page writes and account lookups). Your workflow needs exactly one thing: read your most-recent Jira ticket. Least privilege means allowing those one or two read calls and blocking all the rest.

**Reason through the three-part model** (out loud or in your head — you don't need to write it as prose; the enforcement file below is the artifact that matters):

- **Explicit Read** — the Jira read call(s) only: search my issues, then get the one issue.
- **Explicit Write** — **BLOCKED.** No comment, no create, no transition, no edit, no worklog.
- **Explicit Blocks** — everything else the server exposes: all Confluence tools, the cross-product `search`/`fetch`, account/admin calls, and every other project.

Now encode that reasoning directly in `.claude/settings.local.json` — this is the **deterministic guard** the runtime actually reads: **allow** only the Jira read calls, **deny** the writes and everything else. The shape (fill the exact tool names you confirm from `/mcp`):

```jsonc
{
  "permissions": {
    "allow": [
      "mcp__claude_ai_Atlassian__searchJiraIssuesUsingJql",  // find my latest issue
      "mcp__claude_ai_Atlassian__getJiraIssue"               // read that issue
    ],
    "deny": [
      "mcp__claude_ai_Atlassian__addCommentToJiraIssue",     // the write we'll watch get blocked
      "mcp__claude_ai_Atlassian__createJiraIssue",
      "mcp__claude_ai_Atlassian__editJiraIssue",
      "mcp__claude_ai_Atlassian__transitionJiraIssue"
      // ...plus the Confluence + cross-product tools outside this workflow
    ]
  }
}
```

> **Verify tool names:** open `/mcp`, select the **claude_ai_Atlassian** server, and read its tool list. Confirm every allow/deny entry uses the **exact** tool name it exposes — camelCase with the `mcp__claude_ai_Atlassian__` prefix, not the friendly label. A guessed name silently mis-scopes: the guard won't match, and the block won't fire where you think it does.

> **To be clear — blocking writes is a choice for this exercise, not a rule.** Letting Claude comment on, transition, or create Jira issues is a perfectly good real-world setup; plenty of useful workflows need exactly that. We block writes here so you can *watch the guard fire* and prove the scope is what stops the call. The lesson isn't "MCP writes are dangerous" — it's "scope to what the workflow needs." When your workflow genuinely needs a write, allow it.

Ask Claude to help you enumerate the minimal read calls the workflow needs, but you decide and defend the allow/deny split yourself.

**Success signal:** `.claude/settings.local.json` allows only the two Jira read calls and denies the writes plus the Confluence/cross-product tools outside the workflow; every entry matches an exact `/mcp` tool name.

---

### Step 7 — Run it under auto mode and watch the write get DENIED ★ Point step

Now prove the scope is the safety — not your click.

1. **Enable auto mode** (you learned this earlier in the program; via `/permissions`, not Shift+Tab). With auto mode on, Claude does not stop to ask you to approve tool calls.
2. Ask Claude to: **(a) read your most-recent Jira ticket** (search for the single latest issue assigned to or reported by you, then read it — content doesn't matter), then **(b) add a short comment to that same ticket** (any nonsense text).
3. Watch what happens: the **read succeeds** (it's in your Explicit Read). The **comment write is DENIED by your Explicit Block** — even though auto mode would have auto-approved anything you allowed. No human said no. The scope said no.
4. **Then review locally with git.** Run `git status` / `git diff` in your worktree and confirm nothing changed and no local files were written by the blocked call. This is the review-after-autonomy habit: let it run, then check.

**Expected output shape:**

```
claude_ai_Atlassian ▸ searchJiraIssuesUsingJql(...)      → finds your latest issue key   ✓ allowed
claude_ai_Atlassian ▸ getJiraIssue(<your-latest-key>)    → returns the ticket             ✓ allowed
claude_ai_Atlassian ▸ addCommentToJiraIssue(<key>, ...)  → DENIED by permission rule
                                                           (no approval prompt — auto mode was on)
Result: read completed; comment was NOT created. Scope held with no human in the loop.
```

**Success signal:** Claude reports the content (or key) of your most-recent ticket from the read; the comment attempt returns a permission-denied / blocked result, not a created comment; auto mode never prompted you to approve; `git`-review shows a clean local tree.

> **Note:** the whole point is that this is lab-agnostic — it works against whatever real Jira project you were provisioned. The ticket content is irrelevant; the connection working (read) and the block firing (write) are the lesson.

---

### Step 8 — Worktree isolation (you've been in one all along)

You didn't just run an autonomous agent — you ran it inside a **git worktree** (`lab-7-work`) the whole lab. Confirm it:

```
git worktree list
```

You'll see `lab-7-work` as its own working directory, separate from any other checkout. That's why the auto-mode run in Step 7 could never have escaped into another branch's files or your main checkout.

Write one sentence on why running an autonomous, MCP-connected agent inside a worktree matters (blast radius: the worst case is contained to this working tree). Then note a **qualitative** token-cost estimate for the workflow you ran — relative cost vs a single-agent task, and the biggest cost driver. No absolute number.

**Expected output shape:**

```
$ git worktree list
/path/to/inventory-management-smarsh   <sha> [main]
/path/to/lab-7-work                    <sha> [lab-7-work]
```

**Success signal:** `git worktree list` shows `lab-7-work` as an isolated worktree; you can state in one sentence why isolation bounded the autonomous run.

---

### Step 9 — Keep your takeaway (no commit)

Your two local artifacts — `.claude/settings.local.json` (your enforced scope) and `structured-handoff.md` — stay in your worktree as a personal takeaway. **Do not commit or push anything.**

Think through (no need to write it down): if you scoped this Jira workflow for your own team, what's the one call you'd allow and the one you'd hardest-block?

**Success signal:** both files exist in your worktree; you can point to the `deny` entry in `settings.local.json` that blocked the write in Step 7.

---

## Done criteria

You have completed the core path when all five are true:

1. `structured-handoff.md` exists in your worktree with Findings, Decisions, and Constraints filled; Decisions scoped to the test-targeted field.
2. You executed the handoff: the failing test now passes, and the diff shows only the scoped line changed (the deferred finding left alone).
3. `.claude/settings.local.json` reflects the three-part model — allow names only the Jira read call(s); deny names the writes plus the Confluence/cross-product tools outside the workflow.
4. Under auto mode, the scoped Jira read succeeded and the comment write was DENIED by your deny rule with no approval prompt.
5. `git worktree list` shows you ran the whole lab inside `lab-7-work`; a `git`-review shows a clean local tree.

---

## Extra credit

These are not required for done-criteria or the completion quiz. Work on them if you finish early or want to go deeper.

1. **Raw transcript vs structured handoff comparison.** Re-run Step 5 a second way: pass the reviewer's full raw transcript to a fresh implementer session instead of your `structured-handoff.md`. Compare which produces the cleaner, more targeted fix — this is the direct proof of why the structured handoff was worth building.

2. **Second sub-agent, real topology.** Dispatch `security-auditor` (haiku, read-only) on the same code and compare its findings to `code-reviewer`'s. Did the two-reviewer fan-out earn its cost?

4. **Tighten the scope further.** Add a second Jira write to your deny list (a transition or an update) and re-run Step 7's write attempt against it. Confirm each named write is blocked independently.

---

## Stuck path

**Atlassian won't connect (Step 0 / 7).** Run `/mcp` to see current status. If **claude_ai_Atlassian** shows disconnected, confirm your read-only Atlassian credentials are set (see the MindTickle pre-work module), then relaunch Claude Code. If you still can't connect, you can still complete the scoping half of the lab: ask Claude to read `.mcp.json` and help you think through which specific Jira read calls a workflow that only reads your most-recent ticket would need, and which it must be blocked from, without calling any tool. You'll produce a valid `.claude/settings.local.json` scope and still hit the scoping done-criteria.

**Sub-agent dispatch confuses you (Step 3).** Ask Claude to dispatch the `code-reviewer` sub-agent to review the dashboard summary function in `server/main.py`, report its findings, and confirm it made no file changes. If Claude seems confused about sub-agents, confirm `.claude/agents/code-reviewer.md` exists in the repo.

**Stuck on the handoff (Step 4).** Ask Claude to draft the three sections and quiz you on the scoping calls — the primary finding (the one the failing test targets), any secondary findings worth deferring, and what the minimal fix must avoid touching. You make the scoping calls; Claude drafts from your answers.

**Stuck on permission scoping (Step 6).** Ask Claude to list the minimal set of Jira tool calls a workflow that only reads your most-recent ticket would need, and every Jira write/admin (plus Confluence/cross-product) call that should be explicitly blocked, without calling any tool. Use that list to fill in your `settings.local.json` allow/deny yourself.

**Fully stuck or out of time.** Check out the reference artifacts from the solution branch to see finished examples. First confirm your remote points at the fork:

```
git remote -v
git fetch origin
git checkout origin/lab-7-solution -- .claude/settings.local.json structured-handoff.md
```

Open both files. You'll see what a complete least-privilege scope and a signal-preserving handoff look like. You still leave having seen the 3-part model applied.

**Reset everything.** Run the `/reset-branch` command (not a skill). It does `branch -D` + `reset --hard` + `clean -fd` with no confirmation, so save anything you want to keep first. With worktree-per-lab you mostly just move to the next lab's worktree. Delete `.claude/settings.local.json` before your next lab so the allow/deny list doesn't carry over.

---

## Sources

- [31-lab-7-remediation-design.md](../../lab-build/31-lab-7-remediation-design.md) — authoritative design (Sections 1-8)
