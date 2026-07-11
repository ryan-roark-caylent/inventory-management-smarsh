# Candidate prompts for your library contribution

Pick ONE to refine and contribute. Each is a rough draft — your job is to make
it clear enough to run cold.

## Rating rubric (use in Step 1 and on your own entry)
- **Reuse (0-2):** does it generalize beyond one file/case? 0 = one-off, 2 = any endpoint/component.
- **Reliability (0-2):** does it run cold with no extra context? 0 = needs hand-holding, 2 = self-contained.
An entry should score 2 + 2 before it goes in the library.

## Candidate A — backend test generator
> Generate pytest tests for <ENDPOINT> in server/main.py. Cover happy path,
> empty data, and one malformed input. Follow tests/backend/conftest.py. Return
> only the test file.

## Candidate B — endpoint reviewer (5-point checklist)
> Review <ENDPOINT> in server/main.py against: correctness, style, edge cases,
> hallucinated APIs, and security. List findings by dimension. Do not fix yet.

## Candidate C — PR description writer
> From `git diff --staged`, write a PR description: what changed, why, and how to
> test it. Use the headings Summary / Changes / Testing. Keep it under 200 words.
