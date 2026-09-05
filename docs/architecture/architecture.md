# Initial Backend Architecture

## 1. High-Level Architecture

The original backend is a small FastAPI application served by Uvicorn. It uses
synchronous SQLAlchemy with the psycopg PostgreSQL driver. Configuration is
loaded from environment variables through pydantic-settings. Its initial
endpoint is `GET /health`, which checks both application availability and
PostgreSQL connectivity. The current phase extends this foundation with
database-backed authentication sessions.

Authentication is added as a simple database-backed session layer. Users and
sessions are stored in PostgreSQL, while authorization/RBAC and additional
infrastructure remain deferred.

## 2. Project Structure

```text
app/
├── __init__.py
├── main.py
├── config.py
├── database.py
├── models.py
└── auth.py

tests/
├── __init__.py
├── conftest.py
├── test_health.py
└── test_auth.py

alembic/
└── ...

pyproject.toml
.env.example
README.md
```

## 3. Module Responsibilities

- `app/main.py`: Creates the FastAPI application and defines `GET /health`.
- `app/config.py`: Defines application settings and loads environment-based
  configuration with pydantic-settings.
- `app/database.py`: Creates the SQLAlchemy engine and provides the
  PostgreSQL connectivity check.
- `app/models.py`: Defines the minimal user and session database models.
- `app/auth.py`: Provides password hashing, session creation/lookup, and
  authentication helpers.
- `tests/conftest.py`: Provides shared test fixtures and test substitutions.
- `tests/test_health.py`: Tests healthy and unavailable database responses.
- `pyproject.toml`: Defines dependencies, project metadata, and test
  configuration.
- `.env.example`: Documents required environment variables without secrets.
- `alembic/`: Contains database migrations for the authentication schema.

## 4. Request Flow: `GET /health`

1. Uvicorn receives the HTTP request and passes it to FastAPI.
2. FastAPI invokes the `/health` route in `app/main.py`.
3. The route asks `app/database.py` to execute `SELECT 1` through SQLAlchemy.
4. If the query succeeds, the endpoint returns HTTP `200` with a healthy
   status.
5. If PostgreSQL cannot be reached, the endpoint returns HTTP `503` with an
   unhealthy status.

## 5. Configuration Flow

```text
Environment variables / optional .env
                ↓
       pydantic-settings Settings
                ↓
           DATABASE_URL
                ↓
       SQLAlchemy database engine
```

The settings object is created centrally and used by the database module.
Routes do not read environment variables directly.
`DATABASE_URL` is the required environment variable.

## 6. Database Connection Flow

`app/database.py` creates one synchronous SQLAlchemy engine from
`DATABASE_URL`, using a URL such as:

```text
postgresql+psycopg://user:password@localhost:5432/database
```

For each connectivity check, SQLAlchemy obtains a connection from its pool
and executes `SELECT 1`. The connection is released after the check. The
health-check portion did not require domain models or migrations; the current
authentication phase adds models managed through the Alembic migrations
described below.
Standard SQLAlchemy connection pooling defaults will be used initially.
Database errors are handled so the endpoint returns `503` without exposing
internal error details.

## 7. Testing Approach

pytest and HTTPX exercise the FastAPI application through its HTTP interface.
The default tests replace the database check so they do not require a live
PostgreSQL server. They verify:

- A successful database check produces HTTP `200`.
- A failed database check produces HTTP `503`.
- Configuration reads `DATABASE_URL` from the environment.

Actual PostgreSQL connectivity will be verified separately, rather than as
part of the default mocked test suite.

## 8. Authentication Architecture

Authentication uses database-backed sessions rather than JWTs. A successful
login creates a cryptographically random session token, sends it in an
HttpOnly cookie, and stores only a hash of the token in PostgreSQL. Sessions
have a fixed 24-hour expiration and can be revoked during logout.

The cookie uses `HttpOnly` and `SameSite=Lax`. `Secure` is enabled in HTTPS
environments. Because cookies are sent automatically by browsers,
state-changing authenticated endpoints must account for CSRF protection.

Authentication establishes who the user is. It does not grant permissions.
Authorization and RBAC are a later phase.

## 9. Authentication Database Schema

```text
users
-----
id             integer primary key
email          normalized unique not null
password_hash  Argon2id hash not null
is_active      boolean not null default true
created_at     timestamp not null
updated_at     timestamp not null

sessions
--------
id             integer primary key
user_id        foreign key to users.id
token_hash     unique not null
created_at     timestamp not null
expires_at     timestamp not null
revoked_at     timestamp nullable
```

Alembic will manage creation and future changes to these tables. Plaintext
or reversibly encrypted passwords and raw session tokens are never stored.

## 10. Authentication Lifecycle

```text
registration → Argon2id password hash stored with user
      ↓
login validates password → random session token → HttpOnly cookie
      ↓
authenticated request looks up token hash and user
      ↓
logout revokes session and clears cookie
      ↓
24-hour expiration also invalidates the session
```

## 11. Authentication API

- `POST /auth/register`: Creates a user; duplicate normalized emails are
  rejected without returning a password hash.
- `POST /auth/login`: Validates credentials and creates a session cookie.
  Invalid credentials use a generic `401` response.
- `GET /auth/me`: Returns the authenticated user or `401` when no valid
  session exists.
- `POST /auth/logout`: Revokes the current session and clears the cookie.

## 12. Authentication Security and Scope

Passwords use Argon2id and are never stored plaintext or reversibly. Login
errors are generic to reduce account enumeration. Session tokens are
cryptographically random; only their hashes are persisted. Cookies are
HttpOnly, SameSite=Lax, and Secure under HTTPS. Sessions have fixed
expiration, and cookie-authenticated state changes require CSRF consideration.

This phase excludes RBAC, OAuth/social login, JWTs, refresh tokens, password
reset, email verification, MFA, rate limiting, background workers, Redis, and
other new infrastructure.

## 13. Architecture Diagram

```text
                 HTTP GET /health
                        │
                        ▼
                  Uvicorn
                        │
                        ▼
              FastAPI application
                 (app/main.py)
                        │
                        ▼
             Database health check
                 (app/database.py)
                        │
              SQLAlchemy + psycopg
                        │
                        ▼
                    PostgreSQL

Authentication requests ──► session/user models ──► PostgreSQL
                                   │
                                   └──► HttpOnly session cookie

Environment variables ──► pydantic-settings
                                  │
                                  └──► DATABASE_URL ──► SQLAlchemy engine
```
