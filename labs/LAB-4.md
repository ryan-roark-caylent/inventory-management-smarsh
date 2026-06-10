# Lab 4 — Verify at Scale (Skills + Subagent Reviewers)

**Module 04 · Verifying · 20 minutes · Solo** (one person, one machine, one session)

**What you're proving:** the human's job is specification and verification; skills and subagents let you enforce a standard you wrote once, every time, without granting write access to the checker.

---

## Step 0 (pre-clock) — Get on the lab branch

Run these two commands in a terminal at the repo root before the timer starts. Type them yourself — this controls the environment Claude runs in.

If you have leftover changes from a prior lab, run `/reset-branch` in Claude Code first, then run the two commands below.

```
git fetch origin
```

```
git checkout -b lab-4-work origin/lab-4-start
```

Claude Code should be running at the repo root.

---

## Step 1 (0:00–3:00) — Find the gap

Paste into Claude Code:

```
Run the backend test suite and tell me exactly how many tests passed.
```

**Observe:** Claude runs the repo-root pytest command and reports **40 passed**. You did not tell it which command — the project docs and the backend-api-test skill carry the how. That is the teaching point of routing the run through Claude.

Now open `tests/README.md`. It claims **51 tests total** and lists `tests/backend/test_orders.py` (15 tests). Look in `tests/backend/`: the file is not there. The docs describe a suite that does not exist.

**Write down in a scratch note:** documented test count vs actual test count.

**Self-check 1:** `[ ] skill loaded` ← watch for this in step 2.

---

## Step 2 (3:00–10:00) — Restore the missing tests, skill-driven

Paste into Claude Code:

```
tests/backend/test_orders.py is missing even though tests/README.md documents it. Restore it.
```

**Observe:** before Claude writes any code, the **backend-api-test skill loads**. Watch the transcript for the skill name appearing — you did not ask for the skill; the task matched its trigger ("writing or modifying tests in tests/backend"). Claude generates the file following the skill's conventions: a `TestOrdersEndpoints` class, the `client` fixture, case-insensitive string comparisons, a 404 test.

**If the skill does not auto-trigger,** use this fallback prompt instead:

```
Use the backend-api-test skill to restore tests/backend/test_orders.py.
```

Naming the skill forces the load. The lesson still lands; note in chat that triggers are description-matched, not guaranteed.

**Mark your self-check:** `[x] skill loaded`

**Read the diff before accepting — check these four things:**

1. Every test targets `/api/orders` or `/api/orders/{id}`, endpoints that exist in `server/main.py`.
2. Filter values are real data values: warehouses San Francisco / London / Tokyo; categories from Circuit Boards, Sensors, Power Supplies, Actuators, Controllers. A made-up category would pass against an empty list and test nothing.
3. There is a 404 test asserting `"not found"` in the error detail.
4. No test writes or mutates data; orders endpoints are read-only.

Accept once those hold. If Claude generates fewer than 15 tests, 11 or more is still enough to reach the done criterion — accept and move on.

---

## Step 3 (10:00–13:00) — Run the suite green

Paste into Claude Code:

```
Run the backend test suite again and report the result.
```

**Observe:** 51 or more passed, 0 failed (target: `55 passed`). If anything fails, paste the failure output back into Claude Code:

```
These tests fail. Fix the tests to match the actual API behavior, do not change server code: <paste the pytest failure output>
```

The "do not change server code" clause matters: the tests are the thing under construction; the API is the source of truth here.

---

## Step 4 (13:00–17:00) — Dispatch the reviewer — THE POINT

First, open the root `CLAUDE.md` and read Common Issues rule 1: "Use unique keys in v-for (not `index`)". The project wrote this rule down.

Now paste into Claude Code:

```
Use the code-reviewer agent to review client/src/views/Reports.vue.
```

**Observe:** Claude dispatches the **code-reviewer subagent** (watch the Task tool call in the transcript). The agent uses read-only tools (Read, Grep, Glob) — it has no ability to edit anything. It comes back with findings.

The guaranteed finding: **index used as the v-for `:key` in Reports.vue**, a direct violation of the CLAUDE.md rule you read 60 seconds ago. That is your second self-check.

**If the reviewer returns findings but not the index-key one,** re-prompt:

```
Use the code-reviewer agent to review the v-for key usage in client/src/views/Reports.vue against the root CLAUDE.md Common Issues list.
```

**Mark your self-check:** `[x] reviewer found the index-key violation`

The reviewer may list other observations. Act on only the index-key finding inside this lab.

---

## Step 5 (17:00–20:00) — Fix it and confirm the reviewer clears

Paste into Claude Code:

```
Fix only the v-for index-key violations the reviewer found in Reports.vue (lines 28, 51, 82). Use unique data fields as keys. Make no other changes.
```

