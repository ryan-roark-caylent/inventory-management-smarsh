# Lab 8 — Output Quality, Code Review, and Responsible Use

**Track 3 — AI Teammate | Theme 8**

Your completion and mastery quizzes are in the LMS.

---

## What this lab proves

AI-generated code is untrustworthy in the same way unreviewed human code is. You own the trust call. A subagent is an input to your review, not an authority, and its silence on any issue is not a clean bill of health. Two subagents with different scopes catch different subsets; the union of what they miss is still yours to own.

This lab runs longer than an Academy module because it carries competencies with zero Academy coverage: defensible Trust-Spectrum review and human-vs-agent ownership are net-new here.

---

## The aha moment

At the point step (Steps 3-4), you dispatch two read-only subagents — a general `code-reviewer` and a `security-auditor` — on the same file you already reviewed by hand, while the file is **still broken**. Neither list matches yours, and the two lists don't match each other. The `code-reviewer` reliably flags the boundary bug and the naming; the `security-auditor` is the one that surfaces the PII log line; neither can verify the hallucinated import, because read-only agents have no shell. Every gap is yours to own. That is the moment code review stops being "run the agent and merge."

---

## Core path

Steps 0-8 are the core path. Work at your own pace. Extra credit follows.

**How you work in this lab:** every action on the code routes through Claude — you ask Claude to extract the helper, write the test, apply the fix, change the CORS setting. You don't hand-edit source. The deliberate exceptions are reading the file yourself (Step 1) and writing your own findings and verdicts (Steps 2-4): those judgment calls are yours, not Claude's.

---

### Step 0 — Start clean

You should already be on `lab-8-work` (in your per-lab worktree) from the MindTickle pre-work module. If you are not, check it out now:

```
git fetch origin
git worktree add ../lab-8-work lab-8-start
```

(Your pre-work module has the exact worktree setup; this is the fallback.)

Do the following before you begin:

1. **Switch to Sonnet.** Smarsh defaults to Haiku; this lab is tuned for Sonnet. Run `/model sonnet` (or `/model` and pick Sonnet). The point-step behaviors assume Sonnet.
2. **Start a fresh Claude Code session** so the lab-branch `CLAUDE.md` loads.

**Success signal:** `server/inventory_ops.py` and `docs/lab-8/scenario-cards.md` exist; `git branch --show-current` (or `git worktree list`) shows `lab-8-work`; `/model` shows Sonnet.

> **Docs pointer:** anything this card references as "see the pre-work" lives in your **MindTickle pre-work module**, not in this repo.

> **Note — no MCP in this lab.** Earlier drafts filed the review as a GitHub issue over MCP. This lab keeps the review as a local file. There is no MCP setup, no token, and no `/mcp` step for Lab 8.

---

### Step 1 — Read the generated function (do NOT run it)

Open `server/inventory_ops.py`. This is AI-generated code that landed in a PR. Read it top to bottom before doing anything else.

You will see a function that imports a package, logs some information, looks up a record, and returns a fulfillment decision.

**Success signal:** you can state in one sentence what the function is supposed to do (decide whether a backlog item can be fulfilled from available stock).

> **Expected output — the shape of what you're reading:**
> ```python
> from acme_inventory_sdk import optimize_stock
>
> def do_inv(backlog_id, user_email):
>     logger.info(f"Processing fulfillment for user {user_email}")
>     item = _lookup(backlog_id)
>     needed, available = item["quantity_needed"], item["quantity_available"]
>     fulfillable = available > needed
>     return {"fulfillable": fulfillable, "reorder": optimize_stock(item)}
> ```
> *(Abridged. Open the actual file for the full version.)*

---

### Step 2 — Run the 5-point checklist by reading (open-ended judgment)

Walk the function against each of the five review dimensions. You may ask Claude to help you find candidate issues, but the verdicts and the `CLAUDE.md` rule are your calls. Write your findings into a new file `review-findings.md`. There are **four** planted defects — one per dimension, except one dimension is clean.

> **Working reference — the 5-point checklist (from the Theme 8 video; enough to act on here):**
> - **Correctness** — does it produce the right result (logic, boundaries)?
> - **Style adherence** — does it follow this repo's conventions (naming, structure)?
> - **Edge cases** — does it handle equal / empty / missing / invalid inputs?
> - **Hallucination** — does it call a package, API, or method that does not exist?
> - **Security** — does it leak PII or secrets, or open an attack surface?
>
> **Trust Spectrum reminder:** every finding gets a verdict — **accept** (use as-is), **modify** (fix before use), or **reject** (do not use) — and each verdict cites a **standard or named risk**, never "it felt fine."

