# 🗺️ Mapeo Repositorios ↔ Arquitectura ENIS v3.0

## 📋 Metadata

```yaml
doc_version: "3.0"
doc_type: "Mapping Documentation"
doc_author: "@andaon"
doc_date: "2025-10-09"
doc_updated: "2025-01-09 - Agregados 3 servicios (Voice + XR + DGE)"
dna_version: "3.0"
compliance: "DNA_v3_compliant"
total_repos: 24
categories: ["shared", "edge", "cloud-core", "cloud-ops", "platform"]
major_update: "cloud-core expandido de 12 a 15 repos (2 interfaces avanzadas + 1 governance DGE)"
```

---

## 🎯 Propósito

Este documento mapea la **organización física de repositorios** con la **arquitectura lógica de componentes** de ENIS v3.0, facilitando:

- Entendimiento de la estructura del proyecto
- Navegación entre repositorios
- Planificación de sprints multi-repo
- Coordinación de equipos de desarrollo
- Gestión de dependencias

---

## 📊 Vista General: 24 Repositorios

```yaml
organizacion_repositorios:
  total: 24
  
  categorias:
    shared: 3       # Base común para todos
    edge: 3         # Componentes del cliente
    cloud_core: 15  # Servicios principales (5 macro-módulos + 7 módulos NOPS + 2 interfaces avanzadas + 1 governance)
    cloud_ops: 1    # Infraestructura y operaciones
    platform: 2     # Marketplace y frontend
    
  desglose_cloud_core:
    macro_modulos: 5      # ASM, CGN, AWE, SHIF, Inference
    nops_modules: 7       # Observability, Scorecard, Billing, Sandbox, Governance, Lifecycle, Compliance
    interfaces_avanzadas: 2  # Voice Interface, XR Interface
    governance: 1         # Data Governance Engine (DGE)
```

---

## 📦 SHARED (3 repos) - Base Común

### 1. **agent-contracts**

```yaml
repositorio: "shared/agent-contracts"
proposito: "Definición de contratos, schemas y protocolos"
tecnologias: ["Protocol Buffers", "JSON Schema", "OpenAPI 3.0"]
dependencias: []
dependientes: ["TODOS los repositorios"]

componente_logico: "enis-contracts (Schemas / SDK)"
ubicacion_arquitectura: "Capa de contratos entre edge y cloud"

archivos_clave:
  - "AGENT_CONTRACTS_MASTER_PROMPT.md"
  - "02-architecture-master-prompt.md"
  - "18-security-master-prompt.md"
  - "20-integration-master-prompt.md"

responsabilidades:
  - "Definir schemas de Agent Registry"
  - "Especificar protocolos de comunicación"
  - "Documentar APIs entre componentes"
  - "Versionado de contratos"
```

### 2. **agent-sdks**

```yaml
repositorio: "shared/agent-sdks"
proposito: "SDKs multi-lenguaje para desarrollo de agents"
tecnologias: ["Python", "Go", "TypeScript", "Java", "C#"]
dependencias: ["agent-contracts"]
dependientes: ["edge-agents", "enis-frontend", "agent-marketplace"]

componente_logico: "SDK Libraries"
ubicacion_arquitectura: "Developer tooling layer"

archivos_clave:
  - "AGENT_SDKS_MASTER_PROMPT.md"
  - "04-implementation-master-prompt.md"
  - "09-dev-generation-master-prompt.md"
  - "20-integration-master-prompt.md"
  - "21-testing-master-prompt.md"

responsabilidades:
  - "SDK Python para edge agents"
  - "SDK Go para performance crítico"
  - "SDK TypeScript para web/frontend"
  - "Ejemplos de código y templates"
  - "Testing frameworks"
```

### 3. **enis-infrastructure**

```yaml
repositorio: "shared/enis-infrastructure"
proposito: "Infraestructura como código compartida"
tecnologias: ["Terraform", "Helm", "Ansible", "Kubernetes"]
dependencias: []
dependientes: ["cloud-infrastructure", "edge-infrastructure"]

componente_logico: "IaC Base Layer"
ubicacion_arquitectura: "Infrastructure foundation"

archivos_clave:
  - "ENIS_INFRASTRUCTURE_MASTER_PROMPT.md"
  - "02-architecture-master-prompt.md"
  - "18-security-master-prompt.md"
  - "19-performance-master-prompt.md"
  - "22-monitoring-master-prompt.md"
  - "24-disaster-recovery-master-prompt.md"

responsabilidades:
  - "Terraform modules compartidos"
  - "Helm charts base"
  - "Security baselines"
  - "Networking templates"
  - "Monitoring stack base"
```

---

## ⚡ EDGE (3 repos) - Componentes del Cliente

### 4. **nops-kernel**

```yaml
repositorio: "edge/nops-kernel"
proposito: "Network Operating Platform System - Núcleo del edge"
tecnologias: ["Python 3.11+", "FastAPI", "Redis", "PostgreSQL"]
dependencias: ["agent-contracts", "agent-sdks"]
dependientes: ["edge-agents"]

componente_logico: "NOPS Kernel (Control Plane)"
ubicacion_arquitectura: "Edge control plane - Centro de orquestación"

archivos_clave:
  - "ROADMAP_SPRINTS_NOPS_KERNEL.md" ⭐
  - "07-nops-master-prompt.md" ⭐
  - "11-nops-complete-master-prompt.md" ⭐
  - "02-architecture-master-prompt.md"
  - "06-orchestrator-master-prompt.md"
  - "10-edge-master-prompt.md"
  - "18-security-master-prompt.md"
  - "19-performance-master-prompt.md"
  - "22-monitoring-master-prompt.md"

sprints_asociados: "S1-S21 (21 sprints totales)"

responsabilidades:
  - "Agent runtime y lifecycle"
  - "Event bus (Redis Streams)"
  - "Security policies enforcement"
  - "Intelligent routing"
  - "State management"
  - "Observability module"
  - "Federation capabilities"

master_prompts_criticos:
  primario: "07-nops-master-prompt.md"
  arquitectura: "02-architecture-master-prompt.md"
  edge_integration: "10-edge-master-prompt.md"
  orquestacion: "06-orchestrator-master-prompt.md"
  seguridad: "18-security-master-prompt.md"
  performance: "19-performance-master-prompt.md"
  monitoreo: "22-monitoring-master-prompt.md"
```

