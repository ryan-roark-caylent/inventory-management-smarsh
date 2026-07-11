# Lab 1 — The Full Claude Surface: Pick the Right Tool for the Job

**Track:** Foundations (Lab 1 of 9)
**Repo:** your fork of `ryan-roark-caylent/inventory-management-smarsh`
**Model you will use on lab day:** claude-sonnet-5

---

## What this lab is about

You will work on the same bug twice, using two different Claude surfaces. Claude.ai will reason from the symptom you paste in. Claude Code will open the repo, read the relevant file, and name exactly where the problem is and what a fix looks like. Same underlying model, different surfaces, meaningfully different answers.

The moment that lands is the point: the surface you pick determines whether Claude guesses at your bug or reads your code and identifies the exact location. By the end, you will have a `surface-map.md` committed to the branch, mapping all four surfaces to the kinds of work each handles best, with your own routing decisions and reasoning written in.

Your completion and mastery quizzes are in the LMS.

---

## Pre-work (Skilljar, before lab day)

These installs must be complete before the session. Skipping them on lab day consumes most of your setup window on Windows.

Run each command on its own line (never joined together on one line).

**Backend (in one terminal):**
1. `cd server`
2. `uv venv`
3. `uv sync`

**Frontend (in a new terminal):**
1. `cd client`
2. `npm install`

Both should complete with no errors. If either fails, resolve it before lab day.

---

## Steps

### S0 — Setup

1. `git fetch origin`
2. `git checkout -b lab-1-work origin/lab-1-start`
3. Start the backend and frontend. Use two separate terminals.

> **Windows:** run each command on its own line (not joined on one line). Backend: `cd server`, then `uv run python main.py`. Frontend (new terminal): `cd client`, then `npm run dev`.

> **macOS:** same commands work in Terminal. Backend: `cd server`, then `uv run python main.py`. Frontend (new terminal): `cd client`, then `npm run dev`. If `uv` is not on your PATH, install it with `brew install uv` or by running `curl -LsSf https://astral.sh/uv/install.sh | sh`, then repeat the pre-work steps.

**Expected output:**

The backend terminal should print:
```
Uvicorn running on http://0.0.0.0:8001
```

Open `localhost:3000` in a browser. The inventory dashboard should load.

---

### S1 — Route the three issues (do this BEFORE opening any tool)

**This is an open-ended judgment step. Do it before you touch Claude.**

4. Open `docs/lab-1/tracker-issues.md`. It has three issues of distinct shape: (A) a spec/planning question, (B) a multi-file refactor, (C) a batch/CI script.
5. Open `surface-map.md` at the repo root (it is already on the branch as an empty template). For each of the three issues, write which Claude surface you would open first and one sentence of why. Do this before running any tool.

The four surfaces are: Claude.ai, Claude Code, Claude Cowork, API/CI.

**You know it worked when** `surface-map.md` has three routing decisions, each with a one-line justification, and you have not yet run Claude on any of the issues.

---

### S2 — Round 1: Claude.ai on the bug

6. Here is the symptom: on the dashboard, filtering by a warehouse changes most summary numbers, but the backlog count never moves.

   In **Claude.ai** (browser, `claude.ai`), paste only that symptom description with no repo files attached. Ask Claude to explain the likely cause.

7. Record its response under a "Round 1 (Claude.ai)" heading in `surface-map.md`.

**Expected output:**

A plausible hypothesis about where the bug likely is. Claude.ai will reason from what you described, not from the code itself.

Representative example:
> "The backlog count is likely computed from the full dataset rather than the filtered subset. Check whether the filter is applied to backlog items the same way it's applied to the other summary metrics."

Notice: no filename, no line number. Claude.ai is reasoning from the symptom you gave it.

**You know it worked when** you have a hypothesis that does not name a specific file or line in the repo.

---

### S3 — Round 2: Claude Code on the same bug (POINT STEP)

8. In the repo root, launch Claude Code. Ask Claude Code to find why the dashboard's total backlog count ignores the warehouse filter, and to propose the minimal fix.

> **Windows:** if a `claude` command opens a browser or login flow, add `--browser msedge` to the command.

> **macOS:** no `--browser` flag needed. Claude Code opens your default browser automatically.

9. Record what it found under "Round 2 (Claude Code)" in `surface-map.md`: the file it named, the line, and what it proposed.

**Expected output:**

