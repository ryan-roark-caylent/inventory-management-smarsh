# Lab 3 Participant Guide
## CLAUDE.md + Context Architecture: Sharp, Layered, Cache-Aware

**Theme 3 | Foundations**
**Repo:** `ryan-roark-caylent/inventory-management-smarsh` | Branch: `lab-3-start`
**Model:** claude-sonnet-5

---

### Before you start

You should have completed the CLAUDE.md pre-reading on Skilljar. This lab does not re-teach what a CLAUDE.md is. It builds depth: layering discipline, `@` file injection, cache-aware ordering, and de-bloating a real hierarchy.

---

### What you are building toward

By the end of this lab you will have a sharp, layered, cache-ordered CLAUDE.md set that changes what Claude produces on the next task -- not because you told Claude what to do, but because the instructions ride every request.

**The key insight** lives in Step 6: the *order* of lines in your CLAUDE.md has a cost. Moving a volatile "currently working on..." line from the top to the bottom does not change the file's size, but it preserves the model's KV-cache prefix for the stable content above it. You will see this live by re-running `/context` before and after the reorder.

The core path takes roughly 50 minutes. Extra credit absorbs any remaining time.

---

### Step 0 -- Setup (fresh session required)

Open a terminal and run these commands one at a time:

```
git fetch origin
git checkout -b lab-3-work origin/lab-3-start
```

Then **relaunch Claude Code in a new terminal window** so it loads the `lab-3-start` CLAUDE.md set fresh.

> **Windows:** after switching branches, close your current Claude Code session and open a new one. A session that was open before checkout keeps the old context loaded.

> **macOS:** same requirement. Quit Claude Code and relaunch after switching branches. The active session caches the CLAUDE.md set it opened with.

**Do not run `/init`.** On a repo that already has a CLAUDE.md, `/init` can offer to regenerate it. Accepting that offer overwrites the planted content that Steps 2-4 depend on. If you accidentally ran `/init` and see a clean file with no "My Preferences" section or unusual content, restore it by running `git checkout origin/lab-3-start -- CLAUDE.md` in a terminal, then relaunching Claude Code.

---

### Step 1 -- See what is loaded

Run `/context`. Read the output. Notice:

- Only the root `CLAUDE.md` appears in the launch footprint.
- `client/CLAUDE.md` and `server/CLAUDE.md` are not there yet -- they load lazily when Claude accesses files in those subtrees.

Expected shape at launch:

```
Context Usage
  System prompt        ▓▓
  Tools                ▓▓▓
  Memory files         ▓▓▓       <- root CLAUDE.md only
    ./CLAUDE.md            (small)
  Messages             ▓
```

Now trigger the sub-file loads: ask Claude to open and describe `client/src/api.js` and `server/main.py`. Then re-run `/context`.

You know it worked when: your `/context` output shows a materially larger footprint than at launch, with entries for both `client/CLAUDE.md` and `server/CLAUDE.md` present. The exact section they appear in varies by Claude version -- what matters is that both entries are present and the footprint grew. Notice how much larger the `client/CLAUDE.md` entry is relative to the root.

Expected shape after sub-file load:

```
Context Usage
  System prompt        ▓▓
  Tools                ▓▓▓
  Memory files         ▓▓▓▓▓▓▓   <- sub-files now loaded
    ./CLAUDE.md            (small)
    ./client/CLAUDE.md     (large)
    ./server/CLAUDE.md     (medium)
  Messages             ▓▓
```

> **Note:** having Claude open a source file in the subtree (`client/src/api.js` or `server/main.py`) is the reliable trigger. Asking Claude to read the CLAUDE.md files directly may not trigger the mechanism.

---

### Step 2 -- Trim the root and add rules (open-ended)

Ask Claude to reduce the root `CLAUDE.md` to: the build/test/lint commands, the top-3 Vue-3 + FastAPI conventions for this repo, and **three "always/never" rules drawn from mistakes Claude actually makes on this codebase**.

The starting file has generic advice, personal preferences, and noise that belongs in the sub-files or nowhere. Ask Claude to help you cut it down.

For the three always/never rules, you choose at least one and you must be able to defend why it belongs at the root layer. Here are real rough edges in this codebase to consider:

- Rendering bugs from array-index keys in `v-for` loops
- Components that bypass `client/src/api.js` and hardcode a URL directly
- Filter helpers that count before filtering instead of after
- Date methods called before validating the value

You know it worked when: the root file is materially shorter and every line is repo-specific. A new hire could read it and learn a real quirk about this codebase, not a general best practice.

---

### Step 3 -- Fix stale content and delete credentials

The root `CLAUDE.md` on `lab-3-start` carries two problems: a stale "API Endpoints" section (it lists an endpoint the server does not implement, and omits endpoints that do exist) and a "Deployment & Environment Setup" block with fake credentials that have no place in a CLAUDE.md.

Ask Claude to find why the API Endpoints section is stale by comparing it against `server/main.py`, correct the endpoint list, and delete the credentials block entirely.

Before the fix, the stale section looks like this:

```
## API Endpoints
- GET /api/inventory - Filters: warehouse, category
- GET /api/orders - Filters: warehouse, category, status
- GET /api/suppliers - Supplier directory lookup
- GET /api/dashboard/summary - All filters
...
(reports endpoints missing)
```

You know it worked when: the nonexistent endpoint is gone and the credentials block no longer appears in the file.

---

### Step 4 -- `@` injection

Rather than describing the API inline, you can replace the endpoint list with an `@` reference to the file that actually defines the routes. This guarantees the list matches the code -- it cannot drift the way a hand-maintained inline list can.

