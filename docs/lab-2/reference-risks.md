# Reference risks — AEP-142 low-stock alerting

This file is the facilitator answer key for Move 2 (critique-not-approval).
It shows the shape of critique Claude should produce when asked the sharp
question. A participant's own output need not match this verbatim; what
matters is that it names concrete failure conditions, not restated praise.

---

## Two weaknesses

**Weakness 1 — stale in-memory snapshot.**
The `inventory_items` list is populated once at import time from
`server/data/inventory.json` via `mock_data.py`. No mechanism refreshes it
while the process runs. In a real deployment any physical stock movement
(receiving, picking, spoilage) would not be reflected in alert output until
the process restarts. Ops could act on data that is hours or days old.

**Weakness 2 — missing-category silent skip.**
The spec proposes a per-category threshold dict. If a category key is absent,
the code falls back to `item.reorder_point`. That fallback is reasonable, but
the spec does not address a category string that appears in live data but was
not configured and whose `reorder_point` happens to be zero. That item would
perpetually appear as low-stock (0 <= 0 is true), which is noise, not signal.

---

## One likely failure mode

**A category key typo silently falls back to `reorder_point`.**
If the threshold dict contains `"Sensor"` but the data record says
`"Sensors"`, the lookup misses and falls back silently. No error, no log
entry. Ops sees alerts driven by the item's own `reorder_point` and has no
way to know the per-category threshold is not in effect. The result is a
false-confidence signal for that entire category.

---

## Two alternative designs with tradeoffs

**Alternative A — compute alerts on write (event-driven).**
Each time stock is updated, recompute which items cross their threshold and
cache the result. Eliminates the stale-snapshot problem entirely and makes
`GET /api/inventory/low-stock` a cheap cache read.
Tradeoff: requires write endpoints that do not yet exist. The current backend
is GET-only; adding writes is Lab 4 scope, not this sprint.

**Alternative B — separate thresholds config resource.**
Add `GET /api/config/thresholds` and `PUT /api/config/thresholds` so ops can
update thresholds at runtime without a redeploy.
Tradeoff: one more endpoint to document, version, and secure. For Phase 1 a
hardcoded default with a read-only config endpoint is adequate; the write
half is Phase 2 scope once ops confirms what thresholds they need.

---

## Forward-looking note

A concurrent-write race is not a current failure mode. This backend is
read-only; there are no stock writes. If write endpoints are added in a later
phase, race conditions between a write and a low-stock read become relevant
and should be addressed at that time.
