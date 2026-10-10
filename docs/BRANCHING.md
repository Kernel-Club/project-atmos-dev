# Branching Model — Project Atmos

## 1. Overview

Project Atmos uses a branch-based development workflow to separate feature development, integration, and production releases.

The `main` branch contains stable production-ready code. The `develop` branch integrates changes before they are promoted to production.

## 2. Branch Structure

| Branch | Purpose | Source | Target |
|---|---|---|---|
| `main` | Production-ready code | `develop` | Production |
| `develop` | Development integration and testing | `main` (initial setup) | Development |
| `feature/*` | New features and functionality | `develop` | `develop` |
| `fix/*` | Bug fixes | `develop` | `develop` |
| `release/*` | Optional release stabilization | `develop` | `main` |

## 3. Development Workflow

### Feature Development

1. Create a feature branch from `develop`.
2. Implement the change and commit using Conventional Commits.
3. Open a Pull Request targeting `develop`.
4. Ensure CI checks pass.
5. Merge the Pull Request into `develop`.

Example:

`feature/weather-cache`

### Bug Fixes

1. Create a fix branch from `develop`.
2. Implement and test the fix.
3. Open a Pull Request targeting `develop`.
4. Ensure CI checks pass.
5. Merge the Pull Request into `develop`.

Example:

`fix/weather-api-timeout`

## 4. CI Pipeline

GitHub Actions runs CI on pushes and Pull Requests targeting `main` and `develop`.

The pipeline includes:

- Backend linting with Ruff.
- Backend tests with pytest.
- Frontend linting.
- Frontend production build.
- Docker image build and publication.

Docker images are published to Docker Hub with immutable Git commit SHA tags:

- `streetflow13/project-atmos-backend:<git-sha>`
- `streetflow13/project-atmos-frontend:<git-sha>`

Docker publication runs on pushes to `main` and `develop`, after the backend and frontend jobs succeed. Pull Requests run the validation jobs without publishing Docker images.

## 5. Production Release Workflow

1. Changes are integrated and validated in `develop`.
2. A Pull Request is opened from `develop` to `main`.
3. CI checks must pass before merging.
4. The Pull Request is reviewed and merged.
5. The resulting production commit is identified by its Git SHA.
6. The corresponding Docker images are available using that SHA tag.

Direct commits to `main` are exceptions for urgent, explicitly justified changes. Such changes must be validated by CI and synchronized back to `develop`.

## 6. Release Branches and Versioning

The `release/*` branch convention is reserved for cases requiring a separate stabilization period before production.

Semantic Versioning (`vMAJOR.MINOR.PATCH`) and automated GitHub Releases are planned enhancements. They are not yet part of the active release workflow.

## 7. Branch Synchronization

When changes are made directly to `main`, or production fixes need to be incorporated into development, synchronize `main` back into `develop` through a Pull Request.

This keeps both branches consistent and prevents fixes from being lost in subsequent development.

## 8. Branch Protection and Permissions

GitHub Rulesets are not enforced for this private repository under the current organization plan.

Therefore, the branching policy is currently enforced through the team's development process rather than guaranteed by GitHub branch protection.

Pull Requests and successful CI checks are the standard requirements for integrating changes. No paid GitHub plan upgrade is assumed.

## 9. Environment Mapping

| Environment | Branch | Purpose |
|---|---|---|
| DEV | `develop` | Integration and development validation |
| PROD | `main` | Stable production releases |

The deployment infrastructure is maintained separately in the `project-atmos-k8s` and `project-atmos-iac` repositories.

## 10. Repository Responsibilities

- `project-atmos-dev`: application source, Dockerfiles, CI, and image publication.
- `project-atmos-k8s`: Kubernetes manifests, Kustomize overlays, and deployment configuration.
- `project-atmos-iac`: Terraform configuration and AWS infrastructure provisioning.

This separation keeps application development, deployment configuration, and cloud infrastructure independently maintainable.

## 11. Branching Workflow Diagram

```mermaid
flowchart TD
    F["feature/*"] -->|"Pull Request + CI"| D["develop"]
    X["fix/*"] -->|"Pull Request + CI"| D
    D -->|"Pull Request + CI + Review"| M["main"]
    M --> P["Production Release"]
    P -.->|"Sync fixes back"| D

    D --> CI_D["CI: Lint, Tests, Build"]
    M --> CI_M["CI: Lint, Tests, Build"]

    CI_D --> IMG_D["Docker images: SHA tags"]
    CI_M --> IMG_M["Docker images: SHA tags"]

    IMG_D --> DEV["DEV deployment"]
    IMG_M --> PROD["PROD deployment"]

    style D fill:#1f6feb,color:#fff,stroke:#388bfd
    style M fill:#238636,color:#fff,stroke:#3fb950
    style DEV fill:#1f6feb,color:#fff,stroke:#388bfd
    style PROD fill:#238636,color:#fff,stroke:#3fb950