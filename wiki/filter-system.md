# Filter system

## What it does
Four filters (Time Period, Warehouse, Category, Order Status) apply across the app.

## Client to server flow
- client/src/composables/useFilters.js holds the four filters as module-level refs
  (a singleton: every view shares the same state).
- getCurrentFilters() maps the internal `selectedPeriod` ref to the API param `month`.
- client/src/api.js:3 targets http://localhost:8001/api and sends the filters as query params.
- server/main.py:33 apply_filters(items, warehouse, category, ...) receives them; three
  endpoints call it (get_inventory, get_orders, get_dashboard_summary).

## What the code graph cannot tell you (why this article exists)
- The HTTP hop between api.js and apply_filters() is invisible to graphify:
  `graphify path "useFilters()" "get_inventory()"` returns "No path found." The AST models
  imports and calls, not network requests.
- The internal ref name (selectedPeriod) differs from the API param (month) differs from the
  server-side handling — a rename coupling no single file reveals.

## Sources
- client/src/composables/useFilters.js, client/src/api.js, server/main.py:33-47
