# Current Task

## Objective

Implement the authentication phase for the existing FastAPI backend.

## Requirements

- FastAPI application
- Health check endpoint
- Environment-based configuration
- PostgreSQL connection
- Automated tests

Authentication requirements:

- Database-backed sessions stored in PostgreSQL
- Integer user primary key and normalized unique email login identifier
- Argon2id password hashing
- Cryptographically random session token delivered in an HttpOnly cookie
- Only a hash of the session token stored in PostgreSQL
- Fixed 24-hour session expiration
- Alembic database migrations
- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`
- `POST /auth/logout`

The required environment variable is `DATABASE_URL`.

## Constraints

- Keep the architecture simple
- No unnecessary abstractions
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

Authentication acceptance criteria:

- Users can register with a normalized unique email and password.
- Passwords are stored only as Argon2id hashes.
- Successful login creates a PostgreSQL-backed session cookie.
- Authenticated requests can retrieve the current user.
- Logout revokes the session and clears the cookie.
- Expired sessions are rejected.

The `/health` response contract is:

- HTTP 200: `{"status": "healthy"}`
- HTTP 503: `{"status": "unhealthy"}`

Standard SQLAlchemy connection pooling defaults will be used initially.
Database errors must be handled without exposing internal error details.
The default automated tests will mock the database health check. Actual
PostgreSQL connectivity will be verified separately.

## Out of Scope

- Authorization / RBAC
- OAuth/social login
- JWT and refresh tokens
- Password reset, email verification, and MFA
- Caching
- Rate limiting
- Background workers
- Docker
- AWS
- Load balancing
