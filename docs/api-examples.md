# API Examples

This document provides practical `curl` examples for interacting with the Integration Middleware API, covering successful synchronization, status checks, error handling, and idempotency.

## 1. Synchronize a Customer

Synchronizes a customer from the source system to the target system.

**Request:**

```bash
curl -X POST "https://demos-integration-middleware.g4xorp.easypanel.host/sync/customers" \
  -H "Content-Type: application/json" \
  -d '{"source_customer_id": 1}'
```

**Response (201 Created):**

```json
{
  "id": 1,
  "source_customer_id": 1,
  "target_id": 100,
  "name": "Andrés Del Río",
  "email": "andres@example.com",
  "synced_at": "2026-10-16T21:05:35.658966+00:00"
}
```

## 2. Check Synchronization Status

Allows checking the details of a previously processed synchronization record using its unique identifier.

**Request:**

```bash
curl -X GET "https://demos-integration-middleware.g4xorp.easypanel.host/sync/customers/1"
```

**Response (200 OK):**

```json
{
  "id": 1,
  "source_customer_id": 1,
  "target_id": 100,
  "name": "Andrés Del Río",
  "email": "andres@example.com",
  "synced_at": "2026-10-16T21:05:35.658966+00:00"
}
```

## 3. Customer Not Found in Source

Attempts to synchronize an identifier that does not exist in the source system, returning a controlled error response.

**Request:**

```bash
curl -X POST "https://demos-integration-middleware.g4xorp.easypanel.host/sync/customers" \
  -H "Content-Type: application/json" \
  -d '{"source_customer_id": 999}'
```

**Response (404 Not Found):**

```json
{
  "detail": "source customer not found"
}
```

## 4. Idempotent Synchronization with Control Header

Demonstrates fault tolerance and retry capabilities through the use of the `Idempotency-Key` header to prevent duplicates during repeated operations.

**Request:**

```bash
curl -X POST "https://demos-integration-middleware.g4xorp.easypanel.host/sync/customers" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: abc-234" \
  -d '{"source_customer_id": 1}'
```

**Response (201 Created):**

```json
{
  "id": 1,
  "source_customer_id": 1,
  "target_id": 100,
  "name": "Andrés Del Río",
  "email": "andres@example.com",
  "synced_at": "2026-10-16T21:05:35.658966+00:00"
}
```
