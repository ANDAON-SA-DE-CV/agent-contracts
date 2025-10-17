# 🚀 Roadmap NOPS Kernel v3.0 — Canonical (Slim) [Integrated + S23/S24 + DGE]

> Documento único y canónico. Mantiene **Kernel slim** (contratos + hooks + eventos + perímetro), integra **SEC/SBOM/attestations**, **OTel**, **ZAG**, **DGE Egress Guard**, y agrega **S23 (RGM)** y **S24 (ALM)** como servicios externos con *clients* en el Kernel.
>
> **Actualizado 2025-01-09**: Agregada integración explícita con **DGE (Data Governance Engine)** vía Egress Guard client (S10-P8). Total repos ENIS v3.0: **24** (3 shared + 3 edge + 15 cloud-core + 1 cloud-ops + 2 platform).

---

## 📌 Principios (Slim)
- **NOPS Kernel** NO implementa módulos pesados (Scorecard, Billing, Sandbox Runtime, Lifecycle, Resource Governance).
- Kernel expone **OpenAPI contratos**, **adapters outbound**, **eventos versionados**; seguridad **JWT + mTLS + API-Keys** y **HMAC (nonce+timestamp) + idempotency**.
- Observabilidad avanzada (Prom/Grafana/Jaeger/ELK/Vector) e IaC viven **fuera** del Kernel.

---

## 🧭 Mapa de Sprints (S1 → S24)
**FUNCIONAL EN PRODUCCIÓN**: S1–S7, **S8**, **S9**, **S10-P1 → P5.4**  
**EN PROGRESO**: **S10-P6 → P10**  
**PENDIENTE**: **S11+**

### S1 — Scaffold & Seguridad Base ✅
### S2 — Agent Registry Capability ✅
### S3 — Event Bus ✅
### S4 — Security Policies ✅
### S5 — Routing & Scoring ✅
### S6 — Persistence & Idempotencia ✅
### S7 — DB + Observability Core ✅
### S8 — Observability v1 ✅
### S9 — Federation Bootstrap ✅

### S10 — GA Fix Packs & Evolution ✅/🔄
- **S10-P1** Live Contract ✅
- **S10-P2** Security Headers Fix ✅
- **S10-P3** OpenAPI Hygiene ✅
- **S10-P4** GA Fix Pack (BLAKE2b; Rate-Limit global) ✅
- **S10-P5.1** Feature Flags Core ✅
- **S10-P5.2a** GA Fix Pack 2 ✅
- **S10-P5.2b** GA Safe Slice ✅
- **S10-P5.3** OpenAPI Diff / Release Notes ✅
- **S10-P5.4** Evolution Framework (opt-in) ✅
- **S10-P6** EB01 — Event Bus @Edge (ADR+Bench) 🔄
- **S10-P7** Workload Identity + s2s Scopes (SPIFFE/SPIRE) 🔄
- **S10-P8** Threat Model v1 + Egress Taxonomy (D0..D4) + DGE Integration 🔄
- **S10-P9** Degraded Modes & Criticality Matrix 🔄
- **S10-P10** SLIs/SLOs + Timeouts/CB (E2E < 500 ms p95) 🔄
- **S10-P11** DGE Integration & Egress Guard 🔄
- **S10-P12** Client Boundary Cleanup (SLIM Enforcement) 🔄

### S11 — Agent SDK Touchpoints ⏳
### S11.5 — Agent SDK Completion ⏳
### S12 — Federation Bus + E2E ⏳
### S13 — Security Hardening ⏳
### **S13.5 — SEC (Signed Execution Contract)** ⏳
### S14 — Pre-GA Gate ⏳
### **S14.5 — E2E Integration Testing** ⏳
### S15 — Gateway & Advanced Security ⏳ (incluye **S15-P0 ZAG**)
### S16 — ZKP Engine ⏳
### S17 — Merkle DAG Sync ⏳
### S18 — Advanced Channels ⏳
### S19 — Governance ⏳
### S20 — Blockchain Verifiability ⏳
### S21 — MCP Server Integration ⏳
### S22 — **Air-Gapped Bootstrap** ⏳
### **S23 — Resource Governance Module (RGM)** ⏳
### **S24 — Agent Lifecycle Manager (ALM)** ⏳

---

# 📦 Detalles por Sprint — Meta / Entregables / DoD

## S1 — Scaffold & Seguridad Base
### Meta
- Base ejecutable con FastAPI, JWT básico y headers seguros.
### Entregables
- `/health` y `/_readyz` con dependencias (DB/Redis).
- Emisor/verificador JWT (HS/RS) + bcrypt de bootstrap.
- Headers: HSTS, CSP, X-Content-Type-Options, X-Frame-Options.
### DoD
- `/health` 200; `/_readyz` falla si DB/Redis caen.
- JWT inválido → 401; sin scope → 403.
- Security headers en 100% de rutas.

## S2 — Agent Registry Capability
### Meta
- Registro, heartbeats y llaves para agentes.
### Entregables
- CRUD agentes (pydantic), `heartbeat_at`, `status` por TTL.
- API Keys por agente/tenant; RBAC (SUPER_ADMIN/ADMIN/OPERATOR/VIEWER).
- Eventos: `agent.registered`, `agent.heartbeat`.
### DoD
- Alta/listado/baja con auditoría.
- Agente zombie excluido de routing.

