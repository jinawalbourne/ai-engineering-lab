# Architecture Decisions

## Initial Backend Architecture

### Status

Accepted

### Context

The AI Engineering Lab is a learning project focused on understanding
AI-assisted software engineering and production development.

The initial backend requires:

- FastAPI
- PostgreSQL connectivity
- Environment-based configuration
- Automated tests
- A health endpoint

### Decision

The initial backend will use a simple module-based architecture:

- FastAPI for the web framework
- Uvicorn as the ASGI server
- SQLAlchemy for database access
- psycopg as the PostgreSQL driver
- pydantic-settings for configuration
- pytest and HTTPX for testing

The backend will use synchronous SQLAlchemy because the current
requirements do not justify the additional complexity of asynchronous
database operations.

The `/health` endpoint will verify PostgreSQL connectivity using
`SELECT 1`.

The endpoint response contract is:

- HTTP 200: `{"status": "healthy"}`
- HTTP 503: `{"status": "unhealthy"}`

If PostgreSQL is unavailable, `/health` will return HTTP 503. Database
errors will be handled without exposing internal error details.

The required environment variable is `DATABASE_URL`. Standard SQLAlchemy
connection pooling defaults will be used initially.

The default automated tests will mock the database health check. Actual
PostgreSQL connectivity will be verified separately.

Authorization, caching, rate limiting, background workers, Docker, cloud
deployment, and load balancing are intentionally deferred.

### Rationale

The goal is to keep the initial architecture simple and understandable.
Additional infrastructure will only be introduced when the project
reaches a requirement that justifies it.

### Consequences

This architecture is easy to understand and appropriate for the
current learning stage.

It is not intended to represent the final architecture of a
high-scale production system.

## Database-Backed Authentication Sessions

### Status

Accepted

### Context

The next learning phase requires user registration, login, authenticated
requests, and logout without introducing distributed infrastructure.

### Decision

Authentication will use PostgreSQL-backed sessions:

- Users have an integer primary key and a normalized unique email.
- Passwords are hashed with Argon2id; plaintext and reversible password
  storage are prohibited.
- Login creates a cryptographically random session token.
- The token is delivered in an HttpOnly cookie and only its hash is stored in
  PostgreSQL.
- Sessions expire after a fixed 24 hours and can be revoked on logout.
- Cookies use SameSite=Lax and Secure in HTTPS environments.
- Alembic manages the users and sessions schema.
- The minimum endpoints are registration, login, current-user, and logout.

Authentication identifies the user; authorization and RBAC remain separate
and are not part of this phase. JWTs, refresh tokens, OAuth/social login,
Redis, and background workers are excluded.

### Rationale

Database-backed sessions are easier to revoke and explain than JWTs for this
single-application learning project. PostgreSQL already exists, so no Redis
or other session infrastructure is needed. The design teaches password
hashing, cookies, session expiration, revocation, and CSRF considerations
without adding distributed-system complexity.

### Consequences

Authenticated requests perform a session lookup in PostgreSQL. The design
requires secure cookie handling and CSRF consideration for state-changing
requests. Password hashing and migration tooling add dependencies that must
be approved before implementation.
