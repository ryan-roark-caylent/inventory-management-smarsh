# Lab 9: Team Adoption and Champion Handover

**Track 3 (AI Teammate) | Lab 9 of 9 | Depends on: Labs 6, 7, 8**

Adoption is a portable artifact you hand off, not a feeling you report. This lab closes the programme by turning your personal Claude skills into things your team can pick up and use: a library entry a teammate can run cold, a subagent anyone can invoke by name, and a handoff note specific enough for a teammate to hold you to. You keep all three in your worktree and carry them back to your team. Nothing is committed to the repo.

You'll work entirely in the Claude Code terminal. No app server and no browser are needed on the core path.

Your completion and mastery quizzes are in the LMS.

---

## What this lab proves

Most programme rollouts fail on the bridge back to Monday: no plan, no library, no champion, so engineers revert to old habits under sprint pressure. A Smarsh champion's job is to keep the good path the easy path. A curated library other engineers pull from, a subagent other engineers invoke by name, and a plan someone can check: this lab produces those three artifacts against the real repo.

This lab runs longer than a 101 exercise because it carries competencies with zero Academy coverage: library curation behind a quality gate, subagent authoring, and adoption planning.

---

## Where the concept clicks

Step 1 is the moment. You'll cold-run two seeded library entries in separate fresh sessions, standing in for a teammate who has never seen this repo. The question you're answering: an entry worked for YOU because you had the repo in your head; will it work COLD for someone who doesn't? That gap is the quality gate. Everything else in the lab builds on what you see there.

---

## Track callback (Labs 6, 7, 8)

In Lab 6 you built and triggered a skill and applied the 5-abstraction rubric (CLAUDE.md / skill / hook / subagent / MCP). In Lab 7 you invoked pre-built subagents and saw how scoping narrows what a model can reach. In Lab 8 you ran the 5-point review checklist and made a Trust-Spectrum call with a cited justification. This lab turns those personal skills into team assets: you contribute one to a shared library behind a quality gate, you author a new subagent, and you write the note that keeps the team using them.

---

## Step 0 — Confirm your worktree and orient

You work this lab inside its own git **worktree** so nothing collides with other labs and you keep your work at the end. If your pre-work already created `lab-9-work`, confirm you're in it with `git worktree list`. If not, create it now — run each line separately:

> **Tip:** you can run a shell command without leaving Claude Code by prefixing it with `!` (e.g. `!git worktree list`). Handy throughout the labs.

```
git fetch origin
git worktree add ../lab-9-work lab-9-start
cd ../lab-9-work
```

