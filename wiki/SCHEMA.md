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
- Every article states its evidence: the source files it came from, and whether a claim
  came from the code (cite file:line) or from runtime knowledge the graph cannot see.
- Append one line to log.md for every add or update. Never rewrite an existing log line.
- If an article conflicts with the code, the code wins. Fix the article and log it.
