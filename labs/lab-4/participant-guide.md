# Lab 4: Spec-Driven Development — Write the Contract, Then Build

**Theme 4 | Track 2 (Vibecode) | Time box: 50 minutes**

---

## What you will do

You will take a half-built purchase-orders feature in the inventory-management app and implement it correctly by writing a spec first. The spec is the contract. When Claude's first output violates the contract, you fix the spec (one line), regenerate, and watch the next diff change in exactly the place the spec changed. That moment is the whole point of the lab.

**Capabilities you will practice:**
- The five-element spec (Task / Context / Constraints / Format / Example) as a verifiable contract, not a search query
- Explore → Plan → Code → Commit, grounded in the spec
- The generate-review-iterate loop: when output is wrong, you fix the spec, not the prompt

---

## Before you start

You need:
- The `ryan-roark-caylent/inventory-management-smarsh` fork cloned locally
- Claude Code installed and working
- `uv` installed (backend runs on `uv`)

---

## Step 0: Start clean

Run each command on its own line (do not chain with `&&`):

```
git fetch origin
git checkout -b lab-4-work origin/lab-4-start
```

Start a fresh Claude Code session so the lab-branch `CLAUDE.md` and `specs/spec-template.md` load.

**Success signal:** `specs/spec-template.md` exists in your working tree and the following command prints `lab-4-work`:

```
git branch --show-current
```

---

## Step 1: Survey the half-built feature

Ask Claude to locate everything related to purchase orders in the repo and report what exists versus what is missing. Tell Claude not to fix or change anything yet.

**What Claude should find:**

```
- server/main.py:104  class PurchaseOrder(BaseModel)         # model present
- server/main.py:115  class CreatePurchaseOrderRequest        # model present
- client/src/api.js:97 createPurchaseOrder(...)  -> POST /purchase-orders  (stub, 404s)
- No @app.post("/api/purchase-orders") route exists in server/main.py
```

**Success signal:** Claude confirms the Pydantic models and `api.js` stubs exist but there is no `POST /api/purchase-orders` route (the client stub 404s today).

---

## Step 2: Read the spec template

Open `specs/spec-template.md`. Note its five headings:

1. **Task** — one sentence: what to build
2. **Context** — where it lives, what it touches, what must not change
3. **Constraints** — no new PyPI dependencies, preserve existing GET signatures, acceptance criteria as checkable statements
4. **Format** — exact return shape, JSON keys, status codes
5. **Example** — a concrete input and expected output, modeled on an existing endpoint

---

## Step 3: Write the spec (open-ended judgment step)

Create `specs/purchase-orders.md` by filling in all five elements. Claude can help you phrase elements, but the **decisions are yours**. You must decide and write down, with a one-line defense:

**(a) Where the feature surface lives:** backend route only for the core path, or route plus a Vue modal (extra credit)?

**(b) Which acceptance criteria you enforce:** pick at least two. Examples: unknown `backlog_item_id` returns 404; `quantity` must be a positive integer.

Constraints you must bake in:
- Preserve existing item-CRUD GET signatures (no signature changes)
- No new PyPI dependencies
- Response is JSON
- The Example section must be modeled on the shape of an existing endpoint (copy a `GET /api/backlog` item for the shape)
- Leave the exact response fields for discovery in Step 6 — your spec does not need to name every field the endpoint returns right now

**Success signal:** `specs/purchase-orders.md` exists with all five headings filled and your acceptance criteria written as checkable statements.

---

## Step 4: Explore → Plan (Plan Mode)

Enter Plan Mode and ask Claude to propose an implementation plan for exactly what `specs/purchase-orders.md` describes. Ask it to reference the spec by path.

Before approving the plan, review it against your spec:
- Does every planned change map to a spec line?
- Is anything in the plan *not* in the spec (scope creep)?

**Success signal:** The plan names the file (`server/main.py`), the new route, the validation, and the response shape, and you can point each plan bullet at a spec line.

---

## Step 5: Code → Commit

Approve the plan and let Claude implement the route.

After Claude finishes, read the diff yourself and trace each changed hunk to the spec line it satisfies. Then run the tests:

```
uv run --project server pytest tests/backend/ -v
```

Commit with a message that references the spec. In the commit body, write one line tracing a diff hunk to its spec line.

**Expected test output (before the iterate step):**

```
tests/backend/test_inventory.py::TestInventoryEndpoints::test_get_all_inventory PASSED
...
tests/backend/test_purchase_orders.py::test_create_purchase_order PASSED
========================= 43 passed in 0.60s =========================
```

*(The baseline suite has 40 tests. Adding `test_purchase_orders.py` with 3 tests brings the total to 43.)*

**Success signal:** Tests pass and you can trace every changed line to a spec line.