Then launch Claude Code from inside `lab-9-work`. (The worktree rule is also in this repo's `CLAUDE.md`.)

Confirm your setup:

```
git worktree list
```
```
git status
```

You should see you're on `lab-9-work` with a clean tree.

1. **Switch to Sonnet.** Smarsh defaults to Haiku; this lab is tuned for Sonnet. Run `/model sonnet` (or `/model` and pick Sonnet). The Step 1 behaviors assume Sonnet.

2. Open `PROMPT-LIBRARY.md` at the repo root. Read both seeded entries and the `## How to add an entry` template block.

3. Open `docs/lab-9/candidate-prompts.md` for the reuse/reliability rubric and three candidate prompts you can draw from in Step 2.

**You know you're oriented when:** `PROMPT-LIBRARY.md` shows exactly two entries — `gen-endpoint-tests` (a complete one) and `quick-review` (a deliberately thin one) — under a `## How to add an entry` template block, and you understand the rubric scores reuse and reliability 0-2 each.

Expected library header:
```
$ head -30 PROMPT-LIBRARY.md
# Prompt & Command Library

Shared, peer-tested prompts for this repo. An entry earns a place only if a
teammate can run it COLD and get the same result the author got.

## How to add an entry
The library is an INDEX. It tells a teammate what reusable Claude assets exist
and how to reach them...

## Entries

### gen-endpoint-tests   (strong example)
...
### quick-review   (weak example — do not copy this shape)
...
```

> **Docs pointer:** anything this card references as "see the pre-work" lives in your **MindTickle pre-work module**, not in this repo.

---

## Step 1 — Prove it transfers cold (POINT STEP)

The question this step answers: **an entry worked for YOU because you had the repo in your head. Will it work COLD for a teammate who doesn't?** That's the bar for putting anything in a shared library.

1. Start a **fresh** Claude Code session (`claude`) at the repo root. Load no files and give no other context — you're standing in for a teammate who has never seen this repo's specifics.

2. Open `PROMPT-LIBRARY.md` at the repo root and find the **weak** seeded entry, `quick-review` (under `## Entries`, marked "weak example"). Copy its **Body** block, paste it into the fresh session exactly as written, and run it. Note precisely what Claude had to GUESS to proceed — which file, which checklist, which output shape — and whether you could predict the same guess would happen on someone else's machine.

3. Start another fresh session (quit and relaunch `claude`). From `PROMPT-LIBRARY.md`, copy the **Body** of the **strong** entry, `gen-endpoint-tests` (marked "strong example"), and paste it exactly as written. Note what it did NOT have to guess.

4. Rate each entry on **reuse** (does it generalize past one case?) and **reliability** (does it produce the intended result cold, without guessing?) using the rubric in `docs/lab-9/candidate-prompts.md`. Think through the specific context the weak entry made Claude supply on its own — the thing that would differ for a teammate — then move on.

**You know this worked when:** you can point to at least one thing the weak entry forced Claude to infer (a target, a checklist, or an output format) and explain why that inference is a transfer risk even if the run "looked fine," and you can say why the strong entry has no such gap.

> A capable model may produce a usable result from the weak entry by inferring a target — for example, inspecting recent git history and reviewing the last-touched file. That's the point, not a bug. Reliability here means "no guessing required," not "it errored." On a teammate's machine with different history, that silent guess changes.

> **Teach-the-feature:** starting a truly fresh session matters here. If you keep files open or context loaded, you're not simulating a cold teammate. Quit and relaunch `claude` between the two runs.

Expected behavior:
> **Weak entry, cold session** — Claude proceeds by INFERRING a target: "I'll review the most recently changed file, `server/main.py` — here's what I found…" You never told it which file; it guessed.
> **Strong entry, cold session** — Claude produces `tests/backend/test_inventory_filters.py` with no guessing, because the entry named the endpoint, the cases, the pattern file, and the output format. Same result for anyone who runs it.

---

## Step 2 — Build one shareable item and register it

1. Pick **one** item you'd genuinely recommend to a teammate — one of `docs/lab-9/candidate-prompts.md`, or something of your own from an earlier lab. Decide its **form**: a reusable **prompt**, a slash **command** (`.claude/commands/`), a **skill** (`.claude/skills/`), or a **CLAUDE.md rule**. Apply the scale test: what if 10,000 of these lived in a long-lived monorepo?

   Note: Lab 6's full rubric also includes hook, subagent, and MCP. Those are valid in that broader context but do not map to shareable library entries. You'll author a proper subagent in Step 3.

2. **Build and run it once.** Ask Claude to help you author your chosen form (drive Claude — don't hand-write it), then execute it on a real target in this repo to confirm it works cold and does what you intend.

   As you build, apply the Step 1 lesson directly: bake in the context a teammate would NOT have in their head. The strong entry ran cold because it named its target, its cases, its pattern file, and its output format — yours needs that same specificity, or it will only work for you because you had this repo open. Name the concrete thing (endpoint, file, format), don't assume it.

3. **Register a pointer in `PROMPT-LIBRARY.md`.** The library is an INDEX, not a store of definitions:
   - If your item is a **prompt**, put the prompt body inline in the entry.
   - If it's a **command / skill / CLAUDE.md rule**, put a one-line pointer to where it lives (e.g. `See .claude/commands/<name>.md`) — do NOT paste the definition into the library.

   Every entry carries: a name, when to use it, the pointer (inline body or path), one example of expected output, and a one-line note on the form you chose and why it clears the reuse + reliability bar.

**You know this worked when:** your chosen item exists and you ran it successfully at least once; `PROMPT-LIBRARY.md` has a new entry that either contains your prompt inline or points to your command/skill by path, with a name, usage line, example, and a form-and-why note. All local — nothing committed.

> **Why a pointer, not a paste:** you wouldn't paste a whole skill definition into a prose library — it'd rot out of sync with the real file. The library's job is to tell a teammate *what exists and how to reach it*. Prompts are short enough to live inline; everything else is referenced by path. (This is the same move Step 3 makes when your entry points at `@<subagent>`.)

---

## Step 3 — Author a reusable subagent (Adoption capstone)

This step turns what the team can *prompt for* into what the team can *invoke by name*. A subagent scopes a model to one job with a specific tool allowlist — safer, more predictable, more shareable than a loose prompt. (This is the lab-local capstone — the culminating build of THIS lab.)

1. Choose your subagent from the repo-grounded menu (full descriptions in `docs/lab-9/subagent-menu.md`), or propose your own with equivalent scope:

   | Option | File to create | Allowed tools | One job |
   |--------|----------------|---------------|---------|
   | `test-writer` | `.claude/agents/test-writer.md` | Read, Write, Edit, Bash, Glob, Grep | Generate pytest tests for a named endpoint or function; scope `tests/backend/` only |
   | `api-contract-reviewer` | `.claude/agents/api-contract-reviewer.md` | Read, Grep | Review the named endpoint in `server/main.py` for contract stability; report only, no edits |
   | `vue-auditor` | `.claude/agents/vue-auditor.md` | Read, Glob, Grep | Audit the named Vue component in `client/src/`; report only, no edits |
   | your own | `.claude/agents/<your-name>.md` | narrower than full default | one scoped job you'd use on this repo |

   > **Naming note:** `vue-auditor` (this menu, which you'd author) is a different agent from the pre-existing `vue-expert` already in `.claude/agents/` — different name, different job. Don't overwrite `vue-expert`.

2. Ask Claude to draft the agent `.md` file for your choice (drive Claude). It must have:
   - YAML frontmatter: `name`, `description` (one line stating when to invoke it), `tools` (comma-separated), `model: sonnet`
   - A **one-job system prompt** that names its target path and declines tasks outside that scope

   Edit the draft until it's genuinely one-job. "Help with code" is not a one-job agent.

3. Compare your file's shape to the existing agents (`code-reviewer.md`, `security-auditor.md`, `vue-expert.md`) — that's the reference format.

4. Write the file to `.claude/agents/<name>.md`.

5. Update your `PROMPT-LIBRARY.md` entry from Step 2 to point at the subagent — add a note line such as `Invoke as a scoped run via @<name>.`

**You know this worked when:** `.claude/agents/<name>.md` has valid YAML frontmatter (name, description, tools, model) and a one-job system prompt that names a target path; your `PROMPT-LIBRARY.md` entry references `@<name>`. All local — nothing committed.

Reference frontmatter shape:
```yaml
---
name: <kebab-case>
description: <one line — when to invoke this agent>
tools: <comma-separated list>
model: sonnet
---
```

---

## Step 4 — Write the team-handoff note

This is the artifact you carry back. Your change champion will ask to see it.

1. Open `docs/lab-9/30-day-plan-template.md`. Write `TEAM-HANDOFF.md` at the repo root with three commitments:
   - **This week:** one concrete action (e.g. "run my `gen-endpoint-tests` entry to add empty-data and bad-filter cases for `/api/spending/categories`, which only has happy-path coverage today").
   - **This month:** one team-facing action (e.g. "get two teammates to each contribute one library entry").
   - **Teach a colleague:** one commitment naming a person or a session (e.g. "run a 30-minute show-and-tell for my squad on the 5-point review checklist").

   Each must carry a **number, a task, or a name** — "use Claude more" isn't a commitment.

2. Pick **two real adoption metrics** from the seeded menu in the template (or propose your own leading indicator), and name **two vanity metrics** you'll deliberately NOT track — one sentence each on what the real metric tells you that the vanity one doesn't.

3. Reference the champion cadence as a **pattern** (office hours + regular show-and-tell), not fixed dates — this programme is async.

**You know this worked when:** `TEAM-HANDOFF.md` exists in your worktree with three commitments each carrying a number/task/name, plus a two-real / two-vanity metric split with a one-line justification each.

Expected metric section shape:
```
## Adoption metrics
Real (leading):
- <metric 1> — what it tells you:
- <metric 2> — what it tells you:
Avoided (vanity):
- <vanity metric 1> — why it misleads:
- <vanity metric 2> — why it misleads:
```

---

## Done criteria

You're done when all four are true:

1. You cold-ran both seeded entries and can name, in one sentence, the context the weak entry made Claude guess.
2. `PROMPT-LIBRARY.md` has your new entry with a name, usage line, a form/pointer (prompt inline or artifact path), one example, and a form-and-why note. Local, not committed.
3. `.claude/agents/<name>.md` exists with valid YAML frontmatter (name, description, tools, model) and a one-job system prompt; `PROMPT-LIBRARY.md` references `@<name>`. Local, not committed.
4. `TEAM-HANDOFF.md` exists with three commitments each carrying a number/task/name and a two-real / two-vanity metric split.

Expected end state (local, uncommitted):
```
$ git status --short
 M PROMPT-LIBRARY.md
?? .claude/agents/<name>.md
?? TEAM-HANDOFF.md
```

---

## Carry it back

You now have three local artifacts in your `lab-9-work` worktree: your `PROMPT-LIBRARY.md` entry (pointing at your built item and your subagent), your `.claude/agents/<name>.md`, and your `TEAM-HANDOFF.md`. Nothing is committed — this is yours to hand off. Your change champion closes the loop: they'll ask which entry you contributed, which subagent you scoped and why, and what's in your handoff note. That conversation is the actual handover.

---

## Extra credit (not required for done criteria)

1. **Promote your entry to a real command.** Take the prompt you contributed and package it as a `.claude/commands/<name>.md` slash command with a description tuned for triggering, then invoke it with `/<name>` on a real endpoint. Record whether the command form was worth it over the plain prompt.
   > **Windows / macOS (identical):** if you add anything under `.claude/settings.json` while wiring the command, relaunch Claude Code before testing it.

2. **Cold-run a peer's entry (async-safe).** In the async cohort thread, swap library entries with another participant, run theirs cold, and post a reuse/reliability rating. This is the test-a-neighbor gate done live, without a synchronous session.

3. **Turn the library into a reviewed-merge process.** Write a two-line `## Contribution rules` section for `PROMPT-LIBRARY.md`: open contribution, reviewed merge, and one reuse/reliability check every entry must pass.

4. **Invoke your subagent on a real file.** Start a fresh Claude Code session, type `@<name>` and name a real endpoint or component from the repo. Observe whether the scoping holds. Record any behavior that crossed the boundary and whether a system-prompt tightening fixed it.

---

## If you're stuck

**The strong seeded entry also makes Claude guess.** You may have pasted only part of it. Reopen `PROMPT-LIBRARY.md`, copy the **entire** body of `gen-endpoint-tests` including every line (the endpoint name, the cases to cover, the pattern file, and the output format line), and paste it into a truly fresh `claude` session with no other files open or context loaded.

**You can't decide which form your entry should be.** Ask Claude to recommend which form (prompt / command / skill / CLAUDE.md rule) best fits your item using the scale test: "what if there were 10,000 of these in a long-lived monorepo?" Ask for one recommendation and one runner-up with a line of reasoning each. Then make the call yourself and record it in your entry's note. The choice is yours to defend.

**You can't decide which subagent to author.** Choose `test-writer`: its tool allowlist and scope are spelled out in `docs/lab-9/subagent-menu.md`, and the reference format is in `.claude/agents/code-reviewer.md`. It's the most directly related to the lab's test-generation theme.

**Fully stuck or out of time.** Check out the reference artifacts from the solution branch to see finished examples. First confirm your remote points at the fork:

```
git remote -v
```
```
git fetch origin
```
```
git checkout origin/lab-9-solution -- PROMPT-LIBRARY.md TEAM-HANDOFF.md docs/lab-9/quality-gate-notes.md .claude/agents/test-writer.md
```

Open `PROMPT-LIBRARY.md`, `.claude/agents/test-writer.md`, `docs/lab-9/quality-gate-notes.md`, and `TEAM-HANDOFF.md`. You'll see a complete library entry pointing at an authored subagent, filled-in cold-run ratings, and a checkable handoff note — the LOCAL end state, not a commit history. These are reference files you pulled in; delete them before your next lab so they don't carry over.

**Reset everything.** Run the `/reset-branch` command (not a skill). It does `branch -D` + `reset --hard` + `clean -fd` with no confirmation, so save anything you want to keep first. With worktree-per-lab you mostly just move to the next lab's worktree.

---

Your completion and mastery quizzes are in the LMS.