## S3 — Event Bus
### Meta
- Ingesta/consumo confiables con DLQ.
### Entregables
- Streams/canales base; productores/consumidores referencia.
- DLQ + consola mínima de reprocessing.
- Idempotency key en mensajes críticos.
### DoD
- Throughput ≥ 1k msg/s; DLQ < 0.1%.
- Reprocessing deja DLQ=0 en escenario controlado.

## S4 — Security Policies
### Meta
- Rate limit global, ABAC y hardening.
### Entregables
- 100 req/min por IP por defecto (+ overrides).
- ABAC (atributos: role, tenant, capability).
- TLS min v1.2 y ciphers seguros.
### DoD
- 429 al exceder límites; bloqueos auditados.
- Denegaciones ABAC con rastro en audit trail.

## S5 — Routing & Scoring
### Meta
- Enrutamiento inteligente basado en salud/telemetría.
### Entregables
- Tablas de routing con pesos; fallback automático.
- Health scoring (S5-P2) y pesos dinámicos (S5-P3).
### DoD
- Failover < 3 s; 0 pérdida de solicitud.
- p95 mejora ≥ 10% con pesos dinámicos.

## S6 — Persistence & Idempotencia
### Meta
- Evitar duplicados y asegurar entrega.
### Entregables
- Outbox pattern; `idempotency_key` con TTL.
- Replay engine con ventanas seguras.
### DoD
- 0 duplicados en pruebas concurrentes.

## S7 — DB + Observability Core
### Meta
- Migraciones seguras, pooling, toggles de caos y alertas base.
### Entregables
- Alembic + rollback; pool size/timeout; toggles de caos.
- Alertas SLO base (latencia/error-rate) en Alertmanager.
### DoD
- Rollback sin pérdida; alertas con baja tasa de falsos positivos.

## S8 — Observability v1
### Meta
- Tracing, logs estructurados y health extendido (hooks OTel).
### Entregables
- OTel SDK; logs JSON con correlation_id.
- `/healthz` con verificación de dependencias.
### DoD
- Traces en 100% de rutas críticas; logs sin PII.

## S9 — Federation Bootstrap
### Meta
- Descubrimiento y handshake entre kernels.
### Entregables
- `GET /federation/discover`; `POST /federation/handshake`.
- Trust anchors (certs), nonce y verificación mutua.
### DoD
- Handshake verde con rotación de credenciales.

## S10 — GA Fix Packs & Evolution
- **S10-P1** Live Contract ✅
- **S10-P2** Security Headers Fix ✅
- **S10-P3** OpenAPI Hygiene ✅
- **S10-P4** GA Fix Pack ✅
- **S10-P5.1** Feature Flags ✅
- **S10-P5.2a/2b** Fixes & Safe Slice ✅
- **S10-P5.3** OpenAPI Diff ✅
- **S10-P5.4** Evolution Framework ✅

### S10-P6 — EB01 @Edge (ADR+Bench)
#### Meta
- Seleccionar y parametrizar bus óptimo en edge con garantías de entrega/recuperación.
#### Entregables
- ADR Redis Streams vs NATS (capacidad, consistencia, operabilidad, costo).
- Benchmarks (k6/Locust): throughput, p95/p99, crash-recovery, sharding, failover.
- Productores/consumidores con backpressure (`asyncio.Queue`), idempotency y reintentos.
- Políticas DLQ/reprocessing; **at-least-once** + deduplicación.
- Métricas OTel: lag, consumer latency, requeues, DLQ size, drop rate.
#### DoD
- p95 ≤ 25 ms / p99 ≤ 60 ms a 2k msg/s.
- Crash-recovery con **0 pérdida**; failover < 3 s.
- ADR aprobado (trade-offs + rollback plan).

### S10-P7 — Workload Identity + s2s Scopes (SPIFFE/SPIRE)
#### Meta
- Identidad de workloads para mTLS y autorización por scope.
#### Entregables
- SPIRE CA; **SPIFFE IDs** para Kernel/agents.
- mTLS mutual; verificación de identidad w→w.
- Scopes jerárquicos en routers (service/operation/tenant).
- Rotación automática de certificados; revocación.
#### DoD
- Handshake mTLS en hops críticos.
- 403 cuando scope no coincide.
- Rotación sin downtime con audit.

### S10-P8 — Threat Model v1 + Egress Taxonomy (D0..D4) + DGE Integration (Design)
> **Scope P8**: **Diseño** de amenazas, taxonomía de egress (D0..D4), y definición de hooks/contratos DGE.  
> **Scope P11**: **Implementación** en código del Egress Guard y enforcement de políticas.  
> ⚠️ **Evitar solapamiento**: P8 produce documentos de diseño (DFDs, STRIDE, allow-lists); P11 produce código ejecutable (`egress_guard.py`).

#### Meta
- Modelar amenazas E2E y política de egreso "deny-by-default" con definición de contratos DGE (**solo diseño conceptual**; implementación → S10-P11).
#### Entregables
- **Deliverables de DISEÑO** (documentos, no código):
- DFDs, STRIDE, matriz de riesgos.
- Taxonomía D0..D4 por servicio/tenant; allow-lists firmadas.
- **DGE Integration (Diseño de Contratos)**:
  - Egress Guard client (< 5MB) en `src/security/egress_guard.py`
  - Policy cache (Redis, 5 min TTL) con clasificaciones PII del DGE
  - Pre-egress validation hook: valida datos antes de salir del edge
  - Fail-closed: bloquea egress si DGE unreachable > 5s o classification = PII_SENSITIVE
  - Eventos: `egress.blocked.v1`, `egress.allowed.v1`, `dge.classification.requested.v1`
