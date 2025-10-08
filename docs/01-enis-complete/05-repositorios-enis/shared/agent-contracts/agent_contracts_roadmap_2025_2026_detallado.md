#  Roadmap de Sprints  agent-contracts (completo y actualizado)

_Roadmap Completo  agent-contracts (S0–S16)_

**Monorepo:** `core/agent-contracts`

**Estructura:**
- `openapi/v1/`
- `schemas/`
- `proto/`
- `sdks/{python,typescript,go,java,dotnet}/`
- `scripts/{validate,breaking,baseline,examples,bench}/`
- `tests/{contracts,examples,pact}/`
- `docs/{guides,examples,troubleshooting,benchmarks}/`

## S0 — Kickoff & Repo Bootstrap

### Meta
- Repo production-ready con CI/CD.

### Entregables
- Estructura estándar.
- GitHub Actions (Lint → Validate → Build → Sign → Publish).
- Branch protection.
- pre-commit (spectral, ajv, buf, tsc).
- Docker multi-stage < 500MB.
- `docker-compose.dev.yml` con healthcheck (validators).
- Docs base (README, CONTRIBUTING, Makefile/Taskfile).

### DoD
- Pipeline < 5m.
- `docker-compose up` < 2m.
- Validadores listos: `spectral`, `ajv`, `buf`, `tsc`.
- Artefacto `baseline.b2` generado.

## S1 — Contracts First (OpenAPI + JSON Schema + Protobuf)

### Meta
- Contratos HTTP y streaming; esquemas y protos validados en CI.

### Entregables
- OpenAPI 3.0 inicial para `inference.yaml`, `agents.yaml`, `events.yaml`, `nops.yaml` (draft caps S3/S6).
- JSON Schemas `agent-registration.json`, `inference-request.json`, `event-schema.json`, `policy-schema.json`.
- Protos `inference.proto`, `agents.proto`, `events.proto`, `federation.proto` (esqueleto).
- CI `contracts-validate` (spectral/ajv/tsc) y `contracts-breaking` (oasdiff/buf).

### DoD
- OpenAPI/Schema/Proto publicados.
- Validación en CI verde con gates.
- Documentación inicial en `/docs`.

## S2 — Validation Engine & Baseline

### Meta
- Validación determinista y baseline firmada.

### Entregables
- `scripts/validate-xrefs.py`, `scripts/breaking-changes.py`, `scripts/baseline.py` (BLAKE2b + Cosign).
- Matriz de compatibilidad inicial.

### DoD
- Gate `contracts-baseline` activo (PR falla si cambia hash sin bump).
- Reporte consolidado en PR.

## S3 — SDK Generators (Alpha Py/TS) & Examples

### Meta
- SDKs alfa y ejemplos ejecutables.

### Entregables
- Generadores para `sdks/python` y `sdks/typescript`.
- `docs/examples/{manufacturing-edge-agent-integration.md,inference-workflow-validation.md,multi-service-event-orchestration.md}`.
- Job `examples-smoke`.

### DoD
- SDKs empaquetan y se instalan local.
- `examples-smoke` ≥ 99% éxito.

## S4 — Governance & Versioning

### Meta
- Política SemVer/Deprecation y RFCs.

### Entregables
- `docs/API_GUIDELINES.md`, `docs/BREAKING_CHANGES.md`, plantilla `RFC.md`.
- Matrix de compatibilidad automatizada.

### DoD
- DoR/DoD activos; freeze `FREEZE:S3` aplicado a endpoints núcleo.

## S5 — Observabilidad de Contratos

### Meta
- Métricas, SLOs y dashboards.

### Entregables
- Exporters de validación/gates/SDK build; panel de contratos.

### DoD
- Alertas por `breaking`, `validation_fail`, `sdk_gen_fail`.

## S6 — Security & Supply Chain

### Meta
- SBOM y firma de artefactos.

### Entregables
- Syft CycloneDX por SDK; Cosign sign/verify; policy de licencias.

### DoD
- `sdks-build-sign-sbom` bloquea release si falla.
- Freeze `FREEZE:S6` (feature-freeze para GA).

