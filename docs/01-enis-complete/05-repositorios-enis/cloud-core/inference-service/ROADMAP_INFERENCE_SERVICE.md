#  Roadmap de Sprints  inference-service (completo y actualizado)

_Roadmap Completo  Inference Service (S0S18)_

**Monorepo:** `cloud-core/inference-service`

**Estructura:**
- `src/api/v1/`
- `engine/`
- `providers/`
- `prompts/`
- `models/`
- `core/`
- `integrations/{nops,mcp}`
- `deployment/{kubernetes,helm}`
- `tests/`
- `docs/`

## S0 — Kickoff & Repo Bootstrap

### Meta
- Repo production-ready con CI/CD.

### Entregables
- Estructura estándar.
- GitHub Actions (Lint → Type → Test → Build → Push).
- Branch protection.
- pre-commit (black, ruff, mypy).
- Docker multi-stage <500MB.
- `docker-compose.dev.yml` con healthcheck.
- Docs base (README, CONTRIBUTING, Makefile).

### DoD
- Pipeline < 5m.
- `docker-compose up` < 2m.
- Cobertura > 80%.
- Imagen reproducible.
- Endpoints `/healthz` | `/readyz` | `/livez` OK.

## S1 — Contracts First (OpenAPI + Prompt Schemas + CI)

### Meta
- Contratos HTTP y streaming; manifests de prompts validados en CI.

### Entregables
- OpenAPI 3.0 con:

```text
POST /api/v1/inference           # sync
POST /api/v1/inference:stream    # SSE (text/event-stream)
# Eventos: data | resume | heartbeat | done | error
# resume_token HMAC (kid:offset, TTL 5m)
```

- Autenticación documentada: JWT en header (HTTP/SSE/WS); mTLS integrado con S8.
- Prompts en `src/prompts/manifests/*.yaml` + JSON Schema + checksum JCS+SHA256.
- CI `prompts-validate.yml`: YAML lint, schema, checksums y detección de breaking changes.

### DoD
- OpenAPI publicado.
- Validaciones de manifests en CI.
- Documentación actualizada en `/docs`.

## S2 — Engine Core (Realtime HTTP + PromptResolver)

### Meta
- Inferencia realtime con resolución de prompts y anti-injection.

### Entregables
- PromptResolver FS-only con `AsyncTTLCache` (TTL 15m), preload top-N, budget timeout  15ms, fallback embedded.
- Sanitización anti-injection (role isolation, meta-instr stripping).
- RealtimeEngine con circuit breaker, semáforo y timeouts.

### DoD
- p95 < 200ms (sin provider).
- `resolve` < 15ms (cache caliente).
-  10 tests anti-injection.
- `/readyz` reporta `prompts_loaded`.

## S3  Engine Batch & Workers

### Meta
- Batch idempotente por tenant.

### Entregables
- Celery/Redis; DLQ; idempotency por `task_id`; límites por tenant; métricas de estado.

### DoD
- Idempotencia verificada.
- DLQ tras 3 reintentos.
- 1000 jobs concurrentes.
- Métricas `queued`/`running`/`done`/`failed`.

## S4  Engine Streaming (SSE)

### Meta
- SSE estable con resume HMAC y auth para WS/SSE.

### Entregables
- Multiplexing con `asyncio.Queue`.
- Heartbeats cada 15s.
- `resume_token` HMAC (kid, TTL = 5m) + rotación de claves.
- Auth JWT en upgrade y headers (alineado con S1/S8).

### DoD
- Streams > 5m.
- Resume OK.
- Token inválido  401.
- Sin fugas.
- p95 chunk < 100ms.

## S5  Model Management (Hot-Reload)

### Meta
- Ciclo de vida con swap sin downtime.

### Entregables
- Dual-load + atomic swap; rollback; caché.
- `mem_guard` cgroup v2 (`memory.max/current`) con headroom 1.3.
- Política: < 8GB in-pod swap;  8GB blue/green.

### DoD
- 10 carga/descarga sin OOM.
- Alerta `memory_headroom_low`.
- Zero downtime.
- Rollback probado.

## S6  Providers & Integrations (Sub-sprints)

### S6a  OpenAI
- Meta: Chat/Embeddings/Vision; stream + batch.
- DoD: Contract tests; backoff y rate-limit; errores normalizados.

### S6b  Anthropic
- Meta: Messages API + tool-use; stream.
- DoD: Contract tests; fallback integrado; errores normalizados.

### S6c  Groq
- Meta: Llama-3.1-70B / Mixtral-8x7B / Gemma-7B; stream + batch.
- Entregables: IDs por ENV/Helm (no hardcoded); backoff RL agresivo.
- DoD: 3 modelos operativos; fallback chain OK; errores normalizados.

