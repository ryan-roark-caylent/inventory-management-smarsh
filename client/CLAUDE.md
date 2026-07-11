# CLAUDE.md - Client

This file covers Vue 3 specifics for THIS repo — not general Vue tutorial.

## Repo-Specific Rules

- **All API calls go through `client/src/api.js`.** Never call `http://localhost:8001` directly from a component.
- **Never use `:key="index"` in a `v-for`.** Use a stable identifier (`item.id`, `sku`, `month.month`, `q.quarter`). `Reports.vue` has this bug at lines 28, 51, and 82 — don't copy it.
- **Always validate dates before calling `.getMonth()`.** Several views receive date strings that may be null.
- **`useFilters` is a shared singleton composable.** Import it; do not recreate filter state per component.
- **Composition API only.** No Options API components in this codebase.

## Running the Client

```bash
cd client
npm install && npm run dev
# Runs on http://localhost:3000
```

## Sources

Authored from the bloated `main` client/CLAUDE.md by trimming to repo-specific content only.
