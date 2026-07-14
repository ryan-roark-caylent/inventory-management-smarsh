# Lab 1 — The Full Claude Surface: Pick the Right Tool for the Job

**Track:** Foundations (Lab 1 of 9)
**Repo:** your fork of `ryan-roark-caylent/inventory-management-smarsh`
**Model you will use on lab day:** claude-sonnet-5

---

## What this lab is about

You will work on the same bug twice, using two different Claude surfaces. Claude.ai will reason from the symptom you paste in. Claude Code will open the repo, read the relevant file, and name exactly where the problem is and what a fix looks like. Same underlying model, different surfaces, meaningfully different answers.

The moment that lands is the point: the surface you pick determines whether Claude guesses at your bug or reads your code and identifies the exact location. Then you have Claude Code apply the fix, run it, and watch the dashboard respond — a real change, not just a diagnosis. By the end, you will have a `surface-map.md` in your worktree that maps three surfaces to the kinds of work each handles best, with your own routing decisions and reasoning written in.

You already know what each surface does from the pre-work. Today is about choosing correctly under ambiguity.

Your completion and mastery quizzes are in the LMS (MindTickle).

---

## The three surfaces

- **Claude.ai** — browser chat. Reasons from what you type or paste. No repo access.
- **Claude Code** — the CLI in your repo. Reads files, traces across the codebase, proposes file-anchored changes.
- **API / CI** — non-interactive. A scripted call inside a pipeline or scheduled job, no human in the loop.

Two of these you run hands-on today (Claude.ai and Claude Code). The third, API / CI, is non-interactive: you reason about when it fits and sketch it, you do not run a live session against it.

---

## Steps

### Step 0 — Set up your worktree and start the servers

You work this lab inside its own git **worktree** so nothing collides with other labs and you keep your work at the end. If your pre-work already created `lab-1-work`, confirm you're in it with `git worktree list`. If not, create it now — run each line separately:

> **Tip:** you can run a shell command without leaving Claude Code by prefixing it with `!` (e.g. `!git worktree list`). Handy throughout the labs.

```
git fetch origin
git worktree add ../lab-1-work lab-1-start
cd ../lab-1-work
```

