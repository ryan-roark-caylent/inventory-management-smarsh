#!/usr/bin/env bash
# Create one git worktree per lab, up front. Safe to re-run: skips any that already exist.
# Each lab gets ../lab-N-work on a new branch lab-N-work, created from origin/lab-N-start.
# Run from your clone of the fork.
set -uo pipefail

echo "Fetching latest branches..."
git fetch origin --quiet

created=0
skipped=0
for n in 1 2 3 4 5 6 7 8 9; do
  dir="../lab-${n}-work"
  branch="lab-${n}-work"
  if git worktree list | grep -q "lab-${n}-work"; then
    echo "  lab-${n}: already set up, skipping"
    skipped=$((skipped+1))
    continue
  fi
  if git show-ref --verify --quiet "refs/heads/${branch}"; then
    # branch exists but no worktree — attach it
    git worktree add "$dir" "$branch" && echo "  lab-${n}: worktree created (existing branch)" && created=$((created+1))
  else
    git worktree add -b "$branch" "$dir" "origin/lab-${n}-start" \
      && echo "  lab-${n}: worktree + branch created from origin/lab-${n}-start" \
      && created=$((created+1))
  fi
done

echo ""
echo "Done: ${created} created, ${skipped} already present."
echo "Start a lab with:  cd ../lab-1-work   (then open a fresh Claude Code session there)"