- Hooks de rollback ante violación de política.
- Egress tests (contract + runtime) en CI.
#### DoD
- **Diseño completo** (documentos, NO código):
  - Riesgos críticos mitigados o aceptados (STRIDE matrix)
  - Gates de egress en CI; incidentes simulados con MTTR
  - DFDs + allow-lists firmadas + taxonomía D0..D4 documentada
- **Contratos DGE definidos** (OpenAPI schemas de Egress Guard client)
- **Handoff a S10-P11**: Diseño aprobado por Security Lead + Architects
- **Nota**: NO incluye código ejecutable (eso es S10-P11)

### S10-P9 — Degraded Modes & Criticality Matrix
#### Meta
- Operar bajo degradación controlada priorizando críticos (revenue protection + compliance).
#### Entregables
- **Criticality Matrix** (formal):
  - **CRITICAL** (can't operate without):
    - Agent Registry (S2) → agents no pueden registrarse/heartbeat
    - Billing Module → pérdida de revenue, facturación incorrecta
    - Compliance Module → audit trail incompleto (SOC2/ISO breach)
    - **Egress Guard (DGE client)** → data protection breach (GDPR violation)
  - **ESSENTIAL** (degraded operation acceptable):
    - Routing & Scoring (S5) → fallback to round-robin (performance degraded)
    - Federation Bus (S12) → local-only operation (no cross-kernel)
    - Event Bus (S3) → local queue with sync on recovery (eventual consistency)
  - **BEST-EFFORT** (nice-to-have):
    - Scorecard metrics (analytics) → stale data acceptable
    - Advanced observability (tracing) → logs only, no traces
    - MCP Server Integration (S21) → disable feature
- Feature flags de degradación:
  - `DEGRADED_MODE_ENABLED=true` → activa fallbacks
  - `CRITICAL_SERVICES=["billing", "compliance", "egress_guard"]` → lista priorizada
  - `ESSENTIAL_FALLBACK={"routing": "round_robin", "federation": "local_only"}` → configuración
- Runbooks ≤ 60 min (docs/dr/runbooks/degraded_mode_*.md):
  - `redis_down.md` → Event Bus fallback to local queue
  - `dge_unreachable.md` → Egress Guard fail-closed (block all egress)
  - `inference_down.md` → Return 503 (no fallback, escalate immediately)
- Tableros de estado (Grafana):
  - Dashboard "Degraded Mode Status" con % services healthy
  - Alertas: critical service down → PagerDuty P0
#### DoD
- Simulaciones con continuidad de **Billing/Compliance** (revenue + audit trail sin pérdida).
- Eventos de degradación trazados (OTel): `degraded.mode.activated.v1`, `degraded.mode.recovered.v1`.
- **Egress Guard fail-closed verificado**: Si DGE down, 0 data egress (compliance protection).

### S10-P10 — SLIs/SLOs + Timeouts/CB (E2E < 500 ms p95)
#### Meta
- Asegurar latencia E2E objetivo y resiliencia.
#### Entregables
- Timeouts por hop; retries con **jitter exponencial**; **circuit breaker** (open/half-open/close).
- SLIs (p50/95/99, error rate, saturation) vía OTel→Prometheus.
- Dashboards y alertas por servicio y E2E.
- “Straggler test” 10 s; perfiles CPU/mem para outliers.
#### DoD
- p95 E2E < 500 ms (base) y < 900 ms (pico).
- Sin **retry storms**; CB actúa según umbrales.
- Alertas con baja tasa de falsos positivos (<5%).

### S10-P11 — DGE Integration & Egress Guard (Implementation)
> **Scope**: Implementación en código del Egress Guard y enforcement de políticas DGE. **Diseño conceptual** → ver **S10-P8**.

#### Meta
- Integrar DGE (cloud-core) con un guard ligero en el Kernel que valide y haga cumplir políticas de egress sin romper SLIM. **Implementación en código** del diseño establecido en S10-P8 (**P8 = diseño; P11 = código**).
#### Entregables
- **Deliverables de IMPLEMENTACIÓN** (código ejecutable, no documentos):
- **Client DGE**: 
  - `src/integrations/dge_client.py` (< 5MB)
  - Métodos: `classify(data, context)`, `get_policy(tenant_id, tier)`, `validate_egress(data, classification)`
  - Policy cache (Redis, TTL 5 min) con invalidación proactiva
  - Feature-flag: `DGE_ENABLED=true|false` (graceful degradation)
- **Egress Guard** en capa común de salidas (HTTP/gRPC):
  - Ubicación: `src/security/egress_guard.py` (middleware/interceptor)
  - Lectura de **headers DGE firmados** (HMAC con kid+nonce+timestamp)
  - Evaluación de política por tenant/tier/criticidad:
    - Tier 1/2: allow metadata operacional (non-PII)
    - Tier 3: strict validation (PII blocked, anonymized metadata only)
    - Air-Gapped: 100% egress blocked (fail-closed)
  - Bloqueo/permitir + auditoría razonada (reason code + labels)
  - Integration points:
    - HTTP egress: middleware pre-request
    - gRPC egress: interceptor pre-send
    - Event Bus: pre-publish hook (opcional, configurable)
- **Eventos**:
  - `egress.blocked.v1`: {tenant_id, tier, data_type, classification, reason, timestamp}
  - `egress.allowed.v1`: {tenant_id, tier, data_type, classification, metadata_redacted, timestamp}
  - `dge.classification.requested.v1`: {request_id, tenant_id, data_size_bytes, timestamp}
  - `dge.policy.cache_invalidated.v1`: {tenant_id, reason, timestamp}
- **Observabilidad**: Métricas OTel
  - `egress_guard_requests_total` (labels: result=blocked|allowed, tenant, tier)
  - `egress_guard_latency_ms` (p50/p95/p99)
  - `dge_cache_hit_rate` (target ≥ 80%)
  - `dge_classification_errors_total` (debe ser 0 en steady state)
#### DoD
- **Cobertura**: 100% de rutas de egress críticas pasan por el guard (HTTP/gRPC/WebSocket)
- **Performance**: p95 overhead de validación < 10 ms (con cache-hit ≥ 80%)
- **Resilience**: Fail-closed: si DGE > 5 s sin respuesta → deny + audit razonado (reason: "dge_timeout")
- **E2E Testing**: Integrado en S14.5
  - Fuga simulada de PII (email, SSN, credit card) → bloqueada y auditada
  - Metadata operacional (non-PII) → permitida correctamente
  - Tier 3 strict mode → 0% PII egress
- **Seguridad**: 
  - Verificación HMAC de headers DGE (kid+nonce+timestamp)
  - Clock-skew validation ≤ 5 min (anti-replay protection)
  - Audit trail inmutable en Compliance Module (10 años retention)
- **Graceful degradation**: Si DGE disabled via feature-flag → log warning + allow (NO fail-closed)

### S10-P12 — Client Boundary Cleanup (SLIM Enforcement)
> **Scope**: Refactoring para mantener el Kernel estrictamente SLIM. Eliminar clients a macro-módulos (ASM/CGN/AWE/SHIF) y platform (Marketplace/Portal) que rompen el principio de separación de capas.

#### Meta
- Dejar el Kernel **estrictamente SLIM**: solo clients permitidos (5 NOPS + Inference + DGE Egress Guard), sin acoplamientos a macro-módulos ni plataforma.

#### Problema Identificado
- **Archivos que rompen SLIM** (encontrados en `src/integrations/`):
  - `asm_client.py`, `cgn_client.py`, `awe_client.py`, `shif_client.py` → Macro-módulos invocados por **Inference**, NO por Kernel
  - `marketplace_client.py`, `devportal_client.py`, `private_registry_client.py` → Platform services, NO parte del Kernel
  - `inference_service.py` → Red flag: debe ser `inference_client.py` (client, no service)

#### Entregables
- **Refactor/Move (7 archivos)**:
  - `asm_client.py` → mover a `cloud-core/asm-service/sdk/` o eliminar (Inference los llama)
  - `cgn_client.py` → mover a `cloud-core/cgn-service/sdk/`
  - `awe_client.py` → mover a `cloud-core/awe-service/sdk/`
  - `shif_client.py` → mover a `cloud-core/shif-service/sdk/`
  - `marketplace_client.py` → mover a `platform/agent-marketplace/sdk/`
  - `devportal_client.py` → mover a `platform/enis-frontend/sdk/`
  - `private_registry_client.py` → mover a `platform/agent-marketplace/sdk/`

- **Rename (1 archivo)**:
  - `inference_service.py` → `inference_client.py` (naming consistency)

- **Mantener en Kernel (clients aprobados)**:
  - ✅ `observability_client.py` (NOPS Module 1/5)
  - ✅ `scorecard_client.py` (NOPS Module 2/5)
  - ✅ `billing_client.py` (NOPS Module 3/5) — 🔴 CRITICAL
  - ✅ `sandbox_client.py` (NOPS Module 4/5)
  - ✅ `compliance_client.py` (NOPS Module 5/5) — 🔴 CRITICAL
  - ✅ `inference_client.py` (Kernel enruta tráfico a Inference)
  - ✅ `dge_client.py` (Egress Guard, S10-P11) — 🔴 CRITICAL
  - ✅ `policy_engine_client.py` (si es interno ABAC/RBAC/quotas)
  - ✅ `outbox_dedupe_sync.py` (utilidad interna: idempotencia/colas)

- **Actualizar imports**:
  - Buscar/reemplazar referencias a clients eliminados
  - Update tests que usen macro-módulos clients
  - Update docs/README con clients oficiales (7 aprobados)

- **CI/CD validation**:
  - Pipeline verifica que `src/integrations/` contenga SOLO clients aprobados
  - Lint rule: fail si detecta `*_service.py` en Kernel
  - Contract tests: verificar que NOPS modules + Inference siguen funcionando

#### DoD
- **src/integrations/ limpio**: Contiene SOLO clients aprobados (6-8 archivos máx: 5 NOPS + Inference + DGE + utils)
- **Macro-módulos eliminados**: 0 referencias a ASM/CGN/AWE/SHIF clients en Kernel
- **Platform eliminado**: 0 referencias a Marketplace/DevPortal clients en Kernel
- **CI pasa**: Contratos OpenAPI y eventos versionados intactos
- **Performance sin degradación**: p95 E2E se mantiene < 500ms
- **SLIs/SLOs cumplidos**: Availability, latency, error rate sin cambios
- **Tests actualizados**: Suite completa en verde (unit + integration)
- **Docs actualizados**: README lista solo clients oficiales

#### Arquitectura Post-Cleanup

```yaml
kernel_clients_oficiales:
  nops_modules: [5 clients]
    - observability_client.py (metrics/logs/traces)
    - scorecard_client.py (agent scoring)
    - billing_client.py (metering) 🔴 CRITICAL
    - sandbox_client.py (isolated testing)
    - compliance_client.py (audit trail) 🔴 CRITICAL
  
  inference:
    - inference_client.py (LLM routing)
  
  governance:
    - dge_client.py (Egress Guard) 🔴 CRITICAL
  
  internals:
    - policy_engine_client.py (ABAC/RBAC si interno)
    - outbox_dedupe_sync.py (idempotencia utils)
  
  total_clients: 7-9 archivos (vs ~15 antes del cleanup)

clients_eliminados:
  macro_modulos: [4 eliminados]
    - asm_client.py → movido a asm-service/sdk/
    - cgn_client.py → movido a cgn-service/sdk/
    - awe_client.py → movido a awe-service/sdk/
    - shif_client.py → movido a shif-service/sdk/
    nota: "Inference Service los llama directamente, NO el Kernel"
  
  platform: [3 eliminados]
    - marketplace_client.py → movido a agent-marketplace/sdk/
    - devportal_client.py → movido a enis-frontend/sdk/
    - private_registry_client.py → movido a agent-marketplace/sdk/
    nota: "Platform services NO son responsabilidad del Kernel edge"
```

#### Beneficios del Cleanup

- ✅ **SLIM enforcement**: Kernel < 100MB RAM (sin dependencias pesadas)
- ✅ **Reduced surface**: Menos archivos = menos bugs, menos attack surface
- ✅ **Clear boundaries**: Kernel NO conoce macro-módulos ni platform
- ✅ **Maintainability**: Cada repo mantiene sus propios SDKs
- ✅ **Deployment**: Kernel puede deployarse sin esperar macro-módulos
- ✅ **Testing**: Tests más rápidos (menos mocks necesarios)

## S11 — Agent SDK Touchpoints
### Meta
- Capacitar agentes oficiales con SDK y rotación segura.
### Entregables
- Rotación de API Keys con grace; hooks de métricas.
- SDK Python: register, heartbeat, metrics, rotate.
### DoD
- Rotación sin downtime; ejemplo en CI.

## S11.5 — Agent SDK Completion
### Meta
- Finalizar rotación y documentación.
### Entregables
- Pepper + endpoints admin; retries con jitter; docs.
### DoD
- Ejemplos listos; pruebas automatizadas.

## S12 — Federation Bus + E2E
### Meta
- Bus federado multi-tenant con gobernanza y pruebas de contrato.
### Entregables
- Esquemas versionados; ACL por tenant; auditoría.
- **S12-P5** Contract Tests + Chaos básico (latencia/particiones).
### DoD
- Intercambio entre 2+ kernels estable bajo partición < 30 s.

## S13 — Security Hardening
### Meta
- mTLS everywhere, rotación de secretos y trilas de cumplimiento.
### Entregables
- mTLS por servicio/hop; rotación dual-key.
- Audit trail con hash-chain (resumen por release).
### DoD
- Conexiones sin mTLS bloqueadas; rotación validada.

## **S13.5 — SEC (Signed Execution Contract)**
### Meta
- Integridad y procedencia de artefactos del Kernel y agentes.
### Entregables
- Pipeline de firma (cosign) con HSM/KMS.
- Verificación en arranque (firma + hash-bundle) → Audit Trail.
- SBOM por build y **attestations** SLSA; registry firmado.
- Políticas de ejecución (deny on fail); métricas/alertas.
### DoD
- Merge **bloqueado** sin SBOM/attestation.
- Arranque falla si firma/hash inválidos; audit evidencia.
- Auditoría reproduce cadena de evidencias de una release.

## S14 — Pre-GA Gate
### Meta
- Asegurar calidad y cumplimiento DNA.
### Entregables
- CI Release Gate; `openapi-diff`; verificación **SEC attestations**.
- Docs Freeze + changelog auto.
### DoD
- Pipeline bloquea releases sin evidencias; Freeze marcado.

## **S14.5 — E2E Integration Testing**
### Meta
- Validar integraciones E2E pre-GA, incluyendo DGE, SEC, ZAG, y casos de break-glass.
### Entregables
- Matriz agentes (🟤🟡🟢🔵🔴) × módulos; datos sintéticos.
- Flujo: Registration → Heartbeat → Inference → Billing → Audit.
- DR: Postgres/Redis fail+recovery; partición; expiración de cert.

**Checklist E2E (visible para QA)**:
- [ ] Matriz agents × módulos (25 combinaciones mínimo)
- [ ] Flujo completo (5 pasos: reg → heartbeat → inference → billing → audit)
- [ ] DR scenarios (4: PG/Redis/network/certs)
- [ ] **DGE E2E Tests (4 casos obligatorios)** ✨
- [ ] 🚨 **Break-glass test (override auditado) — OBLIGATORIO** ✨
      - Approval C-level + CISO (dual-approval required)
      - Override < 5 min activación, auto-revoke 1h, 100% audit trail
      - Purge datos < 24h post-incident, RCA documenta justification
- [ ] Performance baseline (p95/p99 targets cumplidos)
- [ ] Audit trail completo (100% eventos trazables)

- **DGE E2E Tests** (4 casos obligatorios):
  - Caso 1: Fuga simulada de PII (email, SSN, credit card) → **bloqueada** por Egress Guard
  - Caso 2: Metadata operacional (non-PII) → **permitida** correctamente
  - Caso 3: Tier 3 strict mode → 0% PII egress verificado
  - Caso 4: DGE down > 5s → **fail-closed** (all egress blocked + audit)
- **Break-Glass Test** (Override Auditado para Soporte):
  - Escenario: Incident P0 requiere egress de logs con PII para debugging
  - Trigger: Incident Commander solicita override (approval C-level + CISO)
  - Mechanism: `X-ENIS-Override: {signature_hmac}` header con tiempo limitado (1h max)
  - Validation: HMAC firmado con clave rotativa (HSM/KMS)
  - Audit trail: `egress.override.activated.v1` con {reason, approver, duration, data_classification}
  - Post-incident: Purge de datos exportados < 24h + RCA documentado
  - DoD: Override funciona < 5 min activación, 100% auditado, auto-revoke después de 1h
### DoD
- Reporte E2E con KPIs (p95/p99, error rate); evidencias DR (MTTR/MTBF).
- **DGE validation**: 4 casos pasados (PII blocked, metadata allowed, Tier 3 strict, fail-closed).
- **Break-glass test**: Override activado y revocado correctamente, audit trail completo.

## S15 — Gateway & Advanced Security
### **S15-P0 — Zero Agent Gateway v1 (CRITICAL)**
- **Dependencias**: S2; S4-P1; **S10-P10** (estabilidad perímetro)
- **Estado actual** (pre-ZAG): Zero Agents operan con Agent Registry; RL global; **sin** HMAC ni RL por tenant
- **Mejoras**: HMAC (anti-spoofing); RL por tenant; anti-replay (nonce+timestamp); **Billing hooks**; DoS protection Zero; **OTel completo** en gateway
- **Rate-cards Integration**:
  - ZAG expone **headers HTTP** alineados al rate-card vigente del tenant:
    - `X-RateLimit-Limit: {tier_rps_max}` (ej: Tier 1 = 100, Tier 2 = 500, Tier 3 = 5000)
    - `X-RateLimit-Remaining: {remaining_in_window}`
    - `X-RateLimit-Reset: {epoch_timestamp}` (window reset time)
    - `Retry-After: {seconds}` (si 429 Too Many Requests)
    - `X-RateLimit-Tier: {1|2|3}` (tier del tenant)
  - Configuración: `zag-gateway/config/rate_limits_by_tier.yaml` (source of truth)
  - Billing integration: eventos `billing.rate_limit_exceeded.v1` si tenant > 95% quota
- **Workaround**: API Keys básicas; RL global MVP; validación firma en backend; whitelist orígenes por tenant
- **DoD**: 
  - p95 < 200 ms validación
  - Bloqueos por HMAC inválido/replay (skew ≤ 5m)
  - Métricas RL por tenant (OTel dashboard)
  - Chaos DoS superado (10k req/s sin caída)
  - **Headers rate-limit en 100% responses**: Incluye `X-RateLimit-*` en 200 OK y `Retry-After` en 429
  - **Billing hook**: Evento `billing.rate_limit_exceeded.v1` si tenant > 95% quota

### S15-P1 — API Gateway Template
### Meta
- Plantilla de gateway (Kong/Envoy/Traefik) con auth y observabilidad.
### Entregables
- Auth JWT + API-Key; logging/metrics; circuit-breaking per-route.
- Configs por ambiente/tenant.
### DoD
- p95 por ruta objetivo; error-rate < 0.2%.

### S15-P2 — WAF & DDoS Mitigation
### Meta
- Protección perimetral contra OWASP Top-10 y picos.
### Entregables
- OWASP CRS; rate-limit burst; bot-detection.
- Runbooks DDoS + pruebas sintéticas.
### DoD
- WAF bloquea payloads comunes; runbook pasado sin caída.

### S15-P3 — JWT/OIDC Federation
### Meta
- Federar identidad entre kernels y externos.
### Entregables
- JWKS fetch/caché; token exchange; validación `aud/scope/exp`.
- Trust con IdP (OIDC); llamada cross-kernel.
### DoD
- Llamada federada trazada/autorizada; `aud` incorrecto → 403.

### S15-P4 — mTLS Termination + Key Rotation
### Meta
- Terminar TLS en gateway con rotación segura.
### Entregables
- Gestión de certs (ACME/step-ca/Internal PKI); dual-cert; SNI.
- HSTS; verificación expiración; métricas TLS.
### DoD
- Rotación sin downtime; expirado bloqueado; métricas visibles.

## S16 — ZKP Engine
> **Nota aclaratoria**: S16 (ZKP Engine) y S17 (Merkle DAG Sync) NO son Voice/XR Interfaces. Las interfaces de **Voice (MP 26)** y **XR (MP 27)** viven en `cloud-core/` como servicios independientes (`voice-interface-service` y `xr-interface-service`), NO son parte del NOPS Kernel.

### Meta
- Biblioteca de pruebas, intercambio y evidencias criptográficas.
### Entregables
- APIs (prove/verify); catálogo de compliance proofs.
- Integración con Audit Trail.
### DoD
- Verificación < 300 ms; evidencia registrada.

## S17 — Merkle DAG Sync
### Meta
- Hashing de estado y sincronización de DAG.
### Entregables
- Hash por snapshot; protocolo intercambio DAG.
- Resolución de conflictos (CRDT/LWW justificado).
### DoD
- Consistencia eventual validada; sin pérdida.

## S18 — Advanced Channels
### Meta
- Agentes cross-kernel, multi-hop y canales cifrados.
### Entregables
- E2E encryption; re-keying; ruteo multi-hop.
### DoD
- Mensajes ilegibles ante nodo comprometido; p95 objetivo.

## S19 — Governance
### Meta
- Políticas de marketplace, contratos SLA y tokenomics base.
### Entregables
- DSL políticas; enforcement simulable; plantillas SLA.
### DoD
- Policies evaluadas en CI; SLAs monitorizados.

## S20 — Blockchain Verifiability
### Meta
- Notarización en ledger y reportes regulatorios.
### Entregables
- Anclaje de hashes (releases/evidencias) en blockchain.
- Export de reportes firmados.
### DoD
- Verificación pública de hash; reporte validado.

## S21 — MCP Server Integration
### Meta
- Integración MCP (server, tools, client SDK) para agentes.
### Entregables
- Server foundation (JSON-RPC, discovery); catálogo de tools; client SDK.
### DoD
- Invocación de tool desde un agente con auth y trazabilidad.

## S22 — **Air-Gapped Bootstrap**
> **Dependencias explícitas**: **S13.5 → S14 → S11.5**
### Meta
- Despliegues totalmente offline con cadena de confianza verificable.
### Entregables
- Playbooks de instalación offline (paquetes, repos locales, trust bundles).
- Firma/verificación offline; actualización segura.
- Auditoría y export de evidencias.
### DoD
- Instalación sin Internet; verificación de firmas en arranque; rotación offline validada.

## **S23 — Resource Governance Module (RGM)**
**Tipo**: Servicio externo (add-on). **Integración Kernel**: `src/integrations/governance_client.py` (HTTP + eventos).  
**Dependencias**: S10-P9 (criticidad), S10-P10 (SLOs), S13.5 (SEC), S15-P0 (si gobierna recursos Zero).
### Meta
- Asignar recursos de forma **justa (multi-tenant)** y **SLA-aware**, con control de costos.
### Entregables
- **S23-P1: Resource Pool Management** — pools CPU/RAM/GPU/I/O; allocations por tenant/agent; métricas OTel.
- **S23-P2: Multi-tenant Fairness Algorithms** — weighted fair-share; prioridad por criticidad; simulador offline.
- **S23-P3: Dynamic Quotas & SLA-aware Scheduling** — cuotas hard/soft, burst, preemption; intents API; auditoría.
- **S23-P4: Cost Optimization Strategies** — idle reclamation, off-peak, límites de costo por tenant; export a Billing.
### DoD
- Integración Kernel con **JWT+mTLS+API-Key + HMAC + idempotency**.
- Fair-share verificado (KPIs: p95 wait-time, utilización, SLA hit-rate).
- Quotas dinámicas sin downtime; auditoría completa (intents/decisions).
- Eventos `governance.allocation.granted/denied/updated` trazables.
### Timeline
- **Q2 2025** (no bloquea GA del Kernel si el client queda listo).

## **S24 — Agent Lifecycle Manager (ALM)**
**Tipo**: Servicio externo (add-on). **Integración Kernel**: `src/integrations/lifecycle_client.py`.  
**Dependencias**: S11/S11.5 (SDK/rotación), S13.5 (SEC), S14 (Pre-GA), S14.5 (E2E).
### Meta
- Orquestar **deploy/upgrade/rollback** de agentes (canary/blue-green) con **auto-recovery** y CI/CD.
### Entregables
- **S24-P1: Deployment Engine** — Rolling/Blue-Green/Canary; gates (health/scorecard).
- **S24-P2: Version Controller & Rollback** — semver; rollback auto en SLO breach.
- **S24-P3: Health Monitoring & Auto-recovery** — checks; thresholds por criticidad; restart/backoff.
- **S24-P4: CI/CD Integration** — webhooks pipelines; firmas (SEC) y **attestations** como gates.
### DoD
- Integración Kernel con **JWT+mTLS+API-Key + HMAC + idempotency**.
- Canary con **abort auto** en brecha p95/error-rate; rollback ≤ 2 min.
- Auditoría completa (quién/qué versión/evidencias SEC).
- Eventos `lifecycle.deploy.requested/succeeded/failed/rolled_back`.
### Timeline
- **Q3 2025** (post-GA del Kernel; no bloquea si client queda listo).

---

# 🧭 Orden de ejecución recomendado (con dependencias)
1) **Cerrar S10-P6 → P12** (core performance/resiliencia/seguridad/cleanup).  
   - **S10-P6**: Event Bus (ADR + benchmarks)
   - **S10-P7**: Workload Identity (SPIFFE/SPIRE)
   - **S10-P8**: Threat Model + Egress Taxonomy (bases conceptuales DGE)
   - **S10-P9**: Degraded Modes + Criticality Matrix
   - **S10-P10**: SLIs/SLOs + Timeouts/CB
   - **S10-P11**: **DGE Integration & Egress Guard** (compliance crítico)
   - **S10-P12**: **Client Boundary Cleanup** (SLIM enforcement) 🆕