### 5. **edge-agents**

```yaml
repositorio: "edge/edge-agents"
proposito: "Implementación de los 5 tipos de Edge Agents"
tecnologias: ["Python", "Go", "Docker", "Kubernetes"]
dependencias: ["nops-kernel", "agent-contracts", "agent-sdks"]
dependientes: []

componentes_logicos:
  - "🟤 Zero Agent - Webhooks"
  - "🟡 Shared Edge - Multi-tenant"
  - "🟢 Edge Lite - Docker"
  - "🔵 Enterprise - Kubernetes"
  - "🔴 Air-Gapped - Zero Egress"

ubicacion_arquitectura: "Edge execution layer"

archivos_clave:
  - "10-edge-master-prompt.md" ⭐
  - "AGENT_CONTRACTS_MASTER_PROMPT.md"
  - "AGENT_SDKS_MASTER_PROMPT.md"
  - "EDGE_INFRASTRUCTURE_MASTER_PROMPT.md"
  - "04-implementation-master-prompt.md"
  - "18-security-master-prompt.md"
  - "19-performance-master-prompt.md"
  - "21-testing-master-prompt.md"

responsabilidades:
  - "Implementar 5 tipos de agents"
  - "SDK integration con NOPS"
  - "Local data processing"
  - "Offline capabilities"
  - "Edge-to-cloud sync"

tiers_pricing:
  zero_agent: "$99-199/mes"
  shared_edge: "$199-299/mes"
  edge_lite: "$500-2K/mes"
  enterprise: "$5-25K/mes"
  air_gapped: "$25-100K/mes"
```

### 6. **edge-infrastructure**

```yaml
repositorio: "edge/edge-infrastructure"
proposito: "Infraestructura para despliegue de edge"
tecnologias: ["K3s", "Docker", "Ansible", "Terraform"]
dependencias: ["enis-infrastructure"]
dependientes: ["nops-kernel", "edge-agents"]

componente_logico: "Edge Infrastructure Layer"
ubicacion_arquitectura: "Edge deployment infrastructure"

archivos_clave:
  - "EDGE_INFRASTRUCTURE_MASTER_PROMPT.md" ⭐
  - "02-architecture-master-prompt.md"
  - "10-edge-master-prompt.md"
  - "18-security-master-prompt.md"
  - "19-performance-master-prompt.md"
  - "22-monitoring-master-prompt.md"
  - "24-disaster-recovery-master-prompt.md"

responsabilidades:
  - "K3s deployment para edge lite/enterprise"
  - "Docker configurations"
  - "Edge networking setup"
  - "Local storage management"
  - "Edge monitoring stack"
```

---

## ☁️ CLOUD-CORE (14 repos) - Servicios Principales

### 📋 Subdivisión:
- **5 Macro-Módulos:** ASM, CGN, AWE, SHIF, Inference
- **7 Módulos NOPS:** Observability, Scorecard, Billing, Sandbox, Resource Governance, Lifecycle, Compliance
- **2 Interfaces Avanzadas:** Voice Interface, XR Interface

---

### 🎯 MACRO-MÓDULOS (5 repos)

### 7. **asm-service**

```yaml
repositorio: "cloud-core/asm-service"
proposito: "Adaptive Schema Management - Gestión de estado adaptativo"
tecnologias: ["Python 3.11+", "FastAPI", "PostgreSQL"]
dependencias: ["agent-contracts"]
dependientes: ["inference-service"]

componente_logico: "ASM - Adaptive State Manager"
ubicacion_arquitectura: "Cloud macro-módulo"

archivos_clave:
  - "13-asm-master-prompt.md" ⭐
  - "02-architecture-master-prompt.md"
  - "18-security-master-prompt.md"
  - "19-performance-master-prompt.md"

responsabilidades:
  - "Schema evolution management"
  - "State synchronization"
  - "Configuration management"
  - "Versioned state storage"
```

### 8. **cgn-service**

```yaml
repositorio: "cloud-core/cgn-service"
proposito: "Causal Graph Networks - Análisis causal"
tecnologias: ["Python 3.11+", "FastAPI", "Neo4j/NetworkX"]
dependencias: ["agent-contracts"]
dependientes: ["inference-service"]

componente_logico: "CGN - Causal Graph Network"
ubicacion_arquitectura: "Cloud macro-módulo"

archivos_clave:
  - "14-cgn-master-prompt.md" ⭐
  - "02-architecture-master-prompt.md"
  - "18-security-master-prompt.md"
  - "19-performance-master-prompt.md"

responsabilidades:
  - "Causal inference engine"
  - "Graph processing"
  - "Relationship discovery"
  - "Predictive analytics"
```

### 9. **awe-service**

