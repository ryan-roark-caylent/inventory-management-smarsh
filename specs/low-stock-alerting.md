# Low-Stock Alerting

## 1. Task
Surface a new `GET /api/inventory/low-stock` endpoint that returns every
`InventoryItem` whose `quantity_on_hand` is at or below a per-category
threshold, with a default fallback to the item's own `reorder_point`, so the
ops team can act before a stockout.

## 2. Context
Files touched:
- `server/main.py` — add threshold config store and new handler
- `client/src/views/Inventory.vue` — surface the low-stock list in the UI

Existing inventory endpoint: `GET /api/inventory` returns
`List[InventoryItem]`. The `/api/dashboard/summary` handler already computes
a crude `low_stock_items` count using `reorder_point` but the ops team does
not trust it.

Shared dependency: `/api/inventory` is consumed by two other internal
services. The low-stock feature lives on a **new endpoint**, not a shape
change to the existing one, preserving backward compatibility.

## 3. Constraints
- In-memory only — no database, no new external dependencies.
- Do not alter the shape of `GET /api/inventory` or
  `GET /api/dashboard/summary`.
- No write endpoints in scope; threshold configuration uses a separate config
  resource (see § Threshold configuration).
- All five real categories must be coverable:
  Actuators, Circuit Boards, Controllers, Power Supplies, Sensors.

## 4. Format
```
GET /api/inventory/low-stock

Response 200:
[
  {
    "id": "...",
    "sku": "...",
    "name": "...",
    "category": "Sensors",
    "warehouse": "...",
    "quantity_on_hand": 5,
    "reorder_point": 10,
    "unit_cost": ...,
    "location": "...",
    "last_updated": "..."
  },
  ...
]
```

Each returned item is the full `InventoryItem` shape (no new fields on the
existing model). An item is included when
`quantity_on_hand <= thresholds.get(category, item.reorder_point)`.

## 5. Example
Existing endpoint for reference shape:
```
GET /api/inventory
→ [..., {"id":"1","sku":"ACT-001","name":"Servo Motor","category":"Actuators",
          "warehouse":"Chicago","quantity_on_hand":45,"reorder_point":15,...}]
```

Low-stock call with default thresholds:
```
GET /api/inventory/low-stock
→ items where quantity_on_hand <= thresholds.get(category, reorder_point)
```

## Risks
**Weakness 1 — stale in-memory snapshot.** The inventory list is loaded once
at process start from `server/data/inventory.json` (see `mock_data.py`). Any
real stock movement does not update the in-memory list until the process
restarts. Alerts will reflect stale data indefinitely in a long-running
process.

**Weakness 2 — missing-category silent skip.** If a category string in the
data has no entry in the thresholds dict, the code falls back to
`item.reorder_point`. That default is sound per the design, but the spec
does not document what happens if `reorder_point` itself is zero — an item
with `reorder_point == 0` and `quantity_on_hand == 0` would appear as
low-stock even if ops considers it obsolete.

**Likely failure mode.** A category key typo (e.g., `"Sensor"` vs
`"Sensors"`) silently falls back to `reorder_point` instead of the
configured threshold, giving ops a false clear signal for that category
without any error or log entry.

**Alternative A — event-driven on write.** Compute alerts at write time and
cache the result. Fewer stale-read risks. Requires write endpoints that do
not yet exist on this read-only backend; out of scope for Phase 1.

**Alternative B — separate thresholds config resource (`GET/PUT
/api/config/thresholds`).** Cleaner ownership; ops can update thresholds
without a redeploy. Adds one more endpoint surface to document, version, and
secure. Preferred for Phase 2 if write endpoints are added.

*Forward-looking note:* a concurrent-write race is not a present failure mode
because this backend is read-only. It becomes relevant when write endpoints
are introduced.

## Threshold configuration
**Decision:** an in-memory dict initialized at startup, exposed via a new
`GET /api/config/thresholds` read endpoint and a `PUT
/api/config/thresholds` write endpoint. Default values are hardcoded per
category in `main.py`; ops can update them at runtime without a redeploy.

**Defense:** a JSON file (`server/data/thresholds.json`) would survive
restarts but couples config to the file system. A hardcoded default in the
handler is simpler but not updatable at runtime. The config-endpoint approach
gives ops agency without adding a database dependency, consistent with the
in-memory-only constraint.
