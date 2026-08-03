# Spec: Days of Cover

Add a computed "days of cover" field to the inventory endpoint. Days of cover is how many days the current stock on hand will last at the current demand rate.

---

## What to build

### 1. Server — `server/main.py`

Extend `InventoryItem` (the Pydantic model at L59-69) with one optional field:

```
days_of_cover: Optional[float] = None
```

In `get_inventory` (L129), after `apply_filters` returns the filtered item list, compute `days_of_cover` for each item:

- Match each inventory item to its demand forecast by SKU (using `demand_forecasts` imported at L5).
- The demand forecast records a `current_demand` value for a period of 30 days. Use that to compute a daily rate.
- `days_of_cover = quantity_on_hand / (current_demand / 30)`
- Round to one decimal place.
- If no forecast exists for the item's SKU, set `days_of_cover` to `None`.

The result must flow through `apply_filters()` — do not bypass the filter chokepoint. The filtering step runs first; the computation runs over the already-filtered list.

Return the enriched items. The endpoint signature (`/api/inventory`) must not change.

### 2. Client — `client/src/views/Inventory.vue`

Surface `days_of_cover` as a new column in the inventory table. Follow the repo's existing i18n convention:

- Add a translatable key to `client/src/locales/en.js` under `inventory.table`. Choose a key name that matches the existing naming style (lowercase camelCase, descriptive noun).
- Add the same key with a Japanese translation to `client/src/locales/ja.js`.
- In `Inventory.vue`, add a `<th>` for the new column using `t('inventory.table.<yourKey>')`, matching the pattern of the existing column headers.
- In each `<tr>`, add a `<td>` that renders the value. If `days_of_cover` is `null`, show `—` (an em dash) rather than a blank or "null".

You will need to find where `useI18n()` is set up in this view, where locale strings live, and how the existing table columns are structured. The codebase has a consistent pattern; follow it.

---

## Constraints

- **In-memory only.** The server uses `mock_data.py` which loads from JSON files. No database writes. No schema migration.
- **No new dependencies.** Do not add any new PyPI packages to `server/` or npm packages to `client/`.
- **No endpoint signature changes.** `/api/inventory` keeps its existing query parameters (`warehouse`, `category`).
- **No app boot required on the critical path.** The backend tests alone are sufficient to verify the computation is correct.

---

## Acceptance criteria

1. `uv run --project server pytest` passes all 40 existing tests with no new failures.
2. The inventory endpoint returns `days_of_cover` for items that have a matching SKU in `demand_forecasts`, and `null` for items that do not.
3. The Inventory view shows a "days of cover" column with a translatable label (not hardcoded English).
4. Items with no forecast show `—`, not blank or "null".