```yaml
repositorio: "cloud-core/awe-service"
proposito: "Adaptive Workflow Evolution - Orquestación de workflows"
tecnologias: ["Python 3.11+", "FastAPI", "Temporal/Airflow"]
dependencias: ["agent-contracts", "asm-service"]
dependientes: ["inference-service"]

componente_logico: "AWE - Workflow Evolution"
ubicacion_arquitectura: "Cloud macro-módulo"

archivos_clave:
  - "15-awe-master-prompt.md" ⭐
  - "02-architecture-master-prompt.md"
  - "18-security-master-prompt.md"
  - "19-performance-master-prompt.md"

responsabilidades:
  - "Workflow orchestration"
  - "Adaptive evolution algorithms"
  - "Process optimization"
  - "Multi-agent coordination"
```

### 10. **shif-service**

```yaml
repositorio: "cloud-core/shif-service"
proposito: "Secure Hybrid Integration Framework - Integración segura"
tecnologias: ["Python 3.11+", "FastAPI", "Apache Camel"]
dependencias: ["agent-contracts"]
dependientes: ["inference-service"]

componente_logico: "SHIF - Integration Fabric"
ubicacion_arquitectura: "Cloud macro-módulo"

archivos_clave:
  - "16-shif-master-prompt.md" ⭐
  - "02-architecture-master-prompt.md"
  - "18-security-master-prompt.md"
  - "19-performance-master-prompt.md"

responsabilidades:
  - "Protocol adapters"
  - "Data transformation"
  - "Integration patterns"
  - "Security enforcement"
```

### 11. **inference-service**

```yaml
repositorio: "cloud-core/inference-service"
proposito: "LLM Router y servicio de inferencia"
tecnologias: ["Python 3.11+", "FastAPI", "LangChain", "LiteLLM"]
dependencias: ["agent-contracts", "asm-service", "cgn-service", "awe-service", "shif-service"]
dependientes: []

componente_logico: "🧠 Inference Service (Cloud Brain)"
ubicacion_arquitectura: "Cloud intelligence layer"

archivos_clave:
  - "ROADMAP_INFERENCE_SERVICE.md" ⭐
  - "12-inference-master-prompt.md" ⭐
  - "AGENT_CONTRACTS_MASTER_PROMPT.md"
  - "02-architecture-master-prompt.md"
  - "18-security-master-prompt.md"
  - "19-performance-master-prompt.md"
  - "22-monitoring-master-prompt.md"

responsabilidades:
  - "LLM routing y balanceo"
  - "Model management"
  - "Inference optimization"
  - "Integration con macro-módulos"
  - "Voice/XR interfaces (S16-S17)"
```

---

### 🟣 MÓDULOS NOPS (7 repos) - Extraídos del NOPS Kernel

Estos servicios fueron **extraídos del NOPS Kernel** según el **Principio SLIM** para mantener el kernel ligero (< 100MB RAM).

### 12. **observability-service**

```yaml
repositorio: "cloud-core/observability-service"
proposito: "Full-stack observability (metrics, logs, traces)"
tecnologias: ["Prometheus", "Grafana", "Jaeger", "ELK", "Vector"]
dependencias: ["enis-infrastructure"]
dependientes: ["TODOS los servicios"]

componente_logico: "Observability Module"
ubicacion_arquitectura: "Monitoring & Observability Layer"

archivos_clave:
  - "37-observability-master-prompt.md" ⭐ (~1,500 líneas)
  - "22-monitoring-master-prompt.md"
  - "02-architecture-master-prompt.md"
  - "18-security-master-prompt.md"
  - "19-performance-master-prompt.md"

responsabilidades:
  - "Metrics collection (Prometheus)"
  - "Distributed tracing (Jaeger + OpenTelemetry)"
  - "Log aggregation (ELK + Vector)"
  - "Dashboards (Grafana)"
  - "Alerting (Alertmanager + PagerDuty)"

nops_kernel_integration:
  client: "ObservabilityAPIClient"
  communication: "mTLS + JWT s2s"
  degraded_mode: "Local Prometheus endpoint + stdout logs"

sprint: "S22-P1"
priority: "P1"
```

### 13. **scorecard-service**

```yaml
repositorio: "cloud-core/scorecard-service"
proposito: "Agent scoring, analytics y ML benchmarks"
tecnologias: ["Python", "scikit-learn", "Redis", "TimescaleDB"]
dependencias: ["observability-service"]
dependientes: ["agent-marketplace"]

componente_logico: "Scorecard Module"
ubicacion_arquitectura: "Analytics & Quality Layer"

archivos_clave:
  - "38-scorecard-master-prompt.md" ⭐ (~1,200 líneas)
  - "02-architecture-master-prompt.md"
  - "18-security-master-prompt.md"

responsabilidades:
  - "Multi-dimensional scoring (accuracy, latency, cost, reliability, security)"
  - "ML quality predictor (Gradient Boosting, 85%+ accuracy)"
  - "Leaderboards públicos (Redis sorted sets)"
  - "Agent certification (Bronze/Silver/Gold/Platinum)"

nops_kernel_integration:
  client: "ScorecardAPIClient"
  communication: "mTLS + JWT s2s"
  degraded_mode: "Routing sin scores (round-robin)"

sprint: "S23-P1"
priority: "P2"
```

### 14. **billing-service**