### S6d  Local Runtimes
- Meta: PyTorch + ONNX; OSS (Llama/Mistral); INT8/INT4.
- DoD: GPU/CPU detection; guía HW.

### S6e  Air-Gapped
- Meta: Zero egress validado.
- Entregables: NetworkPolicy DNS-only; CI `docker --network=none`; tests DNS: `getaddrinfo` externo falla y kube-dns permitido.
- DoD: Zero egress probado.

###  S6f  FE Readiness (Voice/XR)

#### Meta
- Quitar fricción de integración para S16/S17 sin abrir repos nuevos.

#### Protocolos y endpoints congelados

Voice (S16):
```text
WS   /api/v1/voice/ws           # uplink audio/control
POST /api/v1/voice:stream       # SSE out
POST /api/v1/voice/session
```
- TTS por defecto client-side; server-TTS detrás de flag.

XR (S17):
```text
WS   /api/v1/xr/ws              # gaze/pose/gestures/VAD
POST /api/v1/xr:stream          # SSE out
POST /api/v1/xr/session
```

#### Contratos de frames (TS d.ts)
```ts
// Voice  srv
{ type: "audio" | "control", codec: "pcm16" | "opus", seq: number, payload: any, ts: number }

// Voice  srv
{ type: "partial" | "final" | "barge_in" | "metrics" | "error" }

// XR  srv
{ type: "pose" | "gaze" | "gesture" | "voice_vad", data: { /*  */ }, ts: number }
```

#### SDK y ejemplos
- SDK Alpha `@enis/client` (TS) con reconexión + `resume_token`.
- Hooks `useVoice()` / `useXR()`.
- Ejemplos React + vanilla: Voice Console y XR Panel (mocks).
- Storybook de `<VoiceMic/>` y `<XRFeed/>`.

#### Tests y resiliencia
- Contract tests FE/BE (Playwright headless) usando mocks del Sandbox (S7).
- CORS/auth/resiliencia: allowlist por entorno; JWT refresh; WS ping 2030s; SSE heartbeats 15s; fallbacks WS  longpoll, SSE  fetch loop.
- Métricas correladas: FE propaga `X-Request-Id` (S10).

#### DoD
- SDK Alpha publicado.
- Ejemplos corriendo contra Sandbox.
- Storybook build en verde.
- Tests de contrato FE/BE en CI.
- Endpoints y tipos TS congelados para Voice (fin S4) y XR (fin S8).

## S7  Sandbox Seguro

### Meta
- PII filtering + budgets + auditoría (y base para mocks de FE).

### Entregables
- Filtros PII; enforcement de budgets por tenant; audit logs; mock providers; A/B prompts y snapshots aislados.

### DoD
- PII bloqueada; budgets aplicados; suites de testing/mocks operativas.

## S8  Seguridad s2s (mTLS + JWT + Scopes)

### Meta
- mTLS, JWT y scopes.

### Entregables
- Gestión de certs; emisión/validación JWT; scopes por ruta; handshake WS/SSE.

### DoD
- mTLS/JWT verificados; rotación sin downtime; tests WS (válido/ inválido).

## S9  Observabilidad

### Meta
- OTel + Prometheus + Grafana sin filtrar contenido.

### Entregables
- Spans con metadatos no sensibles (`prompt_id`, `content_sha`, slices, provider, `ttft_ms`).
- Scrubber OTel que elimina atributos con `content*`.
- Sampling 100% en errores.

### DoD
- TTFT por provider; intento de log de contenido  redacted.

## S10  Performance & Cost (Budget Guard)

### Meta
- Guardas atómicas + pricing.

### Entregables
- `pricing.yaml` con checksum y CI.
- Lua checkandincrement idempotente.
- `x-request-id` obligatorio propagado a adapters/traces.

### DoD
- Retries (N=3) con mismo `x-request-id` no duplican coste.
- Alertas de presupuesto.

## S11  Compliance & Audit

### Meta
- Trazabilidad inmutable.

### Entregables
- Audit receipts (hash); tamper detection; retención por tenant (30/90/180d) y export endpoint.

### DoD
- Reproducción de decisiones; políticas de retención activas; export validado.

## S12  NOPS Integration

### Meta
- E2E por tipo de agente con data minimization y egress policy.

### DoD
- Suites por tipo de agente verdes; cero drift de contrato.

## S13  SDKs & DevPortal

### Meta
- SDKs Py/TS/Go + templates + cookbook.

