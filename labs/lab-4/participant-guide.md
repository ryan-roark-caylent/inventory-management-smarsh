# Lab 4: Spec-Driven Development — Write the Contract, Then Build

**Theme 4 | Track 2 (Vibecode) | Time box: 50 minutes**

---

## What you will do

You will take a half-built purchase-orders feature in the inventory-management app and implement it correctly by writing a spec first. The spec is the contract. When Claude's first output violates the contract, you fix the spec (one line), regenerate, and watch the next diff change in exactly the place the spec changed. That moment is the whole point of the lab.

Your spec spans the full path — the backend response shape **and** the UI wiring that surfaces it. You build both halves from that one contract, then run the app and watch the Create PO flow work end to end in the browser. The spec stays the source of truth across the whole stack.

**Capabilities you will practice:**
- The five-element spec (Task / Context / Constraints / Format / Example) as a verifiable contract, not a search query, spanning backend and UI
- Explore → Plan → Code, grounded in the spec
- The generate-review-iterate loop: when output is wrong, you fix the spec, not the prompt

---

## Before you start

Prerequisites and model setup are in the LMS pre-work module (MindTickle). Complete that module first — it walks you through cloning the fork, installing Claude Code, `uv`, and node/npm, and running `npm install` and `uv sync` once. Your completion and mastery quizzes are in the same module. You create your per-lab worktree on this card, in Step 0.

---

## Step 0: Start clean (in your worktree)

You work this lab inside its own git **worktree** so nothing collides with other labs and you keep your work at the end. If your pre-work already created `lab-4-work`, confirm you're in it with `git worktree list`. If not, create it now — run each line separately:

> **Tip:** you can run a shell command without leaving Claude Code by prefixing it with `!` (e.g. `!git worktree list`). Handy throughout the labs.

```
git fetch origin
git worktree add ../lab-4-work lab-4-start
cd ../lab-4-work
```

