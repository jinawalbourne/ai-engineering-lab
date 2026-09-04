# Current Task

## Objective

Set up the initial FastAPI backend for the AI Engineering Lab.

## Requirements

- FastAPI application
- Health check endpoint
- Environment-based configuration
- PostgreSQL connection
- Automated tests

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

## Out of Scope

- Authentication
- Authorization / RBAC
- Caching
- Rate limiting
- Background workers
- Docker
- AWS
- Load balancing