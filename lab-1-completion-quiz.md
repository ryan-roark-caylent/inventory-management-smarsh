# Lab 1 — Completion Quiz

**Instructions:** Select the best answer for each question. Answer based on what you observed during the lab.

---

**Q1.** When you ran Claude Code on the backlog-count bug, which location did it identify?

- A) `server/main.py` line 200 (inside `get_dashboard_summary`)
- B) `server/main.py` line 174 (the `get_backlog` loop)
- C) `server/main.py` line 191 (the inventory filter line)
- D) `server/mock_data.py` line 12 (the mock data loader)

---

**Q2.** Claude Code proposed wrapping the backlog count in `apply_filters(backlog_items, warehouse, category)`. What did it also surface about that fix?

- A) It is pattern-consistent with the other metrics but returns 0 under any warehouse filter, because `BacklogItem` has no warehouse field.
- B) The fix is fully correct; `apply_filters` returns all matching items when a field is absent from the underlying data model.
- C) The fix requires renaming `backlog_items` to `filtered_orders` so the count uses the already-filtered orders list from the endpoint.
- D) The fix works but requires moving the backlog count calculation above the inventory filter block to produce the correct result.

---

**Q3.** You called `/api/dashboard/summary?warehouse=London`. Which field did NOT change versus the unfiltered call?

- A) `total_backlog_items`
- B) `low_stock_items`
- C) `total_inventory_value`
- D) `total_orders_value`

---

**Q4.** How did Claude.ai's Round 1 answer differ from Claude Code's Round 2 answer on the same bug?

- A) Claude.ai named a cause without any file or line; Claude Code named the exact file, line, and proposed the fix
- B) Claude.ai named the specific file and line number; Claude Code only restated the symptom without naming any code location
- C) Both surfaces named the same file and proposed the same fix; they differed only in how they explained the root cause
- D) Claude.ai proposed the one-line fix first; Claude Code said it needed to read the repo before it could give an answer

---

**Q5.** In your surface map, the batch/CI script issue (issue C) is routed to the surface that runs unattended and non-interactively. Which surface is that?

- A) API / CI (runs unattended, non-interactive, no human in the loop)
- B) Claude.ai (browser chat, requires a human to read and respond each turn)
- C) Claude Code (interactive CLI session, requires a human to direct and approve steps)
- D) Claude Cowork (desktop app, designed for document and plan work with human review)
