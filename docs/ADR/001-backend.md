# ADR-001: Backend — Python + FastAPI

## Status

In review

## Context

Project Atmos requires a lightweight HTTP API that:

- fetches weather data from OpenWeather;
- uses Redis for caching;
- stores and retrieves weather history in MongoDB;
- provides a clear API for the frontend;
- is easy to containerize and deploy to Kubernetes.

The backend should support the DevOps focus of the project without introducing unnecessary application complexity.

## Options considered

1. **Python + FastAPI**
   - Lightweight and well suited for HTTP APIs.
   - Simple project structure and containerization.
   - Provides built-in API documentation and validation.

2. **Node.js + Express**
   - Lightweight and widely used for web APIs.
   - Large ecosystem and straightforward Docker deployment.
   - Requires additional choices for validation and API documentation.

3. **Go + Gin**
   - Lightweight and efficient.
   - Produces small, self-contained binaries.
   - Adds a new language and ecosystem to the project.

## Decision

We choose **Python + FastAPI** for the backend.

The initial structure will remain intentionally simple:

```text
backend/
├── app/
│   ├── main.py
│   ├── api/
│   ├── services/
│   ├── clients/
│   └── models/
├── tests/
├── Dockerfile
└── requirements.txt
```

## Why

- **Project fit:** FastAPI provides everything required for a small HTTP API.
- **Simplicity:** Easy integration with OpenWeather, MongoDB, and Redis.
- **Engineering fit:** FastAPI provides a lightweight and maintainable foundation for the required HTTP API.
- **DevOps focus:** Keeps application complexity low so the project can focus on containers, Kubernetes, CI/CD, and observability.
- **Maintainability:** FastAPI provides a clear application structure and keeps the backend straightforward to operate and extend.

## Consequences

- **Positive:** Simple backend architecture and straightforward maintenance.
- **Positive:** Easy Docker and Kubernetes deployment.
- **Positive:** Built-in request validation and API documentation.
- **Positive:** Keeps the application layer intentionally lightweight and allows the architecture to focus on operational concerns.
- **Trade-off:** Python generally provides lower runtime performance than compiled languages such as Go, but the expected workload does not require that level of performance.