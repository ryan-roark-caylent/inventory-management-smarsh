# CLAUDE.md
**Currently working on:** PR #142 low-stock alerting — sprint ends Friday. Ping @rohan before merging.

Factory Inventory Management System Demo with GitHub integration - Full-stack application with Vue 3 frontend, Python FastAPI backend, and in-memory mock data (no database).

## Critical Tool Usage Rules

### Subagents
Use the Task tool with these specialized subagents for appropriate tasks:

- **vue-expert**: Use for Vue 3 frontend features, UI components, styling, and client-side functionality
  - Examples: Creating components, fixing reactivity issues, performance optimization, complex state management
  - **MANDATORY RULE: ANY time you need to create or significantly modify a .vue file, you MUST delegate to vue-expert**
- **code-reviewer**: Use after writing significant code to review quality and best practices
- **Explore**: Use for understanding codebase structure, searching for patterns, or answering questions about how components work
- **general-purpose**: Use for complex multi-step tasks or when other agents don't fit

### Skills
- **backend-api-test** skill: Use when writing or modifying tests in `tests/backend` directory with pytest and FastAPI TestClient

### MCP Tools
- **ALWAYS use Playwright MCP tools** (`mcp__playwright__*`) for browser testing
  - Test against: `http://localhost:3000` (frontend), `http://localhost:8001` (API)

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
```

## Key Patterns

**Filter System**: 4 filters (Time Period, Warehouse, Category, Order Status) apply to all data via query params
**Data Flow**: Vue filters → `client/src/api.js` → FastAPI → In-memory filtering → Pydantic validation → Computed properties
**Reactivity**: Raw data in refs (`allOrders`, `inventoryItems`), derived data in computed properties

## API Endpoints
- `GET /api/inventory` - Filters: warehouse, category
- `GET /api/orders` - Filters: warehouse, category, status
- `GET /api/suppliers` - Supplier directory lookup
- `GET /api/dashboard/summary` - All filters
- `GET /api/demand`, `/api/backlog` - No filters
- `GET /api/spending/*` - Summary, monthly, categories, transactions

## Common Issues
1. Use unique keys in v-for (not `index`) - use `sku`, `month`, etc.
2. Validate dates before `.getMonth()` calls
3. Update Pydantic models when changing JSON data structure
4. Inventory filters don't support month (no time dimension)
5. Revenue goals: $800K/month single, $9.6M YTD all months

## File Locations
- Views: `client/src/views/*.vue`
- API Client: `client/src/api.js`
- Backend: `server/main.py`, `server/mock_data.py`
- Data: `server/data/*.json`
- Styles: `client/src/App.vue`

## Design System
- Colors: Slate/gray (#0f172a, #64748b, #e2e8f0)
- Status: green/blue/yellow/red
- Charts: Custom SVG, CSS Grid for layouts
- No emojis in UI

## My Preferences
- I like 2-space indents everywhere.
- Run prettier and show me the diff before you apply changes.
- I usually work in the afternoons EST.

## Deployment & Environment Setup
Deploy target: prod-inventory.internal.example.com
AWS_ACCESS_KEY_ID: AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
DATABASE_URL: postgres://admin:hunter2@db.internal.example.com:5432/inventory

## Workshop Rule
Local commits only. Never push, never create pull requests, never use GitHub remote operations.
Always run the full test suite before claiming a change works.
