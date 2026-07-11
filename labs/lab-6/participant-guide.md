# Lab 6: Claude Skills — Build It, Trigger It, Automate Around It

**What you'll have when you're done:** a skill you named and built from scratch that fires on plain-English requests without you typing `/name`, a PostToolUse hook that runs your backend test suite automatically after every edit, and a written rubric decision committing your own weekly workflow to one of the five Claude Code customization abstractions.

**Track:** 2 (Vibecode). Builds on Lab 3 (CLAUDE.md / context) and Lab 5 (multi-step workflows + debugging loop).

**Your completion and mastery quizzes are in the LMS.**

---

## Before you start

- Fork: `ryan-roark-caylent/inventory-management-smarsh`
- Starting branch: `lab-6-start`
- You need `uv` on PATH (used by the backend test runner and hook script)

---

## Core path (Steps 0–7)

### Step 0 — Setup

Fetch and check out the starting branch, then start the servers:

```
git fetch origin
git checkout -b lab-6-work origin/lab-6-start
```

**Windows:**
```
scripts\start.ps1
```

**Mac:**
```
scripts/start.sh
```

Alternatively, ask Claude to run the `/start` skill.

Open a **fresh** Claude Code session after checkout so it loads this branch's `CLAUDE.md`.

**You know it worked when:** the app loads at `http://localhost:3000` and running the backend tests manually reports all passing:

```
uv run --project server pytest tests/backend/ -q
```

---

### Step 1 — Name your skill (open-ended)

The skill you're building automates this workflow: generate pytest tests for a FastAPI endpoint.

**You decide the name.** Call it whatever you would call it if you were adding it to your own team's repo — not necessarily `gen-tests`. Write one sentence defending your choice.

**Success signal:** a new file exists at `.claude/skills/<your-name>/SKILL.md`.

---

### Step 2 — Author with a deliberately thin description

Give your skill a body that does the work, but write the `description:` frontmatter as a bare title: one short phrase that names the skill but doesn't describe when to use it or provide example trigger phrases.

> **Windows:** relaunch Claude Code after saving `SKILL.md`. Skill name and description metadata load at session start — the skill is not active until you relaunch.

> **Mac:** same — quit and relaunch Claude Code (`claude` in a new terminal tab) after saving `SKILL.md`. Skill metadata is not hot-reloaded mid-session on any platform.

After relaunching, ask Claude, in plain English, to do exactly the task the skill covers. Do not type `/<your-name>`.

**Success signal (the designed failure):** Claude answers your request directly and does not invoke your skill. You will not see your skill's name in the transcript. This is expected.

Expected transcript shape:
```
> [your natural-language request about the task]
I'll write tests for the endpoint. Here's a test file...
(no skill invocation appears)
```

---

### Step 3 — Tune the description until it fires (point step)

Ask Claude to rewrite the `description:` as a routing signal: what the skill does, plus at least five example phrasings a teammate might type to invoke it. Save the file.

> **Windows:** relaunch Claude Code after each description save. The updated description is not active until the next session start. The loop is: rewrite → save → relaunch → test.

> **Mac:** same — quit and relaunch Claude Code after each description save. The rewrite → save → relaunch → test loop applies on all platforms.

After relaunching, re-issue the same plain-English request from Step 2. If the skill still doesn't fire, add more trigger phrasings and synonyms, save, relaunch, and retry.

**Record how many rewrite-relaunch-test cycles it took.** The number depends on the live model — do not assume it will be one.

**Success signal:** Claude invokes your skill from natural language, with no `/<your-name>`. You see the skill name in the transcript.

Expected transcript shape:
```
> [your natural-language request about the task]
Skill: <your-name>
Reading tests/backend/ conventions and the target endpoint...
```

---

### Step 4 — Run it explicitly and read the output

Invoke `/<your-name>` directly against a real endpoint in the repo (for example, the `/api/orders` endpoint).

**Success signal:** the skill produces a runnable Python test file grounded in real repo content. It should use the shared `client` fixture from `tests/backend/conftest.py` and mirror the class-based structure in the existing test files.

Example of what a well-grounded output looks like:
```python
# tests/backend/test_orders.py
import pytest


class TestOrdersEndpoints:
    """Test suite for order-related endpoints."""

    def test_get_orders_returns_200(self, client):
        response = client.get("/api/orders")
        assert response.status_code == 200

    def test_get_orders_returns_list(self, client):
        response = client.get("/api/orders")
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
```

You do not need to run the generated file to pass this step. Reading it and confirming it is grounded in repo content is sufficient.

---

### Step 5 — Wire the auto-test hook and prove it

Ask Claude to author `.claude/settings.json` with a **PostToolUse** hook. The hook should use a matcher for Write and Edit operations, and it should run the test script that already ships on this branch at `.claude/hooks/run_backend_tests.py`. Failures should print to stderr.

> **Windows:** relaunch Claude Code after saving `.claude/settings.json`. Hooks are read at session start.

> **Mac:** same — quit and relaunch Claude Code after saving `.claude/settings.json`. Hooks are not hot-reloaded mid-session on any platform.

