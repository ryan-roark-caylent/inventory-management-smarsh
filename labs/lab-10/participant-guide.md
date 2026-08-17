# Lab 10: Code Knowledge Base

**Extra lab (post-programme, async) | AI Teammate | Depends on: Labs 1-9**

Cloud Capture, a Smarsh team running spec-kit on brownfield repos, hit a hard limit: their codebases "have existed forever," and spec-kit assumes greenfield. To give agents the context they needed without stuffing the whole corpus into context, they built two artifacts: a deterministic code graph and a wiki generated from code. Their reasoning: the code is true, comments may lie, docs lie more, the original spec lies most. "The further you get away from the code, the more lies you accumulate." On a deliberately simple task they measured roughly 30% fewer tokens (up to ~50% in some spec-kit phases), and their reviewers noted slightly better code quality with the graph, which they flagged as unvalidated and accidental. Less context hunting leaves more of the agent's attention on the actual task.

graphify and the code-derived LLM wiki are the tools Cloud Capture chose. Other tools cover the same ground: other AST and code-intelligence tools, embedding/vector RAG over a repo, hand-maintained knowledge bases, and IDE-native indexes. This lab does not evaluate the tool landscape and is not a procurement recommendation. The transferable outcome is the judgment these tools embody, not the specific binaries. A cheap, deterministic structural map lets an agent navigate instead of hunt. A maintained knowledge layer records what the code cannot state about itself: runtime behavior, conventions, and the reasons behind decisions. The real skill is knowing where each adds value on a repo you own.

You'll build both artifacts on the inventory-management fork, wire them into Claude, and prove the difference with the same spec run twice: once cold, once wired. Then you write down which artifact answers which question and why.

---

## Where the concept clicks

Step 4 is the moment. You'll ask graphify to trace the path from the Vue filter composable to the FastAPI function that serves inventory data, and get back "No path found." This is correct, not broken. The graph models static imports and calls. The HTTP boundary between client and server is invisible to the AST by design. Once that lands, the wiki's reason to exist is obvious: it records the runtime facts the graph structurally cannot see. The defend step in Step 9 becomes easy instead of arbitrary.

**A note on scale.** This is a 52-file repo and `CLAUDE.md` already supplies orientation, so **expect a thin token delta or none**. graphify's gains were measured near a million lines, and Cloud Capture runs 40-50 microservices. The real evidence in this lab is the correctness scorecard and the demand-forecast period trap, not a token count. A lab that manufactured a token win would be lying to you.

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

> **We never run `graphify install` in this lab.** graphify's installer writes user-global state: `~/.claude/skills/graphify/` and a `# graphify` section in `~/.claude/CLAUDE.md` that `graphify uninstall` does NOT remove. It also hardcodes an absolute path to the graphify binary, which breaks on any other machine. That violates the project-scope rule. This lab invokes graphify only through `uvx --from graphifyy graphify ...`, which resolves the package per-run and writes zero global config. In Step 6 you wire the same integration by hand, at project scope, for the same reason. After the lab, verify: `grep -c graphify ~/.claude/CLAUDE.md` returns `0`, and `~/.claude/skills/graphify/` does not exist.

**You know this worked when:** `graphify --version` prints through `uvx` with no install step, and `.claude/settings.local.json` is absent from `ls .claude/`.

---

## Step 1 — Run the spec, cold (13 min)

Before you build anything, measure the baseline. You hand Claude a small spec on the untouched repo, watch how it orients itself, then throw the code changes away. The recording is the keeper, not the code.

Use the fresh session you relaunched in Step 0. No graph, no wiki, no hook exists yet. That is the point.

1. Hand Claude the spec at `specs/days-of-cover.md`. Do not read it closely yourself first, and do not add file paths or hints when you hand it over. The spec deliberately states intent without naming locations, because **the orientation work is the thing being measured.** Telling Claude where to look would remove the very cost the graph and wiki are supposed to reduce, and both runs would come out flat.

   What it asks for, at a level that spoils nothing: a computed "days of cover" value on inventory data, a related count on the dashboard, and the value surfaced as a translatable column in the UI. It is greenfield (no such concept exists in the repo yet), it spans server and client, and it requires finding a shared helper and an existing convention on its own.

