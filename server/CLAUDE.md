# CLAUDE.md - Server

This file covers FastAPI specifics for THIS repo — not general REST tutorial.

## Repo-Specific Rules

- **Use the shared filter helpers.** `apply_filters(items, warehouse, category)` and `filter_by_month(items, month)` exist in `main.py`. Do not re-implement filtering inline.
- **Update the Pydantic model when JSON structure changes.** If you add a field to a `server/data/*.json` record, also add it to the matching model class and the `response_model` annotation.
- **`allow_origins=["*"]` is dev-only.** The CORS wildcard at line 52 of `main.py` must be restricted before any production deploy.
- **Data is in-memory.** All data loads from `server/data/*.json` at startup via `mock_data.py`. Restarting the server resets any in-flight changes.
- **Return `response_model`-typed responses.** All endpoints in this repo use `response_model=` to enforce schema. Do not drop it when adding new endpoints.

## Running the Server

```bash
cd server
uv run python main.py
# Server runs on http://localhost:8001
# API docs at http://localhost:8001/docs

# Tests
uv run pytest ../tests/backend/ -q
```

## Sources

Authored from the bloated `main` server/CLAUDE.md by trimming to repo-specific content only.
