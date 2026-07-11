# CLAUDE.md Before/After Notes

## What Changed

**Before (lab-3-start state):**
The root `CLAUDE.md` was ~90 lines and carried several problems:
- A volatile sprint note near the top ("Currently working on: PR #142") that would bust the KV-cache prefix every Friday.
- A stale `## API Endpoints` section listing `GET /api/suppliers` (which does not exist) and omitting `/api/reports/quarterly` and `/api/reports/monthly-trends`.
- A `## Deployment & Environment Setup` block with fake AWS example credentials — a bad habit that trains participants to commit secrets.
- A `## My Preferences` block (personal editor prefs) that had no business in a shared project file.
- Generic content duplicated in `client/CLAUDE.md` (484 lines) and `server/CLAUDE.md` (286 lines) — mostly framework tutorial any competent Vue/FastAPI dev already knows, plus one rule duplicated verbatim from the root.

**After (this solution branch):**
- Root trimmed to ~50 lines: Stack, Quick Start (with test command added), Key Patterns, 3 always/never rules grounded in real rough edges, `@server/main.py` reference, Workshop Rules, and a `# Session Context` block at the bottom holding the volatile sprint line.
- `client/CLAUDE.md` cut to ~20 lines of repo-specific rules (api.js centralization, v-for key, date validation, useFilters singleton, Composition API only).
- `server/CLAUDE.md` cut to ~20 lines of repo-specific rules (shared filter helpers, Pydantic sync, CORS caveat, in-memory constraint, response_model pattern).
- Duplicated "always run the full test suite" rule removed from both sub-files (it lives in root `## Workshop Rule`).
- Credentials block deleted entirely. Volatile PR line moved to bottom `# Session Context`.

## Output Quality Delta

**With CLAUDE.md (before trim, stale API section):**
When asked to add a `supplier` field to the inventory endpoint, Claude updated the `InventoryItem` Pydantic model, the `GET /api/inventory` response, and kept `response_model=List[InventoryItem]` — following the model-sync rule from the sub-file. It used snake_case.

**Without CLAUDE.md (renamed, fresh session):**
Claude added the field only to the dict return in the route handler, did not update the Pydantic model, dropped `response_model` typing, and named the field `supplierName` (camelCase). Three concrete differences: no model update, no response_model, wrong naming convention.

**Cache note:**
Moving the volatile "Currently working on: PR #142" line from line 2 of the file to a `# Session Context` block at the bottom means that editing the sprint note no longer busts the KV-cache prefix for the entire file. Every token after an edited line must be re-evaluated; a volatile line near the top of a 90-line file makes the whole file effectively non-cacheable.

## Sources

- `lab-3-start` branch CLAUDE.md set (root, client/, server/) — the degraded starting state.
- `server/main.py` — authoritative route list verified via grep.
- Real rough edges: `Reports.vue` lines 28/51/82 (`:key="index"`); `main.py:200` (`total_backlog_items` counts unfiltered global); `main.py:52` (CORS wildcard).

**Date generated:** 2026-07-11
