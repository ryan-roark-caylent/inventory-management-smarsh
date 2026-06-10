# Lab 2 — CLAUDE.md Repair (Context Engineering)

**Module 02 | Solo | 15:00 hard cap**

> **Context is currency. Spend it wisely in CLAUDE.md, not in every prompt.**
>
> CLAUDE.md is read into every session before you type a word. If it contains lies, junk, or secrets, Claude pays the cost — and so do you.

---

## Step 0 — Setup (before the clock starts)

In a terminal at the repo root, run these two commands on separate lines:

```
git fetch origin
```

```
git checkout -b lab-2-work origin/lab-2-start
```

Then start a **fresh** Claude Code session. Exit any running session first, or run `/clear`. CLAUDE.md is read at session start — a session opened before the checkout has the wrong file in its head.

*(Your previous lab's work is saved on its branch. Every lab starts from a clean state on purpose.)*

---

## Step 1 — Price the context `0:00–2:00`

Type:

```
/context
```

Find the memory-files line in the output. Locate the token figure attributed to CLAUDE.md.

**Write that number down as your BEFORE figure** (paper or scratch note).

Expected ballpark: **[TOK-A]** tokens. That cost is paid at the start of every session, before you type a single prompt.

---

## Step 2 — Find the drift `2:00–6:00`

**This is the point step.**

Paste exactly:

```
Compare the API Endpoints section of @CLAUDE.md to the actual routes in server/main.py and list every discrepancy. Do not change any files yet.
```

**Observe:** Claude reads `server/main.py` and reports discrepancies between what CLAUDE.md claims and what the code actually defines.

Claude should report **at least three discrepancies**. Write the count down next to your BEFORE figure.

The takeaway: this file was loaded into your session at startup. Until 30 seconds ago, Claude was working from a description of the API that does not match reality.

---

## Step 3 — Fix the drift `6:00–10:00`

Paste exactly:

```
Update only the API Endpoints section of CLAUDE.md so it exactly matches the routes in server/main.py. Add the missing endpoints, remove the one that does not exist, and keep the existing one-line-per-endpoint format. Touch nothing outside that section.
```

**Read the diff** before accepting:

- Verify each changed line against your step-2 list.
- Claude may find more than the minimum three; verify each added or removed line against what `server/main.py` actually defines. All accurate additions are correct under the prompt.
- Zero changed lines outside the `## API Endpoints` section. If the diff touches any other section, press Esc to reject and re-paste the prompt.

Accept the edit.

---

## Step 4 — One targeted junk deletion `10:00–13:00`

Open CLAUDE.md in your editor and find the section titled `## Deployment & Environment Setup`. Note what it contains.

Then paste exactly:

```
Delete the entire "Deployment & Environment Setup" section from CLAUDE.md, including the Required Tokens block. This app has no deployment, and credentials never belong in a context file that gets committed and read into every session. Change nothing else.
```

**Read the diff** before accepting:

- The diff should be pure deletion — one contiguous block starting at `## Deployment & Environment Setup` and ending before the next `##` heading.
- No other section is touched. If it is, press Esc to reject and re-paste the prompt.

Accept.

---

## Step 5 — Re-price `13:00–15:00`

**Run `/clear` first.** CLAUDE.md is priced at session start, so an edit mid-session changes nothing until the window resets.

```
/clear
```

Then:

```
/context
```

Find the CLAUDE.md token figure again. **Write it down as your AFTER figure.**

The drop should be roughly **[TOK-A − TOK-C]** tokens from your BEFORE.

**Optional completion signal:** paste `Lab 2: <BEFORE> -> <AFTER> tokens` into the meeting chat. The stream of deltas is how the facilitator reads completion across the room; react to other people's numbers.

If you have 30 seconds to spare, tell Claude:

```
Commit the CLAUDE.md changes as a local commit with the message "Fix CLAUDE.md drift and remove fake credentials section". Do not push.
```

Read the git commands it runs. Local commit only; never push.

---

## Extra Credit — Full cut-pass (time permitting)

Start only after step 5 is done.

**EC-1 — Full cut-pass against the reference (est. 5 min)**

Two more junk sections remain in CLAUDE.md: `## Project Background & History` and `## Notes from 2025-11-14 session`. Open `docs/lab-2/reference-good.md` (a lean, correct CLAUDE.md for this repo) and `docs/lab-2/reference-bad.md` (an annotated anti-pattern gallery).

Paste:

```
Compare CLAUDE.md against docs/lab-2/reference-good.md. Remove every section from CLAUDE.md that has no counterpart in the reference and adds no durable, project-wide instruction. List what you removed and why before editing.
```

**Read the diff:** only the two sections named above should go. If the diff removes any subagent rules, skill pointers, stack info, key patterns, common issues, file locations, or design system content — press Esc and tighten the prompt. Those sections are load-bearing for later labs.

Then `/clear` + `/context` one more time. If you do EC-1, post your final figure in chat too.

---

## Done criteria (pick any two)

1. **Two numbers written down** — BEFORE and AFTER — and AFTER is lower.
2. **The credentials section is gone:** Ctrl+F "Deployment" in CLAUDE.md finds nothing, or `git diff main -- CLAUDE.md` shows that block deleted in red.
3. **The API section is honest:** CLAUDE.md lists the routes Claude found in step 2, and the fabricated endpoint it reported as missing-from-code is no longer in the file.

---

## Stuck paths

Post the problem in meeting chat; a TA will reply or pull you into a breakout room.

| Failure | Self-serve move |
|---|---|
| `/context` output looks unfamiliar; can't find the memory-files figure | Look for a line that starts with "memory-files" or similar. The ballpark is **[TOK-A]** tokens. Post in chat if you can't locate it. |
| Step 2 audit is vague or wanders into the whole file | Re-paste with this fallback: `List the routes defined by @app.get in server/main.py, then list the endpoints named in the API Endpoints section of @CLAUDE.md, then show me only the differences between the two lists.` |
| Step 3 diff touches sections outside API Endpoints | Press Esc, re-paste the step-3 prompt unchanged. If it happens twice, post in chat. |
| CLAUDE.md is mangled after a bad accept | Run `git checkout origin/lab-2-start -- CLAUDE.md` to restore the starting file, then redo from step 3. Takes about 90 seconds. |
| Session context is confused about file state | `/clear`, then re-point: `Read CLAUDE.md and server/main.py, then ...` followed by the step prompt. The file system is the durable state, not the conversation. |
| Branch is in bad shape with less than 5 minutes left | `/reset-branch`, then: `git fetch origin` on one line, then `git checkout -b lab-2-work-retry origin/lab-2-start` on the next line; jump to step 4 so you still produce a diff and an AFTER number. |
| Hard stuck, time expiring | Post in chat. The TA will send a rescue command. |

---

## Jot it down

One thing you would cut next from a CLAUDE.md you own, and where it belongs instead: **skill / hook / nowhere**.

---

> **CLAUDE.md is not deterministic. Telling it "don't do this" does not guarantee that behavior.** CLAUDE.md biases the model. Skills, hooks, and review gates enforce.