2) **S11-P1/P2 y S11.5** en paralelo (rotación + SDK).  
3) **S12-P1..P5** (Federation Bus + contract/chaos).  
4) **S13-P1..P3** (mTLS, secretos, audit).  
5) **S13.5 SEC** (firmas/SBOM/attestations & runtime verification).  
6) **S14** (Release Gate + DNA Compliance) y **S14.5** (E2E Integration Testing — **incluye validación DGE**).  
7) **S15-P0 ZAG** → luego **S15-P1/P2/P3/P4** (gateway+WAF+OIDC+mTLS).  
8) **S16 → S17 → S18** (ZKP Engine, Merkle DAG Sync, Advanced Channels).  
9) **S19 → S20 → S21** (gobernanza, verificación en ledger, MCP).  
10) **S22** (Air-Gapped) **después** de **S13.5 → S14 → S11.5** (requiere **Egress Guard** para zero-egress enforcement).  
11) **S23 (RGM)** y **S24 (ALM)** en **repos externos**, con **clients/contratos** ya expuestos por el Kernel.

**Notas críticas**:
- **S10-P11 (DGE Egress Guard)** es **blocker para Tier 3 Enterprise** (compliance GDPR/CCPA). Debe completarse antes de S14 (Pre-GA Gate).
- **S10-P12 (Client Boundary Cleanup)** es **refactoring de arquitectura** para enforcement SLIM. Recomendado antes de S13.5 SEC para reducir attack surface y simplificar auditorías.

