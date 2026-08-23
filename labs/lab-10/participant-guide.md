# Lab 10: Code Knowledge Base

**Extra lab (post-programme, async) | AI Teammate | Depends on: Labs 1-9**

Cloud Capture, a Smarsh team running spec-kit on brownfield repos, hit a hard limit: their codebases "have existed forever," and spec-kit assumes greenfield. To give agents the context they needed without stuffing the whole corpus into context, they built two knowledge layers: a deterministic code graph and a wiki generated from code. Their reasoning: the code is true, comments may lie, docs lie more, the original spec lies most. "The further you get away from the code, the more lies you accumulate."

At the inventory-management repo size (53 files) these knowledge layers cost extra steps and stop you shipping a wrong answer. The step overhead is roughly fixed. The correctness benefit grows with the size of the codebase. On a deliberately simple task Cloud Capture measured roughly 30% fewer tokens (up to ~50% in some spec-kit phases), and their reviewers noted slightly better code quality with the graph, which they flagged as unvalidated and accidental. Less context hunting leaves more of the agent's attention on the actual task.

graphify and the code-derived LLM wiki are the knowledge layers Cloud Capture chose. Other tools cover the same ground: other AST and code-intelligence tools, embedding/vector RAG over a repo, hand-maintained knowledge bases, and IDE-native indexes. The transferable outcome is the judgment these knowledge layers embody, not the specific binaries. A cheap, deterministic structural map lets an agent navigate instead of hunt. A maintained knowledge layer records what the code cannot state about itself: runtime behavior, conventions, and the reasons behind decisions. The real skill is knowing where each adds value on a repo you own.

You'll build both knowledge layers on the inventory-management fork, wire them into Claude, and measure the difference with the same spec run twice: once cold, once wired. By the end you should be able to say which knowledge layer answers which question, and why, on a repo you own.

---

## Where the concept clicks

Step 4 is the moment. You'll ask graphify to trace the path from the Vue filter composable to the FastAPI function that serves inventory data, and get back "No path found." This is correct, not broken. The graph models static imports and calls. The HTTP boundary between client and server is invisible to the AST by design. Once that lands, the wiki's reason to exist is obvious: it records the runtime facts the graph structurally cannot see. The defend step in Step 9 becomes easy instead of arbitrary.

**A note on scale.** This is a 53-file repo and `CLAUDE.md` already supplies orientation, so **expect a thin token delta or none, and possibly more tool calls**. The two axes split: the graph and wiki produce more, smaller, targeted reads that replace fewer, larger whole-file reads. A targeted graphify query is cheaper than reading the file, but querying and then reading the file anyway is net neutral or worse on step count. graphify's gains were measured on a repo near a million lines, and Cloud Capture runs 40-50 microservices. The real evidence in this lab is what each knowledge layer could and could not answer, not a token count. A lab that manufactured a token win would be disingenuous.

---

## A note on graphify and the three-layer wiki

These are one Smarsh team's concrete implementation of two general ideas. The Capture team runs them on their services and is available as an internal reference. This lab is not a procurement recommendation. It is a worked example you can adapt to a repo you own.

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

> **We never run `graphify install` in this lab.** graphify's installer writes user-global state: `~/.claude/skills/graphify/` and a `# graphify` section in `~/.claude/CLAUDE.md` that `graphify uninstall` does NOT remove. It also hardcodes an absolute path to the graphify binary, which breaks on any other machine. That violates the project-scope rule. This lab invokes graphify only through `uvx --from graphifyy graphify ...`, which resolves the package per-run and writes zero global config. In Step 6 you wire the same integration by hand, at project scope, for the same reason. After the lab, verify: `grep -c graphify ~/.claude/CLAUDE.md` returns `0`, and `~/.claude/skills/graphify/` does not exist.

**You know this worked when:** `graphify --version` prints through `uvx` with no install step, and `.claude/settings.local.json` is absent from `ls .claude/`.

---

## Step 1 — Run the spec, cold (9 min)

Before you build anything, measure the baseline. You hand Claude a small spec on the untouched repo, watch how it orients itself, then throw the code changes away. The recording is the keeper, not the code.

Use the fresh session you relaunched in Step 0. No graph, no wiki, no hook exists yet. That is the point.

1. Hand Claude the spec at `specs/days-of-cover.md`. Do not read it closely yourself first, and do not add file paths or hints when you hand it over. The spec deliberately states intent without naming locations, because **the orientation work is the thing being measured.** Telling Claude where to look would remove the very cost the graph and wiki are supposed to reduce, and both runs would come out flat.

   What it asks for, at a level that spoils nothing: a computed "days of cover" value on inventory data, a related count on the dashboard, and the value surfaced as a translatable column in the UI. It is greenfield (no such concept exists in the repo yet), it spans server and client, and it requires finding a shared helper and an existing convention on its own.

2. **Keep the work in this session (same rule as Step 7).** If Claude offers to delegate part of the task to a subagent, decline. A subagent is a fresh context, so its tool calls never appear in your count. If you allow delegation here and not in Step 7 (or the reverse), the two runs are measuring different things and the comparison is void. Whatever you do here, do the same there.