```yaml
repositorio: "cloud-core/billing-service"
proposito: "Usage metering, payment processing y invoicing"
tecnologias: ["Python", "Redis Streams", "Stripe", "PayPal", "WeasyPrint"]
dependencias: ["enis-infrastructure"]
dependientes: ["agent-marketplace", "enis-frontend"]

componente_logico: "Billing Module"
ubicacion_arquitectura: "Revenue & Billing Layer"

archivos_clave:
  - "39-billing-master-prompt.md" ⭐ (~1,300 líneas)
  - "02-architecture-master-prompt.md"
  - "18-security-master-prompt.md"

responsabilidades:
  - "Usage metering en tiempo real (Redis Streams)"
  - "Payment processing (Stripe, PayPal, Wire Transfer)"
  - "Invoice generation (PDF con WeasyPrint)"
  - "PCI-DSS Level 1 compliance"

nops_kernel_integration:
  client: "BillingAPIClient"
  communication: "mTLS + JWT s2s + batching"
  degraded_mode: "Funciona sin billing (recupera después)"

sprint: "S22-P3"
priority: "P1 - REVENUE CRITICAL"
```

### 15. **sandbox-service**

```yaml
repositorio: "cloud-core/sandbox-service"
proposito: "Entorno aislado para testing de Edge Agents"
tecnologias: ["gVisor", "Firecracker", "Kubernetes", "eBPF", "Falco"]
dependencias: ["enis-infrastructure"]
dependientes: ["edge-agents", "agent-marketplace"]

componente_logico: "Sandbox Module"
ubicacion_arquitectura: "Security & Testing Layer"

archivos_clave:
  - "40-sandbox-master-prompt.md" ⭐ (~1,100 líneas)
  - "02-architecture-master-prompt.md"
  - "18-security-master-prompt.md"

responsabilidades:
  - "gVisor + Kubernetes isolation"
  - "Resource limits (cgroups v2 + eBPF)"
  - "Security monitoring (Falco)"
  - "Automated testing framework"

nops_kernel_integration:
  client: "SandboxAPIClient"
  communication: "mTLS + JWT s2s"
  degraded_mode: "Testing deshabilitado"

sprint: "S23-P2"
priority: "P3"
```

### 16. **resource-governance-service**

```yaml
repositorio: "cloud-core/resource-governance-service"
proposito: "Fairness algorithms, cost optimization, forecasting"
tecnologias: ["Python", "scikit-learn", "Prophet", "scipy", "OR-Tools"]
dependencias: ["billing-service", "observability-service"]
dependientes: ["nops-kernel"]

componente_logico: "Resource Governance Module"
ubicacion_arquitectura: "Resource Management Layer"

archivos_clave:
  - "43-resource-governance-master-prompt.md" ⭐ (~1,400 líneas)
  - "02-architecture-master-prompt.md"
  - "18-security-master-prompt.md"

responsabilidades:
  - "ML-based fairness (Weighted Fair Queueing, Max-Min)"
  - "Noisy neighbor detection (Isolation Forest)"
  - "Cost optimization (Linear Programming)"
  - "Resource forecasting (Prophet + LSTM)"
  - "Multi-tenant resource optimization"

nops_kernel_integration:
  client: "❌ No requiere (básico en Policy Engine)"
  communication: "Extiende Policy Engine del kernel"
  degraded_mode: "Kernel usa quotas estáticas"

sprint: "S23-S24 (Q2 2025)"
priority: "P2"
```

### 17. **lifecycle-service**

```yaml
repositorio: "cloud-core/lifecycle-service"
proposito: "Deployment strategies, rollbacks, version management"
tecnologias: ["Go", "Kubernetes Operator", "Helm", "Flagger"]
dependencias: ["enis-infrastructure"]
dependientes: ["edge-agents", "nops-kernel"]

componente_logico: "Lifecycle Module"
ubicacion_arquitectura: "Deployment & Release Layer"

archivos_clave:
  - "42-lifecycle-master-prompt.md" ⭐ (~1,200 líneas)
  - "02-architecture-master-prompt.md"
  - "18-security-master-prompt.md"

responsabilidades:
  - "Deployment strategies (Rolling, Blue-Green, Canary, Recreate)"
  - "Kubernetes Operator implementation"
  - "Automated rollback mechanisms"
  - "Version compatibility matrix"
  - "Health & readiness monitoring"

nops_kernel_integration:
  client: "❌ No requiere (operado por CI/CD)"
  communication: "K8s Operator pattern"
  
sprint: "S23-P2"
priority: "P3"
```

### 18. **compliance-service**

```yaml
repositorio: "cloud-core/compliance-service"
proposito: "Audit trail inmutable, SEC validation, regulatory compliance"
tecnologias: ["Python", "PostgreSQL", "S3 WORM", "AWS KMS", "Cosign"]
dependencias: ["enis-infrastructure"]
dependientes: ["TODOS los servicios (audit obligatorio)"]

componente_logico: "Compliance Module"
ubicacion_arquitectura: "Compliance & Audit Layer"

archivos_clave:
  - "41-compliance-master-prompt.md" ⭐ (~1,200 líneas)
  - "02-architecture-master-prompt.md"
  - "18-security-master-prompt.md"

responsabilidades:
  - "SEC (Signed Execution Contract) - S13.5 blocker"
  - "Audit trail inmutable (append-only + hash chain)"
  - "Regulatory compliance (SOC2, GDPR, HIPAA, ISO27001)"
  - "Forensics toolkit"
  - "SBOM validation (CycloneDX, SPDX)"

nops_kernel_integration:
  client: "ComplianceAPIClient"
  communication: "mTLS + JWT s2s + local fallback"
  degraded_mode: "Local audit.jsonl persistence"

sprint: "S22-P4"
priority: "P1 - CRÍTICO (blocker para S14 Pre-GA)"
```

---

### 🔐 GOVERNANCE (1 repo) - Data Governance Engine

### 19. **data-governance-service**

