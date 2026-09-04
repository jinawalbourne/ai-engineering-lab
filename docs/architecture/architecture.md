# Initial Backend Architecture

## 1. High-Level Architecture

The backend is a small FastAPI application served by Uvicorn. It uses
synchronous SQLAlchemy with the psycopg PostgreSQL driver. Configuration is
loaded from environment variables through pydantic-settings. The initial
endpoint is `GET /health`, which checks both application availability and
PostgreSQL connectivity.

Authentication, authorization, migrations, caching, rate limiting, background
workers, and additional infrastructure are intentionally deferred.

## 2. Project Structure

```text
app/
├── __init__.py
├── main.py
├── config.py
└── database.py

tests/
├── __init__.py
├── conftest.py
└── test_health.py

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
- `tests/conftest.py`: Provides shared test fixtures and test substitutions.
- `tests/test_health.py`: Tests healthy and unavailable database responses.
- `pyproject.toml`: Defines dependencies, project metadata, and test
  configuration.
- `.env.example`: Documents required environment variables without secrets.

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
and executes `SELECT 1`. The connection is released after the check. No
database models or migrations are required for the initial task.
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

## 8. Architecture Diagram

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

Environment variables ──► pydantic-settings
                                  │
                                  └──► DATABASE_URL ──► SQLAlchemy engine
```
