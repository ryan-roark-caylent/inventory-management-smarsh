# Smarsh AI-SDLC Hands-On Labs

This repository is the code substrate for the 9-lab Claude Code training series. **The lab instructions do not live on `main`.** Each lab ships as its own branch.

## How to run a lab

1. Make sure your environment meets the prerequisites (see the LMS pre-work / the lab prerequisites checklist).
2. Check out the lab's start branch:
   ```
   git fetch origin
   git checkout -b lab-N-work origin/lab-N-start
   ```
   (Replace `N` with the lab number, 1 through 9.)
3. Open the lab card on that branch: `labs/lab-N/participant-guide.md`. It has everything you need — the scenario, the steps, and how to know you're done.
4. Work through the card in a fresh Claude Code session.
5. When you finish, take that lab's **completion** and **mastery** quizzes in the LMS (MindTickle).

## Rules of the road

- Each start branch is a **clean, independent starting point** — you do not need to have done the earlier labs first.
- If you get stuck, every card has a "stuck path" that ends with checking out `lab-N-solution` so you never leave empty-handed.
- Quizzes and answer keys are **not** in this repository — they are delivered through the LMS.

## What's on each branch

| Branch | Contents |
|--------|----------|
| `main` | App code + this guide. No lab instructions. |
| `lab-N-start` | The app code plus that lab's card (`labs/lab-N/participant-guide.md`) and any planted setup. Your starting point. |
| `lab-N-solution` | The reference answer for lab N (for the stuck path and facilitators). |

Labs 1-9 cover: tool/surface selection, Claude as a thinking partner, CLAUDE.md + context, spec-driven development, multi-step workflows, Claude skills, sub-agents/MCP/automation, code review + responsible use, and team adoption.
