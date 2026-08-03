# Wiki file skeletons — shapes to fill in, not answers to copy

Use these to understand the structure of each file before you build it. The finished reference
wiki (with real content derived from this repo) is available via the stuck-path rescue:
`git checkout origin/lab-10-solution -- wiki`

---

## SCHEMA.md

```markdown
# Wiki schema — maintainer contract

This wiki is the LLM-written knowledge layer for the <repo name> codebase.
It follows the three-layer pattern adapted to source code by Cloud Capture:

1. Raw sources (immutable): <where the code lives>. Never edit the code to make the wiki "true"; the code is ground truth.
2. Wiki articles (this directory): LLM-written prose explaining behavior the AST graph cannot see.
3. This SCHEMA.md: the rules the maintaining agent follows.

## Rules for the maintaining agent
- One article per concept, not per file. Name articles by topic (filter-system.md, not Community_3.md).
- ADD a new article when <condition>. UPDATE the existing article when <condition>. Never create a second article for the same concept.
- Every article states its evidence: source files it came from, and whether a claim came from code (cite file:line) or from runtime knowledge the graph cannot see.
- Append one line to log.md for every add or update. Never rewrite an existing log line.
- If an article conflicts with the code, the code wins. Fix the article and log it.
```

---

## index.md

```markdown
# <Repo name> knowledge wiki

LLM-written knowledge layer. See SCHEMA.md for the maintainer contract.

## Articles
- [<Article title>](<filename>.md) — <one-line description>

## How to use
Ask the agent to answer from this wiki first when the question is about <...>.
For a question about code structure (<example>), use the graphify graph instead — see KB-DECISION.md.
```

---

## log.md

```markdown
# Wiki change log (append-only)

<date>  <action>  <filename>  <derivation source>
```

Column shape: `date` (YYYY-MM-DD), `action` (add or update), `file` (the article file), `derivation` (what source files the content came from).

Example line:
```
2026-08-01  add  filter-system.md  derived from useFilters.js, api.js, server/main.py
```

One line per add or update. Never rewrite a line once written.

---

## An article (e.g., filter-system.md)

```markdown
# <Concept name>

## What it does
<One paragraph: the concept in plain terms.>

## Client to server flow (or the relevant structural section for this concept)
- <file or symbol>: <what it does, with file:line when useful>
- <file or symbol>: <what it does>

## What the code graph cannot tell you (why this article exists)
- <A fact that is invisible to the AST: an HTTP hop, a rename coupling, localStorage, a runtime convention.>
- <Another such fact.>

## Sources
- <file>, <file>, <file>
```

The "What the code graph cannot tell you" section is the reason this file exists. If every fact in the article is also visible in the graph, the article adds nothing.
```
