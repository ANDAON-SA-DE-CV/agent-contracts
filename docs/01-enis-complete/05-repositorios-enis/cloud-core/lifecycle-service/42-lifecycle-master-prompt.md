# 42 - Lifecycle Service Master Prompt

## Metadata

```yaml
prompt_id: "42"
prompt_name: "lifecycle-master-prompt"
service_name: "lifecycle-service"
version: "1.0.0"
category: "cloud-core"
dna_version: "3.0"
created: "2025-10-08"
status: "active"
priority: "P3"
sprint: "S23-P2"
```

---

## 🎯 Propósito del Servicio

El **Lifecycle Service** gestiona el ciclo de vida completo de Edge Agents (deployment, updates, rollbacks).

### Responsabilidades Core:

```yaml
responsabilidades:
  deployment:
    - "Rolling updates con zero downtime"
    - "Blue-Green deployments"
    - "Canary releases con automatic rollback"
    - "Recreate (emergency mode)"
    
  version_management:
    - "Version registry de agentes"
    - "Compatibility matrix"
    - "Rollback automático on failure"
    
  health_monitoring:
    - "Continuous health checks"
    - "Readiness probes"
    - "Liveness probes"
    - "Auto-healing"
```

---

## 🏗️ Arquitectura del Servicio

### Stack Tecnológico:

```yaml
backend:
  framework: "Kubernetes Operator (Go)"
  runtime: "Go 1.21+"
  pattern: "Controller pattern + Reconciliation loop"
  
orchestration:
  platform: "Kubernetes"
  config: "etcd"
  packaging: "Helm charts"
  
deployment_strategies:
  - "Rolling Update (default)"
  - "Blue-Green"
  - "Canary (with Flagger)"
  - "Recreate"
```

---

## 📡 APIs Principales

```yaml
POST /api/v1/deployments:
  auth: "mTLS (CI/CD pipeline)"
  payload:
    agent_spec: object
    strategy: "rolling|bluegreen|canary"
    
POST /api/v1/deployments/{id}/rollback:
  auth: "mTLS"
  
  response:
    rollback_status: "completed|in_progress"
```

---

*Master Prompt creado: 2025-10-08*

