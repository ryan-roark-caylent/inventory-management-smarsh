# Lab 8 — Output Quality, Code Review, and Responsible Use

**Track 3 — AI Teammate | Theme 8**

Your completion and mastery quizzes are in the LMS.

---

## What this lab proves

AI-generated code is untrustworthy in the same way unreviewed human code is. You own the trust call. A subagent is an input to your review, not an authority, and its silence on any issue is not a clean bill of health. Two subagents with different scopes catch different subsets; the union of what they miss is still yours to own.

This lab runs longer than an Academy module because it carries competencies with zero Academy coverage: defensible Trust-Spectrum review and human-vs-agent ownership are net-new here.

---

## The aha moment

At the point step (Steps 4-5), you dispatch two read-only subagents — a general `code-reviewer` and a `security-auditor` — on the same file you already reviewed by hand, while the file is **still broken**. Neither list matches yours, and the two lists don't match each other. Each agent's scope surfaces a different subset of what's wrong, and because read-only agents have no shell, some issues neither one can verify at all. Every gap between their lists and yours is still yours to own. That is the moment code review stops being "run the agent and merge."

---

## Core path

Steps 0-8 are the core path. Work at your own pace. Extra credit follows.

**How you work in this lab:** every action on the code routes through Claude — you ask Claude to extract the helper, write the test, apply the fix, change the CORS setting. You don't hand-edit source. The deliberate exceptions are reading the file yourself (Step 2) and writing your own findings and verdicts (Steps 3-5): those judgment calls are yours, not Claude's.

---

### Step 0 — Start clean

You work this lab inside its own git **worktree** so nothing collides with other labs and you keep your work at the end. If your pre-work already created `lab-8-work`, confirm you're in it with `git worktree list`. If not, create it now — run each line separately:

```
git fetch origin
git worktree add -b lab-8-work ../lab-8-work lab-8-start
cd ../lab-8-work
```

> **Tip:** you can run a shell command without leaving Claude Code by prefixing it with `!` (e.g. `!git worktree list`). Handy throughout the labs.