## S7 — Integración con Inference Service

### Meta
- Conformance E2E con servicios/contratos.

### Entregables
- Pact (consumer-driven) `sdks/python` y `sdks/typescript`; `pact-verify`/`pact-publish`.

### DoD
- 100% verificación de providers en pipelines externos.

## S8 — Integración con NOPS Kernel

### Meta
- Alineación agents/events/state y event-bus.

### Entregables
- Ejemplos E2E y xrefs en docs; mocks estables.

### DoD
- Cero drift; contract tests en verde.

## S9 — Troubleshooting & Cookbooks

### Meta
- Reducir TTR y elevar adopción SDKs.

### Entregables
- `docs/troubleshooting/{contract-validation-errors.md,sdk-generation-issues.md,version-compatibility-guide.md}`.
- Cookbook por lenguaje.

### DoD
- TTR ↓ 30%; ≥ 80% issues con código TROU-*.

## S10 — Performance & Benchmarks

### Meta
- Anti-regresión y objetivos progresivos.

### Entregables
- `benchmarks/validation_bench.md`, `benchmarks/sdk_generation_bench.md`, scripts `scripts/bench/*`.

### DoD
- Gate de regresión (p95 > baseline*1.2 → falla CI).

## S11 — SDKs Enterprise (Go/Java/.NET Beta)

### Meta
- Cobertura multi-lenguaje.

### Entregables
- Plantillas y generación para Go/Java/.NET (beta) + SBOM/firma.

### DoD
- Builds smoke y publicación interna.

## S12 — Macro-Módulos (ASM/CGN/AWE/SHIF)

### Meta
- Contratos v1 para macro-módulos.

### Entregables
- `openapi/v1/{asm.yaml,cgn.yaml,awe.yaml,shif.yaml}` + schemas relacionados.

### DoD
- Lint/compat OK; examples actualizados.

## S13 — SDKs GA (Py/TS) + DevPortal

### Meta
- GA de clientes y portal de devs.

### Entregables
- Publicación GA Py/TS; Quickstarts; Postman/Insomnia.

### DoD
- Time-to-first-api-call ≤ objetivo baseline*0.8.

## S14 — Compliance & Audit

### Meta
- Evidencias y retención.

### Entregables
- Audit trail de contratos, firmas y releases; retención y export.

### DoD
- Auditoría reproducible E2E.

## S15 — GA Gate & Release

### Meta
- Gates en verde y notas de versión.

### Entregables
- Pentest; release notes; guía de operación.

### DoD
- `APPROVED_WITH_ADJUSTMENTS` cerrado; tag `v1.0.0`.

## S16 — Optimización & Roadmap v2

### Meta
- Escala/Performance 10x y features v2 (GraphQL/AsyncAPI/Multi-tenant) definidos.

### Entregables
- CLI `enis-contracts`; PoC GraphQL/AsyncAPI; propuesta multi-tenant; DX suite.

### DoD
- RFCs v2 aprobados; CLI publicada.

---

---
doc_type: "Roadmap"
project: "agent-contracts"
title: "Roadmap Detallado — Agent Contracts v3.0"
version: "1.0.0"
date: "2025-10-08"
owner: "@andaon"
status: "planning_approved"
timeframe: "Q4 2025 – Q3 2026"
---

# Roadmap Detallado — Agent Contracts v3.0

> **Ámbito:** Este roadmap cubre la planificación integral para evolucionar el repositorio **agent-contracts** como **Source of Truth** para contratos (OpenAPI, JSON Schema, Protobuf, Typescript) y la generación/validación de SDKs multi-lenguaje, integrándose con **NOPS Kernel**, **Inference Service**, **Macro-Módulos (ASM, CGN, AWE, SHIF)** y **Integration & APIs**.

---

## 1) Objetivos Estratégicos (12 meses)

