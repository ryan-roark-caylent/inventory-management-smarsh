# CLAUDE.md

Factory Inventory Management System Demo — Full-stack application with Vue 3 frontend, Python FastAPI backend, and in-memory mock data (no database).

## Stack
- **Frontend**: Vue 3 + Composition API + Vite (port 3000)
- **Backend**: Python FastAPI (port 8001)
- **Data**: JSON files in `server/data/` loaded via `server/mock_data.py`

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

## Working in a Worktree (workshop rule — do not remove)

This lab runs inside an isolated git worktree so your work can't collide with other labs and you keep everything at the end. Before doing any work:

- You should be in a `lab-3-work` worktree (created in Step 0 of the participant guide). Confirm with `git worktree list` — your current directory should be the `lab-3-work` entry, not the main clone.
- **If you are editing from the main repo checkout (not a worktree), stop and set one up first:** `git worktree add ../lab-3-work lab-3-start`, then `cd ../lab-3-work` and relaunch Claude Code there.
- Never edit lab files directly from the main clone or commit to the lab's base branch. Keep the whole session — edits, tests, commands — inside the worktree.
