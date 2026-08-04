# Spec: Days of Cover

Add a computed "days of cover" value to the inventory data the app serves and displays, and surface a related count on the dashboard. Days of cover is how many days the current stock on hand will last at the current demand rate.

This spec states intent, not locations. Working out where each piece belongs is part of the task.

---

## What to build

### 1. Server — enrich the inventory response

The inventory listing endpoint should return a `days_of_cover` value on each item, alongside the fields it already returns.

Compute it from data the server already has:

- Match each inventory item to its demand forecast by SKU. The forecast data is already loaded server-side.
- A demand forecast records a demand figure covering a 30-day period. Derive a daily rate from it.
- `days_of_cover = quantity on hand / daily demand rate`
- Round to one decimal place.
- If no forecast exists for an item's SKU, the value is null.

Two requirements about **where** the computation goes:

- The response model must declare the new field as optional, so items without a forecast remain valid.
- The computation must run over the **already-filtered** list. This app funnels inventory filtering through a single shared helper that several endpoints depend on. Filter first, then enrich. Do not bypass or duplicate that helper.

The endpoint's route and existing query parameters must not change.

### 2. Server — add a dashboard metric

The dashboard summary endpoint should also report **`at_risk_items`**: the number of inventory items whose days of cover is below 14.

Requirements:

- It must respect the same filters the dashboard already applies to inventory, so the count reflects what the user is currently looking at.
- Items with no demand forecast (null days of cover) are not counted as at risk.
- The dashboard already computes at least one similar count over filtered inventory. Find that pattern and follow it rather than inventing a new one.
- Do not duplicate the days-of-cover formula. If you find yourself writing the same arithmetic twice, factor it so both call sites share one implementation.

This part is deliberately not self-contained: the two endpoints share filtering machinery, and the value you added in part 1 has to be reachable here too. Work out how they relate before you edit either one.

### 3. Client — surface days of cover in the inventory table

Add the value as a new column in the inventory table view.

The label must be translatable, following the internationalization convention this codebase already uses. That means:

- A new key in the locale files, in the same section and naming style as the existing table-column keys.
- Every locale the app ships gets the key, including the Japanese translation.
- The column header renders through the translation helper, not as a hardcoded string.
- Each row renders the value, showing an em dash (`—`) when it is null. Not blank, not the string "null".

You will need to work out where the inventory view lives, how it obtains the translation helper, where locale strings are kept, and how the existing columns are structured. The codebase is internally consistent; match the pattern you find.

---

## Constraints

- **In-memory only.** The server loads from JSON fixtures. No database, no schema migration, no writes to disk.
- **No new dependencies.** Nothing added to the Python or npm dependency lists.
- **No endpoint signature changes.** Both routes keep their existing query parameters.
- **No app boot required.** The backend test suite alone verifies the computation.
- **One implementation of the formula.** The days-of-cover arithmetic appears once in the codebase, not once per call site.

---

## Acceptance criteria

1. The full backend test suite passes with no new failures, and no existing test was modified.
2. The inventory endpoint returns `days_of_cover` on items whose SKU has a matching demand forecast, and null for those that do not.
3. The dashboard summary endpoint returns `at_risk_items`, counting filtered inventory items with days of cover below 14 and excluding items with no forecast.
4. Applying a warehouse or category filter changes `at_risk_items` accordingly.
5. The inventory table shows a days-of-cover column whose header comes from the translation layer, not a hardcoded English string.
6. Items with no forecast render an em dash.
7. The days-of-cover formula exists in exactly one place, shared by both endpoints.
