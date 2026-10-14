# ADR-003: CI/CD - GitHub Actions + Docker Hub + Kubernetes

## Context

Project Atmos requires a CI/CD process that provides a controlled path from application changes to deployed workloads.

The delivery process must:

- validate changes with linting and tests;
- build and publish versioned Docker images;
- support automated DEV delivery;
- release to PROD only the image that was validated in DEV;
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
Lint → Tests → Build (develop only)
 ↓
Docker Image
 ↓
Docker Hub (dev tag)
 ↓
Automatic DEV deployment
 ↓
Validation
 ↓
Manual approval
 ↓
PROD promotion (same image, new tag)
```

Docker images use tags that include the environment, the application version, and the first 6 characters of the Git commit SHA:

```text
<service>:dev-v1.0.0-<sha6>
<service>:prod-v1.0.0-<sha6>
```

An image is built once, on `develop`. A PROD release adds a `prod-*` tag to the image that already passed DEV. The promotion is a manual workflow run that requires approval of the GitHub Environment `production`. PROD images are never rebuilt.

After a successful CI run on `develop`, the CD workflow deploys to DEV automatically. It sets the image tag in the Kustomize DEV overlay from `project-atmos-k8s`, applies it to Amazon EKS, and verifies the rollout. A failed rollout fails the workflow.

GitHub Actions authenticates to AWS with GitHub OIDC and short-lived credentials. No long-lived AWS keys are stored.

Application CI is managed in `project-atmos-dev`. Kubernetes deployment is managed separately in `project-atmos-k8s`, while AWS infrastructure is managed through Terraform in `project-atmos-iac`.

## Why

- **Project fit:** GitHub Actions integrates directly with the project's GitHub workflow.
- **Simplicity:** No separately managed CI/CD platform is required.
- **Reproducibility:** Versioned image tags allow deployments to reference specific application versions and commits.
- **Same artifact in DEV and PROD:** Promoting a tag instead of rebuilding guarantees that PROD runs exactly what was validated in DEV.
- **No stored cloud keys:** OIDC removes long-lived AWS credentials from GitHub.
- **Repository separation:** Application, Kubernetes, and infrastructure responsibilities remain separated.
- **Operational fit:** GitHub Actions, Docker Hub, and Kubernetes provide the required delivery path without unnecessary infrastructure.

## Consequences

- **Positive:** Application changes are automatically validated and packaged.
- **Positive:** Docker images are versioned and stored in a dedicated registry.
- **Positive:** DEV delivery is automated while PROD remains controlled.
- **Positive:** Application, Kubernetes, and infrastructure workflows remain independently managed.
- **Trade-off:** The delivery process depends on GitHub Actions, Docker Hub, and AWS.
- **Trade-off:** Multiple repositories require coordination between application and deployment configuration.
- **Trade-off:** The application version is set in `APP_VERSION` in both `ci.yml` and `cd.yml` and must be changed in both places.
- **Trade-off:** Docker Hub does not enforce tag immutability here. Tags are treated as immutable by convention.
- **Trade-off:** PROD promotion currently only tags the image. Deployment to the PROD namespace requires the infrastructure work in `project-atmos-iac`.
