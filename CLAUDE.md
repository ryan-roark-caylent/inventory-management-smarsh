# CLAUDE.md

Factory Inventory Management System Demo — Full-stack application with Vue 3 frontend, Python FastAPI backend, and in-memory mock data (no database).

## Stack
- **Frontend**: Vue 3 + Composition API + Vite (port 3000)
- **Backend**: Python FastAPI (port 8001)
- **Data**: JSON files in `server/data/` loaded via `server/mock_data.py`

## Working in a Worktree (workshop rule — do not remove)

- **MANDATORY: before running `git checkout`, `git switch`, or `git worktree` on any `lab-*` branch, STOP.** Confirm your current directory is this lab's `lab-3-work` worktree (`git worktree list` — cwd should be the `lab-3-work` entry, not the main clone). Do not switch branches inside a shared checkout.
- This lab runs inside its own isolated `lab-3-work` worktree so work can't collide across labs and you keep everything at the end. It was created in Step 0 of the participant guide (`git worktree add ../lab-3-work lab-3-start`).
- **If you are in the main clone instead of a worktree, do NOT `git switch`** — create/enter the worktree first: `git worktree add ../lab-3-work lab-3-start`, then `cd ../lab-3-work` and relaunch Claude Code there.
- Never edit lab files from the main clone or commit to the lab's base branch. Keep the whole session — edits, tests, commands — inside the worktree.

## Quick Start

```bash
# Backend
cd server
uv run python main.py

# Frontend
cd client
npm install && npm run dev

# Tests
uv run pytest ../tests/backend/ -q
```

## Key Patterns

**Filter System**: 4 filters (Time Period, Warehouse, Category, Order Status) apply to all data via query params.
**Data Flow**: Vue filters → `client/src/api.js` → FastAPI → In-memory filtering → Pydantic validation → Computed properties.
**Reactivity**: Raw data in refs (`allOrders`, `inventoryItems`), derived data in computed properties.

## Subagents

- **MANDATORY: any time you create or significantly modify a `.vue` file, delegate the work to the `vue-expert` subagent** (via the Task tool). This rule lives only in the root so it applies across the whole repo.

## Always / Never Rules

- **Never** use `:key="index"` in a `v-for` — use a stable ID (`item.id`, `sku`, `month.month`, `q.quarter`). `Reports.vue` does this wrong at lines 28, 51, and 82.
- **Never** hardcode `http://localhost:8001` in a component — route all API calls through `client/src/api.js`.
- **Always** apply filters before counting or aggregating — `total_backlog_items` in `main.py` counts the unfiltered global list.

## API Endpoints

See @server/main.py for the authoritative route list and filters.

## File Locations
- Views: `client/src/views/*.vue`
- API Client: `client/src/api.js`
- Backend: `server/main.py`, `server/mock_data.py`
- Data: `server/data/*.json`

## Design System
- Colors: Slate/gray (#0f172a, #64748b, #e2e8f0)
- Status: green/blue/yellow/red
- Charts: Custom SVG, CSS Grid for layouts
- No emojis in UI

## Workshop Rule
Local commits only. Never push, never create pull requests, never use GitHub remote operations.
Always run the full test suite before claiming a change works.
