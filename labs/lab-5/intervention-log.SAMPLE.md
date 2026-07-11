# Lab 5 — Intervention Log (Reference Sample)

This is the facilitator reference log. It documents both acceptable resolutions (Path A and Path B) so champions can verify participant reasoning regardless of which path was chosen.

---

## Dependency graph

Four layers, ordered by dependency (root to leaf):

1. **`InventoryItem` Pydantic model** (`server/main.py`) — root node. Blast radius: HIGH. Every layer below depends on this contract. A required field here cascades immediately to the data, the route serialization, and any UI that renders the field. Not easily recoverable mid-fan-out.

2. **`server/data/inventory.json`** — data source. Blast radius: MEDIUM. Must satisfy the model contract. If the model requires `supplier`, every record needs it. The fix is mechanical but touches every record.

3. **`GET /api/inventory` route** — serialization point. Blast radius: LOW for this change. `response_model=List[InventoryItem]` auto-serializes any field on the model. No route code change needed once model and data agree.

4. **`InventoryDetailModal.vue`** — display layer. Blast radius: LOW. Reads from the API payload. Once the API contract holds, adding the display row is isolated frontend work.

Dependency arrows: `InventoryDetailModal.vue` → `GET /api/inventory` → `InventoryItem` ← `inventory.json`

---

## Checkpoint placement + defense

**Placement:** After the model change (Step 2), before touching data, route, or Vue.

**Defense:** The model is the root node. If the required field breaks serialization, every downstream layer is building on a broken foundation. Catching the break here costs one pytest run. Catching it after the fan-out means untangling which of four changed layers introduced the failure.

---

## Debugging loop (explain / hypothesis / confirm / fix)

**Explain:**

FastAPI's `response_model` parameter on a route tells FastAPI to validate the outgoing response against the specified Pydantic model before sending it to the client. If a required field is present in the model but absent from the returned data, FastAPI raises a `ResponseValidationError`, which produces an HTTP 500. The validation happens inside `client.get()` in pytest — the assertion line is never reached.

**Hypothesis (written before accepting Claude's answer):**

"FastAPI validates the outgoing payload against `response_model`. Because `supplier` is required in `InventoryItem` but absent from the JSON records, serialization fails and raises a 500 on every `GET /api/inventory` call."

**Confirm / challenge:**

Asked Claude to read `server/data/inventory.json` and report whether any record contains a `supplier` key. Claude confirmed: no record has a `supplier` key. This matches the hypothesis — the data gap is the proximate cause.

**Fix:**

Two valid paths:

- **Path A (reference answer — backfill):** Add a realistic `supplier` string to every record in `inventory.json`. The model's `required` contract is honored. Every item has a real supplier. Downside: requires touching all 32 records; no tolerance for legacy data without a supplier.

- **Path B (also acceptable — Optional):** Change `InventoryItem.supplier` to `Optional[str] = None`. The 500 resolves because the field is no longer required. Downside: weakens the business rule — items can have no supplier indefinitely.

**Grading signal:** The path chosen is less important than whether the written hypothesis correctly names the `response_model` / data contract mismatch and whether the defense is consistent with the path taken.

---

## Design decision + defense

**Path A (reference):** Backfill every record in `inventory.json` with a plausible supplier string. The business rule — "every item must name a supplier" — is worth maintaining as a hard constraint. Legacy records without a supplier indicate missing data, not a tolerable state.

**Path B (also acceptable):** Relax to `Optional[str] = None`. Appropriate when the data migration is out of scope or when the codebase must remain backward-compatible with existing records that legitimately have no supplier. The UI falls back to a dash (`—`) for nulls, so the display degrades gracefully.

---

## Override note

**Example (Path A):** After Step 2 — adding the required field — Claude offered to also update `inventory.json` and the Vue modal in the same response. I redirected: "Stop after the model change. I want to run the checkpoint first." This preserved the point step: seeing the cascade failure before any downstream layer was touched.

**Example (Path B):** Claude suggested adding a `default=""` to the field rather than `Optional[str] = None`. I overrode: an empty string is not the same as an absent value; `Optional` with `None` is the correct signal that the field is intentionally nullable.
