# Lab 4 — Completion Quiz

Answer these after finishing the core path (Steps 1–7).

**Q1.** In your first-pass endpoint, which field appeared in the created-PO JSON that your spec said to exclude?
- A) `supplier_name`
- B) `unit_cost`
- C) `expected_delivery_date`
- D) `backlog_item_id`

**Q2.** When the response didn't match the spec, what did you change to fix it?
- A) Re-ran the same prompt, this time with more explicit wording
- B) Edited one line of `specs/purchase-orders.md`, then regenerated
- C) Hand-edited the JSON response directly in the browser console
- D) Added a new PyPI library to enforce the response contract shape

**Q3.** Running `pytest` for the backend on this lab used which command?
- A) `npm run test:unit -- --dir tests/backend`
- B) `pytest server/main.py --cov -v`
- C) `uv run --project server pytest tests/backend/ -v`
- D) `vitest run tests/backend/ --reporter verbose --passWithNoTests`

**Q4.** What backed the `createPurchaseOrder` call in api.js before you built the route?
- A) A working POST route that returned the newly created PO record
- B) Nothing — the stub 404'd because no backend route backed it
- C) The `/api/backlog` route, which doubled as a placeholder handler
- D) An in-memory SQLite table seeded with test fixtures at startup

**Q5.** Which implementation did the core path (Steps 1–7) require?
- A) Backend POST route only, no new Vue component
- B) Backend POST route plus a new `PurchaseOrderModal.vue` component
- C) Vue modal only — the backend POST route was already present in the repo
- D) A migration adding a `purchase_orders` database table, no route added
