# Lab 3 — Spec, Clear, Implement (Gated Loop with Plan Mode)

**Module 03 — Specifying** | 20 min | Solo (one person, one machine, one session)

> **Thesis:** Specification and verification are the uniquely human jobs. A spec on disk outlives any conversation, so a fresh session plus one markdown file beats a long polluted one.

Budgets total 18:00; you have 2:00 of slack.

---

## Step 0 — Setup (off the clock)

Run `/reset-branch` if you are still on a previous lab's branch. Then type these two commands yourself (the branch ritual is the deliberate human-typed exception to the tell-Claude rule — it controls the environment Claude runs in):

```
git fetch origin
```

```
git checkout -b lab-3-work origin/lab-3-start
```

Run `/start` and confirm http://localhost:3000 loads. Ignore the `GET /api/tasks` 404s in the browser console; they are planted, not breakage.

---

## Step 1 — Orient (1:30)

Open http://localhost:3000, scroll the Dashboard to the Backlog section, and click the "Electric Motor 5HP" row. The Inventory Shortage Details modal opens. Observe: the footer has only a Close button. There is no way to create a purchase order, even though the backend already computes a `has_purchase_order` flag for every backlog item.

The feature is half-built on purpose: Pydantic models exist (`server/main.py`), client API methods exist (`client/src/api.js`), routes and UI do not. Your job in this lab is to write the spec that describes exactly what needs to be built — then implement it in a completely fresh session.

---

## Step 2 — Plan mode: draft the spec (4:00)

In Claude Code, press Shift+Tab twice until the status line reads **plan mode**. Paste exactly:

```
Draft a spec for completing the half-built Purchase Orders feature. The spec will live at specs/purchase-orders.md and must follow the section structure in specs/spec-template.md. Scope: POST /api/purchase-orders and GET /api/purchase-orders/{backlog_item_id} in server/main.py (Pydantic models already exist at main.py:104-121, client methods at client/src/api.js:97-105), plus a "Create Purchase Order" button in client/src/components/BacklogDetailModal.vue and a backlog refresh in Dashboard.vue when a PO is created. UI work is confined to those two existing files; do not propose creating any new Vue component files (a PurchaseOrderModal component was deliberately removed from this codebase and is out of scope). The spec is markdown only, no implementation code. Your plan must consist of exactly one action: creating specs/purchase-orders.md with the full spec content.
```

Observe: Claude reads the relevant files, then presents a plan whose body is the proposed spec. Nothing has been written yet — plan mode is read-only. That is the trust layer: you see the plan before Claude acts.

---

## Step 3 — Human gate: checklist review (3:30)

Do NOT approve yet. The facilitator will paste the Spec Review Checklist into meeting chat at the start of this step. Check the proposed spec against all 7 items. Keep the checklist in the chat window or a scratch note outside the repo.

If an item fails, paste the corrective prompt listed next to that item (still in plan mode). Iterate **at most twice**, then move on even if one minor item is imperfect. Two rounds is the budget; this gate is yours to run.

---

## Step 4 — Approve, read the diff, /clear (1:30)

Approve the plan. Choose the option that lets you review each edit — do not enable auto-accept. Claude writes one file: `specs/purchase-orders.md`. Confirm its content matches what you approved and that no other file was touched.

Then type:

```
/clear
```

The whole research conversation is now noise. Models perform better with less context, and everything that matters survived in the spec file on disk.

---

## Step 5 — Implement from the spec (6:00) — THE POINT

In the now-empty session, paste exactly:

```
Implement @specs/purchase-orders.md exactly as written. Do not use the Task tool or any subagents; edit the files directly in this session. Make no changes beyond what the spec describes.
```

