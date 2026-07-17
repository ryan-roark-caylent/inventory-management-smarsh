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
   - Switch away: if this checkout is a git worktree (`git rev-parse --git-dir` differs from `git rev-parse --git-common-dir`), `main` is usually held by the main clone and `git checkout main` will fail -- switch to the lab's start branch you began from instead (e.g. `git checkout lab-3-start`); otherwise switch to main: `git checkout main`
   - Delete the feature branch: `git branch -D <branch-name>`
   - Show result: `git status` and `git branch`

WARNING: Permanently deletes the feature branch and all its commits/changes. Also discards ALL working directory changes and removes untracked files.
