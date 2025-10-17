# 📊 Scorecard Service - ENIS v3.0

## 📋 Metadata

```yaml
service_name: "scorecard-service"
service_type: "Platform Service"
category: "cloud-core"
priority: "P2 - MEDIA"
status: "📋 Planned - Sprint S22-P2"
stack: "Python 3.11+ / FastAPI"
dependencies: ["pandas", "numpy", "scikit-learn", "observability-service"]
dna_version: "3.0"
```

---

## 🎯 Propósito

Servicio de scoring y analytics extraído del NOPS Kernel (arquitectura SLIM).

Proporciona:
- **Pre-installation assessment** (infraestructura del cliente)
- **Scoring continuo** post-instalación
- **Analytics de rendimiento** con ML
- **Insights y recommendations** automáticas
- **Trend analysis** y optimizaciones

---

## 🏗️ Arquitectura

### Principio SLIM:
Este servicio **NO requiere client directo** en el NOPS Kernel.

```yaml
comunicacion:
  observability_service:
    protocolo: "Internal HTTP"
    accion: "Lee métricas agregadas"
    
  nops_kernel:
    via: "Webhooks (opcional)"
    trigger: "Scores críticos → notificación a NOPS"
    
  frontend:
    acceso: "Dashboard de scores"
    api: "REST API para queries"
```

---

## 📦 Stack Tecnológico

```yaml
backend:
  framework: "FastAPI"
  runtime: "Python 3.11+"
  async: "asyncio"
  
analytics:
  dataframes: "pandas + polars"
  numerical: "numpy"
  ml: "scikit-learn + LightGBM"
  
storage:
  database: "PostgreSQL + TimescaleDB"
  cache: "Redis"
  
security:
  authentication: "JWT (internal)"
  authorization: "RBAC"
```

---

## 📡 APIs Principales

### POST /api/v1/assessments
Pre-installation assessment

### GET /api/v1/scores/{tenant_id}
Scoring continuo

### GET /api/v1/insights/{tenant_id}
Analytics insights

---

## 🚀 Sprint de Implementación

**Sprint:** S22-P2  
**Duración:** 1 semana  
**Prioridad:** P2 (MEDIA)

---

*Servicio creado: 2025-10-08*  
*Estado: Planned - Sprint S22-P2*