- Consolidar **Contract Central** como única fuente de verdad con **governance** y **quality gates**.
- Garantizar **100% backward compatibility** con detección automática de breaking changes.
- Aumentar la **adopción de SDKs** a >85% en equipos internos y partners.
- Integrar **observabilidad** (métricas, dashboards, alerts) y **supply-chain security** (SBOM, firmas).
- Reducir **time-to-first-API-call** a <10 minutos y **time-to-production** a <1 día.

**KPIs Clave**  
- `contracts_validation_success_rate ≥ 99.9%`  
- `breaking_changes_in_main = 0`  
- `sdk_generation_success_rate ≥ 95%`  
- `docs_satisfaction ≥ 90%`  
- `time_to_first_api_call ≤ 10m`

---

## 2) Supuestos y Dependencias

**Supuestos**  
- DNA v3.0 y terminología de ENIS vigentes.  
- Repos **integration-apis**, **nops-kernel**, **inference-service** con owners activos.  
- Presupuesto y headcount aprobados para 12 meses.

**Dependencias Externas (Hard)**  
- _NOPS Kernel APIs_ (event bus, state, agents).  
- _Inference Service_ (predict/models/status).  
- _Integration & APIs_ (API Gateway, AuthN/Z, Rate limiting).  

**Dependencias Internas (Soft)**  
- Security & Compliance (audit trail, policy schemas).  
- Observabilidad (Prometheus/Grafana/Tempo/Loki).  
- CI/CD (GitHub Actions, runners, Cosign, Syft, Buf, oasdiff, ajv, tsc).

---

## 3) Estructura de Trabajo (Workstreams → Épicas)