---

## 📑 Notas de integración (módulos fuera del Kernel)
- **Scorecard / Billing / Sandbox Runtime / Lifecycle / Resource Governance** → **servicios add-on** (repos externos).  
- En Kernel: **Integration Hooks** (OpenAPI + eventos `scorecard.*`, `billing.*`, `sandbox.execute.*`, `lifecycle.*`, `governance.*`), **JWT+mTLS+API-Keys**, **HMAC** e **idempotency**.  
- Observabilidad + SIEM → `cloud-ops/cloud-infrastructure` + `shared/enis-infrastructure`.

## 📑 Notas de integración adicionales (2025-01-09)

### **DGE (Data Governance Engine)** 🔐
- **Tipo**: Servicio externo `cloud-core/data-governance-service` (MP 25)
- **Propósito**: Clasificación PII, redacción, egress control (GDPR/CCPA/PDPA/LGPD compliance)
- **Integración Kernel**: **Egress Guard client** (ligero < 5MB, cache de policies) — **Ver S10-P11**
  - Ubicación: `src/integrations/dge_client.py` + `src/security/egress_guard.py`
  - Cache: Policies de clasificación (Redis, 5 min TTL)
  - Validation: Pre-egress hook valida todos los datos salientes
  - Fail-mode: **Fail-closed** (bloquea egress si DGE unreachable > 5s)