```yaml
repositorio: "cloud-core/data-governance-service"
proposito: "Motor de gobernanza de datos (DGE) para clasificación, redacción y egress control"
tecnologias: ["Python 3.11+", "FastAPI", "Pydantic", "SpaCy", "Presidio", "Redis"]
dependencias: ["agent-contracts", "agent-sdks", "enis-infrastructure"]
dependientes: ["nops-kernel (Egress Guard)", "ALL services (PII redaction)"]

componente_logico: "Data Governance Engine (DGE)"
ubicacion_arquitectura: "Cloud-core governance layer + Edge Egress Guard"
master_prompt: "25-data-governance-master-prompt.md"

archivos_clave:
  - "25-data-governance-master-prompt.md" ⭐
  - "02-architecture-master-prompt.md"
  - "18-security-master-prompt.md"
  - "GDPR_COMPLIANCE_MASTER_PROMPT.md"

responsabilidades:
  - "Clasificación automática de datos (PII, Sensitive, Business)"
  - "Redacción de PII en logs/metrics/eventos"
  - "Egress control (fail-closed por defecto)"
  - "Policy enforcement (región-based data residency)"
  - "Compliance automation (GDPR/CCPA/PDPA/LGPD)"
  - "Audit trails para data access"

funcionalidades_clave:
  clasificacion:
    - "Regex patterns (emails, SSN, credit cards)"
    - "NER/NLP (Named Entity Recognition con SpaCy)"
    - "ML-based classification (custom models)"
    - "Context-aware rules (GDPR Art. 9 sensitive data)"
  
  redaccion:
    - "Masking (***-**-1234)"
    - "Hashing (SHA-256 determinístico)"
    - "Tokenization (preserva formato)"
    - "Removal (purge completo)"
  
  egress_guard:
    - "Lightweight client en NOPS Kernel"
    - "Validation: datos salientes del edge"
    - "Fail-closed: bloquea si clasificación = PII_SENSITIVE"
    - "Audit: log de intentos bloqueados"

integraciones:
  kernel: "Egress Guard ligero (< 5MB, cache de reglas)"
  services: "API client para redacción en logs/metrics"
  compliance: "Reportes automáticos a Compliance Module"
  dpia: "Input para DPIA (Data Protection Impact Assessment)"

roadmap_key_milestones:
  s_dge_1: "Clasificación regex + NER básico"
  s_dge_2: "Redacción multi-estrategia (mask/hash/token)"
  s_dge_3: "Egress Guard en Kernel (fail-closed)"
  s_dge_4: "ML-based classification (custom models)"
  s_dge_5: "GDPR automation (right-to-be-forgotten)"

slos_objetivo:
  classification_latency: "p95 < 50ms (real-time)"
  redaction_latency: "p95 < 20ms (inline)"
  egress_validation: "p95 < 10ms (non-blocking edge)"
  accuracy: "> 95% (PII detection)"
  false_positive_rate: "< 5%"

priority: "P0 - CRÍTICO (compliance blocker para Enterprise Tier 3)"
```

---

## 🔧 CLOUD-OPS (1 repo) - Infraestructura

### 20. **cloud-infrastructure**

```yaml
repositorio: "cloud-ops/cloud-infrastructure"
proposito: "Infraestructura cloud y operaciones"
tecnologias: ["Terraform", "Helm", "Kubernetes", "ArgoCD"]
dependencias: ["enis-infrastructure"]
dependientes: ["TODOS los servicios cloud-core"]

componente_logico: "Cloud Infrastructure & Operations"
ubicacion_arquitectura: "Cloud deployment layer"

archivos_clave:
  - "CLOUD_INFRASTRUCTURE_MASTER_PROMPT.md" ⭐
  - "02-architecture-master-prompt.md"
  - "18-security-master-prompt.md"
  - "19-performance-master-prompt.md"
  - "22-monitoring-master-prompt.md"
  - "24-disaster-recovery-master-prompt.md"
  - "25-cost-optimization-master-prompt.md"

responsabilidades:
  - "Deploy de servicios cloud-core"
  - "Kubernetes cluster management"
  - "CI/CD pipelines"
  - "Disaster recovery"
  - "Cost optimization"
  - "Multi-cloud strategies"
```

---

### 🎤🥽 INTERFACES AVANZADAS (2 repos)

#### 21. **voice-interface-service**

```yaml
repositorio: "cloud-core/voice-interface-service"
proposito: "Procesamiento de voz en tiempo real con capacidades avanzadas"
tecnologias: ["Python 3.11+", "FastAPI", "WebSocket", "SSE", "Whisper", "webrtcvad", "Silero"]
dependencias: ["inference-service", "agent-contracts", "agent-sdks"]
dependientes: ["enis-frontend", "studio-app"]

componentes_logicos:
  - "Voice Orchestrator (STT/VAD/TTS)"
  - "Natural Prompt Controller"
  - "Secure Voice Authenticator"
  - "Fallback Corrector Agent"

ubicacion_arquitectura: "Cloud processing layer"

master_prompts_asociados:
  primario: "26-natural-interface-master-prompt.md"
  arquitectura: "02-architecture-master-prompt.md"
  seguridad: "18-security-master-prompt.md"
  performance: "19-performance-master-prompt.md"
  monitoreo: "22-monitoring-master-prompt.md"

caracteristicas_tecnicas:
  - "TTFT < 300ms"
  - "Bargein < 100ms"
  - "WebSocket + SSE streaming"
  - "Reconexión automática + resume tokens"
  - "Múltiples providers (Whisper, Google STT, webrtcvad, Silero)"

integracion_nops:
  - "Conecta directamente con Inference Service"
  - "NO requiere client en NOPS Kernel"
  - "Opera como microservicio independiente"

roadmap_timeline: "Q2 2025"
```