Ask Claude to replace the inline endpoint list with a reference to the file that is the authoritative source of route definitions.

You know it worked when: the inline endpoint list is replaced by a single `@server/main.py` line, and `/context` shows a larger memory footprint than before this change.

Expected shape after `@` injection:

```
Context Usage
  System prompt        ▓▓
  Tools                ▓▓▓
  Memory files         ▓▓▓▓▓▓   <- root + eagerly-loaded main.py
    ./CLAUDE.md            (small)
    ./server/main.py       (309 lines, loaded by @ reference)
  Messages             ▓
```

> **Teaching point:** `@`-imports are eager. Claude Code pulls the entire referenced file into context when the parent CLAUDE.md loads. The footprint grew because the full `main.py` is now loaded on every session start. That is the tradeoff: the route list cannot drift, but 309 lines are in context on every session launch. Whether the tradeoff is worth it depends on how often the file changes and how large it is.

---

### Step 5 -- Layer and de-duplicate

Open `client/CLAUDE.md` and `server/CLAUDE.md`. They are hundreds of lines of generic framework tutorial. Ask Claude to cut each to only the specifics true for this repo and remove anything that:

- A competent Vue or FastAPI developer already knows
- Duplicates something already in the root

For personal preferences (editor settings, formatting instructions), move them to a `~/.claude/CLAUDE.md` stub. Do **not** commit that file -- it is the personal layer, not the project layer.

You know it worked when: each sub-file fits on roughly one screen and contains nothing generic.

---

### Step 6 -- Context-cost audit (point step)

Run `/context`. Now go through the root `CLAUDE.md` line by line and categorize each line as:

- **Stable:** conventions, rules, commands -- rarely changes
- **Volatile:** session/sprint-specific content -- changes frequently

Ask Claude to help you move every volatile line into a `# Session Context` block at the *bottom* of the file.

Re-run `/context`.

Then write **one sentence** explaining why the order matters even though the file size did not change. Your answer should name the KV-cache prefix.

You know it worked when: the `# Session Context` block is at the bottom and your one-sentence note names the KV-cache prefix.

> The insight: any edit to an early line busts the KV-cache prefix for every token that follows. Stable content at the top stays cached across requests. Volatile content at the bottom changes without busting the stable prefix above it.

---

### Step 7 -- With/without delta

Ask Claude to add a `supplier` field to the inventory endpoint response. Note what it produces.

Now rename the root file in a terminal:

```
git mv CLAUDE.md CLAUDE.md.off
```

**Relaunch Claude Code** (quit and open a new session).

Ask for the same change again. Record **three concrete differences** between the two outputs.

> **Windows:** you must relaunch Claude Code after renaming. A live session keeps the old context cached and the comparison is meaningless.

> **macOS:** same requirement. Quit and relaunch after renaming. If a dev-server process is holding port 8001, stop it with: `lsof -i :8001` to find the PID, then `kill <PID>`.

> **Windows equivalent for stopping a process on port 8001:** run `netstat -ano | findstr :8001` to find the PID, then `taskkill /PID <PID> /F`.

You know it worked when: you have three concrete differences written down and can name at least one convention the CLAUDE.md enforced that the "without" run missed.

---

### Step 8 -- Commit

Restore the file:

```
git mv CLAUDE.md.off CLAUDE.md
```

Then commit the layered CLAUDE.md set (root, `client/`, `server/`) plus a short `claude-md-notes.md` file that describes in prose what changed between the with and without runs. Write the note as prose, not a token count.

---

### Extra credit

1. **Custom slash commands:** author `.claude/commands/inv-review.md` (a command that reviews a Vue component against your CLAUDE.md rules) and `.claude/commands/route-check.md` (a command that checks a new FastAPI route against existing patterns). Run each against a real file.
2. **Reference-good check:** ask Claude to critique your trimmed root file against this bar: "would a new hire understand this repo's quirks from this?" Then iterate once based on the feedback.
3. **Auto-memory observation:** note anything Claude's auto-memory has accumulated across sessions and decide whether it belongs in your curated CLAUDE.md or should stay uncurated.

---

### Done criteria

You are done when all four are true:

1. Root `CLAUDE.md` is trimmed, has at least 3 always/never rules, no fake credentials, no nonexistent endpoint, and an `@server/main.py` reference.
2. Both sub-files are cut to repo-specific content with no cross-layer duplication.
3. Running `/context` shows a `# Session Context` block at the bottom of the root file, and you have a one-sentence cache note ready to share.
4. The with/without run produced three written differences.

**Share-back artifact:** your committed layered CLAUDE.md set (root + `client/` + `server/`) plus `claude-md-notes.md` describing what changed in output quality between the two runs. Write the description as prose, not a token count.

---

### Stuck? Self-service options

**If Claude is drifting or producing inconsistent output:** ask Claude to review your current CLAUDE.md set for layering issues -- which rules belong at root vs. sub-file, whether any volatile content sits above stable content, and whether any generic advice slipped back in. Work through the root file first before touching the sub-files.

**If you want to start over from the planted state:** run `/reset-branch` in Claude Code (this removes `lab-3-work` and returns to `main`). Then, in a terminal:

```
git fetch origin
git checkout -b lab-3-work origin/lab-3-start
```

Then relaunch Claude Code. The shared `lab-3-start` branch on origin is unchanged.

**If you want to see the finished target:** run `git checkout lab-3-solution` in a terminal, then relaunch Claude Code. Run `/context` and open all three CLAUDE.md files. You will see the sharp, layered, cache-ordered result and can experience the point of the lab even if you ran out of time.

---

Your completion and mastery quizzes are in the LMS.
