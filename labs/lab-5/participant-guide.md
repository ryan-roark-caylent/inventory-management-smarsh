# Lab 5 — Multi-Step Workflows and Session Management (+ the Debugging Loop)

**Track 2 (Vibecode) · Position 5 of 9**

**Objective:** Plan a cross-cutting `supplier` field-add across the inventory-management stack, catch the cascade failure at a planned checkpoint, run the 4-step debugging loop to diagnose it, resolve it with a defended design decision, and demonstrate `/compact` and `/clear` discipline.

**Core path: ~50 min · Extra Credit: additional time as available**

---

## Step 0 — Setup

```
git fetch origin
git checkout -b lab-5-work origin/lab-5-start
```

Start the stack:
- **Windows:** `scripts/start.ps1` (or run `/start` in Claude Code)
- **macOS:** `scripts/start.sh`

Open the app in the browser and click into the Inventory view.

---

## Step 1 — Sketch the dependency graph

On paper (or in `intervention-log.md`), list the four layers the `supplier` field touches:

1. The `InventoryItem` Pydantic model (`server/main.py`)
2. The `inventory.json` data source
3. The `GET /api/inventory` route
4. The `InventoryDetailModal.vue` display

Draw arrows for "depends on." For each node, mark blast radius: does a change here cascade to other nodes, and is it recoverable? Then mark the ONE highest-value checkpoint. Write one sentence defending where you put it.

---

## Step 2 — Change the root node only

The business rule: every inventory item must name a supplier. Ask Claude to add a **required** `supplier` string field to the `InventoryItem` model in `server/main.py` — and to change nothing else yet.

---

## Step 3 — Checkpoint 1

Run the backend suite:

```
uv run --project server pytest tests/backend/ -v
```

You know the checkpoint fired when pytest raises a `ResponseValidationError` naming the missing `supplier` field.

Note what you see and record it in your `intervention-log.md`.

---

## Step 4 — The named 4-step debugging loop

Apply the loop explicitly and record each step in `intervention-log.md`:

1. **Explain** — ask Claude to explain how FastAPI's `response_model` validates the outgoing payload for this endpoint.
2. **Hypothesis (required written field)** — before accepting Claude's answer, write your own one-sentence hypothesis for why a model change with no route change produces a 500.
3. **Confirm / challenge** — verify it against the data source. Ask Claude whether `inventory.json` actually contains a `supplier` key.
4. **Fix — your design decision:**
   - **Path A:** backfill every record in `inventory.json` with a real supplier value (honors the "required" contract).
   - **Path B:** relax the field to `Optional[str] = None` (tolerates legacy records; weakens the business rule).
   Pick one, write why.

---

## Step 5 — /compact

The debugging exploration is done and the conclusion is on disk. Run `/compact` to reclaim the budget while keeping the decision.

---

## Step 6 — Fan-out

Now the model is sound, execute the remaining layers:

- Resolve the data per your Step-4 decision.
- Confirm what the route needs: ask Claude whether `GET /api/inventory` needs any code change to expose the new field.
- Add a **Supplier** row to the `info-grid` in `client/src/components/InventoryDetailModal.vue`.

---

## Step 7 — Checkpoint 2

```
uv run --project server pytest tests/backend/ -v
```

Reload the app, open an inventory item's detail modal, and confirm Supplier renders.

---

## Step 8 — /clear + unrelated task

You are switching to an unrelated frontend concern, so the multi-file context is now noise. Run `/clear` (not `/compact`). Then ask Claude to find and explain the `:key="index"` anti-pattern in `client/src/views/Reports.vue`. You are diagnosing, not necessarily fixing (fix is extra credit).

---

## Step 9 — Log + commit

Finish `labs/lab-5/intervention-log.md` (checkpoint map, written hypothesis, named design decision + defense, one place you overrode or redirected Claude). Commit the feature and the log.

---

## Extra Credit

1. **Fix, don't just find:** replace the three `:key="index"` in Reports.vue with stable keys (`q.quarter`, `month.month`) and confirm the app still renders.
2. **Push the field to the filter surface:** add `supplier` as a filterable param in `apply_filters` and wire it through `GET /api/inventory`, then decide with Claude whether that belongs in this change or a separate one.
3. **Prove the contract with a test:** write a pytest that asserts every item in `GET /api/inventory` has a non-empty `supplier`, and run it.
4. **Centralize the Reports.vue leak:** route its two hardcoded `http://localhost:8001` calls through `api.js` like every other view.

---

## Rescue block (self-service)

> **Rescue A — the 500 won't go away after you resolve it.** You likely fixed only one path. Ask Claude: "Check whether `server/data/inventory.json` has a `supplier` key on EVERY record and whether `InventoryItem.supplier` is required; make them consistent." Then re-run `uv run --project server pytest tests/backend/ -v`.

> **Rescue B — you want a clean restart.** Run `/reset-branch` to discard your work and return to `main`, then redo Step 0.

> **Rescue C — you ran out of time.** Check out the finished state so you still see the point of the lab: `git fetch origin` then `git checkout origin/lab-5-solution -- server/main.py server/data/inventory.json client/src/components/InventoryDetailModal.vue`. Restart the servers, open a detail modal, and read `labs/lab-5/intervention-log.SAMPLE.md` on the solution branch.

> **Windows:** if a server port is stuck, find and kill the process: `netstat -ano | findstr :<port>` then `taskkill /PID <pid> /F` (e.g., port 8001 for the backend). If tests auto-run on every edit, a leftover `.claude/settings.local.json` from a prior lab is active — delete it and relaunch Claude Code.
>
> **macOS:** start the stack with `scripts/start.sh`. If a server port is stuck, kill it: `lsof -ti:<port> | xargs kill -9`. The same `settings.local.json` note applies — delete it and relaunch Claude Code.