Then launch Claude Code from inside `lab-8-work`. (The worktree rule is also in this repo's `CLAUDE.md`.)

Do the following before you begin:

1. **Switch to Sonnet.** Smarsh defaults to Haiku; this lab is tuned for Sonnet. Run `/model sonnet` (or `/model` and pick Sonnet). The point-step behaviors assume Sonnet.
2. **Start a fresh Claude Code session** so the lab-branch `CLAUDE.md` loads.

**Success signal:** `server/inventory_ops.py` exists; `git branch --show-current` (or `git worktree list`) shows `lab-8-work`; `/model` shows Sonnet.

> **Docs pointer:** anything this card references as "see the pre-work" lives in your **MindTickle pre-work module**, not in this repo.

> **Note — no MCP in this lab.** Earlier drafts filed the review as a GitHub issue over MCP. This lab keeps the review as a local file. There is no MCP setup, no token, and no `/mcp` step for Lab 8.

---

### Step 1 — Responsible AI Use: frame it before you touch the code

Before you review or fix anything, set the ground rules for what you're allowed to put in front of Claude. AI-assisted coding is fast, and the same speed that helps you ship also makes it easy to leak data you can never un-leak. This step is a quick mental beat — **no writing, no committing** — but the principles carry through every later step and every lab after this one.

> **Responsible-use principles for AI-assisted coding:**
> - **Never paste real PII into prompts.** Customer names, emails, order records, account data — none of it goes into a prompt, ever. Prompts and their context can be logged and retained outside your control.
> - **Never paste secrets into prompts.** API keys, credentials, and production connection strings are off-limits, even "just to show Claude the schema." Describe the shape instead.
> - **Synthetic / example data is fine.** Made-up values like `test.user@example.com` or a fake order for `ACME Corp` carry no real-world risk. Use them freely.
> - **Don't ask Claude to call things that don't exist.** Endpoints, APIs, or integrations that are discussed-but-not-built are aspirational. Verify the surface exists before you wire code to it — otherwise you're building on a hallucination.
> - **Found committed secrets? Rotate and report, don't just delete.** If real credentials are sitting in a repo (say, AWS keys in `CLAUDE.md`), deleting the line doesn't help: the secret is compromised the moment it's committed and it lives on in git history and any forks. Treat it as leaked — rotate the key and tell whoever owns it.

**Guided reflection (think it through, don't write it down).** For each scenario below, decide: **acceptable / needs modification / never acceptable** — and, more importantly, **why**, against the principles above.

1. To debug a pricing bug, you paste a real customer order record (name, email, order total) into a prompt.
2. You inline the production database connection string in a prompt so Claude can "see the schema."
3. You ask Claude to generate a test that uses a made-up email like `test.user@example.com`.
4. You ask Claude to call an internal analytics endpoint the team has discussed but not built yet.
5. You find AWS access keys committed inside this repo's `CLAUDE.md`. What do you do?

> **How to reason through them:** 1 and 2 are real PII and a real secret — **never acceptable**, no version of pasting them is safe. 3 is synthetic data — **acceptable** as-is. 4 is a hallucinated integration — **needs modification**: confirm the endpoint exists (or build it) before asking Claude to call it. 5 isn't a paste question at all — the harm already happened, so **rotate and report** rather than quietly deleting the line. If your read of any scenario doesn't line up with the principle it maps to, re-read the principle before moving on.

**Success signal:** you can state, for each of the five, the verdict and the one principle that decides it — without looking anything up.

---

### Step 2 — Read the generated function (do NOT run it)

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

### Step 3 — Run the 5-point checklist by reading (open-ended judgment)

Walk the function against each of the five review dimensions. You may ask Claude to help you find candidate issues, but the verdicts and the `CLAUDE.md` rule are your calls. Write your findings into a new file `review-findings.md`. There are **four** planted defects — one per dimension, except one dimension is clean.

> **Working reference — the 5-point checklist (enough to act on here):**
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

### Step 4 — Dispatch the code-reviewer on the UNFIXED file and compare (point step)

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

### Step 5 — Second reviewer: dispatch the security-auditor and own the union

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

### Step 6 — Now fix it, driving Claude

Only now do you fix the code — and you drive Claude to do it, you don't hand-edit: Work the numbered actions **in the order shown** -- the import fix must land first so the module can be imported at all.

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

### Step 7 — Classify and fix the CORS wildcard, driving Claude

Find the repo's real `allow_origins=["*"]` setting in `server/main.py` (around line 52). Classify it **acceptable / needs modification / never acceptable** and **name the principle behind your call** — this is a live security finding, not a hypothetical.

Then act on it: **ask Claude to** replace the wildcard with an explicit localhost origin list (the client runs on `http://localhost:3000`), then re-run the suite and confirm it stays green. Also reload the app at `http://localhost:3000` and confirm data still loads: a wrong origin list passes the tests but breaks the browser, and only the reload catches it. Write one line on why the wildcard would fail a deployment security review.

**Success signal:** you classified the CORS setting with a named principle; `server/main.py` no longer uses `["*"]`; the suite is green; the app still loads its data at `localhost:3000`; you have a one-line rationale.

---

### Step 8 — Keep your review record (no push, no commit)

`review-findings.md` **is** your review ticket — a real, sanitized review record you keep locally. **Do not commit or push anything.** There is no GitHub issue to file; the record lives in your worktree.

Responsible-use check on your own artifact: confirm `review-findings.md` **references the PII line by number and never pastes the email value**, and contains no secret. A review record is a permanent record — treat it like one.

> **Expected output — a sanitized record (correct) vs an unsafe one (wrong):**
> ```
> GOOD:  "L14 logs a user email (PII) — see server/inventory_ops.py:14. Redact before logging."
> BAD:   "L14 logs <the actual email value>"   <-- pastes PII into a permanent record
> ```

**Exit ticket:** name the one issue you **rejected** (not just modified) and the standard or risk you cited. One line, ready to paste into the completion quiz.

**Success signal:** `review-findings.md` exists locally, is sanitized, and you can name one rejected issue and its cited standard.

---

## Done criteria

Your core path is complete when all of these are true:

1. `review-findings.md` exists with four issues, each carrying a Trust-Spectrum verdict and a cited standard, plus your authored `CLAUDE.md` rule, your ownership sentence, and the human-vs-code-reviewer-vs-security-auditor diff.
2. `tests/backend/test_inventory_ops.py` failed on the planted code and passes after the fix; the suite is green.
3. The CORS wildcard is classified with a named principle, `server/main.py` no longer uses `allow_origins=["*"]`, and the suite is still green.
4. `review-findings.md` is sanitized (PII by line number, no secrets) and kept locally — nothing committed or pushed.

**Your takeaway:** the local `review-findings.md` (four issues, each with a Trust-Spectrum verdict and cited justification), the pytest that catches the boundary bug, and the CORS fix. All of it stays in your worktree.

---

## Extra Credit

Not required for core done or the completion quiz. Work it if you finish early.

1. **Rewrite a tautological test.** Find or generate an `assert result is not None` test and rewrite it to assert the computed value. A test that can't fail on wrong output isn't a test.

---

## Stuck? Self-service rescues

> **Before any rescue:** run every command from your worktree root (`pwd` should end in `lab-8-work`), not from `server/` or `client/` -- and confirm the worktree is a **sibling** of your main clone, not nested inside it: `git worktree list` (from the main clone) should show its path outside the clone directory; if it is nested, `git worktree remove <path> --force` it and re-create it from the main clone root. If a command referencing `origin/lab-8-solution` fails with "invalid reference", run `git remote set-branches origin '*'` and `git fetch origin`, then retry. If `git worktree add` fails, match the error: "already exists" for a path `git worktree list` shows means a stale entry (`git worktree remove <path> --force`); "already exists" for a path it does NOT show means a plain leftover directory (delete the directory itself and retry); "a branch named `lab-8-work` already exists" means reuse it (`git worktree add ../lab-8-work lab-8-work`) or delete it first (`git branch -D lab-8-work`). Worktree management commands run from the main clone root; every other rescue command runs from the worktree. Worked in the main clone by mistake? The repo's `CLAUDE.md` "Worktree Isolation" section has the exact recovery steps -- ask Claude to walk you through them. Bring any uncommitted work along: `git stash -u` in the main clone, then `git stash pop` inside the worktree (the stash is shared between them).


**Rescue A — can't spot all four issues (Step 3).**
Ask Claude to read `server/inventory_ops.py` and, without fixing anything, list every issue it sees grouped by the five review dimensions (correctness, style, edge cases, hallucination, security), naming the exact line for each. Use that to cross-check your own findings. The verdicts and the `CLAUDE.md` rule are still yours to write.

**Rescue B — the test won't run / import errors (Step 6).**
Run `uv run --project server pytest tests/backend/test_inventory_ops.py -v` (your Step 6 file: expect the test you wrote there to collect; if pytest says the file does not exist, you skipped Step 6 -- go back). Copy the first error line, and ask Claude for the smallest change to make the module importable without adding a dependency.

**Rescue C — fully stuck or out of time.**
First confirm your remote points at the fork: `git remote -v` should show your fork. Then check out the finished review to SEE the trust calls made:

```
git fetch origin
git checkout origin/lab-8-solution -- review-findings.md
```

Open `review-findings.md` to read the four issues with their Trust-Spectrum verdicts, and run `git diff origin/lab-8-solution -- server/inventory_ops.py` to see the fixes. You leave having seen the checklist applied and the trust calls made.

**To reset and try again** (this permanently discards your work in this lab -- keep anything you want first): exit Claude Code, then from the **main clone root** run each line on its own:

```
git worktree remove ../lab-8-work --force
git branch -D lab-8-work
git worktree add -b lab-8-work ../lab-8-work lab-8-start
```

Then `cd ../lab-8-work` and relaunch Claude Code. With worktree-per-lab you mostly just move to the next lab's worktree.

---

## Quizzes

Your completion and mastery quizzes are in the LMS.