> **Note on validation error codes:** FastAPI returns **422** (not 400) for a bad request body by default. If your spec says "invalid input returns 400," that mismatch is itself a spec-conformance decision: either add explicit `400` handling in the route or update your spec to accept `422`. This behavior is the same on Windows and macOS.

---

## Step 6: Review-iterate on a conformance violation (the point step)

Ask Claude for the exact JSON the new endpoint returns for a created purchase order.

Check every field against what your spec intended. There is a gap: your spec described the task and validation rules but did not name the exact response fields, so the first-pass implementation returns the full internal model.

**First-pass response (the gap):**

```json
{
  "id": "PO-1000",
  "backlog_item_id": "3",
  "supplier_name": "Acme Industrial",
  "quantity": 500,
  "unit_cost": 24.99,
  "expected_delivery_date": "2026-08-01",
  "status": "pending",
  "created_date": "2026-07-10"
}
```

One field in that response should not be visible to buyers. Do **not** re-prompt Claude to remove it. Instead, **add one line to `specs/purchase-orders.md`** that names the public response fields explicitly, then ask Claude to bring the implementation into line with the updated spec.

**Second-pass response (conformant):**

```json
{
  "id": "PO-1000",
  "backlog_item_id": "3",
  "supplier_name": "Acme Industrial",
  "quantity": 500,
  "expected_delivery_date": "2026-08-01",
  "status": "pending",
  "created_date": "2026-07-10"
}
```

**Success signal:** The second diff touches only the response model or serialization layer. A pytest assertion `assert "unit_cost" not in response.json()` passes. You can trace the change to the spec line you edited.

---

## Step 7: Exit ticket

Name which of the four integration patterns you used:

- Pre-coding Planner
- Mid-coding Pair
- Post-coding Reviewer
- PR Preparer

Write one sentence: which diff hunk traced to which spec line.

**Success signal:** A one-line pattern name plus one diff-to-spec trace, ready to paste into the completion quiz.

---

## Done criteria

You are done with the core path when all four of these are true on your screen:

1. `specs/purchase-orders.md` exists with five elements filled.
2. `POST /api/purchase-orders` returns 201/200 for a valid body and the JSON response omits the internal cost field.
3. `uv run --project server pytest tests/backend/ -v` is green, including a test that asserts the cost field is absent.
4. A commit exists whose message references the spec and whose body includes a one-line diff-to-spec trace.

**Share-back artifact:** your committed `specs/purchase-orders.md` plus the implementing commit on `lab-4-work`, with the trace note in the commit body. This is a real file and a real commit — not a token count.

---

## Extra credit (after core done)

These steps are not required for the completion quiz.

**1. Second conformance criterion.** Add a pytest that posts `quantity: 0` and asserts the server rejects it (422 or your chosen status code). Iterate the spec if the first pass accepts it.

**2. GET route.** Implement `GET /api/purchase-orders/{backlog_item_id}` to back the second `api.js` stub. Spec it first (include what happens when none exists).

**3. Frontend surface (browser).** Build the missing `PurchaseOrderModal.vue` and register it in `Dashboard.vue` so the "Create PO" button works end to end. Launch both servers:

> **Windows:** run `scripts/start.ps1` in PowerShell. When opening the browser with a `claude` command, add `--browser msedge`.
>
> **macOS:** run `scripts/start.sh`. Claude Code opens your default browser automatically — no `--browser` flag needed.

**4. PR Preparer pattern.** Use `git diff --staged` to have Claude draft a PR description that lists the API surface change and links each change to a spec line.

---

## Stuck? Self-service rescue

Work through these in order.

**Rescue A — spec won't come together (stuck before Step 4).**
Ask Claude to read both `specs/spec-template.md` and your draft `specs/purchase-orders.md`, list which of the five elements (Task / Context / Constraints / Format / Example) is missing or vague, and suggest one concrete line for each gap. Ask it not to write code.

**Rescue B — tests are failing after implementation.**
Run `uv run --project server pytest tests/backend/ -v`, copy the first failing assertion, and ask Claude to explain which spec line the current code violates, then propose the smallest fix.

**Rescue C — fully stuck or out of time.**
Check out the reference solution to see the finished contract and code, then read the diff:

```
git stash -u
git fetch origin
git checkout origin/lab-4-solution -- specs/purchase-orders.md
```

Open `specs/purchase-orders.md` and read the reference spec. Then run:

```
git diff origin/lab-4-solution -- server/main.py
```

to see the implementation that traces to it. You still leave the lab having seen a spec-to-conformant-diff.

**Reset everything:** run the `/reset-branch` skill, then redo Step 0.

---

## Quizzes

Your completion and mastery quizzes are in the LMS.

---

## Sources

Authored from the `20-lab-4-design.md` Phase 2 design document (sections 2, 3, 4, 5, 7, 9).

**Date generated:** 2026-07-11
