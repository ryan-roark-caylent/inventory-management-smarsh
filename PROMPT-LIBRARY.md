# Prompt & Command Library

Shared, peer-tested prompts for this repo. An entry earns a place only if a
teammate can run it COLD and get the same result the author got.

## How to add an entry
The library is an INDEX. It tells a teammate what reusable Claude assets exist
and how to reach them — it does not store the definitions. A prompt is short
enough to live inline; a command, skill, or subagent is referenced by path.

Each entry needs, at minimum:
- **Name** — short, kebab-case.
- **When to use it** — one line.
- **Form / pointer** — either the prompt body inline, OR the form + path of the
  artifact (e.g. "command — .claude/commands/<name>.md", "subagent — @<name>").
- **Example** — one sample of the expected output.
- **Note** — one line on why it clears the reuse + reliability bar.

## Entries

### gen-endpoint-tests   (strong example)
**When to use it:** you need pytest coverage for a specific GET endpoint.
**Form / pointer:** prompt (inline) — see body below.
**Body:**
> Generate pytest tests for the GET /api/inventory endpoint in
> server/main.py. Cover: the happy path (items returned), an empty-data case
> (pass a warehouse value that matches nothing, expect []), and one bad-filter
> case (an unrecognized category value, expect []). Follow the patterns in
> tests/backend/test_inventory.py. Return only the test file contents.
**Example:** produces `tests/backend/test_inventory_filters.py` importing the
TestClient fixture and asserting the real response shape.
**Note:** clears the bar — names the target, the cases, the pattern file, and the
output format.

### quick-review   (weak example — do not copy this shape)
**When to use it:** "when you want a review."
**Form / pointer:** prompt (inline) — see body below.
**Body:**
> Review this and tell me what's wrong.
**Example:** (none provided)
**Note:** this entry is here on purpose so you can see why it fails a cold run.

### gen-endpoint-tests-v2   (reference contribution)
**When to use it:** pytest coverage for any GET endpoint that lacks tests.
**Form / pointer:** prompt (inline) — see body below.
**Body:**
> Generate pytest tests for the GET <ENDPOINT> in server/main.py. Cover: the
> happy path (items returned), an empty-data case (pass a filter value that
> matches nothing, expect []), and one bad-filter case (unrecognized filter
> value, expect []). Follow the patterns in tests/backend/test_inventory.py.
> Return only the test file contents.
**Example:** for /api/inventory, produces test_inventory_filters.py with 3 tests
asserting the real JSON shape and empty-result behavior.
**Note:** clears reuse (any filterable endpoint) + reliability (self-contained).
Invoke as a scoped run via @test-writer for repeatable coverage runs.
