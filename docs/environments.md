# Project Atmos — Environments

## 1. Overview

Project Atmos uses two Kubernetes environments:

- **dev** — development, testing, and CI/CD deployment target.
- **prod** — controlled environment for released versions.

Both environments use the same application architecture and Kubernetes base manifests.

Environment-specific configuration is managed with Kustomize overlays.

```text
k8s/
├── base/
├── overlays/
│   ├── dev/
│   └── prod/
```

---

## 2. Environment Matrix

| Configuration | Dev | Prod |
|---|---|---|
| Namespace | `dev` | `prod` |
| Purpose | Development and validation | Released application |
| Frontend replicas | 1 | 2 |
| Backend replicas | 1 | 2 |
| Resource limits | Lower | Higher |
| Log level | More detailed | Normal |
| Image tag policy | Git commit SHA | Explicit release version |
| Ingress host | Dev-specific host | Prod-specific host |
| Deployment | Automated by CI/CD | Controlled release |
| MongoDB | Persistent storage | Persistent storage |
| Redis | Non-persistent cache | Non-persistent cache |

---

## 3. Kustomize

The Kubernetes `base` contains common resources shared by both environments.

The overlays define environment-specific differences.

```text
base
  │
  ├── common Deployments
  ├── Services
  ├── ConfigMaps
  ├── Secrets
  ├── Storage
  └── Ingress
       │
       ├── dev overlay
       └── prod overlay
```

Example commands:

```bash
kubectl apply -k k8s/overlays/dev
kubectl apply -k k8s/overlays/prod
```

---

## 4. Ingress

Each environment uses its own hostname while keeping the same path-based routing:

```text
/      → Frontend Service
/api/* → Backend Service
```

The exact `nip.io` hosts are environment-specific.

Example:

```text
dev  → <DEV-IP>.nip.io
prod → <PROD-IP>.nip.io
```

---

## 5. Image Versioning

Development deployments use the Git commit SHA as the image tag.

Production deployments use an explicit release version.

Example:

```text
dev:
atmos-backend:<git-sha>

prod:
atmos-backend:1.0.0
```

This provides traceability between the deployed image and the corresponding source revision.

---

## 6. Configuration

Environment-specific configuration is provided through Kustomize, ConfigMaps, and Secrets.

Examples of environment-specific values:

- API configuration;
- log level;
- resource settings;
- replica count;
- Ingress host;
- image version.

Real secrets are not stored in Git.
```