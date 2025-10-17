<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
Índice

- [🗺️ MAPEO DETALLADO: PROMPTS MASTER → REPOSITORIOS](#-mapeo-detallado-prompts-master-%E2%86%92-repositorios)
  - [📋 **TABLA COMPLETA DE CLASIFICACIÓN**](#-tabla-completa-de-clasificaci%C3%93n)
  - [🏗️ **DISTRIBUCIÓN POR REPOSITORIO**](#-distribuci%C3%93n-por-repositorio)
    - [**📦 nops-kernel (8 prompts)**](#-nops-kernel-8-prompts)
    - [**☁️ inference-service (1 prompt)**](#-inference-service-1-prompt)
    - [**🧠 asm-service (1 prompt)**](#-asm-service-1-prompt)
    - [**🕸️ cgn-service (1 prompt)**](#-cgn-service-1-prompt)
    - [**⚡ awe-service (1 prompt)**](#-awe-service-1-prompt)
    - [**🔗 shif-service (1 prompt)**](#-shif-service-1-prompt)
    - [**🛒 agent-marketplace (1 prompt)**](#-agent-marketplace-1-prompt)
    - [**🖥️ enis-dashboard (3 prompts)**](#-enis-dashboard-3-prompts)
    - [**🏗️ enis-infrastructure (7 prompts)**](#-enis-infrastructure-7-prompts)
    - [**📚 enis-docs (6 prompts)**](#-enis-docs-6-prompts)
  - [🎯 **JUSTIFICACIÓN DE CLASIFICACIÓN**](#-justificaci%C3%93n-de-clasificaci%C3%93n)
    - [**Criterios de Clasificación:**](#criterios-de-clasificaci%C3%B3n)
    - [**Ejemplos de Clasificación:**](#ejemplos-de-clasificaci%C3%B3n)
  - [📊 **ESTADÍSTICAS DE DISTRIBUCIÓN**](#-estad%C3%8Dsticas-de-distribuci%C3%93n)
  - [🚀 **PRÓXIMOS PASOS**](#-pr%C3%93ximos-pasos)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# 🗺️ MAPEO DETALLADO: PROMPTS MASTER → REPOSITORIOS

## 📋 **TABLA COMPLETA DE CLASIFICACIÓN**

| # | Prompt Master | Repositorio | Propósito | Tecnología | Estado |
|---|---------------|-------------|-----------|------------|--------|
| **00** | `00-dna-master-prompt-bundle-v3.0-4001` | **enis-docs** | DNA fundacional del proyecto | Markdown | 📋 Planificado |
| **02** | `02-architecture` | **enis-infrastructure** | Arquitectura general del sistema | Markdown | 📋 Planificado |
| **03** | `03-business-master-prompt-bundle-v3.0-4001` | **enis-docs** | Documentación de negocio | Markdown | 📋 Planificado |
| **04** | `04-implementation-master-prompt-bundle-v3.0-4001` | **enis-infrastructure** | Guías de implementación | Markdown | 📋 Planificado |
| **05** | `05-reference-master-prompt-bundle-v3.0-4001` | **enis-docs** | Referencias técnicas | Markdown | 📋 Planificado |
| **06** | `06-orchestrator-master-prompt-bundle-v3.0-4001` | **enis-docs** | Orquestación general | Markdown | 📋 Planificado |
| **07** | `07-nops-master-prompt-bundle-v3.0-4001` | **nops-kernel** | NOPS Kernel Core | Python/FastAPI | ✅ Implementado |
| **08** | `08-marketplace-docs-v3.0-9344` | **agent-marketplace** | Marketplace de agentes | Python/FastAPI | 📋 Planificado |
| **09** | `09-dev-generation-v3.0-ALL-96062` | **enis-infrastructure** | Generación de código | Multi-lenguaje | 📋 Planificado |
| **10** | `10-edge-master-prompt-bundle-v3.0-4001` | **nops-kernel** | Edge Agents | Python/FastAPI | ✅ Implementado |
| **11** | `11-nops-complete-docs-XL-v3.0-38977` | **nops-kernel** | Documentación completa NOPS | Markdown | ✅ Implementado |
| **12** | `12-inference-docs-XL-v3.0-10446` | **inference-service** | Servicio de inferencia | Python/TensorFlow | 🚧 En desarrollo |
| **13** | `13-asm-docs-XL-v3.0-96665` | **asm-service** | Adaptive State Manager | Python/Redis | 📋 Planificado |
| **14** | `14-cgn-docs-XL-v3.0-51555` | **cgn-service** | Cognitive Graph Network | Python/Neo4j | 📋 Planificado |
| **15** | `15-awe-docs-XL-v3.0-40660` | **awe-service** | Adaptive Workflow Evolution | Python/Celery | 📋 Planificado |
| **16** | `16-shif-docs-XL-v3.0-56469` | **shif-service** | Secure Hybrid Integration | Python/Kafka | 📋 Planificado |
| **17** | `17-uiux-dashboard-docs-XL-v3.0-59730` | **enis-dashboard** | Dashboard principal | Next.js/TypeScript | 📋 Planificado |
| **18** | `18-security-XL-v3.0-776016` | **nops-kernel** | Seguridad y compliance | Python/FastAPI | ✅ Implementado |
| **19** | `19-performance` | **nops-kernel** | Optimización de rendimiento | Python/FastAPI | ✅ Implementado |
| **20** | `20-integration-apis_XL` | **enis-infrastructure** | APIs de integración | Multi-lenguaje | 📋 Planificado |
| **21** | `21-testing-qa_XL` | **nops-kernel** | Testing y QA | Python/pytest | ✅ Implementado |
| **22** | `22-monitoring-observability_XL` | **nops-kernel** | Monitoreo y observabilidad | Python/OpenTelemetry | ✅ Implementado |
| **23** | `23-data-management-analytics_XL` | **enis-infrastructure** | Data Management | Python/PostgreSQL | 📋 Planificado |
| **24** | `24-disaster-recovery-bc_XL` | **nops-kernel** | Disaster Recovery | Python/FastAPI | ✅ Implementado |
| **25** | `25-cost-optimization-docs-XXL-v3.0-13650` | **enis-infrastructure** | Optimización de costos | Terraform/K8s | 📋 Planificado |
| **26** | `26-natural-interface-docs-XXL-v3.0-11742` | **enis-dashboard** | Interfaces naturales | Next.js/TypeScript | 📋 Planificado |
| **27** | `27-xr-interface-docs-XXXL-v3.0-52283` | **enis-dashboard** | Interfaces XR (AR/VR) | Next.js/TypeScript | 📋 Planificado |
| **28** | `28-edge-hub-docs-XXL-v3.0-65284` | **enis-infrastructure** | Edge Hub | Python/FastAPI | 📋 Planificado |
| **29** | `29-future-vision-enis-master-prompt-bundle-v3.0-4001` | **enis-docs** | Visión futura | Markdown | 📋 Planificado |
| **future** | `future-proof-updates-XXL-v3.0-92919` | **enis-docs** | Actualizaciones futuras | Markdown | 📋 Planificado |

---

## 🏗️ **DISTRIBUCIÓN POR REPOSITORIO**

### **📦 nops-kernel (8 prompts)**
- `07-nops-master-prompt-bundle-v3.0-4001` - Core NOPS
- `10-edge-master-prompt-bundle-v3.0-4001` - Edge Agents
- `11-nops-complete-docs-XL-v3.0-38977` - Documentación completa
- `18-security-XL-v3.0-776016` - Seguridad
- `19-performance` - Rendimiento
- `21-testing-qa_XL` - Testing
- `22-monitoring-observability_XL` - Monitoreo
- `24-disaster-recovery-bc_XL` - Disaster Recovery

### **☁️ inference-service (1 prompt)**
- `12-inference-docs-XL-v3.0-10446` - Servicio de inferencia

### **🧠 asm-service (1 prompt)**
- `13-asm-docs-XL-v3.0-96665` - Adaptive State Manager

### **🕸️ cgn-service (1 prompt)**
- `14-cgn-docs-XL-v3.0-51555` - Cognitive Graph Network

### **⚡ awe-service (1 prompt)**
- `15-awe-docs-XL-v3.0-40660` - Adaptive Workflow Evolution

### **🔗 shif-service (1 prompt)**
- `16-shif-docs-XL-v3.0-56469` - Secure Hybrid Integration

### **🛒 agent-marketplace (1 prompt)**
- `08-marketplace-docs-v3.0-9344` - Marketplace de agentes

### **🖥️ enis-dashboard (3 prompts)**
- `17-uiux-dashboard-docs-XL-v3.0-59730` - Dashboard principal
- `26-natural-interface-docs-XXL-v3.0-11742` - Interfaces naturales
- `27-xr-interface-docs-XXXL-v3.0-52283` - Interfaces XR

### **🏗️ enis-infrastructure (7 prompts)**
- `02-architecture` - Arquitectura general
- `04-implementation-master-prompt-bundle-v3.0-4001` - Implementación
- `09-dev-generation-v3.0-ALL-96062` - Generación de código
- `20-integration-apis_XL` - APIs de integración
- `23-data-management-analytics_XL` - Data Management
- `25-cost-optimization-docs-XXL-v3.0-13650` - Optimización de costos
- `28-edge-hub-docs-XXL-v3.0-65284` - Edge Hub

### **📚 enis-docs (6 prompts)**
- `00-dna-master-prompt-bundle-v3.0-4001` - DNA fundacional
- `03-business-master-prompt-bundle-v3.0-4001` - Negocio
- `05-reference-master-prompt-bundle-v3.0-4001` - Referencias
- `06-orchestrator-master-prompt-bundle-v3.0-4001` - Orquestación
- `29-future-vision-enis-master-prompt-bundle-v3.0-4001` - Visión futura
- `future-proof-updates-XXL-v3.0-92919` - Actualizaciones futuras

---

## 🎯 **JUSTIFICACIÓN DE CLASIFICACIÓN**

### **Criterios de Clasificación:**

1. **Funcionalidad Principal**: ¿Qué hace el prompt?
2. **Tecnología**: ¿Qué stack tecnológico usa?
3. **Ubicación**: ¿Edge o Cloud?
4. **Dependencias**: ¿De qué otros componentes depende?
5. **Responsabilidad**: ¿Cuál es su responsabilidad principal?

### **Ejemplos de Clasificación:**

#### **nops-kernel**
- **Criterio**: Control plane que vive en el cliente
- **Prompts**: Todos los relacionados con orquestación local, seguridad, monitoreo
- **Justificación**: Es el núcleo que orquesta agentes desde el edge

#### **inference-service**
- **Criterio**: Servicio especializado de inferencia de IA
- **Prompts**: Solo el prompt de inferencia
- **Justificación**: Servicio independiente con responsabilidad específica

#### **enis-docs**
- **Criterio**: Documentación y referencias generales
- **Prompts**: DNA, business, reference, orchestrator
- **Justificación**: Documentación transversal que no pertenece a un servicio específico

---

## 📊 **ESTADÍSTICAS DE DISTRIBUCIÓN**

```yaml
distribucion:
  total_prompts: 29
  total_repositorios: 8

  por_repositorio:
    nops-kernel: 8 (27.6%)
    enis-infrastructure: 7 (24.1%)
    enis-docs: 6 (20.7%)
    enis-dashboard: 3 (10.3%)
    inference-service: 1 (3.4%)
    asm-service: 1 (3.4%)
    cgn-service: 1 (3.4%)
    awe-service: 1 (3.4%)
    shif-service: 1 (3.4%)
    agent-marketplace: 1 (3.4%)

  por_estado:
    implementado: 8 (27.6%)
    en_desarrollo: 1 (3.4%)
    planificado: 20 (69.0%)
```

---

## 🚀 **PRÓXIMOS PASOS**

1. **Validar clasificación** con el equipo técnico
2. **Crear repositorios** según la clasificación
3. **Migrar prompts** a sus repositorios correspondientes
4. **Establecer dependencias** entre repositorios
5. **Implementar CI/CD** para cada repositorio

---

*Mapeo generado el 30 de enero de 2025 - ENIS v3.0*
