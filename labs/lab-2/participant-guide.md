# Lab 2: Claude as a Thinking Partner — From Vague Ticket to Sharp Spec

**Track:** Foundations (Track 1) | **Position:** Lab 2 of 9 | **Depends on:** Lab 1

---

## What you will build

By the end of this lab you will have a committed technical spec for a low-stock alerting feature, grounded in the real inventory model, with a risk list, Jira-ready sub-tasks, and a recorded design decision you can defend. All of it authored through Claude, none of it handed to you.

---

## The point of this lab

Claude earns its keep as a thinking partner only when you make it argue with you. Ask "is this good?" and you get agreement. Ask for two weaknesses, a failure mode, and two alternatives, and you get the kind of thinking that used to happen in your head on a good day. The quality of the output is a function of the question, not the model. That is the flip this lab is designed to show you.

**Point step:** Step 2 (Move 2). When Claude critiques its own spec, the output quality jumps. Watch for it.

---

## Before you start

This is a thinking-and-writing lab, not an implementation lab. You will write a spec; you will not write code. No app servers and no browser are needed for the core path.

**Windows:** This lab runs entirely in the Claude Code terminal UI. No `--browser msedge` flag, no `settings.json` changes, no relaunch required. Run every git command as a separate line, never joined.

**macOS:** Same, run in the terminal. Claude Code opens your default browser automatically if needed. All git commands work the same in bash or zsh.

---

## Core path (Steps 0-6)

### Step 0: Branch and orient

1. In a terminal at the repo root, run these as two separate commands:
   ```
   git fetch origin
   git checkout -b lab-2-work origin/lab-2-start
   ```
   The fetch is not optional. The lab branches were pushed at repo freeze, after your homework clone.

2. Open `docs/lab-2/ticket-AEP-142.md` and read it. It is deliberately vague. That vagueness is the raw material.

3. Start Claude Code (`claude`). Ask Claude to show you the `InventoryItem` model and the `/api/inventory` and `/api/dashboard/summary` handlers so you know the real fields the feature will touch.

   **You know this worked when:** Claude shows an `InventoryItem` with these fields:
   ```python
   class InventoryItem(BaseModel):
       id: str
       sku: str
       name: str
       category: str
       warehouse: str
       quantity_on_hand: int
       reorder_point: int
       unit_cost: float
       location: str
       last_updated: str
   ```
   It should also point out that `/api/dashboard/summary` already returns a crude `low_stock_items` count. If you see invented field names like `stock_level` or `min_threshold`, you are on the wrong branch. Run `git fetch origin` and re-checkout.

---

### Step 1: Move 1 — Spec from the ticket

Ask Claude to turn `ticket-AEP-142.md` into a technical spec. Your prompt should ground it in this repo's actual inventory model and existing endpoints, not a generic e-commerce example. Have Claude write the draft to `specs/low-stock-alerting.md`.

**You know this worked when:** the spec names real fields (`quantity_on_hand`, `reorder_point`, the five real categories) rather than invented ones, and proposes a read-side endpoint that fits the existing GET-only API shape.

---

### Step 2: Move 2 — Make it argue (POINT STEP)

1. First, ask the weak question: **"Is this spec good?"** Read the answer. The model will mostly agree with itself. You will likely see something like:

   > "Overall this is a solid, production-ready spec. It covers the endpoint, the data model, and the UI surface. A few minor polish items aside, it looks good to implement."

2. Now ask the sharp question. Ask Claude to identify at least **two weaknesses**, **one likely failure mode** (think about what happens with a category that has no configured threshold, or what happens to alerts when the in-memory snapshot is stale), and **two alternative designs with tradeoffs**. Do not ask "is this good?" again.

   **You know this worked when:** the second response is materially longer and names concrete failure conditions, not restated praise. You should see something like:

   > "Two weaknesses: (1) the in-memory inventory is loaded once at process start from a static JSON file, so any real-world stock movement would not update alerts until the service restarts; (2) the spec doesn't say who owns default thresholds when a category has none configured — if a category key is missing, the alert check silently produces nothing. Likely failure mode: a category string with no matching threshold key returns zero alerts for that category, giving ops a false sense of safety. Alternative A: compute alerts on write (event-driven) — fewer stale-read risks, requires write endpoints that don't exist yet. Alternative B: a separate thresholds config resource — cleaner ownership, one more endpoint to maintain..."

   That contrast is the point of the lab. The model did not change. The question did.

3. Add a `## Risks` heading to the spec. Record **one risk Claude surfaced that you had not considered** and **one point where you disagreed with Claude and overrode it** (state why).

---

### Step 3: Move 3 — Sub-task drafting

Ask Claude to draft Jira-ready sub-tasks from the spec and the risk list. Each sub-task should have a one-line acceptance check. Have Claude write them to `docs/lab-2/subtasks.md`.

**You know this worked when:** you get discrete tasks (threshold config storage, a new endpoint, surfacing alerts on the view, test coverage) rather than one "build the feature" blob.

---

### Step 4: Move 4 — Bare vs context-rich

1. In a fresh prompt, paste only the bare ticket **title** and ask for a spec. Note how generic the output is.

2. Now paste the title **plus** the contents of `docs/lab-2/system-context.md` (the stack, the shared-items-API note, and the spec-template pointer) and ask again. Add this instruction at the end: **"If the shared-items-API impact is ambiguous, ask me a clarifying question before you draft."**