2. **Keep the work in this session (same rule as Step 7).** If Claude offers to delegate part of the task to a subagent, decline. A subagent is a fresh context, so its tool calls never appear in your count. If you allow delegation here and not in Step 7 (or the reverse), the two runs are measuring different things and the comparison is void. Whatever you do here, do the same there.

3. Notice how Claude orients itself as it works. Take a `/context` reading before and after as a directional signal (not a precise number).

4. When the implementation completes, ask Claude this retrospective question before you inspect the result:

   > Before I look at the result: report on how you worked. How many tool calls did you make in total, and how many came before your first edit to a source file? Which distinct files did you read, and which of those did you read before your first edit? Did you search for the same thing more than once? In one sentence, how did you work out where the shared inventory filter helper lives? What did you assume about the time period the demand figure covers, and where did that assumption come from? And did you use graphify or the wiki at any point: be specific about commands run and files opened, and say plainly if you skipped either.

   Record: total calls, calls before first edit, distinct files read, distinct files read before first edit, repeated-search yes/no. These are self-reported and approximate, which is acceptable because both runs are measured identically and the reading is directional, not precise.

5. Save the cold implementation before discarding it, so Step 8 has both runs to compare:

   ```
   git diff > ../cold-run.patch
   git status --porcelain > ../cold-run-untracked.txt
   ```

6. Then DISCARD the code changes so Run 2 starts from the identical state:

   ```
   git checkout -- .
   git clean -fd server client
   git status
   ```

   `git checkout -- .` restores tracked files to their committed state; the spec file is committed, so it survives. `git clean -fd server client` deletes anything Claude newly created under those directories (a scratch module, a new test file, a new component). Untracked files survive `git checkout` and would otherwise carry into the wired run and invalidate the comparison. `graphify-out/` does not exist yet. `git status` should show `server/` and `client/` clean with no untracked files under either.

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

**You know this worked when:** `god-nodes` shows `useI18n()` at the top. Both `useFilters()` commands return the same 6 views plus `FilterBar.vue`, `App.vue`, and `main.js` (16 connections), but `explain` labels the edge types and includes the symbol's own outbound references, while `affected` gives you only the blast radius. `Reports.vue`, the 7th view, does not import `useFilters` and is correctly absent from both. A plain text search for "useFilters" finds the import lines but not this resolved dependency set.

---

## Step 4 — The discovery beat (POINT STEP) (9 min)

**First, see `path` succeed**, so you know what a hit looks like and can trust the miss that follows. Both of these stay inside one language:

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

## Step 5 — Build the LLM wiki (14 min)

