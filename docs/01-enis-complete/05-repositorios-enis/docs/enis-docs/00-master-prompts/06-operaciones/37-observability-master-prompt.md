# 37 - Observability Service Master Prompt

## Metadata

```yaml
prompt_id: "37"
prompt_name: "observability-master-prompt"
service_name: "observability-service"
version: "1.0.0"
category: "cloud-core"
dna_version: "3.0"
created: "2025-10-08"
status: "active"
priority: "P1"
sprint: "S22-P1"
```

---

## 🎯 Propósito del Servicio

El **Observability Service** es el servicio centralizado de observabilidad para ENIS v3.0, extraído del NOPS Kernel según el principio SLIM.

### Responsabilidades Core:

```yaml
responsabilidades:
  ingesta:
    - "Recibir métricas del NOPS Kernel vía mTLS"
    - "Recibir traces de OpenTelemetry"
    - "Recibir logs estructurados"
    - "Almacenar en series temporales"
    
  storage:
    - "VictoriaMetrics para métricas (long-term)"
    - "Jaeger para traces distribuidos"
    - "Elasticsearch para logs"
    - "PostgreSQL para metadata"
    
  visualizacion:
    - "Grafana dashboards multi-tenant"
    - "Jaeger UI para tracing"
    - "Kibana para log analysis"
    
  alerting:
    - "AlertManager para alertas"
    - "Webhooks a NOPS Kernel"
    - "Email/Slack notifications"
```

---

## 🏗️ Arquitectura del Servicio

### Stack Tecnológico:

```yaml
backend:
  framework: "FastAPI"
  runtime: "Python 3.11+"
  async: "asyncio + uvloop"
  workers: "Gunicorn + Uvicorn"
  
storage:
  timeseries: "VictoriaMetrics"
  tracing: "Jaeger"
  logging: "Elasticsearch"
  metadata: "PostgreSQL"
  cache: "Redis"
  
visualization:
  dashboards: "Grafana"
  tracing_ui: "Jaeger UI"
  logs_ui: "Kibana"
  
collection:
  agents: "Vector / Fluent Bit"
  protocol: "OpenTelemetry Protocol (OTLP)"
  
alerting:
  engine: "AlertManager"
  rules: "PromQL + LogQL"
```

---

## 📡 APIs Principales

### 1. Metrics Ingestion API

```yaml
POST /api/v1/metrics:
  descripcion: "Recibe métricas del NOPS Kernel"
  auth: "mTLS + JWT s2s"
  payload:
    tenant_id: string
    timestamp: ISO8601
    metrics: array
      - name: string
      - value: float
      - labels: object
  
  response:
    status: 202 (Accepted)
    body:
      message: "Metrics queued"
      metrics_received: int
  
  performance:
    throughput: "> 10K metrics/s"
    latency_p95: "< 50ms"
```

### 2. Traces Ingestion API

```yaml
POST /api/v1/traces:
  descripcion: "Recibe traces de OpenTelemetry"
  auth: "mTLS + JWT s2s"
  protocol: "OTLP (OpenTelemetry Protocol)"
  
  performance:
    throughput: "> 1K spans/s"
    latency_p95: "< 100ms"
```

### 3. Logs Ingestion API

```yaml
POST /api/v1/logs:
  descripcion: "Recibe logs estructurados"
  auth: "mTLS + JWT s2s"
  format: "JSON structured logs"
  
  performance:
    throughput: "> 5K logs/s"
    latency_p95: "< 30ms"
```

### 4. Query API

```yaml
GET /api/v1/query/metrics:
  descripcion: "Query métricas (Grafana datasource)"
  auth: "JWT + RBAC"
  query_language: "PromQL"
  
POST /api/v1/query/traces:
  descripcion: "Query traces"
  auth: "JWT + RBAC"
  
POST /api/v1/query/logs:
  descripcion: "Query logs"
  auth: "JWT + RBAC"
  query_language: "LogQL / Lucene"
```

---

## 🔐 Seguridad

```yaml
security:
  authentication:
    nops_kernel: "mTLS + JWT s2s"
    users: "JWT + RBAC"
    
  authorization:
    model: "RBAC por tenant"
    scopes:
      - "metrics:read"
      - "metrics:write"
      - "traces:read"
      - "logs:read"
      - "admin:manage"
    
  encryption:
    in_transit: "TLS 1.3"
    at_rest: "AES-256-GCM"
    
  multi_tenancy:
    isolation: "Tenant ID en todos los queries"
    namespace: "Grafana folders por tenant"
```

---

## 📊 Performance & Scalability

```yaml
performance:
  slos:
    availability: "> 99.9%"
    ingestion_latency_p95: "< 50ms"
    query_latency_p95: "< 200ms"
    
  throughput:
    metrics: "> 10K/s por instancia"
    traces: "> 1K spans/s"
    logs: "> 5K/s"
    
  storage:
    retention_metrics: "90 días (configurable)"
    retention_traces: "30 días"
    retention_logs: "30 días"
    
  escalamiento:
    horizontal: "Stateless API layer"
    vertical: "VictoriaMetrics clusters"
```

---

## 🚀 Deployment

```yaml
deployment:
  platform: "Kubernetes"
  replicas: "3 (HA)"
  resources:
    cpu: "2-4 cores por pod"
    memory: "4-8 GB por pod"
    storage: "1-5 TB (VictoriaMetrics)"
    
  dependencies:
    - "VictoriaMetrics cluster"
    - "Jaeger all-in-one / cluster"
    - "Elasticsearch cluster"
    - "Grafana"
    - "AlertManager"
    
  networking:
    ingress: "NGINX Ingress Controller"
    service_mesh: "Istio (opcional)"
```

---

## 🔗 Cross-References

```yaml
master_prompts_relacionados:
  - "02-architecture-master-prompt.md" (arquitectura general)
  - "07-nops-master-prompt.md" (NOPS Kernel SLIM - cliente)
  - "18-security-master-prompt.md" (seguridad mTLS)
  - "19-performance-master-prompt.md" (optimizaciones)
  - "22-monitoring-master-prompt.md" (self-monitoring)
  - "33-cloud-infrastructure-master-prompt.md" (deployment)
```

---

## 📋 Implementación

### Sprint S22-P1 (1 semana):

```yaml
tasks:
  - "Scaffold FastAPI base"
  - "Implementar API de ingesta de métricas"
  - "Configurar VictoriaMetrics"
  - "Configurar Grafana + dashboards base"
  - "Implementar mTLS + JWT validation"
  - "Tests de integración con NOPS Kernel"
  - "Deployment en K8s (staging)"
```

---

*Master Prompt creado: 2025-10-08*  
*Estado: Active*  
*Próxima revisión: Sprint S22-P1*