**Observe:** Claude may delegate this to the **vue-expert** agent, because root CLAUDE.md mandates it for `.vue` changes. Either path (delegation or direct edit) is fine; if it delegates, you watched a CLAUDE.md rule route work to a scoped subagent.

**Read the diff before accepting — expect exactly these three attribute changes in `client/src/views/Reports.vue`:**

- Line 28: `:key="index"` → `:key="q.quarter"`
- Line 51: `:key="index"` → `:key="month.month"`
- Line 82: `:key="index"` → `:key="month.month"`

Anything beyond those three attributes (restructured template, renamed variables, removed `index` where other lines still use it) should be rejected: press Esc and re-prompt with the step 5 prompt verbatim. Accept the minimal diff.

Re-run the reviewer to confirm the fix:

```
Use the code-reviewer agent to review client/src/views/Reports.vue again. Confirm the v-for key issue is resolved.
```

**Observe:** the reviewer reports the key issue cleared.

Optional if time remains: ask Claude to commit locally. Read the message. Never push.

---

## Done Criteria

Self-verifiable in 10 seconds:

1. **Claude's test run shows a green pytest summary of 51 or more passed, 0 failed** (target: `55 passed`), and `tests/backend/test_orders.py` exists in the file tree.
   **Optional chat signal: paste the one-line pytest summary into the meeting chat.**

2. **Reports.vue has no `:key="index"` left**: the reviewer's second-pass output says the issue is resolved, or `git diff main -- client/src/views/Reports.vue` shows exactly three `:key` changes.

3. Both self-checks confirmed: `[x] skill loaded` and `[x] reviewer found the index-key violation`.

---

## Stuck? Self-serve these first

| What went wrong | Try this |
|---|---|
| Claude's test run errors (uv missing, env broken) | Post in meeting chat. TA will help check `uv --version`; if uv is absent, pre-workshop homework was skipped. |
| Skill does not auto-trigger in step 2 | Re-prompt with the named-skill fallback in step 2 above. |
| Claude writes far fewer tests than expected | Accept anything 11 or more. 40 prior + 11 new already clears the done criterion. |
| Generated tests fail and iteration burns past minute 12 | Post in meeting chat — the TA will send a rescue command. Move to step 4 once you have a green run. |
| Reviewer returns findings but not the index-key one | Re-prompt with the CLAUDE.md Common Issues fallback in step 4 above. |
| Step 5 fix balloons (vue-expert refactors the template) | Press Esc to interrupt. Re-prompt with the step 5 prompt verbatim — it contains "Make no other changes." |
| Total loss / out of time | Post in meeting chat — the TA will post the recovery sequence. |

---

## Extra Credit 1 — Wire a PostToolUse test hook

**Wire a PostToolUse hook that auto-runs the backend tests whenever Claude edits a Python file under `server/`.** This is hooks made concrete: the harness, not the model, enforces the check.

1. Create `.claude/settings.local.json` at the repo root with exactly this content (the hook script ships in the repo at `.claude/hooks/run_backend_tests.py`):

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "uv run --project server python .claude/hooks/run_backend_tests.py"
          }
        ]
      }
    ]
  }
}
```

2. Exit Claude Code and relaunch it at the repo root. Then run `/hooks` and confirm the PostToolUse entry is listed.

3. Trigger it with a change that breaks a test on purpose. Paste:

```
In server/main.py, change the 404 error message for a missing order from "Order not found" to "Order missing".
```

4. **Observe:** after the edit, the hook fires, the suite runs, and the restored 404 test fails because it asserts "not found" in the detail. The hook exits non-zero and feeds the failing output back to Claude, which sees the regression and corrects course without you pasting anything. That is the loop closing by itself.

5. Let Claude revert the message (or ask it to), and confirm the hook passes on the next edit.

6. **REMOVAL STEP — do not skip.** Delete the `hooks` block from `.claude/settings.local.json` (or delete the file). **Settings persist across branches; remove the hook before Lab 5 — it re-runs the suite on every `server/*.py` edit and will slow you down.**

Cross-platform note: the hook command invokes `uv` and Python only. No bash, no jq. It works as-is on Windows, macOS, and Linux.

---

## Extra Credit 2 — Reviewer on your own tests

Dispatch the reviewer at the file the skill just generated:

```
Use the code-reviewer agent to review tests/backend/test_orders.py.
```

Nothing is planted in the generated file. The frame is: see what an LLM-as-judge says about machine-written tests. **A clean bill is an acceptable outcome** — worth noticing — and so is a real finding (a weak assertion, duplicated setup, a tautological check). Read the findings, decide which ones you would act on, and act on at most one. The point is calibrating how much you trust a cheap reviewer over generated code, not polishing the file.
