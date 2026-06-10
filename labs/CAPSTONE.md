# Capstone — Your Task, The Whole Loop

**Module 06** | Solo: one person, one machine, one session | **30 minutes** | Runs if earlier labs finish on time

---

In Lab 5's rubric close you named a task you ask Claude for 2-5 times a week. That task is your capstone candidate.

Check your Lab 5 rubric placement before you start. If you placed your task in a skill or hook, build that artifact here — spec the skill or hook file and run the loop below on it. If you placed it as a one-off session, run the loop on the task directly.

---

Fill this in as you go — it takes under 5 minutes and you can tab back to it between steps: https://forms.gle/GM1HcFEqrokHe6KV6

---

## Pick your task

You need ONE real task from your own work, sized to fit 30 minutes. Good candidates:

- A small feature you have been meaning to add
- A targeted bug fix with a clear symptom
- A test gap where a specific behavior is uncovered
- A doc repair where the written behavior does not match the actual behavior

Write your task statement in two lines before you do anything else:

```
What it does now:
What it should do when you are done:
```

Post that statement in meeting chat at **T+5**.

**No suitable real task?** Two alternatives:

- **Complete an extra credit item from any earlier lab you skipped.** Each lab card names its extra credit items. Pick one, write your two-line task statement around it, and run the loop below. The lab repo is your codebase.
- **Fix the `/api/tasks` console 404** you have seen all day. On a `capstone-work` branch cut from main, spec whether to implement `GET /api/tasks` (returns an empty list, no frontend changes needed) or to remove the dead call in `client/src/App.vue` near line 149 (no backend changes needed). Choosing is the spec exercise. Both resolutions are valid; your Acceptance Checks determine which one passes.

---

## The loop

Work in this order. Do not skip the human gate.

### 1. Spec in plan mode

Open a fresh `claude` session. Ask Claude to help you draft a spec, and to stay in plan mode — no edits to any file yet:

```
I want to spec out a task before implementing it. Stay in plan mode: no file changes yet. Help me write a spec for this: [your two-line task statement]
```

Save the spec to `specs/capstone.md` in this repo. The spec must have exactly these six sections:

```markdown
## Overview
## API or Interface
## Data & Persistence
## UI or Behavior Changes
## Out of Scope
## Acceptance Checks
```

If a section does not apply to your task, write "N/A" and one sentence explaining why.

### 2. Human gate

Read the spec yourself against this five-item checklist:

- [ ] The spec covers exactly one artifact or behavior — not a refactor of everything you have ever wanted to fix
- [ ] The implementation reuses existing structures (existing routes, components, models) rather than inventing new patterns
- [ ] Error cases are named explicitly (what happens when the input is wrong, the resource is missing, or the call fails)
- [ ] Data persistence is stated (in-memory, committed to a file, or deliberately ephemeral — one of these must be written down)
- [ ] Out of Scope has at least one entry, and Acceptance Checks are runnable by you on screen without a test harness

If any item is unchecked, iterate with Claude in the same session. You have two rounds of iteration budget.

When every item is checked, approve. Then read the diff of `specs/capstone.md` to confirm it matches what you approved.

Post "spec approved — specs/capstone.md" in meeting chat at **T+10**.

### 3. /clear

Run `/clear` to start a clean context window. This is the hard boundary between planning and implementation. The spec file is on disk; Claude will read it when you point to it.

### 4. Implement

In the fresh session:

```
Implement the spec at specs/capstone.md. Read it first, then make the changes. Show me each diff before writing any file.
```

Read every diff against the spec before approving. If a diff introduces something not in the spec, either update the spec first (with a plan-mode pass) or reject the diff. The spec is the source of truth.

At **T+20** post your status in meeting chat: "implementing" or "stuck on [one-sentence description]."

### 5. Verify

Run the Acceptance Checks from your spec. Each one must pass on screen.

Post at least one passing Acceptance Check result in meeting chat at **T+25**.

### 6. Commit locally

When every Acceptance Check passes:

```
Commit the changes locally. Do not push. Message: "Capstone: [your one-line task description]"
```

Check the commit exists:

```
git log --oneline -3
```

---

## Done definition

Write this before you implement (in the Acceptance Checks section of your spec). Done means:

- Every Acceptance Check in your spec passes on screen
- Every accepted diff traces to a line in your spec (nothing snuck in)
- A local commit exists with your changes

That is it. There is no answer key — real work has none.

---

## Timed check-ins

| Time | Post in meeting chat |
|------|----------------------|
| T+5 | Your two-line task statement |
| T+10 | "spec approved" and the spec filename |
| T+20 | "implementing" or "stuck on ..." |
| T+25 | One passing Acceptance Check result |
| T+30 | Done, or your honest final status |

If you are stuck at any check-in, post in chat and a TA will respond or open a breakout.

---

## Stuck paths

| Situation | Recovery |
|-----------|----------|
| Spec keeps growing past the human gate checklist | Add one more Out of Scope entry and cut. The goal is a spec you can finish in 15 minutes, not a complete system design. |
| Claude starts implementing before you run /clear | Type Esc, then `/clear`, then re-point Claude at the spec with the implement prompt above. |
| Implementation diverges from the spec | Stop. Ask Claude: "What in the diff does not trace to a line in specs/capstone.md?" Fix the spec or revert the diff — do not accept both. |
| Acceptance Checks all pass but the behavior looks wrong | Trust your eyes over the checklist. Update the Acceptance Checks and recheck. |
| Out of time before verifying | Post your last status and the spec filename. A complete spec with a partial implementation is a legitimate outcome for 30 minutes. |