**Prove it works:** ask Claude to find why the low-stock comparison in `get_dashboard_summary` (`server/main.py`) might count fewer items than expected if the boundary condition changed (hint: look at the `<=` operator). Ask it to make that change.

Watch what happens before Claude's next turn.

**Success signal (the hook fires on the bad edit):** you see a pytest failure in stderr:
```
Backend tests failed after this edit:
FAILED tests/backend/test_dashboard.py::TestDashboardEndpoints::test_dashboard_low_stock_items_calculation
assert 4 == 5
```

Then ask Claude to revert the change.

**Success signal (after revert):** all backend tests pass:
```
tests/backend/... 36 passed
```

(The exact count may differ slightly; what matters is red on the bad edit and green after revert.)

---

### Step 6 — Apply the 5-abstraction rubric (open-ended)

Open the reference at `docs/lab-6/five-abstraction-rubric.md`.

Write a weekly workflow you actually do (one sentence). Apply the rubric and **commit to exactly one** of: CLAUDE.md / skill / hook / subagent / MCP. Write the deciding factor. For example: "must run automatically without being asked, and the logic belongs outside the context window" points to hook.

Save your decision and one-line justification to `rubric-decision.md` at the repo root.

**Success signal:** `rubric-decision.md` names one abstraction and states the deciding factor.

---

### Step 7 — Commit the share-back artifacts

Stage and commit the three files you built:

```
git add .claude/skills/<your-name>/SKILL.md .claude/settings.json rubric-decision.md
```

```
git commit -m "lab-6: skill + auto-test hook + rubric decision"
```

**Success signal:** run the following and confirm all three files appear in the listing:

```
git show --stat HEAD
```

---

## Done criteria

All three of these are observable on your own screen:

1. Your skill fires from a natural-language request — skill name is visible in the transcript (Step 3).
2. After the planted off-by-one, the hook surfaces a pytest failure in stderr; after revert, green (Step 5).
3. `git show --stat HEAD` lists all three committed artifacts (Step 7).

**Share-back:** the commit on your `lab-6-work` branch — `.claude/skills/<name>/SKILL.md`, `.claude/settings.json`, and `rubric-decision.md` in a single diff.

---

## Extra credit

Not required for any quiz or done-criteria. Use these if you finish early.

**EC-1 — Second skill, disambiguation.** Build one of two additional skills: `/inv-review` (flags FastAPI anti-patterns in a diff) or `/pr-desc` (drafts a PR description from `git diff --staged`). Test whether a natural-language request routes to the right skill, or whether the descriptions collide. Tighten the description of whichever skill loses.

**EC-2 — Scope the hook down.** The shipped hook runs the full suite on every server edit. Rewrite it (or the script) to run only the affected test file. Note the tradeoff you accepted (speed vs. missed cross-file regressions).

**EC-3 — Rubric round two.** Name a workflow that should be a **subagent** or **MCP**, not a skill, and defend why a skill is the wrong tool for it. This stretches the rubric past the CLAUDE.md-vs-skill case.

**EC-4 — Test a neighbor.** Hand your `SKILL.md` to a peer (or re-read it cold). Would the description trigger for someone who didn't write it? Revise for a cold reader.

---

## If you get stuck

**Skill won't implicit-trigger after several rewrites.**
Explicit invocation always works: type `/<your-name>` directly to continue the lab. To study a description that does trigger, check out the solution branch's skill and read its `description:` field:

```
git checkout origin/lab-6-solution -- .claude/skills/gen-tests/SKILL.md
```

Read the description. You still see the point: what's in the description is what does the routing. Then delete that file and keep building yours, or continue from the solution as your base.

**Hook doesn't fire.**

1. Relaunch Claude Code after saving `.claude/settings.json`. Hooks load at session start on all platforms (Windows and Mac).
2. Confirm the file is valid JSON. A trailing comma breaks it.
3. Confirm `uv` is on PATH: run `uv run --project server pytest tests/backend/ -q` by hand.
4. If still stuck, land the known-good config and relaunch:

   ```
   git checkout origin/lab-6-solution -- .claude/settings.json
   ```

**Pytest errors or can't tell red from green.**
Run the suite by hand:

```
uv run --project server pytest tests/backend/ -q
```

Your PostToolUse hook should surface a `test_dashboard_low_stock_items_calculation` failure in stderr once the planted change is active, and green once it is resolved. If you cannot tell red from green here, that is the signal your hook is not wired correctly yet, not that your fix is wrong.

**Full reset (last resort).**
Land every answer artifact and inspect it:

```
git checkout origin/lab-6-solution -- .claude/skills .claude/settings.json rubric-decision.md
```

You end up with a working skill, a wired hook, and a rubric decision. The point of the lab is there to read.

---

## Sources

- Lab 6 design doc (facilitator-tier, not on this branch)
- [`docs/lab-6/five-abstraction-rubric.md`](../../docs/lab-6/five-abstraction-rubric.md) — 5-abstraction reference matrix (participant-facing)
- Lab 5 multi-step workflow and debugging loop (prerequisite)
- Lab 3 CLAUDE.md and context patterns (prerequisite)

**Date:** 2026-07-11
