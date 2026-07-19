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

Steps 0-9 are the core path. Work at your own pace.

---

### Step 0 — Pre-flight check

You work this lab inside its own git **worktree** so nothing collides with other labs and you keep your work at the end. If your pre-work already created `lab-7-work`, confirm you're in it with `git worktree list`. If not, create it now — run each line separately:

```
git fetch origin
git worktree add -b lab-7-work ../lab-7-work lab-7-start
cd ../lab-7-work
```

Then launch Claude Code from inside `lab-7-work`. (The worktree rule is also in this repo's `CLAUDE.md`.)

> **Tip:** you can run a shell command without leaving Claude Code by prefixing it with `!` (e.g. `!git worktree list`). Handy throughout the labs.

Do the following before you begin:

1. **Switch to Sonnet.** Smarsh defaults to Haiku; this lab is tuned for Sonnet. Run `/model sonnet` (or `/model` and pick Sonnet). The point-step behaviors assume Sonnet.

2. **Relaunch Claude Code** so the project `.mcp.json` and `CLAUDE.md` load fresh.

3. **Confirm Atlassian is connected.** Run `/mcp` and confirm **claude_ai_Atlassian** shows connected (this one server covers Jira, Confluence, and cross-product tools together). If it shows disconnected, your credentials aren't set — fix them per the MindTickle pre-work module, then relaunch. (There is no GitHub MCP in this lab — Atlassian only.)

4. **Note the exact Atlassian tool names.** In the `/mcp` view, select the **claude_ai_Atlassian** server and read its tool list. Note the exact names for "get an issue," "search issues," and "add a comment" — they're camelCase with a prefix (e.g. `mcp__claude_ai_Atlassian__getJiraIssue`). You'll need the exact names in Step 7; a guessed name silently mis-scopes.

**Success signal:** `git branch --show-current` (or `git worktree list`) shows you on `lab-7-work`; `/model` shows Sonnet; `/mcp` lists **claude_ai_Atlassian** as connected and you can see its tool names.

> **Windows / macOS (identical):** after any `.mcp.json` or settings change, relaunch Claude Code before testing MCP or permissions. The repo ships a project-scoped `.mcp.json` (Playwright); the Atlassian server you use here is the enterprise connector you signed into with `/mcp`. If MCP auth opens a browser, on Windows add `--browser msedge` to that step; on macOS your default browser opens with no flag.

> **Docs pointer:** anything this card references as "see the pre-work" lives in your **MindTickle pre-work module**, not in this repo.

---

### Step 1 — Set up worktree isolation for parallel agentic work

In Step 0 you launched Claude Code from inside `lab-7-work`, a git **worktree** — a second working directory backed by the same repo, checked out to its own branch. This is your working setup for the rest of the lab, and it's the mechanism that lets you run agentic workflows without stepping on other work.

Confirm it:

```
git worktree list
```

You'll see `lab-7-work` as its own directory, separate from your main checkout. Because it's a distinct working tree, an agent running here can edit, test, and iterate against these files while a completely separate Claude session runs in another worktree on another branch — the two never touch each other's files. That's how you run **multiple agentic workflows in parallel on one codebase without collisions**: give each its own worktree, and each agent's blast radius stops at its own working tree.

That property is why the rest of this lab lives here. In Step 8 you'll turn an MCP-connected agent loose under auto mode; the worktree is what bounds it — the worst case is contained to `lab-7-work`, never your main checkout or another branch. Set the mechanism up front, then build on it.

**Success signal:** `git worktree list` shows `lab-7-work` as an isolated worktree, and you can say why an autonomous agent running inside it can't reach files outside it.

---

### Step 2 — Delegation topology (open-ended judgment)

Before you touch anything, frame the work. You have four tasks for this repo:

- (a) Scan all API routes for missing auth and authorization gaps
- (b) Rename one local variable in `main.py`
- (c) Generate pytest tests for 5 independent endpoints
- (d) Apply a one-line CORS config change

Sort each into **delegate to a sub-agent** vs **keep in a single agent**, and think through which tasks earn a sub-agent's coordination overhead and why. Then decide the delegation topology for anything you'd delegate: which sub-agent does what, in what order.

You don't need to write this down — reason it through and move on. The sort is the mental model the rest of the lab runs on: in Step 4 you'll dispatch the reviewer this thinking tells you is worth delegating.

**Success signal:** you can say which of the four tasks earn a sub-agent and why, and name the topology for any you'd delegate.

---

### Step 3 — Read the trigger (local, read-only)

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

### Step 4 — Dispatch the read-only reviewer

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

### Step 5 — Claude drafts the handoff, then quizzes you

Instead of writing the handoff from scratch (or passing the reviewer's raw transcript downstream), **ask Claude to draft `structured-handoff.md`** with three sections — **Findings / Decisions / Constraints** — and then to **quiz you** on the scoping calls it can't make for you:

- Which finding is the one the failing test targets (the primary), and which are separate known issues to defer?
- What is the minimal fix, and what should it deliberately NOT touch?
- What constraints bound it (in-memory only, no new deps, don't touch other endpoints)?

Answer Claude's questions to lock the Decisions and Constraints yourself. The finished handoff should be shorter than the raw transcript and carry no chat noise. It's a local file in your worktree — you'll hand it to an implementer next.

**Success signal:** `structured-handoff.md` exists with all three sections filled; Decisions is scoped to the test-targeted field and explicitly defers the out-of-scope finding; it reads as signal, not transcript.

---

### Step 6 — Execute the handoff (the payoff)

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

### Step 7 — Scope the connection in `settings.local.json` ★ Point step

You're about to let an agent touch Atlassian. Before you do, decide exactly what it may and may not do — then encode that decision where it's actually enforced.

Notice what you're scoping: the connected server is **one combined `claude_ai_Atlassian` server** — it exposes Jira *and* Confluence *and* cross-product tools (~32 calls, including Confluence page writes and account lookups). Your workflow needs exactly one thing: read your most-recent Jira ticket. Least privilege means allowing those one or two read calls and blocking all the rest.

**Reason through the three-part model** (out loud or in your head — you don't need to write it as prose; the enforcement file below is the artifact that matters):

- **Explicit Read** — the Jira read call(s) only: search my issues, then get the one issue. **(You add these.)**
- **Explicit Write** — **BLOCKED, and shipped that way:** no comment, no create, no transition, no edit, no worklog, no link. Leave the deny list in place.
- **Explicit Blocks** — everything else the server exposes stays denied by default: because you only *allow* the two reads, no other tool (all Confluence, the cross-product `search`/`fetch`, account/admin calls, every other project) is ever approved.

This lab ships with a safety floor already in place: open `.claude/settings.local.json` and you'll find the Jira **writes already denied** (comment, create, edit, transition, worklog, link). That's deliberate — you're pointing an agent at a live Atlassian tenant, and a blocked write is the difference between a safe exercise and a real ticket you didn't mean to touch. Deny always wins over allow, so those writes cannot be re-enabled by an allow entry; the floor holds.

Your job is the **allow** half: add the Jira read call(s) your workflow needs so the read actually works, then confirm the writes are still blocked. Encode it directly in `.claude/settings.local.json` — this is the **deterministic guard** the runtime actually reads. The shape (fill the exact read tool names you confirm from `/mcp`):

> **Why this file, and not CLAUDE.md?** `settings.local.json` is a **deterministic control** — the runtime matches every tool call against these allow/deny lists and blocks a denied call *every time*, with no model judgment involved. A `CLAUDE.md` instruction like "please only read from Jira" is the opposite: it's **non-deterministic guidance** the model may follow, misread, or be talked out of (including by a prompt injection). When you need a guarantee — especially before handing an agent autonomy — put it where the machine enforces it, not where the model interprets it. That's the whole point of this step: the guard, not good intentions, is what holds.

```jsonc
{
  "permissions": {
    "allow": [
      // YOU add these — the read call(s) your workflow needs:
      "mcp__claude_ai_Atlassian__searchJiraIssuesUsingJql",  // find my latest issue
      "mcp__claude_ai_Atlassian__getJiraIssue"               // read that issue
    ],
    "deny": [
      // ALREADY SHIPPED — the write floor. Leave these; deny wins over allow.
      "mcp__claude_ai_Atlassian__addCommentToJiraIssue",     // the write we'll watch get blocked
      "mcp__claude_ai_Atlassian__createJiraIssue",
      "mcp__claude_ai_Atlassian__editJiraIssue",
      "mcp__claude_ai_Atlassian__transitionJiraIssue",
      "mcp__claude_ai_Atlassian__addWorklogToJiraIssue",
      "mcp__claude_ai_Atlassian__createIssueLink"
    ]
  }
}
```

> **Why is the deny list shipped, not authored by you?** You're on a *write-capable* enterprise Atlassian connection, and one fumbled config in auto mode could write to a real ticket. So the writes are denied from the moment you open the lab — a fail-closed floor. You still do the real scoping work: decide and add the minimal **reads**, and reason about *why* each write is denied. In your own projects you'd author both halves; here the block ships first so nobody damages a live tenant while learning.

> **Verify tool names:** open `/mcp`, select the **claude_ai_Atlassian** server, and read its tool list. Confirm every allow/deny entry uses the **exact** tool name it exposes — camelCase with the `mcp__claude_ai_Atlassian__` prefix, not the friendly label. A guessed name silently mis-scopes: the guard won't match, and the block won't fire where you think it does.

> **To be clear — blocking writes is a choice for this exercise, not a universal rule.** Letting Claude comment on, transition, or create Jira issues is a perfectly good real-world setup; plenty of useful workflows need exactly that. We ship the writes blocked here for two reasons: so you can *watch the guard fire* and prove the scope is what stops the call, and so a learner on a live tenant can't accidentally write. The lesson isn't "MCP writes are dangerous" — it's "scope to what the workflow needs, and put guarantees where the machine enforces them." When your own workflow genuinely needs a write, you allow it (and remove the matching deny).

Ask Claude to help you enumerate the minimal read calls the workflow needs, but you decide and defend the allow list yourself.

**Success signal:** `.claude/settings.local.json` allows only the Jira read call(s) you added; the shipped write denials are intact; every allow entry matches an exact `/mcp` tool name. Because only the reads are allowed, everything else the server exposes is never auto-approved — nothing but your reads runs unattended.

---

### Step 8 — Run it under auto mode and watch the write get DENIED ★ Point step

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

### Step 9 — Keep your takeaway (no commit)

Your two local artifacts — `.claude/settings.local.json` (your enforced scope) and `structured-handoff.md` — stay in your worktree as a personal takeaway. **Do not commit or push anything.** The worktree you set up in Step 1 is why they're safely yours: they live in `lab-7-work`, isolated from every other checkout.

Think through (no need to write it down): if you scoped this Jira workflow for your own team, what's the one call you'd allow and the one you'd hardest-block? And note a **qualitative** token-cost estimate for the workflow you ran — relative cost vs a single-agent task, and the biggest cost driver. No absolute number.

**Success signal:** both files exist in your worktree; you can point to the `deny` entry in `settings.local.json` that blocked the write in Step 8.

---

## Done criteria

You have completed the core path when all five are true:

1. `structured-handoff.md` exists in your worktree with Findings, Decisions, and Constraints filled; Decisions scoped to the test-targeted field.
2. You executed the handoff: the failing test now passes, and the diff shows only the scoped line changed (the deferred finding left alone).
3. `.claude/settings.local.json` reflects the three-part model — your allow list names only the Jira read call(s); the shipped deny list (the Jira writes) is intact; and because only the reads are allowed, every other tool the server exposes (Confluence, cross-product, admin) is never auto-approved.
4. Under auto mode, the scoped Jira read succeeded and the comment write was DENIED by your deny rule with no approval prompt.
5. `git worktree list` shows you ran the whole lab inside `lab-7-work`; a `git`-review shows a clean local tree.

---

## Extra credit

These are not required for done-criteria or the completion quiz. Work on them if you finish early or want to go deeper.

1. **Raw transcript vs structured handoff comparison.** Re-run Step 6 a second way: pass the reviewer's full raw transcript to a fresh implementer session instead of your `structured-handoff.md`. Compare which produces the cleaner, more targeted fix — this is the direct proof of why the structured handoff was worth building.

2. **Second sub-agent, real topology.** Dispatch `security-auditor` (haiku, read-only) on the same code and compare its findings to `code-reviewer`'s. Did the two-reviewer fan-out earn its cost?

3. **Tighten the scope further.** Pick a second shipped deny entry (a transition or an edit) and re-run Step 8's write attempt against it. Confirm each named write is blocked independently.

---

## Stuck path

> **Before any rescue:** run every command from your worktree root (`pwd` should end in `lab-7-work`), not from `server/` or `client/` -- and confirm the worktree is a **sibling** of your main clone, not nested inside it: `git worktree list` (from the main clone) should show its path outside the clone directory; if it is nested, `git worktree remove <path> --force` it and re-create it from the main clone root. If a command referencing `origin/lab-7-solution` fails with "invalid reference", run `git remote set-branches origin '*'` and `git fetch origin`, then retry. If `git worktree add` fails, match the error: "already exists" for a path `git worktree list` shows means a stale entry (`git worktree remove <path> --force`); "already exists" for a path it does NOT show means a plain leftover directory (delete the directory itself and retry); "a branch named `lab-7-work` already exists" means reuse it (`git worktree add ../lab-7-work lab-7-work`) or delete it first (`git branch -D lab-7-work`). Worktree management commands run from the main clone root; every other rescue command runs from the worktree. Worked in the main clone by mistake? The repo's `CLAUDE.md` "Worktree Isolation" section has the exact recovery steps -- ask Claude to walk you through them. Bring any uncommitted work along: `git stash -u` in the main clone, then `git stash pop` inside the worktree (the stash is shared between them).


**Atlassian won't connect (Step 0 / 8).** Run `/mcp` to see current status. If **claude_ai_Atlassian** shows disconnected, confirm your read-only Atlassian credentials are set (see the MindTickle pre-work module), then relaunch Claude Code. If you still can't connect, you can still complete the scoping half of the lab: the write deny list is already shipped in `.claude/settings.local.json`, so think through which Jira read calls a workflow that only reads your most-recent ticket would need (search for the issue, get the issue) and add those to the `allow` list using the tool names shown on the card — without calling any tool. You'll produce a valid scope and still hit the scoping done-criteria.

**Sub-agent dispatch confuses you (Step 4).** Ask Claude to dispatch the `code-reviewer` sub-agent to review the dashboard summary function in `server/main.py`, report its findings, and confirm it made no file changes. If Claude seems confused about sub-agents, confirm `.claude/agents/code-reviewer.md` exists in the repo.

**Stuck on the handoff (Step 5).** Ask Claude to draft the three sections and quiz you on the scoping calls — the primary finding (the one the failing test targets), any secondary findings worth deferring, and what the minimal fix must avoid touching. You make the scoping calls; Claude drafts from your answers.

**Stuck on permission scoping (Step 7).** The writes are already denied in the shipped `settings.local.json`. Ask Claude to list the minimal set of Jira read calls a workflow that only reads your most-recent ticket would need, without calling any tool. Use that list to fill in the `allow` array yourself; leave the shipped deny list in place.

**Fully stuck or out of time.** Check out the reference artifacts from the solution branch to see finished examples. First confirm you are on your `lab-7-work` branch (`git branch --show-current`) -- this checkout overlays the solution files onto whatever branch is currently checked out, silently -- and that your remote points at the fork:

```
git remote -v
git fetch origin
git checkout origin/lab-7-solution -- .claude/settings.local.json structured-handoff.md
```

Open both files. You'll see what a complete least-privilege scope and a signal-preserving handoff look like. You still leave having seen the 3-part model applied.

**Reset everything** (this permanently discards your work in this lab -- keep anything you want first): exit Claude Code, then from the **main clone root** run each line on its own:

```
git worktree remove ../lab-7-work --force
git branch -D lab-7-work
git worktree add -b lab-7-work ../lab-7-work lab-7-start
```

Then `cd ../lab-7-work` and relaunch Claude Code. With worktree-per-lab you mostly just move to the next lab's worktree. Delete `.claude/settings.local.json` before your next lab so the allow/deny list doesn't carry over.

---

