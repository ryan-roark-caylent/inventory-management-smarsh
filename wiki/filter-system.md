# Filter system

## What it does
Four filters (Time Period, Warehouse, Category, Order Status) apply across the app.

## Client to server flow
- client/src/composables/useFilters.js holds the four filters as module-level refs
  (a singleton: every view shares the same state).
- getCurrentFilters() maps the internal `selectedPeriod` ref to the API param `month`.
- client/src/api.js targets the backend over HTTP and sends the filters as query params.
- The server applies them through one shared filter helper that several endpoints reuse.
  Which endpoints, and what a signature change would break, is a graph question:
  ask graphify rather than trusting a list written here, which would go stale.

## What the code graph cannot tell you (why this article exists)
- The HTTP hop between the client and the server is invisible to graphify:
  `graphify path "useFilters()" "get_inventory()"` returns "No path found." The AST models
  imports and calls, not network requests.
- The internal ref name (selectedPeriod) differs from the API param (month) differs from the
  server-side handling — a rename coupling no single file reveals.

## Sources
- client/src/composables/useFilters.js, client/src/api.js, server/main.py
