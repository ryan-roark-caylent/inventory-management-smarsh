# Lab 9: Team Adoption and Champion Handover

**Track 3 (AI Teammate) | Lab 9 of 9 | Depends on: Labs 6, 7, 8**

Adoption is an artifact you commit, not a feeling you report. This lab closes the programme by turning your personal Claude skills into team assets: a prompt library entry anyone can run cold, a subagent anyone can invoke by name, a CLAUDE.md template for a repo type unlike this one, and a 30-day plan specific enough for a teammate to check on.

You'll work entirely in the Claude Code terminal. No app server and no browser are needed on the core path.

Your completion and mastery quizzes are in the LMS.

---

## What this lab proves

Most programme rollouts fail on the bridge back to Monday: no plan, no library, no champion, so engineers revert to old habits under sprint pressure. A Smarsh champion's job is to keep the good path the easy path. A curated library other engineers pull from, a subagent other engineers invoke by name, a CLAUDE.md pattern that transfers across repo types, and a plan someone can check: this lab produces those four artifacts against the real repo.

---

## Where the concept clicks

Step 1 is the moment. You'll cold-run two seeded library entries in separate fresh sessions, simulating a teammate who's never seen this repo. Watch what each one does. The gap you observe is the quality gate. Everything else in the lab builds on what you see there.

---

## Track callback (Labs 6, 7, 8)

In Lab 6 you built and triggered a skill and applied the 5-abstraction rubric (CLAUDE.md / skill / hook / subagent / MCP). In Lab 7 you invoked pre-built subagents and saw how scoping narrows what a model can reach. In Lab 8 you ran the 5-point review checklist and made a Trust-Spectrum call with a cited justification. This lab turns those personal skills into team assets: you contribute one to a shared library behind a quality gate, you author a new subagent, and you write the plan that keeps the team using them. No app servers and no browser are needed on the core path.

---

## Before you start

> **Windows:** This lab runs entirely in the Claude Code terminal UI. No browser step, no MCP on the core path, and no `settings.json` change are needed. The only multi-line commands are the Step 0 git commands. Run them as separate lines, never joined.
>
> **macOS:** The same applies. All shell commands are POSIX-compatible and run in Terminal or iTerm2. No browser flag or port-kill command is needed on the core path.

---

## Step 0: Branch and orient

1. In a terminal at the repo root, run these as two separate commands:
   ```
   git fetch origin
   ```
   ```
   git checkout -b lab-9-work origin/lab-9-start
   ```
   The fetch is not optional. The lab branches were pushed at repo freeze, after your homework clone.

2. Open `PROMPT-LIBRARY.md` at the repo root and read both seeded entries and the entry template at the top.

3. Open `docs/lab-9/candidate-prompts.md`. It contains three reusable prompt candidates you can draw from in Step 2 and the reuse/reliability rating rubric.

**You know this worked when:** `PROMPT-LIBRARY.md` shows exactly two entries (`gen-endpoint-tests` and `quick-review`) under a `## How to add an entry` template block.

Expected library header:
```
$ head -30 PROMPT-LIBRARY.md
# Prompt & Command Library

Shared, peer-tested prompts for this repo. An entry earns a place only if a
teammate can run it COLD and get the same result the author got.

## How to add an entry
Each entry needs: a name, when to use it, the prompt body, one example of
expected output, and a one-line note on why it clears the reuse + reliability bar.

## Entries

### gen-endpoint-tests   (strong example)
...
### quick-review   (weak example — do not copy this shape)
...
```

---

## Step 1: Cold-run the quality gate (POINT STEP)

1. Start a **fresh** Claude Code session (`claude`) at the repo root. Do not pre-load any files or give Claude any other context. You are simulating a teammate who has never seen this repo's specifics.

2. Paste the body of the **weak** seeded entry (`quick-review`) exactly as written into the fresh session and run it. Watch what Claude does when the prompt does not name a target, a checklist, or an output shape.

