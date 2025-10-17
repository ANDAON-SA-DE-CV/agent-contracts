#  Roadmap de Sprints  agent-contracts (completo y actualizado)

_Roadmap Completo  Agent Contracts (S0–S16)_

**Monorepo:** `shared/agent-contracts`

**Estructura:**
- `openapi/v1/`
- `schemas/`
- `proto/`
- `sdks/{python,typescript,go,java,dotnet}/`
- `scripts/{validate,breaking,baseline,examples,bench}/`
- `tests/{contracts,examples,pact}/`
- `docs/{guides,examples,troubleshooting,benchmarks}/`
- `docs/01-sprint/{S0..S19}/` - Documentación organizada por sprint

---

## 📋 Tabla de Mapeo de Documentación por Sprint

> **Convención de Rutas**: Todos los documentos de sprint se organizan en `docs/01-sprint/S{número}/`

| Sprint | Documentos Clave | Ruta | Propósito |
|--------|------------------|------|-----------|
| **S0** | Kickoff & Setup | `docs/01-sprint/S0/` | |
| | README-Kickoff.md | `docs/01-sprint/S0/README-Kickoff.md` | Checklist de inicio, secrets, setup |
| | roadmap.md | `docs/01-sprint/S0/roadmap.md` | Fechas detalladas S0-S3 |
| | TOOLING_DECISIONS.md | `docs/01-sprint/S0/TOOLING_DECISIONS.md` | Justificación de versiones (TS 5.3.3, oasdiff 1.10.10) |
| | MOCKS-SETUP.md | `docs/01-sprint/S0/MOCKS-SETUP.md` | Configuración Prism/WireMock |
| **S1** | Contratos Core | `docs/01-sprint/S1/` | |
| | errors.md | `docs/01-sprint/S1/errors.md` | Catálogo canónico de error codes |
| | CONTRACTS-GUIDE.md | `docs/01-sprint/S1/CONTRACTS-GUIDE.md` | Guía de diseño de contratos |
| | CHANGE-POLICY.md | `docs/01-sprint/S1/CHANGE-POLICY.md` | **Política única**: FREEZE, Deprecation, Emergency RFC |
| **S2** | Validación & Baselines | `docs/01-sprint/S2/` | |
| | PERFORMANCE_BASELINES.md | `docs/01-sprint/S2/PERFORMANCE_BASELINES.md` | Métricas: p95 100ms (runtime), 1.2s (CI pack) |
| | BASELINE_STRATEGY.md | `docs/01-sprint/S2/BASELINE_STRATEGY.md` | Proceso de firma y rotación |
| | DRIFT-DETECTION.md | `docs/01-sprint/S2/DRIFT-DETECTION.md` | Contract drift detection (runtime vs spec) |
| | runbook-baseline-rollback.md | `docs/01-sprint/S2/runbook-baseline-rollback.md` | Playbook de rollback de baseline |
| **S3** | SDK Alpha | `docs/01-sprint/S3/` | |
| | SDK-BENCHMARKS.md | `docs/01-sprint/S3/SDK-BENCHMARKS.md` | Benchmarks Py ≤30s, TS ≤25s |
| | runbook-sdk-smoke.md | `docs/01-sprint/S3/runbook-sdk-smoke.md` | Smoke tests determinísticos |
| | SDK-INTERNAL-POLICY.md | `docs/01-sprint/S3/SDK-INTERNAL-POLICY.md` | Anti-leak policy (solo registry privado) |
| **S4** | Governance | `docs/01-sprint/S4/` | |
| | RACI.md | `docs/01-sprint/S4/RACI.md` | Nombres reales + backups (CA, Sec, DX, Release) |
| | CODEOWNERS | `docs/01-sprint/S4/CODEOWNERS` | Ownership por carpeta |
| | RFC_TEMPLATE.md | `docs/01-sprint/S4/RFC_TEMPLATE.md` | Template con sección EMERGENCY RFC |
| **S5** | Troubleshooting | `docs/01-sprint/S5/` | |
| | cookbooks/ | `docs/01-sprint/S5/cookbooks/{py,ts,go,java,dotnet}/` | Cookbooks por stack |
| | runbooks/ | `docs/01-sprint/S5/runbooks/` | Runbooks operacionales |
| **S6** | Security | `docs/01-sprint/S6/` | |
| | SEC-README.md | `docs/01-sprint/S6/SEC-README.md` | Evidencias de seguridad auto-generadas |
| | SECURITY_ARCHITECTURE.md | `docs/01-sprint/S6/SECURITY_ARCHITECTURE.md` | Retención, cifrado, key rotation |
| | WAIVER-POLICY.md | `docs/01-sprint/S6/WAIVER-POLICY.md` | Política de excepciones High/Critical |
| **S7** | Pact Testing | `docs/01-sprint/S7/` | |
| | PACT-POLICY.md | `docs/01-sprint/S7/PACT-POLICY.md` | can-i-deploy como gate obligatorio |
| | PACT-MATRIX.md | `docs/01-sprint/S7/PACT-MATRIX.md` | Matrix consumers/providers |
| **S8** | Mocks Vivos | `docs/01-sprint/S8/` | |
| | MOCKS-LIFECYCLE.md | `docs/01-sprint/S8/MOCKS-LIFECYCLE.md` | Ciclo de vida y auto-regeneración |
| | MOCKS-HEALTH.md | `docs/01-sprint/S8/MOCKS-HEALTH.md` | Health badges y alertas |
| **S9** | On-call 2.0 | `docs/01-sprint/S9/` | |
| | ALERTING-KPIS.md | `docs/01-sprint/S9/ALERTING-KPIS.md` | MTTR <30min, drift ≤0.5%, lint budget=0 |
| | runbook-timeouts.md | `docs/01-sprint/S9/runbook-timeouts.md` | Investigación de timeouts |
| | runbook-pact-red.md | `docs/01-sprint/S9/runbook-pact-red.md` | Pact failures |
| **S10** | CLI & Audit Prep | `docs/01-sprint/S10/` | |
| | CLI-REFERENCE.md | `docs/01-sprint/S10/CLI-REFERENCE.md` | Referencia completa de comandos |
| | AUDIT-EVIDENCE-GUIDE.md | `docs/01-sprint/S10/AUDIT-EVIDENCE-GUIDE.md` | Qué se recolecta, dónde, retención |
| **S11** | SDKs Enterprise | `docs/01-sprint/S11/` | |
| | SDK-COMPATIBILITY-MATRIX.md | `docs/01-sprint/S11/SDK-COMPATIBILITY-MATRIX.md` | Feature parity por SDK |
| **S12** | Macro-Módulos | `docs/01-sprint/S12/` | |
| | ACTAS-VALIDACION-ASM.md | `docs/01-sprint/S12/ACTAS-VALIDACION-ASM.md` | Acta firmada ASM |
| | ACTAS-VALIDACION-CGN.md | `docs/01-sprint/S12/ACTAS-VALIDACION-CGN.md` | Acta firmada CGN |
| | ACTAS-VALIDACION-AWE.md | `docs/01-sprint/S12/ACTAS-VALIDACION-AWE.md` | Acta firmada AWE |
| | ACTAS-VALIDACION-SHIF.md | `docs/01-sprint/S12/ACTAS-VALIDACION-SHIF.md` | Acta firmada SHIF |
| | INTERREPO-READINESS.md | `docs/01-sprint/S12/INTERREPO-READINESS.md` | Estado de dependencias inter-repo |
| **S13** | Customer Beta | `docs/01-sprint/S13/` | |
| | BETA-FEEDBACK-TEMPLATE.md | `docs/01-sprint/S13/BETA-FEEDBACK-TEMPLATE.md` | Template de feedback |
| | BETA-REPORT.md | `docs/01-sprint/S13/BETA-REPORT.md` | Informe consolidado |
| **S14** | Compliance Pack | `docs/01-sprint/S14/` | |
| | COMPLIANCE-CONTROLS-MAP.md | `docs/01-sprint/S14/COMPLIANCE-CONTROLS-MAP.md` | Mapeo de evidencias con hash/firma/fuente |
| | compliance-pack.zip | `docs/01-sprint/S14/compliance-pack.zip` | Pack exportable |
| **S15** | GA Gate | `docs/01-sprint/S15/` | |
| | GA-CHECKLIST.md | `docs/01-sprint/S15/GA-CHECKLIST.md` | Checklist 100+ ítems |
| | RELEASE-NOTES-v1.0.0.md | `docs/01-sprint/S15/RELEASE-NOTES-v1.0.0.md` | Release notes completas |
| | MIGRATION-GUIDE-1.0.0.md | `docs/01-sprint/S15/MIGRATION-GUIDE-1.0.0.md` | Guía de migración |
| **S16** | Optimización | `docs/01-sprint/S16/` | |
| | PERFORMANCE-10X-PLAN.md | `docs/01-sprint/S16/PERFORMANCE-10X-PLAN.md` | Plan de optimización 10x |
| **S17** | MCP Discovery | `docs/01-sprint/S17/` | Post-GA |
| | MCP-OVERVIEW.md | `docs/01-sprint/S17/MCP-OVERVIEW.md` | Visión general MCP |
| | MCP-CONTRACTS.md | `docs/01-sprint/S17/MCP-CONTRACTS.md` | Contratos MCP |
| | MCP-SECURITY.md | `docs/01-sprint/S17/MCP-SECURITY.md` | mTLS, JWT scopes |
| **S18** | MCP SDKs | `docs/01-sprint/S18/` | Post-GA |
| | MCP-SDK-ADAPTERS.md | `docs/01-sprint/S18/MCP-SDK-ADAPTERS.md` | Adapters Py/TS |
| | MCP-GOVERNANCE.md | `docs/01-sprint/S18/MCP-GOVERNANCE.md` | Governance MCP |
| **S19** | MCP Pilots | `docs/01-sprint/S19/` | Post-GA |
| | MCP-PILOT-PLAN.md | `docs/01-sprint/S19/MCP-PILOT-PLAN.md` | Plan de pilotos |
| | MCP-HARDENING.md | `docs/01-sprint/S19/MCP-HARDENING.md` | Security hardening |
| | MCP-OBSERVABILITY.md | `docs/01-sprint/S19/MCP-OBSERVABILITY.md` | Observabilidad MCP |

---

## 🔗 Diagrama de Dependencias entre Sprints

### **Cadena Crítica (Bloqueantes)**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    AGENT-CONTRACTS - Sprint Dependencies                │
└─────────────────────────────────────────────────────────────────────────┘

CADENA CRÍTICA (S0→S1→S2→S3):
┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐
│  S0  │─────►│  S1  │─────►│  S2  │─────►│  S3  │
└──┬───┘      └──┬───┘      └──┬───┘      └──┬───┘
   │             │             │             │
   │ Tooling     │ Contracts   │ Baseline    │ SDKs Alpha
   │ Mocks       │ Schemas     │ Validation  │ Examples
   │ CI/CD       │ Protos      │ Drift       │ Benchmarks
   │             │             │             │
   └─────────────┴─────────────┴─────────────┴─────► Habilita S7, S8, S10

GOVERNANCE & OBSERVABILITY (Paralelo desde S4):
   ┌──────┐      ┌──────┐
   │  S4  │─────►│  S5  │
   └──────┘      └──────┘
   Governance    Observabilidad
   RACI          SLOs, Dashboards

SECURITY (Secuencial desde S6):
   ┌──────┐
   │  S6  │──► Habilita gates bloqueantes S7+
   └──────┘
   SBOM, Firmas
   Waiver Policy

CONTRACT TESTING (Requiere S0 + S1):
   ┌──────┐      ┌──────┐
   │  S7  │─────►│  S8  │
   └──────┘      └──────┘
   Pact Formal   Mocks Vivos
   can-i-deploy  Health

TROUBLESHOOTING & CLI (Requiere S3 + S7):
   ┌──────┐      ┌──────┐
   │  S9  │─────►│ S10  │
   └──────┘      └──────┘
   On-call 2.0   CLI MVP
   Runbooks      Audit Prep

ENTERPRISE SDKs (Paralelo desde S11):
   ┌──────┐      ┌──────┐
   │ S11  │      │ S12  │
   └──────┘      └──┬───┘
   Go/Java/.NET     │ Macro-Módulos
                    │ Sign-off ⚠️ BLOQUEANTE
                    ▼
                 Habilita S13

GA PATH (Secuencial crítico):
   ┌──────┐      ┌──────┐      ┌──────┐
   │ S13  │─────►│ S14  │─────►│ S15  │
   └──────┘      └──────┘      └──────┘
   Beta          Compliance    GA Gate ⚠️
   Customer      Pack          Checklist 100+

OPTIMIZATION (Post-GA):
   ┌──────┐
   │ S16  │──► v2.0 Discovery
   └──────┘

MCP PATH (Opcional Post-GA):
   ┌──────┐      ┌──────┐      ┌──────┐
   │ S17  │─────►│ S18  │─────►│ S19  │
   └──────┘      └──────┘      └──────┘
   MCP Spike     SDK Adapters  Pilots
```

### **Dependencias Detalladas**

| Sprint | Depende de (Bloqueantes) | Habilita | Paralelo con | Criticidad |
|--------|--------------------------|----------|--------------|------------|
| **S0** | - | S1, S4, S5 | - | 🔴 CRÍTICO (kickoff) |
| **S1** | S0 | S2, S7, S8 | S4, S5 | 🔴 CRÍTICO (contratos) |
| **S2** | S1 | S3 | S4, S5 | 🔴 CRÍTICO (validación) |
| **S3** | S2 | S7, S9, S10 | S4, S5, S6 | 🔴 CRÍTICO (SDKs) |
| **S4** | S0 | S5 | S1, S2, S3, S6 | 🟡 IMPORTANTE (governance) |
| **S5** | S4 | - | S1-S6 | 🟡 IMPORTANTE (observabilidad) |
| **S6** | S3 | S7+ (gates bloqueantes) | S4, S5 | 🔴 CRÍTICO (seguridad) |
| **S7** | S1, S3, S6 | S8, S10 | S9 | 🔴 CRÍTICO (Pact) |
| **S8** | S7 | S9, S10 | - | 🟡 IMPORTANTE (mocks) |
| **S9** | S3, S7 | S10 | S8 | 🟡 IMPORTANTE (troubleshooting) |
| **S10** | S3, S7, S9 | S11 | S12 | 🟡 IMPORTANTE (CLI + audit) |
| **S11** | S3 | S13 | S12 | 🟢 NORMAL (SDKs enterprise) |
| **S12** | S1, S2 | S13 | S11 | 🔴 CRÍTICO (macro-módulos) |
| **S13** | S11, S12 | S14 | - | 🔴 CRÍTICO (beta) |
| **S14** | S13, S6 (evidencias) | S15 | - | 🔴 CRÍTICO (compliance) |
| **S15** | S14, TODOS los anteriores | S16, v1.0.0 GA | - | 🔴 CRÍTICO (GA gate) |
| **S16** | S15 (GA) | v2.0 Discovery | - | 🟢 NORMAL (optimización) |
| **S17** | S15 (GA) | S18 | - | 🟢 OPCIONAL (MCP) |
| **S18** | S17 | S19 | - | 🟢 OPCIONAL (MCP SDKs) |
| **S19** | S18 | - | - | 🟢 OPCIONAL (MCP pilots) |

### **Bloqueadores Críticos (⚠️ Atención)**

| Sprint | Bloqueador | Impacto si Falla | Mitigación |
|--------|-----------|------------------|------------|
| **S0** | Secrets no disponibles (Pact, Slack, Cosign) | Bloquea S7 (Pact), S6 (firmas) | Checklist en `docs/01-sprint/S0/README-Kickoff.md` - verificar HOY |
| **S1** | Contratos incompletos o con breaking | Bloquea S2 (baseline), S3 (SDKs) | Reviews obligatorios con Tech Leads |
| **S6** | Key compromise o SBOM faltante | Bloquea releases | Key rotation playbook + HSM |
| **S12** | Sign-off de macro-módulos rechazado | Bloquea S13, S14, S15 (GA) | Sesiones de validación calendarizadas |
| **S15** | GA checklist no 100% | Bloquea v1.0.0 | Ritual semanal desde S13 |

---

## 🏗️ CONTEXTO ARQUITECTÓNICO Y ALCANCE

### **Ubicación de Agent Contracts en ENIS v3.0**

Agent Contracts es uno de **24 repositorios** que conforman ENIS v3.0 (DNA Compliant). Su rol es actuar como **Source of Truth centralizado** para todos los contratos de APIs, schemas y protocolos entre servicios.

### **Responsabilidades CORE**

**SÍ hace (este repo)**:
1. ✅ **OpenAPI 3.0 Specifications**: Definir todos los contratos HTTP REST para servicios ENIS
2. ✅ **JSON Schemas**: Validación de payloads, agent registration, policies, events
3. ✅ **Protocol Buffers**: Contratos para gRPC y streaming de alta performance
4. ✅ **SDK Multi-lenguaje**: Generar, firmar y publicar SDKs (Python/TS/Go/Java/.NET)
5. ✅ **Validation Engine**: Detectar breaking changes automáticamente (oasdiff, buf, ajv)
6. ✅ **Baseline Firmado**: BLAKE2b + Cosign para garantizar integridad
7. ✅ **SBOM & Supply Chain**: Generar SBOM CycloneDX, firmas Sigstore
8. ✅ **Contract Testing**: Pact consumer-driven contracts con providers
9. ✅ **Compatibility Matrix**: Matriz automatizada de versiones compatibles
10. ✅ **Developer Experience**: CLI, ejemplos ejecutables, templates

**NO hace (delegado a otros repos)**:
1. ❌ **Implementación de Servicios**: Los servicios implementan estos contratos, no este repo
2. ❌ **Runtime Validation**: Delegado a cada servicio (con SDKs generados)
3. ❌ **API Gateway**: Delegado a Integration & APIs Service
4. ❌ **Authentication/Authorization**: Delegado a cada servicio (contratos definidos aquí)
5. ❌ **Observabilidad Runtime**: Delegado a Observability Service (contratos definidos aquí)
6. ❌ **Deployment**: Delegado a Cloud Infrastructure y servicios individuales

### **Conexiones Críticas (Consumers de Contratos)**

```yaml
agent_contracts_consumers:
  edge:
    - consumer: "NOPS Kernel"
      artifacts: ["nops.yaml OpenAPI", "events.proto", "agent-registration.json"]
      uso: "Contratos para event bus, state management, agent lifecycle"
      sdk: "Python SDK"
      criticality: "🔴 CRITICAL"
    
    - consumer: "Edge Agents (5 tipos)"
      artifacts: ["agents.yaml OpenAPI", "agent-config.json schema"]
      uso: "Contratos para registro, capabilities, configuración"
      sdk: "Python SDK + TypeScript SDK"
      criticality: "🔴 CRITICAL"
  
  cloud_core:
    - consumer: "Inference Service"
      artifacts: ["inference.yaml OpenAPI", "inference-request.json"]
      uso: "Contratos para routing LLM, streaming, prompt resolution"
      sdk: "Python SDK"
      criticality: "🔴 CRITICAL"
    
    - consumer: "ASM Service"
      artifacts: ["asm.yaml OpenAPI", "state-schema.json"]
      uso: "Contratos para Adaptive State Management"
      sdk: "Python SDK + Go SDK"
      criticality: "🔴 CRITICAL"
    
    - consumer: "CGN Service"
      artifacts: ["cgn.yaml OpenAPI", "graph-schema.json"]
      uso: "Contratos para Causal Graph Navigation"
      sdk: "Python SDK + Go SDK"
      criticality: "🟡 MEDIUM"
    
    - consumer: "AWE Service"
      artifacts: ["awe.yaml OpenAPI", "workflow-schema.json"]
      uso: "Contratos para Autonomous Workflow Evolution"
      sdk: "Python SDK + Go SDK"
      criticality: "🟡 MEDIUM"
    
    - consumer: "SHIF Service"
      artifacts: ["shif.yaml OpenAPI", "integration-schema.json"]
      uso: "Contratos para System-Human Integration Fabric"
      sdk: "Python SDK + Java SDK"
      criticality: "🟡 MEDIUM"
    
    - consumer: "Voice Interface Service"
      artifacts: ["voice-integration.yaml OpenAPI"]
      uso: "Contratos para STT/TTS integration"
      sdk: "TypeScript SDK"
      criticality: "🟡 MEDIUM"
    
    - consumer: "XR Interface Service"
      artifacts: ["xr-integration.yaml OpenAPI"]
      uso: "Contratos para OpenXR integration"
      sdk: "TypeScript SDK + .NET SDK"
      criticality: "🟡 MEDIUM"
    
    - consumer: "Observability Service"
      artifacts: ["events.proto", "metrics-schema.json"]
      uso: "Contratos para telemetry y métricas"
      sdk: "Go SDK"
      criticality: "🔴 CRITICAL"
    
    - consumer: "Billing Service"
      artifacts: ["billing.yaml OpenAPI", "cost-event.json"]
      uso: "Contratos para cost attribution"
      sdk: "Python SDK + Java SDK"
      criticality: "🔴 CRITICAL"
    
    - consumer: "Compliance Service"
      artifacts: ["compliance.yaml OpenAPI", "audit-trail.json"]
      uso: "Contratos para audit trail y compliance"
      sdk: "Go SDK + Java SDK"
      criticality: "🔴 CRITICAL"
  
  platform:
    - consumer: "Agent Marketplace"
      artifacts: ["marketplace-api.yaml", "agent-package.json"]
      uso: "Contratos para publicación y distribución de agents"
      sdk: "TypeScript SDK + Python SDK"
      criticality: "🟡 MEDIUM"
    
    - consumer: "ENIS Studio"
      artifacts: ["studio-api.yaml", "agent-definition.json"]
      uso: "Contratos para IDE y desarrollo de agents"
      sdk: "TypeScript SDK"
      criticality: "🟡 MEDIUM"
    
    - consumer: "Developer Portal"
      artifacts: ["ALL OpenAPI specs", "ALL JSON Schemas"]
      uso: "Documentación interactiva y ejemplos"
      sdk: "TypeScript SDK"
      criticality: "🔴 CRITICAL (docs)"

  external_partners:
    - consumer: "Third-party Agent Developers"
      artifacts: ["Public APIs", "SDKs oficiales"]
      uso: "Desarrollo de agents de terceros"
      sdks: "Python, TypeScript, Go, Java, .NET"
      criticality: "🔴 CRITICAL (ecosistema)"
