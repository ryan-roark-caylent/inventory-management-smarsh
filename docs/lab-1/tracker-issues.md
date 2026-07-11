# Tracker Issues — Lab 1

## Issue A — "How should low-stock alerting work?"
We want to notify when an item drops below its reorder point, with a per-category
threshold. No code yet — we need to think through the design and open questions
before anyone writes it.

## Issue B — "Reports page bypasses the shared API client"
Reports.vue hardcodes http://localhost:8001 and reimplements calls instead of using
the shared client in client/src/api.js. Refactor it to go through api.js like every
other view. Touches the Vue component and the API client.

## Issue C — "Nightly stale-inventory report"
Every night, scan the inventory data and emit a CSV of items below reorder point,
grouped by warehouse. Runs unattended in CI — no human in the loop.