3. Start another fresh Claude Code session. Paste the body of the **strong** entry (`gen-endpoint-tests`) exactly as written. Watch what it produces.

4. In a scratch note, rate each entry on **reuse** (does it generalize past the author's one case?) and **reliability** (does it work cold, without hand-holding?) using the rubric in `docs/lab-9/candidate-prompts.md`. Write one sentence on the single thing the weak entry assumed that a teammate would not have.

**You know this worked when:** the weak entry made Claude ask a clarifying question or pick an arbitrary target, and the strong entry did not. You can name the missing context in one sentence.

Expected weak-entry behavior:
> **Claude (fresh session):** "I don't see any code in our conversation yet. Which file or endpoint would you like me to review, and what should I check for: correctness, style, security, all of the above?"

Expected strong-entry behavior:
> **Claude:** "Here is `tests/backend/test_inventory_filters.py`:" *(then a runnable test file that imports the TestClient fixture and asserts on the real response shape)*

---

## Step 2: Contribute one entry that clears the bar

1. Pick **one** prompt from `docs/lab-9/candidate-prompts.md` (or one of your own from an earlier lab) that you would recommend to a teammate. Decide its **abstraction** using the library-entry abstraction menu: is this best as a one-off library **prompt**, a slash **command** (`.claude/commands/`), a **skill** (`.claude/skills/`), or a **CLAUDE.md rule**? Apply the scale test: what if there were 10,000 of these in a long-lived monorepo?

   Note: Lab 6's full rubric also includes hook, subagent, and MCP. Those are valid in that broader context but do not map to shareable library entries. You will author a proper subagent in Step 3.

2. Rewrite the prompt so it clears the gate you applied in Step 1: it must name its target, its inputs, and show one example of expected output. Follow the entry template at the top of `PROMPT-LIBRARY.md`.

3. Add your entry to `PROMPT-LIBRARY.md` under `## Entries`, including a one-line note recording the abstraction you chose and why.

4. Commit:
   ```
   git add PROMPT-LIBRARY.md
   ```
   ```
   git commit -m "library: add <your-entry-name> with reuse+reliability notes"
   ```

**You know this worked when:** `git show --stat HEAD` lists `PROMPT-LIBRARY.md`, and your entry has a name, a trigger/usage line, a body, one example, and an abstraction note.

Expected commit summary:
```
$ git show --stat HEAD
    library: add gen-endpoint-tests with reuse+reliability notes
 PROMPT-LIBRARY.md | 22 ++++++++++++++++++++++
 1 file changed, 22 insertions(+)
```

---

## Step 3: Author a reusable subagent (ADOPTION CLIMAX)

This step turns what the team can prompt for into what the team can invoke by name. A subagent scopes a model to one job with a specific tool allowlist: safer, more predictable, and more shareable than a loose prompt.

1. Choose your subagent from the **repo-grounded menu** in `docs/lab-9/subagent-menu.md`, or propose your own with equivalent scope.

   | Option | File to create | Allowed tools | One job |
   |--------|----------------|---------------|---------|
   | `test-writer` | `.claude/agents/test-writer.md` | Read, Write, Edit, Bash, Glob, Grep | Generate pytest tests for a named endpoint or function; scope `tests/backend/` only |
   | `api-contract-reviewer` | `.claude/agents/api-contract-reviewer.md` | Read, Grep | Review the named endpoint in `server/main.py` for contract stability; report only, no edits |
   | `vue-auditor` | `.claude/agents/vue-auditor.md` | Read, Glob, Grep | Audit the named Vue component in `client/src/`; report only, no edits |
   | your own | `.claude/agents/<your-name>.md` | narrower than full default | one scoped job you'd use on this repo |

2. Ask Claude to draft the agent `.md` file for your choice. The file must have:
   - YAML frontmatter: `name`, `description` (one line stating when to invoke it), `tools` (comma-separated), `model: sonnet`
   - A **one-job system prompt** that names its target path and redirects or declines tasks outside that scope

   Edit the draft until it is useful. A system prompt that says "help with code" is not a one-job agent.

3. Compare your file's shape to the existing agents in `.claude/agents/`: `code-reviewer.md`, `security-auditor.md`, and `vue-expert.md` are the reference format.

4. Write the file to `.claude/agents/<name>.md`.

5. Update your `PROMPT-LIBRARY.md` entry from Step 2 to reference the subagent: add a note line such as `Invoke as a scoped run via @<name>.`

6. Commit:
   ```
   git add .claude/agents/<name>.md PROMPT-LIBRARY.md
   ```
   ```
   git commit -m "library: add <name> subagent + link from PROMPT-LIBRARY entry"
   ```

**You know this worked when:** `.claude/agents/<name>.md` has valid YAML frontmatter (name, description, tools, model) and a one-job system prompt that names a target path; `PROMPT-LIBRARY.md` references `@<name>` or the agent file in your entry; `git show --stat HEAD` shows both files.

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

## Step 4: CLAUDE.md template by repo type

1. Open `docs/lab-9/repo-type-briefs.md`. Three short briefs cover repo types **unlike** inventory-management: a Java/Spring microservice, a shared Python library, and a data-pipeline repo. Pick one.

2. Ask Claude to draft a **CLAUDE.md template section** for that repo type, then edit it yourself. It must differ from the inventory-management CLAUDE.md in ways that fit the target: build/test commands, conventions, and always/never rules specific to that repo type.

3. Write the draft to `docs/lab-9/claude-md-template-<repo-type>.md` and add two bullets at the bottom: **two things that change** vs the inventory-management template and why.

**You know this worked when:** the template names build/test commands and conventions that would be wrong for inventory-management (for example: `mvn test` and controller/service layering for Spring, or semantic-versioning and public-API-stability rules for a shared library), and your two "what changes" bullets are concrete.

---

## Step 5: 30-day plan and real metrics

1. Open `docs/lab-9/30-day-plan-template.md`. Write `30-day-plan.md` at the repo root with three commitments:
   - **This week:** one concrete action (for example: "run the `gen-endpoint-tests` entry to add empty-data and bad-filter cases for `/api/spending/categories`, which only has happy-path coverage in `test_misc_endpoints.py`, this sprint").
   - **This month:** one team-facing action (for example: "get two teammates to each contribute one library entry").
   - **Teach a colleague:** one commitment naming a person or a session (for example: "run a 30-minute show-and-tell for my squad on the 5-point review checklist").

   Each commitment must carry a **number, a task, or a name**. "Use Claude more" is not a commitment.

2. Define **two real adoption metrics** (leading indicators of behavior change) and **explicitly exclude two vanity metrics**, with one sentence each on what the real metric tells you that the vanity metric does not.

3. Reference the champion cadence **pattern** (office hours and regular show-and-tell as the sustaining mechanism), not fixed calendar dates. This programme is async.

4. Commit:
   ```
   git add 30-day-plan.md docs/lab-9/claude-md-template-*.md
   ```
   ```
   git commit -m "adoption: 30-day plan, metrics, and repo-type CLAUDE.md template"
   ```

**You know this worked when:** `git log --oneline -3` shows your three commits, and `30-day-plan.md` has three commitments each carrying a number/task/name plus the two-real / two-vanity metric split.

Expected metric section shape:
```
## Adoption metrics
Real (leading):
- <metric 1> — what it tells you:
- <metric 2> — what it tells you:
Excluded (vanity):
- <vanity metric 1> — why it misleads:
- <vanity metric 2> — why it misleads:
```

---

## Done criteria

You're done when all five are true:

1. You cold-ran both seeded entries and can name, in one sentence, the context the weak entry assumed.
2. `PROMPT-LIBRARY.md` has your committed entry with a name, usage line, body, one example, and an abstraction note.
3. `.claude/agents/<name>.md` is committed with valid YAML frontmatter (name, description, tools, model) and a one-job system prompt; `PROMPT-LIBRARY.md` references it.
4. `docs/lab-9/claude-md-template-<repo-type>.md` exists with a template for a different repo type and two concrete "what changes" bullets.
5. `30-day-plan.md` is committed, with three commitments each carrying a number/task/name and a two-real / two-vanity metric split.

---

## Share-back

Your share-back is the `PROMPT-LIBRARY.md` commit (your contributed, peer-runnable entry referencing your authored subagent) and the committed `30-day-plan.md`. The person-specific signal is which prompt you contributed, which subagent you authored and why you scoped it that way, the repo type you templated, and the metrics you picked.

---

## Extra credit (not required for done criteria)

1. **Promote your entry to a real command.** Take the prompt you contributed and package it as a `.claude/commands/<name>.md` slash command with a description tuned for triggering, then invoke it with `/<name>` on a real endpoint. Record whether the command form was worth it over the plain prompt.
   > **Windows:** if you add anything under `.claude/settings.json` while wiring the command, relaunch Claude Code before testing it.
   > **macOS:** same: relaunch Claude Code (quit with Cmd+Q and reopen) after `.claude/settings.json` changes.

2. **Cold-run a peer's entry (async-safe).** In the async cohort thread, swap library entries with another participant, run theirs cold, and post a reuse/reliability rating. This is the test-a-neighbor gate done live, without a synchronous session.

3. **Write the second repo-type template.** Do Step 4 again for a second repo type from the brief set and enumerate what a single one-size CLAUDE.md would get wrong for both.

4. **Turn the library into a reviewed-merge process.** Write a two-line `## Contribution rules` section for `PROMPT-LIBRARY.md`: open contribution, reviewed merge, and one reuse/reliability check every entry must pass.

5. **Invoke your subagent on a real file.** Start a fresh Claude Code session, type `@<name>` and name a real endpoint or component from the repo. Observe whether the scoping holds. Record any behavior that crossed the boundary and whether a system-prompt tightening fixed it.

---

## If you're stuck

**The strong seeded entry also makes Claude ask questions.** You may have pasted only part of it. Reopen `PROMPT-LIBRARY.md`, copy the **entire** body of `gen-endpoint-tests` including every line (the endpoint name, the cases to cover, the pattern file, and the output format line), and paste it into a truly fresh `claude` session with no other files open or context loaded.

**You can't decide which abstraction your entry should be.** Ask Claude to recommend which abstraction (prompt / command / skill / CLAUDE.md rule) best fits your prompt using the scale test: "what if there were 10,000 of these in a long-lived monorepo?" Ask for one recommendation and one runner-up with a line of reasoning each. Then make the call yourself and record it in your entry's abstraction note. The choice is yours to defend.

**You can't decide which subagent to author.** Choose `test-writer`: its tool allowlist and scope are spelled out in `docs/lab-9/subagent-menu.md`, and the reference format is in `.claude/agents/code-reviewer.md`. It is the most directly related to the lab's test-generation theme.

**You're out of time or blocked.** Check out the reference state so you leave having seen what the finished lab looks like:
```
git stash -u
```
```
git checkout lab-9-solution
```
Open `PROMPT-LIBRARY.md`, `.claude/agents/test-writer.md`, `docs/lab-9/quality-gate-notes.md`, `docs/lab-9/claude-md-template-spring.md`, and `30-day-plan.md`. You now have a complete, peer-runnable library entry, an authored subagent, filled-in cold-run ratings, a repo-type template, and a checkable adoption plan on your screen. Return to your own work:
```
git checkout lab-9-work
```
```
git stash pop
```

---

Your completion and mastery quizzes are in the LMS.