#### 22. **xr-interface-service**

```yaml
repositorio: "cloud-core/xr-interface-service"
proposito: "Procesamiento de interfaces de realidad extendida (XR)"
tecnologias: ["Go 1.21", "OpenXR", "WebGL", "WebRTC", "OpenXR SDK"]
dependencias: ["inference-service", "agent-contracts", "agent-sdks"]
dependientes: ["enis-frontend", "studio-app"]

componentes_logicos:
  - "OpenXR Adapter"
  - "Spatial Context Manager"
  - "Gesture Voice Router"
  - "Avatar Copilot Controller"
  - "Haptic Feedback System"

dispositivos_soportados:
  - "Meta Quest 3"
  - "Apple Vision Pro"
  - "HoloLens 2"

ubicacion_arquitectura: "Cloud processing layer"

master_prompts_asociados:
  primario: "27-xr-interface-master-prompt.md"
  arquitectura: "02-architecture-master-prompt.md"
  seguridad: "18-security-master-prompt.md"
  performance: "19-performance-master-prompt.md"
  monitoreo: "22-monitoring-master-prompt.md"

caracteristicas_tecnicas:
  - "30Hz streaming con jitter < 50ms"
  - "Fusión multimodal (mano + gaze + voz)"
  - "Spatial mapping y gesture recognition"
  - "Haptic feedback system"
  - "3D rendering engines"

integracion_nops:
  - "Conecta directamente con Inference Service"
  - "NO requiere client en NOPS Kernel"
  - "Opera como microservicio independiente"

roadmap_timeline: "Q3 2025"
```

---

## 🛒 PLATFORM (2 repos) - Marketplace y Frontend

### 23. **agent-marketplace**

```yaml
repositorio: "platform/agent-marketplace"
proposito: "Marketplace público y privado de agents"
tecnologias: ["Python 3.11+", "FastAPI", "Next.js", "PostgreSQL"]
dependencias: ["agent-contracts", "agent-sdks"]
dependientes: ["enis-frontend"]

componentes_logicos:
  - "Agent Marketplace (Cloud)"
  - "Private Registry"
  - "Developer Portal"

ubicacion_arquitectura: "Platform marketplace layer"

archivos_clave:
  - "AGENT_MARKETPLACE_MASTER_PROMPT.md" ⭐
  - "08-marketplace-master-prompt.md" ⭐
  - "AGENT_CONTRACTS_MASTER_PROMPT.md"
  - "AGENT_SDKS_MASTER_PROMPT.md"
  - "03-business-master-prompt.md"
  - "18-security-master-prompt.md"
  - "25-cost-optimization-master-prompt.md"

responsabilidades:
  - "Public marketplace"
  - "Private registry"
  - "Developer portal"
  - "Certification workflow"
  - "Revenue sharing 70/30"
  - "Agent discovery"
```

### 24. **enis-frontend**

```yaml
repositorio: "platform/enis-frontend"
proposito: "Frontend y Studio App"
tecnologias: ["Next.js", "React", "TypeScript", "Tailwind CSS"]
dependencias: ["agent-sdks", "agent-marketplace"]
dependientes: []

componente_logico: "Studio App (UI/IDE External)"
ubicacion_arquitectura: "User interface layer"

archivos_clave:
  - "ENIS_FRONTEND_MASTER_PROMPT.md" ⭐
  - "17-uiux-dashboard-master-prompt.md" ⭐
  - "05-reference-master-prompt.md"
  - "23-data-management-master-prompt.md"
  - "26-natural-interface-master-prompt.md"
  - "27-xr-interface-master-prompt.md"
  - "28-edge-hub-master-prompt.md"
  - "29-future-vision-enis-master-prompt.md"

responsabilidades:
  - "Dashboard de gestión"
  - "IDE/Studio para desarrollo"
  - "Voice interface (S16)"
  - "XR interface (S17)"
  - "Agent monitoring UI"
  - "Marketplace browsing"
```

---

## 🗺️ Matriz de Dependencias

| # | Repo | Depende de | Es dependencia de | Master Prompts Principales |
|---|------|------------|-------------------|---------------------------|
| 1 | **agent-contracts** | - | TODOS | 02, 18, 20, **30** |
| 2 | **agent-sdks** | contracts | edge-agents, frontend, marketplace | 04, 09, 20, 21, **31** |
| 3 | **enis-infrastructure** | - | cloud-infra, edge-infra | 02, 18, 19, 22, 24, **32** |
| 4 | **nops-kernel** | contracts, sdks | edge-agents | **07**, 11, 02, 06, 10, 18, 19, 22 |
| 5 | **edge-agents** | nops-kernel, contracts, sdks | - | **10**, 04, 18, 19, 21 |
| 6 | **edge-infrastructure** | enis-infrastructure | nops, edge-agents | 02, 10, 18, 19, 22, 24, **34** |
| 7 | **asm-service** | contracts | inference | **13**, 02, 18, 19 |
| 8 | **cgn-service** | contracts | inference | **14**, 02, 18, 19 |
| 9 | **awe-service** | contracts, asm | inference | **15**, 02, 18, 19 |
| 10 | **shif-service** | contracts | inference | **16**, 02, 18, 19 |
| 11 | **inference-service** | contracts, ASM, CGN, AWE, SHIF | - | **12**, 02, 18, 19, 22, **30** |
| 12 | **observability-service** 🆕 | enis-infrastructure | TODOS | **37**, 02, 18, 19, 22 |
| 13 | **scorecard-service** 🆕 | observability | marketplace | **38**, 02, 18, 19 |
| 14 | **billing-service** 🆕 | enis-infrastructure | marketplace, frontend | **39**, 02, 18, 19 |
| 15 | **sandbox-service** 🆕 | enis-infrastructure | edge-agents, marketplace | **40**, 02, 18 |
| 16 | **resource-governance** 🆕 | billing, observability | nops-kernel | **43**, 02, 18, 19 |
| 17 | **lifecycle-service** 🆕 | enis-infrastructure | edge-agents, nops | **42**, 02, 18 |
| 18 | **compliance-service** 🆕 | enis-infrastructure | TODOS (audit) | **41**, 02, 18 |
| 19 | **cloud-infrastructure** | enis-infrastructure | cloud-core services | 02, 18, 19, 22, 24, 25, **33** |
| 20 | **agent-marketplace** | contracts, sdks | frontend | **08**, 03, 18, 25, **35** |
| 21 | **enis-frontend** | sdks, marketplace | - | **17**, 05, 23, 26, 27, 28, 29, **36** |