Build the second artifact: a three-layer LLM wiki (not to be confused with Lab 3's three-layer CLAUDE.md, a different idea using the same word; here the three layers are immutable raw sources, LLM-written articles, and a schema-maintainer file). This is Cloud Capture's adaptation of Karpathy's curated-document pattern applied to source code because docs rot.

The pattern is: **you read it, the LLM writes it.** So Claude creates and maintains the files. Your job is to set the rules and verify the discipline held. Directing and reviewing is the work; transcription is not.

1. **Author the rules yourself.** Write `wiki/SCHEMA.md`, the maintainer contract: when the agent ADDs a new article vs UPDATEs an existing one, and the rule that the code is always ground truth. This judgment is yours, not Claude's. It is the part you own.

2. **Direct Claude to create the rest** from the actual source files:
   - `wiki/index.md` — the article index and a note on when to reach for the wiki vs the graph.
   - `wiki/log.md` — an append-only change log, one line per add or update.
   - One article covering **the inventory and demand-forecast area** — the same subsystem `specs/days-of-cover.md` asks you to change in Step 7. This targeting is deliberate; see the note below. It should record what the graph cannot see:
     - How the inventory endpoint's response reaches the table in the UI (the HTTP hop between `api.js` and the server)
     - That inventory filtering funnels through one shared helper several endpoints depend on
     - How the demand-forecast records relate to inventory items: matched by SKU, and what the `period` field actually contains. Check the fixture data and the demand view's `translatePeriod` before you write this down, and record what you find rather than what you expect.
     - The dashboard's existing pattern for counting a subset of filtered inventory (one already exists; name it)
     - The i18n convention for a new column label: where locale strings live, which locales must receive the key, and how a header reaches the translation helper
     - Any naming mismatch between what the client calls a field and what the API calls it

> **Why this article and not another.** A wiki with one article can only help with a question that article happens to cover. Point it at the subsystem you are about to modify and the wiki gets a fair test in Step 7. Point it somewhere else and you learn nothing except that a thin wiki misses. Cloud Capture's wiki covers their whole codebase, so theirs gets consulted as a matter of course; yours will cover one corner. You are testing the mechanism at lab scale, not experiencing the benefit at production scale. Choose the corner that matters.

3. **Tell Claude to append a matching entry to `log.md`** in the same pass, and never rewrite a line once written.

4. **Verify the append discipline held.** Confirm `log.md` grew by appended lines and none were rewritten. This check is yours.

Shapes to fill in, not answers to copy: thin skeletons for all four files are planted at `wiki/TEMPLATES.md`. Use them to see the structure. Do not paste them wholesale. (The rescue checkout in "If you're stuck" hands over a *finished* wiki, which is a different thing: an answer to adapt, not a shape to fill.)

**You know this worked when:** `wiki/` holds `SCHEMA.md` (the rules you wrote), `index.md`, `log.md`, and at least one topic-named article (not named `Community_N.md`). `log.md` shows one appended line per add or update, with none rewritten.

---

## Step 6 — Wire the graph into Claude (13 min)

Until now you have run graphify by hand in the terminal. Claude does not know the graph exists. This step wires both artifacts into the project so Claude reaches for them on its own.

You do this by hand, at PROJECT scope, rather than running `graphify install`, for the reason given in Step 0: the installer writes user-global state and hardcodes an absolute path to the graphify binary that would not work on your machine. Wiring it yourself also means you see the config instead of an installer hiding it.

Two mechanisms, one per artifact:

1. **Tell Claude about the graph and wiki.** Append this block to the project CLAUDE.md at the repo root (`./CLAUDE.md`; create it if there is none):

   ```
   ## Code knowledge sources: precedence

   This project has two knowledge layers over the same codebase. They answer different questions, so the order you consult them matters.

   **1. The wiki (`wiki/index.md`) — for "how does this work" and "where does X live".**
   Before reading source files to understand how a feature behaves, check `wiki/index.md` and read any article covering that area. The wiki records what the code cannot state about itself: runtime behavior, cross-boundary contracts (like the HTTP seam between client and server), naming mismatches, and the reasons behind conventions. See `wiki/SCHEMA.md` for the maintainer contract. Distinct from the auto-generated per-community notes under `graphify-out/wiki/`.

   **2. The graph (graphify) — for symbol-level relationships and call chains.**
   Run `uvx --from graphifyy graphify query "<question>"` for a scoped subgraph, `uvx --from graphifyy graphify path "<A>" "<B>"` to trace a relationship between two symbols, and `uvx --from graphifyy graphify explain "<concept>"` for one symbol's neighborhood. These return far less than `GRAPH_REPORT.md` or raw grep. The graph is deterministic AST output: it knows every import and call, and nothing about runtime behavior or network hops.

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

5. **Verify the hooks fire.** In the relaunched session, ask Claude a codebase question that would normally send it grepping (for example, ask where inventory filtering is handled). Watch for one of two signals: Claude runs `uvx --from graphifyy graphify query` instead of grepping, or the PreToolUse hook injects its notice:

   ```
   MANDATORY: graphify-out/graph.json exists. You MUST run `graphify query "<question>"` before grepping raw files. Only grep after graphify has oriented you, or to modify/debug specific lines.
   ```

   The hook emits `graphify query` (bare form) and you cannot change that text. The CLAUDE.md rules you just appended already use the `uvx --from graphifyy graphify` form, so Claude follows those rules when it acts. The two signals are equivalent: the hook tells Claude what to do, and the CLAUDE.md rules tell Claude how to invoke it.

   **The notice itself may not be visible to you.** The hook returns it as `additionalContext`, which Claude receives but the transcript does not necessarily render. So do not wait to see the MANDATORY text. **The observable signal is Claude running a `graphify query` / `explain` / `path` call BEFORE it reads a source file.** That ordering is the proof the hook fired and was obeyed.

Now say the mechanism in your own words. You started this step with an asymmetry: the graph was enforced by a hook, the wiki was adopted by instruction. You just closed it, so **both artifacts have hooks now, and they are different kinds of hook.** That distinction is the thing worth carrying out of this lab. Two questions it answers directly:

- *Is graphify a hook?* Yes. It is a `PreToolUse` hook on `Bash|Grep` and `Read|Glob`. Claude cannot grep or read raw files without the hook firing and pushing it to the graph first. The `hook-guard` binary returns a directive that names the tool to run.
- *Does the wiki need a CLAUDE.md entry?* Yes. The wiki has both: a hook (the nudge you just wired in step 3) and the CLAUDE.md pointer from step 1, plus the `SCHEMA.md` contract you wrote in Step 5. But the hook is a simple nudge, not a guard. It injects a suggestion; it does not validate staleness or tailor the message to the file being read.

**You know this worked when:** after the relaunch, you ask a codebase question and Claude runs a `uvx --from graphifyy graphify query` (or `explain` / `path`) call BEFORE reading any source file, and you can state the difference between a hook that guards (graphify's `hook-guard`) versus a hook that nudges (the wiki hook). Seeing the MANDATORY text is a bonus, not the signal; the call ordering is the signal.

---

## Step 7 — Run the spec again, wired (17 min)

Now measure the difference. Same spec, same starting state, but this time the graph, the wiki, and the hook all exist.

1. **Start a FRESH Claude Code session** so nothing from the wiring or verify step carries into the measured run. State from an earlier session would contaminate the comparison.

2. **Confirm the starting state matches Run 1.** `git status` should show `server/` and `client/` clean (the code you discarded to in Step 1). `graphify-out/` and `wiki/` should be present; the app code should not be modified.

3. **Keep the work in this session, exactly as you did in Step 1.** Decline any offer to delegate to a subagent. Beyond keeping the two runs comparable, there is a lesson here worth carrying out of the lab: a subagent is a fresh context, so the graph and wiki orientation you wired into this session does not follow it. If you wire a real repo, the `CLAUDE.md` pointer has to reach subagent prompts too (graphify's own hook notice says as much).

4. **Hand Claude the SAME spec** (`specs/days-of-cover.md`). Notice how Claude orients itself. Take a `/context` reading before and after. The hook should visibly push Claude toward `uvx --from graphifyy graphify query` before it greps.

5. When the implementation completes, ask Claude the same retrospective question you asked in Step 1:

   > Before I look at the result: report on how you worked. How many tool calls did you make in total, and how many came before your first edit to a source file? Which distinct files did you read, and which of those did you read before your first edit? Did you search for the same thing more than once? In one sentence, how did you work out where the shared inventory filter helper lives? What did you assume about the time period the demand figure covers, and where did that assumption come from? And did you use graphify or the wiki at any point: be specific about commands run and files opened, and say plainly if you skipped either.

   Record the same proxies as Run 1. Compare the before-first-edit row first: it is the only row a structural map can move.

6. **Compare the graph against grep on the structural question.** Ask Claude: *"Which endpoints break if I change the signature of the shared inventory filter helper?"* Note how many calls it took and whether the hook pushed it to the graph first.

   Then answer it yourself, both ways:

   ```
   uvx --from graphifyy graphify affected "apply_filters()"
   grep -rn "apply_filters" server/
   ```

   Record the honest finding: **on a 52-file repo with a single server module, one ripgrep wins.** Then explain the flip. Grep is a complete reverse-dependency engine only when you already know which directory to search and every call site spells the symbol the same way. It degrades on aliased imports, re-export chains, wrapper indirection, and a name that means two different things in two languages. Those are the normal conditions in 40-50 microservices, and they are why the ratio inverts at Cloud Capture's scale and not here.

7. **See how cheap maintenance is.** Your run just modified code, so the graph no longer matches the source. Refresh it:

   ```
   uvx --from graphifyy graphify update .
   ```

   Watch the clock and the output: a few seconds, AST-only, zero API tokens. That is the point of running it here. Staleness is a solvable problem rather than a reason to distrust the graph, and this is the CLAUDE.md rule from Step 6 made concrete.

   Note the ordering, because it matters more than it looks. You built the graph in Step 2 on clean code and nothing modified code until this run, so the graph was accurate for the whole measured run. No refresh was needed beforehand. If you had implemented something before measuring, the graph would have been describing code that no longer existed, and the hook would have downgraded from MANDATORY to advisory ("reading the file directly is fine"). Refresh before you measure, not just after.

8. **Write the comparison.** What changed in HOW Claude oriented itself between the cold run and the wired run, not just token counts. This comparison is the deliverable and feeds your share-back.

> **Honesty, non-negotiable.** Report what you measured, including a null or a regression. A run that shows no improvement, or a worse run, is a valid result, and reporting it honestly is the measurement-discipline lesson. Do not report an absolute token count as a claim; per-session readings vary by machine. Cloud Capture's ~30% is a reference point, not a target.

**You know this worked when:** you have two sets of proxies (cold vs wired) and one or two sentences on what changed in Claude's orientation. The graph is refreshed with `uvx --from graphifyy graphify update .`.

---

## Step 8 — Correctness scorecard and measurement discipline (8 min)

Score both runs against the key facts that realistically matter for implementing the spec. This mirrors graphify's own published measurement axis (key-fact coverage), not token reduction. No first-party token-reduction figure exists in graphify's material.

### Score the key-fact coverage

Use your retrospective answers from Steps 1 and 7 to score each run out of 6:

| # | Fact | Realistically learnable from |
|---|---|---|
| F1 | Inventory filtering funnels through one shared helper, `apply_filters()`, used by three endpoints (`get_inventory`, `get_orders`, `get_dashboard_summary`). | source or graph |
| F2 | The dashboard filters inventory before counting, and already computes `low_stock_items` in the shape `at_risk_items` needs. | source |
| F3 | Client and server are joined by an HTTP call, not a static import: no call path exists between `useFilters()` and `get_inventory()`. | wiki (the graph proves the absence) |
| F4 | The client's internal `selectedPeriod` becomes the API's `month` parameter. The names differ across the seam. | wiki |
| F5 | `period` is free text in several shapes, so "a 30-day period" does not hold for every record. | wiki |
| F6 | A new column label needs a key in every locale file including `ja.js`, rendered through `t()` from `useI18n()`. | source |

Record which facts each run captured before implementing. The cold run has no access to the wiki, so F3, F4, and F5 are structurally unreachable there unless Claude opened the fixture data and client code on its own.

### Compare the two implementations

Apply your cold patch to a scratch copy and compare the `days_of_cover` values it produces against what your wired run produced, for the SKUs whose forecast period is not 30 days (ids 2, 4, 6, 8, 9).

If the cold run divided by 30 and the wired run carried F5, **the same spec produced different numbers for the same input, and one of them is wrong.** That is the demonstration. The computation is exercisable from the backend test path; no app boot required.

### Check which layers actually got used

Review your transcript and the retrospective answers. Three outcomes, and each teaches something different:

- **Consulted and useful.** The wiki answered something the graph could not (the HTTP hop, the SKU relationship, the period trap, a naming mismatch) and Claude acted on it. The pattern works at this scale. Note which specific fact earned its keep.
- **Consulted and not useful.** Claude opened the article and went to the source anyway. That is a lesson about **what belongs in an article**, which is more useful than a lesson about tools. Your article recorded things that were already obvious from the code, or omitted the one thing that was not. Name what it should have said.
- **Not consulted at all.** The wiki hook fired on every read (you wired it in Step 6), yet Claude went to source anyway. A nudge injects a suggestion; graphify's `hook-guard` returns a directive that names the tool to run. The lesson is the difference between a hook that fires and a hook that knows something. That is the gap you saw in Step 6.

### Run graphify's benchmark and read it honestly

```
uvx --from graphifyy graphify benchmark
```

Read the methodology it prints and notice the baseline: stuffing the entire repo corpus into context. No competent agent does that, and it is not what your cold run did either. So the ~20x is measured against something nobody would do. Your own before/after compares two real runs of the same spec on the same repo.

Cloud Capture measured roughly 30% fewer tokens on a deliberately simple task (up to ~50% in some spec-kit phases), with their stated caveats, and found the vendor's 70% claim "didn't stand true." Hold your own result to that same standard: if your wired run did not beat your cold run, that is a valid result and it goes into your exit note as-is.

### Scale-limit honesty

Two caveats so you read your own result correctly:

- **The graph can point at the right files and still not save a read.** A structural map tells you *where* to look. If you then read the file anyway to confirm line-level detail, the graph added a step rather than replacing one. That is a real and common outcome; it means the graph's value is orientation, not substitution.
- **This repo is 52 files.** graphify's own honest benchmark measured coverage gains on a codebase near a million lines. A demo repo caps how much orientation there is to save, so a thin delta here is not evidence the approach fails at scale, and a large delta here would not prove it succeeds.

**You know this worked when:** you have scored both runs out of 6 on the key-fact table, compared the two implementations' `days_of_cover` values for non-30-day forecasts, and identified which of the three consultation outcomes you got. This reasoning feeds your exit note.

---

## Step 9 — Defend which artifact answers which question (5 min)

Pose two questions of different shapes:

- "What breaks if I change `apply_filters()`?" (structural, static — the graph's territory, and note your new spec work made this a live concern across two endpoints)
- "Why does the app's locale persist across page reloads?" (runtime behavior the graph cannot see — the wiki's territory)

Write `KB-DECISION.md` at the repo root. For each question, name which artifact you reached for and one sentence defending why.

**You know this worked when:** `KB-DECISION.md` records one artifact choice per question with a reason. The structural question points at the graph (`affected "apply_filters"` lists callers in one command, and now spans both endpoints). The runtime question points at the wiki (locale persistence is `localStorage`, which the graph never sees). The solution branch has a reference exemplar once you have written your own.

---

## Step 10 — Teardown and share-back (4 min)

Confirm the lab left zero global state. Run both commands:

```
grep -c graphify ~/.claude/CLAUDE.md
```
```
test -d ~/.claude/skills/graphify/ && echo "FAIL" || echo "clean"
```

Both should return `0` and `clean` respectively.

Write an async exit note (Slack thread to the peer channel, or a private doc) with four things:

1. Your own `extract` summary line and one god-node you found non-obvious.
2. Your cold-vs-wired comparison from Steps 1 and 7: what changed in how Claude oriented itself, reported honestly (including a null or negative result if that is what you saw).
3. Which artifact you chose for each of the two Step-9 questions, with one sentence defending each.
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

For Step 8, the `benchmark` reference output:

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
7. You ran the same spec wired (Step 7) in a fresh session and recorded the cold-vs-wired comparison.
8. `KB-DECISION.md` records a graph choice and a wiki choice with reasons.
9. Step 10 teardown confirms no graphify global state was written.

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

Check three things, in order: (1) `.claude/settings.json` must be valid JSON — a trailing comma or a missing brace silently disables the hooks. (2) You must have relaunched Claude Code after writing the file; hooks load at startup. (3) `graphify-out/graph.json` must exist — the hook-guard only fires when the graph is present, so if you removed or never built it, rebuild with `uvx --from graphifyy graphify extract . --code-only`. Fix whichever applies, relaunch, and ask a codebase question again.

---

Your completion and mastery assessments are in the LMS.
