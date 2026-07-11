# Sub-tasks — AEP-142 low-stock alerting

Reference Jira-ready breakdown. Each task is discrete, independently
mergeable, and has a one-line acceptance check.

---

## SUB-1 — Add threshold config store

**Description:** Create an in-memory threshold dict in `server/main.py` with
a default entry for each of the five categories (Actuators, Circuit Boards,
Controllers, Power Supplies, Sensors). Expose it via
`GET /api/config/thresholds` (returns the full dict as JSON).

**Acceptance check:** `GET /api/config/thresholds` returns a JSON object with
a key for every category in `server/data/inventory.json` and no 500 errors.

---

## SUB-2 — Add `GET /api/inventory/low-stock` handler

**Description:** Add a new FastAPI route that iterates `inventory_items`,
compares each item's `quantity_on_hand` against
`thresholds.get(item.category, item.reorder_point)`, and returns the filtered
list. Response model is `List[InventoryItem]`.

**Acceptance check:** `pytest tests/backend/test_low_stock.py` passes,
including a case where a category with no threshold entry falls back to
`reorder_point` and a case where an item above its threshold is excluded.

---

## SUB-3 — Surface low-stock alerts on the Inventory view

**Description:** In `client/src/views/Inventory.vue`, add a section that
calls `GET /api/inventory/low-stock` and renders the result as a dismissible
alert list above the main inventory table. Show item name, category, and
quantity.

**Acceptance check:** running the dev server and visiting the Inventory view
shows a visible low-stock section when items below threshold exist; section is
empty (or hidden) when no items qualify.

---

## SUB-4 — Add pytest coverage for the new handler

**Description:** Add `tests/backend/test_low_stock.py` with at minimum:
(a) items at threshold are included, (b) items above threshold are excluded,
(c) a category with no configured threshold falls back to `reorder_point`,
(d) an empty inventory returns an empty list.

**Acceptance check:** `uv run pytest tests/backend/test_low_stock.py -v`
reports all cases passed with no warnings about missing fixtures.