```

### **Arquitectura de 24 Repos (resumen)**

> **Referencia**: Master Prompt 30 - Arquitectura ENIS v3.0 DNA Compliant  
> **Documentación completa**: `docs/00-enis-complete/MASTER_PROMPT_30_ARQUITECTURA.md`

```yaml
enis_v3_repos:
  edge: 3
    - nops-kernel (control plane slim)
    - edge-agents (5 tipos: Zero/Shared/Lite/Enterprise/Air-Gapped)
    - edge-infrastructure (K3s/Podman, monitoring edge)
  
  cloud_core: 15
    macro_modules: 4
      - asm-service (Adaptive State Manager)
      - cgn-service (Causal Graph Navigator)
      - awe-service (Autonomous Workflow Evolution)
      - shif-service (System-Human Integration Fabric)
    
    inference: 1
      - inference-service (orchestrator LLMs + composición)
    
    interfaces: 2
      - voice-interface-service (STT/VAD/TTS/WebRTC)
      - xr-interface-service (OpenXR/Spatial/Gesture/Render)
    
    nops_modules: 7
      - observability-service (Prometheus/Grafana/Jaeger/Tempo)
      - scorecard-service (SLA tracking, quality metrics)
      - billing-service (cost attribution, showback, FinOps)
      - sandbox-service (mocks, testing environments)
      - compliance-service (audit storage 10+ años, GDPR/CCPA)
      - rgm-service (Resource Governance Module - fairness/quotas)
      - alm-service (Agent Lifecycle Manager - deploy/rollback)
    
    governance: 1
      - data-governance-service (DGE - PII/PHI/PCI classification/redaction)
  
  platform: 3
    - agent-marketplace (público/privado)
    - enis-studio (UI/IDE para crear agents)
    - developer-portal (docs, API refs, SDKs)
  
  cloud_ops: 2
    - cloud-infrastructure (IaC: EKS/GKE/AKS, PKI, WAF, SIEM)
    - enis-infrastructure (cross-cutting: DNS, CDN, secrets management)
  
  shared: 1
    - agent-contracts (👈 ESTE REPO - schemas OpenAPI/Protobuf/JSON Schema, SDKs)
```

### **Mapa Visual de Dependencias entre Repositorios**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        ENIS v3.0 - 24 Repositorios                       │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────── EDGE (3 repos) ────────────────┐
│                                                 │
│  ┌──────────────┐      ┌─────────────┐        │
│  │ NOPS Kernel  │◄─────│ Edge Agents │        │
│  └──────┬───────┘      └──────┬──────┘        │
│         │                     │                │
│         └──────────┬──────────┘                │
│                    │                           │
│         ┌──────────▼────────────┐              │
│         │ Edge Infrastructure   │              │
│         └───────────────────────┘              │
└─────────────────┬───────────────────────────────┘
                  │
                  │ Events, State, Metrics
                  │
┌─────────────────▼─────────────────────────────────────────────────────┐
│                    CLOUD CORE (15 repos)                               │
│                                                                         │
│  ┌─────────────────┐        ┌──────────────── Macro-Modules (4) ───┐ │
│  │ Inference       │◄───────┤  ASM │ CGN │ AWE │ SHIF              │ │
│  │ Service         │        └────────────────────────────────────────┘ │
│  └────────┬────────┘                                                   │
│           │                                                             │
│           ├──────► Observability ──► Scorecard ──► Billing             │
│           ├──────► Compliance ──────► RGM ─────────► ALM               │
│           ├──────► Sandbox (mocks, testing)                            │
│           └──────► Data Governance (DGE - PII/PHI/PCI)                 │
│                                                                         │
│  ┌─────────────── Interfaces (2) ────────────┐                        │
│  │  Voice Interface  │  XR Interface          │                        │
│  └────────────────────────────────────────────┘                        │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────── PLATFORM (3 repos) ──────────────────────┐
│  Agent Marketplace │ ENIS Studio │ Developer Portal         │
└──────────────────────────────────────────────────────────────┘

┌─────────────────── CLOUD OPS (2 repos) ─────────────────────┐
│  Cloud Infrastructure │ ENIS Infrastructure                 │
└──────────────────────────────────────────────────────────────┘

┌─────────────────── SHARED (1 repo) ─────────────────────────┐
│               🎯 AGENT-CONTRACTS (THIS REPO)                 │
│  Consumed by: ALL 23 repos above for contracts & SDKs       │
└──────────────────────────────────────────────────────────────┘
```

### **Cross-References a Documentación de Arquitectura**

| Documento | Ubicación | Propósito |
|-----------|-----------|-----------|
| **Master Prompt 30** | `docs/00-enis-complete/MASTER_PROMPT_30_ARQUITECTURA.md` | Arquitectura completa ENIS v3.0 DNA Compliant |
| **DNA v3.0 Spec** | `docs/00-enis-complete/DNA_V3_SPECIFICATION.md` | Especificación técnica DNA v3.0 |
| **24 Repos Overview** | `docs/00-enis-complete/ENIS_24_REPOS_OVERVIEW.md` | Descripción detallada de todos los repositorios |
| **Agent Contracts Integration** | `docs/00-enis-complete/05-repositorios-enis/shared/AGENT_CONTRACTS_INTEGRATION.md` | Integración con servicios consumidores |
| **API Design Guidelines** | `docs/01-sprint/S1/CONTRACTS-GUIDE.md` | Guía de diseño de contratos OpenAPI/Proto |
| **Security Architecture** | `docs/01-sprint/S6/SECURITY_ARCHITECTURE.md` | Arquitectura de seguridad y compliance |

### **Matriz de Contratos v1.x Target**

| Categoría | Contratos | Total | Prioridad |
|-----------|-----------|-------|-----------|
| **Core APIs** | inference, agents, events, nops, federation | 5 | 🔴 S0-S2 |
| **Macro-Módulos** | asm, cgn, awe, shif | 4 | 🔴 S12 |
| **NOPS Modules** | observability, billing, compliance, scorecard, lifecycle, rgm, sandbox | 7 | 🟡 S9-S14 |
| **Interfaces** | voice-integration, xr-integration | 2 | 🟡 S16-S17 |
| **Platform** | marketplace-api, studio-api | 2 | 🟢 Post-GA |
| **JSON Schemas** | agent-registration, inference-request, event, policy, validation-rules, compatibility-matrix, migration-guides | 8+ | 🔴 S1-S4 |
| **Protobuf** | inference.proto, agents.proto, events.proto, federation.proto | 4 | 🔴 S1-S2 |
| **SDKs** | Python, TypeScript, Go, Java, .NET | 5 | 🔴 S3-S13 |

---

---

## S0 — Kickoff & Repo Bootstrap ⏸️ **PLANIFICADO**

> **Estado**: ⏸️ **PENDIENTE**  
> **Branch**: `feature/s0-kickoff-bootstrap`  
> **Duración estimada**: 1-2 semanas  
> **Owner**: Contract Architect + Platform Engineer

### Meta
- Repo production-ready con CI/CD completo y estructura lista para contratos.

### Entregables

#### **1. Estructura de Monorepo**
```bash
agent-contracts/
├── openapi/v1/              # OpenAPI 3.0 specifications
│   ├── inference.yaml
│   ├── agents.yaml
│   ├── events.yaml
│   ├── nops.yaml
│   └── .baseline/           # Baseline hashes para breaking detection
├── schemas/                 # JSON Schemas
│   ├── agent-registration.json
│   ├── inference-request.json
│   ├── event-schema.json
│   └── policy-schema.json
├── proto/                   # Protocol Buffers
│   ├── inference.proto
│   ├── agents.proto
│   ├── events.proto
│   └── federation.proto
├── sdks/                    # SDKs generados
│   ├── python/
│   ├── typescript/
│   ├── go/
│   ├── java/
│   └── dotnet/
├── scripts/                 # Automatización
│   ├── validate/
│   │   ├── validate-openapi.sh
│   │   ├── validate-json-schema.sh
│   │   └── validate-proto.sh
│   ├── breaking/
│   │   ├── detect-openapi-breaking.py
│   │   └── detect-proto-breaking.sh
│   ├── baseline/
│   │   ├── compute-baseline.py
│   │   └── verify-baseline.py
│   ├── examples/
│   │   └── run-all-examples.sh
│   └── bench/
│       └── validation-bench.py
├── tests/                   # Testing completo
│   ├── contracts/
│   │   ├── test_openapi_contract.py
│   │   └── test_schema_validation.py
│   ├── examples/
│   │   └── test_examples_smoke.py
│   └── pact/
│       └── test_pact_consumer.py
├── docs/                    # Documentación
│   ├── guides/
│   │   ├── quickstart.md
│   │   └── versioning.md
│   ├── examples/
│   │   ├── agent-registration-example.md
│   │   └── inference-request-example.md
│   ├── troubleshooting/
│   │   └── contract-validation-errors.md
│   └── benchmarks/
│       └── validation_bench.md
├── .github/
│   └── workflows/
│       ├── contracts-validate.yml
│       ├── contracts-breaking.yml
│       ├── contracts-baseline.yml
│       ├── sdks-build.yml
│       └── examples-smoke.yml
├── .pre-commit-config.yaml
├── docker-compose.dev.yml
├── Dockerfile
├── Makefile
├── README.md
├── CONTRIBUTING.md
├── CODEOWNERS
└── LICENSE
```

#### **2. GitHub Actions Workflows**

**contracts-validate.yml**:
```yaml
name: Validate Contracts
on: [pull_request, push]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate OpenAPI with Spectral
        run: spectral lint openapi/v1/*.yaml
      - name: Validate JSON Schemas with AJV
        run: ajv validate -s schemas/*.json
      - name: Validate Protos with Buf
        run: buf lint proto/
      - name: TypeScript Compile Check
        run: tsc --noEmit
```

#### **3. Pre-commit Hooks**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/stoplightio/spectral
    rev: v6.11.0
    hooks:
      - id: spectral
        files: \.(yaml|yml)$
        args: ['lint']
  
  - repo: local
    hooks:
      - id: ajv-validate
        name: Validate JSON Schemas
        entry: ajv validate
        language: node
        files: \.json$
      
      - id: buf-lint
        name: Lint Protocol Buffers
        entry: buf lint
        language: golang
        files: \.proto$
```

#### **4. Docker Multi-stage < 500MB**
```dockerfile
# Dockerfile
FROM node:20-alpine AS validator
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run validate

FROM alpine:3.19
WORKDIR /contracts
COPY --from=validator /app/openapi /contracts/openapi
COPY --from=validator /app/schemas /contracts/schemas
COPY --from=validator /app/proto /contracts/proto
HEALTHCHECK CMD ["sh", "-c", "test -f /contracts/openapi/v1/inference.yaml"]
CMD ["tail", "-f", "/dev/null"]
```

#### **5. Tooling**
- **Spectral** 6.11.0: OpenAPI linting con reglas DNA v3.0
- **AJV** 8.12.0: JSON Schema validation estricta
- **Buf** 1.28.1: Protocol Buffer linting y breaking detection
- **TypeScript** 5.3.3: Type checking para SDKs TypeScript
- **oasdiff** 1.10.10: OpenAPI breaking change detection
- **Cosign** 2.2.2: Firmado de artefactos
- **Syft** 0.99.0: SBOM generation

### DoD (Definition of Done)

- [ ] **Pipeline < 5 minutos**: CI/CD completo en < 5min
- [ ] **`docker-compose up` < 2 minutos**: Inicialización rápida
- [ ] **Validadores operacionales**: spectral, ajv, buf, tsc funcionando
- [ ] **Baseline firmado**: Artefacto `baseline.b2` generado y firmado con Cosign
- [ ] **Pre-commit hooks**: Instalados y funcionando en local
- [ ] **Documentación base**: README, CONTRIBUTING, Makefile completados
- [ ] **CODEOWNERS**: Definidos owners por directorio
- [ ] **Branch protection**: Main protegida (require PR + reviews)

### Smoke Tests a Ejecutar

```bash
# 1. Pre-commit validation
pre-commit run --all-files

