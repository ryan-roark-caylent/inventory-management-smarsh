# Lab 6 — Claude Skills: Build It, Trigger It, Automate Around It

By the end of this lab you will have built and committed three things: a skill that fires from natural language (no `/name` required), a PostToolUse hook that auto-runs the backend test suite after every edit, and a one-paragraph rubric decision that defends which of the five customization abstractions fits a workflow you actually do.

---

## Core path (Steps 0–7)

### Step 0 — Setup

```bash
git fetch origin
git checkout -b lab-6-work origin/lab-6-start
```

Start the servers using the `/start` skill, or run `scripts/start.ps1` (Windows) / `scripts/start.sh` (Mac). Open a fresh Claude Code session after checkout so it loads this branch's context.

**You know it worked when:** the app loads at `http://localhost:3000` and running `uv run --project server pytest tests/backend/ -q` from the repo root reports all tests passing.

---

### Step 1 — Name your skill (open-ended)

The workflow for this lab: generate pytest tests for a FastAPI endpoint. You build exactly this skill.

Choose the skill name yourself. It can be `gen-tests` or anything you would name it if you were adding it to your own team's repo. Write one sentence defending the name you picked.

Ask Claude to create the skill file at `.claude/skills/<your-name>/SKILL.md`.

**Success signal:** a new file exists at `.claude/skills/<your-name>/SKILL.md`.

---

### Step 2 — Author with a thin description

Give the skill a body that does the work. For the `description:` frontmatter, write a bare title — one short sentence, no example phrases.

> **Windows:** relaunch Claude Code after saving `SKILL.md`. Skill name and description metadata load at session start, so the skill is not active until you relaunch.

> **Mac:** same — quit and relaunch Claude Code (`claude` in a new terminal tab) after saving `SKILL.md`. Skill metadata is not hot-reloaded mid-session on any platform.

Then, in natural language, ask Claude to do exactly the task the skill covers without typing `/<your-name>`.

**Success signal (the designed failure):** Claude answers the request directly and does not load your skill. You will not see your skill's name invoked in the transcript. This is expected.

---

### Step 3 — Tune the description until it fires (point step)

Ask Claude to rewrite the `description:` as a routing signal: what the skill does plus several example phrasings a teammate might type. Save.

> **Windows:** relaunch Claude Code after each description save. The updated description is not active until the next session start. The loop is: rewrite → save → relaunch → test.

> **Mac:** same — quit and relaunch Claude Code after each description save.

Re-issue the same natural-language request. If it still does not fire, add more trigger phrasings and synonyms, save, relaunch, and retry.

Note how many rewrite-relaunch-test cycles it takes. The number varies by model and phrasing — do not assume it will be one.

**Success signal:** Claude invokes your skill from natural language, with no `/<your-name>`. You see the skill name in the transcript.

---

### Step 4 — Run it explicitly and read the output

Invoke `/<your-name>` directly against a real target (for example, the `/api/orders` endpoint).

**Success signal:** the skill produces a test file grounded in real repo content, using the `client` fixture and the class-based structure from `tests/backend/`.

---

### Step 5 — Wire the auto-test hook and prove it

Ask Claude to author `.claude/settings.json` with a **PostToolUse** hook, matcher `Write|Edit`, that runs the shipped test script and writes failures to stderr. The reference script `.claude/hooks/run_backend_tests.py` already exists on this branch — the hook wires it in.

> **Windows:** relaunch Claude Code after saving `.claude/settings.json` before testing the hook. Hooks are read at session start.

> **Mac:** same — quit and relaunch Claude Code after saving `.claude/settings.json`. Hooks are not hot-reloaded mid-session on any platform.

Prove it: ask Claude to change the low-stock comparison in `get_dashboard_summary` in `server/main.py` from `<=` to `<`. Watch the hook run pytest and surface a failure before Claude's next turn.

Then ask Claude to revert the change and confirm tests pass again.

**Success signal:** after the bad edit you see a pytest failure in stderr naming `test_dashboard_low_stock_items_calculation`; after the revert, all tests pass.

---

### Step 6 — Apply the five-abstraction rubric (open-ended)

Open `docs/lab-6/five-abstraction-rubric.md`. Write your named weekly workflow in one sentence.

Apply the rubric and commit to exactly one of: CLAUDE.md / skill / hook / subagent / MCP. Write the deciding factor (for example: "must run automatically without being asked" points to hook; "always-on for every teammate every turn" points to CLAUDE.md).

Save your decision and one-line justification to `rubric-decision.md` at the repo root.

**Success signal:** `rubric-decision.md` names one abstraction and states the deciding factor.

---

### Step 7 — Commit the share-back artifacts

```bash
git add .claude/skills/<name>/SKILL.md .claude/settings.json rubric-decision.md
git commit -m "lab-6: skill + auto-test hook + rubric decision"
```

**Success signal:** `git show --stat HEAD` lists all three files.

---

## Extra credit

Not required for the core path. Work through these if you finish early.

- **EC-1:** Build a second skill (`/inv-review` for FastAPI anti-patterns or `/pr-desc` for PR descriptions from `git diff --staged`). Test whether natural-language requests route to the right skill, or whether the descriptions collide. Tighten the losing description.
- **EC-2:** Rewrite the hook or the script to run only the affected test file rather than the full suite. Note the tradeoff you accepted.
- **EC-3:** Name a workflow that should be a **subagent** or **MCP**, not a skill, and defend why a skill is the wrong tool for it.
- **EC-4:** Hand your `SKILL.md` to a peer (or re-read it cold). Would the description trigger for someone who did not write it? Revise for a cold reader.

---

## If you get stuck

**Skill won't implicit-trigger after several rewrites.** Explicit invocation always works: type `/<your-name>` directly to run it and continue the lab. To see a description that does trigger, run:

```bash
git checkout lab-6-solution -- .claude/skills/gen-tests/SKILL.md
```

Read its `description:` field. You still experience the point: the description is what does the routing.

**Hook does not fire.**

> **Windows/Mac:** relaunch Claude Code after saving `.claude/settings.json` — hooks load at session start on all platforms.

Check that the file is valid JSON (a trailing comma breaks it). Confirm `uv` is on PATH by running `uv run --project server pytest tests/backend/ -q` manually. To land a known-good config:

```bash
git checkout lab-6-solution -- .claude/settings.json
```

Relaunch, then retry.

**Pytest errors or can't tell red from green.** Run the suite directly:

```bash
uv run --project server pytest tests/backend/ -q
```

On `lab-6-start` this run is RED (one `test_dashboard_low_stock_items_calculation` failure is expected — that is the defect your hook should catch). Once your fix is correct, the suite goes GREEN. If you get stuck on the fix itself, use the full reset below.

**Full reset (last resort).** Land every answer artifact:

```bash
git checkout lab-6-solution -- .claude/skills .claude/settings.json rubric-decision.md
```

---

## Quizzes

- Completion quiz: `lab-6-completion-quiz.md`
- Mastery quiz: `lab-6-mastery-quiz.md`

---

## Sources

Authored from scratch for lab-6-start. Guided-intent steps derived from the lab design (§3) and rescue blocks (§9). No solution prompts, answer keys, or rubric decisions are included.

**Date generated:** 2026-07-11
