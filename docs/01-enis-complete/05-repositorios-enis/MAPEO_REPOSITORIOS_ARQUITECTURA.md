# 🗺️ Mapeo Repositorios ↔ Arquitectura ENIS v3.0

## 📋 Metadata

```yaml
doc_version: "1.0"
doc_type: "Mapping Documentation"
doc_author: "@andaon"
doc_date: "2025-10-08"
dna_version: "3.0"
compliance: "DNA_v3_compliant"
total_repos: 14
categories: ["shared", "edge", "cloud-core", "cloud-ops", "platform"]
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

## 📊 Vista General: 14 Repositorios

```yaml
organizacion_repositorios:
  total: 14
  
  categorias:
    shared: 3    # Base común para todos
    edge: 3      # Componentes del cliente
    cloud_core: 5  # Servicios principales
    cloud_ops: 1   # Infraestructura y operaciones
    platform: 2    # Marketplace y frontend
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

## ☁️ CLOUD-CORE (5 repos) - Servicios Principales

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

## 🔧 CLOUD-OPS (1 repo) - Infraestructura

### 12. **cloud-infrastructure**

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

## 🛒 PLATFORM (2 repos) - Marketplace y Frontend

### 13. **agent-marketplace**

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

### 14. **enis-frontend**

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

| Repo | Depende de | Es dependencia de | Master Prompts |
|------|------------|-------------------|----------------|
| **agent-contracts** | - | TODOS | 02, 18, 20 |
| **agent-sdks** | contracts | edge-agents, frontend, marketplace | 04, 09, 20, 21 |
| **enis-infrastructure** | - | cloud-infrastructure, edge-infrastructure | 02, 18, 19, 22, 24 |
| **nops-kernel** | contracts, sdks | edge-agents | **07**, 11, 02, 06, 10, 18, 19, 22 |
| **edge-agents** | nops-kernel, contracts, sdks | - | **10**, 04, 18, 19, 21 |
| **edge-infrastructure** | enis-infrastructure | nops, edge-agents | 02, 10, 18, 19, 22, 24 |
| **asm-service** | contracts | inference | **13**, 02, 18, 19 |
| **cgn-service** | contracts | inference | **14**, 02, 18, 19 |
| **awe-service** | contracts, asm | inference | **15**, 02, 18, 19 |
| **shif-service** | contracts | inference | **16**, 02, 18, 19 |
| **inference-service** | contracts, ASM, CGN, AWE, SHIF | - | **12**, 02, 18, 19, 22 |
| **cloud-infrastructure** | enis-infrastructure | cloud-core services | 02, 18, 19, 22, 24, 25 |
| **agent-marketplace** | contracts, sdks | frontend | **08**, 03, 18, 25 |
| **enis-frontend** | sdks, marketplace | - | **17**, 05, 23, 26, 27, 28, 29 |

---

## 📋 Roadmaps por Repositorio

```yaml
roadmaps_existentes:
  con_roadmap:
    - "nops-kernel/ROADMAP_SPRINTS_NOPS_KERNEL.md" ✅
    - "inference-service/ROADMAP_INFERENCE_SERVICE.md" ✅
    - "agent-contracts/agent_contracts_roadmap_2025_2026_detallado.md" ✅
  
  sin_roadmap:
    - "edge-agents/" ⏳ (Usar 10-edge-master-prompt.md)
    - "asm-service/" ⏳ (Usar 13-asm-master-prompt.md)
    - "cgn-service/" ⏳ (Usar 14-cgn-master-prompt.md)
    - "awe-service/" ⏳ (Usar 15-awe-master-prompt.md)
    - "shif-service/" ⏳ (Usar 16-shif-master-prompt.md)
    - "agent-marketplace/" ⏳ (Usar 08-marketplace-master-prompt.md)
    - "enis-frontend/" ⏳ (Usar 17-uiux-dashboard-master-prompt.md)
    - "cloud-infrastructure/" ⏳
    - "edge-infrastructure/" ⏳
    - "agent-sdks/" ⏳
    - "enis-infrastructure/" ⏳
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
  total_repositorios: 14
  
  distribucion:
    shared: "21% (3/14) - Base común"
    edge: "21% (3/14) - Cliente/Edge"
    cloud_core: "36% (5/14) - Servicios principales"
    cloud_ops: "7% (1/14) - Infraestructura"
    platform: "14% (2/14) - Marketplace y UI"
  
  roadmaps_con_sprints:
    - "nops-kernel (S1-S21, 21 sprints)"
    - "inference-service (tiene roadmap)"
    - "agent-contracts (roadmap 2025-2026)"
  
  master_prompts_mas_usados:
    1: "18-security-master-prompt.md (14/14 repos = 100%)"
    2: "02-architecture-master-prompt.md (11/14 repos = 79%)"
    3: "19-performance-master-prompt.md (10/14 repos = 71%)"
  
  recomendacion_roadmap_nops:
    estrategia: "Usar TODOS los master prompts relacionados"
    justificacion: "NOPS Kernel es orquestador central que integra TODOS los componentes"
    master_prompts_minimos: ["02", "06", "07", "10", "11", "18", "19", "22"]
    resultado: "Roadmap completo e integrado con dependencias claras"
```

---

## 📌 Referencias

- **Arquitectura Visual**: `arquitecturaenisv2.html`
- **Roadmap NOPS**: `edge/nops-kernel/ROADMAP_SPRINTS_NOPS_KERNEL.md`
- **Roadmap Inference**: `cloud-core/inference-service/ROADMAP_INFERENCE_SERVICE.md`
- **Roadmap Contracts**: `shared/agent-contracts/agent_contracts_roadmap_2025_2026_detallado.md`

---

**Generado:** 2025-10-08  
**Autor:** @andaon  
**Compliance:** DNA v3.0 ✅

