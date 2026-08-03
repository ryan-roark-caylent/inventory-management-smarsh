# Lab 10: Code Knowledge Base

**Extra lab (post-programme, async) | AI Teammate | Depends on: Labs 1-9**

Cloud Capture, a Smarsh team running spec-kit on brownfield repos, hit a hard limit: their codebases "have existed forever," and spec-kit assumes greenfield. To give agents the context they needed without stuffing the whole corpus into context, they built two artifacts: a deterministic code graph and a wiki generated from code. Their reasoning: the code is true, comments may lie, docs lie more, the original spec lies most. "The further you get away from the code, the more lies you accumulate." On a deliberately simple task they measured roughly 30% fewer tokens (up to ~50% in some spec-kit phases), and their reviewers noted slightly better code quality with the graph, which they flagged as unvalidated and accidental. Less context hunting leaves more of the agent's attention on the actual task.

graphify and the code-derived LLM wiki are the tools Cloud Capture chose. Other tools cover the same ground: other AST and code-intelligence tools, embedding/vector RAG over a repo, hand-maintained knowledge bases, and IDE-native indexes. This lab does not evaluate the tool landscape and is not a procurement recommendation. The transferable outcome is the judgment these tools embody, not the specific binaries. A cheap, deterministic structural map lets an agent navigate instead of hunt. A maintained knowledge layer records what the code cannot state about itself: runtime behavior, conventions, and the reasons behind decisions. The real skill is knowing where each adds value on a repo you own.

You'll build both artifacts on the inventory-management fork, wire them into Claude, and prove the difference with the same spec run twice: once cold, once wired. Then you write down which artifact answers which question and why.

---

## Where the concept clicks

Step 4 is the moment. You'll ask graphify to trace the path from the Vue filter composable to the FastAPI function that serves inventory data, and get back "No path found." This is correct, not broken. The graph models static imports and calls. The HTTP boundary between client and server is invisible to the AST by design. Once that lands, the wiki's reason to exist is obvious: it records the runtime facts the graph structurally cannot see. The defend step in Step 10 becomes easy instead of arbitrary.

---

## A note on graphify and the three-layer wiki

These are one Smarsh team's concrete implementation of two general ideas. The Capture team runs them in production and is available as an internal reference. This lab is not a procurement recommendation. It is a worked example you can adapt to a repo you own.

---

## Where this comes from

Source material for every pattern and tool this lab names:

- **graphify** — https://github.com/Graphify-Labs/graphify (Apache-2.0 / MIT, free to run). PyPI package: https://pypi.org/project/graphifyy/ (the package is `graphifyy`, double-y; the CLI it installs is `graphify`).
- **The LLM wiki pattern** — Andrej Karpathy's gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f. This is a personal knowledge base over curated **documents**: three layers, ingest/query/lint. It is the document pattern, not a code-derived wiki.
- **The code-derived adaptation** — internal, no public link. The Smarsh Cloud Capture team applied the wiki shape to **source code** (generate from code because docs rot). Karpathy proposed the document pattern; Cloud Capture is the code adaptation. Do not go looking for a public repo for this part.
- **spec-kit** — https://github.com/github/spec-kit. The brownfield context Cloud Capture works in, and where they hit the greenfield assumption that started this.

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

> **Reminder (you know this from labs 1-9):** prefix a shell command with `!` inside Claude Code to run it and drop its output straight into the conversation. It matters *here* because this lab is about Claude reading graphify's output. Put a command's result where Claude can see it and Claude can reason over the graph instead of just watching you run it. You do not need to `!`-prefix every command below; reach for it when you want Claude to see what a command printed.

> **PATH B — we never run `graphify install`.** graphify's installer writes user-global state: `~/.claude/skills/graphify/` and a `# graphify` section in `~/.claude/CLAUDE.md` that `graphify uninstall` does NOT remove. It also hardcodes an absolute path to the graphify binary, which breaks on any other machine. That violates the project-scope rule. This lab invokes graphify only through `uvx --from graphifyy graphify ...`, which resolves the package per-run and writes zero global config. In Step 7 you wire the same integration by hand, at project scope, for the same reason. After the lab, verify: `grep -c graphify ~/.claude/CLAUDE.md` returns `0`, and `~/.claude/skills/graphify/` does not exist.

