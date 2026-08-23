# Inventory management knowledge wiki

LLM-written knowledge layer. See SCHEMA.md for the maintainer contract.

## Articles
- [Inventory-demand linkage](inventory-demand-linkage.md) — how the inventory table gets its data over HTTP, how demand forecasts join to inventory by SKU, the dashboard's subset-counting pattern, and the i18n convention for adding a table column.
- [Filter system](filter-system.md) — how the four filters travel from the client to the server, and the rename coupling where the client's internal `selectedPeriod` becomes the API's `month` parameter.

## How to use
Reach for this wiki when the question is about a runtime convention or cross-file coupling the code itself can't show: an HTTP hop between the Vue client and the FastAPI server, a join convention between two data files, a naming mismatch between client and API, or where an i18n key needs to land.

For a question about code structure (where a function is defined, who calls it, what a file imports), use the code graph instead — it answers those in seconds and the answer never goes stale.
