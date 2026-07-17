# Lab 5: Multi-Step Workflows and Session Management (+ the Debugging Loop)

**Track 2 (Vibecode) · Position 5 of 9**

**Objective:** Plan a cross-cutting `supplier` field-add across the inventory-management stack, catch the cascade failure at a planned checkpoint, run the 4-step debugging loop to diagnose it, resolve it with a defended design decision, and demonstrate `/compact` and `/clear` discipline.

**Core path: ~50 min · Extra Credit: additional time as available**

Your completion and mastery quizzes are in the LMS (MindTickle). Pre-work (`/model sonnet`, node/npm, and the toolchain checks) is the MindTickle pre-work module — do it before lab day. You create the worktree in Step 0 below.

---

## Step 0: Set up your worktree and start the stack

You work this lab inside its own git **worktree** so nothing collides with other labs and you keep your work at the end. If your pre-work already created `lab-5-work`, confirm you're in it with `git worktree list`. If not, create it now — run each line separately:

> **Tip:** you can run a shell command without leaving Claude Code by prefixing it with `!` (e.g. `!git worktree list`). Handy throughout the labs.

```
git fetch origin
git worktree add -b lab-5-work ../lab-5-work lab-5-start
cd ../lab-5-work
```

Then launch Claude Code from inside `lab-5-work`. (The worktree rule is also in this repo's `CLAUDE.md`.)

- Quick check: run `/model` and confirm you're on **sonnet**. Smarsh Enterprise defaults to Haiku; this lab is tuned for Sonnet. Switch with `/model sonnet` if needed.
- Start the stack: ask Claude to start the app (it has a `/start` command), or run it yourself.
  - Fallback: `scripts/start.ps1` on Windows / `scripts/start.sh` on macOS. Node/npm must already be installed and the client dependencies pulled from pre-work — this lab runs the browser UI.
- Open the app in the browser and click into the Inventory view. Leave it open; you'll watch it change.

---

## Step 1: Have Claude render the dependency graph

Ask Claude to **map the layers the `supplier` field touches and render the dependency graph as a Mermaid (or ASCII) diagram** with "depends on" arrows. The layers:

1. The `InventoryItem` Pydantic model (`server/main.py`)
2. The `inventory.json` data source
3. The `GET /api/inventory` route
4. The `InventoryDetailModal.vue` display

Then do the part Claude can't do for you: **for each node, mark blast radius** — does a change here cascade to other nodes, and is it recoverable? Mark the ONE highest-value checkpoint and write one sentence defending where you put it.

> **Planning discipline:** you're mapping a dependency graph here, not asking Claude to propose an implementation plan for your approval — so you're not in Plan Mode (Labs 2 and 4). The discipline is the same: think before you execute, and it matters more as blast radius grows.

---

## Step 2: Look first, then change the root node only

**First, look at the running app: open the Inventory view and confirm there is no supplier shown anywhere.** Hold that image — you'll see it change.

Now the business rule for this lab: *every inventory item must name a supplier.* Ask Claude to add a **required** `supplier` string field to the `InventoryItem` model in `server/main.py` — and to change nothing else yet: no data, no routes, no frontend.

> Aside (optional): `main.py` already has a `supplier_name` field on `PurchaseOrder`/`CreatePurchaseOrderRequest` (substrate from Lab 4). That is a different field on a different model from the `InventoryItem.supplier` you're adding now — don't conflate them if you're reading the whole file.

---

## Step 3: Checkpoint 1 (the point step)

Run the backend suite:

```
uv run --project server pytest tests/backend/ -v
```

You know the checkpoint fired when pytest raises a `fastapi.exceptions.ResponseValidationError` naming the missing `supplier` field — **11 failures: 9 in `tests/backend/test_inventory.py` and 2 in `tests/backend/test_dashboard.py`** (`test_dashboard_low_stock_items_calculation` and `test_dashboard_inventory_value_calculation`, which call `GET /api/inventory` to cross-check dashboard math and hit the same 500).

**What you should see (abridged):**
```
FAILED tests/backend/test_inventory.py::TestInventoryEndpoints::test_get_all_inventory
  fastapi.exceptions.ResponseValidationError: ... 'loc': ('response', 0, 'supplier'),
  'msg': 'Field required' ...
...
==== 11 failed, ... passed ====   (9 in test_inventory.py, 2 in test_dashboard.py)
```

The exception fires inside `client.get()` before any assertion runs.

**Why this matters:** the route code never changed, yet `/api/inventory` now 500s. The model is a contract the data has to satisfy, and the checkpoint caught the break while it was one layer deep — before you stacked a schema, a route, and a Vue form on a broken foundation. The dashboard failures are expected; they confirm the cascade reached every consumer of the endpoint, not a mistake on your part.

---

## Step 4: The named 4-step debugging loop

> **Working reference:** the **debugging loop** is the named Theme 5 tool — **explain → hypothesis → confirm/challenge → fix** — that turns "it broke" into "I know why it broke." You're running it now for real.

Apply the loop explicitly and build `intervention-log.md` as you go. **The log is not hand-written notes after the fact — it is the executable trace of this loop.** For each step, you drive Claude to actually *do* the check (read the code, inspect the data, re-run the tests) and capture its real output in the log. That trace is what makes the log trustworthy: it records what happened, not what you assume happened.

1. **Explain** — ask Claude to explain how FastAPI's `response_model` validates the outgoing payload for this endpoint. Capture what it reports from the code.
2. **Hypothesis (required written field)** — before accepting Claude's answer, write your own one-sentence hypothesis for why a model change with no route change produces a 500. **This write is the point of the loop:** committing a prediction *before* you read the confirmation is what stops you from accepting the model's first explanation as ground truth.
3. **Confirm / challenge** — have Claude actually check the data source: ask it to read `inventory.json` and report whether a `supplier` key is present on the records. Capture that real result — this is the evidence that confirms or challenges your hypothesis.
4. **Fix — your design decision:** the required-field contract is broken because the data has no `supplier`. Choose and defend one:
   - **Path A:** backfill every record in `inventory.json` with a real supplier value (honors "required"). Plausible values are fine — e.g. one supplier per category — no research needed.
   - **Path B:** relax the field to `Optional[str] = None` (tolerates legacy records; weakens the business rule).

---

## Step 5: /compact

The debugging exploration is done and the conclusion is on disk. Run `/compact` to reclaim the context budget while keeping the decision.

---

## Step 6: Complete the cascade

The model is sound. Execute the remaining layers:

- Resolve the data per your Step-4 decision (ask Claude to do it).
- Confirm what the route needs: ask Claude whether `GET /api/inventory` needs any code change to expose the new field. (It does not — `response_model` serializes it once model and data agree. That's the teaching point.)
- Ask Claude to add a **Supplier** row to the `info-grid` in `client/src/components/InventoryDetailModal.vue`.

---

## Step 7: Checkpoint 2

```
uv run --project server pytest tests/backend/ -v
```

Expect green. Then **reload the app, open an inventory item's detail modal, and watch the Supplier value appear where nothing was before** — the same view you looked at in Step 2, now carrying the field you drove end-to-end.

---

## Step 8: /clear + unrelated task

You're switching to an unrelated frontend concern, so the multi-file context is now noise. Run `/clear` (not `/compact`).

Now start from what a user would *see*: `Reports.vue` renders its lists with `:key="index"`. **Reason about the symptom first** — what happens to Vue's rendering when one of those lists reorders or an item is inserted/removed? THEN ask Claude to explain WHY `:key="index"` causes it. You're **diagnosing, not fixing** (fix is extra credit).

> The symptom to reason about first: reorder or insert a row in a Reports list and Vue reuses DOM nodes by position, not identity — values and state stick to the wrong row. Claude should tie that to the `:key="index"` loops in `Reports.vue` and recommend a stable id (e.g. `q.quarter`, `month.month`).

---

## Step 9: Log + keep it (no commit)

Finish `labs/lab-5/intervention-log.md` — the executable trace you built in Step 4, now covering:
- The dependency graph
- The chosen checkpoint and the one-sentence defense
- All four steps of the debugging loop, with the real output Claude produced at each check (written hypothesis required)
- The design decision (Path A or B) and the defense
- One place you overrode or redirected Claude

**Keep it in your worktree — do not commit or push.** Nothing in this lab goes back to the repo; the log plus your end-to-end `supplier` change is your personal takeaway.

---

## Done criteria

You are done when:

1. `GET /api/inventory` returns 200 and the payload includes a `supplier` field (checkpoint 2 pytest green).
2. The Inventory detail modal renders the Supplier value in the browser.
3. `intervention-log.md` (kept locally in your worktree) contains: the dependency graph, the chosen checkpoint with defense, a written hypothesis, the design decision with defense, and one override note.

Be ready to share where you placed the checkpoint, what you hypothesized, and which resolution you defended.

---

## Extra Credit

1. **Fix, don't just find:** replace the three `:key="index"` in Reports.vue with stable keys (`q.quarter`, `month.month`) and confirm the app still renders.
2. **Push the field to the filter surface:** add `supplier` as a filterable param in `apply_filters` and wire it through `GET /api/inventory`, then decide with Claude whether that belongs in this change or a separate one.
3. **Prove the contract with a test:** ask Claude to write a pytest that asserts every item in `GET /api/inventory` has a non-empty `supplier`, and run it.
4. **Centralize the Reports.vue leak:** route its two hardcoded `http://localhost:8001` calls through `api.js` like every other view.

---

## Rescue block (self-service)

> **Before any rescue:** run every command from your worktree root (`pwd` should end in `lab-5-work`), not from `server/` or `client/`. If a command referencing `origin/lab-5-solution` fails with "invalid reference", run `git remote set-branches origin '*'` and `git fetch origin`, then retry. If `git worktree add` says the path "already exists" or the branch "is already used by worktree", run `git worktree list`, remove the stale entry with `git worktree remove <path> --force`, and re-run the `git worktree add` from the main clone root (worktree management commands run there; every other rescue command runs from the worktree).


**Rescue A: the 500 won't go away after you resolve it.** You likely fixed only one path. Ask Claude to check whether `server/data/inventory.json` has a `supplier` key on every record and whether `InventoryItem.supplier` matches that state. Then re-run:

```
uv run --project server pytest tests/backend/ -v
```

**Rescue B: you want a clean restart.** Run the `/reset-branch` command to discard your work and return to a clean state, then redo Step 0. Note: this permanently deletes uncommitted work — keep anything you want first.

**Rescue C: you ran out of time.** First confirm your remote points at the fork (`git remote -v` should show the lab fork, not your own working copy). Then check out the finished state so you still see the point of the lab:

```
git fetch origin
git checkout origin/lab-5-solution -- server/main.py server/data/inventory.json client/src/components/InventoryDetailModal.vue
```

Restart the servers, open a detail modal, and read `labs/lab-5/intervention-log.SAMPLE.md` on the solution branch to see the worked debugging loop.

---

## Ports and settings notes

If a server port is stuck, find and kill the process (e.g. port 8001 for the backend):
- **Windows:** `netstat -ano | findstr :<port>` then `taskkill /PID <pid> /F`
- **macOS:** `lsof -ti:<port> | xargs kill -9`

If tests auto-run on every edit, a leftover `.claude/settings.local.json` from a prior lab is active. Delete it and relaunch Claude Code (hooks are read at session start).