**You know this worked when:** `graphify --version` prints through `uvx` with no install step, and `.claude/settings.local.json` is absent from `ls .claude/`.

---

## Step 1 — Run the spec, cold (10 min)

Before you build anything, measure the baseline. You hand Claude a small spec on the untouched repo, watch how it orients itself, then throw the code changes away. The recording is the keeper, not the code.

Use the fresh session you relaunched in Step 0. No graph, no wiki, no hook exists yet. That is the point.

1. Hand Claude the spec at `specs/days-of-cover.md`. It asks for a **"days of cover"** field on the inventory endpoint: how many days the current stock will last. It is a greenfield addition (no `days_of_cover` concept exists in the repo yet), and finishing it forces genuine cross-file orientation:
   - It touches `server/main.py` (the `InventoryItem` model and `get_inventory`).
   - It must respect `apply_filters()`, the shared filter chokepoint.
   - Surfacing it in `client/src/views/Inventory.vue` means discovering the i18n convention (`useI18n()` and the locale files `client/src/locales/en.js` and `ja.js`), which a cold agent has to find on its own.
   - It stays in-memory (no database, no new dependency, no app boot required).

2. Record observable effort proxies as Claude works: how many files it read, how many tool calls it made, whether it grepped the same thing more than once, how it found the filter chokepoint and the client-server seam. Take a `/context` reading before and after as a directional signal (not a precise number).

3. Then DISCARD the code changes so Run 2 starts from the identical state:

   ```
   git checkout -- .
   git clean -fd server client
   git status
   ```

   `git checkout -- .` restores tracked files to their committed state; the spec file is committed, so it survives. `git clean -fd server client` deletes anything Claude newly created under those directories (a scratch module, a new test file, a new component) — untracked files survive `git checkout` and would otherwise carry into the wired run and invalidate the comparison. `graphify-out/` does not exist yet. `git status` should show `server/` and `client/` clean with no untracked files under either.

**You know this worked when:** you have a written cold baseline (files read, tool calls, orientation notes, `/context` delta) and `git status` shows the app code back to clean, with no graph, wiki, or hook present.

---

## Step 2 — Build the free graph (6 min)

From the repo root, build a code-only graph. Ask Claude, or run directly:

```
uvx --from graphifyy graphify extract . --code-only
```

Do NOT run `graphify .` or `graphify extract .` without `--code-only`. That form tries semantic extraction on markdown files, defaults to an AWS Bedrock backend, and fails. See rescue path (a) if this happened.

Record your own node, edge, and community counts from the summary line.

**You know this worked when:** the summary line prints `wrote graph.json: N nodes, M edges, K communities` in a few seconds with no API-token or backend message. The run takes 3-4 seconds. Your numbers should land near the reference values in the section below. A warning that `.json` data files or `settings.local.json` produced zero nodes is normal.

---

## Step 3 — Read load-bearing structure (10 min)

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

## Step 4 — The discovery beat (POINT STEP) (9 min)

Ask graphify to trace from the client filter composable to the server endpoint that serves inventory data:

```
uvx --from graphifyy graphify path "useFilters()" "get_inventory()"
```

Read the result. Then contrast it with what `affected "useFilters()"` returned in Step 3.

Write one sentence in your own words explaining why `path` finds nothing while `affected` finds plenty.

**You know this worked when:** you can state that graphify models static imports and calls (which `affected` traverses) but not the runtime HTTP request between `client/src/api.js` and the FastAPI backend (which `path` would need to cross), so the Vue-to-FastAPI boundary is invisible to the AST by design, not broken.

> This is the lab's hinge. "No path found" is the graph telling the truth: it knows every symbol your code imports and nothing about the HTTP call between them, so the Vue-to-FastAPI boundary is invisible by design, not broken. Once you understand why the graph cannot cross this boundary, the wiki's reason to exist lands on its own, and the defend step in Step 10 is obvious rather than arbitrary.

---

## Step 5 — Export and evaluate the generated wiki (8 min)

Generate graphify's own wiki:

```
uvx --from graphifyy graphify export wiki
```

Open `graphify-out/wiki/` and list the article filenames.

Try to answer one navigation question without opening any files: "which article covers the frontend filtering logic?" Record that you cannot tell from the filenames.

**You know this worked when:** most article files are named `Community_0.md` through `Community_27.md` and are unnavigable by name alone. Note that `graphify label` assigns human-readable names but calls an LLM backend and costs API tokens. The graph is free; navigable naming is not. See the extra credit section if you have a backend configured and want to try it.