| Workstream | Épicas | Resultado esperado |
|---|---|---|
| Contracts Core | Governance, Versioning & Deprecation, Compatibility Matrix, Baseline firmado | Política SemVer con **sunset**; baseline firmada; matriz de compatibilidad automatizada |
| OpenAPI / JSON Schema | Normalización OAS3.0, Librería de esquemas, Validación estricta | 15+ especificaciones y 8+ esquemas con linters y ejemplos ejecutables |
| Protobuf | Buf modules & breaking checks | 4 protos con `buf breaking` en gates |
| SDKs | Python, TS, Go, Java, .NET | SDKs generados, versionados y firmados con pipelines verdes |
| CI/CD Contracts | Validation Engine, Breaking Change Detector, Release Orchestrator | `validate-contracts`, `breaking-changes`, `compatibility-check` como jobs obligatorios |
| Security & Compliance | SBOM, Cosign, Policy Schema, Audit Trail | SBOM CycloneDX, firmas Sigstore, auditoría y retención |
| Observabilidad | Métricas, SLOs/Alertas, Dashboards | Exporters + dashboards de contratos/SDKs |
| Documentación & Ejemplos | Playbooks, Troubleshooting, Ejemplos reales | **docs/** con guías, casos y troubleshooting production-ready |

---

## 4) Cronograma por Trimestres (Q4 2025 – Q3 2026)

> Plan basado en sprints bisemanales (6 sprints por trimestre). Cada trimestre incluye **Objetivos**, **Hitos**, **Entregables** y **Criterios de Salida**.

### Q4 2025 — Fundaciones y Gates (Sprints 1–6)

**Objetivos**  
1. Establecer Governance + pipelines de validación y firmas.  
2. Publicar contratos **v1.0.0** (inference, agents, events, nops, macro-módulos).  
3. Entregar SDKs **alpha** (Py/TS/Go) y documentación base.

**Backlog Detallado**  
- **S1:** Esqueleto de repos y carpetas; reglas SemVer; templates RFC; job `validate-xrefs.py`.  
- **S2:** Jobs: `oasdiff breaking`, `ajv-diff`, `buf breaking`, `tsc --noEmit`; baseline `.b2` + firmas cosign.  
- **S3:** OAS v1 para Inference/Agents/Events/NOPS; JSON Schemas (agent-registration, inference-request, event, policy).  
- **S4:** Protos `inference.proto`, `agents.proto`, `events.proto`, `federation.proto`; generación SDK Py/TS inicial.  
- **S5:** Métricas exporters; dashboards mínimos; alertas críticas (breaking, failure rate, latency).  
- **S6:** Docs: quickstart, versioning & deprecation, validation-guide, troubleshooting v1.

**Hitos**  
- H1: Pipelines con **gates en rojo/verde**.  
- H2: **Tag v1.0.0** contratos core.  
- H3: SDKs alpha publicados en repos internos (no GA).

**Criterios de Salida**  
- 0 breaking en main; `validation_success_rate ≥ 99%`.  
- Baseline firmada y verificada en PR.  
- Docs iniciales publicadas.

---

### Q1 2026 — Ampliación & GA SDKs (Sprints 7–12)

**Objetivos**  
1. Completar contratos macro-módulos ASM/CGN/AWE/SHIF.  
2. SDKs **GA** para Python y TypeScript; **beta** Go/Java/.NET.  
3. Integración observabilidad completa + SLOs.

**Backlog Detallado**  
- **S7:** OAS/Schema de ASM/CGN; tests de compatibilidad con NOPS/Inference.  
- **S8:** AWE/SHIF OAS; examples end-to-end; linting y examples coverage `≥ 90%`.  
- **S9:** SDK Python GA (packaging, signing, docs API); ejemplos avanzados.  
- **S10:** SDK TypeScript GA (tree-shakable, typings strictos, ESM/CJS).  
- **S11:** SDKs Go/Java/.NET beta; matriz de compatibilidad automática por contrato.  
- **S12:** SLOs y alertas: `validation ≥ 99.9%`, `sdk_gen ≥ 95%`; dashboards productivos.

**Hitos**  
- H4: **GA Py/TS**.  
- H5: 15+ OpenAPI validadas; 8+ JSON Schemas validados.  
- H6: SLOs activos y alertas en Slack/Email.

**Criterios de Salida**  
- `time_to_first_api_call ≤ 10m`, `docs_satisfaction ≥ 85%`.  
- `breaking_changes_in_main = 0`.  
- Exporters + dashboards completos.

---

### Q2 2026 — Enterprise & Compliance (Sprints 13–18)

**Objetivos**  
1. **Enterprise certification** (ISO/SOC2 ready) para pipelines y artefactos.  
2. SDKs **GA** Go/Java/.NET; **webhooks & events contracts** enterprise.  
3. DR/Resilience para Contract Central; políticas de retención y auditoría.

**Backlog Detallado**  
- **S13:** Supply-chain: SBOM CycloneDX por SDK; firmas/verificación en gates.  
- **S14:** Auditoría completa (logs, trails, evidencias) + retención (90d–1y).  
- **S15:** SDK Go GA (concurrency patterns); Java GA (Spring-friendly); .NET GA (NuGet).  
- **S16:** Webhooks enterprise: retries, idempotencia, firma HMAC; contratos y ejemplos.  
- **S17:** DR: backups firmados, restauración automatizada; ejercicios **tabletop**.  
- **S18:** Compliance pack: reportes automáticos; checklist de auditoría.

**Hitos**  
- H7: SDKs **GA** en los 5 lenguajes.  
- H8: **Compliance pack** publicado (evidencias + reportes).  
- H9: DR ejecutado y aprobado (<2h RTO, <15m RPO).

**Criterios de Salida**  
- `sdk_generation_success_rate ≥ 97%`.  
- Auditoría reproducible E2E con evidencias.  
- Ejercicios DR superados.

---

### Q3 2026 — Optimización & Scale (Sprints 19–24)

**Objetivos**  
1. Performance & scale de validación y generación (10x).  
2. Roadmap v2.0 (features: GraphQL schemas, AsyncAPI, multi-tenant contracts).  
3. Developer Experience: CLI, plantillas, “one-command setup”.

**Backlog Detallado**  
- **S19:** Paralelización/Cache en validación (dag + remote cache); `latency_p95 < 100ms`.  
- **S20:** Aceleración SDK gen (targets p95: Py 30s, TS 45s, Go 25s, Java 60s, .NET 40s).  
- **S21:** CLI `enis-contracts` (scaffold, validate, diff, bump, release).  
- **S22:** Piloto GraphQL/AsyncAPI; PoC multi-tenant.  
- **S23:** DX: plantillas, examples autogenerados, “Open in StackBlitz/Colab”.  
- **S24:** Revisión roadmap v2.0 + RFCs comunitarios.

**Hitos**  
- H10: `validation_latency_p95 < 100ms`.  
- H11: CLI y DX suite publicados.  
- H12: V2 draft con RFCs aprobados.

**Criterios de Salida**  
- `docs_satisfaction ≥ 90%`.  
- `operational_efficiency ≥ 70%` (baseline Q4’25).

---

## 5) Entregables por Épica (Definition of Done)

### Épica: Governance & Versioning
- Política SemVer y **deprecation** con _notice_ (6m) y _sunset_ (12m).
- RFCs con SLA (review 72h / approval 1w).  
- **DoD:** Guía publicada + linter de versiones + hooks de PR activos.

### Épica: Validation Engine
- Jobs: `oasdiff`, `ajv-diff`, `buf breaking`, `tsc --noEmit`.  
- **DoD:** Gates obligatorios; reporte consolidado en PR y en dashboard.

### Épica: SDKs Multi-lenguaje
- Pipelines de generación, firma, publicación y ejemplos ejecutables.  
- **DoD:** Paquetes publicados, changelog, docs API, ejemplos end-to-end.

### Épica: Security & Supply Chain
- SBOM por SDK (Syft), firmas (Cosign), verificación y auditoría.  
- **DoD:** Release bloqueado si no hay SBOM/firma; evidencias guardadas.

### Épica: Observabilidad
- Exporters, SLOs, alertas; dashboards de validación, SDKs y breaking changes.  
- **DoD:** Alertas en Slack/Email; SLOs cumplidos 4 semanas continuas.

### Épica: Documentación & Ejemplos
- Guías: quickstart, versioning, validation, migration, troubleshooting.  
- **DoD:** 90%+ ejemplos ejecutables; feedback rating >4.5/5.

---

## 6) Quality Gates y Acceptance Criteria

| Gate | Criterio | Umbral |
|---|---|---|
| Security Gate | 0 vuln. High/Critical | **Obligatorio** |
| Breaking Gate | `oasdiff/buf` sin breaking | **Obligatorio** |
| Performance Gate | `latency_p95 < 100ms`, `throughput ≥ 5K req/s` | Por contrato crítico |
| Docs Gate | 0 enlaces rotos; 90% ejemplos ejecutables | **Obligatorio** |
| Compliance Gate | Evidencias completas y firmadas | **Obligatorio (Q2 2026)** |

---

## 7) Organización — RACI

| Función | Governance | Validación | SDKs | Seguridad | Observabilidad | Docs |
|---|---|---|---|---|---|---|
| Arquitecto de Contratos | A/R | C | C | C | C | C |
| Tech Leads (servicios) | C | A/R (por servicio) | C | C | C | C |
| Equipo SDKs | C | C | A/R | C | C | C |
| Sec/Compliance | C | C | C | A/R | C | C |
| DevRel/Docs | C | C | C | C | C | A/R |
| SRE/Platform | C | C | C | C | A/R | C |

_A = Accountable, R = Responsible, C = Consulted_

---

## 8) Riesgos y Mitigaciones

| Riesgo | Impacto | Prob. | Mitigación |
|---|---|---|---|
| Drift entre contratos y servicios | Alto | Medio | Gates obligatorios + baseline firmada + alertas |
| Baja adopción de SDKs | Medio | Medio | DX/CLI + ejemplos reales + workshops |
| Breaking changes urgentes | Alto | Bajo | Freeze policy + hotfix path + RFC express |
| Debt en documentación | Medio | Medio | Docs gate + owners por sección + OKRs |
| Dependencias externas retrasadas | Alto | Bajo | Mock servers + simuladores + contratos first |

---

## 9) Presupuesto y Esfuerzo (estimado)

- **Headcount**: 6–9 FTE (2 SDKs, 2 Contracts/CI, 1 Sec/Compliance, 1 SRE, 0–3 Docs/DevRel rotativos).  
- **Infra CI/CD/Observabilidad**: $3–6K/mes.  
- **Auditorías/Certificación**: $25–60K (Q2 2026).

---

## 10) Comunicación y Cadencia

- **Weekly**: status de sprints (30min).  
- **Quincenal**: demo E2E (45min).  
- **Mensual**: revisión KPIs + riesgos (60min).  
- **Trimestral**: revisión roadmap + OKRs (90min).

---

## 11) Hoja de Ruta Visual (Gantt simplificado)

```text
Q4'25: [Foundations]  |████████████████| (Gov, Gates, v1.0, SDK alpha, Obs v1)
Q1'26: [GA & Scale]   |████████████████| (SDK Py/TS GA, Go/Java/.NET beta → GA, SLOs)
Q2'26: [Enterprise]   |████████████████| (Compliance, DR, Webhooks, Auditoría)
Q3'26: [Optimize]     |████████████████| (Perf 10x, CLI/DX, v2.0 Draft)
```

---

## 12) Apéndices

### 12.1 Matriz de Contratos Objetivo (v1.x)

- **OpenAPI**: inference, agents, events, federation, nops, asm, cgn, awe, shif … (15+).  
- **JSON Schema**: agent-registration, inference-request, event, policy, federation, validation-rules, migration-guides, compatibility-matrix.  
- **Protobuf**: inference.proto, agents.proto, events.proto, federation.proto.  
- **SDKs**: Python, TypeScript, Go, Java, .NET.

### 12.2 Políticas de Deprecación
- Aviso mínimo: **6 meses**; Sunset: **12 meses**; comunicación en **issues**, **headers** y **changelog**.

### 12.3 Checklists Operativos
- Release checklist (lint, validate, sign, sbom, publish, docs, announce).  
- DR checklist (backup, restore test, integrity, signatures).

---

**Fin del documento.**



---

## Adjustments & Operating Policies (Aprobado con ajustes)

### 1) Scope Q4’25 (caps por sprint)
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
  out_of_scope_q4:
    - graphql schemas
    - asyncapi
    - multi-tenant contracts
```

### 2) Mock Strategy (S1) + Contract Testing
```yaml
dependency_management:
  mock_strategy:
    s1_setup:
      nops_kernel: { tool: "WireMock", surfaces: ["event-bus", "state", "agents"] }
      inference_service: { tool: "Prism", surfaces: ["predict", "models", "status"] }
      integration_apis: { tool: "Prism", surfaces: ["gateway", "authN", "authZ"] }
  contract_testing:
    pact:
      mode: "consumer_driven"
      consumers: ["sdks/python", "sdks/typescript"]
      providers: ["nops-kernel", "inference-service", "integration-apis"]
      ci_jobs: ["pact-verify", "pact-publish"]
      gates: ["provider-verification-required=true"]
```

### 3) KPIs → Baseline primero (S1–S2) + objetivos progresivos
```yaml
kpi_baseline_plan:
  s1_measures:
    - time_to_first_api_call
    - validation_latency_p95
    - docs_satisfaction_survey_n>=20
  s2_targets:
    time_to_first_api_call: "baseline * 0.8"
    validation_latency_p95: "baseline * 0.8"
    docs_satisfaction: "baseline + 10pp"
  quarterly_targets:
    q4_2025: "baseline +20%"
    q1_2026: "baseline +50%"
    q2_2026: "baseline +80%"
    q3_2026: "target final"
  ci_gates:
    regression_fail_if: "p95 > baseline * 1.2"
```

### 4) Plan de recursos y skills por trimestre
```yaml
resource_planning:
  q4_2025:
    roles:
      - role: Contract Architect     ; fte: 1.0 ; skills: [OpenAPI, JSON Schema, SemVer, governance]
      - role: SDK Engineer (Python)  ; fte: 1.0 ; skills: [packaging, typing, CI publish]
      - role: SDK Engineer (TS)      ; fte: 1.0 ; skills: [types, ESM/CJS, tree-shake]
      - role: Platform/CI Engineer   ; fte: 0.8 ; skills: [GH Actions, buf, oasdiff, ajv, cosign]
      - role: Security Engineer      ; fte: 0.2 ; skills: [SBOM, sigstore, license]
      - role: Tech Writer            ; fte: 0.2 ; skills: [docs IA, examples]
    total_fte: 5.0
  q1_2026:
    add:
      - role: SDK Engineer (Go/Java/.NET) ; fte: 1.0
      - role: DevRel (rotational)         ; fte: 0.5
    total_fte: 6.5
  q2_q3_2026:
    add:
      - role: Compliance Specialist ; start: Q2 ; fte: 1.0
      - role: Performance Engineer  ; start: Q3 ; fte: 1.0
    peak_fte: 8.5
```

### 5) Planning / DoR / Capacity
```yaml
planning_operating_model:
  dor:
    - "Historia con user impact + acceptance criteria"
    - "Mocks/fixtures listos si hay dependencias externas"
    - "Riesgos y owner asignado"
  dod:
    - "CI verde (lint, validate, tests)"
    - "Docs actualizadas"
    - "Ejemplos ejecutables"
  capacity:
    velocity_baseline_sp_per_sprint: 45
    policy:
      - "no más del 20% de capacidad a deuda técnica"
      - "buffers del 15% para riesgos"
```

### 6) Risk Register (owners & triggers)
```yaml
risk_register:
  - id: R-001
    title: "Servicios externos sin SLA"
    owner: "Platform Lead"
    trigger: "Timeout > p95 objetivo durante 2 sprints"
    mitigation: "Mocks obligatorios + Pact + fallback local"
    contingency: "Repriorizar endpoints y mover a S+1"
  - id: R-002
    title: "Baja adopción SDKs"
    owner: "SDKs Lead"
    trigger: "sdk_gen_success < 90% o NPS < 4.0"
    mitigation: "DX CLI + examples + workshops"
    contingency: "Dedicated DevRel sprint"
```

### 7) Comms & Templates
```yaml
communications:
  slack_channels:
    - "#agent-contracts-dev"
    - "#contracts-alerts"
  wiki:
    space: "Contracts"
    templates: ["RFC.md", "DesignDoc.md", "Runbook.md"]
  email_lists:
    - "contracts-announce@"
  status_page:
    public: true
    metrics: ["validation_success", "breaking_changes", "sdk_gen_success"]
```

### 8) Sprint 1 — Exit Criteria (medibles)
```yaml
sprint_1_exit_criteria:
  technical:
    ci_green: true
    mock_servers_healthy: ["wiremock","prism"]
    baseline_signed: true
  governance:
    semver_policy_approved: true
    rfc_001_merged: true
  contracts:
    drafts:
      inference.yaml: ">=5 endpoints"
      agents.yaml: ">=3 endpoints"
      event-schema.json: "present"
  telemetry:
    time_to_first_api_call_baseline: "medido"
    validation_latency_p95_baseline: "medido"
```

### 9) Approval como PR Template + CODEOWNERS
```yaml
approval:
  process:
    - "PR con sección 'approval_checklist' completada"
    - "Revisores obligatorios (CODEOWNERS): architect, product, security"
    - "Etiqueta 'APPROVED_WITH_ADJUSTMENTS' si hay condiciones"
  monthly_review:
    - "Revisar KPIs vs baseline"
    - "Actualizar riesgos y owners"
```



---

## Release Trains & Freezes (sin tiempos)

**Tren actual:** `R-NEXT`

**Hitos estándar:** `RC1 (S6)` → `GA (S16)`

**Jobs CI (nomenclatura estándar):**
- `contracts-validate` · `contracts-breaking` · `contracts-baseline`
- `sdks-build-sign-sbom` · `examples-smoke` · `pact-verify` · `pact-publish`

**Marcadores de congelamiento:**
- `FREEZE:S3` → cierre de alcance para endpoints núcleo.
- `FREEZE:S6` → *feature-freeze* rumbo a GA.

> Nota: sin fechas ni quarters; el tren activo cambia por etiqueta (`R-NEXT`, `R-ALPHA`, `R-GA-1`, etc.) según planning.

