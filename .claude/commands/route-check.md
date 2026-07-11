# route-check

Check a new FastAPI route against existing patterns in this repository.

Usage: `/route-check <path-to-route-handler-or-description>`

## What to check

1. **response_model** — is `response_model=` present on the `@app.get`/`@app.post` decorator? Every route in this repo uses it; do not drop it.
2. **Pydantic model sync** — if the route returns fields not yet in the matching Pydantic model, flag the model that needs updating.
3. **Filter helpers** — if the route accepts `warehouse`, `category`, or `month` query params, does it call `apply_filters` or `filter_by_month` rather than filtering inline?
4. **Naming convention** — field names should be snake_case in Python models and returned JSON.
5. **CORS note** — remind that `allow_origins=["*"]` is dev-only; any new route that sends sensitive data should note this.

For each issue, show the specific line or pattern and the fix.
