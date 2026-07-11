# Cold-run ratings (reference)

## quick-review (weak)
Reuse: 0 — "review this" generalizes to nothing; there is no target.
Reliability: 0 — run cold, Claude asks which file/endpoint and what to check.
What it assumed: a file the author already had open, a checklist in the author's
head, and an output format never stated. Fails the gate.

## gen-endpoint-tests (strong)
Reuse: 2 — swap the endpoint name and it works for any GET route.
Reliability: 2 — names the target, the cases, the pattern file, the output shape;
runs cold with no extra context.
