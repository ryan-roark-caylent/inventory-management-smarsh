# Lab 6: Claude Skills — Build It, Trigger It, Automate Around It

**What you'll have when you're done:** a skill you named and built from scratch that fires on plain-English requests without you typing `/name`, a PostToolUse hook that runs your backend test suite automatically after every edit, and a written rubric decision committing your own weekly workflow to one of the five Claude Code customization abstractions. All of it stays local in your worktree — nothing gets pushed to the repo.

**Track:** 2 (Vibecode). Builds on Lab 3 (CLAUDE.md / context) and Lab 5 (multi-step workflows + debugging loop).

This lab runs a little long because it carries skill-authoring and hook-wiring competencies that the Agent Skills Academy course does not cover. It sits near Lab 4 in depth.

**Your completion and mastery quizzes are in the LMS (MindTickle).** Prerequisites and install steps are in the MindTickle pre-work module.

---

## Before you start

- Fork: `ryan-roark-caylent/inventory-management-smarsh`
- Starting branch: `lab-6-start`
- Complete the MindTickle pre-work module first: it installs `uv` and node/npm, runs `npm install` and a client boot.

---

## Core path (Steps 0–7)

### Step 0 — Setup

You work this lab inside its own git **worktree** so nothing collides with other labs and you keep your work at the end. If your pre-work already created `lab-6-work`, confirm you're in it with `git worktree list`. If not, create it now — run each line separately:

```
git fetch origin
git worktree add ../lab-6-work lab-6-start
cd ../lab-6-work
```