3. Diff the two responses.

   **You know this worked when:** the context-rich run surfaces the shared-items-API backward-compat concern in a way the bare run did not. It will appear as either an up-front clarifying question before drafting or as a flagged open decision inside the spec. For example:

   > "Before I draft: the items API is shared with two other services. Should low-stock alerting add fields to the existing `/api/inventory` response (risking backward-compat breakage for those consumers) or live behind a new endpoint? That choice changes the whole design."

   Record how the concern surfaced in your notes. The bare run will not raise this.

---

### Step 5: Move 5 — Plan Mode as disposable exploration

1. Enter Plan Mode and ask Claude to propose an implementation plan for the feature, touching the Vue view (`client/src/views/Inventory.vue`) and the FastAPI model/endpoint. Review the plan.

2. **Do NOT implement.** Exit Plan Mode without approving. Implementation is Lab 4.

   **You know this worked when:** after Plan Mode, `git status` shows no `.py` or `.vue` files modified:
   ```
   On branch lab-2-work
   Untracked files:
     (use "git add <file>..." to include in what will be committed)
           docs/lab-2/subtasks.md
           specs/low-stock-alerting.md
   ```
   Only your untracked spec and sub-task files appear. Plan Mode proposed a plan; it did not edit any files. The plan was disposable. The spec on disk is the durable artifact.

---

### Step 6: Decide and commit

1. Decide where per-category thresholds are **stored and configured**. Options include: a new config endpoint with an in-memory dict, a hardcoded default in the handler, a `server/data/` JSON file, or an env-driven default. Any defensible choice is valid.

   Write your choice and a one-sentence defense into the spec under `## Threshold configuration`. "It felt right" is not a defense.

2. Commit the spec and sub-tasks:
   ```
   git add specs/low-stock-alerting.md docs/lab-2/subtasks.md
   git commit -m "spec: low-stock alerting with per-category thresholds"
   ```

   **You know this worked when:** `git log --oneline -1` shows your commit and `git show --stat HEAD` lists the two files:
   ```
    docs/lab-2/subtasks.md       | 24 ++++++++++++
    specs/low-stock-alerting.md  | 61 +++++++++++++++++++++++++++++
    2 files changed, 85 insertions(+)
   ```
   (Line counts in your actual output will vary. What matters is that both files are in the commit.)

---

## Done criteria

Check all five before you call it done:

1. `specs/low-stock-alerting.md` is committed and names real repo fields (`quantity_on_hand`, `reorder_point`, the five actual categories).
2. The spec contains a `## Risks` section with one risk Claude surfaced that you had not considered, and one recorded override with your rationale.
3. `docs/lab-2/subtasks.md` exists with discrete, Jira-ready sub-tasks (not a blob).
4. You recorded how the context-rich run (Move 4) surfaced the shared-items-API backward-compat concern, as either an up-front clarifying question or a flagged open decision in the spec.
5. After Plan Mode (Move 5), `git status` showed no `.py` or `.vue` files, proving the plan was disposable.

**Share-back artifact:** your committed `specs/low-stock-alerting.md` (spec + risk list + threshold-config decision) and `docs/lab-2/subtasks.md` on your branch. The person-specific signal is the surfaced risk, the override, and the threshold-config decision you defended.

---

## Extra credit

Extra credit is optional and does not affect Quiz 1 or done criteria.

1. **Feed a constraint Claude could not know.** Tell Claude: "Low-stock alerts must not fire during scheduled reorder windows, and every alert must be reconstructable for a compliance audit." Iterate the **spec**, not the prompt. Note how the design changes (audit log, window suppression). Record it under `## Constraints`.

2. **Surface comparison (Lab 1 callback).** Run Move 1 in Claude.ai in a browser and compare the thinking-partner dialogue to Claude Code. Note one thing each surface did better.

   **Windows:** launch the browser from the CLI with `claude --browser msedge`.

   **macOS:** no `--browser` flag is needed. Claude Code opens your default browser automatically.

3. **Manual-vs-AI timing.** Before you started, estimate how long this spec would have taken you by hand. Compare to the wall-clock time you spent. Post the delta, one thing Claude got right, and one you had to correct in the async peer debrief.

---

## If you get stuck

**The spec uses invented field names (not real repo fields).**
Ask Claude to read the server code before rewriting the spec, and confirm you are looking at the actual `InventoryItem` model and existing endpoint shapes. If the output still drifts, check out the reference branch to see a finished example:
```
git stash -u
git checkout lab-2-solution
```
Open `specs/low-stock-alerting.md` and `docs/lab-2/reference-risks.md`. You now have a complete, sharp spec on your screen. Return to your work:
```
git checkout lab-2-work
git stash pop
```

**The critique response still just agrees with itself.**
Remove any "is this good?" phrasing from your prompt. Ask specifically for weaknesses, a failure mode tied to how this backend actually works, and alternatives with tradeoffs. If the output still hedges, check out `lab-2-solution` and read `docs/lab-2/reference-risks.md` to see the shape of what a sharp critique should look like, then return to your branch.

**You ran out of time or hit a wall.**
Check out the reference and read the finished spec so you leave having seen the target:
```
git stash -u
git checkout lab-2-solution
```
Open `specs/low-stock-alerting.md`, `docs/lab-2/reference-risks.md`, and `docs/lab-2/reference-plan.md`. Return when ready:
```
git checkout lab-2-work
git stash pop
```

**`fatal: 'origin/lab-2-start' is not a valid object name`**
You skipped the `git fetch origin` step. Run it first, then re-checkout.

---

## Quizzes

Your completion and mastery quizzes are in the LMS.

---

## Sources

- [20-lab-2-design.md](../../lab-build/20-lab-2-design.md) — authoritative post-amendment design, Sections 2-5, 7, 9.

**Date generated:** 2026-07-11
