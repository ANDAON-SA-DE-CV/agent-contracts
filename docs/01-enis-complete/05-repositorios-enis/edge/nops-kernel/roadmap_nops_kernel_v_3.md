# 🚀 Roadmap NOPS Kernel v3.0 — Canonical (Slim) [Integrated + S23/S24]

> Documento único y canónico. Mantiene **Kernel slim** (contratos + hooks + eventos + perímetro), integra **SEC/SBOM/attestations**, **OTel**, **ZAG**, y agrega **S23 (RGM)** y **S24 (ALM)** como servicios externos con *clients* en el Kernel.

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
- **S10-P8** Threat Model v1 + Egress Taxonomy (D0..D4) + rollback 🔄
- **S10-P9** Degraded Modes & Criticality Matrix 🔄
- **S10-P10** SLIs/SLOs + Timeouts/CB (E2E < 500 ms p95) 🔄

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

### S10-P8 — Threat Model v1 + Egress Taxonomy (D0..D4) + rollback
#### Meta
- Modelar amenazas E2E y política de egreso “deny-by-default”.
#### Entregables
- DFDs, STRIDE, matriz de riesgos.
- Taxonomía D0..D4 por servicio/tenant; allow-lists firmadas.
- Hooks de rollback ante violación de política.
- Egress tests (contract + runtime) en CI.
#### DoD
- Riesgos críticos mitigados o aceptados.
- Gates de egress en CI; incidentes simulados con MTTR.

### S10-P9 — Degraded Modes & Criticality Matrix
#### Meta
- Operar bajo degradación controlada priorizando críticos.
#### Entregables
- Matriz Critical/Essential/Best-Effort.
- Feature flags de degradación.
- Runbooks ≤ 60 min; tableros de estado.
#### DoD
- Simulaciones con continuidad de **Billing/Compliance**.
- Eventos de degradación trazados (OTel).

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
- Validar integraciones E2E pre-GA.
### Entregables
- Matriz agentes (🟤🟡🟢🔵🔴) × módulos; datos sintéticos.
- Flujo: Registration → Heartbeat → Inference → Billing → Audit.
- DR: Postgres/Redis fail+recovery; partición; expiración de cert.
### DoD
- Reporte E2E con KPIs (p95/p99, error rate); evidencias DR (MTTR/MTBF).

## S15 — Gateway & Advanced Security
### **S15-P0 — Zero Agent Gateway v1 (CRITICAL)**
- **Dependencias**: S2; S4-P1; **S10-P10** (estabilidad perímetro)
- **Estado actual** (pre-ZAG): Zero Agents operan con Agent Registry; RL global; **sin** HMAC ni RL por tenant
- **Mejoras**: HMAC (anti-spoofing); RL por tenant; anti-replay (nonce+timestamp); **Billing hooks**; DoS protection Zero; **OTel completo** en gateway
- **Workaround**: API Keys básicas; RL global MVP; validación firma en backend; whitelist orígenes por tenant
- **DoD**: p95 < 200 ms validación; bloqueos por HMAC inválido/replay (skew ≤ 5m); métricas RL por tenant; Chaos DoS superado

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
### Meta
- Biblioteca de pruebas, intercambio y evidencias.
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
1) **Cerrar S10-P6 → P10** (core performance/resiliencia).  
2) **S11-P1/P2 y S11.5** en paralelo (rotación + SDK).  
3) **S12-P1..P5** (Federation Bus + contract/chaos).  
4) **S13-P1..P3** (mTLS, secretos, audit).  
5) **S13.5 SEC** (firmas/SBOM/attestations & runtime verification).  
6) **S14** (Release Gate + DNA Compliance) y **S14.5** (E2E Integration Testing).  
7) **S15-P0 ZAG** → luego **S15-P1/P2/P3/P4** (gateway+WAF+OIDC+mTLS).  
8) **S16 → S17 → S18** (pruebas, DAG, canales).  
9) **S19 → S20 → S21** (gobernanza, verificación en ledger, MCP).  
10) **S22** (Air-Gapped) **después** de **S13.5 → S14 → S11.5**.  
11) **S23 (RGM)** y **S24 (ALM)** en **repos externos**, con **clients/contratos** ya expuestos por el Kernel.

---

## 📑 Notas de integración (módulos fuera del Kernel)
- **Scorecard / Billing / Sandbox Runtime / Lifecycle / Resource Governance** → **servicios add-on** (repos externos).  
- En Kernel: **Integration Hooks** (OpenAPI + eventos `scorecard.*`, `billing.*`, `sandbox.execute.*`, `lifecycle.*`, `governance.*`), **JWT+mTLS+API-Keys**, **HMAC** e **idempotency**.  
- Observabilidad + SIEM → `cloud-ops/cloud-infrastructure` + `shared/enis-infrastructure`. 

