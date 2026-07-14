# Lab 2: Claude as a Thinking Partner — From Vague Ticket to Sharp Spec

**Track:** Foundations (Track 1) | **Position:** Lab 2 of 9 | **Depends on:** Lab 1

---

## What you will build

By the end of this lab you will have a technical spec for a low-stock alerting feature, grounded in the real inventory model, with a risk list, Jira-ready sub-tasks, and a design decision you resolved and can defend. You keep it as a local artifact in your worktree. All of it authored through Claude, none of it handed to you.

---

## The point of this lab

Claude earns its keep as a thinking partner only when you make it argue with you. Ask "is this good?" and you get agreement. Ask for two weaknesses, a failure mode, and two alternatives, and you get the kind of thinking that used to happen in your head on a good day. The quality of the output is a function of the question, not the model. That is the flip this lab is designed to show you.

**Point step:** Step 2. When Claude critiques its own spec, the output quality jumps. Watch for it.

---

## Before you start

This is a thinking-and-writing lab, not an implementation lab. You will write a spec; you will not write code. Implementation is Lab 4.

**Surface note (Lab 1 callback):** In Lab 1 you chose a surface per task. This thinking-partner workflow runs in Claude Code so the spec lands on disk and you can use Plan Mode. No app servers and no browser are needed.

**Windows + macOS (identical guidance):** This lab runs entirely in the Claude Code terminal. No `--browser` flag, no `settings.json` changes, no relaunch. Run each git command on its own line, never joined with `&&`. The only genuinely OS-specific line is the `--browser msedge` flag in extra credit, kept split there.

---

## Core path (Steps 0-6)

### Step 0: Set up your worktree

You work this lab inside its own git **worktree** so nothing collides with other labs and you keep your work at the end. If your pre-work already created `lab-2-work`, confirm you're in it with `git worktree list`. If not, create it now — run each line separately:

```
git fetch origin
git worktree add ../lab-2-work lab-2-start
cd ../lab-2-work
```

> **Tip:** you can run a shell command without leaving Claude Code by prefixing it with `!` (e.g. `!git worktree list`). Handy throughout the labs.

