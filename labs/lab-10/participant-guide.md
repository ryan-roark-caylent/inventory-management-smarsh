# Lab 10: Code Knowledge Base

**Extra lab (post-programme, async) | AI Teammate | Depends on: Labs 1-9**

Cloud Capture, a Smarsh team running spec-kit on brownfield repos, hit a hard limit: their codebases "have existed forever," and spec-kit assumes greenfield. To give agents the context they needed without stuffing the whole corpus into context, they built two artifacts: a deterministic code graph and a wiki generated from code. Their reasoning: the code is true, comments may lie, docs lie more, the original spec lies most. "The further you get away from the code, the more lies you accumulate." On a deliberately simple task they measured roughly 30% fewer tokens (up to ~50% in some spec-kit phases), and their reviewers noted slightly better code quality with the graph, which they flagged as unvalidated and accidental. Less context hunting leaves more of the agent's attention on the actual task.

graphify and the code-derived LLM wiki are the tools Cloud Capture chose. Other tools cover the same ground: other AST and code-intelligence tools, embedding/vector RAG over a repo, hand-maintained knowledge bases, and IDE-native indexes. This lab does not evaluate the tool landscape and is not a procurement recommendation. The transferable outcome is the judgment these tools embody, not the specific binaries. A cheap, deterministic structural map lets an agent navigate instead of hunt. A maintained knowledge layer records what the code cannot state about itself: runtime behavior, conventions, and the reasons behind decisions. The real skill is knowing where each adds value on a repo you own.

You'll build both artifacts on the inventory-management fork, see each answer the question the other cannot, and write down which you'd reach for and why.

---

## Where the concept clicks

Step 3 is the moment. You'll ask graphify to trace the path from the Vue filter composable to the FastAPI function that serves inventory data, and get back "No path found." This is correct, not broken. The graph models static imports and calls. The HTTP boundary between client and server is invisible to the AST by design. Once that lands, the wiki's reason to exist is obvious: it records the runtime facts the graph structurally cannot see. The defend step in Step 7 becomes easy instead of arbitrary.

---

## A note on graphify and the three-layer wiki

These are one Smarsh team's concrete implementation of two general ideas. The Capture team runs them in production and is available as an internal reference. This lab is not a procurement recommendation. It is a worked example you can adapt to a repo you own.

---

## Step 0 — Setup (7 min)

