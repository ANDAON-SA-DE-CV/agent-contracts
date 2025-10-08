# 38 - Scorecard Service Master Prompt

## Metadata

```yaml
prompt_id: "38"
prompt_name: "scorecard-master-prompt"
service_name: "scorecard-service"
version: "1.0.0"
category: "cloud-core"
dna_version: "3.0"
created: "2025-10-08"
status: "active"
priority: "P2"
sprint: "S22-P2"
```

---

## 🎯 Propósito del Servicio

El **Scorecard Service** proporciona scoring, analytics y recommendations para la plataforma ENIS.

### Responsabilidades Core:

```yaml
responsabilidades:
  pre_installation:
    - "Assessment de infraestructura del cliente"
    - "Scoring de readiness (compute, network, storage, security)"
    - "Recommendations pre-deployment"
    - "Estimación de performance esperado"
    
  post_installation:
    - "Scoring continuo de rendimiento"
    - "Analytics de uso y eficiencia"
    - "Trend analysis (improving/stable/declining)"
    - "Optimization opportunities detection"
    - "Insights generation con ML"
    
  reporting:
    - "Performance reports por tenant"
    - "Comparative analytics (peer benchmarking)"
    - "Cost efficiency scoring"
```

---

## 🏗️ Arquitectura del Servicio

### Stack Tecnológico:

```yaml
backend:
  framework: "FastAPI"
  runtime: "Python 3.11+"
  async: "asyncio"
  
analytics:
  dataframes: "pandas + polars"
  numerical: "numpy"
  ml: "scikit-learn + LightGBM"
  statistical: "scipy + statsmodels"
  
storage:
  database: "PostgreSQL + TimescaleDB"
  cache: "Redis"
  
data_sources:
  primary: "observability-service (métricas agregadas)"
  secondary: "billing-service (usage data)"
```

---

## 📡 APIs Principales

### 1. Pre-Installation Assessment

```yaml
POST /api/v1/assessments:
  auth: "JWT + RBAC"
  payload:
    tenant_id: string
    infrastructure:
      compute: object
      network: object
      storage: object
      security: object
  
  response:
    overall_score: float (0-100)
    scores:
      compute_readiness: float
      network_readiness: float
      storage_readiness: float
      security_readiness: float
    ready_for_deployment: boolean
    recommendations: array[string]
```

### 2. Continuous Scoring

```yaml
GET /api/v1/scores/{tenant_id}:
  auth: "JWT + RBAC"
  parameters:
    period: "7d|30d|90d"
    
  response:
    scores:
      availability: float
      latency: float
      throughput: float
      error_rate: float
      cost_efficiency: float
    trend: "improving|stable|declining"
    insights: array[string]
    optimization_opportunities: array
```

---

## 🤖 ML Models

```yaml
ml_models:
  scoring_models:
    - "LightGBM para readiness prediction"
    - "Random Forest para optimization recommendations"
    
  anomaly_detection:
    - "Isolation Forest para detección de anomalías"
    - "ARIMA para trend forecasting"
    
  clustering:
    - "K-means para peer grouping"
    - "DBSCAN para pattern detection"
```

---

## 🔗 Cross-References

```yaml
master_prompts_relacionados:
  - "02-architecture-master-prompt.md"
  - "18-security-master-prompt.md"
  - "19-performance-master-prompt.md"
  - "37-observability-master-prompt.md" (data source)
  - "39-billing-master-prompt.md" (usage data)
```

---

*Master Prompt creado: 2025-10-08*  
*Estado: Active*

