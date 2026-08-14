# Demand forecasts

## What they are
Demand forecast records in `server/data/demand_forecasts.json` relate to inventory items by SKU.
Each record carries `current_demand`, `forecasted_demand`, `trend`, and a `period` field.

## The period field (critical: it's free text)
The `period` field is **free text in several shapes**, not a standardized value. Verified against
fixture data (9 records): "Next 30 days", "Next 3 months", "Q1 2025", "90 days", "Next 60 days".
A function that assumes every period is 30 days will compute the wrong value for non-30-day records.

client/src/views/Demand.vue:192-207 defines `translatePeriod()` to handle these formats:
- "Next N months" / "Next N days" / "N days"
- "QN 2025" (Q1, Q2, Q3, Q4)

The regex branches confirm the values are matched patterns, not database enums.

## Why this article exists (what the graph cannot tell you)
The demand forecast fixture data lives in a JSON file (`server/data/demand_forecasts.json`). JSON
data files produce zero graph nodes (verified: graphify warns "0 code nodes from .json"). So the
graph models the `get_demand_forecasts()` endpoint and the `translatePeriod()` function, but it
cannot tell you what the `period` field actually contains across the 9 fixture records. Only
reading the data file or this article reveals the variation.

## Sources
- server/data/demand_forecasts.json (9 records, ids 1-9)
- client/src/views/Demand.vue:192-207 (translatePeriod function)
