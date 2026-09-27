# ADR-003: CI/CD — GitHub Actions + Docker Hub

## Status

In review

## Context

Project Atmos requires a CI/CD pipeline that:

- validates changes with linting and tests;
- builds Docker images;
- pushes images to a container registry;
- deploys the application to Kubernetes;
- provides a controlled path from development to production.

The project source code, issues, project board, and documentation are already managed in GitHub. The CI/CD solution should integrate naturally with this workflow without introducing unnecessary infrastructure.

## Options considered

1. **GitHub Actions + Docker Hub**
   - Native integration with the GitHub repository.
   - Supports linting, testing, Docker builds, registry authentication, and deployment workflows.
   - Docker Hub provides a dedicated registry with a clear UI for image and tag management.

2. **GitLab CI/CD**
   - Mature CI/CD platform with integrated pipelines and container registry.
   - Would require moving the repository and project workflow to GitLab or maintaining two platforms.

3. **Jenkins**
   - Widely used and highly customizable CI/CD platform.
   - Requires additional infrastructure, maintenance, configuration, and credentials management.

## Decision

We choose **GitHub Actions** as the CI/CD platform and **Docker Hub** as the container registry.

The initial deployment flow will be:

```text
Pull Request
    ↓
Lint
    ↓
Tests
    ↓
Build Docker Image
    ↓
Push to Docker Hub
    ↓
Deploy to Kubernetes Dev
    ↓
Validation
    ↓
Controlled Production Release
```

Docker images are published with immutable versioned tags, such as the Git commit SHA for development and an explicit release version for production.

## Why

- **Project fit:** GitHub Actions integrates directly with the existing GitHub repository and project workflow.
- **Simplicity:** No separate CI server or platform is required.
- **Operational fit:** Provides the required CI/CD capabilities for validation, image delivery, and Kubernetes deployment without introducing a separate CI platform.
- **Registry integration:** Docker Hub provides a dedicated container registry with versioned image tags and straightforward authentication for CI/CD.
- **Maintainability:** Pipeline configuration is version-controlled alongside the application and does not require a separately managed CI server.

## Consequences

- **Positive:** CI/CD configuration is stored alongside the application code.
- **Positive:** Pull requests can be automatically validated before deployment.
- **Positive:** Docker images are versioned and stored in a dedicated registry.
- **Positive:** Dev deployment can be automated while production remains controlled.
- **Trade-off:** GitHub Actions creates some dependency on the GitHub ecosystem.
- **Trade-off:** Docker Hub becomes an additional external service that must be configured and authenticated.