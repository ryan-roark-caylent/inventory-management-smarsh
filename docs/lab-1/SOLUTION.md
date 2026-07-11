# Lab 1 Solution — Facilitator Reference

**Facilitator-tier only. Never shown to participants.**

---

## Issue routing (model answer — defensible, not exclusive)

| Issue | Surface | Reasoning |
|-------|---------|-----------|
| A — "How should low-stock alerting work?" (spec/planning) | Claude.ai | No code exists yet. This is design thinking and open questions — a conversational planning session in the browser is the right starting surface. Optionally follow with Cowork for a structured written plan doc. |
| B — "Reports page bypasses the shared API client" (multi-file refactor) | Claude Code | Needs to read `Reports.vue`, trace `api.js`, and plan changes across files. Claude Code can read the repo and propose a precise, file-anchored diff. |
| C — "Nightly stale-inventory report" (batch/CI script) | API / CI | Runs unattended, non-interactively, on a schedule. No human in the loop. The API surface is the only one that fits. |

---

## Round 1 vs Round 2 delta

**Round 1 (Claude.ai, symptom only):**
Claude.ai has no access to the repo. It reasons from the symptom description alone and returns a general hypothesis: the backlog count is computed from the full dataset rather than the filtered subset. It cannot name a file or line because it has not read any code.

**Round 2 (Claude Code, repo-grounded):**
Claude Code reads `server/main.py`, locates `get_dashboard_summary`, and identifies line 200:

```python
total_backlog_items = len(backlog_items)
```

Every other field uses the filtered list (`filtered_inventory`, `filtered_orders`). The backlog count uses the global `backlog_items`. Claude Code proposes the minimal fix:

```python
total_backlog_items = len(apply_filters(backlog_items, warehouse, category))
```

**The lesson:** same underlying model, different surface, different quality of answer. The surface you pick decides whether Claude guesses from a symptom or reads your code and lands the exact fix.

---

## Filter bug locations

1. **`server/main.py:200`** — `total_backlog_items = len(backlog_items)` uses the unfiltered list. Fix: `len(apply_filters(backlog_items, warehouse, category))`.

2. **`server/main.py:17`** — `filter_by_month` falls through to `return items` when the quarter string is unrecognized (e.g., `Q1-2026`). Fix: change fallthrough to `return []`.

---

## Important note on the `apply_filters` fix (line 200)

The one-line fix at line 200 is **pattern-consistent** with the rest of `get_dashboard_summary` but is **not production-complete**.

`BacklogItem` has no `warehouse` or `category` field. When `apply_filters` receives `backlog_items` with a warehouse filter active, it cannot match any item on the warehouse field — so it returns an empty list. The fixed endpoint returns `total_backlog_items: 0` under any warehouse filter rather than the true filtered count.

**What a production-complete fix requires:**
1. Add a `warehouse` field (and optionally `category`) to the `BacklogItem` model in `server/main.py`.
2. Add a `"warehouse"` string to every record in `server/data/backlog_items.json`, matching the warehouse names used in inventory.
3. Re-verify that `apply_filters` checks `warehouse` on the item dict — it already does for inventory items, so the logic generalizes once the field exists.

EC4 is where participants observe this gap directly: they apply the one-liner, re-hit the API, and see the count drop to 0 rather than the true filtered value. That result is the teaching point, not a sign the fix is wrong.

---

## Model/effort selection (reference reasoning)

- **Trivial rename (one file):** lighter tier (e.g., Haiku/Sonnet), low/normal effort. Task is simple and low-risk; burning reasoning budget here adds latency with no benefit.
- **Multi-file refactor (`Reports.vue` + `api.js`):** stronger tier (Sonnet or above), higher reasoning effort. Task spans files, has correctness risk (breaking the shared client), and benefits from longer context and more careful planning.

The principle: match effort to complexity and risk. This is a reasoning habit, not an evaluation sweep — pick once and act, don't benchmark both.

---

## Sources

- [20-lab-1-design.md](../../../../smarsh-ai-sdlc/lab-build/20-lab-1-design.md) — Sections 6, 8, 10, 11
- `server/main.py:200` (verified on main)
- `server/main.py:17` (`filter_by_month` fallthrough, verified on main)

**Date generated:** 2026-07-11