Then launch Claude Code from inside `lab-1-work`. (The worktree rule is also in this repo's `CLAUDE.md`.)

- Quick check: run `/model` and confirm you are on **sonnet**. Smarsh defaults to Haiku; this lab is tuned for Sonnet. Switch with `/model sonnet` if needed. (This is the one place `/model` is taught. Step 6 reuses it as pure reasoning.)
- Start the backend and frontend. Ask Claude to start the app (it has a `/start` command), or run the servers yourself in two separate terminals.

> **Fallback (run it yourself, Windows / macOS identical):** run each command on its own line, never joined with `&&`. Backend: `cd server`, then `uv run python main.py`. Frontend (new terminal): `cd client`, then `npm run dev`. (Dependencies were installed in pre-work.)

> **macOS only:** if `uv` is not on your PATH, install it with `brew install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`, then repeat the pre-work install.

**You know it worked when** the backend terminal prints `Uvicorn running on http://0.0.0.0:8001` and `localhost:3000` renders the inventory dashboard.

Now **explore the app before you touch any tool.** Click through the pages (dashboard, orders, reports, backlog). Change the warehouse and category filters and watch the summary tiles react. Get a feel for what this inventory app actually does — you will be working in it across the next several labs, so build a mental model now. As you click, jot down anything that looks off. One thing to watch for: filter by a warehouse (for example, London) and see whether every tile responds. Note the issues you spot; you will route and diagnose one of them next.

**You know it worked when** you have clicked through the main pages, driven the filters, and written down at least one thing that looks wrong (the frozen backlog count is the one this lab chases).

---

### Step 1 — Route the three issues (before opening any tool)

**This is an open-ended judgment step. Do it before you touch Claude.**

Open `docs/lab-1/tracker-issues.md`. It has three issues of distinct shape: (A) a spec/planning question, (B) a multi-file refactor, (C) a batch/CI script.

Open `surface-map.md` at the repo root (it is already on the branch as a template). For **each** of the three issues, write which of the three surfaces you would open first and one sentence of why. Do this before running any tool.

**You know it worked when** `surface-map.md` shows three routing decisions, each with a one-line justification, and you have not yet run Claude on any of them.

---

### Step 2 — See the bug, then Round 1: Claude.ai

You saw it while exploring in Step 0: filter the dashboard by a warehouse (for example, London) and most summary numbers change while the **backlog count stays frozen**. That frozen number is the bug this lab chases.

Now open **Claude.ai** (browser at `claude.ai`) and paste only that symptom, with no repo files attached. Ask it to explain the likely cause. Record its hypothesis under a "Round 1 (Claude.ai)" heading in `surface-map.md`.

**Expected output:** a plausible hypothesis. Claude.ai reasons from what you described, not from the code.

Representative example:
> "The backlog count is likely computed from the full dataset rather than the filtered subset. Check whether the filter is applied to backlog items the same way it is applied to the other summary metrics."

Notice: no filename, no line number. Claude.ai is reasoning from the symptom you gave it.

**You know it worked when** you have a plausible hypothesis that names **no** specific file or line (Claude.ai cannot see the repo).

---

### Step 3 — Round 2: Claude Code on the same bug (POINT STEP)

In the repo root, launch Claude Code. Ask it to find why the dashboard's total backlog count ignores the warehouse filter, and to propose the minimal fix. Record the file, line, and proposed change under "Round 2 (Claude Code)" in `surface-map.md`.

> **Modes and auto mode (quick intro):** Claude Code has permission *modes*. Press **shift-tab** to cycle them and watch the mode indicator change (normal → auto-accept → plan, and back). In **auto mode**, Claude runs its steps without asking you to approve each one. For this lab, stay in normal mode so you see each action. Later labs lean on auto mode, so get comfortable cycling now. This is a light intro; the deep treatment is Lab 7.

> **Windows only:** if a `claude` command opens a browser or login flow, add `--browser msedge`. (macOS opens your default browser automatically.)

**Expected output:** Claude Code reads the repo and names a specific file, function, and line in `server/`. It proposes a concrete minimal change and may surface (or be prompted to surface) a caveat about whether the fix is complete given how the data model is structured.

**You know it worked when** Claude Code names a specific file and line in `server/`, proposes a concrete change, and your Round 2 note is more specific than your Round 1 note. Compare the two rounds. That delta is the lesson: same model, one surface saw the symptom, the other read the code.

---

### Step 4 — Apply the fix and watch it land (PAYOFF STEP)

Diagnosis is not the finish line. Have **Claude Code apply the change it just proposed** to the backlog count, then run the app and see what happens.

Ask Claude Code to make the edit, then to restart or re-hit the backend so the change takes effect. Back on the dashboard at `localhost:3000`, filter by a warehouse again (London) and watch the backlog tile. It is no longer frozen — it now moves with the filter like the other tiles.

Look closely at what it moves *to*. Ask Claude Code whether the number it shows under a warehouse filter is the true count, and have it explain what it finds. The one-line fix is pattern-consistent with the other metrics, but the underlying data model shapes the result — that gap is the teaching point, not a sign the fix is wrong. Note in `surface-map.md`, under a "Round 2" follow-up, what you observed and what a production-complete fix would still require.

> Stay in normal mode so you approve the edit and see it happen. This is the first time in the labs you have Claude Code change real code and you watch the running app respond.

**You know it worked when** the backlog tile responds to the warehouse filter in the UI (it was frozen before), and you can state — from what Claude Code surfaced — why the one-liner is not yet production-complete.

---

### Step 5 — Model and effort selection (reasoning-only)

Two tasks: (i) rename a variable in one file; (ii) refactor `Reports.vue` off its hardcoded `localhost:8001` and into the shared `api.js` client (touches multiple files).

For each task, decide **which model tier and effort or reasoning level you WOULD pick, and why**. The reasoning is the point. You already know how to switch (`/model` from Step 0); you do not need to switch here. Think it through and move on, no need to write it down.

This is a reasoning habit, not a benchmark. Do not run both tasks and compare outputs.

**You know it worked when** you can state, for each task, the tier and effort you would choose and the task-complexity reason behind it.

---

### Step 6 — Finalize (local, no commit)

Review `surface-map.md`. Confirm it has:
- A one-line "when I'd use this" for **all three** surfaces (Claude.ai, Claude Code, API / CI)
- The **three** issue routings with reasoning
- The Round 1 and Round 2 notes showing the specificity delta, plus your Step 4 follow-up on what you observed after applying the fix

**Keep this file in your worktree. It is your personal takeaway. Do not commit it.**

**You know it worked when** `surface-map.md` is complete and saved in your worktree.

---

## Extra credit

These steps absorb extra time and add depth. None are required for the done criteria or quizzes.

**EC1 — Second filter bug.** Ask Claude Code why `GET /api/orders?month=Q1-2026` returns every order instead of none. It should identify where the filter falls through and what the correct behavior should be.

**EC2 — IDE integration leg.** Open a Vue component in your editor with Claude Code's IDE integration active. Ask for an inline explanation of a reactive data flow and review the diff without leaving the editor. Note how the write-loop feel compares to the CLI.

**EC3 — API/CI framing.** For issue C (the batch/CI script), write one paragraph sketching how you would call Claude via the API in a CI step, with no interactive session. Where does the API surface win over the other two?

---

## Done criteria

You are done when:

1. `surface-map.md` contains: a one-line "when I'd use this" for all three surfaces, the three issue routings with reasoning, and the Round 1 / Round 2 notes.
2. Round 1 and Round 2 show the difference in specificity between Claude.ai's response and Claude Code's response.
3. You had Claude Code apply the fix and watched the backlog tile respond to the warehouse filter in the running app (it was frozen before), and you can say why the one-liner is not yet production-complete.
4. The file is saved in your worktree (not committed).

**Personal takeaway:** `surface-map.md`. It holds your three-surface map, your three-issue routing with reasoning, and your Round-1-vs-Round-2 comparison. Keep it; it is yours.

---

## Stuck path

**Servers won't start (port or `uv` issues).**

Confirm `uv` is installed (`uv --version`) and that the venv was created in pre-work (`server/.venv/` should exist). If ports 3000 or 8001 are already in use:

- **Windows:** `netstat -ano | findstr :8001`, then `taskkill /F /PID <pid>` (replace `<pid>` with the PID from the output).
- **macOS:** `lsof -i :8001 | grep LISTEN`, then `kill <pid>`.

If pre-work was not done, run `uv venv` then `uv sync` in `server/` first (allow 3-5 minutes), then start the server. Run each command on its own line.

**Claude Code is not finding the bug.**

Try asking with more direction: point it at the specific function in `server/main.py` that builds the dashboard summary, and ask why the backlog count does not respond to the warehouse filter. If still stuck, open `server/main.py` and look at the function that builds the summary response. Compare how the backlog count is computed against how the inventory and order counts are computed.

**Out of time or too far stuck.**

First run `git remote -v` and confirm `origin` points at your fork. Then:
1. `git stash`
2. `git checkout lab-1-solution`

Open `surface-map.md` (a completed example) and `docs/lab-1/SOLUTION.md`. Read the Round-1-vs-Round-2 comparison and the routing table. You leave having seen the point of the lab even if you did not produce the artifact yourself.