(The repo's CLAUDE.md mandates a vue-expert subagent for .vue edits; this prompt overrides it to keep the lab inside 20 minutes. Lab 4 is where subagents get their turn.)

Observe: Claude reads the spec and edits three files (`server/main.py`, `client/src/components/BacklogDetailModal.vue`, `client/src/views/Dashboard.vue`). Read each diff before accepting:

- Confirm each edit traces to a line in your approved spec. If you cannot point at the spec line that asked for a change, flag it — ask Claude to justify or remove it.
- Confirm the diff stays inside the spec's boundaries: no files beyond the ones the spec names, no rework of existing code the spec never mentions.
- Keep the chat-posted Spec Review Checklist open and read the diff against it. The same items you gated the spec on are the items the implementation must honor.

Accept each edit after reading it.

**Recovery moves (use any time):** if implementation drifts mid-stream, press Esc to interrupt, then either correct course in one sentence or `/clear` and re-paste the Step 5 prompt. The spec survives the session.

> **Aha moment:** the spec outlived the conversation. You threw away the entire chat and the feature still got built, because the artifact that mattered was on disk, not in the context window.

---

## Step 6 — Verify (1:30)

New routes need a backend restart (uvicorn runs without reload). **Run `/start` again before verifying — this is the most common failure point.**

1. Refresh http://localhost:3000, open the "Electric Motor 5HP" backlog row, click "Create Purchase Order". Observe the modal shift to its created state. Close the modal, reopen the same row: the footer shows the created state instead of the Create button (driven by the refreshed `has_purchase_order` flag).

2. Ask Claude to verify the API. Paste exactly:

```
Verify the new endpoint: call GET http://localhost:8001/api/purchase-orders/2 against the running backend and show me the status code and response body.
```

Observe a 200 with your PO's JSON in Claude's reply.

---

## Done Criteria

You are done when you can check off any **two** of:

- [ ] The shortage modal shows the post-creation state, or Claude's Step 6 verification reports a 200 from `GET /api/purchase-orders/2`.
- [ ] `specs/purchase-orders.md` exists (open in an editor or listed by `git status`).
- [ ] A multi-file diff (`main.py` + `BacklogDetailModal.vue` + `Dashboard.vue`) accepted in the Claude Code transcript.

**Minimum artifact (nobody leaves empty-handed):** `specs/purchase-orders.md` exists and passed the chat-posted checklist. A participant who never reaches Step 5 still has a reviewed, approved spec.

**Optional chat signal** (doubles as the facilitator's completion read): paste ONE line into meeting chat — the 200 status line from the Step 6 verification, or your three-file diffstat.

---

## Extra Credit

**1. Commit it (Lab 1 callback).** Ask Claude: `Commit this work with a clear message. Do not push.` Read the message before approving. Local commit only.

**2. Persistence drill.** Run `/start` to restart the servers, then re-paste the Step 6 verification prompt to Claude. The PO is gone (404). Find the section of your spec that predicted this. If your spec has no persistence section, the checklist caught a real gap.

**3. Spec amendment flow.** Add one line to `specs/purchase-orders.md` yourself in an editor: a `GET /api/purchase-orders` route returning all POs. Then prompt: `The spec changed. Implement only the new GET /api/purchase-orders list route described in @specs/purchase-orders.md.` Specs are living documents; amendments beat re-explaining.

**4. Install a shared skill (bonus).** Kris and Kyle have built spec-driven-development skills for Claude Code. If they share the skill files during the workshop (via chat or download), you can install them without any repo changes. Ask Claude:

```
I have a skill file to install. What directory should I put it in, and how do I verify it loaded?
```

Once loaded, ask Claude to list the available skills and explain what each one does. Then re-run this lab's feature through their workflow and compare the output to your `specs/purchase-orders.md`. The same human gate applies: review everything before approving.

---

## Stuck Path

| If this happens | Try this |
|---|---|
| Can't enter plan mode or wrong mode | Shift+Tab cycles modes; the status line must read "plan mode" before Step 2. If unsure, paste the status-line text into chat or screen-share in the TA breakout. |
| Claude proposes code or multi-file actions in the plan | Paste: `Revise the plan: it must contain exactly one action, creating specs/purchase-orders.md. Markdown spec only, no implementation code.` |
| Spec still failing checklist after 2 iterations | Stop iterating. Post "stuck at the gate" in meeting chat — the TA will send the rescue command. |
| Plan approval triggered implementation immediately | Esc to interrupt. The spec file is untracked and survives. `/clear`, then resume at Step 5. |
| Claude spawns the vue-expert subagent anyway | Esc, paste: `Stop. Do not use the Task tool. Edit the files directly in this session.` |
| Implementation drifts from the spec or runs long | Esc, `/clear`, re-paste the Step 5 prompt verbatim. The spec survives; the conversation is disposable. |
| New endpoint returns 404 during verify | **Backend was not restarted.** Run `/start`. |
| Servers won't start or ports are stuck | `/start` kills ports 3000/8001 first. If it still fails, post in chat — the TA will send the manual start commands. |
| Everything is broken | `/reset-branch`, then post in chat — the TA will send the rescue command. |
