# Cold-run ratings (reference)

## quick-review (weak)
Reuse: 0 — "review this" generalizes to nothing; there is no target.
Reliability: 0 — run cold, Claude has to GUESS a target. A capable model often
proceeds anyway (e.g. it inspects recent git history and reviews the last-touched
file) — that silent inference is the transfer risk, not an error. Reliability
here means "no guessing required," not "it broke." On a teammate's machine with
different history, the guess changes.
What it forced Claude to infer: which file, a checklist that lived in the author's
head, and an output format never stated. Fails the gate because it doesn't
transfer identically to a cold teammate.

## gen-endpoint-tests (strong)
Reuse: 2 — swap the endpoint name and it works for any GET route.
Reliability: 2 — names the target, the cases, the pattern file, the output shape;
runs cold with no guessing, so it transfers the same way for every teammate.
