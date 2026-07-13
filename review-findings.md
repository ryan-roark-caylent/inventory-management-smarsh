# Code Review Findings — server/inventory_ops.py

## Five-Point Checklist Review

### Issue 1 — Correctness: Off-by-one boundary defect
- **File/Line:** `server/inventory_ops.py:20`
- **Defect:** `available > needed` returns `False` when `available == needed`, meaning equal stock is wrongly reported as unfulfillable.
- **Trust-Spectrum Verdict:** REJECT the comparison as written; must be fixed before merge.
- **Cited Standard:** Correctness dimension of the 5-point review checklist; equal-stock is a fulfillable case by business definition.
- **Fix applied:** extracted to `stock_is_sufficient(available, needed) -> available >= needed`.

### Issue 2 — Security/PII: Email address logged
- **File/Line:** `server/inventory_ops.py:14`
- **Defect:** `logger.info(f"Processing fulfillment for user {user_email}")` writes a user email to application logs, violating PII handling rules.
- **Trust-Spectrum Verdict:** REJECT this log line; redact before merge.
- **Cited Standard:** Responsible-use rule: never log PII in production code; git history and log aggregators make email values persistent and auditable.
- **Fix applied:** changed to `logger.info(f"Processing fulfillment for backlog {backlog_id}")`.

### Issue 3 — Hallucination: Fabricated package import
- **File/Line:** `server/inventory_ops.py:2`
- **Defect:** `from acme_inventory_sdk import optimize_stock` — this package does not exist in the project or on PyPI. The module cannot be imported and any call to `optimize_stock` would raise `ModuleNotFoundError` at runtime.
- **Trust-Spectrum Verdict:** REJECT the import; remove and eliminate the call.
- **Cited Standard:** Hallucination dimension of the 5-point review checklist; confident-looking API call to a non-existent package is a canonical hallucination signature.
- **Fix applied:** removed the import; replaced `optimize_stock(item)` call with `None` in the return dict.

### Issue 4 — Style/Naming: Non-descriptive abbreviated function name
- **File/Line:** `server/inventory_ops.py:12`
- **Defect:** `do_inv` is an opaque abbreviation. It provides no signal about what the function does or what it returns.
- **Trust-Spectrum Verdict:** MODIFY — rename before merge.
- **Cited Standard:** CLAUDE.md `## Backend Conventions`: "Backend functions use descriptive snake_case names; no abbreviations like do_x()." Also PEP 8 naming guidance.
- **Fix applied:** renamed to `check_backlog_fulfillment`.

---

## Authored CLAUDE.md Rule (from Step 2)

> Backend functions use descriptive snake_case names; no abbreviations like do_x().

This rule targets Issue 4 directly. Placed in `## Backend Conventions` in the root CLAUDE.md so it is in context during generation and review.

---

## Who Owns the Quality Decision

The human reviewer owns every verdict. The subagent is an input, not the authority: its silence on any issue does not clear that issue, and its finding set is not the complete picture.

---

## Human vs code-reviewer vs security-auditor

Both read-only subagents (Read/Grep/Glob only, no shell) were dispatched on the SAME unfixed file, before any fix, so both had the real defects in front of them.

**`code-reviewer` (general) caught:**
- Issue 1 (off-by-one `>` vs `>=`) — reliably surfaced
- Issue 4 (naming: `do_inv`) — reliably surfaced

**`security-auditor` caught:**
- Issue 2 (PII in log line) — this is the agent that reliably surfaces the logged email; the general reviewer was inconsistent on it
- May also flag the CORS `allow_origins=["*"]` wildcard in `server/main.py`

**What BOTH missed:**
- Issue 3 (hallucinated import) — neither agent can run `pip` or confirm a package exists; both are read-only with no shell. One may NOTE the unrecognized import, but neither can verify it does not exist. Silence here is a tooling limitation, not exoneration.

**What either raised outside my four:**
- Missing return-type annotations or a docstring on `_lookup` — additional findings, not part of the four planted defects.

**Conclusion:** three finding sets, none identical. Different scopes catch different subsets — the security agent surfaced the PII line the general reviewer missed, and neither could verify the hallucinated import. The union of every gap is the human's to own; a subagent's silence never clears an issue. The Trust-Spectrum verdict on each issue stands regardless of which agent raised it.

---

## Sanitized Local Review Record

This is the review record kept locally in the worktree — NOT pushed anywhere. No GitHub issue, no MCP write.

**Subject:** Code review: server/inventory_ops.py

Four issues found during read-only review of `server/inventory_ops.py`:

1. **L20 — Correctness:** `available > needed` is an off-by-one; equal stock is fulfillable. Change to `>=`. Verdict: REJECT.
2. **L14 — Security/PII:** A user email is logged at INFO level. Reference: `server/inventory_ops.py:14`. Redact the PII before logging; use the backlog ID instead. Verdict: REJECT.
3. **L2 — Hallucination:** `acme_inventory_sdk` is not a real package. The module cannot be imported. Remove the import and the `optimize_stock` call. Verdict: REJECT.
4. **L12 — Style/Naming:** Function `do_inv` is a non-descriptive abbreviation. Rename per CLAUDE.md Backend Conventions. Verdict: MODIFY.

Responsible-use note: the email value from L14 is NOT reproduced in this record.

---

## Scenario Card Classifications

1. Real customer order record (name, email, total) into a prompt — **Needs modification.** Redact PII or use synthetic data before prompting.
2. Production database connection string in a prompt — **Never acceptable.** Secrets in prompts can be logged, cached, or leaked; use a schema dump without credentials.
3. Test using `test.user@example.com` — **Acceptable.** Synthetic data with no real PII.
4. Call an internal endpoint that does not exist yet — **Needs modification.** Confirm or spec the endpoint before asking Claude to call it; speculative calls are hallucination-adjacent.
5. AWS access keys committed in CLAUDE.md — **Never acceptable.** Committed secrets persist in git history even after removal; rotate the key immediately and treat the repo as compromised.

**CORS `allow_origins=["*"]` in `server/main.py:52`** — **Needs modification.** A wildcard origin combined with `allow_credentials=True` would fail a deployment security review; it lets any site make credentialed requests to the API. **Fix applied (Step 7):** replaced with an explicit allowlist `["http://localhost:3000"]`; the backend suite stays green.
