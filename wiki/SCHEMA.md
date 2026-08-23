# Wiki schema — maintainer contract

This wiki is the LLM-written knowledge layer for the inventory-management codebase.
It follows the three-layer pattern Andrej Karpathy described for curated document
collections, adapted to source code by Cloud Capture (generate from code because docs rot):

1. Raw sources (immutable): the code in client/ and server/, plus graphify-out/graph.json.
   Never edit the code to make the wiki "true"; the code is ground truth.
2. Wiki articles (this directory): LLM-written prose explaining behavior the AST graph
   cannot see (HTTP contracts, localStorage, runtime data shape).
3. This SCHEMA.md: the rules the maintaining agent follows.

## Rules for the maintaining agent
- One article per concept, not per file. Name articles by topic (filter-system.md),
  never by community number.
- ADD a new article when a concept has no article yet. UPDATE the existing article when
  the concept is already covered. Never create a second article for the same concept.
- **Never record anything the code graph can derive.** No caller lists, no import
  relationships, no symbol locations, no line numbers. Those go stale the moment someone
  refactors, and the graph regenerates them for free. If a reader needs them, they query
  the graph. This wiki records only what the graph structurally cannot see.
- Every article names the source files it was derived from, at file level, so a reader can
  verify it. Do not pin claims to line numbers; lines move.
- Append one line to log.md for every add or update. Never rewrite an existing log line.
- If an article conflicts with the code, the code wins. Fix the article and log it.
