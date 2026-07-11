# Reference Plan Mode output — AEP-142 low-stock alerting

This file captures what a Plan Mode session produces for this feature.
It is a prose plan only. Zero files were modified when this plan was reviewed.
`git status` after reviewing this plan showed only untracked spec and sub-task
files — no `.py` or `.vue` modifications.

The plan is a disposable artifact. The spec on disk (`specs/low-stock-alerting.md`)
is the durable output.

---

## Plan: implement low-stock alerting

### Step 1 — Add threshold config store to `server/main.py`

After the existing `inventory_items` load, add an in-memory dict:

```python
CATEGORY_THRESHOLDS: dict[str, int] = {
    "Actuators": 20,
    "Circuit Boards": 15,
    "Controllers": 10,
    "Power Supplies": 10,
    "Sensors": 25,
}
```

Values are illustrative defaults; ops will tune them. No database required.

### Step 2 — Add `GET /api/config/thresholds`

```python
@app.get("/api/config/thresholds")
def get_thresholds():
    return CATEGORY_THRESHOLDS
```

Provides transparency into the active thresholds without hardcoding them in
the client.

### Step 3 — Add `GET /api/inventory/low-stock`

```python
@app.get("/api/inventory/low-stock", response_model=List[InventoryItem])
def get_low_stock_items():
    return [
        item for item in inventory_items
        if item.quantity_on_hand <= CATEGORY_THRESHOLDS.get(
            item.category, item.reorder_point
        )
    ]
```

New endpoint; no change to existing `/api/inventory` shape.

### Step 4 — Surface in `client/src/views/Inventory.vue`

- Import the new `getLowStockItems()` API function (add to `client/src/api.js`).
- On component mount, call `getLowStockItems()` and store results in a reactive ref.
- Render a `<div class="low-stock-banner">` above the main inventory table when
  the list is non-empty; list item name, category, and `quantity_on_hand`.

### Step 5 — Add backend tests

Create `tests/backend/test_low_stock.py` with four cases:
1. Item at threshold is included.
2. Item above threshold is excluded.
3. Category with no threshold entry falls back to `reorder_point`.
4. Empty inventory returns empty list.

---

## What this plan does NOT do

- No write endpoint for thresholds (Phase 2 scope).
- No persistent storage (in-memory only, consistent with constraint).
- No modification to `GET /api/inventory` or `GET /api/dashboard/summary`.
- No implementation here — this was a Plan Mode review, not an execution.
