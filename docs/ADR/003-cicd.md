# ADR-003: CI/CD - GitHub Actions + Docker Hub + Kubernetes

## Context

Project Atmos requires a CI/CD process that provides a controlled path from application changes to deployed workloads.

The delivery process must:

- validate changes with linting and tests;
- build and publish immutable Docker images;
- support automated DEV delivery;
- require explicit approval for PROD releases;
- keep application, Kubernetes, and infrastructure responsibilities separated.

Project Atmos uses three repositories:

| Repository | Responsibility |
|---|---|
| `project-atmos-dev` | Application, Docker, Compose, CI |
| `project-atmos-k8s` | Kubernetes and deployment configuration |
| `project-atmos-iac` | AWS infrastructure with Terraform |

## Decision

We choose **GitHub Actions** as the CI/CD automation platform and **Docker Hub** as the container registry.

The delivery flow is:

```text
Code
 ↓
GitHub Actions
 ↓
Lint → Tests → Build
 ↓
Docker Image
 ↓
Docker Hub
 ↓
DEV
 ↓
Validation
 ↓
Manual approval
 ↓
PROD
```

Docker images use immutable tags:

```text
<service>:<git-sha>
```

Production releases use explicit version tags:

```text
<service>:v1.0.0
```

Application CI is managed in `project-atmos-dev`. Kubernetes deployment is managed separately in `project-atmos-k8s`, while AWS infrastructure is managed through Terraform in `project-atmos-iac`.

## Why

- **Project fit:** GitHub Actions integrates directly with the project's GitHub workflow.
- **Simplicity:** No separately managed CI/CD platform is required.
- **Reproducibility:** Immutable image tags allow deployments to reference specific application versions.
- **Repository separation:** Application, Kubernetes, and infrastructure responsibilities remain separated.
- **Operational fit:** GitHub Actions, Docker Hub, and Kubernetes provide the required delivery path without unnecessary infrastructure.

## Consequences

- **Positive:** Application changes are automatically validated and packaged.
- **Positive:** Docker images are versioned and stored in a dedicated registry.
- **Positive:** DEV delivery can be automated while PROD remains controlled.
- **Positive:** Application, Kubernetes, and infrastructure workflows remain independently managed.
- **Trade-off:** The delivery process depends on GitHub Actions, Docker Hub, and AWS.
- **Trade-off:** Multiple repositories require coordination between application and deployment configuration.