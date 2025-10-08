# 🚀 Roadmap NOPS Kernel v3.0 — **Canonical (Slim) [Integrated]**

> **Propósito:** Documento único, canónico y ejecutable por equipo. Unifica los 3 roadmaps previos y **aplica** los ISSUES aceptados (#3 ZAG, #4 Air‑Gapped, #5 E2E Testing). Mantiene **Kernel slim** (contratos + hooks + eventos + perímetro), explicita **SEC/SBOM/attestations**, **OTel** y **ZAG**.

---

## 📌 Principios (Slim)

* **NOPS Kernel** no implementa módulos pesados (Scorecard, Billing, Sandbox Runtime, Lifecycle).
* Kernel expone **OpenAPI contratos**, **adapters outbound**, **eventos versionados**; seguridad **JWT + mTLS + API‑Keys** y **HMAC (nonce+timestamp) con idempotency**.
* Observabilidad avanzada (Prom/Grafana/Jaeger/ELK/Vector) e IaC fuera del Kernel.

---

## 🧭 Mapa de Sprints (S1 → S22)

### S1 — Scaffold & Seguridad Base ✅

* **S1-P1** Health (FastAPI)
* **S1-P2** JWT Basic
* **S1-P3** Security Headers

### S2 — Agent Registry Capability ✅

* **S2-P1** Agent CRUD
* **S2-P2** Heartbeats
* **S2-P3** Capabilities Model

### S3 — Event Bus ✅

* **S3-P1** Ingestion/Consumption
* **S3-P2** DLQ Initial

### S4 — Security Policies ✅

* **S4-P1** Global Rate‑Limiting
* **S4-P2** ABAC Preliminar
* **S4-P3** Security Hardening

### S5 — Routing & Scoring ✅

* **S5-P1** Intelligent Routing
* **S5-P2** Health Scoring (base)
* **S5-P3** Telemetry Dynamic Weights

### S6 — Persistence & Idempotencia ✅

* **S6-P1** Outbox Pattern
* **S6-P2** Idempotent Store
* **S6-P3** Replay Engine

### S7 — DB + Observability Core ✅

* **S7-P1** Alembic/PG Migration
* **S7-P2** Pooling & Retries
* **S7-P3** Chaos Toggles
* **S7-P4** SLO Alerts (base)

### S8 — Observability v1 ✅

* **S8-P1** Tracing hooks
* **S8-P2** Logging Hardening
* **S8-P3** Health Extended

### S9 — Federation Bootstrap ✅

* **S9-P1** Kernel Discovery
* **S9-P2** Kernel Handshake
* **S9-P3** Trust Negotiation

### S10 — GA Fix Packs & Evolution ✅/🔄

* **S10-P1** Live Contract ✅
* **S10-P2** Security Headers Fix ✅
* **S10-P3** OpenAPI Hygiene ✅
* **S10-P4** GA Fix Pack (BLAKE2b; Rate‑Limit global) ✅
* **S10-P5.1** Feature Flags Core ✅
* **S10-P5.2a** GA Fix Pack 2 ✅
* **S10-P5.2b** GA Safe Slice ✅
* **S10-P5.3** OpenAPI Diff / Release Notes ✅
* **S10-P5.4** Evolution Framework (opt‑in) ✅
* **S10-P6** EB01 — Event Bus @Edge (ADR+Bench) 🔄
  *Bench Redis Streams vs NATS JetStream (p95/p99, 0 pérdida crash‑recovery, sharding/failover)*

## Meta

* Seleccionar y parametrizar el bus de eventos óptimo en edge con garantías de entrega y recuperación.

### Entregables

* ADR comparativo Redis Streams vs NATS JetStream (capacidad, consistencia, operabilidad, costo).
* Suite de benchmarks (k6/Locust) con escenarios: throughput, p95/p99, crash-recovery, sharding, failover.
* Productores/consumidores de referencia con backpressure (`asyncio.Queue`), idempotency keys y reintentos.
* Políticas de DLQ y reprocessing; semántica **at-least-once** con deduplicación.
* Métricas OTel: lag, consumer latency, requeues, DLQ size, drop rate.

### DoD

* p95 ≤ 25 ms / p99 ≤ 60 ms a 2k msg/s (carga sostenida) en entorno de referencia.
* Crash‑recovery con **0 pérdida** en pruebas de interrupción controlada.
* Failover < 3 s con continuidad de consumo.
* ADR aprobado por Arquitectura (trade‑offs explícitos, rollback plan).
  *Bench Redis Streams vs NATS JetStream (p95/p99, 0 pérdida crash‑recovery, sharding/failover)*
* **S10-P7** Workload Identity + s2s Scopes (SPIFFE/SPIRE PoC) 🔄

## Meta

* Establecer identidad de workloads para autenticación mTLS y autorización por scope.

### Entregables

* Autoridad SPIRE operativa; emisión de **SPIFFE IDs** para Kernel/agents.
* mTLS mutual entre servicios con verificación de identidad (workload → workload).
* Mapeo de **scopes jerárquicos** en OpenAPI routers (service, operation, tenant).
* Rotación automática de certificados (short‑lived) y política de revocación.

### DoD

* Handshake mTLS exitoso en todos los hops críticos.
* Rechazo (403) cuando el scope no coincide.
* Cert rotation validada (sin downtime) y logs de auditoría.
* **S10-P8** Threat Model v1 + Egress Taxonomy (D0..D4) + rollback 🔄

## Meta

* Modelar amenazas end‑to‑end y establecer política de egreso "deny‑by‑default" por tier.

### Entregables

* DFDs del Kernel y superficies expuestas; análisis STRIDE; matriz de riesgos.
* Taxonomía de egreso D0..D4 por servicio/tenant; allow‑lists firmadas.
* Hooks de rollback seguro ante violaciones de política.
* Pruebas automatizadas de egress (contract + runtime) en CI.

### DoD

* Riesgos críticos mitigados o aceptados formalmente.
* Egress tests integrados a CI con **gates**.
* Incidentes simulados documentados con tiempos MTTR.
* **S10-P9** Degraded Modes & Criticality Matrix 🔄
  *Billing/Compliance=Critical; Observability=Essential; runbooks 60m*

## Meta

* Operar bajo degradación controlada priorizando funciones críticas.

### Entregables

* Matriz de criticidad por feature (Critical/Essential/Best‑Effort).
* Feature flags para toggles de degradación.
* Runbooks de operación (≤ 60 min) y tableros de estado.

### DoD

* Simulaciones de degradación con continuidad de **Billing/Compliance**.
* Registro de eventos de degradación y recuperación con OTel.
  *Billing/Compliance=Critical; Observability=Essential; runbooks 60m*
* **S10-P10** SLIs/SLOs + Timeouts/CB (E2E < 500 ms p95) 🔄

## Meta

* Asegurar latencia E2E objetivo y resiliencia por servicio.

### Entregables

* Timeouts por hop, retries con **jitter exponencial**, políticas de **circuit breaker** (open/half‑open/close).
* Colección de SLIs (latencia p50/95/99, error rate, saturation) vía OTel → Prometheus.
* Dashboards y alertas (Alertmanager) por servicio y E2E.
* "Straggler test" de 10 s y perfiles de CPU/memoria para outliers.

### DoD

* p95 E2E < 500 ms en caso base y < 900 ms en pico.
* Sin **retry storms** detectados; CB actúa según umbrales.
* Alertas con baja tasa de falsos positivos (<5%).

### S11 — Agent SDK Touchpoints ⏳

* **S11-P1** API Keys Rotation + Grace
* **S11-P2** SDK Python (register/heartbeat/metrics/rotate)
* **S11-P3** TTL/Zombie Cleanup ✅
* **S11-P4** Enterprise Evolution Extensions ✅

### S11.5 — Agent SDK Completion (Subsprint) ⏳

* **S11.5-P1** Complete API Keys Rotation (pepper, grace, admin endpoints, métricas)
* **S11.5-P2** Python Client SDK (auto‑register, heartbeat, metrics, rotation, retries, docs)

### S12 — Federation Bus + E2E ⏳

* **S12-P1** Federation Bus Core
* **S12-P2** Cross‑Agent Proof Exchange
* **S12-P3** Multi‑tenant Contracts
* **S12-P4** Federation Governance
* **S12-P5** **Contract Tests + Chaos básico** (latency/partition games)

### S13 — Security Hardening ⏳

* **S13-P1** mTLS Everywhere
* **S13-P2** Secrets Rotation
* **S13-P3** Compliance Audit Trails

### **S13.5 — SEC (Signed Execution Contract) — Supply Chain Integrity** ⏳

* **P1** Binary Signing (cosign/sigstore/Notary v2; HSM/KMS)
* **P2** Runtime Verification (hash‑bundle, allowlist certs)
* **P3** SBOM & Provenance (Syft; SLSA attestations)
* **P4** SEC Audit Trail & Enforcement (políticas por tier; métricas/alertas)
* **P5** Documentación (rotación de claves; matrix de cumplimiento)

## Meta

* Garantizar integridad y procedencia de artefactos del Kernel y agentes.

### Entregables

* Pipeline de firma (cosign) con almacenamiento seguro de claves (HSM/KMS).
* Verificación en arranque (firma y hash‑bundle) con reporte a Audit Trail.
* SBOM por build y **attestations** SLSA; publicación en registry firmado.
* Políticas de ejecución por tier (deny on fail), métricas y alertas.

### DoD

* Merge **bloqueado** sin SBOM/attestation.
* Arranque falla con firma inválida o hash inconsistente (evidencia en audit).
* Auditoría reproduce cadena de evidencias para una release.

### S14 — Pre‑GA Gate ⏳

* **S14-P1** CI/CD Release Gate
* **S14-P2** DNA Compliance Validation **(requiere S13.5)**
* **S14-P3** Docs Freeze

> **Gate adicional:** `openapi-diff` + verificación de **SEC attestations** obligatoria.

### **S14.5 — E2E Integration Testing (Nuevo subsprint pre‑GA)** ⏳

* **P1 — Edge Agent Integration Matrix**

  * Matriz: agentes (🟤 Zero, 🟡 Shared, 🟢 Lite, 🔵 Enterprise, 🔴 Air‑Gapped) × módulos
  * Validación: Billing correcto, métricas OTel, audit trails
* **P2 — End‑to‑End Workflow Validation**

  * Flujo: Registration → Heartbeat → Inference → Billing → Audit
  * Validación: Zero data loss, idempotency, SLO compliance (p95/p99)
* **P3 — Disaster Recovery Scenarios**

  * Postgres failure + recovery; Redis failure + cache rebuild; partial network partition; certificate expiration handling
* **DoD**: Reporte E2E con KPIs (p95/p99, error rate), evidencias de DR (MTTR/MTBF objetivos)

## Meta

* Validar integraciones de extremo a extremo previas a GA.

### Entregables

* Test matrix automatizada (agents × módulos) con datos sintéticos y semillas reproducibles.
* Suites de resiliencia (DR) ejecutadas en CI nocturno.
* Reportes comparables por commit/release.

### DoD

* 100% de casos críticos cubiertos; sin regresiones funcionales.
* MTTR/MTBF dentro de objetivos declarados.

### S15 — Gateway & Advanced Security ⏳

* **S15-P1** API Gateway Template
* **S15-P2** WAF & DDoS Mitigation
* **S15-P3** JWT/OIDC Federation
* **S15-P0 — Zero Agent Gateway v1 (CRITICAL)**

  * **Dependencias**: S2 Agent Registry; S4‑P1 Global RL; **S10‑P10** SLOs/Timeouts/CB
  * **Estado actual** (pre‑ZAG): Zero Agents operan con Agent Registry básico; RL global; **sin** HMAC, **sin** RL por tenant
  * **Mejoras con ZAG**: HMAC signature verification (anti‑spoofing); RL por tenant (multi‑tenancy); anti‑replay (nonce+timestamp); **Billing hooks**; DoS protection específico Zero; **OTel completo** (metrics/logs/traces) en gateway
  * **Workaround hasta ZAG**: API Keys básicas (S2); RL global suficiente para MVP; validación de firma en backend (menos performante); whitelist de orígenes por tenant
  * **DoD**: p95 < 200 ms en validación; bloqueo por HMAC inválido y replay (skew ≤ 5m); rate‑limit por tenant con métricas exportadas; Chaos DoS (burst req/s) sin caída

## Meta

* Endurecer el perímetro de Zero Agents sin engordar el Kernel.

### Entregables

* Verificación HMAC (kid, nonce, timestamp) y protección anti‑replay.
* Rate‑limit por tenant y rutas con métricas exportadas (Prom/OTel).
* Hooks de billing (usage metering) y auditoría.
* Pruebas de **DoS** (burst y sostenido) + whitelists por tenant.

### DoD

* 401 para firmas inválidas o timestamp fuera de skew.

* p95 de ruta de validación < 200 ms; error rate < 0.1% en pico.

* Reportes de métricas y auditoría por tenant.

* **S15-P4** **mTLS Termination + Key Rotation** (enterprise) **mTLS Termination + Key Rotation** (enterprise)

### S16 — ZKP Engine ⏳

* **S16-P1** Proof Library
* **S16-P2** Proof Exchange
* **S16-P3** Compliance Proofs
* **S16-P4** **Audit Trail Forensics** (hash‑chain receipts, evidencias regulatorias)

### S17 — Merkle DAG Sync ⏳

* **S17-P1** State Hashing
* **S17-P2** DAG Exchange
* **S17-P3** Conflict Resolution

### S18 — Advanced Channels ⏳

* **S18-P1** Cross‑Kernel Agents
* **S18-P2** Multi‑hop Federation
* **S18-P3** Encrypted Channels

### S19 — Governance ⏳

* **S19-P1** Marketplace Policies
* **S19-P2** SLA Contracts
* **S19-P3** Tokenomics

### S20 — Blockchain Verifiability ⏳

* **S20-P1** Ledger Integration
* **S20-P2** Smart Contracts
* **S20-P3** Regulatory Reporting

### S21 — MCP Server Integration ⏳

* **S21-P1** MCP Server Foundation (JSON‑RPC, discovery)
* **S21-P2** MCP Tools Catalog (agents, inference, federation, observability)
* **S21-P3** MCP Client SDK (Edge Agents)

### S22 — **Air‑Gapped Bootstrap** ⏳

> **Dependencias explícitas**: **S13.5 → S14 → S11.5** (en ese orden)

* **S22-P1** Provisioning offline + trust bundles
* **S22-P2** Rotación offline + actualización segura
* **S22-P3** Validación **SEC** offline + auditoría (evidencias)
* **DoD**: instalación 100% sin red; verificación de firmas en arranque; procedimiento de rotación offline validado

## Meta

* Habilitar despliegues totalmente offline con cadena de confianza verificable.

### Entregables

* Playbooks de instalación offline (paquetes, repos locales, trust bundles).
* Herramientas de firma/verificación offline y procedimiento de actualización segura.
* Auditoría y export de evidencias para auditor externo.

### DoD

* Instalación reproducible sin Internet.
* Validación de firmas/attestations documentada.
* Rotación de llaves offline ejecutada y auditada con éxito.

---

# 📦 Detalles por Sprint — Meta / Entregables / DoD (complemento)

> Esta sección añade el nivel de detalle solicitado para **todos los sprints y subsprints restantes** siguiendo el patrón: **Meta → Entregables → DoD**. No modifica el alcance slim del Kernel; los módulos pesados permanecen fuera.

## S1 — Scaffold & Seguridad Base

### Meta

* Base ejecutable con FastAPI, JWT básico y headers seguros.

### Entregables

* `/health` con dependencias (DB/Redis) y `readyz`.
* Emisor/verificador JWT (HS/RS) + bcrypt para credenciales de bootstrap.
* Headers: HSTS, CSP, X-Content-Type-Options, X-Frame-Options.

### DoD

* `/health` 200 con dependencias sanas; `/readyz` fail si DB/Redis caen.
* JWT inválido → 401; expirado → 401; sin scope → 403.
* Security headers presentes en 100% de rutas.

## S2 — Agent Registry Capability

### Meta

* Registro, heartbeats y llaves para agentes.

### Entregables

* CRUD agentes (pydantic + validaciones), `heartbeat_at`, `status` derivado por TTL.
* API Keys por agente/tenant; RBAC (SUPER_ADMIN/ADMIN/OPERATOR/VIEWER).
* Webhooks de eventos: `agent.registered`, `agent.heartbeat`.

### DoD

* Alta/listado/baja de agentes con auditoría.
* Agente zombie (sin heartbeat > TTL) marcado y excluido de routing.

## S3 — Event Bus

### Meta

* Ingesta/consumo confiables con DLQ inicial.

### Entregables

* Streams/canales base, productor/consumidor de referencia.
* DLQ + consola mínima para reprocessing.
* Idempotency key en mensajes críticos.

### DoD

* Throughput mínimo 1k msg/s estable; DLQ < 0.1%.
* Reprocessing convierte DLQ=0 en escenario controlado.

## S4 — Security Policies

### Meta

* Rate limit global, ABAC preliminar y hardening.

### Entregables

* 100 req/min por IP por defecto (+ overrides por ruta).
* ABAC (atributos: role, tenant, capability).
* Hardened config: TLS min v1.2, deshabilitar ciphers inseguros.

### DoD

* 429 al exceder límites; bloqueos auditados.
* Denegaciones ABAC con rastro en audit trail.

## S5 — Routing & Scoring

### Meta

* Enrutamiento inteligente basado en salud/telemetría.

### Entregables

* Tablas de routing con pesos; fallback automático.
* Health scoring (S5-P2) y actualización de pesos por telemetría (S5-P3).

### DoD

* Failover activo < 3 s; 0 pérdida de solicitud.
* p95 mejora ≥ 10% al activar pesos dinámicos en estrés.

## S6 — Persistence & Idempotencia

### Meta

* Evitar duplicados y asegurar entrega.

### Entregables

* Outbox pattern por servicio; `idempotency_key` con TTL configurable.
* Replay engine con ventanas seguras.

### DoD

* 0 duplicados en pruebas concurrentes; idempotency 100% efectiva.

## S7 — DB + Observability Core

### Meta

* Migraciones seguras, pooling óptimo, toggles de caos y alertas base.

### Entregables

* Alembic + rollback validado; pool size/timeout; toggles de caos.
* Alertas SLO base (latencia/error-rate) en Alertmanager.

### DoD

* Rollback sin pérdida; alertas disparan con baja tasa de falsos positivos.

## S8 — Observability v1

### Meta

* Trazas, logs estructurados y health extendido (hooks OTel).

### Entregables

* OTel SDK integrado; logs JSON con correlation_id.
* `/healthz` con verificación de dependencias.

### DoD

* Traces en 100% de rutas críticas; logs sin PII.

## S9 — Federation Bootstrap

### Meta

* Descubrimiento y handshake entre kernels.

### Entregables

* `GET /federation/discover`; `POST /federation/handshake`.
* Trust anchors (certs), nonce y verificación mutua.

### DoD

* Handshake verde en ambiente de prueba con rotación de credenciales.

## S11 — Agent SDK Touchpoints

### Meta

* Capacitar a agentes oficiales con SDK y rotación segura.

### Entregables

* Rotación de API Keys con grace window; hooks de métricas.
* SDK Python: register, heartbeat, metrics, rotate.

### DoD

* Rotación sin downtime; ejemplo funcional integrado en CI.

## S11.5 — Agent SDK Completion

### Meta

* Finalizar rotación y documentación del SDK.

### Entregables

* Pepper + endpoints admin; retries con jitter; docs completas.

### DoD

* Ejemplos listos para copiar/pegar; pruebas de rotación automatizadas.

## S12 — Federation Bus + E2E

### Meta

* Bus federado multi‑tenant con gobernanza y pruebas de contrato.

### Entregables

* Esquemas versionados; ACL por tenant; auditoría de intercambio.
* **S12-P5** Contract Tests + Chaos básico (latencia/particiones).

### DoD

* Intercambio entre 2+ kernels estable bajo partición breve (< 30 s).

## S13 — Security Hardening

### Meta

* mTLS everywhere, rotación de secretos y trilas de cumplimiento.

### Entregables

* mTLS por servicio/hop; rotación con doble key y ventana segura.
* Audit trail con hash‑chain (resumen por release).

### DoD

* Conexiones sin mTLS bloqueadas; rotación validada; auditoría verificable.

## S14 — Pre‑GA Gate

### Meta

* Asegurar calidad/liberación cumpliendo DNA.

### Entregables

* CI Release Gate; `openapi-diff`; verificación **SEC attestations**.
* Docs Freeze + changelog automatizado.

### DoD

* Pipeline bloquea releases sin evidencias; etiqueta Freeze creada.

## S15-P1 — API Gateway Template

### Meta

* Plantilla de gateway (Kong/Envoy/Traefik) con autenticación y observabilidad.

### Entregables

* Autenticación JWT + API‑Key; logging/metrics; circuit‑breaking per‑route.
* Ejemplos de configuración por ambiente y por tenant.

### DoD

* p95 por ruta objetivo; error‑rate < 0.2%; dashboards operativos.

## S15-P2 — WAF & DDoS Mitigation

### Meta

* Protección perimetral contra OWASP Top‑10 y picos de tráfico.

### Entregables

* Reglas WAF (OWASP CRS); reglas de rate‑limit burst; bot‑detection.
* Runbooks de DDoS y pruebas sintéticas.

### DoD

* WAF bloquea payloads maliciosos comunes; runbook pasado sin caída.

## S15-P3 — JWT/OIDC Federation

### Meta

* Federar identidad entre kernels y servicios externos.

### Entregables

* JWKS fetch/caché; token exchange; validación `aud/scope/exp`.
* Trust con IdP (OIDC); prueba de llamada cross‑kernel.

### DoD

* Llamada federada trazada y autorizada; `aud` incorrecto → 403.

## S15-P4 — mTLS Termination + Key Rotation

### Meta

* Terminar TLS en gateway con rotación automatizada segura.

### Entregables

* Gestión de certs (ACME/step‑ca/Internal PKI); dual‑cert y SNI.
* HSTS; verificación de expiración; métricas de TLS.

### DoD

* Rotación sin downtime; cert expirado bloqueado; métricas visibles.

## S16 — ZKP Engine

### Meta

* Biblioteca de pruebas, intercambio y evidencias de cumplimiento.

### Entregables

* APIs de pruebas (prove/verify); catálogos de pruebas de compliance.
* Integración con Audit Trail para evidencias.

### DoD

* Prueba verificada E2E (< 300 ms); evidencia registrada.

## S17 — Merkle DAG Sync

### Meta

* Hashing de estado y sincronización de DAG.

### Entregables

* Cálculo de hash por snapshot; protocolo de intercambio DAG.
* Resolución de conflictos (CRDT/last‑write‑wins justificado).

### DoD

* Consistencia eventual validada; conflictos resueltos sin pérdida.

## S18 — Advanced Channels

### Meta

* Agentes cross‑kernel, multi‑hop y canales cifrados.

### Entregables

* E2E encryption; re‑keying; ruteo multi‑hop con latencia objetivo.

### DoD

* Mensajes ilegibles ante nodo comprometido; p95 dentro de objetivo.

## S19 — Governance

### Meta

* Políticas de marketplace, contratos de SLA y tokenomics base.

### Entregables

* DSL de políticas; enforcement simulable; plantillas SLA.

### DoD

* Policies evaluadas en CI (lint/sim); SLAs monitorizados.

## S20 — Blockchain Verifiability

### Meta

* Notarización en ledger y reportes regulatorios.

### Entregables

* Anclaje de hashes (releases/evidencias) en blockchain soportada.
* Export de reportes regulatorios firmados.

### DoD

* Verificación pública de hash; reporte validado por auditor.

## S21 — MCP Server Integration

### Meta

* Integración MCP (server, tools, client SDK) para agentes.

### Entregables

* Server foundation (JSON‑RPC, discovery); catálogo de tools; client SDK.

### DoD

* Invocación de tool desde un agente con autorización y trazabilidad.

---

# 🧭 Orden de ejecución recomendado (con dependencias)

1. **Cerrar S10‑P6 → P10** (core performance/resiliencia).
2. **S11‑P1/P2 y S11.5** en paralelo (rotación + SDK) — necesarios para robustecer agentes.
3. **S12‑P1..P5** (Federation Bus + contract/chaos).
4. **S13‑P1..P3** (mTLS, secretos, audit).
5. **S13.5 SEC** (firmas/SBOM/attestations & runtime verification).
6. **S14** (Release Gate + DNA Compliance) y **S14.5** (E2E Integration Testing).
7. **S15‑P0 ZAG** (perímetro Zero) **→** luego **S15‑P1/P2/P3/P4** (gateway+WAF+OIDC+mTLS).
8. **S16 → S17 → S18** (pruebas, DAG, canales).
9. **S19 → S20 → S21** (gobernanza, verificación en ledger, MCP).
10. **S22** (Air‑Gapped) **después** de **S13.5 → S14 → S11.5**.

> Notas:
> • Ítems (2) y (3) pueden solaparse parcialmente si hay equipo paralelo.
> • `S15‑P0` requiere haber estabilizado **S10‑P10**.
> • `S22` es estrictamente posterior a `SEC (S13.5)`, `Pre‑GA (S14)` y `API Keys Rotation (S11.5)`.
