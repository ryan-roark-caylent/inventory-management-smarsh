---
description: Switch to main and delete previous branch
---

Switch back to main branch and delete the branch you were on, discarding all commits and changes.

Steps:
1. Check current branch with `git branch --show-current`
2. If already on main/master, inform user no reset needed
3. If on feature branch:
   - Show commits to be lost: `git log main..HEAD --oneline`
   - Store the branch name
   - Discard all tracked changes FIRST: `git reset --hard HEAD` (a dirty tree would otherwise abort the branch switch below)
   - Remove untracked files: `git clean -fd` to remove untracked files and directories
   - Switch away: if this checkout is a git worktree (`git rev-parse --git-dir` differs from `git rev-parse --git-common-dir`), `main` -- and often the lab's start branch too -- is held by the main clone, so `git checkout main` will fail. Use a detached checkout of the start branch instead: `git checkout --detach origin/lab-N-start` (detached is fine for a reset). Otherwise switch to main: `git checkout main`
   - Delete the feature branch: `git branch -D <branch-name>`
   - Show result: `git status` and `git branch`

WARNING: Permanently deletes the feature branch and all its commits/changes. Also discards ALL working directory changes and removes untracked files.
