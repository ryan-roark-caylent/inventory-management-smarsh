# Inventory-demand linkage

## What it does
The Inventory and Demand Forecast views both start from the in-memory inventory dataset, but they reach it through different paths and join to it differently. This article covers the parts of that relationship a code graph can't see: the network hop, the join convention between demand records and inventory items, a counting pattern reused across views, and where a new column's translation has to land.

## The HTTP hop between the client and the server
The client never reads server data directly; every view goes through the shared API client, which issues an `axios` GET to a FastAPI server running on a separate port (client dev server on 3000, API on 8001). The request carries filters as query-string params, not a request body, and the server applies filtering to its in-memory list before responding — the client receives an already-filtered array, not the full dataset. There is no shared type between the Pydantic response model and the JS caller; the client trusts the JSON shape it gets back. If the two drift, the failure shows up at runtime (a missing/undefined field in the UI), not at build or lint time.

## How demand forecasts join to inventory
Demand forecast records and inventory items are two independent JSON files with no foreign key enforcement. They join at runtime, in the client, by matching the demand record's SKU field against the inventory item's SKU field (see the naming mismatch below). The join is used to make the Demand view filter-aware: the demand endpoint itself takes no filter params, so the client fetches all forecasts, fetches the filtered inventory list separately, builds a set of SKUs from that filtered inventory, and keeps only forecast records whose SKU is in that set. This is a client-side filter join, not a server-side one — filtering demand by warehouse or category only works because the client already has the filtered inventory list in hand.

The forecast's `period` field is a free-text string written into the source JSON, not a structured value (examples in the data: `"Next 30 days"`, `"Next 3 months"`, `"Q1 2025"`). There is no enum or fixed set of periods — whatever string is in the JSON is displayed close to verbatim. For the Japanese locale, the UI doesn't translate `period` through the normal i18n key lookup; it runs the raw string through a set of regex substitutions (matching fragments like "Next ", "months", "days", "Q1"–"Q4") to produce a Japanese rendering. A period string that doesn't match one of those patterns (e.g. a newly authored period like "Rest of FY25") passes through untranslated in Japanese.

## The dashboard's subset-count pattern
The dashboard shows a count of backlog items next to the "Inventory Shortages" heading by rendering the length of the same client-side filtered-join array described above (backlog matched against the filtered inventory's SKU set), interpolated directly into the heading text rather than going through the `itemsCount`-style pluralization key used elsewhere (e.g. in the Demand view's trend cards). Any new "count of a filtered subset" display should follow one of these two existing conventions rather than inventing a third: interpolate a computed array's `.length` directly, or use an `itemsCount` translation key with a `{count}` placeholder.

## The i18n convention for a new column label
Locale strings live in two parallel files, `client/src/locales/en.js` and `client/src/locales/ja.js`, each exporting one object with matching nested keys. There is no key-completeness check between the two files at build time — a key present in `en.js` but missing in `ja.js` silently falls back to the English string at runtime (the translation helper walks the current locale's object, and on a missing key retries the same path against English before giving up). Adding a table column's header means adding the same new key under both files' matching nested path (e.g. `demand.table.<newKey>`), in both locales, or the Japanese UI will silently show English for that header. A header reaches the page through the translation helper by calling it with the dotted key path (`t('demand.table.newKey')`); there's no separate registration step beyond adding the key to the locale files.

## Naming mismatch: SKU field
The inventory item's SKU field is named `sku` in both the JSON data and the API response model. Every other dataset that references an inventory item by SKU (demand forecasts, backlog items) names that same value `item_sku` instead. Any code joining across these datasets has to know to compare `inventoryItem.sku` against `otherRecord.item_sku` — there's no shared field name to grep for.

## Sources
- client/src/api.js
- server/main.py
- server/data/demand_forecasts.json
- client/src/views/Demand.vue
- client/src/views/Dashboard.vue
- client/src/composables/useI18n.js
- client/src/locales/en.js
- client/src/locales/ja.js
