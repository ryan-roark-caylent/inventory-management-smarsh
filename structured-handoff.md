# Structured Handoff — Dashboard Summary Filter Bug

## Findings

**Primary (test-targeted):** `total_inventory_items` in `get_dashboard_summary` (`server/main.py`) is computed as `len(inventory_items)` — the global unfiltered list. `filtered_inventory` is already computed two lines above (`filtered_inventory = apply_filters(inventory_items, warehouse, category)`) but is not used for this field. Result: the field always returns 32 regardless of warehouse or category filters, so `test_inventory_count_respects_filter` fails with `assert 32 < 32`.

**Secondary (known issue, out of scope):** `total_backlog_items = len(backlog_items)` at line 200 is also unfiltered. However, `backlog_items` carries no `warehouse` or `category` fields, so `apply_filters` cannot meaningfully filter it. This is a separate known issue and is explicitly deferred from this workflow.

**Additional observation:** `allow_origins=["*"]` in the CORS config is broad for anything beyond a demo environment. Not related to the failing test; noted for future work.

## Decisions

Fix: change line 201 from:
```python
total_inventory_items = len(inventory_items)
```
to:
```python
total_inventory_items = len(filtered_inventory)
```

Scope: `total_inventory_items` only. One line, no new variables, no new dependencies. `filtered_inventory` is already computed and available in scope. Do not touch `total_backlog_items` — that fix is non-trivial and out of scope for this workflow.

## Constraints

- In-memory only — no database, no new imports, no new dependencies.
- Touch only the `get_dashboard_summary` function in `server/main.py`.
- Do not modify any other endpoint.
- The fix must make `test_inventory_count_respects_filter` pass: for warehouse="San Francisco", `total_inventory_items` must return 12 (not 32).
- `total_backlog_items` fix is explicitly deferred.