---

## 📋 Roadmaps por Repositorio

```yaml
roadmaps_existentes:
  con_roadmap:
    - "nops-kernel/ROADMAP_SPRINTS_NOPS_KERNEL.md" ✅ (S1-S22, incluye S13.5 SEC)
    - "inference-service/ROADMAP_INFERENCE_SERVICE.md" ✅
    - "agent-contracts/agent_contracts_roadmap_2025_2026_detallado.md" ✅
  
  sin_roadmap_usar_master_prompts:
    # Edge
    - "edge-agents/" ⏳ (Usar 10-edge-master-prompt.md)
    - "edge-infrastructure/" ⏳ (Usar 34-edge-infrastructure-master-prompt.md)
    
    # Cloud-Core: Macro-Módulos
    - "asm-service/" ⏳ (Usar 13-asm-master-prompt.md)
    - "cgn-service/" ⏳ (Usar 14-cgn-master-prompt.md)
    - "awe-service/" ⏳ (Usar 15-awe-master-prompt.md)
    - "shif-service/" ⏳ (Usar 16-shif-master-prompt.md)
    
    # Cloud-Core: 7 Módulos NOPS 🆕
    - "observability-service/" ⏳ (Usar 37-observability-master-prompt.md)
    - "scorecard-service/" ⏳ (Usar 38-scorecard-master-prompt.md)
    - "billing-service/" ⏳ (Usar 39-billing-master-prompt.md)
    - "sandbox-service/" ⏳ (Usar 40-sandbox-master-prompt.md)
    - "compliance-service/" ⏳ (Usar 41-compliance-master-prompt.md)
    - "lifecycle-service/" ⏳ (Usar 42-lifecycle-master-prompt.md)
    - "resource-governance-service/" ⏳ (Usar 43-resource-governance-master-prompt.md)
    
    # Platform
    - "agent-marketplace/" ⏳ (Usar 08-marketplace-master-prompt.md + 35)
    - "enis-frontend/" ⏳ (Usar 17-uiux-dashboard-master-prompt.md + 36)
    
    # Shared
    - "agent-sdks/" ⏳ (Usar 31-agent-sdks-master-prompt.md)
    - "enis-infrastructure/" ⏳ (Usar 32-enis-infrastructure-master-prompt.md)
    
    # Cloud-Ops
    - "cloud-infrastructure/" ⏳ (Usar 33-cloud-infrastructure-master-prompt.md)
```

---

## 🔗 Integración Multi-Repo en Sprints

### Ejemplo: Sprint S2 - Agent Registry

```yaml
sprint_s2_multi_repo:
  repos_involucrados:
    nops_kernel:
      responsabilidad: "Implementar Agent Registry core"
      archivos:
        - "src/registry/agent_registry.py"
        - "src/models/agent.py"
        - "tests/test_registry.py"
    
    agent_contracts:
      responsabilidad: "Definir schemas de Agent"
      archivos:
        - "schemas/agent_registry.proto"
        - "schemas/agent_capabilities.json"
        - "api/agent_api.yaml (OpenAPI)"
    
    agent_sdks:
      responsabilidad: "SDK para registro de agents"
      archivos:
        - "python/enis_sdk/registry.py"
        - "go/pkg/registry/client.go"
        - "typescript/src/registry.ts"
    
    edge_agents:
      responsabilidad: "Implementar auto-registro"
      archivos:
        - "src/common/registration.py"
        - "src/heartbeat/service.py"
  
  coordinacion:
    secuencia:
      1: "agent-contracts define schema"
      2: "nops-kernel implementa registry"
      3: "agent-sdks genera cliente"
      4: "edge-agents integra auto-registro"
    
    validacion:
      - "Contract tests entre repos"
      - "Integration tests end-to-end"
      - "Performance benchmarks"
```

---

## 📊 Master Prompts vs Repositorios

### Por Master Prompt

```yaml
master_prompt_coverage:
  "02-architecture-master-prompt.md":
    presente_en: ["nops-kernel", "edge-agents", "edge-infrastructure", "asm", "cgn", "awe", "shif", "inference", "cloud-infrastructure", "agent-contracts", "enis-infrastructure"]
    cobertura: "11/14 (79%)"
    
  "07-nops-master-prompt.md":
    presente_en: ["nops-kernel"]
    cobertura: "1/14 (7%)"
    criticidad: "ALTA - Core del NOPS"
    
  "10-edge-master-prompt.md":
    presente_en: ["nops-kernel", "edge-agents", "edge-infrastructure"]
    cobertura: "3/14 (21%)"
    criticidad: "ALTA - Especificación edge"
    
  "18-security-master-prompt.md":
    presente_en: ["TODOS los 14 repositorios"]
    cobertura: "14/14 (100%)"
    criticidad: "CRÍTICA - Security by design"
    
  "19-performance-master-prompt.md":
    presente_en: ["nops-kernel", "edge-agents", "edge-infrastructure", "asm", "cgn", "awe", "shif", "inference", "cloud-infrastructure", "enis-infrastructure"]
    cobertura: "10/14 (71%)"
    criticidad: "ALTA - Performance targets"
    
  "22-monitoring-master-prompt.md":
    presente_en: ["nops-kernel", "edge-infrastructure", "inference", "cloud-infrastructure", "enis-infrastructure"]
    cobertura: "5/14 (36%)"
    criticidad: "ALTA - Observabilidad"
```