For each finding, write: the line number, the dimension, your Trust-Spectrum verdict, and the standard or risk you cite. Then **author one `CLAUDE.md` rule** that would have stopped the style defect at generation time, and write **one sentence on who owns the quality decision** (not the AI, not the subagent — you).

**Success signal:** `review-findings.md` names four issues, each with a verdict and a cited standard, plus your authored `CLAUDE.md` rule and your ownership sentence.

---

### Step 3 — Dispatch the code-reviewer on the UNFIXED file and compare (point step)

**Do not fix anything yet.** Ask Claude to dispatch the read-only `code-reviewer` subagent (Read / Grep / Glob only) on `server/inventory_ops.py` as it stands — still broken. Read its report. Then, in `review-findings.md`, note **which of your four issues it also caught, which it missed, and anything it raised that you didn't.**

> **Why the file is still broken:** you run the reviewer BEFORE fixing so it has the real defects in front of it. If you fixed first, the reviewer would find little and the comparison would be dull.

> **Refresher:** the subagent runs in its **own context window** and has **read-only tools** — it cannot run the code, `pip`-check an import, or write files. That is exactly why its silence on the hallucinated import (or the PII line) is not exoneration.

> **Expected output — the shape of a subagent report (contents will differ from yours, and that's the point):**
> ```
> # Code Review: inventory_ops
> **Files Reviewed**: server/inventory_ops.py
> ## Critical Issues
> 1. <a correctness / boundary finding>
> ## Improvements
> 1. <a naming / style finding>
> (No files modified — reviewer has Read/Grep/Glob only.)
> ```
> Which specific issues it raises is non-deterministic and will not perfectly match your four. That mismatch is the lesson: compare its list to yours and decide what you still own.

**Success signal:** `review-findings.md` has a "human vs code-reviewer" section showing both finding sets with at least one difference noted; every issue still carries a verdict and cited standard.

---

### Step 4 — Second reviewer: dispatch the security-auditor and own the union

Ask Claude to dispatch the `security-auditor` subagent on the same unfixed file. Diff its findings against the `code-reviewer`'s. Note in `review-findings.md`: **what the security agent caught that the general reviewer missed** (typically the PII log line), and what BOTH missed (the hallucinated import — neither can verify a package exists).

Confirm your Trust-Spectrum verdict for each issue now that you have three opinions (yours plus two agents). The lesson: **different scopes catch different subsets; the union of gaps is still yours to own.**

> **Expected output — the shape of a security-auditor report:**
> ```
> # Security Audit: inventory_ops
> ## Findings
> 1. <a data-handling / logging finding>
> (No files modified — read-only.)
> ```

**Success signal:** `review-findings.md` has a "human vs code-reviewer vs security-auditor" comparison; you've noted at least one issue each agent surfaced that the other didn't, and stated the ownership conclusion.

---

### Step 5 — Now fix it, driving Claude

Only now do you fix the code — and you drive Claude to do it, you don't hand-edit:

1. **Ask Claude to neutralise the hallucinated import** so the module imports (remove or stub it — no new dependency). This is your "reject" action on the hallucination.
2. **Ask Claude to extract the comparison logic** into a standalone helper `stock_is_sufficient(available, needed)` and **write a pytest** that calls `stock_is_sufficient(850, 850)` and asserts `True`.
3. Run it, watch it fail on the planted `>`; **ask Claude to change `>` to `>=`**; run green.

```
uv run --project server pytest tests/backend/ -v
```

> **Expected output — the import error, then your test failing then passing (shape only):**
> ```
> E   ModuleNotFoundError: No module named 'acme_inventory_sdk'
> ...
> tests/backend/test_inventory_ops.py::test_equal_stock_is_fulfillable FAILED
> ...
> tests/backend/test_inventory_ops.py::test_equal_stock_is_fulfillable PASSED
> ```
> This is the point of "read, don't run": a happy-path smoke test never gets far enough to reveal the boundary bug, and the confident-looking `optimize_stock` call is pure hallucination.

**Success signal:** your new test failed on the planted code and passes after the one-character fix; the suite is green.

---

### Step 6 — Work the responsible-use scenario cards

Open `docs/lab-8/scenario-cards.md`. For each of the five cards, classify it **acceptable / needs modification / never acceptable** and **state WHY — name the principle behind your call.** Then classify the repo's real `allow_origins=["*"]` setting in `server/main.py` (around line 52).

**Success signal:** five classifications plus the CORS call, each with a one-line justification that names the principle.

---

### Step 7 — Fix the CORS wildcard, driving Claude

You just classified `allow_origins=["*"]` as needs-modification. Now act on it: **ask Claude to** replace the wildcard with an explicit localhost origin list (the client runs on `http://localhost:3000`), then re-run the suite and confirm it stays green. Write one line on why the wildcard would fail a deployment security review.

**Success signal:** `server/main.py` no longer uses `["*"]`; the suite is green; you have a one-line rationale.

---

### Step 8 — Keep your review record (no push, no commit)

`review-findings.md` **is** your review ticket — a real, sanitized review record you keep locally. **Do not commit or push anything.** There is no GitHub issue to file; the record lives in your worktree.

Responsible-use check on your own artifact: confirm `review-findings.md` **references the PII line by number and never pastes the email value**, and contains no secret. A review record is a permanent record — treat it like one.

> **Expected output — a sanitized record (correct) vs an unsafe one (wrong):**
> ```
> GOOD:  "L4 logs a user email (PII) — see server/inventory_ops.py:4. Redact before logging."
> BAD:   "L4 logs <the actual email value>"   <-- pastes PII into a permanent record
> ```

**Exit ticket:** name the one issue you **rejected** (not just modified) and the standard or risk you cited. One line, ready to paste into the completion quiz.

**Success signal:** `review-findings.md` exists locally, is sanitized, and you can name one rejected issue and its cited standard.

---

## Done criteria

Your core path is complete when all of these are true:

1. `review-findings.md` exists with four issues, each carrying a Trust-Spectrum verdict and a cited standard, plus your authored `CLAUDE.md` rule, your ownership sentence, and the human-vs-code-reviewer-vs-security-auditor diff.
2. `tests/backend/test_inventory_ops.py` failed on the planted code and passes after the fix; the suite is green.
3. Five scenario cards plus the CORS wildcard are classified with cited justifications.
4. `server/main.py` no longer uses `allow_origins=["*"]`, and the suite is still green.
5. `review-findings.md` is sanitized (PII by line number, no secrets) and kept locally — nothing committed or pushed.

**Your takeaway:** the local `review-findings.md` (four issues, each with a Trust-Spectrum verdict and cited justification), the pytest that catches the boundary bug, and the CORS fix. All of it stays in your worktree.

---

## Extra Credit

Not required for core done or the completion quiz. Work it if you finish early.

1. **Rewrite a tautological test.** Find or generate an `assert result is not None` test and rewrite it to assert the computed value. A test that can't fail on wrong output isn't a test.

---

## Stuck? Self-service rescues

**Rescue A — can't spot all four issues (Step 2).**
Ask Claude to read `server/inventory_ops.py` and, without fixing anything, list every issue it sees grouped by the five review dimensions (correctness, style, edge cases, hallucination, security), naming the exact line for each. Use that to cross-check your own findings. The verdicts and the `CLAUDE.md` rule are still yours to write.

**Rescue B — the test won't run / import errors (Step 5).**
Run `uv run --project server pytest tests/backend/ -v`, copy the first error line, and ask Claude for the smallest change to make the module importable without adding a dependency.

**Rescue C — fully stuck or out of time.**
First confirm your remote points at the fork: `git remote -v` should show your fork. Then check out the finished review to SEE the trust calls made:

```
git fetch origin
git checkout origin/lab-8-solution -- review-findings.md
```

Open `review-findings.md` to read the four issues with their Trust-Spectrum verdicts, and run `git diff origin/lab-8-solution -- server/inventory_ops.py` to see the fixes. You leave having seen the checklist applied and the trust calls made.

To reset and try again, run the `/reset-branch` command and redo Step 0. It does `branch -D` + `reset --hard` + `clean -fd` with no confirmation, so keep anything you want first. With worktree-per-lab you mostly just move to the next lab's worktree.

---

## Quizzes

Your completion and mastery quizzes are in the LMS.
