# Lab 3 Participant Guide
## CLAUDE.md + Context Architecture: Sharp and Layered

**Theme 3 | Foundations**
**Repo:** `ryan-roark-caylent/inventory-management-smarsh` | Branch: `lab-3-start`
**Model:** Sonnet

---

### Before you start

You should have watched the CLAUDE.md pre-reading and completed the pre-work setup in the LMS (MindTickle pre-work module). This lab does not re-teach what a CLAUDE.md is. It builds depth: layering, `@` file injection, de-bloating a real hierarchy, and managing what Claude pays for on every turn.

The core path takes roughly 50 minutes. Extra credit absorbs any remaining time.

---

### What you are building toward

By the end of this lab you will have a sharp, layered CLAUDE.md set that changes what Claude produces on the next task — not because you told Claude what to do that session, but because the instructions ride every request. You will also be able to *see and control* what Claude loads into context on every turn.

**The key insight** lives in Step 5: an `@`-import is **always-on** (it sits in `/context` at launch, before you do anything), while a sub-directory `CLAUDE.md` is **lazy** (it only shows up once Claude touches that directory). Two opposite cost models, both visible in one `/context` reading. You decide which mode fits which content.

Throughout this lab, drive Claude — ask Claude to make the edits. Don't hand-edit the files yourself unless a step says to (the terminal `git mv` and `/context` reads are the exceptions).

---

### Step 0 — You should already be here (fresh session)

You work this lab inside its own git **worktree** so nothing collides with other labs and you keep your work at the end. If your pre-work already created `lab-3-work`, confirm you're in it with `git worktree list`. If not, create it now — run each line separately:

```
git fetch origin
git worktree add -b lab-3-work ../lab-3-work lab-3-start
cd ../lab-3-work
```