---

## 🎯 Recomendaciones para Roadmap NOPS Kernel

### ✅ **Master Prompts CRÍTICOS a Integrar:**

```yaml
roadmap_nops_debe_considerar:
  criticos:
    - "07-nops-master-prompt.md" ⭐⭐⭐ (YA APLICADO)
    - "10-edge-master-prompt.md" ⭐⭐⭐ (PARCIALMENTE - falta detalles de 5 tipos)
    - "18-security-master-prompt.md" ⭐⭐⭐ (YA APLICADO)
    - "02-architecture-master-prompt.md" ⭐⭐ (PARCIALMENTE)
    
  importantes:
    - "06-orchestrator-master-prompt.md" ⭐⭐ (YA APLICADO implícitamente)
    - "19-performance-master-prompt.md" ⭐⭐ (YA APLICADO)
    - "22-monitoring-master-prompt.md" ⭐⭐ (YA APLICADO)
    - "11-nops-complete-master-prompt.md" ⭐ (Referencia)
    
  adicionales:
    - "13-asm-master-prompt.md" ⭐ (Para integración ASM)
    - "12-inference-master-prompt.md" ⭐ (Para integración Inference)
    - "20-integration-master-prompt.md" (Para patrones)
```

### 📝 **Sprints que Requieren Multi-Repo:**

```yaml
sprints_multi_repo:
  S2_agent_registry:
    repos: ["nops-kernel", "agent-contracts", "agent-sdks", "edge-agents"]
    coordinacion: "Alta"
    
  S11_agent_sdk:
    repos: ["nops-kernel", "agent-sdks", "agent-contracts"]
    coordinacion: "Muy Alta"
    
  S12_federation:
    repos: ["nops-kernel", "inference-service", "agent-contracts"]
    coordinacion: "Alta"
    
  S13_security:
    repos: ["nops-kernel", "edge-agents", "inference-service", "agent-contracts"]
    coordinacion: "Crítica"
    
  S15_gateway:
    repos: ["nops-kernel", "cloud-infrastructure", "agent-marketplace"]
    coordinacion: "Media"
```

---

## 🚀 Conclusión

### **Estructura del Proyecto:**

```yaml
resumen_ejecutivo:
  total_repositorios: 24  # Actualizado 2025-01-09
  
  distribucion:
    shared: "12.5% (3/24) - Base común"
    edge: "12.5% (3/24) - Cliente/Edge"
    cloud_core: "62.5% (15/24) - Servicios principales (5 macro + 7 NOPS + 2 interfaces avanzadas + 1 governance DGE)"
    cloud_ops: "4.2% (1/24) - Infraestructura"
    platform: "8.3% (2/24) - Marketplace y UI"
  
  cloud_core_detalle:
    macro_modulos: "5 repos (ASM, CGN, AWE, SHIF, Inference)"
    nops_modules: "7 repos (Obs, Score, Bill, Sandbox, Governance, Lifecycle, Compliance)"
    interfaces_avanzadas: "2 repos (Voice Interface, XR Interface)"
    governance: "1 repo (Data Governance Engine - DGE)"
  
  roadmaps_con_sprints:
    - "nops-kernel (S1-S22, incluye S13.5 SEC)"
    - "inference-service (roadmap completo)"
    - "agent-contracts (roadmap 2025-2026)"
  
  master_prompts_nuevos:
    rango: "37-43 (7 módulos NOPS)"
    total_lineas: "~9,000 líneas profesionales"
    estado: "TODOS completados ✅"
    
  master_prompts_mas_usados:
    1: "18-security-master-prompt.md (21/21 repos = 100%)"
    2: "02-architecture-master-prompt.md (19/21 repos = 90%)"
    3: "19-performance-master-prompt.md (16/21 repos = 76%)"
  
  nops_kernel_api_clients:
    implementados: 5
    clientes:
      - "ObservabilityAPIClient (37)"
      - "ScorecardAPIClient (38)"
      - "BillingAPIClient (39)"
      - "SandboxAPIClient (40)"
      - "ComplianceAPIClient (41)"
    no_requieren_client:
      - "ResourceGovernance (43 - básico en Policy Engine)"
      - "Lifecycle (42 - K8s Operator)"
```

---

## 📌 Referencias

- **Arquitectura Visual**: `arquitecturaenisv2.html`
- **Roadmap NOPS**: `edge/nops-kernel/ROADMAP_SPRINTS_NOPS_KERNEL.md`
- **Roadmap Inference**: `cloud-core/inference-service/ROADMAP_INFERENCE_SERVICE.md`
- **Roadmap Contracts**: `shared/agent-contracts/agent_contracts_roadmap_2025_2026_detallado.md`

---

**Generado:** 2025-10-08  
**Actualizado:** 2025-10-09 (Agregados 7 módulos NOPS)  
**Autor:** @andaon  
**Compliance:** DNA v3.0 ✅  
**Versión:** 2.0 (21 repositorios)

