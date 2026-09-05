# API Design

## `GET /health`

### Purpose

Reports whether the FastAPI application is running and PostgreSQL is
reachable.

### Request

```http
GET /health
```

The request has no body or required parameters.

Authentication is not required. Authentication and authorization are out of
scope for the initial backend.

### Responses

#### Healthy application and database

Status: `200 OK`

```json
{
  "status": "healthy"
}
```

#### PostgreSQL unavailable

Status: `503 Service Unavailable`

```json
{
  "status": "unhealthy"
}
```

The endpoint determines database availability by executing `SELECT 1` through
SQLAlchemy and psycopg. Database errors are handled without exposing internal
error details.

### HTTP Status Codes

- `200 OK`: The application is running and PostgreSQL connectivity succeeds.
- `503 Service Unavailable`: The application is running, but PostgreSQL is
  unavailable.

### Example

Request:

```bash
curl http://localhost:8000/health
```

Successful response:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{"status":"healthy"}
```

## Authentication API

Authentication uses a PostgreSQL-backed session cookie. No endpoint in this
phase grants authorization or RBAC permissions.

### `POST /auth/register`

Creates a user from a normalized email and password. A successful request
returns `201 Created`; duplicate emails return `409 Conflict`. Passwords are
never returned.

```json
{
  "email": "user@example.com",
  "password": "example-password"
}
```

### `POST /auth/login`

Validates credentials and creates a fixed 24-hour session. The response sets
an HttpOnly, SameSite=Lax cookie, with Secure enabled in HTTPS environments.
Invalid credentials return a generic `401 Unauthorized` response.

```json
{
  "email": "user@example.com",
  "password": "example-password"
}
```

### `GET /auth/me`

Returns the current authenticated user. A missing, expired, or revoked session
returns `401 Unauthorized`.

### `POST /auth/logout`

Revokes the current session and clears the session cookie. The operation may
return `204 No Content` when no valid session exists.

Cookie-authenticated state-changing requests require CSRF consideration.
