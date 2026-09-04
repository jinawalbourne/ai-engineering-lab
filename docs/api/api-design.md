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