Claude Code reads the repo and names a specific file, function, and line number. It proposes a minimal change and may also surface a caveat about whether the fix is complete given how the data model is structured. Contrast this against the Round 1 response.

Compare the two rounds. The delta is the lesson: same model, one surface saw the symptom, the other read the code.

**You know it worked when** Claude Code names a specific file and line in `server/`, proposes a concrete change, and your Round 2 note is more specific than your Round 1 note.

---

### S4 — Model and effort selection

10. Two tasks: (i) rename a variable in one file; (ii) refactor `Reports.vue` off its hardcoded `localhost:8001` and into the shared `api.js` client (touches multiple files). For each, choose a model tier and an effort or reasoning level, and write one sentence of reasoning in `surface-map.md`.

This is a reasoning habit, not a benchmark run. Do not run both tasks and compare outputs. The goal is to make a considered choice based on task complexity and write down why.

**You know it worked when** `surface-map.md` has two model/effort choices, each tied to why that task warrants that tier.

---

### S5 — Cowork and finalize

11. Add the fourth surface: write your one-sentence "when I'd use Claude Cowork" (the desktop app suited for doc and plan work away from the repo).

12. Review `surface-map.md`. Confirm it has:
    - A one-line "when I'd use this" for all four surfaces (Claude.ai, Claude Code, Claude Cowork, API/CI)
    - The three issue routings with reasoning
    - Round 1 and Round 2 notes showing the specificity difference
    - Two model/effort choices with reasoning

13. Commit:
    - `git add surface-map.md`
    - `git commit -m "lab-1: surface selection map"`

**Expected output:**

```
git log --oneline -1
```

Shows your commit message: `lab-1: surface selection map`

**You know it worked when** `git log --oneline -1` shows your commit and `surface-map.md` is complete.

---

## Extra credit

These steps absorb extra time and add depth. None are required for the done criteria or quizzes.

**EC1 — Second filter bug.** Ask Claude Code why `GET /api/orders?month=Q1-2026` returns every order instead of none. It should identify where the filter falls through and what the correct behavior should be.

**EC2 — IDE integration leg.** Open a Vue component in your editor with Claude Code's IDE integration active. Ask for an inline explanation of a reactive data flow and review the diff without leaving the editor. Note how the write-loop feel compares to the CLI.

**EC3 — API/CI framing.** For issue C (the batch/CI script), write one paragraph sketching how you would call Claude via the API in a CI step, with no interactive session. Where does the API surface win over the other three?

**EC4 — Implement the fix.** Apply Claude Code's proposed change to the backlog count, then call `/api/dashboard/summary?warehouse=London` and observe what the count returns. The result is a teaching point about the data model. Think about what a production-complete fix would require beyond the one-liner.

---

## Done criteria

You are done when:

1. `surface-map.md` is committed and contains: a one-line "when I'd use this" for all four surfaces, the three issue routings with reasoning, and two model/effort notes.
2. Round 1 and Round 2 are recorded in `surface-map.md`, showing the difference in specificity between Claude.ai's response and Claude Code's response.
3. `git log --oneline -1` shows your commit.

**Share-back artifact:** `surface-map.md`. This is a real file worth showing. It holds your four-surface map, your three-issue routing with reasoning, and your model/effort thinking.

---

## Stuck path

**Servers won't start (port or `uv` issues).**

Confirm `uv` is installed (`uv --version`) and that the venv was created in pre-work (`server/.venv/` should exist). If ports 3000 or 8001 are already in use:

- **Windows:** `netstat -ano | findstr :8001`, then `taskkill /F /PID <pid>` (replace `<pid>` with the PID from the output).
- **macOS:** `lsof -i :8001 | grep LISTEN`, then `kill <pid>`.

If pre-work was not done, run `uv venv` then `uv sync` in `server/` first (allow 3-5 minutes), then start the server.

Run each command on its own line.

**Claude Code is not finding the bug.**

Try asking with more direction: point it at the specific function in `server/main.py` that builds the dashboard summary, and ask why the backlog count doesn't respond to the warehouse filter. If still stuck, open `server/main.py` and look at the function that builds the summary response. Compare how the backlog count is computed against how the inventory and order counts are computed.

**Out of time or too far stuck.**

Run:
1. `git stash`
2. `git checkout lab-1-solution`

Open `surface-map.md` (a completed example) and `docs/lab-1/SOLUTION.md`. Read the Round-1-vs-Round-2 comparison and the routing table. You leave having seen the point of the lab even if you didn't produce the artifact yourself.
