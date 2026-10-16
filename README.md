# Integration Middleware

Synchronizes customers between a source system and a target system via REST. Implemented in Python/FastAPI following an OpenAPI contract, featuring TDD, idempotency, and Docker deployment.

**Live Demo:** https://demos-integration-middleware.g4xorp.easypanel.host/

## Architecture

Source system (mock) --> Middleware --> Target system (mock)

The middleware is implemented in Python (`python-impl`), validated against an acceptance test suite (`tests/`), and uses a language-independent API contract (`openapi/openapi.yaml`).

## How to Run Locally

python3 -m venv .venv && source .venv/bin/activate
pip install -r python-impl/requirements.txt
python3 mocks/source-system/source_mock.py &
python3 mocks/target-system/target_mock.py &
uvicorn main:app --reload --port 8096 --app-dir python-impl
pytest tests/

## Technical Decisions

- **Contract-first:** The OpenAPI contract was written before any code (see `openapi/openapi.yaml`).
- **TDD:** Acceptance tests were written prior to the implementation.
- **Idempotency:** The `Idempotency-Key` header prevents duplicate records during retries.
- **Docker:** `docker-compose.yml` spins up all 3 services together.

## Repository Structure

- `mocks/`          Simulated systems for development
- `openapi/`        Shared API contract
- `tests/`          Acceptance test suite
- `python-impl/`    FastAPI implementation

## API Call Examples

See [docs/api-examples.md](docs/api-examples.md) for concrete API calls and usage examples.

