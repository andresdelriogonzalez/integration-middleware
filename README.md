# Integration Middleware

Sincroniza clientes entre un sistema origen y un sistema destino via REST. Implementado en Python/FastAPI contra el OpenAPI, con TDD, idempotencia y despliegue en Docker.

**Demo en vivo:** https://demos-integration-middleware.g4xorp.easypanel.host/

## Arquitectura

Sistema origen (mock) --> Middleware --> Sistema destino (mock)

El middleware existe en implementación python-impl, validada contra suite de tests de aceptacion (tests/)y usando contrato (openapi/openapi.yaml) independiente del lenguaje.

## Como correrlo en local

python3 -m venv .venv && source .venv/bin/activate
pip install -r python-impl/requirements.txt
python3 mocks/source-system/source_mock.py &
python3 mocks/target-system/target_mock.py &
uvicorn main:app --reload --port 8096 --app-dir python-impl
pytest tests/

## Decisiones tecnicas

- Contract-first: el OpenAPI se escribio antes que el codigo (ver openapi/openapi.yaml).
- TDD: los tests de aceptacion se escribieron antes de la implementacion.
- Idempotencia: header Idempotency-Key evita duplicados en reintentos.
- Docker: docker-compose.yml levanta los 3 servicios juntos.

## Estructura del repo

openapi/        contrato compartido
mocks/          sistemas simulados para desarrollo
python-impl/    implementacion en FastAPI
tests/          suite de aceptacion (corre contra cualquiera de las dos implementaciones)