3. When the implementation completes, ask Claude this retrospective question before you inspect the result:

   > Before I look at the result: report on how you worked. How many tool calls did you make in total, and how many came before your first edit to a source file? Which distinct files did you read, and which of those did you read before your first edit? Did you search for the same thing more than once? In one sentence, how did you work out where the shared inventory filter helper lives? What did you assume about the time period the demand figure covers, and where did that assumption come from? And did you use graphify or the wiki at any point: be specific about commands run and files opened, and say plainly if you skipped either.

   Record: total calls, calls before first edit, distinct files read, distinct files read before first edit, repeated-search yes/no. These are self-reported and approximate, which is acceptable because both runs are measured identically and the reading is directional, not precise.

4. Then DISCARD the code changes so Run 2 starts from the identical state:

   ```
   git checkout -- .
   git clean -fd server client
   git status
   ```

   `git checkout -- .` restores tracked files to their committed state; the spec file is committed, so it survives. `git clean -fd server client` deletes anything Claude newly created under those directories (a scratch module, a new test file, a new component). Untracked files survive `git checkout` and would otherwise carry into the wired run and invalidate the comparison. `graphify-out/` does not exist yet. `git status` should show `server/` and `client/` clean with no untracked files under either.

**You know this worked when:** you have a written cold baseline (files read, tool calls, orientation notes) and `git status` shows the app code back to clean, with no graph, wiki, or hook present.

---

## Step 2 — Build the free graph (6 min)

From the repo root, build a code-only graph. Ask Claude, or run directly:

```
uvx --from graphifyy graphify extract . --code-only
```

Do NOT run `graphify .` or `graphify extract .` without `--code-only`. That form tries semantic extraction on markdown files, defaults to an AWS Bedrock backend, and fails. See rescue path (a) if this happened.

Record your own node, edge, and community counts from the summary line.

**You know this worked when:** the summary line prints `wrote graph.json: N nodes, M edges, K communities` in a few seconds with no API-token or backend message. The run takes 3-4 seconds. Your numbers should land near the reference values in the section below. A warning that `.json` data files or `settings.local.json` produced zero nodes is normal.

### Then export graphify's generated notes (3 min)

graphify can turn the graph into a set of markdown files, one per community:

```
uvx --from graphifyy graphify export wiki
```

Open `graphify-out/wiki/` and look at the filenames. Then try to answer one question without opening anything: *which of these covers the frontend filtering logic?*

You cannot tell. Most files are named `Community_0.md` through `Community_27.md`, because communities are computed clusters with no inherent names. `uvx --from graphifyy graphify label` assigns readable names, but that call goes to an LLM backend and costs API tokens. **The graph is free; navigable naming is not.** That tradeoff is the whole lesson here.

> **Two different things called "wiki." Keep them straight for the rest of the lab.**
>
> - **`graphify-out/wiki/` — graphify's generated notes.** Machine-derived from the graph, one file per community, free to produce, unnavigable until you pay for labeling. This is what you just made.
> - **`wiki/` — your LLM wiki.** You build this in Step 5, by hand-directing Claude. It records what the code cannot state about itself: runtime behavior, the HTTP seam, conventions and their reasons. Structurally different, and the one the precedence rule in Step 5 points Claude at.
>
> When this lab says "the wiki" from here on, it means **your** `wiki/`.

**You know this worked when:** `graphify-out/wiki/` holds mostly `Community_N.md` files, you could not answer the navigation question from the filenames, and you can state why labeling costs money while the graph does not.

---

## Step 3 — Read load-bearing structure (8 min)

### The five commands, in one place

| Command | What it answers |
|---|---|
| `god-nodes` | Which symbols carry the most connections. The load-bearing abstractions. |
| `explain "<symbol>"` | Everything touching one symbol, in both directions, with the edge type on each. |
| `affected "<symbol>"` | Reverse-only: what would break if you changed this symbol. |
| `path "<A>" "<B>"` | The shortest chain of references connecting two symbols, if one exists. |
| `query "<question>"` | A scoped subgraph relevant to a plain-language question. |

**Community:** graphify clusters the graph into groups whose members reference each other more than they reference the rest of the codebase. Those clusters are "communities." They are computed, not curated, which is why they start out named `Community_0`, `Community_1`, and so on. You will see them again in the next step.

### First, find the hubs

```
uvx --from graphifyy graphify god-nodes --top 10
```

### Then run `explain` and `affected` on the SAME symbol

This is the point of this step. Same symbol, two commands, so the difference you see is the difference between the commands and nothing else.

```
uvx --from graphifyy graphify explain "useFilters()"
```

```
uvx --from graphifyy graphify affected "useFilters()"
```

Compare them. `explain` shows the full neighborhood in both directions and labels each edge (`imports`, `calls`, `imports_from`). `affected` answers a narrower and more practical question: if I change this, what breaks? It walks the graph in reverse only.

