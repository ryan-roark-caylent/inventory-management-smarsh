# Lab 8 — Output Quality, Code Review, and Responsible Use

**Theme:** Output Quality / Code Review / Responsible Use
**Track:** AI Teammate (Track 3)
**Time box:** 55 minutes (core done at ~40 min; Extra Credit after)

---

## What this lab proves

AI-generated code is untrustworthy in the same way unreviewed human code is. You own the trust call. A subagent is an input to your review, not an authority, and its silence on any issue is not a clean bill of health.

---

## The aha moment

At the point step (Step 4), you will dispatch a read-only `code-reviewer` subagent on the same file you already reviewed by hand. Its finding set will differ from yours in some way: it may surface issues you did not catch, miss ones you did, or raise something orthogonal. Any gap is yours to own. The moment you notice the lists diverge is the moment code review stops being "run the agent and merge."

---

## Before you begin

Make sure you have:
- `uv` installed
- Node 18+ installed
- Python 3.11+ available
- A GitHub account with access to the fork

---

## Steps

### Step 0 — Start clean

Run these commands one at a time:

```
git fetch origin
```

```
git checkout -b lab-8-work origin/lab-8-start
```

Start a fresh Claude Code session so the lab-branch `CLAUDE.md` loads.

**Windows:** open a new terminal, navigate to the repo, and run `claude` to start the session.
**macOS:** open a new terminal, navigate to the repo, and run `claude` to start the session.

**Success signal:** `server/inventory_ops.py` and `docs/lab-8/scenario-cards.md` exist in the repo, and `git branch --show-current` prints `lab-8-work`.

---

### Step 1 — Read the generated function (do NOT run it)

Open `server/inventory_ops.py`. This is AI-generated code that landed in a PR. Read it top to bottom before doing anything else.

You will see a function that imports a package, logs some information, looks up a record, and returns a fulfillment decision.

**Success signal:** you can state in one sentence what the function is supposed to do (decide whether a backlog item can be fulfilled from available stock).

**Expected output — what you are reading:**

```python
from acme_inventory_sdk import optimize_stock   # unrecognised import

def do_inv(backlog_id, user_email):
    logger.info(f"Processing fulfillment for user {user_email}")
    item = _lookup(backlog_id)
    needed, available = item["quantity_needed"], item["quantity_available"]
    fulfillable = available > needed
    return {"fulfillable": fulfillable, "reorder": optimize_stock(item)}
```

*(Abridged for the card. Open the actual file in the repo for the full version.)*

---

### Step 2 — Run the 5-point checklist by reading (open-ended judgment)

Walk the function against each of the five review dimensions and write your findings into a new file `review-findings.md`. There are **four** planted defects — one per line of the checklist except one dimension is clean.

The five dimensions: **correctness, style adherence, edge cases, hallucination, security.**

For each finding, write:
- The line number
- The dimension
- Your **Trust Spectrum verdict** (accept / modify / reject)
- The **standard or named risk** you cite for that verdict

You must also **author one `CLAUDE.md` rule** that would have stopped the style defect at generation time, and write **one sentence on who owns the quality decision** (not the AI, not the subagent, you).

You may ask Claude to help find issues, but the verdicts and the `CLAUDE.md` rule are your calls.

**Success signal:** `review-findings.md` names four issues with a verdict and cited standard for each, plus your authored `CLAUDE.md` rule and your ownership sentence.

---

### Step 3 — Make it run, then catch the off-by-one with a test

The module will not import because of a hallucinated dependency. Neutralise that line (remove or stub the import). This is your "reject" action on the hallucination.

Next, extract the comparison logic as a standalone helper function `stock_is_sufficient(available, needed)` so you can test it in isolation. Write a pytest that calls `stock_is_sufficient(850, 850)` and asserts `True`.

Run the test:

```
uv run --project server pytest tests/backend/ -v
```

Watch it fail. Then make the one-character boundary fix. Run again and confirm green.

**Expected output — the import error before you neutralise it:**

```
E   ModuleNotFoundError: No module named 'acme_inventory_sdk'
```

*(This is the point of "read, don't run": a happy-path smoke test never gets far enough to reveal the boundary bug, and the confident-looking call is pure hallucination.)*

**Expected output — your test failing, then passing after the boundary fix:**

```
tests/backend/test_inventory_ops.py::test_equal_stock_is_fulfillable FAILED
    assert False is True        # available == needed wrongly reported unfulfillable
...
tests/backend/test_inventory_ops.py::test_equal_stock_is_fulfillable PASSED
========================= 37 passed in 0.6s =========================
```

**Success signal:** your new test failed on the planted code and passes after the one-character fix; the suite is green.

---

### Step 4 — Dispatch the code-reviewer subagent and compare (point step)

Ask Claude to use the `code-reviewer` subagent (which is read-only: it can only use Read, Grep, and Glob) to review `server/inventory_ops.py`. Read its report.

Then, in `review-findings.md`, add a "human vs subagent" section noting:
- Which of your four issues the subagent also caught
- Which it missed
- Anything it raised that you did not

Confirm your Trust Spectrum verdict for each issue now that you have two opinions. State the ownership conclusion explicitly: any gap is yours to own, not the subagent's to clear.

**Expected output — a representative subagent report (your actual run will vary):**

