# Guía de Uso: Plantilla Universal ENIS v2.4

**Versión:** 2.4 Enterprise Universal  
**Fecha:** 2025-10-16  
**Compatibilidad:** 24 repositorios ENIS v3.0

---

## 🎯 Objetivo

Esta guía explica cómo usar la **Plantilla Universal v2.4** en cualquiera de los 24 repositorios ENIS, adaptando los comandos y estructura según el stack tecnológico.

---

## 📦 Los 24 Repositorios ENIS

### 1. Cloud-Core (4 repos) - Backend Python FastAPI

| Repo | Stack | Puerto | Descripción |
|------|-------|--------|-------------|
| `cloud-core/inference-service` | Python + FastAPI | 8000 | Motor de inferencia LLM |
| `cloud-core/observability-service` | Python + FastAPI | 8001 | OTel + SIEM + métricas |
| `cloud-core/compliance-service` | Python + FastAPI | 8002 | Audit trails inmutables |
| `cloud-core/billing-service` | Python + FastAPI | 8003 | Budget guard + pricing |

**Comandos típicos:**
```bash
# Install
pip install -e .

# Test
pytest tests/ -v --cov=src --cov-fail-under=85

# Run
uvicorn src.main:app --reload --port 8000

# Lint
ruff check src/ tests/
```

---

### 2. Macro-Modules (4 repos) - Backend Python FastAPI

| Repo | Stack | Puerto | Descripción |
|------|-------|--------|-------------|
| `macro-modules/asm-service` | Python + FastAPI | 9000 | Agent State Manager |
| `macro-modules/cgn-service` | Python + FastAPI | 9001 | Conversational Graph Navigator |
| `macro-modules/awe-service` | Python + FastAPI | 9002 | Agent Workflow Engine |
| `macro-modules/shif-service` | Python + FastAPI | 9003 | Scorecard & Hierarchy Intelligence |

**Comandos típicos:**
```bash
# Install
pip install -e .

# Test
pytest tests/ -v --cov=src

# Run
uvicorn src.main:app --reload --port 9000
```

---

### 3. Shared (3 repos) - Mixto

| Repo | Stack | Descripción |
|------|-------|-------------|
| `shared/agent-contracts` | YAML + JSON Schema | Contratos API entre servicios |
| `shared/agent-sdks` | Python + TypeScript + Go | SDKs cliente multi-lenguaje |
| `shared/nops-sdk` | Python + TypeScript | SDK para NOPS Kernel |

**Comandos típicos:**

#### agent-contracts (YAML)
```bash
# Validate
python scripts/validate_contracts.py

# Test
pytest tests/ -v

# Publish
python scripts/publish_contracts.py
```

#### agent-sdks (Multi-lenguaje)
```bash
# Python SDK
cd python-sdk/
pip install -e .
pytest tests/

# TypeScript SDK
cd typescript-sdk/
npm install
npm test

# Go SDK
cd go-sdk/
go test ./...
```

---

### 4. NOPS (2 repos) - Python + Next.js

| Repo | Stack | Puerto | Descripción |
|------|-------|--------|-------------|
| `nops/nops-kernel` | Python + FastAPI | 7000 | Orquestador central NOPS |
| `nops/nops-dashboard` | Next.js + TypeScript | 3001 | Dashboard de monitoreo NOPS |

**Comandos típicos:**

#### nops-kernel (Python)
```bash
pip install -e .
pytest tests/ -v
uvicorn src.main:app --reload --port 7000
```

#### nops-dashboard (Next.js)
```bash
npm install
npm test
npm run dev -- --port 3001
```

---

### 5. Edge (2 repos) - Go + Python

| Repo | Stack | Descripción |
|------|-------|-------------|
| `edge/edge-agents` | Go + Kubernetes | Agentes edge (5 tipos) |
| `edge/edge-lite` | Python + Docker | Edge lite para air-gapped |

**Comandos típicos:**

#### edge-agents (Go)
```bash
go mod download
go test ./...
go build -o bin/edge-agent cmd/main.go
```

#### edge-lite (Python)
```bash
pip install -e .
pytest tests/ -v
python -m src.main
```

---

