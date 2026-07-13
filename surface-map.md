# Surface Selection Map — Lab 1

**Example — not the only correct routing. Your reasoning matters more than matching this exactly.**

## The three surfaces — one line each ("when I'd use this")
- Claude.ai: When I want to think through a design problem or get a general explanation, without giving it repo access.
- Claude Code: When the task requires reading files, tracing across the repo, or proposing a code change with exact file and line context.
- API / CI: When the task needs to run unattended, non-interactively, on a schedule or in a pipeline with no human in the loop.

## Issue routing (fill in BEFORE opening any tool)
- Issue A (spec/planning) -> surface: Claude.ai because: no code exists yet; this is design thinking and open questions, best worked through in a conversational session before anyone writes anything.
- Issue B (multi-file refactor) -> surface: Claude Code because: it needs to read Reports.vue and api.js, trace the call pattern, and propose a precise diff — Claude Code can read the repo and anchor its suggestions to real file locations.
- Issue C (batch/CI script) -> surface: API / CI because: it runs unattended on a schedule with no human in the loop; that is exactly the API surface's job.

## The bug: Claude.ai vs Claude Code
### Round 1 (Claude.ai) hypothesis:
The backlog count is likely computed from the full dataset rather than the filtered subset. Check whether the filter is applied to backlog items the same way it is applied to the other summary metrics.
*(No file or line — Claude.ai reasons from the symptom alone.)*

### Round 2 (Claude Code) — file, line, fix:
Found in `server/main.py` line 200 inside `get_dashboard_summary`. Every other field uses `filtered_inventory` or `filtered_orders`; the backlog count uses the global `backlog_items`. Minimal fix:
```python
total_backlog_items = len(apply_filters(backlog_items, warehouse, category))
```
Caveat: `BacklogItem` has no `warehouse` field, so this fix returns 0 under any warehouse filter — pattern-consistent, but not production-complete until the model is extended.