Then launch Claude Code from inside `lab-2-work`. (The worktree rule is also in this repo's `CLAUDE.md`.)

1. Quick check: run `/model` and confirm you are on **sonnet**. Smarsh Enterprise defaults to Haiku; this lab is tuned for Sonnet. Switch with `/model sonnet` if needed.

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
   It should also point out that `/api/dashboard/summary` already returns a crude `low_stock_items` count. If you see invented field names like `stock_level` or `min_threshold`, you are on the wrong branch.

---

### Step 1: Spec from the ticket

1. Ask Claude to turn `ticket-AEP-142.md` into a technical spec. Your prompt should ground it in this repo's actual inventory model and existing endpoints, not a generic e-commerce example, and follow `specs/spec-template.md`. Have Claude write the draft to `specs/low-stock-alerting.md`.

2. In the same prompt, tell Claude that where the ticket leaves a real design choice open, it must **flag it in a clearly-marked `## Decisions needed from you` section** rather than silently picking for you. You will resolve those in Step 6.

   **You know this worked when:** the spec names real fields (`quantity_on_hand`, `reorder_point`, the five real categories) rather than invented ones, proposes a read-side endpoint that fits the existing GET-only API shape, and carries a `## Decisions needed from you` section listing at least the where-do-per-category-thresholds-live question (and likely: the default when a category has no threshold, and whether to add a new endpoint or extend `/api/inventory`).

---

### Step 2: Make it argue (POINT STEP)

1. First, deliberately ask the weak question: **"Is this spec good?"** Read the answer. The model will mostly agree with itself. You will likely see something like:

   > "Overall this is a solid, production-ready spec. It covers the endpoint, the data model, and the UI surface. A few minor polish items aside, it looks good to implement."

   **Rewind before you sharpen:** you do not want that weak Q/A sitting in context when you ask the real question. Press **Esc twice** (or run **`/rewind`**) to open the rewind menu and roll the session back to just before the weak question. Then ask the sharp one into a clean context. This is context hygiene at the exact moment it pays off. A bad prompt and its answer do not have to pollute everything that follows.

2. Now ask the sharp question. Ask Claude to identify at least **two weaknesses**, **one likely failure mode** (think about a category with no configured threshold, or a stale in-memory snapshot), and **two alternative designs with tradeoffs**. Do not ask "is this good?" again.

   **You know this worked when:** the second response is materially longer and names concrete failure conditions, not restated praise. You should see it open with something like:

   > "Two weaknesses: (1) the in-memory inventory is loaded once at process start, so alerts reflect stale data until the service restarts; (2) ..."

   That contrast is the point of the lab. The model did not change. The question did.

3. Add a `## Risks` heading to the spec. Record **one risk Claude surfaced that you had not considered** and **one point where you overrode Claude** (rejected a suggestion, and why). This is a real before/after your completion quiz keys on, so write it down.

---

### Step 3: Sub-task drafting

Ask Claude to draft Jira-ready sub-tasks from the spec and the risk list. Each sub-task should have a one-line acceptance check. Have Claude write them to `docs/lab-2/subtasks.md`.

**You know this worked when:** you get discrete tasks (threshold config, endpoint, view surfacing, tests) rather than one "build the feature" blob.

---

### Step 4: Bare vs context-rich

1. In a fresh prompt, paste **just the TITLE line of `ticket-AEP-142.md`** — the same ticket you have worked all lab — with **none of its body**, and ask for a spec. This is the "bare" run: title only, zero context.

2. Now paste that **same title plus** the contents of `docs/lab-2/system-context.md` (the stack, the shared-items-API note, the spec-template pointer) and ask again. Append: **"If the shared-items-API impact is ambiguous, ask me a clarifying question before you draft."**

3. Diff the two responses.

   **You know this worked when:** the context-rich run surfaces the shared-items-API backward-compat concern the bare run missed, either as an up-front clarifying question or as a flagged open decision in the spec. For example:

   > "Before I draft: the items API is shared with two other services. Should low-stock alerting add fields to the existing `/api/inventory` response (risking backward-compat breakage for those consumers) or live behind a new endpoint?"

   Note how the concern surfaced. The bare run will not raise this.

   **The point:** bare title vs title+context, same ticket, same model. The only variable is what you fed it. That gap is why context is the lever.

---

### Step 5: Plan Mode as disposable exploration

1. Enter Plan Mode and ask Claude to propose an implementation plan for the feature, touching the Vue view (`client/src/views/Inventory.vue`) and the FastAPI model/endpoint. Review the plan.

   **How to use Plan Mode:** press **`shift-tab`** to cycle Claude Code into Plan Mode (you will see the mode indicator change); press **`shift-tab`** again to cycle back out. In Plan Mode Claude proposes but writes nothing until you approve.

2. **Do NOT implement.** Exit Plan Mode without approving. Implementation is Lab 4.

   **You know this worked when:** after Plan Mode, `git status` shows no `.py` or `.vue` files:
   ```
   On branch lab-2-work
   Untracked files:
     (use "git add <file>..." to include in what will be committed)
           docs/lab-2/subtasks.md
           specs/low-stock-alerting.md
   ```
   Only your untracked spec and sub-task files appear. Plan Mode proposed a plan; it did not edit any files. The plan was disposable. The spec on disk is the durable artifact.

---

### Step 6: Resolve the open decisions

1. Open the `## Decisions needed from you` section your spec surfaced back in Step 1. These are the calls Claude correctly refused to make for you. **Resolve the threshold-config one:** decide where per-category thresholds are **stored and configured** — a new config endpoint with an in-memory dict, a hardcoded per-category default, a `server/data/` JSON file, an env-driven default, or another defensible option. Write your choice and a one-sentence defense directly under that decision. "It felt right" is not a defense.

   This is your call because the spec surfaced it as an open decision. That is the skill: a good spec tells you where a human still has to choose.

2. **Keep your work (no commit):** your `specs/low-stock-alerting.md` (spec + risks + resolved decision) and `docs/lab-2/subtasks.md` are your personal takeaway. Keep them in your worktree. **Do not commit or push** — nothing in this lab goes back to the repo.

   **You know this worked when:** the threshold decision under `## Decisions needed from you` has a choice plus a one-sentence defense, and both files exist in your worktree:
   ```
   On branch lab-2-work
   Untracked files:
           docs/lab-2/subtasks.md
           specs/low-stock-alerting.md
   ```
   (Untracked is fine. That uncommitted local artifact is the intended end state.)

---

## Done criteria

Check all five before you call it done:

1. `specs/low-stock-alerting.md` exists locally and names real repo fields (`quantity_on_hand`, `reorder_point`, the five actual categories).
2. The spec contains a `## Risks` section with one risk Claude surfaced that you had not considered, and one recorded override with your rationale.
3. `docs/lab-2/subtasks.md` exists with discrete, Jira-ready sub-tasks (not a blob).
4. You noted how the context-rich run (Step 4) surfaced the shared-items-API backward-compat concern, as either an up-front clarifying question or a flagged open decision in the spec.
5. After Plan Mode (Step 5), `git status` showed no `.py` or `.vue` files, and your `## Decisions needed from you` section carries your resolved threshold choice plus a one-sentence defense.

**Share-back artifact:** your local `specs/low-stock-alerting.md` (spec + risk list + resolved decision) and `docs/lab-2/subtasks.md` in your worktree, uncommitted. The person-specific signal is the surfaced risk, the override, and the threshold-config decision you defended.

---

## Extra credit

Extra credit is optional and does not affect Quiz 1 or done criteria.

1. **Feed a constraint Claude could not know.** Tell Claude: "Low-stock alerts must not fire during scheduled reorder windows, and every alert must be reconstructable for a compliance audit." Iterate the **spec**, not the prompt. Note how the design changes (audit log, window suppression). Record it under `## Constraints`.

2. **Surface comparison (Lab 1 callback).** Run the Step 1 spec draft in Claude.ai in a browser and compare the thinking-partner dialogue to Claude Code. Note one thing each surface did better.

   **Windows:** launch the browser from the CLI with `claude --browser msedge`.

   **macOS:** no `--browser` flag is needed. Claude Code opens your default browser automatically.

3. **Manual-vs-AI timing.** Before you started, estimate how long this spec would have taken you by hand. Compare to the wall-clock time you spent. Post the delta, one thing Claude got right, and one you had to correct in the async peer debrief.

---

## If you get stuck

**The spec uses invented field names (not real repo fields).**
Ask Claude to read the server code before rewriting the spec, and confirm you are looking at the actual `InventoryItem` model and existing endpoint shapes. If the output still drifts, open the solution in a second worktree to see a finished example. First confirm your remote points at the fork:
```
git remote -v
```
You should see `ryan-roark-caylent/inventory-management-smarsh`. Then open the solution alongside your work:
```
git worktree add ../lab-2-solution lab-2-solution
```
Open `specs/low-stock-alerting.md` and `docs/lab-2/reference-risks.md` in that worktree. You now have a complete, sharp spec on your screen without disturbing your own work.

**The critique response still just agrees with itself.**
Remove any "is this good?" phrasing from your prompt, and make sure you rewound the weak exchange (Esc twice or `/rewind`) so the agreeable answer is not anchoring the model. Ask specifically for weaknesses, a failure mode tied to how this backend actually works, and alternatives with tradeoffs. If it still hedges, open `docs/lab-2/reference-risks.md` in the solution worktree to see the shape of a sharp critique.

**You ran out of time or hit a wall.**
Open the solution in a second worktree and read the finished spec so you leave having seen the target:
```
git remote -v
git worktree add ../lab-2-solution lab-2-solution
```
Open `specs/low-stock-alerting.md`, `docs/lab-2/reference-risks.md`, and `docs/lab-2/reference-plan.md` there.

---

## Quizzes

Your completion and mastery quizzes are in the LMS pre-work module.

---

## Sources

- Lab 2 pre-work module in the LMS (MindTickle) — thinking-partner workflow, critique-not-approval, context richness.
