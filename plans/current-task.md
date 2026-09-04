# Current Task

## Objective

Set up the initial FastAPI backend for the AI Engineering Lab.

## Requirements

- FastAPI application
- Health check endpoint
- Environment-based configuration
- PostgreSQL connection
- Automated tests

The required environment variable is `DATABASE_URL`.

## Constraints

- Keep the architecture simple
- No unnecessary abstractions
- No authentication yet
- No authorization yet
- No Redis yet
- No Docker yet
- No cloud deployment yet

## Acceptance Criteria

- Application starts locally
- `GET /health` returns `200`
- PostgreSQL connection works
- Automated tests pass
- Configuration is environment-based

The `/health` response contract is:

- HTTP 200: `{"status": "healthy"}`
- HTTP 503: `{"status": "unhealthy"}`

Standard SQLAlchemy connection pooling defaults will be used initially.
Database errors must be handled without exposing internal error details.
The default automated tests will mock the database health check. Actual
PostgreSQL connectivity will be verified separately.

## Out of Scope

- Authentication
- Authorization / RBAC
- Caching
- Rate limiting
- Background workers
- Docker
- AWS
- Load balancing
