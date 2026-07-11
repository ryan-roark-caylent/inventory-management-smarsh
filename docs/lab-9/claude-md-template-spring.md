# CLAUDE.md template — Java/Spring microservice

## Build & test
- Build: `mvn clean package`
- Test: `mvn test`   (JUnit 5 + Mockito)

## Conventions
- Controller -> Service -> Repository layering; no business logic in controllers.
- DTOs for all request/response bodies; never expose JPA entities directly.
- Snake_case for JSON field names; camelCase for Java identifiers.

## Always / Never
- ALWAYS validate request bodies with `@Valid`.
- NEVER put secrets in `application.properties`; use the vault profile.
- ALWAYS return a consistent error envelope: `{ "error": "<message>", "status": <code> }`.
- NEVER bypass the service layer from a controller to call the repository directly.

## API contracts
Response shapes are consumed by other teams. Removing or renaming a field is a
breaking change — bump the major version and add a changelog entry.

---

**What changes vs the inventory-management template:**
- Build/test is Maven + JUnit, not `uv run pytest`; the controller/service/repository
  layering rule is Spring-specific and has no equivalent in the FastAPI in-memory demo.
- A shared microservice behind an API gateway needs an API-contract-stability rule
  (versioning, breaking-change policy) that the single-team in-memory demo does not.