**You know this worked when:** `god-nodes` shows `useI18n()` at the top. Both `useFilters()` commands return the views that import it plus `FilterBar.vue`, `App.vue`, and `main.js`, but `explain` labels the edge types and includes the symbol's own outbound references, while `affected` gives you only the blast radius. `Reports.vue` does not import `useFilters` and is correctly absent from both. A plain text search for "useFilters" finds the import lines but not this resolved dependency set.

---

## Step 4 — The discovery beat (POINT STEP) (9 min)

**First, see `path` succeed**, so you know what a hit looks like and can trust the miss that follows. Both of these stay within a single side of the app (frontend or backend):

```
uvx --from graphifyy graphify path "get_inventory()" "apply_filters()"
```

```
uvx --from graphifyy graphify path "useFilters()" "FilterBar.vue"
```

Each returns a 1-hop edge: `get_inventory() --calls--> apply_filters()`, and `useFilters() <--imports-- FilterBar.vue`. The command works, and it names the edge type.

**Now cross the client-server boundary** with the same command:

```
uvx --from graphifyy graphify path "useFilters()" "get_inventory()"
```

`No path found.` Nothing is broken. Compare it against the two successes above and the `affected` output from Step 3.

**You know this worked when:** the two same-language paths each return a 1-hop edge, the client-to-server path returns "No path found," and you can say why: graphify models static imports and calls (which `affected` traverses and the working paths follow) but not the runtime HTTP request between `client/src/api.js` and the FastAPI backend. The Vue-to-FastAPI boundary is invisible to the AST by design.

> This is the lab's hinge. "No path found" is the graph telling the truth: it knows every symbol your code imports and nothing about the HTTP call between them, so the Vue-to-FastAPI boundary is invisible by design, not broken. Once you understand why the graph cannot cross this boundary, the wiki's reason to exist lands on its own, and the defend step in Step 9 is obvious rather than arbitrary.

---

## Step 5 — Build the LLM wiki (10 min)

