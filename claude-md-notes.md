# CLAUDE.md Before/After Notes

## What Changed

**Before (lab-3-start state):**
The root `CLAUDE.md` was ~90 lines and carried several problems:
- A stale `## API Endpoints` section listing `GET /api/suppliers` (which does not exist) and omitting `/api/reports/quarterly` and `/api/reports/monthly-trends`.
- A `## Deployment & Environment Setup` block with fake AWS example credentials — a bad habit that trains people to commit secrets.
- A `## My Preferences` block (personal editor prefs) that had no business in a shared project file.
- Generic content duplicated in `client/CLAUDE.md` (~484 lines) and `server/CLAUDE.md` (~286 lines) — mostly framework tutorial any competent Vue/FastAPI dev already knows, plus one rule duplicated verbatim from the root.

**After (this solution branch):**
- Root trimmed to ~55 lines: Stack, Quick Start (with test command added), Key Patterns, the root-only `vue-expert` delegation rule, 3 always/never rules grounded in real rough edges, an `@server/main.py` reference, and the Workshop Rule.
- The stale inline API list was replaced by `@server/main.py`, so the route list can never drift again. That `@`-import is eager: `main.py` now rides every session's launch footprint.
- `client/CLAUDE.md` cut to ~20 lines of repo-specific rules (api.js centralization, v-for key, date validation, useFilters singleton, Composition API only).
- `server/CLAUDE.md` cut to ~20 lines of repo-specific rules (shared filter helpers, Pydantic sync, CORS caveat, in-memory constraint, response_model pattern).
- Duplicated "always run the full test suite" rule removed from both sub-files (it lives in root `## Workshop Rule`).
- Credentials block and personal-preferences block deleted entirely.

## Context Management (eager vs lazy)

Two loading modes are visible in one `/context` reading:
- The `@server/main.py` import is **always-on** — it sits in the launch footprint before any work, and rides every request. Use it for things Claude must always know and that can't be allowed to drift, like the route list.
- `server/CLAUDE.md` is **lazy** — it does not appear at launch; it enters the footprint the moment Claude touches a file under `server/`. On current Sonnet the entry lands under Messages, not Memory files. Use sub-files to scope directory-specific rules so they cost nothing until you are in that directory.

## Output Quality Delta (with vs without root)

The root carries a rule that lives only in it: any `.vue` create/modify must be delegated to the `vue-expert` subagent. No sub-file mentions delegation, so renaming only the root gives a clean comparison.

**With the root CLAUDE.md (task: add a supplier column to the inventory table view):**
Claude delegated the `.vue` edit to the `vue-expert` subagent — the transcript shows a `Task(vue-expert)` call. The subagent followed repo conventions: stable `:key="item.id"`, API access through `client/src/api.js`.

**Without the root (`git mv CLAUDE.md CLAUDE.md.off`, relaunch):**
Claude edited the `.vue` file directly, no delegation. Three concrete differences: (1) no `vue-expert` delegation — Claude did the edit itself; (2) used `:key="index"` (the anti-pattern the root rule forbids) rather than a stable id; (3) reached for an inline fetch instead of routing through `client/src/api.js`.

The sub-files (`client/`, `server/`) stayed in place for both runs and did not muddy the result, because none of them says anything about delegation — the delta is attributable to the root alone.

## Sources

- `lab-3-start` branch CLAUDE.md set (root, client/, server/) — the degraded starting state.
- `server/main.py` — authoritative route list verified via grep (309 lines; routes confirmed).
- Real rough edges: `Reports.vue` lines 28/51/82 (`:key="index"`); `main.py` `total_backlog_items` counts the unfiltered global list; `main.py` CORS wildcard `allow_origins=["*"]`.
- Root-only convention: the `vue-expert` MANDATORY-delegation rule (`.claude/agents/vue-expert.md` defines the subagent).

**Date generated:** 2026-07-13
