# Lab 5 — Intervention Log

This log is the executable trace of your debugging loop, not notes written after the fact. As you work each step, drive Claude to run the actual check (read the code, inspect the data, re-run the tests) and capture its real output in the matching section below. Keep this in your worktree as your personal takeaway — do not commit it.

---

## Dependency graph

*(List the four layers, draw the dependency arrows, and note blast radius for each node.)*

---

## Checkpoint placement + defense

*(Where did you place your highest-value checkpoint, and why?)*

---

## Debugging loop (explain / hypothesis / confirm / fix)

**Explain:**

*(What did Claude report — from reading the code — about how FastAPI's `response_model` validates the outgoing payload?)*

**Hypothesis:**

*(Your one-sentence hypothesis — written before accepting Claude's explanation — for why a model change with no route change produces a 500.)*

**Confirm / challenge:**

*(What did Claude find when it actually read `inventory.json` and checked for the `supplier` key? Capture the real result.)*

**Fix:**

*(Which path did you choose — Path A (backfill) or Path B (Optional)? Why?)*

---

## Design decision + defense

*(State your final resolution and the reasoning behind it.)*

---

## Override note

*(One place where you overrode or redirected Claude during this lab. What happened and what did you do?)*