Then launch Claude Code from inside `lab-4-work`. (The worktree rule is also in this repo's `CLAUDE.md`.)

Start a fresh Claude Code session so the lab-branch `CLAUDE.md` and `specs/spec-template.md` load.

**Confirm your model:** run `/model` and select `sonnet` if you are not already on it. (Smarsh defaults to Haiku; this lab is tuned for Sonnet.)

**Success signal:** `specs/spec-template.md` exists in your working tree and `git worktree list` shows a `lab-4-work` entry with your current directory pointing at it.

---

## Step 1: Survey the half-built feature, then run it and look

Ask Claude to locate everything related to purchase orders in the repo and report what exists versus what is missing. Tell Claude not to fix or change anything yet.

**What Claude should find:**

```
- server/main.py  class PurchaseOrder(BaseModel)         # model present
- server/main.py  class CreatePurchaseOrderRequest        # model present
- client/src/api.js  createPurchaseOrder(...)  -> POST /purchase-orders  (stub, 404s)
- No @app.post("/api/purchase-orders") route exists in server/main.py
```

**Run it and look.** Ask Claude to start the app (it has a `/start` command), or run it yourself:
- Windows: `scripts/start.ps1`; macOS: `scripts/start.sh` (either boots both servers).

Open the dashboard at `http://localhost:3000`, find a backlog item, and click **Create PO**. Nothing opens. Open your browser dev tools (Console) and you will see Vue fail to resolve a `PurchaseOrderModal` component — the frontend half of this feature was never finished (the modal is referenced but never built or imported). As your survey found, the backend half is missing too: there is no `POST /api/purchase-orders` route. This lab closes **both** gaps: you spec and build the backend route **and** the UI wiring, so by the end **Create PO** works end to end in the browser.

**Success signal:** Claude's survey reports the models and `api.js` stub exist but there is no `POST /api/purchase-orders` route, AND you saw **Create PO** fail in the running app (the modal never opens; the Console shows Vue failing to resolve the `PurchaseOrderModal` component).

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

Create `specs/purchase-orders.md` by filling in all five elements. This spec is **end to end**: it describes the backend route **and** the UI wiring that surfaces it, so you build the whole feature from one contract. Claude can help you phrase elements, but the **decisions are yours**. You decide:

**(a) The backend surface:** the `POST /api/purchase-orders` route — what it accepts and (in part) what it returns.

**(b) The UI surface:** how the feature reaches the browser — the create-PO modal (`PurchaseOrderModal.vue`) and how it gets wired into `Dashboard.vue` so the **Create PO** button opens it and a submit calls your new route. Describe the wiring in the spec (which component, which parent, which handler / API call), not the exact Vue syntax — that is Claude's job to implement from your contract.

**(c) Which acceptance criteria you enforce:** pick at least two. Examples: unknown `backlog_item_id` returns 404; `quantity` must be a positive integer.

Constraints you must bake in:
- Preserve existing item-CRUD GET signatures (no signature changes)
- No new PyPI dependencies
- Response is JSON
- The Example section must be modeled on the shape of an existing endpoint (copy a `GET /api/backlog` item for the shape)
- Leave the exact response fields for discovery in Step 6 — your spec does not need to name every field the endpoint returns right now

> **Note:** The template's **Format** heading says "exact return shape, JSON keys, status codes," but you can leave your Format section **partial on purpose** here. Naming every response field is exactly what Step 6 is for. Spec what you have decided; leave the response-field list open. A spec is allowed to mark what is still to be discovered.

**Success signal:** `specs/purchase-orders.md` exists with all five headings filled, describes both the backend route and the UI wiring, and your acceptance criteria are written as checkable statements.

---

## Step 4: Explore → Plan (Plan Mode)

Enter Plan Mode and ask Claude to propose an implementation plan for exactly what `specs/purchase-orders.md` describes. Ask it to reference the spec by path.

> **How to enter Plan Mode:** press **shift-tab** to cycle into Plan Mode; shift-tab again to exit.

Before approving the plan, review it against your spec:
- Does every planned change map to a spec line?
- Is anything in the plan *not* in the spec (scope creep)?

> **Pro tip (optional):** for a change like this, some people **plan on Opus** (deeper reasoning for the plan), then switch with `/model sonnet` to **execute** the approved plan. Use the stronger model where the thinking is hardest, the faster one to carry it out. Not required for this lab.

**Success signal:** The plan names the backend file (`server/main.py`), the new route, the validation, and the response shape, **and** the UI pieces (`PurchaseOrderModal.vue` plus its wiring into `Dashboard.vue`) — and you can point each plan bullet at a spec line.

---

## Step 5: Code the backend, then run it and look

Approve the plan and let Claude implement the backend route first. (You build the UI half in Step 7, once the response shape is conformant.)

After Claude finishes, read the diff yourself and trace each changed hunk to the spec line it satisfies. Then run the tests:

```
uv run --project server pytest tests/backend/ -v
```

**Run it and look.** With the app still running, hit your new endpoint live — open the API docs at `http://localhost:8001/docs` (FastAPI Swagger) and POST a purchase order, or watch the Network tab. See the real JSON come back. Note what is in it — you will use that in Step 6.

**Expected test result:** the backend suite is green, including a new test in `test_purchase_orders.py`.

Keep your `specs/purchase-orders.md` and the implementing change in your worktree as your **local takeaway** — no commit needed. Jot your one diff→spec trace in a scratch note; you will reuse it in the exit ticket.

**Success signal:** tests pass, you can trace every changed line to a spec line, and you saw the live endpoint return its JSON.

> **Note on validation error codes:** FastAPI returns **422** (not 400) for a bad request body by default. If your spec says "invalid input returns 400," that mismatch is itself a spec-conformance decision: either add explicit `400` handling in the route or update your spec to accept `422`.

---

## Step 6: Review-iterate on a conformance violation (the point step)

Ask Claude for the exact JSON the endpoint returns for a created PO (or reuse what you saw in Step 5). Check it against your spec. There is a gap: your spec set the task and validation rules but never named the **public** response fields, so the endpoint returns the full internal model, including **`unit_cost`**. That field is **internal-only**: it is your cost and margin, and buyers placing an order should never see it.

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
  "created_date": "2026-07-10",
  "notes": null
}
```

*The `PO-1000` id is illustrative (the reference implementation uses `1000 + count of existing POs`); your spec does not need to mandate this exact format.*

**Fix it the spec-driven way:** add **one line** to `specs/purchase-orders.md` naming the public response fields (everything except `unit_cost`), then ask Claude to bring the endpoint's response into line with the updated spec. You are still driving Claude — through the contract, not a patch. The point is to fix the **spec**, not to hand-patch the symptom.

**Second-pass response (conformant):**

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

**Success signal:** the second diff touches only the response model or serialization layer, `unit_cost` is gone, a pytest assertion `assert "unit_cost" not in response.json()` passes, and you can trace the change to the spec line you edited.

---

## Step 7: Build the UI from the spec, then run it and see it work

The backend is conformant. Now build the other half of your contract. Ask Claude to implement the UI wiring your spec describes: create the missing `PurchaseOrderModal.vue` and register it in `Dashboard.vue` so the **Create PO** button opens the modal and its submit calls `POST /api/purchase-orders`. Point Claude at the spec by path — same contract-first move, now on the frontend.

Review the diff against your spec the same way you did for the backend: every changed hunk should trace to a UI line in `specs/purchase-orders.md`; anything extra is scope creep.

**Run it and look.** Ask Claude to start the app (it has a `/start` command), or launch both servers yourself: Windows `scripts/start.ps1`; macOS `scripts/start.sh`. On Windows, if you open the browser with a `claude` command, add `--browser msedge`; on macOS Claude Code opens your default browser. Open `http://localhost:3000`, click **Create PO** on a backlog item — this time the modal opens. Fill it in, submit, and watch the PO get created through your new route. The Console warning from Step 1 is gone.

