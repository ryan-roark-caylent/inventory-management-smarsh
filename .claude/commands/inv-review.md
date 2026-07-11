# inv-review

Review a Vue component against the CLAUDE.md rules for this repository.

Usage: `/inv-review <path-to-component>`

## What to check

1. **v-for keys** — does any `v-for` use `:key="index"`? Flag it and suggest the stable ID (`item.id`, `sku`, `month.month`, `q.quarter`).
2. **API calls** — does the component call `http://localhost:8001` directly, or does it go through `client/src/api.js`?
3. **Date validation** — is `.getMonth()` called without a prior null/undefined check on the date value?
4. **useFilters** — if filters are needed, is the shared `useFilters` composable imported rather than local state recreated?
5. **Composition API** — is the component using Composition API (not Options API)?

For each violation found, show the line number, the rule it breaks, and the fix.
