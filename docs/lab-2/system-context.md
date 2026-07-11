# System context for AEP-142

**Stack:** Vue 3 + Vite frontend (`client/`), Python FastAPI backend (`server/`),
in-memory JSON data (no database). All list endpoints are GET-only today.

**Inventory model:** `InventoryItem` has `quantity_on_hand`, `reorder_point`,
`category`, `warehouse`. Categories in the data: Actuators, Circuit Boards,
Controllers, Power Supplies, Sensors.

**Shared dependency:** the `/api/inventory` response is consumed by two other
internal services besides this dashboard. Any change to its shape is a
backward-compatibility decision, not a local one.

**Spec format:** follow `specs/spec-template.md`.
