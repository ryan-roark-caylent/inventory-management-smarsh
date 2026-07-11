# Repo-type briefs (for the CLAUDE.md template exercise)

Pick ONE. Write a CLAUDE.md template section that fits THIS repo type — not the
inventory-management demo.

## Brief 1 — Java/Spring microservice
Build: Maven. Test: JUnit 5 + Mockito. Layered controller/service/repository.
DTOs for all request/response bodies. Secrets in a vault profile. Deployed
behind an API gateway; response contracts are consumed by other teams.

## Brief 2 — Shared Python library (published to an internal index)
No app to run; it is imported by other repos. Semantic versioning matters.
Public API stability is a hard rule. Tests must cover the public surface.
Breaking changes require a major-version bump and a changelog entry.

## Brief 3 — Data-pipeline repo (batch ETL)
Jobs run on a scheduler. Idempotency and re-run safety are non-negotiable.
Config lives in environment-specific files. Failures must be observable and
retryable. No interactive UI.