### DoD
- SDKs en CI; quickstarts < 5m; Postman/Insomnia listos.

> Nota: `@enis/client` Beta aquí, tras el Alpha de S6f.

## S14  DR & SRE Readiness

### Meta
- Multiregión, DR/BC y game days.

### Entregables
- Runbooks; SLOs/error budgets; key rotation E2E (HMAC/JWT/certs); blue/green.

### DoD
- Game day (outage + failover) ejecutado; RTO/RPO OK.

## S15  GA Gate & Launch

### Meta
- Gates de seguridad/coste/fiabilidad.

### Entregables
- Pentest; carga final (1k usuarios, p99 < 500ms, < 1% errores); release notes; guía de operación.

### DoD
- Todos los gates en verde; P0 = 0; tag `v1.0.0`.

## S16  Natural Interface (Voice)  ProMaster 26

### Meta
- TTFT < 300ms; bargein < 100ms.

### Entregables
- `engine/voice.py`; endpoints ya congelados en S6f.
- STT/VAD integrables (Whisper/Google STT + webrtcvad/Silero).
- `prompts/voice.yaml` (slices `voice_core`, `short_answers`, `guardrails`, `barge_in`).

### DoD
- Métricas TTFT/bargein.
- E2E voice.
- Reconexion + resume sin pérdida > 10 chunks.
- Demo Voice Console en staging.

## S17  XR Interface Engine  ProMaster 27

### Meta
- Fusión multimodal (mano + gaze + voz + espacial).

### Entregables
- `engine/xr.py`; endpoints ya congelados en S6f.
- `prompts/xr.yaml` (`xr_spatial`, `gesture_aware`, `avatar_mode`).
- Anclaje espacial; audio/haptics básicos.

### DoD
- WS estable  30Hz con jitter < 50ms.
- SSE sin cortes > 2s.
- Demo XR Panel con mocks.

## S18  MCP Gateway (postGA, flag OFF)

### Meta
- MCP bajo feature flag con fallback a providers nativos.

### Entregables
- `integrations/mcp/` + Helm `mcp.enabled=false`.
- mTLS + JWT scopes; fallback < 300ms.

### DoD
- Con flag ON: `invoke/stream/discover` OK; métricas/trazas visibles.

##  Milestones & Gates

- Foundations: S0S5 (realtime/batch/streaming, prompts, hotreload).
- Providers: S6ae + S6f FE Readiness (3+ providers, fallback, airgapped, SDK Alpha y contratos FE congelados).
- Production: S7S11 (seguridad, observabilidad, coste, compliance).
- Integración: S12S14 (NOPS, SDKs Beta, SRE/DR).
- GA: S15.
- Avanzado: S16S18 (Voice, XR, MCP).

##  Dependencias (actualizado)

- S0  S1  S2  S5  S6a/S6b/S6c  S6e  S6f  S7  S8  S12  S14  S15 (critical path)
- S16 depende de S2, S4, S6f  S17 depende de S2, S4, S6f  S18 depende de S15.

##  Checklist de las 8 mejoras (integradas)

- OpenAPI streaming + `resume_token` (S1)
- Enum de errores homogéneo (S6)
- Antiinjection + tests (S2/S7)
- `mem_guard` cgroup v2 (S5)
- Idempotencia de coste con `x-request-id` (S10)
- Tests DNS pos/neg en airgapped (S6e)
- Scrubbing OTel + 100% sampling en errores (S9)
- Auth WS/SSE documentada y testeada (S1/S4/S8)

---

## 📈 **ESTADO ACTUAL DE DESARROLLO - INFERENCE SERVICE v1.0**

### **✅ COMPLETADO (S0 a S1) - 10% del Total**

#### **🏗️ FUNDACIONES (S0-S1) - 100% COMPLETO**
- **S0** ✅ **Kickoff & Repo Bootstrap** - Estructura production-ready, CI/CD, Docker multi-stage, Health checks
- **S1** ✅ **Contracts First** - OpenAPI 3.0 con streaming, autenticación JWT/mTLS, Prompts manifests validados

### **🔄 EN PROGRESO (S2) - 0% INICIADO**

#### **⚡ ENGINE CORE (S2) - PRÓXIMO SPRINT**
- **S2** ⏳ **Engine Core (Realtime HTTP + PromptResolver)** - Inferencia realtime, resolución de prompts, anti-injection

### **📋 PENDIENTE (S3 en adelante) - 90% PENDIENTE**

