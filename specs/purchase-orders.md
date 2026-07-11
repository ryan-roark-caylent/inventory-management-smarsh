# Feature Spec: POST /api/purchase-orders

## Task
Build a `POST /api/purchase-orders` endpoint that creates a new purchase order for an existing backlog item.

## Context
Lives in `server/main.py` alongside the existing FastAPI routes. The `PurchaseOrder` and `CreatePurchaseOrderRequest` Pydantic models are already defined. The in-memory `purchase_orders` list (imported from `mock_data`) stores records at runtime. Backlog items are in the in-memory `backlog_items` list. The client stub `createPurchaseOrder` in `client/src/api.js` calls `POST /purchase-orders` but currently 404s — this route backs it. Must not change any existing GET endpoint signatures.

## Constraints
- No new PyPI dependencies
- Preserve existing GET endpoint signatures unchanged
- `quantity` must be a positive integer; reject with 422 if zero or negative
- `backlog_item_id` must match an existing backlog item; reject with 404 if not found
- Response must exclude the `unit_cost` field (internal cost data, not for buyers)
- Append the new record to the in-memory `purchase_orders` list (no database)

## Format
Returns HTTP 200 with a JSON object containing exactly these fields:
- `id` (string, format `PO-{N}` where N = `len(purchase_orders) + 1000`)
- `backlog_item_id` (string)
- `supplier_name` (string)
- `quantity` (integer)
- `expected_delivery_date` (string)
- `status` (string, always `"pending"` on creation)
- `created_date` (string)
- `notes` (string or null)

`unit_cost` is stored internally but never returned.

## Example

Request body (modeled on the shape of a `POST` to a typical create endpoint):
```json
{
  "backlog_item_id": "3",
  "supplier_name": "Acme Industrial",
  "quantity": 500,
  "unit_cost": 24.99,
  "expected_delivery_date": "2026-08-01"
}
```

Expected response (conformant — no `unit_cost`):
```json
{
  "id": "PO-1000",
  "backlog_item_id": "3",
  "supplier_name": "Acme Industrial",
  "quantity": 500,
  "expected_delivery_date": "2026-08-01",
  "status": "pending",
  "created_date": "2026-07-10",
  "notes": null
}
```

Error cases (modeled on existing FastAPI error conventions):
- `quantity: 0` → 422 Unprocessable Entity
- `backlog_item_id: "NOPE"` → 404 Not Found