- **Eventos**: `egress.blocked.v1`, `egress.allowed.v1`, `dge.classification.requested.v1`, `dge.policy.cache_invalidated.v1`
- **SLOs objetivo**:
  - Classification latency: p95 < 50ms (DGE service cloud-core)
  - Egress validation overhead: p95 < 10ms (Kernel Egress Guard)
  - Cache hit rate: ≥ 80% (Redis policy cache)
  - Accuracy: > 95% (PII detection)
  - False positive rate: < 5%
- **Sprint relacionado**: **S10-P11** (DGE Integration & Egress Guard) — Implementación completa
- **Dependencies**: S10-P8 (Egress Taxonomy D0..D4 bases conceptuales) → S10-P11 (implementación)
- **Timeline**: Post-S13.5 SEC (requiere audit trail + compliance module)
- **Priority**: **P0 - CRÍTICO** para Enterprise Tier 3 (compliance blocker para GDPR/CCPA)

### **Voice/XR Interfaces** 🎤🥽
- **Tipo**: Servicios independientes `cloud-core/voice-interface-service` (MP 26) y `cloud-core/xr-interface-service` (MP 27)
- **NO son parte del NOPS Kernel**: Operan como microservicios autónomos
- **Conexión**: Se comunican directamente con `inference-service` y `enis-frontend`
- **Kernel NO tiene clients** para Voice/XR (son servicios horizontales)
- **Nota**: S16/S17 en este roadmap refieren a **ZKP Engine** y **Merkle DAG Sync**, NO a Voice/XR

### **24 Repositorios Totales** 📦
- **Kernel awareness**: El NOPS Kernel interactúa con:
  - 5 NOPS Modules (Obs, Scorecard, Billing, Sandbox, Compliance) → clients en `src/clients/`
  - 2 External Services (RGM, ALM) → clients opcionales en `src/integrations/`
  - 1 Governance Service (DGE) → Egress Guard client en `src/security/`
  - Inference Service → HTTP/mTLS para routing
  - ZAG Gateway → HMAC validation (S15-P0)
- **Total repos en ENIS v3.0**: 24 (3 shared + 3 edge + 15 cloud-core + 1 cloud-ops + 2 platform)