**Primary bootstrap** (use this regardless of whether you've run `setup-worktrees`):

```
git fetch origin
git checkout -b lab-10-work origin/lab-10-start
```

Then open a fresh Claude Code session from inside `lab-10-work`.

**Convenience path:** if you already created `lab-10-work` via `setup-worktrees`, skip the checkout above and just open Claude Code there.

Once you are on `lab-10-work`:

1. Delete any leftover settings file from an earlier lab so a prior allow/deny list or auto-test hook does not carry into this session:

   ```
   rm -f .claude/settings.local.json
   ls .claude/
   ```

   The file should not appear in the listing. (It is not gitignored and not tracked on `main`. A copy left in a reused working directory from labs 5-7 is the contamination risk.)

2. Relaunch Claude Code from inside the worktree so the branch's context loads fresh. Windows and macOS both require this after a branch or settings change.

3. Confirm `uv` is on PATH:

   ```
   uv --version
   ```

   Expect `0.11.7` or higher. On Windows, `uv` installs to `%APPDATA%\Roaming\Python\Python3xx\Scripts`. If `uv` is not found, open a new terminal or run `uv tool update-shell` and recheck.

4. Warm the graphify cache. This is the one network operation the lab needs:

   ```
   uvx --from graphifyy graphify --version
   ```

   Expect `graphify 0.9.31` or higher. Every step after this runs offline.

> **PATH B — we never run `graphify install`.** graphify's installer writes user-global state: `~/.claude/skills/graphify/` and a `# graphify` section in `~/.claude/CLAUDE.md` that `graphify uninstall` does NOT remove. That violates the project-scope rule. This lab invokes graphify only through `uvx --from graphifyy graphify ...`, which resolves the package per-run and writes zero global config. After the lab, verify: `grep -c graphify ~/.claude/CLAUDE.md` returns `0`, and `~/.claude/skills/graphify/` does not exist.

**You know this worked when:** `graphify --version` prints through `uvx` with no install step, and `.claude/settings.local.json` is absent from `ls .claude/`.

---

## Step 1 — Build the free graph (6 min)

From the repo root, build a code-only graph. Ask Claude, or run directly:

```
uvx --from graphifyy graphify extract . --code-only
```

Do NOT run `graphify .` or `graphify extract .` without `--code-only`. That form tries semantic extraction on markdown files, defaults to an AWS Bedrock backend, and fails. See rescue path (a) if this happened.

Record your own node, edge, and community counts from the summary line.

**You know this worked when:** the summary line prints `wrote graph.json: N nodes, M edges, K communities` in a few seconds with no API-token or backend message. The run takes 3-4 seconds. Your numbers should land near the reference values in the section below. A warning that `.json` data files or `settings.local.json` produced zero nodes is normal.

---

## Step 2 — Read load-bearing structure (10 min)

Ask which symbols carry the most connections:

```
uvx --from graphifyy graphify god-nodes --top 10
```

Inspect the most-connected symbol:

```
uvx --from graphifyy graphify explain "useI18n()"
```

Ask what depends on the shared filter state:

```
uvx --from graphifyy graphify affected "useFilters()"
```

**You know this worked when:** `god-nodes` shows `useI18n()` at the top. `affected "useFilters()"` lists all 6 views that import it plus `FilterBar.vue`, `App.vue`, and `main.js` (16 connections total). `Reports.vue`, the 7th view, does not import useFilters and is correctly absent. Note that a plain text search for "useFilters" finds the import lines but not this resolved dependency set.

---

## Step 3 — The discovery beat (POINT STEP) (9 min)

Ask graphify to trace from the client filter composable to the server endpoint that serves inventory data:

```
uvx --from graphifyy graphify path "useFilters()" "get_inventory()"
```

Read the result. Then contrast it with what `affected "useFilters()"` returned in Step 2.

Write one sentence in your own words explaining why `path` finds nothing while `affected` finds plenty.

**You know this worked when:** you can state that graphify models static imports and calls (which `affected` traverses) but not the runtime HTTP request between `client/src/api.js` and the FastAPI backend (which `path` would need to cross), so the Vue-to-FastAPI boundary is invisible to the AST by design, not broken.

> This is the lab's hinge. Once you understand why the graph cannot cross this boundary, the wiki's reason to exist lands on its own, and the defend step in Step 7 is obvious rather than arbitrary.

---

## Step 4 — Export and evaluate the generated wiki (8 min)

Generate graphify's own wiki:

```
uvx --from graphifyy graphify export wiki
```

Open `graphify-out/wiki/` and list the article filenames.

Try to answer one navigation question without opening any files: "which article covers the frontend filtering logic?" Record that you cannot tell from the filenames.

**You know this worked when:** most article files are named `Community_0.md` through `Community_27.md` and are unnavigable by name alone. Note that `graphify label` assigns human-readable names but calls an LLM backend and costs API tokens. The graph is free; navigable naming is not. See the extra credit section if you have a backend configured and want to try it.

---

## Step 5 — Build the LLM wiki (14 min)

Create a `wiki/` directory in the repo root. You are building the three-layer pattern (not to be confused with Lab 3's three-layer CLAUDE.md — different idea, same word; here the three layers are: immutable raw sources, LLM-written articles, and a schema-maintainer file). This is Cloud Capture's adaptation of Karpathy's curated-document pattern applied to source code because docs rot.

Create these three files:

- `wiki/SCHEMA.md` — the maintainer contract: when the maintaining agent ADDs a new article vs UPDATEs an existing one, and the rule that the code is always ground truth.
- `wiki/index.md` — the article index and a note on when to reach for the wiki vs the graph.
- `wiki/log.md` — an append-only change log. One line per add or update. Never rewrite a line once written.

Ask Claude to generate one article (the filter system is a natural first choice) from the actual source files. The article should record what the code graph cannot tell you: the HTTP hop between `api.js` and `apply_filters()`, the `selectedPeriod` to `month` rename coupling, and any runtime state the AST cannot see.

After Claude appends to `log.md`, write a second entry yourself to practice the append discipline.

**You know this worked when:** `wiki/` holds `SCHEMA.md`, `index.md`, `log.md`, and at least one topic-named article (not named `Community_N.md`). `log.md` has two appended lines, none rewritten.

---

## Step 6 — Measurement discipline (6 min)

Run graphify's benchmark and read the methodology it prints:

```
uvx --from graphifyy graphify benchmark
```

Write why the reported reduction (~20x) is a strawman. The baseline is stuffing the entire repo corpus into context, which no competent agent does.

State the honest alternative: Cloud Capture measured roughly 30% fewer tokens on a deliberately simple task (up to ~50% in some spec-kit phases), with their stated caveats, and found the vendor's 70% claim "didn't stand true." No first-party token-reduction percentage exists in graphify's own material. Credit the ~30% measurement to Cloud Capture, not to graphify.

**You know this worked when:** your note names the strawman baseline and attributes the only real measurement to Cloud Capture with caveats, without treating either the 20x or the 70% as evidence.

---

## Step 7 — Defend which artifact answers which question (8 min)

With both artifacts present, pose two question types:

- "What breaks if I change `apply_filters()`?" (structural, static — the graph's territory)
- "Why does the app's locale persist across page reloads?" (runtime behavior the graph cannot see — the wiki's territory)

Write `KB-DECISION.md` at the repo root. For each question, name which artifact you reached for and write one sentence defending why.

**You know this worked when:** `KB-DECISION.md` records one artifact choice per question with a one-sentence reason for each. The structural question points at the graph (`affected "apply_filters"` lists callers in one command). The runtime question points at the wiki (locale persistence is `localStorage`, which the graph never sees). The solution branch has a reference exemplar once you have written your own.

---

## Step 8 — Teardown and share-back (4 min)

Confirm Path B left zero global state. Run both commands:

```
grep -c graphify ~/.claude/CLAUDE.md
```
```
test -d ~/.claude/skills/graphify/ && echo "FAIL" || echo "clean"
```

Both should return `0` and `clean` respectively.

Write an async exit note (Slack thread to the peer channel, or a private doc) with three things:

1. Your own `extract` summary line and one god-node you found non-obvious.
2. Which artifact you chose for each of the two Step-7 questions, with one sentence defending each.
3. One judgment call you made (for example, choosing not to run `graphify label`).

If sharing to a channel tracked for LMS evidence, include these synthesized competency IDs (assigned for this extra lab, mapped from the existing LMS competency framework rather than inherited from the original 9-lab mapping):

- **2.6** CLI workflows — the graphify command surface runs entirely via `uvx`
- **1.3** Context and spec management — choosing which artifact answers which question
- **4.3** Knowledge sharing — establishing a repo knowledge base others read
- **4.5** AI workflow optimization — token efficiency and the free-graph / paid-navigation tradeoff

**You know this worked when:** the two verification commands return clean, and your exit note names one non-obvious god-node, your two artifact choices, and one judgment call.

---

## Reference values (Step 1 extract output)

These are reference values from a verified run. **Your numbers may differ by a few** — the repo drifts. Expect a summary line similar to:

```
[graphify extract] found 52 code, 0 docs, 0 papers, 0 images
[graphify extract] wrote graph.json: 312 nodes, 416 edges, 28 communities
```

Reference: 52 code files, 312 nodes, 416 edges, 28 communities.

For Step 4: `export wiki` produces 38 articles, of which 28 are named `Community_0.md` through `Community_27.md`, plus 10 auto-named god-node articles.

Your Step 1 success signal still holds if your node count lands in the 250-400 range. The run should take 3-4 seconds with zero API tokens.

For Step 6, the `benchmark` reference output:

```
Corpus:          ~20,800 tokens (naive)
Graph:           312 nodes, 416 edges
Avg query cost:  ~1,035 tokens
Reduction:       ~20x fewer tokens per query
```

---

## Done criteria

You're done when all six are true:

1. `graphify extract . --code-only` produced a graph and you recorded your own counts.
2. You ran `path "useFilters()" "get_inventory()"` and can explain "No path found" in one sentence.
3. `graphify-out/wiki/` exists and you saw the `Community_N` naming.
4. `wiki/` holds `SCHEMA.md`, `index.md`, an append-only `log.md`, and at least one topic-named article.
5. `KB-DECISION.md` records a graph choice and a wiki choice with reasons.
6. Step 8 teardown confirms no graphify global state was written.

---

## Extra credit (not required)

1. **Run `graphify label` (requires an LLM backend).** If you have an AWS Bedrock configuration (boto3 + credentials) or an `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` env var, run:

   ```
   uvx --from graphifyy graphify label
   ```

   Then re-run `export wiki` and compare the article names against your unlabeled set. Token cost: labeling calls the LLM once per community to assign a name, so the cost scales with your community count and is non-trivial relative to the free extract (zero tokens). No backend? Skip it. The unlabeled state is the teaching beat, and a pre-labeled snapshot is on `lab-10-solution` for reference (see rescue path c).

2. **Add graphify's MCP server.** Apply what you built in Lab 7: add a graphify stdio entry to `.mcp.json` at project scope, relaunch, confirm with `/mcp`, and scope its tools using the read/write/block model from Lab 7.

3. **Tune a `query` budget.** Run:

   ```
   uvx --from graphifyy graphify query "how does an inventory item get updated when filters change" --budget 800
   ```

   Observe the `[!] TRUNCATED` warning, then raise `--budget` until the traversal completes. Note where the budget/answer tradeoff sits.

4. **Boot the app.** Run the frontend (`cd client && npm install && npm run dev`, opens `http://localhost:3000`) and backend (`cd server && uv run python main.py`, port 8001). Change the Warehouse filter in `FilterBar` and watch the singleton state drive `Dashboard.vue` — the coupling `god-nodes` surfaced. Requires network for `npm install`, so this is extra credit only.

---

## If you're stuck

**(a) Bare `graphify .` aborted on boto3 / Bedrock.**

You ran `graphify .` or `graphify extract .` without `--code-only`. It tried semantic extraction on markdown files, defaulted to an AWS Bedrock backend, and failed. Rescue:

```
uvx --from graphifyy graphify extract . --code-only
```

**(b) Cold-cache `uvx` fetch fails (no PyPI egress).**

The first `uvx --from graphifyy graphify ...` hangs or errors resolving ~25 tree-sitter grammar wheels. Rescue in order: (1) retry on a connection that reaches PyPI, or set `HTTPS_PROXY` and retry — the wheels are prebuilt and need no compiler; (2) if you have run graphify before on this machine, the uv cache already holds the wheels and later runs are offline — reuse the same machine; (3) if the machine is truly air-gapped, escalate to IT for a one-time PyPI mirror entry. This is the only place a locked-down machine can stall.

**(c) No LLM backend for `label`.**

Expected and fine. The unlabeled `Community_0` through `Community_27` state is the teaching beat. To see what labeled names look like, check out the committed snapshot:

```
git fetch origin
git checkout origin/lab-10-solution -- reference/labeled-wiki
```

Open `reference/labeled-wiki/` to compare human-readable names against your `graphify-out/wiki/`.

**(d) `uvx graphify` says command not found.**

The PyPI package is `graphifyy` (double-y). Always include the `--from` flag:

```
uvx --from graphifyy graphify <subcommand>
```

**(e) The `wiki/` build went sideways.**

Copy the reference wiki and adapt it:

```
git checkout origin/lab-10-solution -- wiki
```

---

Your completion and mastery assessments are in the LMS.