---

## Step 6 — Build the LLM wiki (14 min)

Build the second artifact: a three-layer LLM wiki (not to be confused with Lab 3's three-layer CLAUDE.md, a different idea using the same word; here the three layers are immutable raw sources, LLM-written articles, and a schema-maintainer file). This is Cloud Capture's adaptation of Karpathy's curated-document pattern applied to source code because docs rot.

The pattern is: **you read it, the LLM writes it.** So Claude creates and maintains the files. Your job is to set the rules and verify the discipline held. Directing and reviewing is the work; transcription is not.

1. **Author the rules yourself.** Write `wiki/SCHEMA.md`, the maintainer contract: when the agent ADDs a new article vs UPDATEs an existing one, and the rule that the code is always ground truth. This judgment is yours, not Claude's. It is the part you own.

2. **Direct Claude to create the rest** from the actual source files:
   - `wiki/index.md` — the article index and a note on when to reach for the wiki vs the graph.
   - `wiki/log.md` — an append-only change log, one line per add or update.
   - One article (the filter system is a natural first choice). It should record what the graph cannot see: the HTTP hop between `api.js` and `apply_filters()`, the `selectedPeriod` to `month` rename coupling, and runtime state like `localStorage`.

3. **Tell Claude to append a matching entry to `log.md`** in the same pass, and never rewrite a line once written.

4. **Verify the append discipline held.** Confirm `log.md` grew by appended lines and none were rewritten. This check is yours.

Shapes to fill in, not answers to copy: thin skeletons for all four files are planted at `wiki/TEMPLATES.md`. Use them to see the structure. Do not paste them wholesale. (The rescue checkout in "If you're stuck" hands over a *finished* wiki, which is a different thing: an answer to adapt, not a shape to fill.)

**You know this worked when:** `wiki/` holds `SCHEMA.md` (the rules you wrote), `index.md`, `log.md`, and at least one topic-named article (not named `Community_N.md`). `log.md` shows one appended line per add or update, with none rewritten.

---

## Step 7 — Wire the graph into Claude (10 min)

Until now you have run graphify by hand in the terminal. Claude does not know the graph exists. This step wires both artifacts into the project so Claude reaches for them on its own.

You do this by hand, at PROJECT scope, rather than running `graphify install`, for the same reason as Path B: the installer writes user-global state and hardcodes an absolute path to the graphify binary that would not work on your machine. Wiring it yourself also means you see the config instead of an installer hiding it.

Two mechanisms, one per artifact:

1. **Tell Claude about the graph and wiki.** Append this block to the project CLAUDE.md at the repo root (`./CLAUDE.md`; create it if there is none):

   ```
   ## graphify

   This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

   Rules:
   - For codebase questions, first run `uvx --from graphifyy graphify query "<question>"` when graphify-out/graph.json exists. Use `uvx --from graphifyy graphify path "<A>" "<B>"` for relationships and `uvx --from graphifyy graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
   - If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
   - Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
   - After modifying code, run `uvx --from graphifyy graphify update .` to keep the graph current (AST-only, no API cost).
   ```

2. **Enforce the graph with a hook.** Write this to project-scope `.claude/settings.json`. Note the `uvx` form (not the absolute `.EXE` path the installer would write, which is why we author it by hand):

   ```json
   {
     "hooks": {
       "PreToolUse": [
         {
           "matcher": "Bash|Grep",
           "hooks": [{ "type": "command", "command": "uvx --from graphifyy graphify hook-guard search" }]
         },
         {
           "matcher": "Read|Glob",
           "hooks": [{ "type": "command", "command": "uvx --from graphifyy graphify hook-guard read" }]
         }
       ]
     }
   }
   ```

3. **Relaunch Claude Code.** Hooks load at startup, so they do not take effect until you relaunch (you know this from labs 1-9).

4. **Verify the hook fires.** In the relaunched session, ask Claude a codebase question that would normally send it grepping (for example, ask where inventory filtering is handled). Watch for one of two signals: Claude runs `uvx --from graphifyy graphify query` instead of grepping, or the PreToolUse hook injects its notice:

   ```
   MANDATORY: graphify-out/graph.json exists. You MUST run `graphify query "<question>"` before grepping raw files. Only grep after graphify has oriented you, or to modify/debug specific lines.
   ```

   The hook emits `graphify query` (bare form) and you cannot change that text. The CLAUDE.md rules you just appended already use the `uvx --from graphifyy graphify` form, so Claude follows those rules when it acts. The two signals are equivalent: the hook tells Claude what to do, and the CLAUDE.md rules tell Claude how to invoke it.

Now say the mechanism in your own words. **The graph is enforced by a hook; the wiki is adopted by instruction.** Two questions the owner asked, answered directly:

- *Is graphify a hook?* Yes. It is a `PreToolUse` hook on `Bash|Grep` and `Read|Glob`. Claude cannot grep or read raw files without the hook firing and pushing it to the graph first.
- *Does the wiki need a CLAUDE.md entry?* Yes, and that IS its mechanism. The wiki has no hook. It reaches Claude through the CLAUDE.md pointer above plus the `SCHEMA.md` contract you wrote in Step 6.

**You know this worked when:** after the relaunch, a codebase question triggers either the MANDATORY hook notice or a `uvx --from graphifyy graphify query` call, and you can state which artifact is enforced by a hook versus adopted by instruction.

---

## Step 8 — Run the spec again, wired (12 min)

Now measure the difference. Same spec, same starting state, but this time the graph, the wiki, and the hook all exist.

1. **Start a FRESH Claude Code session** so nothing from the wiring or verify step carries into the measured run. State from an earlier session would contaminate the comparison.

2. **Confirm the starting state matches Run 1.** `git status` should show `server/` and `client/` clean (the code you discarded to in Step 1). `graphify-out/` and `wiki/` should be present; the app code should not be modified.

3. **Hand Claude the SAME spec** (`specs/days-of-cover.md`). Record the same proxies you recorded in Step 1: files read, tool calls, whether it grepped, how it oriented itself. Take a `/context` reading before and after. The hook should visibly push Claude toward `uvx --from graphifyy graphify query` before it greps.

4. **Refresh the stale graph.** Run 2 modifies code, so your graph no longer matches. Refresh it (AST-only, costs nothing):

   ```
   uvx --from graphifyy graphify update .
   ```

   This is the CLAUDE.md rule from Step 7 made concrete.

5. **Write the comparison.** What changed in HOW Claude oriented itself between the cold run and the wired run, not just token counts. This comparison is the deliverable and feeds your share-back.

> **Honesty, non-negotiable.** Report what you measured, including a null or a regression. A run that shows no improvement, or a worse run, is a valid result, and reporting it honestly is the measurement-discipline lesson. Do not report an absolute token count as a claim; per-session readings vary by machine. Cloud Capture's ~30% is a reference point, not a target.

**You know this worked when:** you have two sets of proxies (cold vs wired) and one or two sentences on what changed in Claude's orientation. The graph is refreshed with `uvx --from graphifyy graphify update .`.

---

## Step 9 — Measurement discipline (6 min)

Run graphify's benchmark and read the methodology it prints:

```
uvx --from graphifyy graphify benchmark
```

Write why the reported reduction (~20x) is a strawman. The baseline is stuffing the entire repo corpus into context, which no competent agent does, and which is not what your cold run in Step 1 did either. You now hold your own before/after from Steps 1 and 8. Contrast the two: the vendor's number compares against a baseline nobody uses; your number compares two real runs of the same spec on the same repo.

State the honest alternative: Cloud Capture measured roughly 30% fewer tokens on a deliberately simple task (up to ~50% in some spec-kit phases), with their stated caveats, and found the vendor's 70% claim "didn't stand true." No first-party token-reduction percentage exists in graphify's own material. Credit the ~30% measurement to Cloud Capture, not to graphify. Hold your own result to the same standard: if your wired run did not beat your cold run, that is a valid result worth reporting.

**You know this worked when:** your note names the strawman baseline, contrasts it with your own two-run measurement, and attributes the ~30% to Cloud Capture with caveats, without treating either the 20x or the 70% as evidence.

---

## Step 10 — Defend which artifact answers which question (8 min)

With both artifacts present, pose two question types:

- "What breaks if I change `apply_filters()`?" (structural, static — the graph's territory)
- "Why does the app's locale persist across page reloads?" (runtime behavior the graph cannot see — the wiki's territory)

Write `KB-DECISION.md` at the repo root. For each question, name which artifact you reached for and write one sentence defending why.

**You know this worked when:** `KB-DECISION.md` records one artifact choice per question with a one-sentence reason for each. The structural question points at the graph (`affected "apply_filters"` lists callers in one command). The runtime question points at the wiki (locale persistence is `localStorage`, which the graph never sees). The solution branch has a reference exemplar once you have written your own.

---

## Step 11 — Teardown and share-back (4 min)

Confirm Path B left zero global state. Run both commands:

```
grep -c graphify ~/.claude/CLAUDE.md
```
```
test -d ~/.claude/skills/graphify/ && echo "FAIL" || echo "clean"
```

Both should return `0` and `clean` respectively.

Write an async exit note (Slack thread to the peer channel, or a private doc) with four things:

1. Your own `extract` summary line and one god-node you found non-obvious.
2. Your cold-vs-wired comparison from Steps 1 and 8: what changed in how Claude oriented itself, reported honestly (including a null or negative result if that is what you saw).
3. Which artifact you chose for each of the two Step-10 questions, with one sentence defending each.
4. One judgment call you made (for example, choosing not to run `graphify label`).

If sharing to a channel tracked for LMS evidence, include these synthesized competency IDs (assigned for this extra lab, mapped from the existing LMS competency framework rather than inherited from the original 9-lab mapping):

- **2.6** CLI workflows — the graphify command surface runs entirely via `uvx`
- **1.3** Context and spec management — choosing which artifact answers which question
- **4.3** Knowledge sharing — establishing a repo knowledge base others read
- **4.5** AI workflow optimization — token efficiency and the free-graph / paid-navigation tradeoff

**You know this worked when:** the two verification commands return clean, and your exit note names one non-obvious god-node, your cold-vs-wired comparison, your two artifact choices, and one judgment call.

---

## Reference values (Step 2 extract output)

These are reference values from a verified run. **Your numbers may differ by a few** — the repo drifts. Expect a summary line similar to:

```
[graphify extract] found 52 code, 0 docs, 0 papers, 0 images
[graphify extract] wrote graph.json: 312 nodes, 416 edges, 28 communities
```

Reference: 52 code files, 312 nodes, 416 edges, 28 communities.

For Step 5: `export wiki` produces 38 articles, of which 28 are named `Community_0.md` through `Community_27.md`, plus 10 auto-named god-node articles.

Your Step 2 success signal still holds if your node count lands in the 250-400 range. The run should take 3-4 seconds with zero API tokens.

For Step 9, the `benchmark` reference output:

```
Corpus:          ~20,800 tokens (naive)
Graph:           312 nodes, 416 edges
Avg query cost:  ~1,035 tokens
Reduction:       ~20x fewer tokens per query
```

---

## Done criteria

You're done when all nine are true:

1. You ran `specs/days-of-cover.md` cold (Step 1), recorded the baseline proxies, and fully discarded the code changes (`git checkout -- .` plus `git clean -fd server client`, leaving no untracked files behind).
2. `graphify extract . --code-only` produced a graph and you recorded your own counts.
3. You ran `path "useFilters()" "get_inventory()"` and can explain "No path found" in one sentence.
4. `graphify-out/wiki/` exists and you saw the `Community_N` naming.
5. `wiki/` holds `SCHEMA.md` (rules you authored), `index.md`, an append-only `log.md`, and at least one topic-named article, with log lines appended, none rewritten.
6. You wired both artifacts into Claude: the graphify section in `./CLAUDE.md`, the PreToolUse hooks in `.claude/settings.json`, relaunched, and verified the hook fires.
7. You ran the same spec wired (Step 8) in a fresh session and recorded the cold-vs-wired comparison.
8. `KB-DECISION.md` records a graph choice and a wiki choice with reasons.
9. Step 11 teardown confirms no graphify global state was written.

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

**(f) The hook does not fire after Step 7.**

Check three things, in order: (1) `.claude/settings.json` must be valid JSON — a trailing comma or a missing brace silently disables the hooks. (2) You must have relaunched Claude Code after writing the file; hooks load at startup. (3) `graphify-out/graph.json` must exist — the hook-guard only fires when the graph is present, so if you removed or never built it, rebuild with `uvx --from graphifyy graphify extract . --code-only`. Fix whichever applies, relaunch, and ask a codebase question again.

---

Your completion and mastery assessments are in the LMS.
