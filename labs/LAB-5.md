# Lab 5 — MCP vs CLI, Same Task Twice

**Module 05 | Solo | 20:00**

> **An MCP server costs context-window tokens before you type anything. Pay that cost when the task needs a capability the CLI cannot give you. The rubric tells you which abstraction earns its tokens.**

---

## Pre-flight (before the clock starts)

In a terminal at the repo root, run these two commands on separate lines:

```
git fetch origin
```

```
git checkout -b lab-5-work origin/lab-5-start
```

If the servers are not running, start a Claude session and run:

```
/start
```

Then exit that session. Have a scratch note ready (paper or any text file you do not commit). You will record two /context readings, a per-page verdict table for six pages, and your rubric answer.

**Read the tool ledger:** this lab makes no code changes in the core path, so "reading the diff" means reading the exact command or MCP tool call Claude proposes before you approve it, the same gate you applied to code diffs in Labs 1–4.

---

## Step 1 — Launch with MCP off `0:00–2:00`

From the repo root, in your terminal. This launch is human-typed on purpose: session-level toggles set the environment Claude runs in, and no prompt can do it for you.

```
claude --strict-mcp-config --mcp-config .claude/no-mcp.json
```

Then inside Claude:

```
/mcp
```

**Observe:** /mcp reports no MCP servers configured. The project `.mcp.json` (which ships Playwright) was ignored because `--strict-mcp-config` loads only the servers in the file you passed, and `.claude/no-mcp.json` is an empty server list.

**Read the ledger:** nothing to approve yet. You are confirming the harness state before spending tokens.

---

## Step 2 — Baseline /context `2:00–3:00`

```
/context
```

**Observe:** the context breakdown has no MCP tools entry, or shows 0.

**Jot this number on your scratch note as your Round 1 reading.** This is your control reading.

---

## Step 3 — Round 1: verify via CLI `3:00–9:00`

Paste exactly:

```
Without using any MCP tools, verify the app: confirm http://localhost:3000 loads and that each of the six pages (Dashboard, Inventory, Orders, Demand, Spending, Reports) is working, using curl and any CLI you need. Base each verdict only on what the running app returns, not on reading the source code. Do not fix anything. Report a PASS/FAIL verdict per page with the evidence you used.
```

**Observe:** Claude curls localhost:3000 and the API endpoints behind each page. Read each Bash or curl command before approving it. Note on your scratch note what the evidence consists of: HTTP status codes and JSON payloads. Nothing in Round 1 looked at a rendered page.

**Record:** jot the Round 1 verdict and evidence type per page on your scratch note.

If Claude is still exploring at minute 5 of this step, paste:

```
Stop and give the verdict table now.
```

---

## Step 4 — Relaunch with MCP on `9:00–11:00`

Exit the session:

```
/exit
```

Then launch plain (again human-typed; same reason as Step 1):

```
claude
```

If prompted to approve the project's MCP servers, approve. Then:

```
/mcp
```

```
/context
```

**Observe:** /mcp lists `playwright` connected. /context now shows an MCP tools entry costing real tokens, and you have not typed a prompt yet.

**Jot this number as your Round 2 reading and compute the delta.** This is the price of admission, paid up front, every session. You will share the delta in meeting chat at Step 6.

---

## Step 5 — Round 2: same task via Playwright MCP `11:00–17:00`

**THE POINT.**

Paste exactly:

```
Using the Playwright MCP tools, verify the app: navigate to http://localhost:3000, screenshot the dashboard, click through all six nav tabs (Dashboard, Inventory, Orders, Demand, Spending, Reports), verify each page renders its content, and report any console errors. Do not fix anything. Report a PASS/FAIL verdict per page with the evidence you used.
```

**Observe:** a real browser opens. Claude navigates, screenshots the dashboard, clicks each tab, and reads page snapshots and console messages.

**Read the ledger:** approve each Playwright tool call after reading it (`browser_navigate`, `browser_click`, `browser_snapshot`, `browser_console_messages`). These are what those up-front tokens bought: eyes and hands in a real DOM.

**Record:** jot the Round 2 verdicts per page. Compare your Round 2 table to your Round 1 table. One page will flip verdict. The Round 2 console will also show `/api/tasks` 404 errors from earlier in the day; those are planted noise, not a finding for this lab.

---

## Step 6 — Compare and apply the rubric `17:00–20:00`

Answer these questions against your scratch note:

1. What did Round 1's evidence prove, and what could it never prove?
2. What did Round 2 catch that Round 1 missed?
3. Round 2's console showed two kinds of errors. Which were planted noise and which was the finding?
4. Was Playwright MCP worth its tokens for this task? Name a task where CLI-only is the right call.

**Optional completion signal:** post your token delta and the verdict-flip line (the one page that changed from Round 1 to Round 2) in meeting chat. The stream of posts is how the facilitator reads completion across the room.

**Rubric close** (from `labs/lab-5-rubric.md`):

1. Write down one task you ask Claude for 2–5 times a week.
2. Place it in exactly one box: CLAUDE.md / Skill / Hook / Subagent / MCP server.
3. Write a one-sentence defense. The wrong answer is "all of the above."

Cross-check your choice against the four pre-mapped Perforce scenarios on the rubric card. Nothing gets committed in this lab's core path; your scratch note is the artifact.

---

## Done criteria

Check all three on your scratch note in under 10 seconds:

1. **Two /context readings jotted down** (Round 1 reading near zero, Round 2 a real number) with the delta computed.
2. **One page flips verdict between rounds** (PASS in Round 1, FAIL in Round 2).
3. **One rubric box chosen** with a one-sentence defense written next to it.

---

## Extra Credit (time permitting)

### EC-1 — Fix what Round 2 found

Paste:

```
The page that failed Round 2 renders blank in the browser even though its API endpoint returns 200. Find and fix the frontend bug in its view component, then verify the fix using the Playwright MCP tools.
```

Watch for the root CLAUDE.md mandatory rule: any `.vue` change must go through the vue-expert subagent. Read the one-line diff, accept, and watch Claude re-verify with the browser. Then tell Claude:

```
Commit the fix locally with a descriptive message. Do not push.
```

### EC-2 — Round 3: the same verification via Playwright CLI

Paste:

```
Without using any MCP tools, write and run a Playwright CLI script that performs the same six-page verification: load http://localhost:3000, visit each of the six pages, confirm each renders its content, and capture any console errors. Install anything you need. Do not fix anything. Report a PASS/FAIL verdict per page with the evidence you used.
```

This is the true three-way comparison (curl vs Playwright CLI vs Playwright MCP). Note the difference: the CLI route gets real DOM eyes with zero up-front token cost per session, but Claude had to write the script. The reasoning and prompts are the unlock.

If the Playwright browser download takes more than 2 minutes, drop this item. It is extra credit and the core comparison stands on Rounds 1 and 2.

### EC-3 — Share the rubric

Post your weekly-task placement and one-sentence defense in meeting chat, or unmute and read it. Accept a challenge question from the facilitator or a peer. Suggested challenge: "What if 10,000 teams had different workflows — should they all inherit this CLAUDE.md?" If your answer was a hook, name the event and what the script does.

---

## Stuck paths

Post the problem in meeting chat; a TA will reply or pull you into a breakout room.

| Failure | Recovery move |
|---|---|
| Step 1: /mcp still shows playwright in the no-MCP session | You launched outside the repo root or the flag was mistyped. Post in chat. TA will send a fallback: exit, rename the project config off (Windows: `Rename-Item .mcp.json .mcp.json.off`; other: `mv .mcp.json .mcp.json.off`), launch plain `claude`, then rename it back before Step 4. |
| Step 3: Claude reads source files and spots the planted bug despite the prompt | Not a failure. Record its verdict and note on your scratch note that the running-app evidence (curl) still said PASS. The compare question in Step 6 still lands. |
| Step 3 overruns at minute 5 | Paste: `Stop and give the verdict table now.` Move on with whatever is filled. |
| Step 4: playwright shows "failed" in /mcp, or the first tool call hangs | Pre-warm homework should prevent this. Post in chat; the TA will send the dry-run reference numbers and Round 2 verdict table. Jot them down marked "reference" and proceed to Step 6. |
| Step 5: browser fails to launch (no Chromium) | Ask Claude to run the Playwright browser_install tool, or fall back to the reference numbers as above. |
| Step 5: all six pages pass Round 2 | Click through every nav tab one at a time and report console errors for each page. The TypeError is deterministic once the affected page is visited. |
| Token quota exhausted | Post in chat. The facilitator will narrate this as a cost-management moment; the TA posts reference numbers so you can complete the comparison and rubric. |
| EC-2: Playwright CLI install drags | Drop the item. It is extra credit. |
| Anything else or out of time | Post in chat. The rubric close (Step 6) is the must-do; cut Round 2 exploration before cutting it. |

**Full reset at any point:**

```
/reset-branch
```

Then re-run the pre-flight commands.