Build the second knowledge layer: a three-layer LLM wiki (not to be confused with Lab 3's three-layer CLAUDE.md, a different idea using the same word; here the three layers are immutable raw sources, LLM-written articles, and a schema-maintainer file). This is Cloud Capture's adaptation of Karpathy's curated-document pattern applied to source code because docs rot.

The pattern is: **you read it, the LLM writes it.** So Claude creates and maintains the files. Your job is to decide what the wiki must cover and to verify the discipline held. Directing and reviewing is the work; transcription is not.

**Review this prompt before running it.** It directs Claude to build the four wiki files with the right targeting for Step 7's spec. Once you have reviewed it and understand what it asks for, hand it to Claude:

> Build a three-layer LLM wiki for this repo at `wiki/`. Create four files:
>
> 1. `wiki/SCHEMA.md` — the maintainer contract. State when to ADD a new article versus UPDATE an existing one, and that code is always ground truth. Include this rule explicitly: **never record anything the code graph can derive.** No caller lists, no import relationships, no symbol locations, no line numbers. Those go stale the moment someone refactors, and the graph regenerates them for free in seconds. This wiki records only what the graph structurally cannot see. Keep it short; I will review it and it governs your future edits to this wiki.
>
> 2. `wiki/index.md` — the article index and a note on when to reach for the wiki versus the graph.
>
> 3. `wiki/log.md` — an append-only change log, one line per add or update. Never rewrite a line once written.
>
> 4. One article covering the inventory and demand-forecast area. Name it `inventory-demand-linkage.md`. Record only what the graph cannot see. Do not name functions, callers, or line numbers; if a reader needs those, they should query the graph:
>    - How the inventory endpoint's response reaches the table in the UI (the HTTP hop between `api.js` and the FastAPI server)
>    - How demand-forecast records relate to inventory items: matched by SKU, and what the `period` field actually contains. Check `server/data/demand_forecasts.json` and `client/src/views/Demand.vue`'s `translatePeriod` function before writing this down, and record what you find rather than what you expect.
>    - The dashboard's existing pattern for counting a subset of filtered inventory (one already exists; name it)
>    - The i18n convention for a new column label: where locale strings live, which locales must receive the key, how a header reaches the translation helper, and what happens at runtime if a key exists in one locale file but not the other
>    - Any place the same value carries different names across a boundary. Check two kinds: between what the client calls a field and what the API calls it, and between what two data files call the same identifier. Name both if both exist.
>
> Append a matching entry to `log.md` as you create each file. Shapes to fill in (not answers to copy) are planted at `wiki/TEMPLATES.md` if you need to see the structure.

After Claude completes, **verify the append discipline held.** Confirm `log.md` grew by appended lines and none were rewritten. 

> **Why this article and not another.** A wiki with one article can only help with a question that article happens to cover. Point it at the subsystem you are about to modify (Step 7's spec) and the wiki gets a fair test. Point it somewhere else and you learn nothing except that a thin wiki misses. Cloud Capture's wiki covers their whole codebase, so theirs gets consulted as a matter of course; yours will cover one corner. You are testing the mechanism at lab scale, not experiencing the benefit at production scale.

**You know this worked when:** `wiki/` holds `SCHEMA.md` (which you have read and agree with), `index.md`, `log.md`, and at least one topic-named article (not named `Community_N.md`). `log.md` shows one appended line per add or update, with none rewritten.

---

## Step 6 — Wire the graph into Claude (13 min)

Until now you have run graphify by hand in the terminal. Claude does not know the graph exists. This step wires both knowledge layers into the project so Claude reaches for them on its own.

You do this by hand, at PROJECT scope, rather than running `graphify install`, for the reason given in Step 0: the installer writes user-global state and hardcodes an absolute path to the graphify binary that would not work on your machine. Wiring it yourself also means you see the config instead of an installer hiding it.

Two mechanisms, one per knowledge layer:

1. **Tell Claude about the graph and wiki.** Append this block to the project CLAUDE.md at the repo root (`./CLAUDE.md`; create it if there is none):

   ```
   ## Code knowledge sources: precedence

   This project has two knowledge layers over the same codebase. They answer different questions, so the order you consult them matters.

   **1. The wiki (`wiki/index.md`) — for "how does this work" and "where does X live".**
   Before reading source files to understand how a feature behaves, check `wiki/index.md` and read any article covering that area. The wiki records what the code cannot state about itself: runtime behavior, cross-boundary contracts (like the HTTP seam between client and server), naming mismatches, and the reasons behind conventions. See `wiki/SCHEMA.md` for the maintainer contract. Distinct from the auto-generated per-community notes under `graphify-out/wiki/`.

   **2. The graph (graphify) — for symbol-level relationships and call chains.**
   Run `uvx --from graphifyy graphify query "<question>"` for a scoped subgraph, `uvx --from graphifyy graphify path "<A>" "<B>"` to trace a relationship between two symbols, and `uvx --from graphifyy graphify explain "<concept>"` for one symbol's neighborhood. These return far less than `GRAPH_REPORT.md` or raw grep. The graph is deterministic AST output: it knows every import and call, and nothing about runtime behavior or network hops.

   **Run the graph for any structural question even if the wiki appears to answer it.** Who calls what, what a change breaks, where a symbol is defined: the wiki is prose a human wrote at some point in the past and it can be silently out of date, while the graph is regenerated from the current source in seconds. Treat a structural claim in the wiki as a lead to confirm, not an answer to trust.

   **3. Raw source — last, or first when you already know the location.**
   Read files directly after the layers above have oriented you, or immediately when a task already names the exact files and lines. When a spec pinpoints locations, there is no navigation problem to solve and skipping both layers is correct.

   Other rules:
   - Read `graphify-out/GRAPH_REPORT.md` only for broad architecture review, or when query/path/explain do not surface enough context.
   - After modifying code, run `uvx --from graphifyy graphify update .` to keep the graph current (AST-only, no API cost).
   - Both layers go stale. The graph reports staleness itself; the wiki does not, so treat an old article as a lead rather than truth, and verify against code.
   ```

   Note what this block does and does not do. It gives the wiki an ordering and a job, but the wiki is still only prose in a file. The graph gets a hook in the next sub-step. That asymmetry is deliberate and you will see its effect in Step 7.

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

3. **Give the wiki a hook too.** The graph is enforced (step 2 above), but the wiki is only prose in `CLAUDE.md`. Close that gap by adding a third `PreToolUse` entry alongside the two graphify hooks.

   > **REPLACE the file with the block below. Do not paste it after the block above.** This is the complete final `.claude/settings.json`, the same two graphify hooks plus one new entry, **three entries in total.** Appending it to the previous block would leave two top-level JSON objects in one file, which is invalid JSON, and Claude Code disables every hook without telling you. That is rescue path (f).

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
         },
         {
           "matcher": "Read|Grep|Glob",
           "hooks": [{ "type": "command", "command": "bash .claude/hooks/pre-tool-use-wiki.sh" }]
         }
       ]
     }
   }
   ```

   **Check the file before you relaunch.** A malformed `settings.json` disables every hook silently, and you would spend the rest of the lab wondering why nothing fires:

   ```
   python -c "import json;h=json.load(open('.claude/settings.json'))['hooks']['PreToolUse'];print(len(h),'entries');[print(' ',e['matcher']) for e in h]"
   ```

   Expect `3 entries` and the matchers `Bash|Grep`, `Read|Glob`, `Read|Grep|Glob`. Any other count means you appended when you should have replaced. A `JSONDecodeError` means the file is invalid and no hook is active.

   The script `.claude/hooks/pre-tool-use-wiki.sh` already exists on this branch. It checks for `wiki/index.md` and nudges Claude to consult it before reading source. Notice what you just wired and what you did not. There is no wiki equivalent of graphify's `hook-guard` binary, so nothing here validates staleness or tailors the message to the file being read. You wired a nudge, not a guard. That gap between "a hook fires" and "a hook knows something" is worth understanding before you decide what your own repo needs.

4. **Relaunch Claude Code.** Hooks load at startup, so they do not take effect until you relaunch (you know this from labs 1-9).

5. **Verify the hooks fire.** Ask two questions in the relaunched session, in this order. The pair shows the precedence rule you just wrote deciding where each one goes.

   **First, a structural question:**

   > What calls `apply_filters()`?

   **Then a runtime-behavior question:**

   > What happens if a locale key exists in `en.js` but is missing from `ja.js`?

   **Watch which layer answers, and notice that the wiki can route as well as answer.** The structural question should reach the graph directly, in about one call, because "what calls what" is exactly what an AST resolves and your `SCHEMA.md` forbade the wiki from recording it. The second should reach the wiki and stay there, because a silent runtime fallback is invisible to any AST.

   A third outcome is common and worth expecting: Claude opens `wiki/index.md`, finds that the index itself says structural questions belong to the graph, and forwards itself to graphify. **That is the two layers cooperating, not a failure.** Because the wiki no longer records symbol locations, its index has become a router for the questions it deliberately does not answer.

   **Watch whether either question ends up opening a source file.** With the hooks live it should not need to, because both answers exist in a layer. If it does, that is diagnostic rather than broken, and it usually means one of two things: the hooks did not load (ask Claude whether it received the notices), or **your wiki under-covered the area the question asks about**, so there was nothing to find and source was the only option left. The second is the more common and more useful finding, because it tells you what your article should have recorded.

   The PreToolUse hook may also inject its notice:

   ```
   MANDATORY: graphify-out/graph.json exists. You MUST run `graphify query "<question>"` before grepping raw files. Only grep after graphify has oriented you, or to modify/debug specific lines.
   ```

   The hook emits `graphify query` (bare form) and you cannot change that text. The CLAUDE.md rules you just appended already use the `uvx --from graphifyy graphify` form, so Claude follows those rules when it acts. The two signals are equivalent: the hook tells Claude what to do, and the CLAUDE.md rules tell Claude how to invoke it.

   **The notice itself may not be visible to you.** The hook returns it as `additionalContext`, which Claude receives but the transcript does not necessarily render. So do not wait to see the MANDATORY text, and do not use "did graphify run" as your test either, because the precedence rule legitimately sends some questions elsewhere.

   **Ask Claude instead.** It receives the notices even when you cannot see them:

   > In the message you just answered, did you receive any injected notice or additionalContext from a PreToolUse hook before making your tool calls? Quote it verbatim if you did. If you received nothing, say so plainly.

   Both hooks are working if Claude quotes both notices: the graph's `MANDATORY: graphify-out/graph.json exists...` and the wiki's `Check wiki/index.md for an article covering this area...`. **That is the signal, and it is independent of which layer Claude then chose to use.** If Claude reports receiving nothing, the hooks did not load: see rescue (f).

Now say the mechanism in your own words. You started this step with an asymmetry: the graph was enforced by a hook, the wiki was adopted by instruction. You just closed it, so **both knowledge layers have hooks now, and they are different kinds of hook.** That distinction is the thing worth carrying out of this lab. Two questions it answers directly:

- *Is graphify a hook?* Yes. It is a `PreToolUse` hook on `Bash|Grep` and `Read|Glob`. Claude cannot grep or read raw files without the hook firing and pushing it to the graph first. The `hook-guard` binary returns a directive that names the tool to run.
- *Does the wiki need a CLAUDE.md entry?* Yes. The wiki has both: a hook (the nudge you just wired in step 3) and the CLAUDE.md pointer from step 1, plus the `SCHEMA.md` contract you wrote in Step 5. But the hook is a simple nudge, not a guard. It injects a suggestion; it does not validate staleness or tailor the message to the file being read.

**You know this worked when:** after the relaunch, Claude confirms it received both hook notices when you ask, you noted whether either question needed a source file and what that told you, and you can state the difference between a hook that guards (graphify's `hook-guard`) versus a hook that nudges (the wiki hook). Which layer answered each question is the precedence rule at work, not a pass or fail, and the wiki forwarding a question to the graph counts as the rule working. Seeing the MANDATORY text yourself is a bonus, not the signal; what Claude reports receiving is the signal.

---

## Step 7 — Run the spec again, wired (14 min)

Now measure the difference. Same spec, same starting state, but this time the graph, the wiki, and the hook all exist.

1. **Start a FRESH Claude Code session** so nothing from the wiring or verify step carries into the measured run. State from an earlier session would contaminate the comparison.

2. **Confirm the starting state matches Run 1.** `git status` should show `server/` and `client/` clean (the code you discarded to in Step 1). `graphify-out/` and `wiki/` should be present; the app code should not be modified.

3. **Keep the work in this session, exactly as you did in Step 1.** Decline any offer to delegate to a subagent. Beyond keeping the two runs comparable, there is a lesson here worth carrying out of the lab: a subagent is a fresh context, so the graph and wiki orientation you wired into this session does not follow it. If you wire a real repo, the `CLAUDE.md` pointer has to reach subagent prompts too (graphify's own hook notice says as much).

4. **Hand Claude the SAME spec** (`specs/days-of-cover.md`). Notice how Claude orients itself and which layers it consults.

5. When the implementation completes, ask Claude the same retrospective question you asked in Step 1:

   > Before I look at the result: report on how you worked. How many tool calls did you make in total, and how many came before your first edit to a source file? Which distinct files did you read, and which of those did you read before your first edit? Did you search for the same thing more than once? In one sentence, how did you work out where the shared inventory filter helper lives? What did you assume about the time period the demand figure covers, and where did that assumption come from? And did you use graphify or the wiki at any point: be specific about commands run and files opened, and say plainly if you skipped either.

   Record the same proxies as Run 1. Compare the before-first-edit row first: it is the only row a structural map can move.

6. **Compare the graph against grep on the structural question.** First, run `/clear`. This matters more than it looks: you have just implemented against `server/main.py`, so its contents are already in your context and Claude will answer from memory in zero tool calls, which measures nothing. Clear the context and the question becomes a real one.

   Then ask Claude: *"Which endpoints break if I change the signature of the shared inventory filter helper?"* Note how many calls it took and which layer answered first. A run that uses both layers well needs about **three tool calls and never opens `server/main.py`**:

   1. `wiki/index.md`, following the precedence rule you wrote in Step 6
   2. `wiki/filter-system.md`, which already carried the answer and the location
   3. `uvx --from graphifyy graphify explain "apply_filters"`, to confirm the callers deterministically

   It then said it deliberately skipped the source because the wiki and the graph already agreed. **That is the only place in this lab where the two layers replace reading source rather than adding to it**, and it is worth sitting with, because it explains the result you just measured in Steps 1 and 7:

   > These layers are **substitutive when you are planning** and **additive when you are changing code.** A question can be answered without opening the source. An edit cannot, because you have to open every file you touch. Your implementation run cost more tool calls. This question cost three and zero source reads.

   **This is the lab's most transferable idea.** Most of the job is question-shaped: *Where does this live, what else calls it, what breaks if I change it, what does this field actually contain?* That is planning, and planning comes before every change you make. It is not an occasional activity, it is the first half of all of them.

   **Agentic workflows make this even more critical.** Hand a spec to an agent and it does that planning on your behalf, asking far more of those questions than you would, most of which you never see in the transcript. The payoff lands there, before the first edit is written.

   Notice too that each layer did a different job on one question. The wiki gave the location and the answer, the graph confirmed the caller set with line numbers, and the wiki volunteered something the graph structurally cannot see: the client's filter names do not match the server's parameters, so a rename has to be chased into `useFilters.js` and `api.js` as well. Neither layer alone was sufficient.

   **Now compare against text search.** First run:

   ```
   uvx --from graphifyy graphify affected "apply_filters()"
   ```

   The graph returns the resolved set. Then run:

   ```
   grep -rn "apply_filters" server/
   ```

   The shell `grep` returns your three real call sites **mixed with matches that are not your code at all**: `server/.venv/` holds the third-party libraries this project downloaded, and one of them (`pygments`) defines its own unrelated function also called `apply_filters`, alongside binary cache files and `graphify-out/`. That can come back as tens of kilobytes and get truncated to a file.

   Now ask Claude to search for the same symbol with its own Grep tool:

   > Use your Grep tool to find all references to `apply_filters` in the server directory. Compare what you find against the shell grep output I just ran.

   That tool runs ripgrep, which honours `.gitignore`, so it skips `.venv/` and returns cleanly.

   **The finding, stated fairly.** The graph answers "what references this symbol" by resolving the code. Text search answers "what contains this text." Those agree until the same name means two different things, and then only the graph is right. A well-configured search is a good and cheap answer on a repo this size. What it will not give you is the confidence that the list is complete, or the client-side naming gotcha the wiki supplied. The graph's edge is resolution, not speed, and that edge grows as a codebase accumulates repeated names, wrappers, and re-exports, which is the normal condition across 40-50 services.

7. **See how cheap maintenance is.** Your run just modified code, so the graph no longer matches the source. Refresh it:

   ```
   uvx --from graphifyy graphify update .
   ```

   Watch the clock and the output: a few seconds, AST-only, zero API tokens. That is the point of running it here. Staleness is a solvable problem rather than a reason to distrust the graph, and this is the CLAUDE.md rule from Step 6 made concrete.

   Note the ordering, because it matters more than it looks. You built the graph in Step 2 on clean code and nothing modified code until this run, so the graph was accurate for the whole measured run. No refresh was needed beforehand. If you had implemented something before measuring, the graph would have been describing code that no longer existed, and the hook would have downgraded from MANDATORY to advisory ("reading the file directly is fine"). Refresh before you measure, not just after.

8. **Check how many items got a value.** The spec says `days_of_cover` is null when a SKU has no matching demand forecast, so this tells you how much of the inventory the feature actually covers:

   ```
   cd server && uv run python -c "from fastapi.testclient import TestClient; from main import app; r=TestClient(app).get('/api/inventory').json(); print(sum(1 for i in r if i.get('days_of_cover') is not None), 'of', len(r), 'items have a value')"
   ```

   **Write the number down; the quiz asks for it.** Most inventory items have no forecast, which is why the field had to be nullable. That is F4 on the scorecard in Step 8, and it is a fixture fact rather than an implementation choice, so it does not change between your two runs.

> **Honesty, non-negotiable.** Report what you measured, including a null or a regression. A run that shows no improvement, or a worse run, is a valid result, and reporting it honestly is the measurement-discipline lesson. Do not report an absolute token count as a claim; per-session readings vary by machine. Cloud Capture's ~30% is a reference point, not a target.

**You know this worked when:** you have two sets of proxies (cold vs wired) and you recorded how many items got a `days_of_cover` value. The graph is refreshed with `uvx --from graphifyy graphify update .`.

---

## Step 8 — Correctness scorecard and measurement discipline (3 min)

This step names the key facts that realistically matter for implementing the spec, maps them to which knowledge layer can supply them, and states the findings from two human dry runs. This mirrors graphify's own published measurement axis (key-fact coverage), not token reduction. No first-party token-reduction figure exists in graphify's material.

### The key-fact scorecard

Six facts determined whether an implementation was correct and complete:

| # | Fact | Realistically learnable from |
|---|---|---|
| F1 | Inventory filtering funnels through one shared helper, `apply_filters()`, used by three endpoints (`get_inventory`, `get_orders`, `get_dashboard_summary`). Reading missed one of three. | source or graph |
| F2 | The dashboard filters inventory before counting, and already computes `low_stock_items` in the shape `at_risk_items` needs. | source |
| F3 | Client and server are joined by an HTTP call, not a static import: no call path exists between `useFilters()` and `get_inventory()`. | wiki (the graph proves the absence) |
| F4 | Demand forecasts match inventory items by SKU, and most inventory items have no matching forecast, so `days_of_cover` must be nullable. | wiki or source |
| F5 | `period` is free text in several shapes, so "a 30-day period" does not hold for every record. | wiki |
| F6 | A new column label needs a key in every locale file including `ja.js`, rendered through `t()` from `useI18n()`. | source |

### One fact worth noticing about F5

The spec states, assertively, that "a demand forecast records a demand figure covering a 30-day period." The fixture data disagrees: `period` is free text, and the values include `Next 3 months`, `Q1 2025`, `90 days`, and `Next 60 days`. So a fixed 30-day divisor computes the wrong daily rate for most records, and it does so without erroring. The numbers stay plausible and the tests still pass.

Note whether your run questioned that or coded straight to the spec. Both happen, and runs are nondeterministic, so yours is not a pass or a fail.

**The transferable point:** the wiki can record a fact and the agent can still override it, because an assertive instruction carries more weight than a note. If a fact cannot afford to be overridden, put it somewhere with teeth: a test, a schema constraint, or a corrected spec. A knowledge layer informs; it does not enforce.

### Check which layers actually got used

Review your transcript and the retrospective answers from Steps 1 and 7. Which layer answered which question, and why? Three possible outcomes:

- **Consulted and useful.** The wiki or graph answered something the other could not (the HTTP hop, the complete caller set, a data gotcha, a naming mismatch) and Claude acted on it. Note which specific fact earned its keep.
- **Consulted and not useful.** Claude opened the knowledge layer and went to source anyway. That is a lesson about **what belongs in an article or when to query the graph**, which is more useful than a lesson about tools. Note what should have been recorded or asked differently.
- **Not consulted at all, despite the hook.** The wiki hook nudges, but graphify's `hook-guard` returns a directive. At 53 files with a good wiki, Claude may get its orientation entirely from the wiki and skip graphify for the implementation run. That is a valid outcome: the wiki answered completely, so no structural gap remained. It is also evidence of the asymmetry you wired in Step 6.

### Run graphify's benchmark and read it honestly

```
uvx --from graphifyy graphify benchmark
```

Read the methodology it prints and notice the baseline: stuffing the entire repo corpus into context. No competent agent does that, and it is not what your cold run did either. So the ~20x is measured against something nobody would do. Your own before/after compares two real runs of the same spec on the same repo.

Cloud Capture measured roughly 30% fewer tokens on a deliberately simple task (up to ~50% in some spec-kit phases), with their stated caveats, and found the vendor's 70% claim "didn't stand true." Hold your own result to that same standard: if your wired run did not beat your cold run, that is a valid result.

**Notice that their number varied by phase, and think about why.** spec-kit splits work into specify, plan, tasks, and implement. The first three are question-shaped and the last one is edit-shaped, which is exactly the split you measured in Step 7. If their strongest phases were the planning ones, your own result explains the variance rather than contradicting it. 

### Scale-limit honesty

Two caveats so you read your own result correctly:

- **A knowledge layer can point at the right file and still not save a read.** It tells you *where* to look. If you then read the file anyway to confirm line-level detail, it added a step rather than replacing one. That happens when you are about to edit the file, because you cannot avoid opening what you change. It does not happen when you are only asking, which is why the structural question in Step 7 cost three calls and no source read at all. Whether these layers substitute or merely add depends on whether you are planning or changing code.
- **This repo is 53 files.** graphify's own honest benchmark measured coverage gains on a codebase near a million lines. A demo repo caps how much orientation there is to save, so a thin delta here is not evidence the approach fails at scale, and a large delta here would not prove it succeeds.

**You know this worked when:** you can state the key-fact scorecard, say why a knowledge layer informs rather than enforces, and identify which layers your runs consulted and whether they were useful.

---

## Step 9 — Defend which knowledge layer answers which question (3 min)

Pose two questions of different shapes and note which knowledge layer answers each:

- "What breaks if I change `apply_filters()`?" (structural)
- "Why does joining an inventory item to its demand forecast require knowing two different field names?" (a data-shape convention)

**The first is the graph's territory.** `uvx --from graphifyy graphify affected "apply_filters()"` lists every caller in one command, and after your spec work that now spans two endpoints. Because `SCHEMA.md` forbade the wiki from recording caller lists, the wiki has nothing to offer here and should either send you to the graph or stay silent.

**The second is the wiki's territory.** Inventory items carry `sku`; every dataset that references an inventory item (demand forecasts, backlog items) calls the same value `item_sku`. So any code joining across them has to know both names, and **there is no single field name you can grep for.** The graph cannot tell you this: it resolves symbols, and these are string keys in two JSON files that never reference each other in code.

That second one is worth sitting with, because it is the same limitation you saw in Step 7's grep comparison arriving from the other direction. Text search fails because the name differs. The graph fails because there is no symbol relationship to resolve. A human noticed the mismatch once and wrote it down, and that note is the only thing that answers the question.

**You know this worked when:** you can say which layer answered each question and why, and you can name at least one question in this codebase that neither the graph nor a text search can answer, only a note a human left behind.

---

## Step 10 — Teardown (2 min)

Confirm the lab left zero global state. Run both commands:

```
grep -c graphify ~/.claude/CLAUDE.md
```
```
test -d ~/.claude/skills/graphify/ && echo "FAIL" || echo "clean"
```

Both should return `0` and `clean` respectively.

**You know this worked when:** the two verification commands return clean.

---

## Reference values (Step 2 extract output)

These are reference values from a verified run. **Your numbers may differ by a few** — the repo drifts. Expect a summary line similar to:

```
[graphify extract] found 53 code, 0 docs, 0 papers, 0 images
[graphify extract] wrote graph.json: 314 nodes, 417 edges, 28 communities
```

Reference: 53 code files, 314 nodes, 417 edges, 28 communities.

For the `export wiki` sub-step in Step 2: it produces 38 articles, of which 28 are named `Community_0.md` through `Community_27.md`, plus 10 auto-named god-node articles.

Your Step 2 success signal still holds if your node count lands in the 250-400 range. The run should take 3-4 seconds with zero API tokens.

For Step 8, the `benchmark` reference output:

```
Corpus:          ~20,800 tokens (naive)
Graph:           314 nodes, 417 edges
Avg query cost:  ~1,035 tokens
Reduction:       ~20x fewer tokens per query
```

---

## Done criteria

You're done when all eight are true:

1. You ran `specs/days-of-cover.md` cold (Step 1), recorded the baseline proxies, and fully discarded the code changes (`git checkout -- .` plus `git clean -fd server client`, leaving no untracked files behind).
2. `graphify extract . --code-only` produced a graph and you recorded your own counts.
3. You ran `path "useFilters()" "get_inventory()"` and can explain "No path found" in one sentence.
4. `graphify-out/wiki/` exists and you saw the `Community_N` naming.
5. `wiki/` holds `SCHEMA.md` (which you reviewed), `index.md`, an append-only `log.md`, and at least one topic-named article, with log lines appended, none rewritten.
6. You wired both knowledge layers into Claude: the graphify section in `./CLAUDE.md`, the PreToolUse hooks in `.claude/settings.json`, relaunched, and verified a hook fired.
7. You ran the same spec wired (Step 7) in a fresh session, recorded the proxies, and observed which layers Claude consulted and how the implementations differed.
8. Step 10 teardown confirms no graphify global state was written.

---

## Extra credit (not required)

1. **Run the `label` subcommand (requires an LLM backend).** If you have an AWS Bedrock configuration (boto3 + credentials) or an `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` env var, run:

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

**(f) The hook does not fire after Step 6.**

First make sure you have the right problem. **Claude choosing the wiki over graphify is not a hook failure**, it is the precedence rule you wrote. You are in this rescue path only if Claude reports receiving no hook notice at all when you ask it.

Confirm the commands themselves work, outside any session:

```
echo '{"tool_name":"Read","tool_input":{"file_path":"server/main.py"}}' | uvx --from graphifyy graphify hook-guard read
bash .claude/hooks/pre-tool-use-wiki.sh
```

The first should print a `MANDATORY` notice, the second a line of JSON mentioning `wiki/index.md`. If the first says the graph "may be STALE" instead, rebuild it (`uvx --from graphifyy graphify extract . --code-only`); a stale graph downgrades the guard to advisory. If both commands work but Claude still receives nothing, the wiring is the problem, so check three things, in order: (1) `.claude/settings.json` must be valid JSON, where a trailing comma or a missing brace silently disables the hooks. (2) You must have relaunched Claude Code after writing the file; hooks load at startup. (3) `graphify-out/graph.json` must exist — the hook-guard only fires when the graph is present, so if you removed or never built it, rebuild with `uvx --from graphifyy graphify extract . --code-only`. Fix whichever applies, relaunch, and ask a codebase question again.

---

Your completion and mastery assessments are in the LMS.