```
CRITICAL  Correctness — `available > needed` is an off-by-one; equal stock is fulfillable. Use >=.
MEDIUM    Naming — `do_inv` is non-descriptive; prefer check_backlog_fulfillment.
INFO      Missing return-type annotations on _lookup and do_inv; add type hints per PEP 484.
```

The specific findings the subagent raises are non-deterministic. The subagent has no shell access and cannot verify that a package does not exist. Its silence on any issue is not exoneration.

**Success signal:** `review-findings.md` has a "human vs subagent" section showing both finding sets, at least one difference noted, and every issue has a final verdict, cited standard, and the ownership conclusion stated.

---

### Step 5 — Work the responsible-use scenario cards

Open `docs/lab-8/scenario-cards.md`. For each of the five cards, classify it as **acceptable / needs modification / never acceptable** and cite the rule. Then classify the repo's real `allow_origins=["*"]` setting in `server/main.py` (around line 52).

**Success signal:** five classifications plus the CORS call, each with a one-line cited justification.

---

### Step 6 — MCP round-trip: file a sanitized review ticket

Use the GitHub MCP to open an issue on the fork titled `Code review: server/inventory_ops.py`. The body should list your four findings by line and dimension.

**Responsible-use constraint:** reference the PII log line by line number, do not paste the email value. Do not paste any secret into the issue body. Permanent tickets are public records.

**Windows note:** the GitHub MCP must be configured at project scope in `.mcp.json` (not user-global). Relaunch Claude Code after editing `.mcp.json` before the MCP tools appear.
**macOS note:** same requirement — project scope, quit and reopen Claude Code after saving `.mcp.json`.

**Expected output — a sanitized issue body (correct) vs an unsafe one (wrong):**

```
GOOD:  "L4 logs a user email (PII) — see server/inventory_ops.py:4. Redact before logging."
BAD:   "L4 logs rohan.mehta@smarsh.com"   <-- pastes the PII value into a permanent ticket
```

**Rescue/fallback (if MCP is unavailable):**

Run this command (each flag on its own line if your shell requires it):

```
gh issue create --title "Code review: server/inventory_ops.py" --body-file review-findings.md
```

If `gh` is not authenticated, keep `review-findings.md` as your artifact. Core done does not depend on the ticket landing remotely.

**Success signal:** an issue URL, a `gh` confirmation, or the committed `review-findings.md`.

---

### Step 7 — Exit ticket

Name the one issue you **rejected** (not just modified) and the standard or risk you cited. Write it in one line, ready to paste into the completion quiz.

**Success signal:** one rejected issue and one cited standard.

---

## Extra Credit

These steps are not required for core done or the completion quiz. Work them if you finish early.

1. **Second reviewer.** Dispatch the `security-auditor` subagent on the same file and diff its findings against the `code-reviewer` report. Note where a security-focused agent surfaces the PII/log issue that the general reviewer missed.
2. **Fix the real CORS wildcard.** Change `allow_origins=["*"]` in `server/main.py` to an explicit localhost list, run the suite, and write one line on why the wildcard would fail a deployment review.
3. **Rewrite a tautological test.** Find or generate an `assert result is not None` test and rewrite it to assert the computed value.
4. **Jira instead of GitHub.** File the same sanitized findings as a Jira issue via the Jira MCP. Note which permission scope each round-trip needed (read vs create).

---

## Done criteria

Your core path is complete when all four of these are true:

1. `review-findings.md` exists with four issues, each carrying a Trust Spectrum verdict and a cited standard, plus your authored `CLAUDE.md` rule, your ownership sentence, and the human-vs-subagent diff.
2. `tests/backend/test_inventory_ops.py` failed on the planted code and passes after the fix; the suite is green.
3. Five scenario cards plus the CORS wildcard are classified with cited justifications.
4. A sanitized review ticket exists (GitHub issue URL, `gh` confirmation, or the committed `review-findings.md` under fallback).

**Share-back artifact:** the committed `review-findings.md` (four issues, each with a Trust Spectrum verdict and cited justification) plus the pytest that catches the boundary bug. If the MCP round-trip landed, include the GitHub issue URL.

---

## Stuck? Self-service rescues

**Rescue A — can't spot all four issues (stuck at Step 2).**
Ask Claude to read the file and list every issue it sees, grouped by the five review dimensions (correctness, style, edge cases, hallucination, security), naming the exact line number for each, without changing the file. Use that list to cross-check your own findings. The verdicts and the `CLAUDE.md` rule are still yours to write.

**Rescue B — the test won't run / import errors (Step 3).**
Run `uv run --project server pytest tests/backend/ -v`, copy the first error line, and ask Claude what the smallest change would be to make the module importable for testing, without adding any new dependency.

**Rescue C — GitHub MCP won't connect (Step 6).**
Use the CLI fallback: `gh issue create --title "Code review: server/inventory_ops.py" --body-file review-findings.md`. If `gh` is not authenticated, keep `review-findings.md` as your artifact. Core done does not require the remote ticket.

**Rescue D — fully stuck or out of time.**
Check out the solution branch to see a finished review and the fixed function:

```
git stash -u
```

```
git fetch origin
```

```
git checkout origin/lab-8-solution -- review-findings.md
```

Open `review-findings.md` and read the four issues with their Trust Spectrum verdicts. You leave having seen the checklist applied and the trust calls made. To reset and try again, run the `/reset-branch` skill and redo Step 0.

---

## Quizzes

Your completion and mastery quizzes are in the LMS.