**Success signal:** the **Create PO** button opens the modal in the running app, submitting it creates a PO through `POST /api/purchase-orders`, no `PurchaseOrderModal` resolve warning in the Console, and every UI diff hunk traces to a spec line.

---

## Step 8: Exit ticket

Write one sentence tracing one diff hunk to the spec line it satisfies — pick either half (for example, "the response-model change traces to the public-fields line I added in Step 6," or "the modal-wiring change traces to the UI-surface line in my spec"). Keep this trace note with your spec in your worktree — it is your takeaway.

**Success signal:** one diff-to-spec trace you can point to, backed by the working Create PO flow on your screen.

---

## Done criteria

You are done with the core path when all five of these are true on your screen:

1. `specs/purchase-orders.md` exists with five elements filled, covering **both** the backend route and the UI wiring.
2. `POST /api/purchase-orders` returns 200 for a valid body and the JSON response omits the internal cost field.
3. `uv run --project server pytest tests/backend/ -v` is green, including a test that asserts the cost field is absent.
4. In the running app, the **Create PO** button opens the modal and a submit creates a PO through your new route — no `PurchaseOrderModal` resolve warning in the Console.
5. You have a one-line diff-to-spec trace note kept with your spec in your worktree.

The point stays the same: the spec is the source of truth. It now spans the full stack, so both halves — backend response and UI wiring — trace back to lines you wrote in the contract.

**Local takeaway:** your `specs/purchase-orders.md`, the implementing change, and the trace note, all kept in your Lab 4 worktree. No commit needed — this is your personal artifact, not a share-back.

---

## Extra credit (after core done)

These steps are not required for the completion quiz.

**1. Second conformance criterion.** Add a pytest that posts `quantity: 0` and asserts the server rejects it (422 or your chosen status code). Iterate the spec if the first pass accepts it.

**2. GET route.** Implement `GET /api/purchase-orders/{backlog_item_id}` to back the second `api.js` stub. Spec it first (include what happens when none exists).

**3. Draft a PR description.** Use `git diff` to have Claude draft a PR description that lists the API surface change and the UI wiring, linking each change to a spec line.

---

## Stuck? Self-service rescue

Work through these in order.

**Rescue A — spec won't come together (stuck before Step 4).**
Ask Claude to read both `specs/spec-template.md` and your draft `specs/purchase-orders.md`, list which of the five elements (Task / Context / Constraints / Format / Example) is missing or vague, and suggest one concrete line for each gap. Ask it not to write code.

**Rescue B — tests are failing after implementation.**
Run `uv run --project server pytest tests/backend/ -v`, copy the first failing assertion, and ask Claude to explain which spec line the current code violates, then propose the smallest fix.

**Rescue C — fully stuck or out of time.**
First confirm your remote points at the fork: run `git remote -v` and check that `origin` is the `inventory-management-smarsh` fork. If it points at your own local clone, `origin/lab-4-solution` will not resolve. Then check out the reference contract and read the diff:

```
git fetch origin
git checkout origin/lab-4-solution -- specs/purchase-orders.md
```

Open `specs/purchase-orders.md` and read the reference spec. Then run:

```
git diff origin/lab-4-solution -- server/main.py client/src
```

to see the backend route and the UI wiring that trace to it. You still leave the lab having seen a spec-to-conformant-diff across the full stack.

**Reset everything:** run the `/reset-branch` **command**, then redo Step 0. **Warning:** `/reset-branch` runs `git branch -D` + `git reset --hard` + `git clean -fd` with **no confirmation** — it permanently deletes uncommitted work. Because you are working in a per-lab worktree, you should not need it for hygiene between labs; keep it only for a hard reset of *this* lab.

---

## Quizzes

Your completion and mastery quizzes are in the LMS (MindTickle) pre-work module.
