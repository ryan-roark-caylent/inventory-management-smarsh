# Lab 1 — The Core Loop (Ask → Review Diff → Accept → Verify → Commit)

**Time budget: 20 minutes** | **Solo** (one person, one machine, one session)

**Objective:** run one complete change loop in Claude Code, read the full diff before accepting, verify the change in the running app, and commit with a clear message.

**The thesis:** Reading the diff is the gate between a demo and production work.

---

> **Tell-Claude convention:** every app, server, and test action in this lab goes through Claude or the repo's slash skills (`/start`), never the raw terminal. CLAUDE.md and the skills already carry the how. The two deliberate human-typed exceptions are the Step 0 branch ritual and the Step 6 `git log` check — those control and verify the environment Claude runs in.

---

## Step 0 — Branch and start (2 min)

1. In a terminal at the repo root, type:
   ```
   git fetch origin
   git checkout -b lab-1-work origin/lab-1-start
   ```
   The fetch is not optional. You cloned during homework, before the lab branches were pushed at repo freeze. Without it the checkout fails with `fatal: 'origin/lab-1-start' is not a valid object name`.

2. Start Claude Code (`claude`) and type:
   ```
   /start
   ```
   Approve the commands Claude proposes (it kills anything on ports 3000/8001, then starts both servers).

3. Open `http://localhost:3000` in your browser. **Observe:** the dashboard renders with KPI cards and an "Inventory Shortages (4)" card.

4. **Expected and OK:** the browser dev-tools console shows failing `GET /api/tasks` requests. That 404 is planted course material for a later exercise, not breakage. Ignore it.

---

## Step 1 — See the bug before you fix it (2 min)

1. Open these two URLs in two browser tabs:
   ```
   http://localhost:8001/api/dashboard/summary
   http://localhost:8001/api/dashboard/summary?warehouse=Tokyo
   ```

2. **Observe:** between unfiltered and Tokyo, every field changes except one:
   - `total_inventory_value`: 439073.6 → 154567.3
   - `low_stock_items`: 4 → 3
   - `pending_orders`: 54 → 16
   - `total_orders_value`: ~31.17M → ~13.00M
   - `total_backlog_items`: **4 → 4. It ignored the filter. That is the bug.**

3. Cross-check the UI: on `localhost:3000`, set the Warehouse filter to Tokyo. The "Inventory Shortages" card shows (0), because the frontend filters that count itself. The backend summary endpoint claims 4. Frontend and backend disagree; you are about to make the backend honest.

---

## Step 2 — `/model` beat (1 min)

1. In Claude Code, type:
   ```
   /model
   ```

2. **Observe:** the model picker. Confirm **Sonnet** is selected; if not, select it.

3. Why (one line): this is a one-line bug fix. Sonnet does it as well as Opus at a fraction of the cost and latency. Defaulting to Opus burns your monthly quota for nothing.

---

## Step 3 — Ask (4 min)

1. Paste this prompt exactly:
   ```
   The dashboard's total_backlog_items ignores the warehouse and category filters while every other summary stat respects them. Find and fix it in server/main.py.
   ```

2. **Observe:** Claude reads `server/main.py`, finds the summary endpoint, and proposes an edit. A **permission prompt** appears before any file changes. That prompt is the default permission mode doing its job: nothing touches your files until you approve it. Do NOT approve yet; go to Step 4.

   > **No prompt appeared and the edit is already applied?** You are in `accept edits` mode — check the mode indicator at the bottom of the screen and press **Shift+Tab** until it shows default mode. Approving the prompt IS the "accept" in this lab's loop; there is no separate accept step afterward. If an edit slipped through, review it with `git diff` instead, and redo this lab's gate on the next prompt.

---

## Step 4 — Read the diff. All of it. (3 min)

**This is the point of the lab.**

"Read the diff" means concretely, inside the Edit approval prompt:

1. **The file path.** Check it says `server/main.py` and nothing else. One file.

2. **The red line** (what is being removed):
   ```python
   total_backlog_items = len(backlog_items)
   ```

3. **The green line(s)** (what replaces it). Read every insertion. The right shape: one or two lines that call `apply_filters(backlog_items, warehouse, category)` directly — the same helper the surrounding stats already use. Claude may produce this as a single inline call or as two lines (assign then count); both are correct if they call `apply_filters`.

4. **The sanity check:** does the replacement call `apply_filters` with `warehouse` and `category` — the same helper and arguments the filtered stats use a few lines above? If yes, accept. If the replacement builds a SKU set from inventory (`{item["sku"] for item in ...}`) or touches any other file, reject it, press Esc twice to rewind, and re-paste the Step 3 prompt. A SKU-join looks plausible but breaks the unfiltered count (Step 5 will catch it either way).

