# 30-day adoption plan (reference)

## This week
- Run the `gen-endpoint-tests` entry to add empty-data and bad-filter cases for
  `/api/spending/categories`, which only has happy-path coverage in
  `test_misc_endpoints.py`, this sprint.

## This month
- Get 2 teammates to each contribute 1 library entry and pass the cold-run gate
  before merging.

## Teach a colleague
- Run a 30-minute show-and-tell for my squad on the 5-point review checklist and
  the reuse + reliability gate — walk through the weak vs strong seeded entries live.

## Adoption metrics
Real (leading indicators of behavior change):
- Shared-library entry invocations per engineer per week — shows the good path is
  actually the easy path, not just installed.
- PR cycle time on AI-assisted reviews vs the sprint baseline — shows a workflow
  change, not just Claude Code usage.

Excluded (vanity):
- LMS logins / % certified — completion can mask zero behavior change; an engineer
  can finish the module and never open Claude Code again.
- Number of prompts in the library — count without reuse is a dump folder; 40
  entries no one opens is worse than 5 entries everyone reaches for.

## Champion cadence
Sustain via the pattern: weekly office hours (open slot, no agenda required) and a
regular show-and-tell (every two to four weeks, rotate who presents). No fixed
calendar dates — this programme is async and sprint schedules vary.