Then launch Claude Code from inside `lab-6-work`. (The worktree rule is also in this repo's `CLAUDE.md`.)

- Run `/model sonnet`. Smarsh defaults to Haiku; this lab's trigger behavior is tuned for Sonnet. (How-to: type `/model`, then pick Sonnet.)
- Start the servers: ask Claude to run the `/start` command, or run the start script for your OS (`scripts\start.ps1` on Windows, `scripts/start.sh` on Mac). Then open the app.
- Open a **fresh** Claude Code session so it loads this branch's `CLAUDE.md`.

You are isolated by construction: because you work in the `lab-6-work` worktree the whole time, there is no branch-switch and no reset to worry about — your edits can't cross-contaminate anything.

**You know it worked when:** the app loads at `http://localhost:3000` and running the backend tests manually reports all passing:

```
uv run --project server pytest tests/backend/ -q
```

---

### Step 1 — Name your skill (open-ended)

The skill you're building automates this workflow: generate pytest tests for a FastAPI endpoint. You build exactly this skill.

**You decide the name.** Call it whatever you would call it if you were adding it to your own team's repo — the reference solution happens to be `gen-tests`, but you are not required to match it. Think through one reason your name is a good routing signal, then move on.

> **Card aside:** a too-generic name (for example `helper` or `tests`) gives Claude a weaker routing signal. You'll feel this in Step 3.

**Success signal:** a new file exists at `.claude/skills/<your-name>/SKILL.md`.

---

### Step 2 — Author with a deliberately weak description

Ask Claude to write the skill body so it does the real work, but set the `description:` frontmatter to a **bare title**: one short phrase that names the skill and says nothing about when to use it and gives no example phrasings (for example, `description: Generates tests.`).

> **Relaunch Claude Code after saving `SKILL.md`.** Skill name and description metadata load at session start, so the skill is not active until you relaunch — on all platforms. On Mac, quit the terminal Claude session and start a fresh one (`claude` in a new tab); on Windows, relaunch the app.

After relaunching, ask Claude, in plain English, to do exactly the task the skill covers. Do **not** type `/<your-name>`.

**Success signal (the designed failure):** Claude answers your request directly and invokes no skill at all. You will not see a `Skill(...)` line in the transcript — not your skill, not any skill. This is expected.

> If you DO see any skill fire here, tell your champion — the branch is misconfigured.

Expected transcript shape:
```
> [your natural-language request about the task]
I'll write tests for the endpoint. Here's a test file...
(no skill invocation appears — not yours, not any)
```

---

### Step 3 — Tune the description until YOUR skill fires (point step)

Ask Claude to rewrite the `description:` as a routing signal: one sentence on what the skill does, plus **at least five example phrasings** a teammate might type to invoke it. Save the file.

> **Relaunch after each description save** (same as Step 2 — metadata loads at session start on all platforms). The loop is: rewrite → save → relaunch → test.

After relaunching, re-issue the same plain-English request from Step 2. If the skill still doesn't fire, add more trigger phrasings and synonyms, save, relaunch, and retry.

Expect more than one pass — the number depends on the live model, so notice that it took iteration (you don't need to record the exact count).

**Success signal:** the transcript shows **`Skill(<your-name>)`** — your exact chosen name — on a request with no `/<your-name>`. The signal is your name specifically, not "a skill loaded." You matched the words in the description to the request: a description is a routing signal, not a label.

Expected transcript shape:
```
> [your natural-language request about the task]
Skill(<your-name>)
Reading tests/backend/ conventions and the target endpoint...
```

---

### Step 4 — Run it explicitly and read the output

Invoke `/<your-name>` directly against a real endpoint in the repo (for example, the `/api/orders` endpoint).

**Success signal:** the skill produces a runnable Python test file grounded in real repo content. It should use the shared `client` fixture from `tests/backend/conftest.py` and mirror the class-based structure in the existing test files.

Abridged shape of a well-grounded output:
```python
# tests/backend/test_orders.py  (abridged)
class TestOrdersEndpoints:
    def test_get_orders_returns_200(self, client):
        response = client.get("/api/orders")
        assert response.status_code == 200
    # ... additional test_ methods
```

You do not need to run the generated file to pass this step. Reading it and confirming it is grounded in repo content is sufficient. To study a fuller set of testing patterns for structure, read `docs/lab-6/backend-test-patterns.md`.

---

### Step 5 — Wire the auto-test hook and prove it

Ask Claude to author `.claude/settings.json` with a **PostToolUse** hook. The hook should use a matcher for Write and Edit operations, and it should run the test script that already ships on this branch at `.claude/hooks/run_backend_tests.py`. Failures should print to stderr.

> **Relaunch Claude Code after saving `.claude/settings.json`.** Hooks load at session start on all platforms. On Mac, quit and start a fresh session; on Windows, relaunch the app.

**Prove it works:** ask Claude to change the low-stock comparison in `get_dashboard_summary` (`server/main.py`) from `<=` to `<`. Watch what happens before Claude's next turn.

**Run it and look (optional):** before the edit, glance at the dashboard's low-stock count in the open UI. After the bad edit, the boundary item drops out of that count. This lab is mostly backend, so this is an optional observability beat — the hook's stderr failure is the real signal.

**Success signal (the hook fires on the bad edit):** you see a pytest failure in stderr naming the dashboard low-stock test:
```
Backend tests failed after this edit:
FAILED tests/backend/test_dashboard.py::TestDashboardEndpoints::test_dashboard_low_stock_items_calculation
assert 4 == 5
```

Then ask Claude to revert the change.

**Success signal (after revert):** all backend tests pass (`N passed`). What matters is red on the bad edit, green after revert.

---

### Step 6 — Apply the 5-abstraction rubric (open-ended)

Open the reference at `docs/lab-6/five-abstraction-rubric.md`.

Write a weekly workflow you actually do (one sentence). Apply the rubric and **commit to exactly one** of: CLAUDE.md / skill / hook / subagent / MCP. State the deciding factor. For example: "must run automatically without being asked, and the logic belongs outside the context window" points to a hook.

Save your decision and one-line justification to `rubric-decision.md` at the repo root. This is a genuine deliverable — write it down.

**Success signal:** `rubric-decision.md` names one abstraction and states the deciding factor.

---

### Step 7 — Keep your artifacts (no commit)

Your three artifacts stay **local in your worktree** — they are your personal takeaway:

- `.claude/skills/<your-name>/SKILL.md`
- `.claude/settings.json`
- `rubric-decision.md`

**Do NOT `git add` or `git commit`.** Nothing gets pushed to the repo.

**Success signal:** `git status` shows the three files present (as new/untracked or modified) in your worktree. You keep them; you do not commit them.

---

## Done criteria

All three of these are observable on your own screen:

1. Your skill fires from a natural-language request — `Skill(<your-name>)`, your own name, is visible in the transcript (Step 3).
2. After the planted off-by-one, the hook surfaces a pytest failure in stderr; after revert, green (Step 5).
3. `git status` lists all three artifacts present in your worktree — the skill, the settings file, and `rubric-decision.md` (Step 7).

---

## Extra credit

Not required for any quiz or done-criteria. Use these if you finish early.

**EC-1 — Second skill, disambiguation.** Build one of two additional skills: `/inv-review` (flags FastAPI anti-patterns in a diff) or `/pr-desc` (drafts a PR description from `git diff --staged`). Test whether a natural-language request routes to the right skill, or whether the two descriptions collide. Tighten the description of whichever skill loses.

**EC-2 — Scope the hook down.** The shipped hook runs the full suite on every server edit. Rewrite it (or the script) to run only the affected test file. Note the tradeoff you accepted (speed vs. missed cross-file regressions).

**EC-3 — Rubric round two.** Name a workflow that should be a **subagent** or **MCP**, not a skill, and defend why a skill is the wrong tool for it. This stretches the rubric past the CLAUDE.md-vs-skill case.

**EC-4 — Test a neighbor.** Hand your `SKILL.md` to a peer (or re-read it cold). Would the description trigger for someone who didn't write it? Revise for a cold reader.

---

## If you get stuck

**Skill won't implicit-trigger after several rewrites.**
Explicit invocation always works: type `/<your-name>` directly to continue the lab. If it still won't route from natural language, add more trigger phrasings and synonyms to the description, save, relaunch, and retry. The point holds either way: what's in the description is what does the routing.

**Hook doesn't fire.**

1. Relaunch Claude Code after saving `.claude/settings.json`. Hooks load at session start on all platforms.
2. Confirm the file is valid JSON. A trailing comma breaks it.
3. Confirm `uv` is on PATH: run `uv run --project server pytest tests/backend/ -q` by hand.

**Pytest errors or can't tell red from green.**
Run the suite by hand:

```
uv run --project server pytest tests/backend/ -q
```

Your PostToolUse hook should surface a `test_dashboard_low_stock_items_calculation` failure in stderr once the planted change is active, and green once it is resolved. If you cannot tell red from green here, that is the signal your hook is not wired correctly yet, not that your fix is wrong.

Note: `/reset-branch` is a **command** on this branch (`.claude/commands/reset-branch.md`), not a skill — a useful reminder for this lab, which is all about the skill-vs-command distinction. You don't need it here: the worktree keeps you isolated.

---

## Sources

- Lab 6 design doc (facilitator-tier, not on this branch)
- [`docs/lab-6/five-abstraction-rubric.md`](../../docs/lab-6/five-abstraction-rubric.md) — 5-abstraction reference matrix (participant-facing)
- [`docs/lab-6/backend-test-patterns.md`](../../docs/lab-6/backend-test-patterns.md) — backend test-pattern reference (study for structure)
- Lab 5 multi-step workflow and debugging loop (prerequisite)
- Lab 3 CLAUDE.md and context patterns (prerequisite)

**Date:** 2026-07-13