Then launch Claude Code from inside `lab-3-work`. (The worktree rule is also in this repo's `CLAUDE.md`.)

> **Tip:** you can run a shell command without leaving Claude Code by prefixing it with `!` (e.g. `!git worktree list`). Handy throughout the labs.

- Quick check: run `/model` and confirm you are on **Sonnet**. Smarsh defaults to Haiku; this lab is tuned for Sonnet. Switch with `/model sonnet` if needed.
- Launch Claude Code fresh in this worktree so it loads the `lab-3-start` CLAUDE.md set.
- **Do not run `/init`.** On a repo that already has a CLAUDE.md, `/init` can offer to regenerate it and would overwrite the planted content that Steps 2-3 depend on. (See Stuck if you did.)

> **Relaunch callout (Windows + macOS — identical guidance):** if a Claude Code session was open before you entered this worktree, quit and relaunch it so the correct CLAUDE.md set loads.

---

### Step 1 — See what is loaded

Run `/context`. Read the output, then open and skim the root `CLAUDE.md`.

Notice: **only the root `CLAUDE.md` is in the launch footprint.** `client/CLAUDE.md` and `server/CLAUDE.md` are not there — they load lazily when Claude works in those subtrees. You will use that fact in Step 5.

Expected shape at launch (read the relative bars, not counts):

```
Context Usage
  System prompt   ▓▓
  Tools           ▓▓▓
  Memory files    ▓▓▓      <- root CLAUDE.md only
    ./CLAUDE.md       (small)
  Messages        ▓
```

---

### Step 2 — Fix stale content and delete credentials (do this before trimming)

The root `CLAUDE.md` has two planted problems:

- A stale **"API Endpoints"** section — it lists `GET /api/suppliers`, which the server does not implement, and omits real endpoints.
- A **"Deployment & Environment Setup"** block with credentials that have no place in a CLAUDE.md.

Ask Claude to (a) delete the credentials block entirely, and (b) fix the stale API list the durable way: replace the hand-maintained inline list with an `@` reference to the file that actually defines the routes, so it can never drift again.

> **Relaunch callout (Windows + macOS):** after the `@` reference is added, quit and relaunch Claude Code, then re-run `/context`. Editing CLAUDE.md mid-session does not reload it — you need a fresh launch to see the `@`-import take effect.

> **Teaching point:** `@`-imports are **eager**. Claude Code pulls the *entire* referenced file into context at launch, every session. Your `/context` footprint is now **larger** than before — the win is the route list can't drift; the cost is the whole file rides every request.

Expected shape after `@server/main.py` + relaunch (footprint LARGER):

```
Context Usage
  System prompt   ▓▓
  Tools           ▓▓▓
  Memory files    ▓▓▓▓▓▓   <- root + eagerly-loaded main.py
    ./CLAUDE.md       (small)
    ./server/main.py  (full file, pulled by @ reference)
  Messages        ▓
```

You know it worked when: the credentials block is gone, the inline endpoint list is replaced by a single `@server/main.py` line, and `/context` shows a larger footprint after relaunch.

---

### Step 3 — Trim the root and add rules (open-ended)

Ask Claude to reduce the root `CLAUDE.md` to: the build/test/lint commands, the top-3 Vue-3 + FastAPI conventions for *this* repo, and **three "always/never" rules drawn from mistakes Claude actually makes on this codebase**. Cut generic advice and noise.

> **Protected — do not trim:** leave the `## Workshop Rule` section intact ("Local commits only; never push…; always run the full test suite…") **and** the `## Working in a Worktree` section (marked "do not remove"). Those are the workshop's own operating rules, not bloat. Tell Claude to keep both.

Real rough edges you can turn into rules (pick at least one, and be ready to defend the layer it belongs at):

- Array-index keys in a `v-for` (`Reports.vue` does this)
- Components that hardcode `http://localhost:8001` instead of routing through `client/src/api.js`
- Counting before filtering instead of after
- Calling a date method before validating the value

Re-run `/context`. You know it worked when: the root file is materially shorter, every line is repo-specific, the Workshop Rule survived, and the footprint **shrank** versus the bloated start — the always-on cost you just stopped paying every turn.

---

### Step 4 — Layer and de-duplicate the sub-files

Open `client/CLAUDE.md` and `server/CLAUDE.md` — hundreds of lines of generic framework tutorial. Ask Claude to cut each to only what is true for *this* repo (the shared filter helper, the api.js-centralization rule, "update the Pydantic model when JSON changes," the v-for-key rule, return `response_model`-typed responses) and remove anything a competent Vue/FastAPI dev already knows or that duplicates the root.

> ---
> **Personal preferences don't belong in a project CLAUDE.md.** Editor settings, "run prettier before showing me a diff," your work hours — those are *yours*, not the repo's. Move them to a personal `~/.claude/CLAUDE.md` that rides with **you** across every repo. Do **not** commit it — it is the personal layer, not the project layer.
> ---

You know it worked when: each sub-file fits on roughly one screen and contains nothing generic; any rule duplicated between root and a sub-file has been hoisted to a single home.

---

### Step 5 — ★ POINT STEP: manage your context (eager vs lazy)

You have now set up two ways CLAUDE.md content reaches Claude. This step makes the difference **visible** so you can decide which to use.

1. Relaunch Claude Code for a clean session. Run `/context`. Look at what is loaded **before you do any work**: the root `CLAUDE.md` and the full `server/main.py` (pulled in eagerly by your Step-2 `@` reference). The sub-CLAUDE.md files are **not** there.
2. **Predict:** is `server/CLAUDE.md` loaded yet? (No — it is lazy.)
3. Ask Claude to work with a file in the server subtree — e.g. "explain what `server/mock_data.py` does." Re-run `/context`.
4. Observe: the footprint **grew**, and a `server/CLAUDE.md` entry now appears. You never asked for it — it loaded the instant Claude touched `server/`.

Expected shape — the contrast:

```
Context Usage
  System prompt   ▓▓
  Tools           ▓▓▓
  Memory files    ▓▓▓▓▓▓   <- root + main.py (unchanged)
    ./CLAUDE.md
    ./server/main.py
  Messages        ▓▓▓▓     <- GREW; server/CLAUDE.md entry appears here
```

The decision this teaches: **`@`-import = always-on** (pay every turn; use it for things Claude must always know and that can't drift, like the route list). **Sub-CLAUDE.md = lazy** (pay only when relevant; use it to scope directory-specific rules so they cost nothing until you are in that directory).

> **Success signal:** you know it worked when the total `/context` footprint is **larger after** Claude works in `server/` than it was at launch, and a `server/CLAUDE.md` entry now appears. **Where it appears (Messages vs Memory files) depends on the Claude version — on current Sonnet it lands under Messages.** Don't look for it only under "Memory files"; look for total growth and the new entry wherever it shows up.

---

### Step 6 — With/without delta

The root `CLAUDE.md` carries a rule that lives **only** in the root: any time Claude creates or significantly modifies a `.vue` file, it must delegate to the `vue-expert` subagent. No sub-file mentions delegation — so renaming the root alone gives you a clean comparison.

1. Ask Claude to **add a supplier column to the inventory table view** (a `.vue` file). Watch the transcript: with the root in place, Claude delegates — you will see a `Task(vue-expert)` call. Note what it produces.
2. Discard that code change and take the root file out of play, then relaunch:

   ```
   git checkout -- .
   git mv CLAUDE.md CLAUDE.md.off
   ```

3. **Relaunch Claude Code** (quit and open a new session).
4. Ask for the **same** change again. This time Claude edits the `.vue` file directly, with no delegation.
5. Record **three concrete differences** between the two runs.

> **Relaunch callout (Windows + macOS):** you must relaunch after renaming a CLAUDE.md — a live session keeps the old context cached and the comparison is meaningless.

> **If a dev server is holding port 8001:** macOS — `lsof -i :8001` then `kill <PID>`. Windows — `netstat -ano | findstr :8001` then `taskkill /PID <PID> /F`.

You know it worked when: you have three concrete differences written down, and can name at least one convention the root file enforced (delegation to `vue-expert`) that the bare run missed.

---

### Step 7 — Keep your work (no commit)

Restore the renamed file:

```
git mv CLAUDE.md.off CLAUDE.md
```

Your layered CLAUDE.md set (root + `client/` + `server/`) plus a short `claude-md-notes.md` prose note — what changed in output quality between the two runs, written as prose, not a token count — is your **personal takeaway**. Keep it in your worktree. **Do not commit or push.** Nothing in this lab goes back to the repo.

---

### Extra credit

1. **`!` bash prefix:** run a few shell commands from inside Claude Code with `!` (e.g. `!git status`, `!ls server/`).
2. **Custom slash commands:** ask Claude to author `.claude/commands/inv-review.md` (reviews a Vue component against your CLAUDE.md rules) and `.claude/commands/route-check.md` (checks a new FastAPI route against existing patterns). Run each against a real file.
3. **Auto-memory observation:** note what Claude's auto-memory has accumulated across sessions and decide whether it belongs in your curated CLAUDE.md or should stay uncurated.

---

### Done criteria

You are done when all four are true:

1. Root `CLAUDE.md` is trimmed, has at least 3 always/never rules, no fake credentials, no nonexistent endpoint, and an `@server/main.py` reference. The `## Workshop Rule` section survived.
2. Both sub-files are cut to repo-specific content with no cross-layer duplication.
3. In Step 5 you saw the total `/context` footprint grow and a `server/CLAUDE.md` entry appear only after Claude worked in `server/`, and you can say why an `@`-import costs on every turn while a sub-file does not.
4. The with/without run in Step 6 produced three written differences.

**Personal takeaway (local, not committed):** your layered CLAUDE.md set (root + `client/` + `server/`) plus `claude-md-notes.md` describing what changed in output quality between the two runs. Write the description as prose, not a token count.

---

### Stuck? Self-service options

> **Before any rescue:** run every command from your worktree root (`pwd` should end in `lab-3-work`), not from `server/` or `client/`. If a command referencing `origin/lab-3-solution` fails with "invalid reference", run `git remote set-branches origin '*'` and `git fetch origin`, then retry. If `git worktree add` says the path "already exists" or the branch "is already used by worktree", run `git worktree list`, remove the stale entry with `git worktree remove <path> --force`, and re-run the `git worktree add` from the main clone root (worktree management commands run there; every other rescue command runs from the worktree).


**If Claude is drifting or producing inconsistent output:** ask Claude to review your current CLAUDE.md set for layering issues — which rules belong at root vs. sub-file, and whether any generic advice slipped back in. Work through the root file first before touching the sub-files.

**If you want to start over from the planted state:** run the `/reset-branch` command in Claude Code (this is a slash command, not a skill). Note that it permanently deletes uncommitted work in this worktree, so keep anything you want first. Then relaunch Claude Code.

**If you want to see the finished target:** first confirm your remote is the fork — run `!git remote -v` and check that `origin` points at `ryan-roark-caylent/inventory-management-smarsh`. Then run `git checkout origin/lab-3-solution -- CLAUDE.md client/CLAUDE.md server/CLAUDE.md` in a terminal and open all three files. You will see the sharp, layered result and can experience the point of the lab even if you ran out of time.

---

Your completion and mastery quizzes are in the LMS.