Accept the edit. The whole review took about ten seconds. That is the entire cost of knowing exactly what changed.

---

## Step 5 — Verify in the running app (4 min)

1. The backend does not hot-reload Python. Restart it:
   ```
   /start
   ```

2. Refresh both browser tabs from Step 1. **Observe:**
   - Unfiltered: `total_backlog_items` is still **4** (unchanged behavior preserved).
   - `?warehouse=Tokyo`: `total_backlog_items` is now **0**.

3. Why 0 is correct: the four backlog records carry no warehouse tag (look at `server/data/backlog_items.json` if curious), so none of them belong to Tokyo. The frontend already said 0 for the same reason. Backend and frontend now agree.

4. **Trap check (important):** if your unfiltered tab now shows **0 instead of 4**, Claude gave you a plausible-looking wrong fix (usually a SKU join against inventory). Your verification caught what the diff read could not. Tell Claude:
   ```
   The unfiltered count must stay 4. Match the apply_filters pattern the other summary stats use on the lines above.
   ```
   Then re-run Step 4 and Step 5.

---

## Step 6 — Commit locally, never push (3 min)

1. Paste this prompt exactly:
   ```
   Commit this fix locally with a clear one-line commit message. Local commit only: do not push, do not create a pull request.
   ```

2. A permission prompt shows the `git commit` command including the message. **Read the message before approving.** A good one names the behavior, not the line: e.g. "Fix dashboard total_backlog_items to respect warehouse and category filters". If it is vague ("fix bug"), tell Claude to rewrite it before approving.

3. Confirm in your terminal:
   ```
   git log --oneline -2
   ```
   **Observe:** exactly one new commit sits on top of the commit you branched from (the `lab-1-start` tip). If Claude offers to push or open a PR, decline. Nothing leaves your machine today.

4. Self-check the done criteria with two things on your own screen: the `?warehouse=Tokyo` browser tab and the `git log` output. Then post the chat signal (optional but encouraged): paste your one-line diff and your `git log --oneline -2` output into the meeting chat.

---

## Done Criteria

Self-check both of these on your own screen:

- [ ] `http://localhost:8001/api/dashboard/summary?warehouse=Tokyo` shows `"total_backlog_items": 0`
- [ ] `git log --oneline -2` shows one new commit above the `lab-1-start` tip on a `lab-1-work` branch

**Optional chat signal (encouraged):** paste the one-line diff and `git log --oneline -2` output into the meeting chat. That post is how facilitators read completion across the call.

---

## Stuck? Post in meeting chat.

A TA will reply in chat or pull you into a breakout room.

| Symptom | Self-serve move |
|---|---|
| `fatal: 'origin/lab-1-start' is not a valid object name` | You cloned before the branches were pushed. Run `git fetch origin`, then re-run the checkout. |
| `/start` errors; port in use; `uv` or npm missing | `/start` already kills by port — approve its kill commands. If toolchain is missing (homework not done), post in chat and a TA will help. |
| Edit prompt touches multiple files, multiple hunks, or proposes a refactor | Reject the edit, press Esc twice to rewind, re-paste the Step 3 prompt verbatim. The prompt names the file; second attempts converge. |
| After restart, the unfiltered URL shows 0 instead of 4 | Wrong fix (SKU join variant). Use the corrective prompt in Step 5.4, re-read the diff, re-verify. |
| Tokyo tab still shows 4 after the edit | Backend was not restarted (no Python hot-reload). Run `/start` again and hard-refresh the tab. |

---

## Extra Credit (time permitting)

Run the whole loop again, unassisted, on a second planted bug.

**Part 1 — see it:**

Open:
```
http://localhost:8001/api/dashboard/summary?month=Q1-2026
```

**Observe:** `total_orders_value` is ~31.17M, the all-time total. A quarter with zero data returned everything.

**Part 2 — fix it:**

Paste:
```
filter_by_month in server/main.py silently returns ALL items when given a quarter it does not recognize, like Q1-2026. Unknown quarters should return no items. Fix it.
```

Read the diff (small, single function), accept, restart with `/start`, refresh: `total_orders_value` for `?month=Q1-2026` should now be 0. Unfiltered and `?month=Q1-2025` behavior must not change.

Commit locally with a message you reviewed. Same rule: never push.

**Part 3 — bonus codebase Q&A (zero risk, no file changes):**

```
Where is the monthly revenue goal set, and what is its value?
```