# 2. OpenAPI validation
spectral lint openapi/v1/*.yaml

# 3. JSON Schema validation
ajv validate -s schemas/*.json

# 4. Proto validation
buf lint proto/

# 5. TypeScript check
tsc --noEmit

# 6. Docker build
docker build -t enis/agent-contracts:dev .

# 7. Docker Compose
docker-compose up -d --build
docker-compose ps  # Should show healthy

# 8. Baseline generation
python scripts/baseline/compute-baseline.py --write
python scripts/baseline/verify-baseline.py
```

### Versiones Tecnológicas Target

| Componente | Versión | Justificación |
|------------|---------|---------------|
| Spectral | 6.11.0 | Latest stable OpenAPI linter |
| AJV | 8.12.0 | JSON Schema Draft 2020-12 support |
| Buf | 1.28.1 | Protocol Buffer tooling estándar |
| TypeScript | 5.3.3 | Latest LTS con decorators stage 3 |
| oasdiff | 1.10.10 | Breaking change detection precisa |
| Cosign | 2.2.2 | Sigstore signing de artefactos |
| Syft | 0.99.0 | SBOM CycloneDX generation |
| Node.js | 20 LTS | SDK TypeScript build |
| Python | 3.11 | SDK Python build |
| Go | 1.21 | SDK Go build + Buf tooling |

### 🔍 Gaps Identificados y Mejoras

#### ➕ Agregar

1. **`tools/versions.json`** como fuente de verdad única
   - Versiones canónicas: TypeScript 5.3.3, Spectral 6.11.0, oasdiff 1.10.10, Buf 1.28.1, Cosign 2.2.2, Syft 0.99.0
   - Justificar desviaciones en `docs/TOOLING_DECISIONS.md`
   - Script `tools/check-versions.sh` para validación

2. **Pact Broker** (coordinado con cloud-ops)
   - URL interna + credenciales en GitHub Secrets
   - Canal Slack `#contracts-rfcs` para decisiones de governance
   - Ejemplo dummy de contrato publicado para validar conectividad

3. **Seed de mocks tempranos**
   - Prism (Inference Service): `contracts/mocks/prism/config.yaml`
   - WireMock (NOPS Kernel): `contracts/mocks/wiremock/mappings/`
   - Healthchecks en `docker-compose.dev.yml` con retry logic

4. **Security scanning inicial** (modo informativo, no bloqueante)
   - Semgrep + Trivy en workflow `.github/workflows/security-scan.yml`
   - Dashboard de vulnerabilidades en modo monitor
   - Preparación para gates bloqueantes en S6

5. **Calendario con fechas exactas**
   - `KICKOFF_DATE` definido: 2025-10-14
   - Sprints bisemanales hasta 2026-09-30
   - Milestones con fechas target en `docs/ROADMAP_DATES.md`

#### 🔧 Modificar

- **README.md**: Aclarar diferencia entre "spec production-ready" (S1-S2) vs "GA operativo" (S15)
- **Makefile**: Agregar comando `make check-versions` que valida contra `tools/versions.json`

#### 📦 Artefactos Adicionales (Rutas Estandarizadas)

```
tools/versions.json                            # Source of Truth de versiones
tools/check-versions.sh                         # Script de validación
.github/workflows/security-scan.yml             # Security scanning (informativo)
.github/workflows/contracts-ci.yml              # CI con gate check-versions
contracts/mocks/prism/config.yaml              # Mock Inference Service
contracts/mocks/wiremock/mappings/             # Mock NOPS Kernel
docker-compose.mocks.yml                       # Compose para mocks
docs/01-sprint/S0/README-Kickoff.md           # Checklist: secrets, setup, smoke
docs/01-sprint/S0/roadmap.md                   # Fechas detalladas S0-S3
docs/01-sprint/S0/TOOLING_DECISIONS.md        # Justificación TS 5.3.3, oasdiff 1.10.10
docs/01-sprint/S0/MOCKS-SETUP.md              # Setup Prism/WireMock con healthchecks
```

#### 🔒 Gates Bloqueantes (Nuevos)

1. **`make check-versions`** - Falla PR si hay drift de versiones vs `tools/versions.json`
2. **Mocks healthcheck** - `docker compose ps` debe mostrar todos healthy
3. **Secrets verificados** - Checklist en `README-Kickoff.md`:
   - `PACT_BROKER_BASE_URL`
   - `PACT_BROKER_TOKEN`
   - `SLACK_WEBHOOK_URL`
   - (Opcional) `COSIGN_KEY` para firmas

#### ⚠️ Riesgos & Mitigación

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| **Deriva de versiones** entre desarrolladores | 🔴 Alto | Gate `check-versions` **BLOQUEANTE** en CI |
| **Secrets faltantes** en CI | 🔴 Alto | Checklist obligatorio en `README-Kickoff.md` |
| **Mocks no funcionales** al inicio | 🟡 Medio | Healthchecks + retry logic; fallback a specs directas |
| **Pact Broker no disponible** | 🟡 Medio | Setup en paralelo con cloud-ops; validar en S0 |

#### 👥 Owners

- **Platform Engineer**: CI/CD, mocks, tooling, check-versions gate
- **Contract Architect**: Roadmap dates, RFC channel, governance
- **Security Lead**: Setup de secrets, initial scanning

### Preparado para S1 (Contracts First)
- ✅ Estructura de directorios lista
- ✅ Tooling de validación instalado
- ✅ CI/CD pipelines configurados
- ✅ Pre-commit hooks funcionando
- ✅ Docker compose para desarrollo local
- ✅ `tools/versions.json` como fuente de verdad
- ✅ Mocks seed funcionales con healthchecks
- ✅ Fechas de sprints definidas

---

## S1 — Contracts First (OpenAPI + JSON Schema + Protobuf) ⏸️ **PLANIFICADO**

> **Estado**: ⏸️ **PENDIENTE**  
> **Branch**: `feature/s1-contracts-first`  
> **Duración estimada**: 2-3 semanas  
> **Owner**: Contract Architect + 2 SDK Engineers  
> **Depende de**: S0 completado

### Meta
- Contratos HTTP y streaming; esquemas JSON y protos validados en CI con baseline firmado.

### Entregables

#### **1. OpenAPI 3.0 Specifications (4 specs core)**

**inference.yaml** (Inference Service):
```yaml
openapi: 3.0.3
info:
  title: ENIS Inference Service API
  version: 1.0.0
  description: Routing de LLMs y composición de macro-módulos

servers:
  - url: https://api.enis.io/v1

security:
  - bearerAuth: []
  - mtls: []

paths:
  /inference:
    post:
      summary: Synchronous inference request
      operationId: createInference
      tags: [Inference]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InferenceRequest'
            examples:
              basic:
                summary: Basic inference
                value:
                  messages: [{role: "user", content: "Hello"}]
                  model: "gpt-4"
      responses:
        '200':
          description: Inference response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InferenceResponse'
        '503':
          description: Service unavailable
          
  /inference:stream:
    post:
      summary: Streaming inference (SSE)
      operationId: streamInference
      tags: [Inference]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InferenceRequest'
      responses:
        '200':
          description: SSE stream
          content:
            text/event-stream:
              schema:
                type: string
                description: Server-sent events

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
    mtls:
      type: mutualTLS
  
  schemas:
    InferenceRequest:
      type: object
      required: [messages]
      properties:
        messages:
          type: array
          items:
            $ref: '#/components/schemas/Message'
        model:
          type: string
          enum: [gpt-4, gpt-3.5-turbo, claude-3-opus]
        temperature:
          type: number
          minimum: 0
          maximum: 2
          default: 0.7
        max_tokens:
          type: integer
          minimum: 1
          maximum: 8192
    
    Message:
      type: object
      required: [role, content]
      properties:
        role:
          type: string
          enum: [system, user, assistant]
        content:
          type: string
    
    InferenceResponse:
      type: object
      required: [id, choices, usage]
      properties:
        id:
          type: string
          format: uuid
        choices:
          type: array
          items:
            $ref: '#/components/schemas/Choice'
        usage:
          $ref: '#/components/schemas/Usage'
    
    Choice:
      type: object
      required: [index, message]
      properties:
        index:
          type: integer
        message:
          $ref: '#/components/schemas/Message'
    
    Usage:
      type: object
      required: [prompt_tokens, completion_tokens, total_tokens]
      properties:
        prompt_tokens:
          type: integer
        completion_tokens:
          type: integer
        total_tokens:
          type: integer
```

**agents.yaml** (Agent Registration & Lifecycle):
```yaml
openapi: 3.0.3
info:
  title: ENIS Agents API
  version: 1.0.0
  description: Agent registration, capabilities and lifecycle

paths:
  /agents:
    post:
      summary: Register new agent
      operationId: registerAgent
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: 'schemas/agent-registration.json'
      responses:
        '201':
          description: Agent registered
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AgentRegistrationResponse'
    
    get:
      summary: List agents
      operationId: listAgents
      parameters:
        - name: tier
          in: query
          schema:
            type: string
            enum: [zero, shared, lite, enterprise, air-gapped]
      responses:
        '200':
          description: Agents list
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/AgentMetadata'
  
  /agents/{agent_id}:
    get:
      summary: Get agent details
      operationId: getAgent
      parameters:
        - name: agent_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Agent details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AgentDetails'
    
    patch:
      summary: Update agent configuration
      operationId: updateAgent
      parameters:
        - name: agent_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AgentUpdate'
      responses:
        '200':
          description: Agent updated
    
    delete:
      summary: Deregister agent
      operationId: deregisterAgent
      parameters:
        - name: agent_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '204':
          description: Agent deregistered

components:
  schemas:
    AgentRegistrationResponse:
      type: object
      required: [agent_id, api_key, status]
      properties:
        agent_id:
          type: string
          format: uuid
        api_key:
          type: string
          description: JWT token for agent authentication
        status:
          type: string
          enum: [pending, active, suspended]
        created_at:
          type: string
          format: date-time
    
    AgentMetadata:
      type: object
      required: [agent_id, name, tier, status]
      properties:
        agent_id:
          type: string
          format: uuid
        name:
          type: string
        tier:
          type: string
          enum: [zero, shared, lite, enterprise, air-gapped]
        status:
          type: string
          enum: [active, suspended, offline]
    
    AgentDetails:
      allOf:
        - $ref: '#/components/schemas/AgentMetadata'
        - type: object
          properties:
            capabilities:
              type: array
              items:
                type: string
            version:
              type: string
            last_heartbeat:
              type: string
              format: date-time
    
    AgentUpdate:
      type: object
      properties:
        name:
          type: string
        capabilities:
          type: array
          items:
            type: string
        config:
          type: object
          additionalProperties: true
```

**events.yaml** (Event Bus):
```yaml
openapi: 3.0.3
info:
  title: ENIS Events API
  version: 1.0.0
  description: Event publishing and subscription

paths:
  /events:
    post:
      summary: Publish event
      operationId: publishEvent
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: 'schemas/event-schema.json'
      responses:
        '202':
          description: Event accepted
          content:
            application/json:
              schema:
                type: object
                required: [event_id]
                properties:
                  event_id:
                    type: string
                    format: uuid
```

**nops.yaml** (NOPS Kernel):
```yaml
openapi: 3.0.3
info:
  title: ENIS NOPS Kernel API
  version: 1.0.0
  description: Control plane para edge agents

paths:
  /state/{agent_id}:
    get:
      summary: Get agent state
      operationId: getAgentState
      parameters:
        - name: agent_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Agent state
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AgentState'
    
    put:
      summary: Update agent state
      operationId: updateAgentState
      parameters:
        - name: agent_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/StateUpdate'
      responses:
        '200':
          description: State updated

components:
  schemas:
    AgentState:
      type: object
      required: [agent_id, status, last_updated]
      properties:
        agent_id:
          type: string
          format: uuid
        status:
          type: string
          enum: [running, paused, stopped, error]
        memory:
          type: object
          additionalProperties: true
        context:
          type: object
          additionalProperties: true
        last_updated:
          type: string
          format: date-time
    
    StateUpdate:
      type: object
      properties:
        status:
          type: string
          enum: [running, paused, stopped]
        memory:
          type: object
        context:
          type: object
```

#### **2. JSON Schemas (4 schemas core)**

**schemas/agent-registration.json**:
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://enis.io/schemas/agent-registration.json",
  "title": "Agent Registration",
  "description": "Schema for agent registration payload",
  "type": "object",
  "required": ["name", "tier", "capabilities", "version"],
  "properties": {
    "name": {
      "type": "string",
      "minLength": 3,
      "maxLength": 64,
      "pattern": "^[a-zA-Z0-9-_]+$",
      "description": "Unique agent name"
    },
    "tier": {
      "type": "string",
      "enum": ["zero", "shared", "lite", "enterprise", "air-gapped"],
      "description": "Agent tier"
    },
    "capabilities": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": [
          "text-generation",
          "code-generation",
          "image-analysis",
          "voice-interaction",
          "xr-interaction",
          "workflow-automation",
          "data-analysis"
        ]
      },
      "minItems": 1,
      "uniqueItems": true
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "Semantic version (X.Y.Z)"
    },
    "config": {
      "type": "object",
      "properties": {
        "max_concurrent_tasks": {
          "type": "integer",
          "minimum": 1,
          "maximum": 100,
          "default": 5
        },
        "timeout_seconds": {
          "type": "integer",
          "minimum": 30,
          "maximum": 3600,
          "default": 300
        }
      },
      "additionalProperties": false
    },
    "metadata": {
      "type": "object",
      "additionalProperties": true
    }
  },
  "additionalProperties": false
}
```

**schemas/inference-request.json**:
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://enis.io/schemas/inference-request.json",
  "title": "Inference Request",
  "description": "Schema for inference request payload",
  "type": "object",
  "required": ["messages"],
  "properties": {
    "messages": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/Message"
      },
      "minItems": 1
    },
    "model": {
      "type": "string",
      "enum": ["gpt-4", "gpt-3.5-turbo", "claude-3-opus", "claude-3-sonnet"],
      "default": "gpt-4"
    },
    "temperature": {
      "type": "number",
      "minimum": 0,
      "maximum": 2,
      "default": 0.7
    },
    "max_tokens": {
      "type": "integer",
      "minimum": 1,
      "maximum": 8192,
      "default": 1024
    },
    "stream": {
      "type": "boolean",
      "default": false
    }
  },
  "$defs": {
    "Message": {
      "type": "object",
      "required": ["role", "content"],
      "properties": {
        "role": {
          "type": "string",
          "enum": ["system", "user", "assistant"]
        },
        "content": {
          "type": "string",
          "minLength": 1
        }
      }
    }
  }
}
```

**schemas/event-schema.json**:
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://enis.io/schemas/event-schema.json",
  "title": "ENIS Event",
  "description": "Schema for ENIS event bus events",
  "type": "object",
  "required": ["event_type", "source", "timestamp", "data"],
  "properties": {
    "event_id": {
      "type": "string",
      "format": "uuid"
    },
    "event_type": {
      "type": "string",
      "enum": [
        "agent.registered",
        "agent.deregistered",
        "agent.heartbeat",
        "inference.requested",
        "inference.completed",
        "inference.failed",
        "state.updated",
        "cost.attributed"
      ]
    },
    "source": {
      "type": "string",
      "description": "Service that generated the event"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "data": {
      "type": "object",
      "additionalProperties": true
    },
    "metadata": {
      "type": "object",
      "properties": {
        "correlation_id": {
          "type": "string",
          "format": "uuid"
        },
        "tenant_id": {
          "type": "string"
        }
      }
    }
  }
}
```

**schemas/policy-schema.json**:
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://enis.io/schemas/policy-schema.json",
  "title": "ENIS Policy",
  "description": "Schema for ABAC/RBAC policies",
  "type": "object",
  "required": ["policy_id", "effect", "actions", "resources"],
  "properties": {
    "policy_id": {
      "type": "string",
      "pattern": "^pol_[a-zA-Z0-9]{16}$"
    },
    "effect": {
      "type": "string",
      "enum": ["allow", "deny"]
    },
    "actions": {
      "type": "array",
      "items": {
        "type": "string",
        "pattern": "^[a-z]+:[a-z]+$"
      },
      "examples": [
        ["agents:register", "agents:deregister"],
        ["inference:request", "inference:stream"]
      ]
    },
    "resources": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "examples": [
        ["arn:enis:agents:*"],
        ["arn:enis:inference:tenant-123:*"]
      ]
    },
    "conditions": {
      "type": "object",
      "additionalProperties": true
    }
  }
}
```

#### **3. Protocol Buffers (4 protos)**

**proto/inference.proto**:
```protobuf
syntax = "proto3";

package enis.inference.v1;

option go_package = "github.com/andaon/enis/proto/inference/v1;inferencev1";

service InferenceService {
  rpc CreateInference(InferenceRequest) returns (InferenceResponse);
  rpc StreamInference(InferenceRequest) returns (stream InferenceChunk);
}

message InferenceRequest {
  repeated Message messages = 1;
  string model = 2;
  optional float temperature = 3;
  optional int32 max_tokens = 4;
}

message Message {
  enum Role {
    ROLE_UNSPECIFIED = 0;
    ROLE_SYSTEM = 1;
    ROLE_USER = 2;
    ROLE_ASSISTANT = 3;
  }
  
  Role role = 1;
  string content = 2;
}

message InferenceResponse {
  string id = 1;
  repeated Choice choices = 2;
  Usage usage = 3;
}

message Choice {
  int32 index = 1;
  Message message = 2;
}

message Usage {
  int32 prompt_tokens = 1;
  int32 completion_tokens = 2;
  int32 total_tokens = 3;
}

message InferenceChunk {
  string id = 1;
  string delta = 2;
  bool done = 3;
}
```

**proto/agents.proto**:
```protobuf
syntax = "proto3";

package enis.agents.v1;

option go_package = "github.com/andaon/enis/proto/agents/v1;agentsv1";

service AgentsService {
  rpc RegisterAgent(RegisterAgentRequest) returns (RegisterAgentResponse);
  rpc GetAgent(GetAgentRequest) returns (Agent);
  rpc UpdateAgent(UpdateAgentRequest) returns (Agent);
  rpc DeregisterAgent(DeregisterAgentRequest) returns (google.protobuf.Empty);
  rpc ListAgents(ListAgentsRequest) returns (ListAgentsResponse);
}

enum AgentTier {
  AGENT_TIER_UNSPECIFIED = 0;
  AGENT_TIER_ZERO = 1;
  AGENT_TIER_SHARED = 2;
  AGENT_TIER_LITE = 3;
  AGENT_TIER_ENTERPRISE = 4;
  AGENT_TIER_AIR_GAPPED = 5;
}

enum AgentStatus {
  AGENT_STATUS_UNSPECIFIED = 0;
  AGENT_STATUS_PENDING = 1;
  AGENT_STATUS_ACTIVE = 2;
  AGENT_STATUS_SUSPENDED = 3;
  AGENT_STATUS_OFFLINE = 4;
}

message RegisterAgentRequest {
  string name = 1;
  AgentTier tier = 2;
  repeated string capabilities = 3;
  string version = 4;
  map<string, string> metadata = 5;
}

message RegisterAgentResponse {
  string agent_id = 1;
  string api_key = 2;
  AgentStatus status = 3;
  google.protobuf.Timestamp created_at = 4;
}

message GetAgentRequest {
  string agent_id = 1;
}

message Agent {
  string agent_id = 1;
  string name = 2;
  AgentTier tier = 3;
  AgentStatus status = 4;
  repeated string capabilities = 5;
  string version = 6;
  google.protobuf.Timestamp last_heartbeat = 7;
  map<string, string> metadata = 8;
}

message UpdateAgentRequest {
  string agent_id = 1;
  optional string name = 2;
  repeated string capabilities = 3;
  map<string, string> config = 4;
}

message DeregisterAgentRequest {
  string agent_id = 1;
}

message ListAgentsRequest {
  optional AgentTier tier = 1;
  int32 page_size = 2;
  string page_token = 3;
}

message ListAgentsResponse {
  repeated Agent agents = 1;
  string next_page_token = 2;
}
```

**proto/events.proto**:
```protobuf
syntax = "proto3";

package enis.events.v1;

option go_package = "github.com/andaon/enis/proto/events/v1;eventsv1";

service EventsService {
  rpc PublishEvent(PublishEventRequest) returns (PublishEventResponse);
  rpc SubscribeEvents(SubscribeEventsRequest) returns (stream Event);
}

enum EventType {
  EVENT_TYPE_UNSPECIFIED = 0;
  EVENT_TYPE_AGENT_REGISTERED = 1;
  EVENT_TYPE_AGENT_DEREGISTERED = 2;
  EVENT_TYPE_AGENT_HEARTBEAT = 3;
  EVENT_TYPE_INFERENCE_REQUESTED = 4;
  EVENT_TYPE_INFERENCE_COMPLETED = 5;
  EVENT_TYPE_INFERENCE_FAILED = 6;
  EVENT_TYPE_STATE_UPDATED = 7;
  EVENT_TYPE_COST_ATTRIBUTED = 8;
}

message Event {
  string event_id = 1;
  EventType event_type = 2;
  string source = 3;
  google.protobuf.Timestamp timestamp = 4;
  google.protobuf.Struct data = 5;
  map<string, string> metadata = 6;
}

message PublishEventRequest {
  Event event = 1;
}

message PublishEventResponse {
  string event_id = 1;
}

message SubscribeEventsRequest {
  repeated EventType event_types = 1;
  optional string filter = 2;
}
```

**proto/federation.proto**:
```protobuf
syntax = "proto3";

package enis.federation.v1;

option go_package = "github.com/andaon/enis/proto/federation/v1;federationv1";

service FederationService {
  rpc SyncState(SyncStateRequest) returns (SyncStateResponse);
  rpc ReplicateEvent(ReplicateEventRequest) returns (google.protobuf.Empty);
}

message SyncStateRequest {
  string source_cluster = 1;
  string target_cluster = 2;
  repeated string agent_ids = 3;
}

message SyncStateResponse {
  int32 synced_count = 1;
  repeated string failed_agent_ids = 2;
}

message ReplicateEventRequest {
  enis.events.v1.Event event = 1;
  string source_cluster = 2;
}
```

#### **4. CI/CD Jobs**

**contracts-validate.yml** (completo):
```yaml
name: Validate Contracts

on:
  pull_request:
    paths:
      - 'openapi/**'
      - 'schemas/**'
      - 'proto/**'
  push:
    branches: [main, develop]

jobs:
  validate-openapi:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install Spectral
        run: npm install -g @stoplight/spectral-cli@6.11.0
      
      - name: Lint OpenAPI specs
        run: |
          spectral lint openapi/v1/*.yaml \
            --ruleset .spectral.yaml \
            --fail-severity warn
      
      - name: Validate examples
        run: |
          for spec in openapi/v1/*.yaml; do
            echo "Validating examples in $spec"
            spectral lint "$spec" --fail-on-unmatched-globs
          done
  
  validate-json-schemas:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install AJV
        run: npm install -g ajv-cli@5.0.0
      
      - name: Validate JSON Schemas
        run: |
          for schema in schemas/*.json; do
            echo "Validating $schema"
            ajv compile -s "$schema" --strict=true
          done
  
  validate-protos:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Buf
        uses: bufbuild/buf-setup-action@v1
        with:
          version: '1.28.1'
      
      - name: Lint Protocol Buffers
        run: buf lint proto/
      
      - name: Check Proto formatting
        run: buf format --diff --exit-code proto/
  
  typescript-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: npm ci
        working-directory: sdks/typescript
      
      - name: TypeScript compile check
        run: tsc --noEmit
        working-directory: sdks/typescript
```

**contracts-breaking.yml**:
```yaml
name: Detect Breaking Changes

on:
  pull_request:
    paths:
      - 'openapi/**'
      - 'proto/**'

jobs:
  detect-openapi-breaking:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Setup oasdiff
        run: |
          wget https://github.com/Tufin/oasdiff/releases/download/v1.10.10/oasdiff_1.10.10_linux_amd64.tar.gz
          tar -xzf oasdiff_1.10.10_linux_amd64.tar.gz
          sudo mv oasdiff /usr/local/bin/
      
      - name: Get base branch specs
        run: |
          git checkout origin/main
          mkdir -p /tmp/baseline
          cp -r openapi/v1/*.yaml /tmp/baseline/
          git checkout -
      
      - name: Detect breaking changes
        run: |
          for spec in openapi/v1/*.yaml; do
            filename=$(basename "$spec")
            echo "Checking $filename for breaking changes"
            oasdiff breaking \
              /tmp/baseline/$filename \
              $spec \
              --fail-on ERR
          done
  
  detect-proto-breaking:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Setup Buf
        uses: bufbuild/buf-setup-action@v1
        with:
          version: '1.28.1'
      
      - name: Detect breaking changes
        run: |
          buf breaking proto/ \
            --against '.git#branch=main'
```

### 🔍 Gaps Identificados y Mejoras

#### ➕ Agregar

1. **Golden samples** (ejemplos request/response completos)
   - Por cada endpoint: `contracts/openapi/v1/examples/{service}/{operation}.json`
   - Validados automáticamente contra schemas en CI
   - Target: ≥ 95% endpoints con examples

2. **`.spectral.yaml`** con reglas custom
   - Reglas de compliance DNA v3.0
   - Severidades documentadas en `docs/LINTING_RULES.md`
   - Regla `examples-required` obligatoria

3. **Tabla canónica de error codes**
   - `docs/ERROR_CODES.md`: códigos 4xx/5xx estandarizados
   - Ejemplos de respuestas de error por código
   - Schema de error response consistente

4. **Versionado explícito** en `info.version`
   - Formato SemVer estricto: `1.0.0`
   - Pre-releases: `1.0.0-alpha.{build}`

#### 🔧 Modificar

- **FREEZE:S3**: Aplicar solo a breaking changes en endpoints core (inference, agents, events, nops), no a endpoints nuevos
- **Deprecation policy**: Unificada en **`docs/01-sprint/S1/CHANGE-POLICY.md`** (fuente única)
  - Notice 6 meses / Sunset 12 meses
  - Documentar en cada spec con `deprecated: true` + `x-sunset-date`
  - Header HTTP: `X-API-Deprecated: true; sunset=YYYY-MM-DD`

#### 📦 Artefactos Adicionales (Rutas Estandarizadas)

```
contracts/openapi/v1/inference.yaml
contracts/openapi/v1/agents.yaml
contracts/openapi/v1/events.yaml
contracts/openapi/v1/nops.yaml
contracts/openapi/v1/examples/inference/create-inference.json
contracts/openapi/v1/examples/agents/register-agent.json
contracts/schemas/agent-registration.json
contracts/schemas/inference-request.json
contracts/schemas/event-schema.json
contracts/schemas/policy-schema.json
contracts/proto/inference.proto
contracts/proto/agents.proto
contracts/proto/events.proto
contracts/proto/federation.proto
.spectral.yaml                                  # Reglas custom DNA v3.0
docs/01-sprint/S1/errors.md                   # ⭐ Catálogo canónico error codes
docs/01-sprint/S1/CONTRACTS-GUIDE.md          # Guía de diseño de contratos
docs/01-sprint/S1/CHANGE-POLICY.md            # ⭐ POLÍTICA ÚNICA: FREEZE, Deprecation, Emergency RFC
docs/01-sprint/S1/LINTING_RULES.md            # Reglas Spectral documentadas
```

#### 🎯 Política Única de Cambios (Referencia)

> **Documento maestro**: `docs/01-sprint/S1/CHANGE-POLICY.md`
> 
> Esta política se referencia desde S2, S4, S7 y S15 para evitar duplicación.
>
> **Contenido**:
> - FREEZE:S3 (breaking en endpoints core)
> - FREEZE:S6 (feature-freeze pre-GA)
> - Deprecation: notice 6m, sunset 12m
> - Emergency RFC: SLA < 24h, bypass de freezes
> - Communication plan: pre/post breaking changes

#### ⚠️ Riesgos & Mitigación

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| **Falta de ejemplos** en specs | 🟡 Medio | Gate Spectral con regla `examples-required` bloqueante |
| **Inconsistencia error codes** entre servicios | 🟡 Medio | Validator custom que verifica contra `ERROR_CODES.md` |
| **Specs incompletos** por prisa | 🔴 Alto | Reviews obligatorios con Tech Leads antes de merge |

#### 👥 Owners

- **Contract Architect**: Diseño de specs, error codes, deprecation policy
- **Tech Leads (Inference/NOPS/Agents)**: Validación por servicio

### DoD (Definition of Done)

- [ ] **4 OpenAPI specs** publicados: inference, agents, events, nops
- [ ] **4 JSON Schemas** validados: agent-registration, inference-request, event-schema, policy-schema
- [ ] **4 Protocol Buffers** con buf lint OK: inference, agents, events, federation
- [ ] **Validación CI verde**: Spectral + AJV + Buf + TSC pasando
- [ ] **Breaking change detection**: oasdiff + buf breaking configurados
- [ ] **Baseline generado**: `.baseline/` con hashes BLAKE2b
- [ ] **Documentación**: Ejemplos ejecutables por cada contrato
- [ ] **Tests**: Contract tests pasando (≥ 20 tests)
- [ ] **`docs/ERROR_CODES.md`** con tabla completa y ejemplos
- [ ] **Examples coverage** ≥ 95% endpoints con golden samples
- [ ] **Spectral custom rules** implementadas y pasando

### Smoke Tests a Ejecutar

```bash
# 1. Validate all OpenAPI specs
spectral lint openapi/v1/*.yaml --fail-severity warn

# 2. Validate all JSON Schemas
for schema in schemas/*.json; do
  ajv compile -s "$schema" --strict=true
done

# 3. Validate all Protocol Buffers
buf lint proto/
buf format --diff --exit-code proto/

# 4. TypeScript compile check
cd sdks/typescript && tsc --noEmit && cd ../..

# 5. Detect breaking changes (should be none)
for spec in openapi/v1/*.yaml; do
  oasdiff breaking .baseline/$(basename $spec) $spec
done

buf breaking proto/ --against '.baseline/proto'

# 6. Generate baseline
python scripts/baseline/compute-baseline.py --write

# 7. Run contract tests
pytest tests/contracts/ -v
```

### Resultados Esperados

| Metric | Target | Measurement |
|--------|--------|-------------|
| OpenAPI specs | 4 | inference, agents, events, nops |
| JSON Schemas | 4 | agent-registration, inference-request, event, policy |
| Protocol Buffers | 4 | inference, agents, events, federation |
| Spectral violations | 0 errors | Spectral lint output |
| AJV validation | 100% pass | AJV compile success |
| Buf lint | 0 errors | Buf lint output |
| Breaking changes | 0 | oasdiff + buf breaking |
| Contract tests | ≥ 20 passing | Pytest results |
| CI pipeline time | < 8 minutes | GitHub Actions runtime |

### Preparado para S2 (Validation Engine & Baseline)
- ✅ Contratos OpenAPI definidos y validados
- ✅ JSON Schemas con validación estricta
- ✅ Protocol Buffers con buf lint
- ✅ CI/CD pipelines configurados
- ✅ Breaking change detection básico funcionando

---

### S2 — Validation Engine & Baseline 🔐
**Meta:** Validación determinista y baseline firmada

**Entregables:**
- ✅ Scripts: `validate-xrefs.py`, `breaking-changes.py`, `baseline.py` (BLAKE2b + Cosign)
- ✅ Matriz de compatibilidad inicial

#### 🔍 Gaps Identificados y Mejoras

**➕ Agregar:**
1. **Baseline firmada** (BLAKE2b + Cosign) con proceso de actualización documentado
2. **Cross-reference validation** - Script que detecta `$ref` rotos entre specs
3. **Contract drift detection** (runtime vs spec) - Compara tráfico de mocks vs schemas
4. **Performance baselines documentados** en `docs/PERFORMANCE_BASELINES.md`
   - Runtime validation: p95 ≤ 100ms
   - CI validation pack: p95 ≤ 1.2s
   - Dataset, HW specs, comandos reproducibles

**🔧 Modificar:**
- **Autoridad de firma**: Contract Architect (primary) + Security Lead (backup)
- **Notificación**: Slack `#contracts-alerts` + email ante rotación de baseline

**📦 Artefactos (Rutas Estandarizadas):**
```
docs/01-sprint/S2/PERFORMANCE_BASELINES.md      # ⭐ Métricas claras: p95 100ms (runtime), 1.2s (CI pack)
docs/01-sprint/S2/BASELINE_STRATEGY.md          # Proceso firma, autoridad, notificaciones
docs/01-sprint/S2/DRIFT-DETECTION.md            # Contract drift (runtime vs spec)
docs/01-sprint/S2/runbook-baseline-rollback.md  # Playbook rollback
.github/workflows/contracts-drift.yml            # Job drift detection
.github/workflows/contracts-baseline.yml         # Baseline verification gate
scripts/baseline/compute-baseline.py
scripts/baseline/verify-baseline.py
scripts/validate/validate-xrefs.py               # Cross-reference validation
```

**📊 Métricas de Performance (Sin Ambigüedades)**

> **Definiciones en `docs/01-sprint/S2/PERFORMANCE_BASELINES.md`**:
>
> 1. **p95 ≤ 100ms** = Validación runtime **por operación individual**
>    - Spectral lint de 1 spec: ≤ 50ms p95
>    - AJV validate de 1 schema: ≤ 15ms p95
>    - Buf lint de 1 proto: ≤ 40ms p95
>
> 2. **p95 ≤ 1.2s** = Validación completa **CI pack** (set completo)
>    - Todos los OpenAPI + Schemas + Protos
>    - Ejecutado en: GitHub Actions (ubuntu-latest, 2 vCPU)
>
> 3. **Dataset reproducible**:
>    - 4 OpenAPI specs (inference, agents, events, nops)
>    - 4 JSON Schemas
>    - 4 Protocol Buffers
>    - Hardware: Documentado en PERFORMANCE_BASELINES.md
>    - Comando: `scripts/bench/validation-bench.py --reproduce`

**⚠️ Riesgos:**
- Baseline "mal firmado" → playbook `docs/01-sprint/S2/runbook-baseline-rollback.md`
- Métricas contradictorias → Fuente única en `PERFORMANCE_BASELINES.md`

**DoD:**
- Gate `contracts-baseline` activo (PR falla si cambia hash sin bump)
- Reporte consolidado automático en PRs
- `PERFORMANCE_BASELINES.md` con **métricas SIN ambigüedades** (runtime vs CI pack)
- Job `contracts-drift-check` comparando mocks vs spec
- Referencias a CHANGE-POLICY.md desde S2 (evitar duplicación)

---

### S3 — SDK Generators (Alpha Py/TS) & Examples 🔧
**Meta:** SDKs alfa y ejemplos ejecutables

**Entregables:**
- ✅ Generadores: `sdks/python` y `sdks/typescript`
- ✅ Ejemplos: manufacturing-edge, inference-workflow, multi-service-orchestration
- ✅ Job `examples-smoke` automatizado

#### 🔍 Gaps Identificados y Mejoras

**➕ Agregar:**
1. **Benchmarks SDK** automatizados en `scripts/bench/sdk-bench.py`
   - Build time: Python ≤ 30s p95, TypeScript ≤ 25s p95
   - Import time, simple call latency
2. **Golden tests** de compilación determinísticos en `tests/golden/`
3. **Registry interno** (private) para publicación nightly con tag `alpha`
4. **On-call rotation** documentada en `docs/oncall.md`
   - Runbooks mínimos: `sdk-smoke.md`, `validation-fail.md`

**🔧 Modificar:**
- **Publicación**: Solo interna (pre-GA), no pública
- **Versionado**: `1.0.0-alpha.{build}` con auto-increment

**📦 Artefactos (Rutas Estandarizadas):**
```
sdks/python/                                    # SDK Python generado
sdks/typescript/                                # SDK TypeScript generado
.github/workflows/sdk-alpha.yml                 # ⭐ Con anti-leak policy
scripts/bench/sdk-bench.py                      # Benchmarks Py ≤30s, TS ≤25s
tests/golden/sdk-python/                        # Golden tests determinísticos
tests/golden/sdk-typescript/
docs/01-sprint/S3/SDK-BENCHMARKS.md           # Metodología benchmarks
docs/01-sprint/S3/runbook-sdk-smoke.md        # Smoke tests
docs/01-sprint/S3/SDK-INTERNAL-POLICY.md      # ⭐ Anti-leak: solo registry privado
docs/01-sprint/S3/oncall.md                    # On-call rotation
```

**🔒 Política Estrictamente Interna (Anti-Leak)**

> **Documento**: `docs/01-sprint/S3/SDK-INTERNAL-POLICY.md`
>
> **Enforcement en workflow**:
> - Publicación **SOLO** en registry interno (privado)
> - Tag: `alpha` (NO `latest` ni público)
> - Gate: Workflow falla si detecta push a npm.js o PyPI público
> - Instalación requerida: VPN interna + credenciales

**⚠️ Riesgos:**
- Leak accidental a registries públicos → **Gate anti-leak en workflow** (bloqueante)
- Flakes en builds → caché agresivo + golden tests + retry logic (3x)

**👥 Owners:**
- **SDK Engineers (2)**: Generadores, tests, benchmarks
- **On-call Lead**: Rotation, runbooks
- **Platform Engineer**: Registry interno, anti-leak enforcement

**DoD:**
- SDKs instalables localmente SOLO desde registry **privado**
- `examples-smoke` ≥ 99% de éxito
- SDK Python build ≤ 30s p95; TypeScript build ≤ 25s p95
- Nightly builds publicados con tag `alpha` (privado)
- `docs/01-sprint/S3/oncall.md` y runbooks listos
- **Anti-leak policy** verificada: intentos de publicación pública fallan

---

### S4 — Governance & Versioning 📋
**Meta:** Política SemVer/Deprecation y RFCs

**Entregables:**
- ✅ Docs: `API_GUIDELINES.md`, `BREAKING_CHANGES.md`, plantilla `RFC.md`
- ✅ Matriz de compatibilidad automatizada

#### 🔍 Gaps Identificados y Mejoras

**➕ Agregar:**
1. **RACI con nombres reales** en `docs/RACI.md`
   - Contract Architect, Security Lead, DX Lead, Release Manager
2. **Dashboards de contracts** en `observability/contracts-dashboard.json`
   - Lint errors, drift rate, baseline status, SDK builds
3. **Emergency RFC template** para parches críticos (SLA < 24h)

**🔧 Modificar:**
- **RFC template**: Agregar sección EMERGENCY RFC con criterios de uso
- **API Guidelines**: Consolidar en documento único

**📦 Artefactos (Rutas Estandarizadas):**
```
docs/01-sprint/S4/RACI.md                      # ⭐ Nombres REALES + backups
docs/01-sprint/S4/CODEOWNERS                   # ⭐ Ownership por carpeta crítica
docs/01-sprint/S4/RFC_TEMPLATE.md              # Template con EMERGENCY RFC
observability/contracts-dashboard.json          # Dashboard inicial
observability/exporters/validation-exporter.py
observability/exporters/sdk-build-exporter.py
```

**🎯 RACI con Nombres Reales (NO roles genéricos)**

> **Documento**: `docs/01-sprint/S4/RACI.md`
>
> **Formato requerido**:
> ```
> | Rol                  | Persona(s)      | Email                 | Slack         | Backup        |
> |----------------------|-----------------|-----------------------|---------------|---------------|
> | Contract Architect   | [NOMBRE REAL]   | contracts-arch@...    | @person       | [BACKUP]      |
> | Security Lead        | [NOMBRE REAL]   | security-lead@...     | @person       | [BACKUP]      |
> | DX Lead              | [NOMBRE REAL]   | dx-lead@...           | @person       | [BACKUP]      |
> | Release Manager      | [NOMBRE REAL]   | release-mgr@...       | @person       | [BACKUP]      |
> ```

**🔒 CODEOWNERS Reforzado**

> **Documento**: `docs/01-sprint/S4/CODEOWNERS`
>
> **Carpetas críticas**:
> - `openapi/` → @contract-architect @tech-lead-platform
> - `schemas/` → @contract-architect @security-lead
> - `proto/` → @contract-architect @tech-lead-platform
> - `pact/` → @dx-lead @contract-architect
> - `mocks/` → @platform-engineer
> - `sdks/` → @sdk-lead @dx-lead

**⚠️ Riesgos:**
- Propiedad difusa → RACI firmado explícitamente en PR por stakeholders + CODEOWNERS obligatorio
- Nombres no actualizados → Review trimestral de RACI (Q1/Q2/Q3/Q4)

**👥 Owners:**
- **Release Manager**: RACI ownership, quarterly review
- **Contract Architect**: RFC process, governance docs
- **SRE**: Dashboards, exporters
- **Product Manager**: Stakeholder alignment

**DoD:**
- DoR/DoD activos en todos los equipos
- **FREEZE:S3** aplicado a endpoints núcleo (referencia a `docs/01-sprint/S1/CHANGE-POLICY.md`)
- `docs/01-sprint/S4/RACI.md` con **nombres REALES** (no "TBD")
- `docs/01-sprint/S4/CODEOWNERS` activo en repo (PRs requieren approval de owners)
- Dashboard publicado y accesible con métricas en tiempo real

---

### S5 — Observabilidad de Contratos 📊
**Meta:** Métricas, SLOs y dashboards

**Entregables:**
- ✅ Exporters: validación, gates, SDK builds
- ✅ Dashboard de contratos en Grafana

#### 🔍 Gaps Identificados y Mejoras

**➕ Agregar:**
1. **SLOs definidos y monitoreados** en `docs/SLOs.md`
   - Validation success rate ≥ 99.9%
   - SDK generation success ≥ 95%
   - Breaking changes in main = 0
2. **Alertas configuradas** (Slack `#contracts-alerts` + email)
3. **Métricas adicionales**: contract coverage, docs satisfaction, drift rate

**📦 Artefactos:**
```
docs/SLOs.md
observability/alerting/slos.yaml
docs/runbooks/alert-breaking-detected.md
```

**DoD:**
- Alertas configuradas: `breaking`, `validation_fail`, `sdk_gen_fail`
- SLOs monitoreados 24/7
- 4 semanas continuas con SLOs cumplidos
- Runbooks por cada tipo de alerta

---

### S6 — Security & Supply Chain 🛡️
**Meta:** SBOM y firma de artefactos

**Entregables:**
- ✅ SBOM CycloneDX por SDK (Syft)
- ✅ Cosign sign/verify implementado
- ✅ Policy de licencias aprobada

#### 🔍 Gaps Identificados y Mejoras

**➕ Agregar:**
1. **SBOM automático** (SLSA-ish) publicado en `releases/v{version}/sbom/`
2. **Security gates bloqueantes** (no solo informativos)
   - Semgrep + Trivy bloquean PR si High/Critical sin `severity-exempt`
3. **SEC-README.md** auto-generado en CI con evidencias
4. **Relación SEC repo-level vs platform** documentada

**🔧 Modificar:**
- **Release process**: Bloquear si falta SBOM o firma

**📦 Artefactos (Rutas Estandarizadas):**
```
.github/workflows/security-gates.yml            # ⭐ Gates bloqueantes (S6+)
.github/workflows/sdks-build-sign-sbom.yml      # SBOM + firmas por release
docs/01-sprint/S6/SEC-README.md               # ⭐ Auto-generado, evidencias
docs/01-sprint/S6/SECURITY_ARCHITECTURE.md    # Retención ≥12m, cifrado, key rotation
docs/01-sprint/S6/WAIVER-POLICY.md            # ⭐ Excepciones High/Critical documentadas
scripts/security/generate-sbom.sh
scripts/security/sign-artifacts.sh
scripts/security/verify-signatures.sh
releases/v{version}/sbom/*.cdx.json             # SBOM CycloneDX
releases/v{version}/signatures/*.sig            # Firmas Cosign
```

**🔒 Escalamiento de Seguridad (Informativo → Bloqueante)**

> **Estrategia documentada en**: `docs/01-sprint/S6/SECURITY_ARCHITECTURE.md`
>
> **S0-S5** (Fase Adopción):
> - Scans **informativos** (Trivy/Semgrep no bloquean)
> - Objetivo: Acelerar adopción sin fricción
>
> **S6+** (SEC Repo-Level):
> - Trivy/Semgrep **BLOQUEAN** en High/Critical
> - Excepción requiere: `docs/01-sprint/S6/WAIVER-POLICY.md`
> - Waiver aprobado por Security Lead + justificación técnica
>
> **SBOM + Firmas** (Mandatorio desde S6):
> - SBOM CycloneDX generado con Syft por release
> - Firmas Cosign en todos los artefactos
> - Verificación automática en CI de consumers

**⚠️ Riesgos:**
- Key compromise → Key rotation playbook + HSM para prod keys en `SECURITY_ARCHITECTURE.md`
- Ruido de findings falsos positivos → Waiver policy clara y auditada

**👥 Owners:**
- **Security Lead**: Policy, exemptions, key management, waivers
- **Platform Engineer**: SBOM generation, CI automation
- **Contract Architect**: Security architecture docs

**DoD:**
- Job `sdks-build-sign-sbom` bloquea release si falla
- **FREEZE:S6** activado (feature-freeze para GA, ref. `docs/01-sprint/S1/CHANGE-POLICY.md`)
- SBOM en 100% de releases y artefactos firmados
- Pipelines fallan ante High/Critical **sin waiver aprobado** en `WAIVER-POLICY.md`
- `SEC-README.md` auto-generado con evidencias por release

---

### S7 — Integración con Inference Service 🤖
**Meta:** Conformance E2E con servicios/contratos

**Entregables:**
- ✅ Pact (consumer-driven): `sdks/python`, `sdks/typescript`
- ✅ Jobs: `pact-verify`, `pact-publish`

#### 🔍 Gaps Identificados y Mejoras

**➕ Agregar:**
1. **Pact Broker** matrix consumers/providers en `docs/PACT_MATRIX.md`
2. **Política de verificación** en deployment con conflict resolution por RFC
3. **Ownership table** por contrato en `docs/CONTRACT_OWNERSHIP.md`

**🔧 Modificar:**
- **PR checks**: Agregar `pact-verify` obligatorio en servicios dependientes

**📦 Artefactos (Rutas Estandarizadas):**
```
contracts/pact/python/consumer-contracts.json
contracts/pact/typescript/consumer-contracts.json
.github/workflows/pact-publish.yml
.github/workflows/pact-verify.yml              # ⭐ Con can-i-deploy obligatorio
docs/01-sprint/S7/PACT-POLICY.md              # ⭐ can-i-deploy como gate
docs/01-sprint/S7/PACT-MATRIX.md              # Matrix consumers/providers
docs/01-sprint/S7/CONTRACT_OWNERSHIP.md       # Ownership por contrato
docs/01-sprint/S7/pact-quickstart.md          # Guía rápida
```

**🔒 can-i-deploy como Gate Obligatorio**

> **Política en**: `docs/01-sprint/S7/PACT-POLICY.md`
>
> **Enforcement**:
> 1. **PRs de servicios consumidores** deben ejecutar:
>    ```bash
>    pact-broker can-i-deploy \
>      --pacticipant inference-service \
>      --version $GIT_SHA \
>      --to production
>    ```
> 2. **PR falla** si can-i-deploy retorna error
> 3. **Conflict resolution**: RFC express + reunión ≤ 72h con stakeholders
>
> **Matrix documentada** en `PACT-MATRIX.md`:
> - Consumer → Provider mappings
> - Frecuencia de verificación (on_deploy, nightly)
> - Owners por contrato

**⚠️ Riesgos:**
- Pact conflicts bloquean deploys → RFC express + can-i-deploy checks + conflict resolution ≤72h
- Pact Broker downtime → Fallback a modo degradado (warning, no blocking temporalmente)

**👥 Owners:**
- **SDK Engineers**: Consumer contracts
- **Tech Leads (Services)**: Provider verification
- **Platform Engineer**: Pact Broker, CI integration, can-i-deploy enforcement

**DoD:**
- 100% verificación de providers en pipelines externos
- Contract tests pasando en todos los entornos
- `pact:verify` en cada deployment
- **`can-i-deploy` obligatorio** en PRs de servicios consumidores (gate bloqueante)
- Matrix de ownership completa en `docs/01-sprint/S7/PACT-MATRIX.md`

---

### S8 — Integración con NOPS Kernel ⚙️
**Meta:** Alineación agents/events/state y event-bus

**Entregables:**
- ✅ Ejemplos E2E con NOPS Kernel
- ✅ Cross-references en documentación
- ✅ Mocks estables y mantenidos

#### 🔍 Gaps Identificados y Mejoras

**➕ Agregar:**
1. **Estrategia de actualización de mocks** en `docs/MOCK_STRATEGY.md`
2. **Healthchecks automatizados** - Job cada 6h en dev
3. **Validación mock ↔ spec** en CI

**📦 Artefactos:**
```
contracts/mocks/prism/auto-update.sh
.github/workflows/mocks-health-check.yml
docs/MOCK_STRATEGY.md
```

**DoD:**
- Cero drift detectado entre contratos y NOPS
- Contract tests en verde (100%)
- Mocks se regeneran ante cambios en specs
- Alerta si mock desactualizado > 1 sprint

---

### S9 — Troubleshooting & Cookbooks 📚
**Meta:** Reducir TTR y elevar adopción SDKs

**Entregables:**
- ✅ Guías: `contract-validation-errors`, `sdk-generation-issues`, `version-compatibility`
- ✅ Cookbook por lenguaje (Py/TS/Go/Java/.NET)

#### 🔍 Gaps Identificados y Mejoras

**➕ Agregar:**
1. **Cookbooks por stack** con pasos reproducibles en `docs/cookbooks/{lang}/`
2. **Runbooks on-call ampliados** con escenarios reales (timeouts, drift, freeze violado)
3. **Alertas basadas en KPIs** con thresholds en `docs/ALERTING_THRESHOLDS.md`
4. **Simulación de incidentes** - Game days con MTTR medido

**🔧 Modificar:**
- **Cookbooks**: Integrar links a dashboards relevantes

**📦 Artefactos:**
```
docs/cookbooks/python/quickstart.md
docs/runbooks/oncall-scenarios.md
docs/ALERTING_THRESHOLDS.md
docs/gamedays/incident-simulation-report.md
```

**DoD:**
- TTR reducido en 30%
- ≥ 80% de issues con código TROU-*
- ≥ 3 runbooks verificados en staging
- Simulación de 2 incidentes con MTTR < 30min
- Alertas activas en `#contracts-ops`

---

### S10 — Performance & Benchmarks ⚡
**Meta:** Anti-regresión y objetivos progresivos

**Entregables:**
- ✅ Benchmarks: `validation_bench.md`, `sdk_generation_bench.md`
- ✅ Scripts automatizados en `scripts/bench/*`

#### 🔍 Gaps Identificados y Mejoras

**➕ Agregar:**
1. **CLI MVP `enis-contracts`** - Comandos: lint, diff, baseline, publish, pact-run, validate
2. **Preparación auditoría externa** - Checklist + evidencias automatizadas
3. **Templates de scaffold** - Genera estructura base

**🔧 Modificar:**
- **Roadmap**: Mover CLI de S16 a S10 por impacto DX crítico

**📦 Artefactos:**
```
cli/enis-contracts/
docs/CLI_REFERENCE.md
docs/compliance/audit-checklist.md
scripts/compliance/generate-evidence.sh
```

**⚠️ Riesgos:**
- CLI scope creep → Mantener MVP estricto; features avanzadas en S16

**👥 Owners:**
- **DX Lead**: CLI design, UX
- **SDK Engineers**: CLI implementation

**DoD:**
- Gate de regresión activo (p95 > baseline × 1.2 → falla CI)
- Reportes automáticos en PRs
- Binario `enis-contracts` instalable y funcional
- ≥ 6 comandos implementados
- Checklist auditoría 80% completado

---

### S11 — SDKs Enterprise (Go/Java/.NET Beta) 🏢
**Meta:** Cobertura multi-lenguaje completa

**Entregables:**
- ✅ Generadores Go/Java/.NET (beta)
- ✅ SBOM y firmas por SDK
- ✅ Documentación y ejemplos

#### 🔍 Gaps Identificados y Mejoras

**➕ Agregar:**
1. **Criterio de priorización** por adopción/NPS en `docs/SDK_PRIORITIZATION.md`
2. **Matrix de compatibilidad** por contrato y lenguaje en `docs/SDK_COMPATIBILITY_MATRIX.md`
3. **Benchmarks por SDK**: Go ≤ 35s build p95; Java/.NET establecer baseline

**📦 Artefactos:**
```
sdks/go/, sdks/java/, sdks/dotnet/
docs/SDK_PRIORITIZATION.md
docs/SDK_COMPATIBILITY_MATRIX.md
```

**⚠️ Riesgos:**
- Fragmentación de features entre SDKs → Feature parity matrix + plan convergencia

**DoD:**
- Builds smoke pasando (≥ 95%)
- Publicación en repos internos
- Benchmarks medidos y documentados

---

### S12 — Macro-Módulos (ASM/CGN/AWE/SHIF) 🎛️
**Meta:** Contratos v1 para macro-módulos

**Entregables:**
- ✅ OpenAPI: `asm.yaml`, `cgn.yaml`, `awe.yaml`, `shif.yaml`
- ✅ Schemas relacionados y validados

#### 🔍 Gaps Identificados y Mejoras

**➕ Agregar:**
1. **Validación con Tech Leads** - Sesiones de revisión por módulo con actas firmadas
2. **Matrix inter-repo readiness** en `docs/INTERREPO_READINESS.md`
3. **Ejemplos E2E** por macro-módulo ejecutables

**📦 Artefactos (Rutas Estandarizadas):**
```
contracts/openapi/v1/asm.yaml                  # Adaptive State Management
contracts/openapi/v1/cgn.yaml                  # Causal Graph Navigation
contracts/openapi/v1/awe.yaml                  # Autonomous Workflow Evolution
contracts/openapi/v1/shif.yaml                 # System-Human Integration Fabric
contracts/schemas/asm-state-schema.json
contracts/schemas/cgn-graph-schema.json
contracts/schemas/awe-workflow-schema.json
contracts/schemas/shif-integration-schema.json
docs/01-sprint/S12/ACTAS-VALIDACION-ASM.md   # ⭐ Acta firmada ASM
docs/01-sprint/S12/ACTAS-VALIDACION-CGN.md   # ⭐ Acta firmada CGN
docs/01-sprint/S12/ACTAS-VALIDACION-AWE.md   # ⭐ Acta firmada AWE
docs/01-sprint/S12/ACTAS-VALIDACION-SHIF.md  # ⭐ Acta firmada SHIF
docs/01-sprint/S12/INTERREPO-READINESS.md    # Estado dependencias inter-repo
docs/examples/macro-modules/asm-e2e.md
docs/examples/macro-modules/cgn-e2e.md
docs/examples/macro-modules/awe-e2e.md
docs/examples/macro-modules/shif-e2e.md
```

**🔒 Bloqueo por Sign-off (Gate Crítico)**

> **Enforcement**: El **merge a main** debe **FALLAR** si falta acta firmada de algún módulo.
>
> **Proceso**:
> 1. **Sesión de validación** con Tech Lead del módulo
> 2. **Acta generada** usando template en `docs/01-sprint/S12/ACTAS-VALIDACION-{MODULE}.md`
> 3. **Formato de acta**:
>    ```markdown
>    # Acta de Validación: {MODULE}
>    
>    **Fecha**: YYYY-MM-DD
>    **Participantes**: [Tech Lead], [Contract Architect]
>    **Contratos revisados**: {module}.yaml, {module}-schema.json
>    
>    ## Validación
>    - [ ] Endpoints complete y documentados
>    - [ ] Schemas validan correctamente
>    - [ ] Ejemplos ejecutables
>    - [ ] Sin breaking changes vs dependencias
>    
>    ## Aprobación
>    **Tech Lead**: [FIRMA/NOMBRE]
>    **Contract Architect**: [FIRMA/NOMBRE]
>    **Estado**: APROBADO / RECHAZADO / PENDIENTE
>    ```
> 4. **CI check**: Workflow verifica existencia de actas con estado "APROBADO"
> 5. **PR falla** si alguna acta falta o está en estado "PENDIENTE"/"RECHAZADO"

**⚠️ Riesgos:**
- Desacuerdo en contratos → RFC express; escalation a Steering si no se resuelve en 72h
- Sign-off bloqueado → Daily stand-up con stakeholders hasta resolución

**👥 Owners:**
- **Contract Architect**: Facilitación de validaciones, documentación
- **Tech Leads (Macro-Módulos)**: Revisión y sign-off FORMAL
- **Platform Engineer**: CI enforcement del gate de sign-off

**DoD:**
- Lint/compatibilidad OK (100%)
- Ejemplos E2E ejecutables para cada módulo
- **Actas de validación FIRMADAS** por todos los módulos (ASM/CGN/AWE/SHIF)
- **Gate de sign-off activo**: Merge falla si falta aprobación
- `docs/01-sprint/S12/INTERREPO-READINESS.md` actualizado con estado

---

### S13 — SDKs GA (Py/TS) + DevPortal 🚀
**Meta:** GA de SDKs y portal para desarrolladores

**Entregables:**
- ✅ Publicación GA: Python, TypeScript
- ✅ Quickstarts y guías
- ✅ Colecciones Postman/Insomnia

#### 🔍 Gaps Identificados y Mejoras

**➕ Agregar:**
1. **Customer beta pilot** con 2-3 partners, feedback formal
2. **Hardening de SDKs** - Telemetría opt-in, trazas DX, error messages mejorados
3. **Release candidate** (RC) `1.0.0-rc.1` con testing exhaustivo

**📦 Artefactos:**
```
docs/beta-feedback-template.md
docs/beta-pilot-report.md
docs/TELEMETRY_POLICY.md
```

**⚠️ Riesgos:**
- Feedback negativo beta → Iteración rápida; roadmap ajustable

**👥 Owners:**
- **Product Manager**: Beta program
- **DX Lead**: Hardening, telemetry

**DoD:**
- Time-to-first-api-call ≤ 10 minutos
- Portal DevPortal publicado y documentado
- Informe beta con issues y plan de cierre
- ≥ 90% feedback positivo (NPS ≥ 40)

---

### S14 — Compliance & Audit 📜
**Meta:** Evidencias y retención para auditorías

**Entregables:**
- ✅ Audit trail completo (contratos, firmas, releases)
- ✅ Sistema de retención y export
- ✅ Reportes automáticos para compliance

#### 🔍 Gaps Identificados y Mejoras

**➕ Agregar:**
1. **Evidencias automatizadas históricas** consolidadas desde S3
2. **Revisión trimestral** documentada retroactivamente
3. **Compliance pack exportable** `compliance-pack.zip` generado en CI
4. **Retención** storage con backup ≥ 12 meses

**🔧 Modificar:**
- **No iniciar desde cero**: Consolidar evidencias históricas

**📦 Artefactos:**
```
scripts/compliance/consolidate-historical.sh
docs/compliance/quarterly-reviews/
docs/compliance/checklist-iso-soc2.md
docs/compliance/pack.zip (auto-generated)
```

**⚠️ Riesgos:**
- Evidencias faltantes → Reconstrucción desde git history + CI logs

**DoD:**
- Auditoría reproducible E2E (< 2h)
- Evidencias guardadas por 12+ meses
- `compliance-pack.zip` generado automáticamente
- Checklist 100% con links verificables

---

### S15 — GA Gate & Release 🎉
**Meta:** Gates en verde y lanzamiento v1.0.0

**Entregables:**
- ✅ Pentest completado y remediado
- ✅ Release notes publicadas
- ✅ Guía de operación para SRE

#### 🔍 Gaps Identificados y Mejoras

**➕ Agregar:**
1. **GA checklist granular** (100+ ítems) en `docs/GA_CHECKLIST.md`
   - Contratos congelados, SDKs GA, Pact green, evidencia compliance, dashboards estables
2. **Política Emergency RFC activa** durante freeze
3. **Release notes completas** con changelog consolidado y migration guides
4. **Guía operacional SRE** con runbooks y escalation paths

**📦 Artefactos (Rutas Estandarizadas):**
```
docs/01-sprint/S15/GA-CHECKLIST.md            # ⭐ Checklist 100+ ítems granular
docs/01-sprint/S15/GA-STATUS-TRACKER.md       # ⭐ Tracker semanal On Track/At Risk/Blocked
docs/01-sprint/S15/OPERATIONS_GUIDE.md        # Guía operacional SRE
docs/01-sprint/S15/RELEASE_NOTES_v1.0.0.md    # Release notes v1.0.0
docs/01-sprint/S15/MIGRATION_GUIDE_1.0.0.md   # Guía migración v0→v1
releases/v1.0.0/                               # Release artifacts firmados
```

**🔒 GA Checklist Granular (100+ Ítems)**

> **Documento maestro**: `docs/01-sprint/S15/GA-CHECKLIST.md`
>
> **Categorías principales** (mínimo 8):
> 1. **Contratos** (15 ítems): Congelados, zero breaking, baselines
> 2. **SDKs** (20 ítems): GA en 5 lenguajes, benchmarks, SBOM
> 3. **Pact** (10 ítems): can-i-deploy green, matrix completa
> 4. **Security** (15 ítems): Gates bloqueantes, firmas, compliance
> 5. **Observabilidad** (12 ítems): SLOs, dashboards estables ≥4 semanas
> 6. **Docs & DX** (15 ítems): Portal, NPS ≥90%, CLI
> 7. **Governance** (10 ítems): RACI real, CODEOWNERS, Emergency RFC
> 8. **Operations** (8 ítems): SRE training, runbooks, DR plan
>
> **Ritual Semanal** (desde S13):
> - Reunión Viernes 3pm, 30min
> - Review de `GA-STATUS-TRACKER.md` por categoría
> - Status: On Track / At Risk / Blocked
> - Blocked items: Plan de mitigación inmediato

**⚠️ Riesgos:**
- GA bloqueada por ítem crítico → Checklist revisado semanalmente desde S13; early warnings en S14
- Waiver board desbordado → Límite 5 waivers activos; escalation si >5

**👥 Owners:**
- **Release Manager**: Checklist ownership, rituales semanales
- **Contract Architect**: Sign-off técnico
- **Security Lead**: Sign-off seguridad
- **Product Manager**: Steering Committee, coordinación

**DoD:**
- Status `APPROVED_WITH_ADJUSTMENTS` cerrado
- Tag `v1.0.0` publicado en producción
- **100% ítems GA checklist verificados** (mínimo 100 ítems)
- Aprobación formal Steering Committee (acta firmada)
- SRE training completado (≥ 80% equipo)
- Tracker semanal con 4+ semanas de histórico (On Track)
- Referencias a `docs/01-sprint/S1/CHANGE-POLICY.md` (Emergency RFC durante freeze)

---

### S16 — Optimización & Roadmap v2 🔮
**Meta:** Performance 10x y definición de features v2

**Entregables:**
- ✅ CLI `enis-contracts` (scaffold, validate, diff, bump, release)
- ✅ PoC: GraphQL schemas, AsyncAPI, multi-tenant
- ✅ DX suite completa
- ✅ RFCs v2.0 aprobados

#### 🔍 Gaps Identificados y Mejoras

**➕ Agregar:**
1. **Milestones intermedios para 10x performance** en `docs/PERFORMANCE_10X_PLAN.md`
   - Validación p95 < 100ms, SDK gen: Py ≤ 20s, TS ≤ 18s, Go ≤ 25s
2. **Discovery v2.0 iniciado** (no esperar post-S16)
   - RFCs v2.0: GraphQL, AsyncAPI, multi-tenant en `docs/roadmap/v2.0/`
3. **CLI advanced features** - ≥ 10 comandos + plugins system
4. **DX suite** - Templates, StackBlitz/Colab integration

**📦 Artefactos:**
```
docs/PERFORMANCE_10X_PLAN.md
docs/roadmap/v2.0/SCOPE_RFC.md
cli/enis-contracts/plugins/
templates/stackblitz/, templates/colab/
```

**⚠️ Riesgos:**
- Optimización prematura sin ROI → Benchmarks continuos; priorizar bottlenecks

**👥 Owners:**
- **Performance Engineer**: 10x plan
- **Contract Architect**: v2.0 roadmap

**DoD:**
- Performance: validación p95 < 100ms, generación SDKs < 60s
- Roadmap v2 aprobado por stakeholders
- Informe performance con metas alcanzadas
- RFC alcance v2.0 priorizado
- `docs_satisfaction ≥ 90%` (NPS)

---

## 🔮 Sprints Post-GA (Extensiones & MCP)

> **Nota**: Los siguientes sprints son propuestos para exploración post-GA de funcionalidad extendida (MCP - Model Context Protocol)

---

### S17 — MCP Discovery & Contracts (Spike Controlado) 🔬

**Meta:** Evaluar viabilidad y cerrar contratos mínimos para MCP sin comprometer el core

**Alcance:** Contratos y seguridad; nada de producción todavía

#### 🔍 Gaps Identificados y Mejoras

**➕ Agregar:**

1. **Contratos MCP (request/response)** para:
   - **Tool/Resource Catalog**: Listar herramientas/recursos disponibles
   - **Invocation Contract**: Invocación de herramientas con parámetros tipados
   - **Session/Context**: Scoping, límite de tokens/datos

2. **Estrategia de aislamiento**
   - Feature flag `mcp.enabled=false` por defecto
   - Rollout controlado por tenant

3. **Modelo de autorización**
   - mTLS + JWT s2s
   - Scopes por herramienta
   - Rate-limiting por tenant

4. **Mocks MCP Server/Client**
   - Prism/WireMock configurados
   - Pact consumers/providers para MCP

**📦 Artefactos:**
```
docs/01-sprint/S17/MCP-OVERVIEW.md
docs/01-sprint/S17/MCP-CONTRACTS.md (catálogo, invocación, sesión)
docs/01-sprint/S17/MCP-SECURITY.md (mTLS, JWT scopes, rate-limit)
docs/01-sprint/S17/MCP-MOCKS.md (arranque, datasets, limitaciones)
docs/01-sprint/S17/MCP-RISKS.md (impactos y mitigaciones)
contracts/openapi/v1/mcp.yaml (draft)
contracts/schemas/mcp-tool-catalog.json
contracts/schemas/mcp-invocation.json
```

**⚠️ Riesgos:**
- Complejidad no anticipada → Spike time-boxed (2 semanas máx)
- Impacto en contratos existentes → Gate: 0 breaking changes en APIs core

**👥 Owners:**
- **Contract Architect**: Diseño de contratos MCP
- **Security Lead**: Modelo de autorización
- **DX Lead**: Developer experience

**DoD / Gates:**
- [ ] Specs MCP lint + Pact green contra mocks
- [ ] **Sin cambios en endpoints existentes** (gate no-breaking estricto)
- [ ] Riesgo documentado + plan de rollback
- [ ] RFC MCP aprobado con stakeholders
- [ ] Feature flag `mcp.enabled` implementada y testeada

**Estimación:** 10-12 días (spike controlado)

---

### S18 — MCP SDK Adapters (Py/TS) + Governance 🔌

**Meta:** Agregar capas SDK para MCP sin romper DX actual

**Alcance:** Adapters opcionales en Py/TS, sin public GA

#### 🔍 Gaps Identificados y Mejoras

**➕ Agregar:**

1. **SDK Adapters MCP (Python/TypeScript)**
   - **Descubrimiento**: `list_tools()`, `describe_resource()`
   - **Invocación**: `invoke(tool, params, context)`
   - **Resiliencia**: Timeouts, retries, circuit-breaker, idempotencia

2. **Policy DX**
   - Nombres/espacios MCP consistentes
   - Trazas opt-in para debugging
   - Límites de payload documentados

3. **Governance MCP**
   - Reglas Spectral/Schema específicas para recursos MCP
   - Validadores oasdiff para contratos MCP
   - Deprecation policy para tools MCP

**🔧 Modificar:**
- SDKs Python/TypeScript: Agregar módulo `mcp` como optional extra
- Instalación: `pip install enis-contracts[mcp]` / `npm install @enis/contracts --with-mcp`

**📦 Artefactos:**
```
docs/01-sprint/S18/MCP-SDK-ADAPTERS.md (APIs, ejemplos)
docs/01-sprint/S18/MCP-GOVERNANCE.md (naming, límites, trazas)
docs/01-sprint/S18/MCP-BENCHMARKS.md (metodología y metas)
sdks/python/enis_contracts/mcp/
sdks/typescript/src/mcp/
.spectral-mcp.yaml (reglas específicas MCP)
```

**⚠️ Riesgos:**
- Overhead de adapter → Target: ≤ +10% vs llamadas directas
- Fragmentación DX → Documentación clara de cuándo usar MCP vs REST

**👥 Owners:**
- **SDK Engineers**: Implementación de adapters
- **DX Lead**: Governance y documentación
- **Contract Architect**: Validación de contratos

**DoD / Gates:**
- [ ] SDK beta interno (registry privado) con ejemplos y smoke determinísticos
- [ ] **Benchmarks**: Overhead de adapter ≤ +10% vs llamadas directas simuladas
- [ ] Pact consumers de SDK pasan contra MCP mocks
- [ ] Documentación de migración REST → MCP (cuando aplica)
- [ ] Feature parity matrix actualizada

**Estimación:** 12-14 días

---

### S19 — Pilot Integrations + Security Hardening 🛡️

**Meta:** Probar MCP con 1-2 integraciones reales controladas y endurecer seguridad

**Alcance:** Pilotos limitados; sin rollout masivo

#### 🔍 Gaps Identificados y Mejoras

**➕ Agregar:**

1. **Pilotos Controlados** (ejemplos razonables)
   - **"Data Fetcher"** (read-only): Lectura de recursos internos
   - **"Notifier"** (write-light): Notificaciones vía MCP

2. **Security Hardening**
   - **Allow-list de herramientas**: Solo tools aprobados pueden registrarse
   - **Egress guard**: Clasificación PII y bloqueo de datos sensibles
   - **Audit trail firmado**: Registro de uso con firma digital
   - **Rate-limit por herramienta/tenant**: Quotas configurables
   - **Observabilidad dedicada**: Panel MCP separado

3. **Compliance MCP**
   - SBOM adapters MCP
   - Firmas de invocaciones
   - Pact contracts versionados
   - Logs firmados con Cosign

**📦 Artefactos:**
```
docs/01-sprint/S19/MCP-PILOT-PLAN.md
docs/01-sprint/S19/MCP-HARDENING.md (allow-list, quotas, egress)
docs/01-sprint/S19/MCP-OBSERVABILITY.md
docs/01-sprint/S19/MCP-EVIDENCE.md (qué se recolecta y dónde)
observability/mcp-dashboard.json
docs/compliance/mcp-evidence/
contracts/openapi/v1/mcp-pilots/
```

**⚠️ Riesgos:**
- Pilotos con problemas de seguridad → Rollback inmediato + post-mortem
- PII leak → Egress guard con clasificación automática
- Abuso de rate-limits → Quotas estrictas + alertas

**👥 Owners:**
- **Security Lead**: Hardening y egress guard
- **SRE**: Observabilidad y rate-limiting
- **Product Manager**: Pilotos y feedback
- **Compliance Lead**: Evidencias y auditoría

**DoD / Gates:**
- [ ] Piloto con **NPS ≥ 40** y **0 incidentes críticos**
- [ ] Panel MCP con métricas:
  - Errores p95
  - Tasa de éxito
  - Latencia por tool
  - Egress block events
- [ ] Pack de evidencias MCP listo (para auditar)
- [ ] Allow-list operativo con proceso de aprobación
- [ ] Audit trail con 100% de invocaciones registradas y firmadas

**Estimación:** 14-16 días

---

## 🎯 Objetivos Estratégicos

### Visión 2025-2026
Consolidar **Agent Contracts** como el **Contract Central** de ENIS v3.0, garantizando:

1. 🔒 **100% Backward Compatibility** - Detección automática de breaking changes
2. 📦 **Adopción > 85%** - SDKs utilizados por equipos internos y partners
3. 🛡️ **Security by Design** - SBOM, firmas digitales, auditoría completa
4. ⚡ **Developer Experience** - Time-to-first-API-call < 10 minutos
5. 📊 **Observabilidad Total** - Métricas, dashboards, alertas en tiempo real

### 📈 KPIs Clave

| KPI | Target | Medición |
|-----|--------|----------|
| 🎯 Validation Success Rate | ≥ 99.9% | CI/CD pipeline metrics |
| 🚫 Breaking Changes in Main | 0 | Automated gates (oasdiff/buf) |
| 🔧 SDK Generation Success | ≥ 95% | Build pipeline metrics |
| 📚 Docs Satisfaction | ≥ 90% | Developer surveys (NPS) |
| ⚡ Time to First API Call | ≤ 10min | Onboarding telemetry |
| 🏢 Internal Adoption | ≥ 85% | Team surveys |
| 📊 Contract Coverage | 100% | Services with contracts |

---

## 🔗 Supuestos y Dependencias

### ✅ Supuestos
- 📘 **DNA v3.0** y terminología de ENIS vigentes y estables
- 👥 Repositorios con **owners activos**: integration-apis, nops-kernel, inference-service
- 💰 **Presupuesto y headcount** aprobados para 12 meses (6-9 FTE)
- 🏗️ Infraestructura de **CI/CD** disponible y escalable

### 🔴 Dependencias Externas (Hard/Bloqueantes)

| Servicio | Superficie | Criticidad | Estrategia de Mitigación |
|----------|-----------|------------|-------------------------|
| 🧠 **NOPS Kernel** | event-bus, state, agents | Alta | Mocks WireMock (S1) + Pact |
| 🤖 **Inference Service** | predict, models, status | Alta | Mocks Prism (S1) + Pact |
| 🔐 **Integration & APIs** | gateway, authN, authZ, rate-limiting | Media | Mocks Prism + simuladores |

### 🟡 Dependencias Internas (Soft)

| Área | Componentes | Owner |
|------|-------------|-------|
| 🛡️ **Security & Compliance** | audit trail, policy schemas, SBOM | Security Team |
| 📊 **Observabilidad** | Prometheus, Grafana, Tempo, Loki | SRE Team |
| 🔄 **CI/CD** | GitHub Actions, Cosign, Syft, Buf, oasdiff | Platform Team |

---

## 🏗️ Workstreams y Épicas

| 🎯 Workstream | 📦 Épicas | ✅ Resultado Esperado | Sprints |
|---------------|-----------|----------------------|---------|
| **Contracts Core** | Governance, Versioning, Deprecation, Compatibility Matrix, Baseline | Política SemVer con sunset; baseline firmada; matriz automatizada | S1-S4 |
| **OpenAPI / JSON Schema** | Normalización OAS3.0, Librería de schemas, Validación estricta | 15+ specs, 8+ schemas con linters y ejemplos | S1, S3, S12 |
| **Protobuf** | Buf modules, Breaking checks, Proto validation | 4 protos con `buf breaking` en gates | S1, S2 |
| **SDKs Multi-Language** | Python, TypeScript, Go, Java, .NET | SDKs generados, versionados, firmados con CI verde | S3, S11, S13 |
| **CI/CD Contracts** | Validation Engine, Breaking Detector, Release Orchestrator | Jobs obligatorios: validate, breaking, compatibility | S0, S2, S5 |
| **Security & Compliance** | SBOM, Cosign, Policy Schema, Audit Trail | SBOM CycloneDX, firmas Sigstore, auditoría completa | S6, S14 |
| **Observabilidad** | Métricas, SLOs/Alertas, Dashboards | Exporters + dashboards Grafana de contratos/SDKs | S5, S12 |
| **Documentación & DX** | Playbooks, Troubleshooting, Ejemplos, CLI | Docs production-ready + CLI `enis-contracts` | S3, S9, S16 |

---

## 📅 Cronograma Trimestral (Q4 2025 – Q3 2026)

> **Modelo de trabajo:** Sprints bisemanales (6 sprints/trimestre)  
> **Cada trimestre incluye:** Objetivos · Hitos · Entregables · Criterios de Salida

---

### 🏗️ Q4 2025 — Fundaciones y Gates (S0-S6)

#### 🎯 Objetivos Clave
1. ✅ Establecer **Governance** + pipelines de validación y firmas
2. ✅ Publicar contratos **v1.0.0** (inference, agents, events, nops)
3. ✅ Entregar SDKs **alpha** (Python/TypeScript) y documentación base

#### 📦 Backlog por Sprint

| Sprint | Foco | Entregables Clave |
|--------|------|-------------------|
| **S0** | 🎬 Repo Bootstrap | Estructura monorepo, CI/CD, Docker < 500MB, pre-commit hooks |
| **S1** | 📝 Contracts First | OpenAPI 3.0 (inference/agents/events/nops), JSON Schemas, Protos |
| **S2** | 🔐 Validation Engine | Scripts validación, breaking changes, baseline firmada (BLAKE2b) |
| **S3** | 🔧 SDK Alpha Py/TS | Generadores SDKs Python/TypeScript, ejemplos ejecutables |
| **S4** | 📋 Governance | API Guidelines, SemVer policy, RFC templates, **FREEZE:S3** |
| **S5** | 📊 Observabilidad v1 | Exporters, dashboards Grafana, alertas críticas |
| **S6** | 🛡️ Security | SBOM CycloneDX, Cosign signing, **FREEZE:S6** |

#### 🏆 Hitos
- **H1:** Pipelines con gates operacionales (verde/rojo)
- **H2:** Tag **v1.0.0** contratos core publicado
- **H3:** SDKs alpha disponibles en repos internos

#### ✅ Criterios de Salida
- ✓ **0 breaking changes** en main
- ✓ `validation_success_rate ≥ 99%`
- ✓ Baseline firmada y verificada en PRs
- ✓ Documentación inicial publicada (`README`, `CONTRIBUTING`, guías básicas)

---

### 🚀 Q1 2026 — Ampliación & GA SDKs (S7-S12)

#### 🎯 Objetivos Clave
1. ✅ Completar contratos **macro-módulos** (ASM/CGN/AWE/SHIF)
2. ✅ SDKs **GA** Python y TypeScript; **beta** Go/Java/.NET
3. ✅ Integración observabilidad completa + SLOs activos

#### 📦 Backlog por Sprint

| Sprint | Foco | Entregables Clave |
|--------|------|-------------------|
| **S7** | 🤖 Inference Integration | Pact consumer-driven, conformance E2E, provider verification |
| **S8** | ⚙️ NOPS Integration | Alineación agents/events/state, mocks estables, xrefs docs |
| **S9** | 📚 Troubleshooting | Guías de resolución, cookbooks por lenguaje, reducción TTR |
| **S10** | ⚡ Performance & Benchmarks | Anti-regresión, benchmarks automatizados, gates de latencia |
| **S11** | 🏢 SDKs Enterprise Beta | Go/Java/.NET generators, SBOM, documentación |
| **S12** | 🎛️ Macro-Módulos | ASM/CGN/AWE/SHIF contracts, schemas, ejemplos |

#### 🏆 Hitos
- **H4:** SDKs Python y TypeScript **GA** publicados
- **H5:** 15+ OpenAPI specs validadas, 8+ JSON Schemas
- **H6:** SLOs activos con alertas en Slack/Email

#### ✅ Criterios de Salida
- ✓ `time_to_first_api_call ≤ 10 minutos`
- ✓ `docs_satisfaction ≥ 85%` (NPS)
- ✓ `breaking_changes_in_main = 0`
- ✓ Exporters + dashboards operacionales en producción

---

### 🏢 Q2 2026 — Enterprise & Compliance (S13-S15+)

#### 🎯 Objetivos Clave
1. ✅ **Enterprise certification** (ISO/SOC2 ready) para pipelines y artefactos
2. ✅ SDKs **GA** en los 5 lenguajes (Py/TS/Go/Java/.NET)
3. ✅ DR/Resilience + políticas de retención y auditoría completa

#### 📦 Backlog por Sprint

| Sprint | Foco | Entregables Clave |
|--------|------|-------------------|
| **S13** | 🚀 SDKs GA Py/TS | Publicación GA, DevPortal, Quickstarts, Postman/Insomnia |
| **S14** | 📜 Compliance & Audit | Audit trail, retención, evidencias, reportes automáticos |
| **S15** | 🎉 GA Gate & Release | Pentest, release notes v1.0.0, guía operacional |
| **S16+** | 🔮 Preparación v2 | DR drills, compliance pack, SDKs enterprise refinement |

#### 🏆 Hitos
- **H7:** SDKs **GA** en los 5 lenguajes (Python, TypeScript, Go, Java, .NET)
- **H8:** **Compliance pack** publicado con evidencias + reportes
- **H9:** DR ejecutado y aprobado (RTO < 2h, RPO < 15min)

#### ✅ Criterios de Salida
- ✓ `sdk_generation_success_rate ≥ 97%`
- ✓ Auditoría reproducible E2E con trazabilidad completa
- ✓ Ejercicios DR completados y documentados
- ✓ Tag **v1.0.0** publicado en producción

---

### ⚡ Q3 2026 — Optimización & Scale (S16+)

#### 🎯 Objetivos Clave
1. ✅ Performance & scale **10x** (validación y generación)
2. ✅ Roadmap **v2.0** definido (GraphQL, AsyncAPI, multi-tenant)
3. ✅ Developer Experience: CLI, plantillas, "one-command setup"

#### 📦 Áreas de Trabajo

| Área | Iniciativas | Targets |
|------|-------------|---------|
| ⚡ **Performance** | Paralelización, cache distribuido, optimización | `validation_p95 < 100ms` |
| 🔧 **SDK Generation** | Aceleración targets por lenguaje | Py: 30s, TS: 45s, Go: 25s, Java: 60s, .NET: 40s |
| 🛠️ **CLI & Tools** | `enis-contracts` CLI completa | scaffold, validate, diff, bump, release |
| 🔮 **v2.0 Features** | PoCs GraphQL, AsyncAPI, multi-tenant | RFCs aprobados, roadmap definido |
| 🎨 **Developer Experience** | Plantillas, auto-generated examples, StackBlitz | `docs_satisfaction ≥ 90%` |

#### 🏆 Hitos
- **H10:** `validation_latency_p95 < 100ms` alcanzado
- **H11:** CLI `enis-contracts` y DX suite publicados
- **H12:** Roadmap v2.0 con RFCs aprobados por stakeholders

#### ✅ Criterios de Salida
- ✓ `docs_satisfaction ≥ 90%` (NPS)
- ✓ `operational_efficiency ≥ 70%` vs baseline Q4'25
- ✓ Performance 10x vs baseline inicial
- ✓ Roadmap v2.0 aprobado y planificado

---

## 📦 Entregables y Definition of Done

### 📋 Épica: Governance & Versioning
**Entregables:**
- ✅ Política SemVer y **deprecation** (notice: 6m, sunset: 12m)
- ✅ RFCs con SLA (review: 72h, approval: 1w)
- ✅ Matriz de compatibilidad automatizada

**DoD:**
- Guía publicada en `/docs/API_GUIDELINES.md`
- Linter de versiones en pre-commit hooks
- Hooks de PR activos con validación automática

---

### 🔍 Épica: Validation Engine
**Entregables:**
- ✅ Jobs CI: `oasdiff`, `ajv-diff`, `buf breaking`, `tsc --noEmit`
- ✅ Scripts: `validate-xrefs.py`, `breaking-changes.py`, `baseline.py`
- ✅ Reporte consolidado automático

**DoD:**
- Gates obligatorios en todos los PRs
- Reporte consolidado visible en PRs y dashboard
- Baseline firmada con BLAKE2b + Cosign

---

### 🔧 Épica: SDKs Multi-lenguaje
**Entregables:**
- ✅ Generadores: Python, TypeScript, Go, Java, .NET
- ✅ Pipelines: generación, firma, publicación
- ✅ Ejemplos ejecutables por SDK

**DoD:**
- Paquetes publicados en repos internos/públicos
- Changelog automatizado con cada release
- Documentación API completa
- Ejemplos end-to-end ejecutables (≥ 90% coverage)

---

### 🛡️ Épica: Security & Supply Chain
**Entregables:**
- ✅ SBOM CycloneDX por SDK (Syft)
- ✅ Firmas digitales (Cosign/Sigstore)
- ✅ Verificación automática en CI
- ✅ Política de licencias aprobada

**DoD:**
- Release **bloqueado** si falta SBOM/firma
- Evidencias guardadas con retención ≥ 12 meses
- Auditoría reproducible E2E

---

### 📊 Épica: Observabilidad
**Entregables:**
- ✅ Exporters Prometheus (validación, gates, SDK builds)
- ✅ Dashboards Grafana (contratos, SDKs, breaking changes)
- ✅ SLOs definidos y monitoreados
- ✅ Alertas configuradas (Slack/Email/PagerDuty)

**DoD:**
- Alertas operacionales en producción
- SLOs cumplidos durante 4 semanas continuas
- Dashboard publicado y accesible al equipo

---

### 📚 Épica: Documentación & DX
**Entregables:**
- ✅ Guías: quickstart, versioning, validation, migration, troubleshooting
- ✅ Cookbooks por lenguaje
- ✅ CLI `enis-contracts`
- ✅ Ejemplos interactivos (StackBlitz/Colab)

**DoD:**
- ≥ 90% de ejemplos ejecutables
- Feedback rating ≥ 4.5/5 (NPS ≥ 85%)
- CLI publicada y documentada
- Portal DevPortal en producción

---

## 🚦 Quality Gates y Acceptance Criteria

Todos los PRs y releases deben pasar estos gates obligatorios:

| 🛡️ Gate | 📋 Criterio | 🎯 Umbral | 🚨 Criticidad |
|---------|-------------|-----------|--------------|
| **Security** | 0 vulnerabilidades High/Critical | Obligatorio | 🔴 Bloqueante |
| **Breaking Changes** | `oasdiff`/`buf` sin breaking changes | Obligatorio | 🔴 Bloqueante |
| **Validation** | Spectral + AJV + TSC sin errores | `success_rate ≥ 99.9%` | 🔴 Bloqueante |
| **Performance** | `latency_p95 < 100ms`, `throughput ≥ 5K req/s` | Por contrato crítico | 🟡 Warning |
| **Documentation** | 0 enlaces rotos, 90% ejemplos ejecutables | Obligatorio | 🔴 Bloqueante |
| **Compliance** | Evidencias completas y firmadas | Obligatorio (desde Q2 2026) | 🔴 Bloqueante |
| **Tests** | Coverage ≥ 80%, todos los tests pasando | Obligatorio | 🔴 Bloqueante |

---

## 👥 Organización y RACI

**Matriz de Responsabilidades** (A = Accountable · R = Responsible · C = Consulted · I = Informed)

| 👤 Rol | 📋 Governance | 🔍 Validación | 🔧 SDKs | 🛡️ Seguridad | 📊 Observabilidad | 📚 Docs |
|--------|--------------|--------------|---------|-------------|------------------|---------|
| **Contract Architect** | A/R | C | C | C | C | C |
| **Tech Leads (Services)** | C | A/R* | C | C | C | C |
| **SDK Engineers** | C | C | A/R | C | C | C |
| **Security/Compliance** | C | C | C | A/R | C | C |
| **DevRel/Docs** | C | C | C | C | C | A/R |
| **SRE/Platform** | C | C | C | C | A/R | C |
| **Product Manager** | C | I | I | I | I | C |

_* A/R por servicio específico_

### 📋 Descripción de Roles

| Rol | Responsabilidades Clave | FTE |
|-----|-------------------------|-----|
| **Contract Architect** | Diseño de contratos, governance, políticas SemVer, RFCs | 1.0 |
| **SDK Engineers** | Generación, testing, publicación SDKs (Py/TS/Go/Java/.NET) | 2.0-3.0 |
| **Platform/CI Engineer** | CI/CD, gates, automatización, infraestructura | 0.8-1.0 |
| **Security Engineer** | SBOM, firmas, auditoría, compliance | 0.2-1.0 |
| **Tech Writer/DevRel** | Documentación, ejemplos, developer experience | 0.2-1.0 |
| **SRE** | Observabilidad, dashboards, alertas, DR | 0.3-0.5 |

---

## ⚠️ Riesgos y Mitigaciones

### 🔴 Riesgos Críticos (Alta Prioridad)

| ID | 🚨 Riesgo | 📊 Impacto | 🎲 Prob. | 🛡️ Mitigación | 👤 Owner |
|----|-----------|-----------|---------|---------------|----------|
| **R-001** | Drift contratos ↔ servicios | 🔴 Alto | 🟡 Medio | Gates obligatorios + baseline firmada + alertas + Pact | Contract Architect |
| **R-002** | Breaking changes urgentes | 🔴 Alto | 🟢 Bajo | Freeze policy + hotfix path + RFC express (<24h) | Tech Leads |
| **R-003** | Dependencias externas bloqueadas | 🔴 Alto | 🟢 Bajo | Mocks (WireMock/Prism) + simuladores + contracts-first | Platform Lead |

### 🟡 Riesgos Moderados

| ID | 🚨 Riesgo | 📊 Impacto | 🎲 Prob. | 🛡️ Mitigación | 👤 Owner |
|----|-----------|-----------|---------|---------------|----------|
| **R-004** | Baja adopción de SDKs | 🟡 Medio | 🟡 Medio | DX/CLI + ejemplos reales + workshops + NPS tracking | SDK Lead |
| **R-005** | Deuda técnica en docs | 🟡 Medio | 🟡 Medio | Docs gate + owners por sección + OKRs | DevRel |
| **R-006** | Performance degradation | 🟡 Medio | 🟢 Bajo | Benchmarks + gates anti-regresión + monitoreo | SRE |

### 🟢 Riesgos Bajos

| ID | 🚨 Riesgo | 📊 Impacto | 🎲 Prob. | 🛡️ Mitigación |
|----|-----------|-----------|---------|---------------|
| **R-007** | Rotación de personal | 🟡 Medio | 🟢 Bajo | Documentación exhaustiva + pair programming + knowledge transfer |
| **R-008** | Tool/vendor lock-in | 🟢 Bajo | 🟢 Bajo | Open standards (OpenAPI/Protobuf) + abstracciones |

### 📋 Plan de Contingencia

**Trigger:** Si ocurre un riesgo crítico (R-001 a R-003)
1. 🚨 **Alertar** stakeholders inmediatamente (< 1h)
2. 🔍 **Evaluar** impacto y opciones (< 4h)
3. 🛠️ **Ejecutar** plan de mitigación (< 24h)
4. 📊 **Reportar** lecciones aprendidas (< 1 semana)

---

## 💰 Presupuesto y Recursos

### 👥 Headcount (12 meses)

| Trimestre | Roles | FTE Total | Costo Estimado* |
|-----------|-------|-----------|-----------------|
| **Q4 2025** | Contract Arch (1) + SDK Eng (2) + Platform (0.8) + Security (0.2) + Writer (0.2) | 4.2 | $180K-$250K |
| **Q1 2026** | + SDK Eng Go/Java/.NET (1) + DevRel (0.5) | 5.7 | $240K-$340K |
| **Q2 2026** | + Compliance (1) | 6.7 | $280K-$400K |
| **Q3 2026** | + Performance Eng (1) | 7.7 | $320K-$460K |
| **Promedio Anual** | | **6.1 FTE** | **$255K-$363K** |

_* Basado en salarios promedio senior: $50K-$75K/año por FTE_

### 🏗️ Infraestructura (12 meses)

| Categoría | Componentes | Costo Mensual | Costo Anual |
|-----------|-------------|---------------|-------------|
| **CI/CD** | GitHub Actions runners, storage, bandwidth | $1,500-$2,500 | $18K-$30K |
| **Observabilidad** | Grafana Cloud, Prometheus, Loki, Tempo | $800-$1,500 | $10K-$18K |
| **Security** | Cosign, Syft, Trivy, vulnerability scanning | $500-$1,000 | $6K-$12K |
| **Testing** | Pact Broker, mock servers, test infrastructure | $300-$800 | $4K-$10K |
| **Storage** | Artifact registry, backups, SBOM storage | $400-$700 | $5K-$8K |
| **Total Mensual** | | **$3,500-$6,500** | **$43K-$78K** |

### 🎯 Otros Costos

| Item | Cuándo | Costo Estimado |
|------|--------|----------------|
| **Auditoría de Seguridad** | Q2 2026 | $25K-$40K |
| **Certificación ISO/SOC2** | Q2 2026 | $15K-$30K |
| **Training & Workshops** | Continuo | $10K-$20K |
| **Herramientas & Licencias** | Anual | $5K-$10K |

### 💵 Resumen Presupuesto Anual

```
👥 Headcount:           $255K - $363K
🏗️ Infraestructura:     $43K  - $78K
🎯 Otros:               $55K  - $100K
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 TOTAL ANUAL:        $353K - $541K
```

---

## 📢 Comunicación y Cadencia

### 📅 Reuniones Regulares

| Frecuencia | Tipo | Duración | Participantes | Objetivo |
|------------|------|----------|---------------|----------|
| **Semanal** | Sprint Standup | 30 min | Equipo Core | Status, blockers, próximos pasos |
| **Bisemanal** | Sprint Review/Demo | 45 min | Equipo + Stakeholders | Demo funcionalidades, feedback |
| **Bisemanal** | Sprint Planning | 60 min | Equipo Core | Planificación próximo sprint |
| **Mensual** | KPIs & Risk Review | 60 min | Equipo + Leadership | Métricas, riesgos, ajustes |
| **Trimestral** | Roadmap & OKR Review | 90 min | Todos + Stakeholders | Revisión trimestral, OKRs |

### 📱 Canales de Comunicación

| Canal | Propósito | Respuesta SLA |
|-------|-----------|---------------|
| **#agent-contracts-dev** (Slack) | Desarrollo diario, preguntas técnicas | < 2h (horario laboral) |
| **#contracts-alerts** (Slack) | Alertas automáticas (CI, breaking changes) | Inmediato |
| **#contracts-announcements** (Slack) | Releases, cambios importantes | Broadcast |
| **contracts-team@** (Email) | Comunicación formal, decisiones | < 24h |
| **Weekly Newsletter** | Resumen semanal para stakeholders | Viernes 4pm |

### 📊 Reportes

| Tipo | Frecuencia | Audiencia | Contenido |
|------|------------|-----------|-----------|
| **Sprint Report** | Bisemanal | Equipo + PM | Completados, WIP, blockers, próximos |
| **KPI Dashboard** | Continuo | Todos | Métricas en tiempo real (Grafana) |
| **Monthly Status** | Mensual | Leadership | Progreso, riesgos, presupuesto, ajustes |
| **Quarterly Review** | Trimestral | Stakeholders | OKRs, roadmap, planificación próximo Q |

### 📝 Plantillas y Herramientas

- **Wiki**: Confluence space "Agent Contracts"
- **Plantillas**: RFC.md, DesignDoc.md, Runbook.md, PostMortem.md
- **Status Page**: [status.enis.io/contracts](https://status.enis.io/contracts) (público)
- **Dashboards**: Grafana (métricas), GitHub Projects (tracking)

---

## 📊 Hoja de Ruta Visual

### Gantt Simplificado (12 meses)

```
Trimestre    │ Sprint │ Fase Principal         │ Hitos Clave
─────────────┼────────┼────────────────────────┼──────────────────────────────
Q4 2025      │ S0-S6  │ 🏗️ FOUNDATIONS         │ ► H1: Pipelines operacionales
Oct-Dic      │        │ ████████████████       │ ► H2: Tag v1.0.0 contratos
             │        │                        │ ► H3: SDKs alpha (Py/TS)
─────────────┼────────┼────────────────────────┼──────────────────────────────
Q1 2026      │ S7-S12 │ 🚀 GA & SCALE          │ ► H4: SDKs Py/TS GA
Ene-Mar      │        │ ████████████████       │ ► H5: 15+ OpenAPI validadas
             │        │                        │ ► H6: SLOs activos
─────────────┼────────┼────────────────────────┼──────────────────────────────
Q2 2026      │ S13-15 │ 🏢 ENTERPRISE          │ ► H7: 5 SDKs GA (todos)
Abr-Jun      │        │ ████████████████       │ ► H8: Compliance pack
             │        │                        │ ► H9: DR aprobado, v1.0.0 PROD
─────────────┼────────┼────────────────────────┼──────────────────────────────
Q3 2026      │ S16+   │ ⚡ OPTIMIZATION         │ ► H10: Performance 10x
Jul-Sep      │        │ ████████████████       │ ► H11: CLI publicada
             │        │                        │ ► H12: Roadmap v2.0 aprobado
```

### Timeline por Workstream

```
Workstream            │ Q4'25      │ Q1'26      │ Q2'26      │ Q3'26
──────────────────────┼────────────┼────────────┼────────────┼────────────
🔒 Contracts Core     │ ████████   │ ██         │            │
📝 OpenAPI/Schema     │ ██████     │ ████       │ ██         │
🔧 SDKs Py/TS         │ ████       │ ████████   │ ██         │
🏢 SDKs Go/Java/.NET  │            │ ██████     │ ████████   │ ██
🔐 Validation Engine  │ ██████     │ ██         │            │
🛡️ Security/SBOM      │ ████       │ ██         │ ████████   │
📊 Observabilidad     │ ██████     │ ████       │ ██         │ ██
📚 Docs & DX          │ ████       │ ████       │ ████       │ ████████
🎛️ Macro-Módulos      │            │ ██████     │            │
🔮 v2.0 Features      │            │            │            │ ██████
```

---

## 📚 Políticas Operativas

### 🔒 Definition of Ready (DoR)

Para que una historia entre al sprint:
- ✅ **User story** clara con criterios de aceptación
- ✅ **Mocks/fixtures** listos si hay dependencias externas
- ✅ **Estimación** completada (story points)
- ✅ **Riesgos** identificados y owner asignado
- ✅ **Dependencias** técnicas resueltas o bloqueadas explícitamente

### ✅ Definition of Done (DoD)

Para dar por completada una historia:
- ✅ **Código** implementado y revisado (PR aprobado)
- ✅ **Tests** escritos y pasando (coverage ≥ 80%)
- ✅ **CI verde** (lint, validate, build, security)
- ✅ **Documentación** actualizada (código + docs/)
- ✅ **Ejemplos** ejecutables si aplica
- ✅ **Demo** presentada en sprint review

### 🔄 Capacity Planning

- **Velocity baseline**: 45 story points por sprint (bisemanal)
- **Deuda técnica**: Máximo 20% de capacidad por sprint
- **Buffers**: 15% para riesgos e imprevistos
- **Innovación**: 10% para exploración y mejoras

### 🚀 Release Process

**Release Checklist:**
1. ✅ Lint verde (spectral, ajv, buf, tsc)
2. ✅ Validación completa pasada
3. ✅ Baseline firmada actualizada
4. ✅ SBOM generado por SDK
5. ✅ Firmas Cosign aplicadas
6. ✅ Tests de integración verdes
7. ✅ Docs actualizadas (changelog)
8. ✅ Anuncio en #contracts-announcements

**Deprecation Policy:**
- **Notice mínimo**: 6 meses antes del sunset
- **Sunset**: 12 meses después del notice
- **Comunicación**: Issues, headers HTTP, changelog, newsletter

---

## 📎 Apéndices

### A) Matriz de Contratos v1.x

| Tipo | Contratos | Total |
|------|-----------|-------|
| **OpenAPI 3.0** | inference, agents, events, federation, nops, asm, cgn, awe, shif, billing, lifecycle, scorecard, compliance | 15+ |
| **JSON Schema** | agent-registration, inference-request, event, policy, federation, validation-rules, migration-guides, compatibility-matrix | 8+ |
| **Protobuf** | inference.proto, agents.proto, events.proto, federation.proto | 4 |
| **SDKs** | Python, TypeScript, Go, Java, .NET | 5 |

### B) Jobs CI/CD (nomenclatura estándar)

```yaml
# Validation
- contracts-validate          # Spectral + AJV + TSC
- contracts-breaking          # oasdiff + buf breaking
- contracts-baseline          # BLAKE2b hash + Cosign verify

# SDKs
- sdks-build-sign-sbom        # Generate, build, sign, SBOM
- examples-smoke              # Run all examples
- pact-verify                 # Contract testing (consumer)
- pact-publish                # Publish Pact contracts

# Quality
- security-scan               # Trivy + Syft
- performance-bench           # Benchmarks anti-regresión
```

### C) Scope Caps Q4 2025

```yaml
q4_2025_scope_caps:
  endpoints_caps:
    inference.yaml: { total_max: 12, s3_freeze: 8, s6_freeze: 12 }
    agents.yaml:    { total_max: 16, s3_freeze: 8, s6_freeze: 16 }
    events.yaml:    { total_max: 10, s3_freeze: 6, s6_freeze: 10 }
    nops.yaml:      { total_max: 18, s3_freeze: 10, s6_freeze: 18 }
  sdks_alpha:
    - python
    - typescript
  deferred_to_q1_26:
    - sdk_go
    - sdk_java
    - sdk_dotnet
  out_of_scope_q4:
    - graphql schemas
    - asyncapi
    - multi-tenant contracts
```

### D) Mock Strategy (S1)

```yaml
dependency_management:
  mock_strategy:
    s1_setup:
      nops_kernel:
        tool: "WireMock"
        surfaces: ["event-bus", "state", "agents"]
        healthcheck: "http://localhost:8080/__admin/health"
      inference_service:
        tool: "Prism"
        surfaces: ["predict", "models", "status"]
        healthcheck: "http://localhost:4010/health"
      integration_apis:
        tool: "Prism"
        surfaces: ["gateway", "authN", "authZ"]
        healthcheck: "http://localhost:4011/health"
```

### E) KPIs Baseline Plan

```yaml
kpi_baseline_plan:
  s1_measures:
    - time_to_first_api_call
    - validation_latency_p95
    - docs_satisfaction_survey (n≥20)
  s2_targets:
    time_to_first_api_call: "baseline × 0.8"
    validation_latency_p95: "baseline × 0.8"
    docs_satisfaction: "baseline + 10pp"
  quarterly_targets:
    q4_2025: "baseline + 20%"
    q1_2026: "baseline + 50%"
    q2_2026: "baseline + 80%"
    q3_2026: "target final (90%+)"
  ci_gates:
    regression_fail_if: "p95 > baseline × 1.2"
```

### F) Sprint 1 Exit Criteria

```yaml
sprint_1_exit_criteria:
  technical:
    ci_green: true
    mock_servers_healthy: ["wiremock", "prism"]
    baseline_signed: true
  governance:
    semver_policy_approved: true
    rfc_001_merged: true
  contracts:
    drafts:
      inference.yaml: "≥ 5 endpoints"
      agents.yaml: "≥ 3 endpoints"
      event-schema.json: "present"
  telemetry:
    time_to_first_api_call_baseline: "measured"
    validation_latency_p95_baseline: "measured"
```

### G) Release Trains & Freezes

**Tren actual:** `R-NEXT`

**Hitos estándar:**
- `RC1` (S6) → Release Candidate 1
- `GA` (S15) → General Availability v1.0.0

**Marcadores de congelamiento:**
- `FREEZE:S3` → Cierre de alcance para endpoints núcleo
- `FREEZE:S6` → Feature-freeze rumbo a GA

> **Nota:** Sin fechas fijas; el tren activo cambia por etiqueta según planning.

---

## 🎯 Próximos Pasos Inmediatos

### Para empezar AHORA (Sprint 0):

1. 📋 **Crear estructura de repositorio**
   ```bash
   mkdir -p agent-contracts/{openapi/v1,schemas,proto,sdks,scripts,tests,docs}
   ```

2. 🔧 **Configurar CI/CD básico**
   - GitHub Actions workflows
   - Pre-commit hooks
   - Docker multi-stage

3. 📝 **Documentación inicial**
   - README.md con quickstart
   - CONTRIBUTING.md
   - LICENSE (propietario ANDAON)

4. 👥 **Formar equipo core**
   - Contract Architect (lead)
   - 2 SDK Engineers
   - 1 Platform Engineer

5. 📊 **Setup herramientas**
   - Slack channels (#agent-contracts-dev, #contracts-alerts)
   - GitHub Projects (tracking)
   - Confluence space

---

## 📚 Glosario de Términos ENIS v3.0

> **Referencia**: Master Prompt 30 - Terminología DNA v3.0  
> **Fuente**: `docs/00-enis-complete/DNA_V3_SPECIFICATION.md`

### **Términos Arquitectónicos**

| Término | Definición | Contexto en Agent-Contracts |
|---------|------------|----------------------------|
| **DNA v3.0** | Design & Architecture v3.0 - Arquitectura base de ENIS | Compliance mandatorio en todos los contratos |
| **Agent Contracts** | Repositorio centralizado de contratos (OpenAPI/Proto/Schemas) | Este repositorio |
| **NOPS Kernel** | Neural Operations Kernel - Control plane slim para edge | Consumer crítico de contratos: events.proto, nops.yaml |
| **ASM** | Adaptive State Manager - Gestión de estado adaptativa | Macro-módulo con contratos en S12: asm.yaml |
| **CGN** | Causal Graph Navigator - Navegación de grafos causales | Macro-módulo con contratos en S12: cgn.yaml |
| **AWE** | Autonomous Workflow Evolution - Evolución autónoma de workflows | Macro-módulo con contratos en S12: awe.yaml |
| **SHIF** | System-Human Integration Fabric - Integración sistema-humano | Macro-módulo con contratos en S12: shif.yaml |
| **RGM** | Resource Governance Module - Gobernanza de recursos | NOPS module: quotas, fairness |
| **ALM** | Agent Lifecycle Manager - Gestión de ciclo de vida de agents | NOPS module: deploy, rollback |
| **DGE** | Data Governance Engine - Motor de gobernanza de datos | Clasificación PII/PHI/PCI |

### **Términos de Contratos**

| Término | Definición | Ubicación en Repo |
|---------|------------|-------------------|
| **OpenAPI 3.0** | Especificación estándar para APIs REST | `contracts/openapi/v1/*.yaml` |
| **JSON Schema** | Esquemas de validación de payloads | `contracts/schemas/*.json` |
| **Protocol Buffers (Proto)** | Contratos para gRPC y streaming | `contracts/proto/*.proto` |
| **Golden Samples** | Ejemplos request/response completos y validados | `contracts/openapi/v1/examples/` |
| **Baseline** | Hash BLAKE2b firmado de todos los contratos | `.baseline/baseline.json` |
| **Breaking Change** | Cambio incompatible con versión anterior | Detectado por oasdiff/buf |
| **Deprecation** | Marcado de endpoint/field para sunset futuro | Notice 6m, sunset 12m |
| **FREEZE** | Período de congelamiento de cambios | FREEZE:S3 (core), FREEZE:S6 (GA) |

### **Términos de Validación**

| Término | Definición | Herramienta |
|---------|------------|-------------|
| **Spectral** | Linter de OpenAPI con reglas custom | Spectral 6.11.0 |
| **AJV** | Validador de JSON Schema | AJV 8.12.0 |
| **Buf** | Linter y breaking detector de Protocol Buffers | Buf 1.28.1 |
| **oasdiff** | Detector de breaking changes en OpenAPI | oasdiff 1.10.10 |
| **Drift Detection** | Detección de desviación entre spec y runtime | Job `contracts-drift-check` |
| **Cross-reference Validation** | Validación de `$ref` entre specs | Script `validate-xrefs.py` |

### **Términos de SDKs**

| Término | Definición | Sprints |
|---------|------------|---------|
| **SDK Alpha** | Versión interna pre-release (privada) | S3 - Solo registry interno |
| **SDK Beta** | Versión para testing limitado | S11 - Go/Java/.NET |
| **SDK GA** | General Availability - Versión pública estable | S13 - Py/TS; S15 - Todos |
| **Registry Interno** | Repositorio privado de paquetes (PyPI/npm interno) | S3+ |
| **Anti-leak Policy** | Política que previene publicación pública accidental | S3 - Gate en workflow |
| **Feature Parity** | Igualdad de funcionalidades entre SDKs | Matrix en S11 |
| **SBOM** | Software Bill of Materials - Lista de dependencias | CycloneDX, generado con Syft |

### **Términos de Testing**

| Término | Definición | Ubicación |
|---------|------------|-----------|
| **Pact** | Consumer-driven contract testing | contracts/pact/, S7 |
| **can-i-deploy** | Comando Pact para verificar compatibilidad pre-deploy | Gate obligatorio en S7 |
| **Pact Broker** | Servidor centralizado de contratos Pact | URL interna, cloud-ops |
| **Mock Server** | Servidor simulado para desarrollo/testing | Prism (Inference), WireMock (NOPS) |
| **Smoke Test** | Test básico de funcionalidad | Job `examples-smoke` |
| **Golden Test** | Test con output esperado fijo y versionado | `tests/golden/` |

### **Términos de Seguridad**

| Término | Definición | Sprint |
|---------|------------|--------|
| **Cosign** | Herramienta de firma digital (Sigstore) | S0 setup, S6 mandatorio |
| **Syft** | Generador de SBOM | S6+ |
| **Trivy** | Escáner de vulnerabilidades | S0 informativo, S6+ bloqueante |
| **Semgrep** | SAST - Análisis estático de código | S0 informativo, S6+ bloqueante |
| **Waiver** | Excepción documentada para vulnerabilidad | Requiere aprobación Security Lead |
| **mTLS** | Mutual TLS - Autenticación bidireccional | MCP security (S17) |
| **HSM** | Hardware Security Module - Almacenamiento seguro de claves | Producción (S6+) |

### **Términos de Governance**

| Término | Definición | Documento |
|---------|------------|-----------|
| **RFC** | Request for Comments - Propuesta de cambio | Template en S4 |
| **Emergency RFC** | RFC con SLA acelerado (< 24h) para critical patches | `docs/01-sprint/S1/CHANGE-POLICY.md` |
| **DoR** | Definition of Ready - Criterios para entrar a sprint | Governance S4 |
| **DoD** | Definition of Done - Criterios de completitud | Por sprint |
| **RACI** | Responsible, Accountable, Consulted, Informed | `docs/01-sprint/S4/RACI.md` |
| **CODEOWNERS** | Ownership de código por directorio | `docs/01-sprint/S4/CODEOWNERS` |
| **SemVer** | Semantic Versioning - X.Y.Z | Mayor.Minor.Patch |

### **Términos de Observabilidad**

| Término | Definición | Sprint |
|---------|------------|--------|
| **SLO** | Service Level Objective - Objetivo de nivel de servicio | S5 |
| **MTTR** | Mean Time To Recovery - Tiempo promedio de recuperación | Target < 30min (S9) |
| **p95** | Percentil 95 - 95% de requests bajo este valor | Métricas de latencia |
| **NPS** | Net Promoter Score - Satisfacción de desarrolladores | Target ≥ 85% (S5), ≥ 90% (S13) |
| **Drift Rate** | Tasa de desviación entre spec y runtime | Target ≤ 0.5% semanal |

### **Términos de Compliance**

| Término | Definición | Sprint |
|---------|------------|--------|
| **Audit Trail** | Registro auditable de cambios y decisiones | S6+ automático |
| **Compliance Pack** | Conjunto de evidencias para auditoría | S14 - compliance-pack.zip |
| **Retención** | Período de almacenamiento de evidencias | ≥ 12 meses (S6+) |
| **ISO/SOC2** | Estándares de certificación | S14 readiness |
| **Evidence** | Evidencia auditable (SBOM, firma, logs, Pact) | Automatizada desde S6 |

### **Términos de Releases**

| Término | Definición | Sprint |
|---------|------------|--------|
| **Alpha** | Versión pre-release interna | S3 - Py/TS |
| **Beta** | Versión para testing extendido | S11 - Go/Java/.NET |
| **RC** | Release Candidate - Versión pre-GA | S13 - 1.0.0-rc.1 |
| **GA** | General Availability - Versión producción | S15 - v1.0.0 |
| **Sunset** | Fecha de retiro de endpoint/feature deprecated | 12 meses desde notice |

### **Términos de MCP (Model Context Protocol)**

| Término | Definición | Sprint |
|---------|------------|--------|
| **MCP** | Model Context Protocol - Protocolo para tool invocation | S17-S19 (Post-GA) |
| **Tool Catalog** | Catálogo de herramientas disponibles vía MCP | S17 |
| **Invocation Contract** | Contrato de invocación de herramientas con params tipados | S17 |
| **Egress Guard** | Guardia de salida para prevenir leaks de PII | S19 |
| **Allow-list** | Lista de herramientas aprobadas para uso | S19 |

### **Acrónimos Técnicos**

| Acrónimo | Significado Completo |
|----------|---------------------|
| **ENIS** | Enterprise Neural Intelligence Systems |
| **DNA** | Design & Architecture |
| **NOPS** | Neural Operations |
| **CI/CD** | Continuous Integration / Continuous Deployment |
| **SBOM** | Software Bill of Materials |
| **SLSA** | Supply-chain Levels for Software Artifacts |
| **CVSS** | Common Vulnerability Scoring System |
| **JWT** | JSON Web Token |
| **SSE** | Server-Sent Events |
| **gRPC** | Google Remote Procedure Call |
| **TLS** | Transport Layer Security |
| **PII** | Personally Identifiable Information |
| **PHI** | Protected Health Information |
| **PCI** | Payment Card Industry |

---

## 📅 Timeline Visual con Hitos Arquitectónicos

### **2025-2026 Roadmap (Sprints Bisemanales)**

> **Timezone**: America/Tegucigalpa (UTC-6)  
> **Cadencia**: Sprints de 2 semanas (10 días hábiles)  
> **Modelo**: Agile con gates de calidad

```
Q4 2025 ────────────────────────────────────────────────────────────────
Oct │ Nov │ Dec │
────┼─────┼─────┤
S0  │ S1  │ S2  │ S3  │ S4  │ S5  │ S6  │
────┴─────┴─────┴─────┴─────┴─────┴─────┘
 ▲     ▲     ▲     ▲           ▲     ▲
 │     │     │     │           │     │
 │     │     │     │           │     └─ 🛡️ SEC: SBOM + Firmas
 │     │     │     │           └─────── 📊 Observabilidad: SLOs
 │     │     │     └─────────────────── 🔧 SDKs Alpha (Py/TS)
 │     │     └───────────────────────── 🔐 Baseline Firmada
 │     └─────────────────────────────── 📝 Contratos Core
 └───────────────────────────────────── ⚙️  Repo Bootstrap

🎯 Hito Q4'25: Fundaciones + Contratos v1.0.0 + SDKs Alpha


Q1 2026 ────────────────────────────────────────────────────────────────
Ene │ Feb │ Mar │
────┼─────┼─────┤
Buffer│ S7  │ S8  │ S9  │ S10 │ S11 │ S12 │
──────┴─────┴─────┴─────┴─────┴─────┴─────┘
🎄     ▲     ▲     ▲     ▲     ▲     ▲
       │     │     │     │     │     │
       │     │     │     │     │     └─ 🎛️  Macro-Módulos: ASM/CGN/AWE/SHIF
       │     │     │     │     └─────── 🏢 SDKs Enterprise (Go/Java/.NET)
       │     │     │     └─────────── 🛠️  CLI enis-contracts MVP
       │     │     └───────────────── 📚 Troubleshooting & On-call
       │     └─────────────────────── ⚙️  Mocks Vivos
       └───────────────────────────── 🤖 Pact: can-i-deploy

🎯 Hito Q1'26: Macro-Módulos + SDKs Beta + CLI


Q2 2026 ────────────────────────────────────────────────────────────────
Abr │ May │ Jun │
────┼─────┼─────┤
S13 │ S14 │ S15 │ S16 │
────┴─────┴─────┴─────┘
 ▲     ▲     ▲     ▲
 │     │     │     │
 │     │     │     └─────────────────── 🔮 Optimización 10x + v2.0
 │     │     └─────────────────────── 🎉 GA v1.0.0 + Operations Guide
 │     └───────────────────────────── 📜 Compliance Pack ISO/SOC2
 └─────────────────────────────────── 🚀 Customer Beta + SDKs GA

🎯 Hito Q2'26: GA v1.0.0 + Compliance + Enterprise Ready


Q3 2026 (Opcional - MCP) ───────────────────────────────────────────────
Jul │ Ago │ Sep │
────┼─────┼─────┤
S17 │ S18 │ S19 │
────┴─────┴─────┘
 ▲     ▲     ▲
 │     │     │
 │     │     └─────────────────────── 🛡️  MCP Pilots + Hardening
 │     └─────────────────────────── 🔌 MCP SDK Adapters
 └───────────────────────────────── 🔬 MCP Discovery (Spike)

🎯 Hito Q3'26: MCP Integration (Opcional Post-GA)
```

### **Hitos Arquitectónicos Clave**

| Hito | Fecha Target | Sprint | Entregable Principal | Dependencias Arquitectónicas |
|------|--------------|--------|---------------------|------------------------------|
| **H1** | 2025-11-09 | S1 | **Contratos v1.0.0** publicados | Master Prompt 30, DNA v3.0 |
| **H2** | 2025-11-23 | S2 | **Baseline firmada** operativa | Cosign keys, Security architecture |
| **H3** | 2025-12-07 | S3 | **SDKs Alpha** (Py/TS) internos | Registry interno, anti-leak policy |
| **H4** | 2025-12-21 | S6 | **SBOM + Firmas** mandatorias | Supply chain security setup |
| **Buffer** | 2025-12-22 → 2026-01-05 | - | Hotfix/Soporte | Fin de año |
| **H5** | 2026-01-18 | S7 | **Pact can-i-deploy** como gate | Pact Broker, consumer contracts |
| **H6** | 2026-02-15 | S10 | **CLI enis-contracts** MVP | SDKs, Pact, baseline integrados |
| **H7** | 2026-03-15 | S12 | **Macro-Módulos** con sign-off | ASM/CGN/AWE/SHIF Tech Leads |
| **H8** | 2026-04-15 | S13 | **Customer Beta** + SDKs GA (Py/TS) | Beta partners, feedback loop |
| **H9** | 2026-05-15 | S14 | **Compliance Pack** ISO/SOC2 ready | Evidencias automatizadas desde S6 |
| **H10** | 2026-06-15 | S15 | **🎉 GA v1.0.0** - Production Release | TODOS los sprints anteriores |
| **H11** | 2026-06-30 | S16 | **Performance 10x** + v2.0 Roadmap | Benchmarks, optimizaciones |
| **H12** | 2026-07-31 | S17 | **MCP Spike** completado | GA v1.0.0 estable |
| **H13** | 2026-08-31 | S18 | **MCP SDKs** beta | MCP contracts validados |
| **H14** | 2026-09-30 | S19 | **MCP Pilots** con hardening | Security compliance |

### **Milestones de Integración con 24 Repos**

```
Timeline de Integración Cross-Repo:

S1  ─────► Contratos disponibles para:
            - inference-service
            - nops-kernel
            - edge-agents

S7  ─────► Pact contracts publicados:
            - Inference Service (provider verification)
            - NOPS Kernel (provider verification)

S12 ─────► Contratos Macro-Módulos disponibles:
            - asm-service
            - cgn-service
            - awe-service
            - shif-service

S13 ─────► SDKs GA disponibles para:
            - developer-portal (documentación)
            - agent-marketplace (integración)
            - enis-studio (desarrollo)

S15 ─────► TODOS los 23 repos pueden consumir:
            - 15+ OpenAPI specs
            - 8+ JSON Schemas
            - 5 SDKs (Py/TS/Go/Java/.NET)
            - Pact contracts verificados
```

---

## 📋 APÉNDICES TRANSVERSALES - GAPS CONSOLIDADOS

### A) Breaking Change Policy (Clarificación Completa)

```yaml
breaking_change_policy:
  freeze_s3:
    scope: "Breaking changes en endpoints core (inference, agents, events, nops)"
    enforcement: "Gate `oasdiff` bloquea PR si detecta breaking sin RFC aprobado"
    applies_to: "Cambios en schemas, paths, métodos HTTP, campos required"
    not_applies_to: "Endpoints nuevos, campos opcionales, deprecations documentadas"
  
  deprecation:
    notice_period: "6 meses mínimo antes de sunset"
    sunset_period: "12 meses desde notice inicial"
    documentation:
      - "Marcar en spec: deprecated: true + x-sunset-date: YYYY-MM-DD"
      - "Header HTTP: X-API-Deprecated: true; sunset=YYYY-MM-DD"
      - "Issue en repo con label deprecation + milestone"
      - "Changelog entry con severity: BREAKING"
      - "Newsletter semanal + Slack #contracts-announcements"
      - "Migration guide en docs/migrations/"
  
  emergency_rfc:
    trigger: 
      - "Critical security vulnerability (CVSS ≥ 7.0)"
      - "Production incident P0 que requiere breaking change"
      - "Regulatory compliance crítica"
    sla: 
      approval: "< 24h desde creación RFC"
      notification: "Inmediata a stakeholders"
      implementation: "< 48h desde aprobación"
    bypass: 
      - "Permite skip de FREEZE:S3 y FREEZE:S6 con justificación"
      - "Requiere aprobación Contract Architect + Security Lead"
    post_mortem: "Mandatorio dentro de 72h con RCA y preventive actions"
  
  communication_plan:
    pre_breaking:
      - "RFC abierto ≥ 2 semanas antes de implementación (normal flow)"
      - "Email directo a tech leads de servicios afectados"
      - "Actualización de SDK examples con código viejo y nuevo"
    post_breaking:
      - "Release notes detalladas con before/after"
      - "Office hours para Q&A (2 sesiones)"
      - "Monitoring de adoption rate durante 4 semanas"
```

### B) Owners/Roles Nominales (Actualizar en `docs/RACI.md`)

**Template para asignar nombres reales:**

| Rol | Persona(s) | Email | Slack | Backup |
|-----|-----------|-------|-------|--------|
| **Contract Architect** | `[TBD]` | contracts-arch@andaon.com | @contracts-arch | `[TBD]` |
| **Security Lead** | `[TBD]` | security-lead@andaon.com | @sec-lead | `[TBD]` |
| **DX Lead** | `[TBD]` | dx-lead@andaon.com | @dx-lead | `[TBD]` |
| **Release Manager** | `[TBD]` | release-mgr@andaon.com | @release-mgr | `[TBD]` |
| **Platform Engineer** | `[TBD]` | platform-eng@andaon.com | @platform-eng | `[TBD]` |
| **SDK Engineers** | `[TBD]` (×2-3) | sdk-team@andaon.com | @sdk-team | `[TBD]` |
| **Compliance Lead** | `[TBD]` | compliance@andaon.com | @compliance | `[TBD]` |
| **On-call Lead** | `[TBD]` (rotation) | oncall@andaon.com | @oncall | Rotation schedule |
| **Performance Engineer** | `[TBD]` | perf-eng@andaon.com | @perf-eng | `[TBD]` |

**Responsabilidades críticas por rol:**

- **Contract Architect**: Aprobar RFCs, firmar baseline, definir deprecation timeline
- **Security Lead**: Firmar artefactos (backup), aprobar exemptions, key management
- **DX Lead**: CLI ownership, docs satisfaction (NPS), SDK usability
- **Release Manager**: Coordinar releases v1.x, comunicación stakeholders, GA checklist
- **On-call**: MTTR incidents, runbooks updates, escalation a Security/Platform

### C) KPIs Consolidados (Tracker en Dashboard)

```yaml
kpis_consolidated:
  validation:
    runtime_p95: 
      target: "≤ 100ms"
      measurement: "scripts/bench/validation-bench.py"
      alert_threshold: "> 150ms"
    ci_pack_p95: 
      target: "≤ 1.2s"
      measurement: "GitHub Actions workflow duration"
      alert_threshold: "> 2.0s"
    success_rate: 
      target: "≥ 99.9%"
      measurement: "CI pass rate últimos 30 días"
      alert_threshold: "< 98%"
  
  sdk_builds:
    python_p95: 
      target: "≤ 30s"
      stretch: "≤ 20s (S16)"
    typescript_p95: 
      target: "≤ 25s"
      stretch: "≤ 18s (S16)"
    go_p95: 
      target: "≤ 35s"
      stretch: "≤ 25s (S16)"
    java_p95: 
      target: "≤ 60s"
      stretch: "≤ 45s (S16)"
    dotnet_p95: 
      target: "≤ 40s"
      stretch: "≤ 30s (S16)"
    success_rate: 
      target: "≥ 95%"
      alert_threshold: "< 90%"
  
  drift:
    rate_weekly: 
      target: "≤ 0.5%"
      measurement: "contracts-drift-check diff percentage"
      alert_threshold: "> 1%"
    detection_latency: 
      target: "< 1h desde commit"
      measurement: "Time from PR merge to drift alert"
  
  breaking_changes:
    in_main: 
      target: "= 0"
      enforcement: "oasdiff + buf breaking gates"
      exception_path: "Emergency RFC only"
    detection_rate: 
      target: "100%"
      measurement: "Breaking changes caught pre-merge / total attempts"
  
  documentation:
    satisfaction_nps: 
      s5_target: "≥ 85%"
      s13_target: "≥ 90%"
      measurement: "Quarterly developer surveys (n ≥ 30)"
    examples_executable: 
      target: "≥ 90%"
      measurement: "examples-smoke pass rate"
    links_broken: 
      target: "= 0"
      measurement: "Weekly link checker job"
  
  time_to_first_api_call:
    target: "≤ 10 minutes"
    measurement: 
      - "Onboarding telemetry (opt-in)"
      - "User surveys post-quickstart"
      - "Time from SDK install to successful API call"
    segments:
      python: "≤ 8 min"
      typescript: "≤ 9 min"
      go: "≤ 12 min"
  
  contract_coverage:
    target: "100% servicios core"
    measurement: "Services with published contracts / Total core services"
    core_services:
      - inference-service
      - nops-kernel
      - edge-agents
      - asm-service
      - cgn-service
      - observability-service
      - billing-service
      - compliance-service
```

### D) Alerting & Escalation Matrix

```yaml
alerting_escalation:
  severity_levels:
    P0_CRITICAL:
      examples: 
        - "Breaking change merged to main sin RFC"
        - "Security vulnerability High/Critical detectada"
        - "Baseline compromise o firma inválida"
        - "Pact verification fail en deployment producción"
      response_time: "< 15 min"
      escalation_path:
        primary: "PagerDuty → On-call"
        secondary: "Security Lead (si sec vuln)"
        tertiary: "Contract Architect"
      notification_channels:
        - "PagerDuty (SMS + Call)"
        - "Slack #contracts-alerts (mention @channel)"
        - "Email a contracts-team@ + leadership@"
      actions:
        - "Rollback inmediato si es deployment"
        - "Block PR si es pre-merge"
        - "Incident Commander asignado"
        - "War room en Slack #incident-{id}"
    
    P1_HIGH:
      examples:
        - "Validation fail rate > 5% últimas 2h"
        - "SDK build fail rate > 10% últimas 24h"
        - "Drift rate > 1% detectado"
        - "SLO breach: validation success < 99%"
      response_time: "< 1h"
      escalation_path:
        primary: "Slack mention → On-call"
        secondary: "Contract Architect"
      notification_channels:
        - "Slack #contracts-alerts (mention @oncall)"
        - "Email a contracts-team@"
      actions:
        - "Investigar root cause"
        - "Update status page si user-facing"
        - "Create incident ticket"
    
    P2_MEDIUM:
      examples:
        - "Lint errors increasing trend (>20% week-over-week)"
        - "Mock desync detected (drift < 1% pero > 0)"
        - "Performance regression (p95 > baseline × 1.1)"
        - "Docs satisfaction NPS drop > 5pp"
      response_time: "< 4h business hours"
      escalation_path:
        primary: "Slack → Team"
        secondary: "Relevant owner (DX Lead / Platform Engineer)"
      notification_channels:
        - "Slack #contracts-alerts (no mention)"
      actions:
        - "Create task en backlog próximo sprint"
        - "Investigate en office hours"
    
    P3_LOW:
      examples:
        - "Docs update needed (broken link)"
        - "Example outdated (still works pero no best practice)"
        - "Minor performance improvement opportunity"
      response_time: "< 1 week"
      escalation_path:
        primary: "GitHub Issue"
      notification_channels:
        - "GitHub Issue con label low-priority"
      actions:
        - "Triage en sprint planning"
```

### E) Comando de Referencia Rápida

```bash
# Validación local completa
make validate-all          # Spectral + AJV + Buf + TSC
make check-versions        # Verifica tools/versions.json
make check-breaking        # oasdiff + buf breaking vs main

# Baseline
make baseline-generate     # Genera .baseline/*.b2
make baseline-verify       # Verifica firmas Cosign
make baseline-update       # Actualiza y re-firma (requiere aprobación)

# SDKs
make sdk-build-all         # Build Python + TypeScript + Go + Java + .NET
make sdk-test-all          # Run smoke tests
make sdk-bench             # Benchmarks de build time

# Mocks
make mocks-up              # docker compose up con healthchecks
make mocks-regen           # Regenera desde specs actuales
make mocks-verify          # Valida mock ↔ spec sync

# Compliance
make compliance-pack       # Genera compliance-pack.zip
make audit-evidence        # Consolida evidencias históricas

# CLI
enis-contracts lint        # Lint local sin CI
enis-contracts diff main   # Diff vs rama main
enis-contracts publish     # Publica a Pact Broker
enis-contracts scaffold    # Genera template nuevo contrato
```

---

**Fin del Roadmap Detallado**

**Software Propietario © 2025 ANDAON SA DE CV**  
**Versión:** 1.5.0 | **Última actualización:** 2025-10-11  
**Cambios v1.5.0 - Mejoras Arquitectónicas y Operativas:** 

**🗺️ Estructura y Navegación:**
- ✅ Tabla de mapeo completa: 97 documentos organizados por sprint (S0-S19)
- ✅ Rutas estandarizadas: `docs/01-sprint/S{número}/` con convención uniforme
- ✅ Diagrama de dependencias entre sprints con cadena crítica visual
- ✅ Mapa visual de 24 repositorios ENIS v3.0 con consumidores
- ✅ Cross-references explícitas a Master Prompt 30 y documentación arquitectónica

**🔒 Gates y Enforcement:**
- ✅ Gates bloqueantes reforzados:
  - S0: `make check-versions` + secrets checklist
  - S7: `can-i-deploy` obligatorio en PRs de consumers
  - S12: Sign-off de macro-módulos (merge falla sin actas)
  - S15: GA checklist 100+ ítems con ritual semanal
- ✅ Política única de cambios: `docs/01-sprint/S1/CHANGE-POLICY.md` (evita duplicación)
- ✅ Escalamiento de seguridad: S0-S5 informativo, S6+ bloqueante con waiver policy

**📊 Métricas y Claridad:**
- ✅ Métricas sin ambigüedades: p95 100ms (runtime/operación), 1.2s (CI pack completo)
- ✅ Dataset reproducible documentado con hardware y comandos
- ✅ KPIs consolidados: MTTR <30min, drift ≤0.5%, lint budget=0

**🛠️ Developer Experience:**
- ✅ SDKs alpha estrictamente internos con anti-leak policy (S3)
- ✅ RACI con nombres reales + CODEOWNERS reforzado (S4)
- ✅ CLI enis-contracts MVP movido a S10 (impacto DX crítico)

**📚 Documentación:**
- ✅ Glosario de términos ENIS v3.0 (80+ términos arquitectónicos, contratos, SDKs, testing, seguridad, governance)
- ✅ Timeline visual con 14 hitos arquitectónicos clave (2025-10-14 → 2026-09-30)
- ✅ Milestones de integración cross-repo (S1, S7, S12, S13, S15)
- ✅ Acrónimos técnicos y terminología estandarizada

**🔮 Extensiones Post-GA:**
- ✅ Sprints Post-GA (S17-S19): MCP Discovery, SDK Adapters, Pilot Integrations
- ✅ Buffer de fin de año: 2025-12-22 → 2026-01-05 (hotfix/soporte)
