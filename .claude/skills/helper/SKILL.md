---
name: helper
description: Repo utility.
---

# Helper

Generate pytest tests for a FastAPI endpoint in this repo.

## What this skill produces

A `test_<feature>.py` file in `tests/backend/` that:
- Uses the `client` fixture from `tests/backend/conftest.py`
- Follows the class-based structure in `test_inventory.py` and `test_orders.py`
- Covers the happy path (200 status, correct response shape)
- Covers at least one filter (if the endpoint accepts filters)
- Covers one error case (404 for a nonexistent resource, or 422 for invalid input)
- Uses lowercase comparisons for string fields (status, category)
- Uses `abs(a - b) < 0.01` for float comparisons

## Steps

1. Read the target endpoint in `server/main.py` — identify route path, method, query params, response model.
2. Read `tests/backend/conftest.py` — understand available fixtures.
3. Read the most similar existing test file (e.g. `test_inventory.py` for inventory-like endpoints) for naming conventions and assertion patterns.
4. Write `tests/backend/test_<feature>.py` using the class-based template.
5. Confirm the file is runnable: `uv run --project server pytest tests/backend/test_<feature>.py -q`.

## Reference: test file template

```python
"""
Tests for <feature> API endpoints.
"""
import pytest


class Test<Feature>Endpoints:
    """Test suite for <feature>-related endpoints."""

    def test_get_all_<resources>(self, client):
        """Test getting all <resources>."""
        response = client.get("/api/<resources>")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_get_<resource>_by_filter(self, client):
        """Test filtering <resources> by <filter>."""
        response = client.get("/api/<resources>?<filter>=<value>")
        assert response.status_code == 200

        data = response.json()
        for item in data:
            assert item["<filter>"].lower() == "<value>".lower()

    def test_get_nonexistent_<resource>(self, client):
        """Test getting a <resource> that doesn't exist."""
        response = client.get("/api/<resources>/nonexistent-999")
        assert response.status_code == 404
        assert "detail" in response.json()
```

## Key reminders

- Reference `docs/lab-6/five-abstraction-rubric.md` for when a skill is the right abstraction vs a hook, CLAUDE.md, subagent, or MCP.
- The backend test-pattern reference (`docs/lab-6/backend-test-patterns.md`) has a full set of testing patterns — read it for edge-case guidance.
- Run tests with: `uv run --project server pytest tests/backend/ -q`