#### **🔧 ENGINE AVANZADO (S3-S5) - PENDIENTE**
- **S3** ⏳ **Engine Batch & Workers** - Celery/Redis, DLQ, idempotencia por tenant
- **S4** ⏳ **Engine Streaming (SSE)** - SSE estable con resume HMAC y auth
- **S5** ⏳ **Model Management (Hot-Reload)** - Ciclo de vida con swap sin downtime

#### **🌐 PROVIDERS & INTEGRATIONS (S6) - PENDIENTE**
- **S6a-S6e** ⏳ **Providers** - OpenAI, Anthropic, Groq, Local Runtimes, Air-Gapped
- **S6f** ⏳ **FE Readiness** - Voice/XR endpoints congelados, SDK Alpha, Storybook

#### **🔒 SEGURIDAD Y OBSERVABILIDAD (S7-S11) - PENDIENTE**
- **S7** ⏳ **Sandbox Seguro** - PII filtering, budgets, auditoría
- **S8** ⏳ **Seguridad s2s** - mTLS, JWT, scopes
- **S9** ⏳ **Observabilidad** - OTel + Prometheus + Grafana
- **S10** ⏳ **Performance & Cost** - Guardas atómicas + pricing
- **S11** ⏳ **Compliance & Audit** - Trazabilidad inmutable

#### **🔗 INTEGRACIÓN Y PRODUCCIÓN (S12-S15) - PENDIENTE**
- **S12** ⏳ **NOPS Integration** - E2E por tipo de agente con data minimization
- **S13** ⏳ **SDKs & DevPortal** - SDKs Py/TS/Go + templates
- **S14** ⏳ **DR & SRE Readiness** - Multiregión, DR/BC, game days
- **S15** ⏳ **GA Gate & Launch** - Gates de seguridad/coste/fiabilidad

#### **🚀 INTERFACES AVANZADAS (S16-S18) - PENDIENTE**
- **S16** ⏳ **Natural Interface (Voice)** - TTFT <300ms, bargein <100ms
- **S17** ⏳ **XR Interface Engine** - Fusión multimodal (mano + gaze + voz + espacial)
- **S18** ⏳ **MCP Gateway** - MCP bajo feature flag con fallback

### **📊 MÉTRICAS DE PROGRESO**

| Categoría | Completado | En Progreso | Pendiente | Total |
|-----------|------------|-------------|-----------|-------|
| **Fundaciones** | 2/2 (100%) | 0/2 (0%) | 0/2 (0%) | 2 |
| **Engine Core** | 0/4 (0%) | 1/4 (25%) | 3/4 (75%) | 4 |
| **Providers** | 0/6 (0%) | 0/6 (0%) | 6/6 (100%) | 6 |
| **Seguridad & Ops** | 0/5 (0%) | 0/5 (0%) | 5/5 (100%) | 5 |
| **Integración** | 0/4 (0%) | 0/4 (0%) | 4/4 (100%) | 4 |
| **Interfaces Avanzadas** | 0/3 (0%) | 0/3 (0%) | 3/3 (100%) | 3 |
| **TOTAL** | **2/24 (8%)** | **1/24 (4%)** | **21/24 (88%)** | **24** |

### **🎯 PRÓXIMOS HITOS**

1. **Inmediato (S2)**: Implementar Engine Core con PromptResolver y anti-injection
2. **Corto plazo (S3-S5)**: Completar Batch, Streaming y Model Management
3. **Mediano plazo (S6-S11)**: Providers, Seguridad y Observabilidad
4. **Largo plazo (S12-S18)**: Integración, Producción e Interfaces Avanzadas

### **⚠️ RIESGOS Y DEPENDENCIAS**

- **Dependencia crítica**: S2 (Engine Core) es bloqueante para S3-S5
- **Dependencia de providers**: S6 debe completarse antes de S12 (NOPS Integration)
- **Dependencia de seguridad**: S7-S8 necesarios antes de S15 (GA Gate)
- **Dependencia de interfaces**: S6f (FE Readiness) necesario para S16-S17

### **🚀 LOGROS DESTACADOS**

- ✅ **Infraestructura sólida**: Repo production-ready con CI/CD completo
- ✅ **Contratos robustos**: OpenAPI 3.0 con streaming y autenticación completa
- ✅ **Validación automática**: Prompts manifests con validación en CI
- ✅ **Arquitectura escalable**: Docker multi-stage <500MB, health checks implementados

### **📈 VELOCIDAD DE DESARROLLO**

- **Sprints completados**: 2/18 (11%)
- **Tiempo estimado restante**: 16 sprints (~4 meses)
- **Critical path**: S0 → S1 → S2 → S5 → S6 → S12 → S15
- **Bottlenecks identificados**: S6 (Providers) y S12 (NOPS Integration)