### 6. Interfaces (2 repos) - Python FastAPI

| Repo | Stack | Puerto | Descripción |
|------|-------|--------|-------------|
| `interfaces/voice-interface-service` | Python + FastAPI | 6000 | STT → Inference → TTS |
| `interfaces/xr-interface-service` | Python + FastAPI | 6001 | OpenXR → Inference → Render |

**Comandos típicos:**
```bash
pip install -e .
pytest tests/ -v
uvicorn src.main:app --reload --port 6000
```

---

### 7. Frontend (3 repos) - Next.js

| Repo | Stack | Puerto | Descripción |
|------|-------|--------|-------------|
| `frontend/enis-dashboard` | Next.js + TypeScript | 3000 | Dashboard principal ENIS |
| `frontend/agent-portal` | Next.js + TypeScript | 3002 | Portal de agentes |
| `frontend/dev-portal` | Next.js + TypeScript | 3003 | Portal de desarrolladores |

**Comandos típicos:**
```bash
npm install
npm test
npm run dev -- --port 3000
npm run build
npm run lint
```

---

### 8. Infrastructure (2 repos) - IaC

| Repo | Stack | Descripción |
|------|-------|-------------|
| `infrastructure/k8s-manifests` | Kubernetes + Helm | Manifests K8s + Helm charts |
| `infrastructure/terraform-modules` | Terraform + HCL | Módulos Terraform multi-cloud |

**Comandos típicos:**

#### k8s-manifests (Kubernetes)
```bash
# Lint
helm lint charts/[service]/

# Dry-run
helm install [service] charts/[service]/ --dry-run --debug

# Validate
kubeval charts/[service]/templates/*.yaml

# Apply
helm upgrade --install [service] charts/[service]/
```

#### terraform-modules (Terraform)
```bash
terraform init
terraform validate
terraform plan
terraform apply -auto-approve
tflint
```

---

### 9. Docs (2 repos) - Markdown + Specs

| Repo | Stack | Descripción |
|------|-------|-------------|
| `docs/enis-docs` | Markdown + Docusaurus | Documentación técnica |
| `docs/enis-specs` | OpenAPI + AsyncAPI | Especificaciones API |

**Comandos típicos:**

#### enis-docs (Docusaurus)
```bash
npm install
npm start
npm run build
```

#### enis-specs (OpenAPI)
```bash
# Validate
openapi-generator validate -i specs/openapi.yaml

# Generate
openapi-generator generate -i specs/openapi.yaml -g python -o clients/python/
```

---

## 🔧 Cómo Usar la Plantilla Universal

### Paso 1: Identificar el Repositorio

Determina en qué repositorio vas a trabajar:

```bash
# Detectar stack automáticamente
cd /path/to/[repo]
scripts/detect_stack.sh

# Output ejemplo:
# Repository: cloud-core/inference-service
# Stack: python
# Framework: fastapi
# Port: 8000
```

### Paso 2: Copiar y Adaptar la Plantilla

```bash
# Copiar plantilla
cp docs/03-Template/SPRINT_TEMPLATE_CLAUDE_CLI.md docs/01-sprint/S[N]/S[N]_[name].md

# Reemplazar placeholders
# [repository-name] → inference-service
# [Stack] → Python + FastAPI
# [N] → 8
# etc.
```

### Paso 3: Adaptar Comandos según Stack

La plantilla incluye auto-detección. Usa la tabla de comandos:

| Stack | Install | Test | Build | Lint | Run |
|-------|---------|------|-------|------|-----|
| **Python** | `pip install -e .` | `pytest` | `python setup.py build` | `ruff check` | `uvicorn src.main:app` |
| **Node.js** | `npm install` | `npm test` | `npm run build` | `npm run lint` | `npm start` |
| **Next.js** | `npm install` | `npm test` | `npm run build` | `npm run lint` | `npm run dev` |
| **Go** | `go mod download` | `go test ./...` | `go build` | `golangci-lint run` | `go run main.go` |
| **Terraform** | `terraform init` | `terraform validate` | `terraform plan` | `tflint` | `terraform apply` |
| **Kubernetes** | `helm dependency update` | `helm lint` | `helm package` | `kubeval` | `helm install` |

