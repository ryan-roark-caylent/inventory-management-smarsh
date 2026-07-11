# Lab 5 — Completion Quiz

Answer each question based on what you observed during the lab.

---

**Q1.** After you added the required `supplier` field to `InventoryItem` and ran pytest before changing anything else, what did the suite report?

- A) 11 tests failed with `ResponseValidationError`; `supplier` was missing from every serialized record
- B) All tests passed because FastAPI silently drops model fields not present in the underlying data source
- C) `test_get_all_inventory` raised a `404` after the route's `response_model` registration failed on startup
- D) The backend raised an `ImportError` on startup from `mock_data`, preventing any tests from executing

---

**Q2.** The route function for `GET /api/inventory` — what did you have to change in it to expose `supplier` in the response?

- A) Nothing — once model and data agreed, `response_model` serialized the field automatically
- B) Add `supplier` as a named query parameter in the route signature alongside `warehouse` and `category`
- C) Add a `supplier` branch inside `apply_filters` so the field passes through to the serialized response
- D) Write a separate endpoint that joins supplier records with the inventory list before responding to the client

---

**Q3.** What is the key difference between the Path A and Path B resolutions for the missing `supplier` field?

- A) Path A backfills every data record with a real value; Path B relaxes the field to `Optional[str] = None`
- B) Path A auto-generates supplier names from the item SKU; Path B prompts the user on first view of the detail modal
- C) Path A updates only the Pydantic model's default value; Path B updates both the model and every JSON data record
- D) Path A and Path B produce the same runtime result; both yield `supplier: null` until a user manually enters a value

---

**Q4.** You placed your highest-value checkpoint after the model change and before the fan-out. Why there specifically?

- A) A broken model cascades to data, route, and Vue — catching it early limits blast radius
- B) It is the cheapest checkpoint because the frontend build has not been started yet at this step
- C) Checkpoints must always follow the final change; the model change happens to be that last step
- D) The model change is effectively read-only in this step, so verifying early carries negligible blast radius

---

**Q5.** Why did you use `/clear` (not `/compact`) before the Reports.vue task?

- A) Multi-file context is noise for an unrelated task; `/clear` drops it, `/compact` retains it
- B) `/compact` cannot run twice in a session, leaving `/clear` as the only remaining available option
- C) `/clear` preserves the supplier conclusions in context; `/compact` would have discarded them entirely
- D) Reports.vue is a separate concern, and `/clear` is required whenever switching between feature domains
