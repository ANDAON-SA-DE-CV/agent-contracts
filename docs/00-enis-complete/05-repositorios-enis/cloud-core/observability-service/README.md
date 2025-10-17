# 🔍 Observability Service - ENIS v3.0

## 📋 Metadata

```yaml
service_name: "observability-service"
service_type: "Platform Service"
category: "cloud-core"
priority: "P1 - ALTA"
status: "📋 Planned - Sprint S22-P1"
stack: "Python 3.11+ / FastAPI"
dependencies: ["Prometheus", "Grafana", "Jaeger", "ELK", "VictoriaMetrics"]
dna_version: "3.0"
```

---

## 🎯 Propósito

Servicio de observabilidad centralizado extraído del NOPS Kernel (arquitectura SLIM).

Proporciona:
- **Almacenamiento de métricas** (series temporales)
- **Dashboards** interactivos (Grafana)
- **Tracing distribuido** (Jaeger + OpenTelemetry)
- **Log aggregation** (ELK Stack)
- **Alerting avanzado** (AlertManager)

---

## 🏗️ Arquitectura

### Principio SLIM:
Este servicio es **EXTERNO** al NOPS Kernel. El kernel usa un **API client ligero** (`ObservabilityAPIClient`) para enviar métricas.

```yaml
comunicacion:
  nops_kernel:
    protocolo: "mTLS + JWT s2s"
    endpoint: "POST /api/v1/metrics"
    timeout: "5s (agresivo)"
    degraded_mode: "Kernel continúa sin observability avanzada"
    
  edge_agents:
    via: "NOPS Kernel (no conexión directa)"
    
  dashboards:
    acceso: "Grafana UI"
    datasource: "VictoriaMetrics / Prometheus"
```

---

## 📦 Stack Tecnológico

```yaml
backend:
  framework: "FastAPI"
  runtime: "Python 3.11+"
  async: "asyncio + uvloop"
  
storage:
  timeseries: "VictoriaMetrics (métricas)"
  database: "PostgreSQL (metadata)"
  cache: "Redis (hot data)"
  
monitoring:
  metrics: "Prometheus"
  dashboards: "Grafana"
  tracing: "Jaeger"
  logging: "ELK Stack (Elasticsearch + Logstash + Kibana)"
  collection: "Vector / Fluent Bit"
  
security:
  authentication: "mTLS + JWT"
  authorization: "RBAC por tenant"
  encryption: "TLS 1.3"
```

---

## 📡 APIs Principales

### POST /api/v1/metrics
Recibe métricas del NOPS Kernel

### POST /api/v1/traces
Recibe traces de OpenTelemetry

### POST /api/v1/logs
Recibe logs estructurados

### GET /api/v1/query/metrics
Query métricas (Grafana datasource)

---

## 🚀 Sprint de Implementación

**Sprint:** S22-P1  
**Duración:** 1 semana  
**Prioridad:** P1 (ALTA)

**Dependencias:**
- NOPS Kernel con ObservabilityAPIClient (✅ ya implementado)
- cloud-infrastructure con Helm charts

---

## 📚 Master Prompts

- `02-architecture-master-prompt.md` - Arquitectura del servicio
- `18-security-master-prompt.md` - Seguridad y mTLS
- `19-performance-master-prompt.md` - Optimizaciones
- `22-monitoring-master-prompt.md` - Self-monitoring

---

*Servicio creado: 2025-10-08*  
*Estado: Planned - Sprint S22-P1*

