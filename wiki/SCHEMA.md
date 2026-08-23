# Wiki schema — maintainer contract

This wiki is the LLM-written knowledge layer for the inventory-management codebase.
It follows the three-layer pattern adapted to source code:

1. Raw sources (immutable): the `server/` and `client/` trees. The code is ground truth. Never edit the code to make the wiki "true" — fix the wiki instead.
2. Wiki articles (this directory): prose explaining behavior the code graph cannot see.
3. This SCHEMA.md: the rules the maintaining agent follows.

## The core rule

Never record anything the code graph can derive. No caller lists, no import relationships, no symbol locations, no line numbers. Those go stale the moment someone refactors, and the graph regenerates them for free in seconds. This wiki records only what the graph structurally cannot see: HTTP hops between processes, data-shape conventions (which fields join across files, what a field's value actually contains), runtime/config behavior, and cross-cutting conventions like i18n key placement. If a fact is visible by reading one file's AST, it does not belong here.

## Rules for the maintaining agent

- One article per concept, not per file. Name articles by topic (`inventory-demand-linkage.md`, not `Demand_3.md`).
- **ADD** a new article when a concept has no existing article covering it.
- **UPDATE** the existing article when new work touches a concept already covered — never create a second article for the same concept.
- Verify claims against the current code before writing them down. Record what the code actually does, not what you expect it to do.
- Append one line to `log.md` for every add or update. Never rewrite an existing log line.
- If an article conflicts with the code, the code wins. Fix the article and log the correction.