### Paso 4: Adaptar SLOs según Tipo de Sprint

#### Backend (Python/Go)
```json
"slos": {
  "latency_p95_ms": 200,
  "throughput_rps": 1000,
  "error_rate_percent": 0.5,
  "availability_percent": 99.9
}
```

#### Frontend (Next.js)
```json
"slos": {
  "fcp_ms": 1500,       // First Contentful Paint
  "lcp_ms": 2500,       // Largest Contentful Paint
  "tti_ms": 3500,       // Time to Interactive
  "lighthouse_score": 90
}
```

#### Infrastructure (Terraform/K8s)
```json
"slos": {
  "apply_time_minutes": 10,
  "validation_pass_rate": 100,
  "drift_detection": "enabled",
  "compliance_score": 100
}
```

---

## 📊 Dashboards Grafana por Tipo de Repo

### ¿Qué repos necesitan Dashboard Grafana?

| Categoría | Dashboard | Razón |
|-----------|-----------|-------|
| **Cloud-Core (4)** | ✅ SÍ | Métricas runtime críticas (latencia, throughput, errors) |
| **Macro-Modules (4)** | ✅ SÍ | Orquestación + composición + timeouts |
| **Shared/SDKs (3)** | ⚠️ OPCIONAL | Solo si hay métricas de uso/distribución |
| **NOPS (2)** | ✅ SÍ | Kernel = orchestrator, Dashboard = monitoreo |
| **Edge (2)** | ✅ SÍ | Métricas por tier de agente |
| **Interfaces (2)** | ✅ SÍ | Latencia multimodal (voice/XR) |
| **Frontend (3)** | ⚠️ OPCIONAL | Web Vitals (LCP, FCP, TTI) - puede ser RUM en lugar de Grafana |
| **Infrastructure (2)** | ❌ NO | No hay métricas runtime (solo validación) |
| **Docs (2)** | ❌ NO | Documentación estática |

---

## 🎯 Ejemplos Completos por Repositorio

### Ejemplo 1: inference-service (Cloud-Core)

```markdown
# S8 — Seguridad s2s (mTLS + JWT) ⏸️ **IN_PROGRESS**

> **📦 Información del Repositorio:**
> - **Repo:** `cloud-core/inference-service`
> - **Stack:** Python 3.11 + FastAPI + PostgreSQL + Redis
> - **Branch:** `feature/s8-security-s2s`
> - **Arquitectura:** ENIS v3.0 DNA v3.0 Compliant

**AI Agent Configuration:**
```json
{
  "sprint": {
    "number": "8",
    "name": "Seguridad s2s (mTLS + JWT)",
    "repo": "cloud-core/inference-service",
    "repo_category": "cloud-core",
    "stack": "python",
    "framework": "fastapi"
  },
  "slos": {
    "latency_p95_ms": 50,
    "throughput_rps": 1000,
    "error_rate_percent": 0.1
  }
}
```

**Comandos:**
```bash
# Install
pip install -e .

# Test
pytest tests/ -v --cov=src --cov-fail-under=85

# Run
uvicorn src.main:app --reload --port 8000
```

**Dashboard Grafana:** ✅ SÍ (métricas mTLS handshake, JWT validation)
```

---

### Ejemplo 2: enis-dashboard (Frontend)

```markdown
# S12 — Dashboard Performance Optimization ⏸️ **IN_PROGRESS**

> **📦 Información del Repositorio:**
> - **Repo:** `frontend/enis-dashboard`
> - **Stack:** Next.js 14 + TypeScript + Tailwind CSS
> - **Branch:** `feature/s12-dashboard-perf`
> - **Arquitectura:** ENIS v3.0 DNA v3.0 Compliant

**AI Agent Configuration:**
```json
{
  "sprint": {
    "number": "12",
    "name": "Dashboard Performance Optimization",
    "repo": "frontend/enis-dashboard",
    "repo_category": "frontend",
    "stack": "nextjs",
    "framework": "nextjs"
  },
  "slos": {
    "fcp_ms": 1500,
    "lcp_ms": 2500,
    "tti_ms": 3500,
    "lighthouse_score": 90
  }
}
```

**Comandos:**
```bash
# Install
npm install

# Test
npm test

# Run
npm run dev -- --port 3000

# Build
npm run build
```

**Dashboard Grafana:** ⚠️ OPCIONAL (Web Vitals - considerar RUM en lugar de Grafana)
```

---

### Ejemplo 3: edge-agents (Edge)

```markdown
# S10 — Edge Agent Multi-Tier ⏸️ **IN_PROGRESS**

> **📦 Información del Repositorio:**
> - **Repo:** `edge/edge-agents`
> - **Stack:** Go 1.21 + Kubernetes + Docker
> - **Branch:** `feature/s10-edge-multi-tier`
> - **Arquitectura:** ENIS v3.0 DNA v3.0 Compliant

**AI Agent Configuration:**
```json
{
  "sprint": {
    "number": "10",
    "name": "Edge Agent Multi-Tier",
    "repo": "edge/edge-agents",
    "repo_category": "edge",
    "stack": "go",
    "framework": "gin"
  },
  "slos": {
    "latency_p95_ms": 100,
    "throughput_rps": 500,
    "memory_mb": 256
  }
}
```

**Comandos:**
```bash
# Install
go mod download

# Test
go test ./... -v -cover

# Build
go build -o bin/edge-agent cmd/main.go

# Run
./bin/edge-agent
```

**Dashboard Grafana:** ✅ SÍ (métricas por tier: Zero/Shared/Lite/Enterprise/Air-Gapped)
```

---

### Ejemplo 4: k8s-manifests (Infrastructure)

```markdown
# S15 — Helm Chart Multi-Region ⏸️ **IN_PROGRESS**

> **📦 Información del Repositorio:**
> - **Repo:** `infrastructure/k8s-manifests`
> - **Stack:** Kubernetes 1.28 + Helm 3.12
> - **Branch:** `feature/s15-helm-multi-region`
> - **Arquitectura:** ENIS v3.0 DNA v3.0 Compliant

**AI Agent Configuration:**
```json
{
  "sprint": {
    "number": "15",
    "name": "Helm Chart Multi-Region",
    "repo": "infrastructure/k8s-manifests",
    "repo_category": "infrastructure",
    "stack": "kubernetes",
    "framework": "helm"
  },
  "slos": {
    "apply_time_minutes": 10,
    "validation_pass_rate": 100,
    "rollout_time_minutes": 5
  }
}
```

**Comandos:**
```bash
# Lint
helm lint charts/inference/

# Validate
kubeval charts/inference/templates/*.yaml

# Dry-run
helm install inference charts/inference/ --dry-run --debug

# Apply
helm upgrade --install inference charts/inference/ -n enis-system
```

**Dashboard Grafana:** ❌ NO (no hay métricas runtime, solo validación)
```

---

## ✅ Checklist de Adaptación

Antes de usar la plantilla en un nuevo repo, verifica:

- [ ] ¿He identificado el stack tecnológico? (Python/Node.js/Go/etc.)
- [ ] ¿He adaptado los comandos de install/test/build/run?
- [ ] ¿He ajustado los SLOs según el tipo de servicio?
- [ ] ¿He determinado si necesita Dashboard Grafana?
- [ ] ¿He actualizado el repo_category en AI Agent Configuration?
- [ ] ¿He verificado la estructura de directorios del repo?
- [ ] ¿He revisado si hay dependencias cross-repo?

---

## 📚 Referencias

- **Plantilla Universal:** `docs/03-Template/SPRINT_TEMPLATE_CLAUDE_CLI.md`
- **Guía de Dashboards:** `docs/03-Template/GRAFANA_DASHBOARDS_GUIDE.md`
- **Resumen v2.4:** `docs/03-Template/TEMPLATE_v2.4_UPDATE_SUMMARY.md`
- **Arquitectura ENIS:** `docs/00-enis-complete/03-reports/ENIS_COMPLETE_ARCHITECTURE_REPORT.md`

---

**Última actualización:** 2025-10-16  
**Versión:** 2.4 Enterprise Universal  
**Mantenedor:** Platform Engineering Team

