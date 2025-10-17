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

---

## 🏗️ CONTEXTO ARQUITECTÓNICO Y ALCANCE

### **Ubicación de Inference Service en ENIS v3.0**

Inference Service es uno de **24 repositorios** que conforman ENIS v3.0 (DNA Compliant). Su rol es actuar como **orchestrator central** para routing de LLMs y composición de macro-módulos.

### **Responsabilidades CORE**

**SÍ hace (este repo)**:
1. ✅ **Routing de LLMs**: Decidir qué proveedor (OpenAI/Anthropic/Groq/Local) usar según tenant tier, availability, cost
2. ✅ **Composición de Macro-Módulos**: Orquestar llamadas a ASM/CGN/AWE/SHIF vía mTLS+JWT para respuestas complejas
3. ✅ **Prompt Management**: Resolver, cachear y versionar prompts desde `src/prompts/manifests/*.yaml`
4. ✅ **Backend APIs para Voice/XR**: Exponer endpoints HTTP/SSE/WS que las interfaces Voice/XR consumen (S6f, S16, S17)
5. ✅ **Cost Tracking & Budgets**: Guardar atómicas de coste por tenant, integración con Billing Module
6. ✅ **Observability & Audit**: Spans OTel (scrubbed), audit receipts inmutables, métricas de latencia/coste

**NO hace (delegado a otros repos)**:
1. ❌ **Agent Registry/State**: Delegado a NOPS Kernel (edge) y ASM Service (cloud)
2. ❌ **Policy Enforcement**: Delegado a NOPS Kernel (ABAC/RBAC/quotas en edge)
3. ❌ **Data Governance (PII/PHI/PCI)**: Delegado a DGE Service (cloud-core/data-governance-service)
4. ❌ **Voice Processing (STT/VAD/TTS/WebRTC)**: Delegado a Voice Interface Service (repo 15)
5. ❌ **XR Processing (OpenXR/Spatial/Gesture/Render)**: Delegado a XR Interface Service (repo 16)
6. ❌ **Lifecycle Management (Deploy/Rollback)**: Delegado a ALM Service (NOPS Module)
7. ❌ **Compliance Storage (10+ años)**: Delegado a Compliance Service (NOPS Module)

### **Conexiones Críticas (mTLS+JWT s2s)**

```yaml
inference_service_connections:
  inbound:
    - source: "NOPS Kernel (edge)"
      protocol: "mTLS+JWT (scoped)"
      path: "POST /api/v1/inference, POST /api/v1/inference:stream"
      uso: "Kernel enruta agent requests a inference para LLM routing"
      necesario_en: "S12 (NOPS Integration)"
      criticality: "🔴 CRITICAL (hub central edge)"
    
    - source: "Voice Interface Service (cloud-core)"
      protocol: "mTLS+JWT (scoped)"
      path: "POST /api/v1/inference/voice:query"
      uso: "Voice service consume inference backend para routing LLMs"
      necesario_en: "S16 (Voice Backend Integration)"
      criticality: "🟡 MEDIUM (post-GA)"
    
    - source: "XR Interface Service (cloud-core)"
      protocol: "mTLS+JWT (scoped)"
      path: "POST /api/v1/inference/xr:query"
      uso: "XR service consume inference backend para routing LLMs + vision models"
      necesario_en: "S17 (XR Backend Integration)"
      criticality: "🟡 MEDIUM (post-GA)"
  
  outbound:
    - target: "ASM Service (Adaptive State Manager)"
      protocol: "mTLS+JWT"
      path: "GET /api/v1/state/get, PUT /api/v1/state/update"
      uso: "Obtener/actualizar contexto y memoria del agent para enriched prompts"
      necesario_en: "S2 (Macro-Módulos Composition)"
      criticality: "🔴 CRITICAL (composición core)"
    
    - target: "CGN Service (Causal Graph Navigator)"
      protocol: "mTLS+JWT"
      path: "POST /api/v1/graph/reason"
      uso: "Razonamiento causal y decisiones complejas (causal chains)"
      necesario_en: "S2 (Macro-Módulos Composition)"
      criticality: "🟡 MEDIUM (value-add feature)"
    
    - target: "AWE Service (Autonomous Workflow Evolution)"
      protocol: "mTLS+JWT"
      path: "POST /api/v1/workflow/evolve"
      uso: "Generar workflows evolutivos basados en ML"
      necesario_en: "S2 (Macro-Módulos Composition)"
      criticality: "🟡 MEDIUM (value-add feature)"
    
    - target: "SHIF Service (System-Human Integration Fabric)"
      protocol: "mTLS+JWT"
      path: "POST /api/v1/integrations/execute"
      uso: "Integraciones con sistemas externos (ERP/CRM/APIs)"
      necesario_en: "S2 (Macro-Módulos Composition)"
      criticality: "🟡 MEDIUM (value-add feature)"
    
    - target: "DGE Service (Data Governance Engine)"
      protocol: "mTLS+JWT"
      path: "POST /api/v1/dge/classify, POST /api/v1/dge/redact"
      uso: "Clasificación PII/PHI/PCI y redacción antes de egress"
      necesario_en: "S7 (Sandbox Seguro)"
      criticality: "🔴 CRITICAL (Tier 3 compliance)"
    
    - target: "OpenAI/Anthropic/Groq APIs (external)"
      protocol: "HTTPS (API-Key)"
      uso: "Llamadas a LLM providers externos"
      necesario_en: "S6a-c (Providers)"
      criticality: "🔴 CRITICAL (core functionality)"
    
    - target: "NOPS Modules (Observability/Billing/Compliance)"
      protocol: "mTLS+JWT + Event Bus (Redis Streams / NATS)"
      uso: "Métricas/trazas, cost attribution, audit events"
      necesario_en: "S9-S12 (Observability, NOPS Integration)"
      criticality: "🔴 CRITICAL (production ops)"
```

### **Arquitectura de 24 Repos (resumen)**

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
      - inference-service (👈 ESTE REPO - orchestrator LLMs + composición)
    
    interfaces: 2
      - voice-interface-service (STT/VAD/TTS/WebRTC - repo 15)
      - xr-interface-service (OpenXR/Spatial/Gesture/Render - repo 16)
    
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
    - agent-contracts (schemas OpenAPI/Protobuf/JSON Schema, SDKs Py/TS/Go/Java)
```

---

## S0 — Kickoff & Repo Bootstrap ✅ **COMPLETADO** (2025-10-05)

> **Estado**: ✅ **IMPLEMENTADO**  
> **Branch**: `feature/s0-kickoff-bootstrap`  
> **Informe**: Disponible en docs/sprints/S0_INFORME_IMPLEMENTACION.md

### Meta
- Repo production-ready con CI/CD. ✅

### Entregables Implementados
- ✅ Estructura estándar (31 archivos creados/modificados)
- ✅ GitHub Actions (Lint → Type → Test → Helm → Build)
- ✅ Branch protection (configurado)
- ✅ Pre-commit (ruff 0.6.9, mypy 1.11.2)
- ✅ Docker multi-stage <500MB (python:3.11-slim)
- ✅ `docker-compose.dev.yml` con healthcheck CMD-SHELL (Python stdlib, sin curl)
- ✅ Docs base (README actualizado, CONTRIBUTING, Makefile, CODEOWNERS)
- ✅ **App mínima FastAPI**: `/healthz`, `/livez`, `/readyz` funcionales
- ✅ **Settings con timeouts**: `INFER_HTTP_TIMEOUT`, `INFER_INFERENCE_TIMEOUT`, `INFER_SHUTDOWN_TIMEOUT`
- ✅ **Helm chart K8s**: deployment.yaml, service.yaml, hpa.yaml validados
- ✅ **Tooling completo**: ruff.toml, mypy.ini, pytest.ini, .editorconfig, .gitattributes

### DoD (100% Cumplido)
- ✅ Pipeline < 10m (timeout configurado)
- ✅ `docker-compose up` < 2m
- ✅ Cobertura > 90% (health endpoints + settings)
- ✅ Imagen reproducible (versiones pinneadas: FastAPI 0.115.2, Uvicorn 0.30.6, Pydantic 2.9.2)
- ✅ Endpoints `/healthz` | `/readyz` | `/livez` OK
- ✅ **Helm lint + template**: Sin errores
- ✅ **Healthcheck healthy**: Docker Compose marca contenedor como `(healthy)`
- ✅ **Timeouts configurables**: Presentes en `core/settings.py`
- ✅ **`/readyz` estructurado**: Placeholders para providers/cache (S2+)
- ✅ **EOLs normalizados**: `.gitattributes` con LF

### Resultados Clave
- **31 archivos** creados/modificados
- **~150 líneas** de código productivo (src/)
- **~300 líneas** de configuración (CI/CD/Helm/Docker)
- **100%** de objetivos del sprint cumplidos
- **0 deuda técnica** en scope S0

### Smoke Tests Ejecutados
```bash
✅ pre-commit run --all-files          # Passed: ruff, mypy
✅ ruff check . && mypy src && pytest  # 0 errors, 0 warnings
✅ helm lint deploy/helm               # 1 chart(s) linted, 0 failed
✅ docker build -t enis/inference-service:dev .  # Successfully built
✅ docker compose up -d --build        # Status: Up (healthy)
✅ curl http://localhost:8080/readyz   # {"status":"ready","checks":{...},"version":"0.0.1"}
```

### Versiones Tecnológicas Implementadas
| Componente | Versión | Justificación |
|------------|---------|---------------|
| Python | 3.11 | LTS, performance improvements |
| FastAPI | 0.115.2 | Latest stable |
| Uvicorn | 0.30.6 | Latest stable with [standard] |
| Pydantic | 2.9.2 | V2 con mejor performance |
| Pydantic-settings | 2.6.0 | Settings management |
| Ruff | 0.6.9 | Fastest Python linter |
| Mypy | 1.11.2 | Latest stable (strict mode) |
| Pytest | 8.3.3 | Latest stable |
| Pre-commit | 3.8.0 | Git hooks automation |
| Helm | 3.15.4 | Latest stable K8s package manager |

### Preparado para S1 (Contracts First)
- ✅ Base FastAPI lista para agregar endpoints OpenAPI
- ✅ Settings modulares para configuración de contratos
- ✅ Tests structure preparada para contract testing
- ✅ CI/CD pipeline listo para validación de schemas
- ✅ Helm chart ready para deployments

## S1 — Contracts First (OpenAPI + Prompt Schemas + CI) ✅ **COMPLETADO** (2025-10-07)

> **Estado**: ✅ **IMPLEMENTADO**  
> **Branch**: `feat/s1-contracts`  
> **Commits**: `20ca3c8`, `08b66c6`  
> **PR**: [#8](https://github.com/ANDAON-SA-DE-CV/inference-service/pull/8)  
> **Informe**: Disponible en docs/02-sprint/S1/S1-IMPLEMENTATION-REPORT.md

### Meta
- Contratos HTTP y streaming; manifests de prompts validados en CI. ✅

### Entregables Implementados
- ✅ **OpenAPI 3.0** con especificación completa:

```text
POST /api/v1/inference           # sync (completions estándar)
POST /api/v1/inference:stream    # SSE (text/event-stream)
# Eventos SSE: data | resume | heartbeat | done | error (5 tipos)
# resume_token HMAC format: v<kid>:<offset>:<mac_b64url> (TTL 5m)
```

- ✅ **Autenticación documentada**: 
  - JWT bearerAuth en ambos endpoints
  - mTLS documentado en securitySchemes (implementación en S8)
  - Security tests validando presencia de bearerAuth
  
- ✅ **Sistema de Prompts**:
  - 3 manifiestos: `default.yaml`, `voice.yaml`, `xr.yaml`
  - JSON Schema estricto: `src/prompts/schemas/manifest.json`
  - Checksums SHA256 automáticos (JCS canonical JSON)
  - Loader con validación: `src/prompts/loader.py`
  - Semantic versioning (X.Y.Z)

- ✅ **CI/CD Pipeline** (`prompts-validate.yml`):
  - ✅ YAML syntax validation
  - ✅ JSON Schema validation
  - ✅ Checksums verification (strict mode)
  - ✅ Breaking changes detection (baseline comparison)
  - ✅ Full test suite (56 tests)

- ✅ **Scripts de Validación** (5 scripts):
  - `validate_yaml_syntax.py`
  - `validate_schema.py`
  - `check_checksums.py`
  - `compute_checksums.py` (con --write flag)
  - `detect_openapi_breaking_changes.py`

- ✅ **Suite de Tests** (6 nuevos tests):
  - Contract tests: `test_openapi_contract.py`, `test_openapi_security.py`
  - Prompt tests: `test_loader_checksum.py`, `test_loader_negative_checksum.py`
  - Schema tests: `test_schema_validation.py`, `test_manifest_version_invalid.py`

- ✅ **Makefile Targets**:
  - `make ci` - Ejecutar todas las validaciones
  - `make contracts-baseline` - Establecer baseline OpenAPI
  - `make prompts-fix-checksums` - Generar/reparar checksums

### DoD (100% Cumplido)
- ✅ **OpenAPI publicado**: `docs/openapi.yaml` con baseline en `docs/.baseline/`
- ✅ **Validaciones manifests en CI**: Workflow automático en cada PR
- ✅ **Documentación actualizada**: Informe completo + documentación sprint
- ✅ **Breaking change detection**: Automático en CI con baseline comparison
- ✅ **Tests pasando**: 56/56 tests (100% cobertura nuevas features)
- ✅ **Checksums validados**: SHA256 para todos los manifiestos
- ✅ **Security schemes**: bearerAuth + mTLS documentados

### Resultados Clave
- **29 archivos** creados/modificados
- **~1,889 líneas** añadidas
- **56 tests** pasando (6 nuevos)
- **100% cobertura** de nuevas features
- **0 breaking changes** detectados
- **~8.5s** tiempo de CI

### Smoke Tests Ejecutados
```bash
✅ YAML syntax: OK
✅ Schema validation: OK
✅ Checksums: OK (compute + check)
✅ OpenAPI breaking changes: NONE
✅ Tests: 56 passed in 8.54s
✅ Bearer auth: Present in both endpoints
```

### Manifiestos Implementados
| Manifest | ID | Versión | Uso |
|----------|----|---------|----- |
| `default.yaml` | default | 1.0.0 | Asistente general con guardrails |
| `voice.yaml` | voice_assistant | 1.0.0 | Optimizado para interfaces de voz |
| `xr.yaml` | xr_assistant | 1.0.0 | Asistente XR con referencias espaciales |

### Endpoints OpenAPI Completos
| Endpoint | Método | Auth | Response | Formato |
|----------|--------|------|----------|---------|
| `/api/v1/inference` | POST | bearerAuth | 200, 503 | JSON |
| `/api/v1/inference:stream` | POST | bearerAuth | 200, 401 | text/event-stream |

### Preparado para S1.5 (Contract Validation Detallada)
- ✅ Contratos OpenAPI definidos
- ✅ Sistema de prompts listo
- ✅ CI/CD validando contratos
- ✅ Baseline para breaking changes

## S1.5 — Contract Validation Detallada 🟡 **RECOMENDADO**

> **Estado**: ⏸️ **PLANIFICADO**  
> **Prioridad**: 🟡 **MEDIO** (reduce deuda técnica)  
> **Branch**: `feat/s1.5-contract-validation`  
> **Duración**: 1-2 semanas

### Meta
- Reforzar validación de contratos con headers obligatorios (`Idempotency-Key`, `X-Request-Id`), fuzzing con Schemathesis, autogeneración de SDKs desde OpenAPI, y breaking-changes CI endurecido.

### Entregables

#### **1. Headers Obligatorios Enforcement**

```yaml
# Enforce headers en todos los endpoints

required_headers:
  - X-Request-Id: "UUID4 generado por client o gateway"
  - Idempotency-Key: "Unique key para POST requests (opcional pero recomendado)"
  - Authorization: "Bearer JWT token"

middleware:
  # src/middleware/required_headers.py
  - Valida presencia de X-Request-Id (genera si falta)
  - Valida formato Idempotency-Key si presente
  - Retorna 400 Bad Request si headers críticos missing
```

**Implementación**:

```python
# src/middleware/required_headers.py

from fastapi import Request, HTTPException
import uuid

async def validate_request_headers(request: Request):
    """Validate required headers."""
    
    # X-Request-Id (obligatorio)
    request_id = request.headers.get("X-Request-Id")
    if not request_id:
        # Auto-generate si falta
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
    else:
        # Validate UUID format
        try:
            uuid.UUID(request_id)
            request.state.request_id = request_id
        except ValueError:
            raise HTTPException(400, "Invalid X-Request-Id format (must be UUID)")
    
    # Idempotency-Key (opcional pero validado si presente)
    if request.method == "POST":
        idempotency_key = request.headers.get("Idempotency-Key")
        if idempotency_key:
            # Validate format (alphanumeric + hyphens, 16-64 chars)
            if not re.match(r'^[a-zA-Z0-9\-]{16,64}$', idempotency_key):
                raise HTTPException(400, "Invalid Idempotency-Key format")
            request.state.idempotency_key = idempotency_key
```

#### **2. Schemathesis Property-Based Testing**

```python
# tests/contract/test_schemathesis_fuzzing.py

import schemathesis

schema = schemathesis.from_path("docs/openapi.yaml")

@schema.parametrize()
def test_api_fuzzing(case):
    """Property-based testing con Schemathesis."""
    response = case.call()
    case.validate_response(response)
    
    # Additional checks
    assert response.status_code in [200, 400, 401, 403, 429, 500, 503]
    assert "application/json" in response.headers.get("content-type", "")
```

#### **3. SDK Autogeneración desde OpenAPI**

```bash
# scripts/generate_sdks.sh

# Python SDK
openapi-python-client generate \
  --path docs/openapi.yaml \
  --output-path sdks/python

# TypeScript SDK
npx openapi-typescript docs/openapi.yaml \
  --output sdks/typescript/types.ts

openapi-generator-cli generate \
  -i docs/openapi.yaml \
  -g typescript-fetch \
  -o sdks/typescript

# Go SDK
openapi-generator-cli generate \
  -i docs/openapi.yaml \
  -g go \
  -o sdks/go
```

#### **4. Breaking Changes CI Endurecido**

```python
# scripts/detect_openapi_breaking_changes.py (ENHANCED)

breaking_changes = {
    # Existing checks
    "removed_paths": [],
    "removed_methods": [],
    "removed_200_responses": [],
    
    # NEW: Stricter checks
    "changed_request_schema": [],      # Request schema changes
    "changed_response_schema": [],     # Response schema changes
    "removed_required_fields": [],     # Required fields removed
    "changed_enum_values": [],         # Enum values changed
    "changed_parameter_types": [],     # Parameter type changes
}

# Fail CI si hay breaking changes (no solo warn)
if any(breaking_changes.values()):
    print("❌ BREAKING CHANGES DETECTED")
    sys.exit(1)
```

### DoD

- [ ] **Headers enforcement**: `X-Request-Id` + `Idempotency-Key` validados
- [ ] **Schemathesis**: 1000+ fuzzing tests generados automáticamente
- [ ] **SDKs autogenerados**: Python, TypeScript, Go desde OpenAPI
- [ ] **Breaking changes CI**: Endurecido (fail on any breaking change)
- [ ] **Tests**: 20+ tests adicionales (headers, fuzzing, SDK)

## S2 — Engine Core (Realtime HTTP + PromptResolver + Macro-Módulos Composition)

### Meta
- Inferencia realtime con resolución de prompts, anti-injection, y **composición de 4 macro-módulos** (ASM/CGN/AWE/SHIF).

### Entregables

#### **1. PromptResolver** (FS-based)
- `AsyncTTLCache` (TTL 15m), preload top-N
- Budget timeout 15ms, fallback embedded
- Hot-reload sin downtime (file watcher)

#### **2. Sanitización Anti-Injection**
- Role isolation (user vs system vs assistant)
- Meta-instruction stripping
- 10+ tests anti-injection (SQL, prompt leak, jailbreak)

#### **3. RealtimeEngine**
- Circuit breaker por provider (open/half-open/close)
- Semáforo de concurrencia (max 100 concurrent)
- Timeouts configurables (default 30s)

#### **4. Macro-Módulos Composition Engine** ✨ **CORE RESPONSIBILITY**

> **Arquitectura**: Inference Service actúa como **orchestrator** que compone los 4 macro-módulos (ASM/CGN/AWE/SHIF) vía mTLS+JWT para generar respuestas complejas.

**Composición Pattern**:

```python
# src/engine/composition.py

class MacroModulesComposer:
    """Orquesta ASM/CGN/AWE/SHIF para respuestas complejas."""
    
    def __init__(self):
        self.asm_client = ASMClient()      # mTLS+JWT a asm-service
        self.cgn_client = CGNClient()      # mTLS+JWT a cgn-service
        self.awe_client = AWEClient()      # mTLS+JWT a awe-service
        self.shif_client = SHIFClient()    # mTLS+JWT a shif-service
    
    async def compose(
        self, 
        query: str, 
        context: dict,
        composition_strategy: str = "auto"  # auto | simple | full
    ) -> dict:
        """
        Compone macro-módulos según complexity del query.
        
        Args:
            query: User query
            context: {agent_id, tenant_id, tier, session_id}
            composition_strategy: 
                - "auto": Decide automáticamente (ML classifier)
                - "simple": Solo LLM directo (no macro-módulos)
                - "full": Compone todos los macro-módulos
        
        Returns:
            {
                "response": str,
                "composition_used": ["asm", "cgn"],  # cuáles se usaron
                "latency_breakdown": {
                    "asm_ms": 50,
                    "cgn_ms": 80,
                    "llm_ms": 120,
                    "total_ms": 250
                },
                "metadata": {...}
            }
        """
        
        # Paso 1: Routing decision (¿requiere macro-módulos?)
        requires_composition = await self._classify_complexity(query, context)
        
        if not requires_composition or composition_strategy == "simple":
            # LLM directo (fast path)
            return await self._direct_llm(query, context)
        
        # Paso 2: Parallel calls a macro-módulos (donde aplicable)
        tasks = []
        
        if await self._needs_state(query):
            tasks.append(self.asm_client.get_state(context["agent_id"]))
        
        if await self._needs_reasoning(query):
            tasks.append(self.cgn_client.reason(query, context))
        
        if await self._needs_workflow(query):
            tasks.append(self.awe_client.evolve_workflow(query, context))
        
        if await self._needs_integration(query):
            tasks.append(self.shif_client.execute_integration(query, context))
        
        # Ejecutar en paralelo (p95 < 150ms con 2-3 macro-módulos)
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Paso 3: Compose prompt final con resultados de macro-módulos
        enriched_prompt = self._build_composed_prompt(
            query=query,
            asm_state=results.get("asm"),
            cgn_reasoning=results.get("cgn"),
            awe_workflow=results.get("awe"),
            shif_data=results.get("shif")
        )
        
        # Paso 4: LLM call con contexto enriquecido
        response = await self.llm_provider.complete(enriched_prompt)
        
        return {
            "response": response,
            "composition_used": [k for k in results.keys() if results[k] is not None],
            "latency_breakdown": {...},
            "metadata": {...}
        }
```

**Configuración mTLS+JWT**:

```yaml
# config/macro_modules.yaml

macro_modules:
  asm_service:
    url: "https://asm-service.enis.svc.cluster.local:8443"
    timeout_ms: 200
    circuit_breaker:
      threshold: 5  # errores consecutivos
      timeout_s: 30
    retry:
      max_attempts: 2
      backoff_ms: [100, 200]
  
  cgn_service:
    url: "https://cgn-service.enis.svc.cluster.local:8443"
    timeout_ms: 300  # Reasoning puede ser más lento
    circuit_breaker:
      threshold: 3
      timeout_s: 60
  
  awe_service:
    url: "https://awe-service.enis.svc.cluster.local:8443"
    timeout_ms: 250
  
  shif_service:
    url: "https://shif-service.enis.svc.cluster.local:8443"
    timeout_ms: 500  # External APIs pueden ser lentas
    circuit_breaker:
      threshold: 10  # Más tolerante (depende de external APIs)

mtls_config:
  cert_path: "/etc/inference/certs/tls.crt"
  key_path: "/etc/inference/certs/tls.key"
  ca_path: "/etc/inference/certs/ca.crt"
  verify: true

jwt_s2s:
  issuer: "inference-service"
  audience: ["asm-service", "cgn-service", "awe-service", "shif-service"]
  scopes: ["macro.compose.execute", "macro.state.read"]
  expiration_s: 300  # 5 min (short-lived)
```

**Métricas OTel**:

```yaml
metrics:
  - inference_macro_composition_requests_total (labels: modules_used, tier)
  - inference_macro_composition_latency_ms (p50/p95/p99, breakdown por module)
  - inference_macro_composition_errors_total (labels: module, error_type)
  - inference_macro_module_circuit_breaker_state (labels: module, state=open|half_open|closed)
```

**Flujo de Composición (ejemplo)**:

```yaml
composition_flow:
  paso_1_routing_decision:
    input: "User query + context (tenant, tier, capabilities)"
    decision: "¿Requiere composición de macro-módulos o solo LLM directo?"
    rules:
      simple_query: "LLM directo (OpenAI/Anthropic) - sin macro-módulos"
      complex_query: "Compose ASM/CGN/AWE/SHIF - respuesta avanzada"
    
    ejemplos:
      simple: "¿Qué hora es? → GPT-4o-mini directo (no macro-módulos)"
      complex: "Analiza el estado de mis ventas y sugiere workflow → ASM+CGN+AWE+SHIF"
  
  paso_2_asm_adaptive_state:
    cuando: "Query requiere contexto/memoria del agent"
    llamada: "POST https://asm-service.enis.svc.cluster.local/api/v1/state/get"
    payload: "{agent_id, tenant_id, session_id}"
    response: "{state: {memory, context, preferences}, metadata}"
    uso: "Enriquecer prompt con estado del agent"
  
  paso_3_cgn_causal_graph:
    cuando: "Query requiere razonamiento causal o decisiones complejas"
    llamada: "POST https://cgn-service.enis.svc.cluster.local/api/v1/graph/reason"
    payload: "{query, state_from_asm, constraints}"
    response: "{causal_chain: [...], reasoning: '...', confidence: 0.95}"
    uso: "Guiar decisión del LLM con razonamiento causal"
  
  paso_4_awe_workflow_evolution:
    cuando: "Query requiere automatización o workflow"
    llamada: "POST https://awe-service.enis.svc.cluster.local/api/v1/workflow/evolve"
    payload: "{task, context, feedback_history}"
    response: "{workflow_steps: [...], optimizations: [...], confidence: 0.92}"
    uso: "Generar workflow evolutivo basado en ML"
  
  paso_5_shif_integration:
    cuando: "Query requiere integración con sistemas externos"
    llamada: "POST https://shif-service.enis.svc.cluster.local/api/v1/integrations/execute"
    payload: "{integration_type, credentials, payload}"
    response: "{data: {...}, status: 'success', latency_ms: 150}"
    uso: "Obtener data externa (ERP, CRM, APIs) para respuesta"
  
  paso_6_llm_final_composition:
    input: "Query + ASM state + CGN reasoning + AWE workflow + SHIF data"
    prompt_template: |
      System: Eres un agente empresarial.
      Context (ASM): {state}
      Reasoning (CGN): {causal_chain}
      Workflow (AWE): {steps}
      Data (SHIF): {external_data}
      User: {query}
    llm_call: "GPT-4 / Claude (con full context)"
    output: "Respuesta completa y contextualizada"
```

### DoD (expandido para incluir macro-módulos)

- ✅ p95 < 200ms (sin provider) — **sin macro-módulos**
- ✅ **p95 < 400ms con composición de 2-3 macro-módulos** (parallelization)
- ✅ `resolve` < 15ms (cache caliente)
- ✅ 10 tests anti-injection
- ✅ `/readyz` reporta `prompts_loaded`
- ✅ **Macro-módulos integration**:
  - ✅ mTLS+JWT s2s hacia ASM/CGN/AWE/SHIF verificado
  - ✅ Circuit breakers funcionando (simulación de failures)
  - ✅ Parallel calls optimizados (2-3 módulos en < 150ms p95)
  - ✅ Fallback graceful: Si macro-módulo down → LLM directo (degraded but functional)
  - ✅ Contract tests con cada macro-módulo (staging o comprehensive mocks)
- ✅ **Composition strategy**:
  - ✅ Auto-classification de complexity (ML-based o rules-based)
  - ✅ Simple queries → LLM directo (fast path, no overhead)
  - ✅ Complex queries → Compose macro-módulos (value-add path)
  - ✅ Metrics: % queries usando composition (target: 20-30% en Tier 2/3)

## S2.5 — Batch Infrastructure Prep ⏸️ **PLANIFICADO**

> **Estado**: ⏸️ **PLANIFICADO**  
> **Branch**: `feat/s2.5-batch-infrastructure`  
> **Documentación**: Disponible en docs/02-sprint/S2.5/

### Meta
- Infraestructura completa para batch processing (Celery + Redis + DLQ + Idempotency), preparando el terreno para S3.

### Contexto y Justificación

**Problema**: S3 requiere infraestructura batch completa que S2 no provee:
- ❌ Redis en S2 es in-memory (no distribuido)
- ❌ No hay Celery workers configurados
- ❌ No existe sistema de DLQ (Dead Letter Queue)
- ❌ Falta sistema de idempotency

**Solución**: S2.5 prepara toda la infraestructura batch, permitiendo que S3 se enfoque exclusivamente en lógica de negocio.

**Impacto en Timeline**:
- **Sin S2.5**: S3 = Infraestructura + Lógica → 3-4 semanas (alto riesgo)
- **Con S2.5**: S2.5 (3-5 días) + S3 (1-2 semanas) → 2.5-3 semanas total ✅

### Entregables Detallados

#### **1. Redis Production Setup** 🔴 CRÍTICO
- ✅ Redis 7.4 Alpine con connection pool (max 50 connections)
- ✅ AsyncTTLCache con Redis backend real (reemplaza in-memory de S2)
- ✅ Healthcheck integration en `/readyz`
- ✅ Sentinel para HA (documentado para producción)
- ✅ Fallback automático a in-memory si Redis down
- **Tests**: 8 tests (connection, cache, TTL, pool, failover)

#### **2. Celery Base Configuration** 🔴 CRÍTICO
- ✅ Celery app factory con Redis broker
- ✅ Task base classes con retry logic integrado
- ✅ Worker process scripts (Linux/macOS + Windows .ps1)
- ✅ Result backend (Redis DB 1, separado del broker)
- ✅ Task routing configuration (default/batch queues)
- **Tests**: 5 tests (app creation, task routing, execution)

#### **3. Task Serialization & Idempotency** 🔴 CRÍTICO
- ✅ JSON serializer para Celery tasks (human-readable)
- ✅ Idempotency key management: `idempotency:{tenant_id}:{task_id}`
- ✅ TTL 24h para idempotency keys (configurable)
- ✅ BatchJob Pydantic models (`BatchJob`, `BatchJobCreate`, `BatchJobResponse`)
- ✅ Deduplication logic con Redis hash
- **Tests**: 14 tests (serialization 6 + idempotency 8)

#### **4. DLQ (Dead Letter Queue) Setup** 🔴 CRÍTICO
- ✅ DLQ queue en Redis (`celery:dlq`)
- ✅ Retry policy: 3 intentos con exponential backoff (1s, 2s, 4s)
- ✅ DLQ handler para inspección manual
- ✅ Scripts para requeue desde DLQ (preparado para S3)
- ✅ Alerting threshold (100 items)
- **Tests**: 7 tests (DLQ routing, retry, backoff, requeue)

#### **5. Worker Monitoring & Metrics** 🟡 ALTO
- ✅ Métricas Celery: queued, running, done, failed
- ✅ Worker health endpoint: `GET /api/v1/workers/status`
- ✅ Active tasks count por tenant
- ✅ Queue depth monitoring (real-time)
- ✅ Flower dashboard (http://localhost:5555)
- **Tests**: 5 tests (metrics API, queue depth, worker stats)

#### **6. BONUS: mTLS + JWT Scaffold** 🟡 MEDIO
- ✅ Certificate loader (`src/core/certs.py`) - mock para tests
- ✅ JWT s2s generator stub (`src/core/jwt_utils.py`)
- ✅ BaseClient scaffold con mTLS+JWT signature (`src/clients/base.py`)
- ✅ Config structure para S8 (Security) y S12 (NOPS)
- **Tests**: 4 tests (cert loading, validation)
- **Nota**: Implementación completa en S8 (Security)

### Archivos a Crear/Modificar

**Nuevos (32 archivos)**:
```text
config/
├─ celery_config.py           # Celery broker/backend config
├─ redis_config.yaml          # Redis + Sentinel config
├─ dlq_config.yaml            # DLQ policy + alerting
└─ mtls_config.yaml           # mTLS scaffold (S8)

src/core/
├─ redis_client.py            # Redis client con connection pool
├─ cache.py                   # MODIFICADO: Redis backend
├─ certs.py                   # Certificate loader (scaffold)
└─ jwt_utils.py               # JWT s2s generator (scaffold)

src/workers/
├─ __init__.py
├─ celery_app.py              # Celery app factory
├─ tasks.py                   # Task base classes
├─ serializers.py             # JSON serialization
├─ idempotency.py             # Idempotency store
├─ dlq.py                     # Dead letter queue handler
├─ retry_policy.py            # Retry config
└─ metrics.py                 # Worker metrics

src/models/
└─ batch_job.py               # BatchJob Pydantic models

src/clients/
├─ __init__.py
└─ base.py                    # BaseClient scaffold (S12)

src/api/v1/endpoints/
└─ workers.py                 # Worker status API

scripts/
├─ start_worker.sh            # Worker script (Linux/macOS)
└─ windows/
   └─ start_worker.ps1        # Worker script (Windows)

tests/
├─ test_redis_connection.py   # Redis tests (6 tests)
├─ test_redis_cache.py        # Cache tests (8 tests)
├─ test_celery_setup.py       # Celery tests (5 tests)
├─ test_serialization.py      # Serialization (6 tests)
├─ test_idempotency.py        # Idempotency (8 tests)
├─ test_dlq.py                # DLQ tests (7 tests)
├─ test_retry_policy.py       # Retry policy (4 tests)
├─ test_worker_metrics.py     # Metrics (5 tests)
├─ test_certs.py              # Certs (4 tests)
├─ conftest.py                # Test fixtures
└─ integration/
   └─ test_batch_flow.py      # Integration tests (8 tests)

docker-compose.workers.yml    # Redis + Workers + Flower
docs/HOWTO_S2.5.md           # Quick start guide
```

**Modificados (5 archivos)**:
- `requirements.txt` → + celery==5.4.0, redis==5.1.0, flower==2.0.1
- `pyproject.toml` → + dependencies
- `Makefile` → + worker, flower, redis, monitor-queue targets
- `src/core/cache.py` → Redis backend (mantiene fallback in-memory)
- `src/api/v1/router.py` → + workers endpoint

### DoD (100% Completo para Merge)

#### Infrastructure ✅
- [ ] Redis healthy en docker-compose (CMD: `redis-cli ping`)
- [ ] Celery worker inicia sin errores (`make worker`)
- [ ] Connection pool configurado (max 50, healthcheck 30s)
- [ ] AsyncTTLCache usa Redis real (no in-memory en producción)
- [ ] Flower dashboard accesible (http://localhost:5555)

#### Batch Core ✅
- [ ] Task serialization funcional (JSON, human-readable)
- [ ] Idempotency previene duplicados (mismo task_id → cached result)
- [ ] DLQ recibe failed tasks (después de 3 retries)
- [ ] Retry policy con exponential backoff (1s, 2s, 4s)
- [ ] Task routing funciona (default/batch queues)

#### Monitoring ✅
- [ ] Worker metrics accesibles: `GET /api/v1/workers/status`
- [ ] Queue depth reportado correctamente (`LLEN celery`)
- [ ] `/readyz` incluye Redis + Celery health
- [ ] Flower dashboard funcional con task history
- [ ] DLQ size monitoreado (`LLEN celery:dlq`)

#### Testing & CI ✅
- [ ] 53 tests pasando (Redis 8 + Cache 8 + Celery 5 + Serialization 6 + Idempotency 8 + DLQ 7 + Retry 4 + Metrics 5 + Certs 4 + Integration 8)
- [ ] Coverage > 85% (`pytest --cov=src`)
- [ ] CI verde (lint + type + tests + integration)
- [ ] Integration tests con Redis real (docker-compose)
- [ ] Tests markeados correctamente (`@pytest.mark.integration`)

#### Documentation ✅
- [ ] HOWTO_S2.5.md completo (quick start + workflows)
- [ ] README actualizado con comandos workers
- [ ] Troubleshooting guide (S2.5-TROUBLESHOOTING.md)
- [ ] Docstrings en todos los módulos públicos
- [ ] Implementation guide (S2.5-IMPLEMENTATION-GUIDE.md)

#### DX (Developer Experience) ✅
- [ ] `make worker` inicia worker (Linux/macOS)
- [ ] `scripts/windows/start_worker.ps1` funcional (Windows)
- [ ] `docker-compose.workers.yml` documentado
- [ ] `make infra-up` / `make infra-down` funcionales
- [ ] `make monitor-queue` muestra queue depth en real-time

### Resultados Clave

- **32 archivos nuevos** (~1,400 líneas de código)
- **5 archivos modificados** (~150 líneas)
- **53 tests** (85%+ coverage)
- **Duración estimada**: 3-5 días
- **Complexity**: Media-Alta
- **0 deuda técnica**: Todo listo para S3

### Smoke Tests a Ejecutar

```bash
# 1. Start infrastructure
make infra-up
# Esperar: redis (healthy), worker (Up), flower (Up)

# 2. Check Redis
docker exec inference-redis redis-cli ping
# Expected: PONG

# 3. Check Celery worker
celery -A src.workers.celery_app inspect active
# Expected: {} (sin tasks activas)

# 4. Enqueue test task
python -c "
from src.workers.celery_app import app
result = app.send_task('workers.tasks.health_check')
print(f'Task ID: {result.id}')
print(f'Result: {result.get(timeout=10)}')
"
# Expected: {"status": "healthy", ...}

# 5. Check idempotency
python -c "
import asyncio
from src.workers.idempotency import check_idempotency, store_idempotency, clear_idempotency
async def test():
    tenant = 'test'; task = 'task-1'
    await clear_idempotency(tenant, task)
    r1 = await check_idempotency(tenant, task)
    print(f'First: {r1}')  # None
    await store_idempotency(tenant, task, 'result-123')
    r2 = await check_idempotency(tenant, task)
    print(f'Second: {r2}')  # result-123
asyncio.run(test())
"

# 6. Check worker status API
curl http://localhost:8081/api/v1/workers/status | jq .
# Expected: {"status": "healthy", "redis_healthy": true, ...}

# 7. Run full test suite
pytest tests/ -v
# Expected: 53 passed in ~8-10s

# 8. Check coverage
pytest --cov=src --cov-report=term
# Expected: >85% coverage
```

### Versiones Tecnológicas

| Componente | Versión | Justificación |
|------------|---------|---------------|
| Redis | 7.4-alpine | Latest stable, lightweight |
| Celery | 5.4.0 | Latest stable, Python 3.11 support |
| Redis-py | 5.1.0 | Async support, connection pooling |
| Flower | 2.0.1 | Latest, Celery 5.x compatible |
| Pydantic | 2.9.2 | (from S0) V2 performance |

### Preparado para S3 (Engine Batch & Workers)

- ✅ Redis production-ready con connection pooling
- ✅ Celery workers operativos (Linux/macOS/Windows)
- ✅ Idempotency store funcional (24h TTL, Redis hash)
- ✅ DLQ con retry policy configurable (exponential backoff)
- ✅ Monitoring completo (Flower dashboard + API endpoints)
- ✅ Tests comprehensivos (unit + integration, 85% coverage)
- ✅ Scripts multiplataforma (bash + PowerShell)
- ✅ Documentación completa (implementation + troubleshooting)

## S3 — Engine Batch & Workers (Lógica Batch Completa)

> **Dependencias**: ✅ S2.5 (infraestructura batch lista: Redis, Celery, DLQ, Idempotency)

### Meta
- Batch idempotente por tenant con endpoints completos, prioridad por colas, at-least-once delivery, cost tracking y cuotas por tenant.

### Entregables

#### **1. Endpoints Batch**

```python
# src/api/v1/endpoints/batch.py

@router.post("/batch/submit")
async def batch_submit(request: BatchSubmitRequest) -> BatchSubmitResponse:
    """
    Submit batch inference job.
    
    Request:
      {
        "tenant_id": "t_123",
        "jobs": [
          {"prompt": "...", "model": "gpt-4o-mini"},
          {"prompt": "...", "model": "gpt-4o-mini"}
        ],
        "priority": "normal",  # low | normal | high
        "idempotency_key": "batch_abc123"  # Opcional
      }
    
    Response:
      {
        "batch_id": "batch_456def",
        "job_ids": ["job_1", "job_2"],
        "status": "queued",
        "estimated_completion_time": "2025-10-10T13:00:00Z"
      }
    """

@router.get("/batch/{batch_id}/status")
async def batch_status(batch_id: str) -> BatchStatusResponse:
    """
    Get batch job status.
    
    Response:
      {
        "batch_id": "batch_456def",
        "status": "running",  # queued | running | completed | failed | cancelled
        "progress": {
          "total": 100,
          "completed": 45,
          "failed": 2,
          "running": 10,
          "queued": 43
        },
        "results_available": 45
      }
    """

@router.post("/batch/{batch_id}/cancel")
async def batch_cancel(batch_id: str) -> BatchCancelResponse:
    """Cancel batch job (best-effort)."""
```

#### **2. Prioridad por Colas**

```yaml
# config/batch_queues.yaml

queues:
  high_priority:
    name: "celery:high"
    max_workers: 20
    concurrency_per_tenant: 10
    use_cases: ["Tier 3 urgent", "SLA-critical"]
  
  normal_priority:
    name: "celery:default"
    max_workers: 50
    concurrency_per_tenant: 5
    use_cases: ["Tier 2/3 standard"]
  
  low_priority:
    name: "celery:low"
    max_workers: 10
    concurrency_per_tenant: 2
    use_cases: ["Tier 1 batch", "background jobs"]

routing:
  tier_3: "high_priority"
  tier_2: "normal_priority"
  tier_1: "low_priority"
```

#### **3. At-Least-Once + Idempotencia Dura**

```python
# src/workers/batch_processor.py

async def process_batch_job(
    job_id: str,
    tenant_id: str,
    payload: dict
) -> dict:
    """
    Process batch job con at-least-once + idempotencia dura.
    
    Idempotencia dura: Hash del payload completo
    (no solo job_id, previene duplicados con payload diferente)
    """
    # Hash payload para idempotencia dura
    payload_hash = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()
    ).hexdigest()
    
    idempotency_key = f"{tenant_id}:{job_id}:{payload_hash}"
    
    # Check idempotency (ya implementado en S2.5)
    cached_result = await check_idempotency(tenant_id, idempotency_key)
    if cached_result:
        return cached_result  # Ya procesado, return cached
    
    # Process job
    result = await engine.infer(payload["prompt"])
    
    # Store result para idempotency
    await store_idempotency(tenant_id, idempotency_key, result.id)
    
    return result
```

#### **4. Cost Tracking por Tenant**

```python
# src/engine/batch_cost_tracker.py

async def track_batch_cost(
    tenant_id: str,
    batch_id: str,
    job_results: list[dict]
) -> dict:
    """
    Track cost por batch job.
    
    Returns:
      {
        "tenant_id": "t_123",
        "batch_id": "batch_456",
        "total_cost_usd": 1.25,
        "total_tokens": {
          "input": 5000,
          "output": 3000,
          "total": 8000
        },
        "cost_breakdown": [
          {"job_id": "job_1", "cost_usd": 0.50, "tokens": 2000},
          {"job_id": "job_2", "cost_usd": 0.75, "tokens": 3000}
        ]
      }
    """
    # Emit billing event (S10)
    await event_bus.publish(
        event="billing.cost.incurred",
        payload={
            "tenant_id": tenant_id,
            "batch_id": batch_id,
            "total_cost_usd": total_cost,
            "timestamp": datetime.utcnow().isoformat()
        }
    )
```

#### **5. Cuotas por Tenant**

```yaml
# config/batch_quotas.yaml

tenant_quotas:
  tier_1:
    max_concurrent_batches: 2
    max_jobs_per_batch: 100
    max_daily_jobs: 1000
  
  tier_2:
    max_concurrent_batches: 10
    max_jobs_per_batch: 500
    max_daily_jobs: 10000
  
  tier_3:
    max_concurrent_batches: 50
    max_jobs_per_batch: 5000
    max_daily_jobs: 100000
```

### DoD (expandido con S2.5 como base)

- [ ] **Endpoints**: `/batch/submit`, `/batch/{id}/status`, `/batch/{id}/cancel` funcionales
- [ ] **Prioridad por colas**: high/normal/low routing por tier
- [ ] **At-least-once delivery**: Con idempotencia dura (hash payload)
- [ ] **No doble cobro**: Retries con mismo payload no duplican coste
- [ ] **DLQ tras 3 reintentos**: Exponential backoff (1s, 2s, 4s) - ya en S2.5
- [ ] **1000 jobs concurrentes**: Verificado con load test
- [ ] **Métricas**: `GET /batch/metrics` expone queued/running/done/failed por tenant
- [ ] **Cost tracking**: Eventos a billing-service por batch completado
- [ ] **Cuotas por tenant**: Max concurrent batches respetado

## S4 — Engine Streaming (SSE con Resume HMAC)

### Meta
- SSE estable con resume HMAC y auth para WS/SSE.

> **Nota de Coherencia con S6f/S16/S17**: El `resume_token` HMAC (formato `v<kid>:<offset>:<mac_b64url>`, TTL 5m) es el mismo mecanismo usado por Voice/XR streaming en S16/S17. La rotación de claves (kid) se comparte entre todos los endpoints streaming (inference/voice/xr).

### Entregables
- Multiplexing con `asyncio.Queue`
- **Heartbeats cada 15s** (SSE keepalive, previene proxy timeout)
- `resume_token` HMAC (kid, TTL = 5m) + rotación de claves automática
- Auth JWT en upgrade y headers (alineado con S1/S8)
- **Coherencia S6f/S16/S17**: Mismo formato `resume_token` para Voice/XR streaming
- **Backpressure handling**: Slow consumer detection + flow control

```python
# src/engine/streaming.py

async def stream_with_backpressure(
    request: InferenceRequest,
    max_queue_size: int = 100
) -> AsyncGenerator:
    """
    SSE streaming con backpressure handling.
    
    Si consumer es lento (queue >80% full):
    - Slow down chunk generation
    - Emit warning event
    - Continue (no disconnect)
    """
    queue = asyncio.Queue(maxsize=max_queue_size)
    
    async def producer():
        for chunk in llm_stream:
            # Backpressure check
            if queue.qsize() > max_queue_size * 0.8:
                await asyncio.sleep(0.05)  # Slow down
                metrics.backpressure_slow_consumer.inc()
            
            await queue.put(chunk)
    
    async def consumer():
        while True:
            chunk = await queue.get()
            yield chunk
```

### DoD
- [ ] **Streams > 5m sin disconnects** (tested con long-running inference)
- [ ] **Resume OK**: Reconexión sin pérdida >10 chunks (tested)
- [ ] **Token inválido → 401** Unauthorized
- [ ] **Sin memory leaks**: Streams activos monitoreados (no growth)
- [ ] **p95 chunk delivery < 100ms** (benchmarked)
- [ ] **Heartbeats cada 15s**: SSE keepalive funcional (tested con proxies)
- [ ] **Backpressure handling**: Slow consumer no causa disconnect (tested)
- [ ] **Resume token compartido**: Voice/XR usan mismo mecanismo (validado en S6f)

## S5 — Model Management (Hot-Reload con mem_guard)

### Meta
- Ciclo de vida con swap sin downtime y `mem_guard` cgroup v2 validado en CI.

### Entregables

#### **1. Dual-load + Atomic Swap**
- Dual-load pattern: Load new model antes de unload old
- Atomic swap: Switch pointer de forma atómica
- Rollback automático si new model falla health check
- Model cache: Keep 2 versiones en cache (current + previous)

#### **2. mem_guard cgroup v2** 🔴 CRÍTICO

```python
# src/core/mem_guard.py

class MemoryGuard:
    """Monitor memory con cgroup v2 y alerta headroom."""
    
    def __init__(self, headroom_multiplier: float = 1.3):
        self.headroom = headroom_multiplier
        self.cgroup_path = "/sys/fs/cgroup/memory.max"
    
    async def check_memory_headroom(self) -> dict:
        """
        Check memory headroom (current vs max).
        
        Formula: headroom_ratio = memory.current / (memory.max / 1.3)
        Alert si headroom_ratio > 0.9 (approaching limit)
        """
        memory_max = self._read_cgroup("memory.max")
        memory_current = self._read_cgroup("memory.current")
        
        safe_limit = memory_max / self.headroom  # 1.3x headroom
        headroom_ratio = memory_current / safe_limit
        
        if headroom_ratio > 0.9:
            # Alert: Approaching memory limit
            await metrics.memory_headroom_low.set(headroom_ratio)
            logger.warning(
                f"Memory headroom low: {headroom_ratio:.2%} "
                f"(current: {memory_current / 1024**3:.2f}GB, "
                f"safe_limit: {safe_limit / 1024**3:.2f}GB)"
            )
        
        return {
            "memory_current_gb": memory_current / 1024**3,
            "memory_max_gb": memory_max / 1024**3,
            "safe_limit_gb": safe_limit / 1024**3,
            "headroom_ratio": headroom_ratio,
            "alert": headroom_ratio > 0.9
        }
```

#### **3. Política de Swap**

```yaml
# config/model_swap_policy.yaml

swap_policy:
  in_pod_swap:
    enabled: true
    max_model_size_gb: 8  # Si modelo <8GB → in-pod swap
    strategy: "dual_load"
    
  blue_green:
    enabled: true
    min_model_size_gb: 8  # Si modelo ≥8GB → blue/green deployment
    strategy: "rolling_update"
    
  mem_guard:
    headroom_multiplier: 1.3  # Reserve 30% headroom
    alert_threshold: 0.9  # Alert at 90% of safe limit
    
  ci_validation:
    enabled: true
    test_cgroup: true
    fail_on_oom: true
```

#### **4. CI Validation mem_guard**

```yaml
# .github/workflows/model-swap-test.yml

name: Model Swap & Memory Guard

on:
  pull_request:
    paths: ['src/engine/model_manager.py', 'config/model_swap_policy.yaml']

jobs:
  test-mem-guard:
    runs-on: ubuntu-22.04
    steps:
      - name: Setup cgroup v2
        run: |
          sudo mount -t cgroup2 none /sys/fs/cgroup
          sudo mkdir -p /sys/fs/cgroup/test
          echo "1073741824" > /sys/fs/cgroup/test/memory.max  # 1GB limit
      
      - name: Test memory guard
        run: |
          pytest tests/engine/test_mem_guard.py \
            --cgroup-path /sys/fs/cgroup/test
      
      - name: Test model swap (10 cycles)
        run: |
          pytest tests/engine/test_model_swap.py \
            --cycles 10 \
            --check-oom
```

### DoD (expandido con mem_guard CI)

- [ ] **10× carga/descarga sin OOM**: Tested en CI con cgroup v2
- [ ] **Alerta `memory_headroom_low`**: Emitida cuando headroom ratio >0.9
- [ ] **Zero downtime**: Swap verificado en producción (no 503 errors)
- [ ] **Rollback probado**: Automatic rollback si new model fails
- [ ] **mem_guard validado en CI**: cgroup v2 tests pasando
- [ ] **Política enforcement**: <8GB in-pod, ≥8GB blue/green
- [ ] **Headroom 1.3x**: Reserva 30% memory headroom verificada

## S6  Providers & Integrations (Sub-sprints)

### S6a — OpenAI Provider

**Meta**: Chat/Embeddings/Vision; stream + batch con normalización de errores.

**Entregables**:
- GPT-4, GPT-4o, GPT-4o-mini, GPT-3.5-turbo support
- Streaming SSE + batch mode
- Errores normalizados a enum común: `RATE_LIMIT | TIMEOUT | CONTENT_FILTER | QUOTA_EXCEEDED | UNAVAILABLE`
- Retry budgets por provider (max 3 retries)
- Exponential backoff con jitter (base 2s, max 60s)

**DoD**:
- Contract tests con OpenAI API
- Rate limits respetados (429 → backoff)
- Errores mapeados a enum común
- Fallback a otros providers si UNAVAILABLE

### S6b — Anthropic Provider

**Meta**: Messages API + tool-use; stream con normalización.

**Entregables**:
- Claude-3-opus, Claude-3.5-sonnet, Claude-3-haiku support
- Streaming SSE
- Tool-use (function calling) support
- Errores normalizados a enum común
- Retry budgets (max 3 retries)

**DoD**:
- Contract tests con Anthropic API
- Fallback integrado si provider down
- Errores normalizados (429/500/503 → enum común)

### S6c — Groq Provider

**Meta**: Llama-3.1-70B / Mixtral-8x7B / Gemma-7B con retry agresivo.

**Entregables**:
- 3 modelos operativos (Llama, Mixtral, Gemma)
- Model IDs por ENV/Helm (no hardcoded)
- Backoff rate-limit agresivo (Groq límites estrictos)
- Errores normalizados a enum común

**DoD**:
- 3 modelos operativos y tested
- Fallback chain OK (Groq → OpenAI si rate limit)
- Rate limits respetados
- Errores normalizados

### S6d — Local Runtimes

**Meta**: PyTorch + ONNX; OSS models (Llama/Mistral); quantization INT8/INT4.

**Entregables**:
- PyTorch runtime (GPU/CPU)
- ONNX runtime (CPU optimized)
- Quantization: INT8 (4x faster), INT4 (8x faster)
- GPU/CPU auto-detection
- Model zoo: Llama-3.1-7B, Mistral-7B

**DoD**:
- GPU/CPU detection automático
- INT8 quantization 4x faster verificado
- Guía hardware requirements (GPU: A100/H100, CPU: 32GB RAM)

### S6e — Air-Gapped

**Meta**: Zero egress validado con NetworkPolicy + DNS tests.

**Entregables**:
- NetworkPolicy: DNS-only (kube-dns permitido, external DNS bloqueado)
- CI test: `docker --network=none` (build funciona offline)
- DNS tests: `getaddrinfo` a google.com falla, kube-dns.svc.cluster.local OK
- Local models bundle para offline

**DoD**:
- Zero egress probado (no external API calls)
- DNS tests pos/neg pasando
- CI `--network=none` verde
- Bundle offline funcional

### S6f — FE Backend Readiness (Voice/XR) — Congelar APIs Backend

> ⚠️ **NOTA ARQUITECTÓNICA CRÍTICA**:
> - Este sprint **NO implementa** Voice/XR completo (STT/VAD/TTS/OpenXR).
> - Solo **congela contratos y tipos backend** que Voice/XR services consumirán.
> - **Backend implementation** en:
>   - **S16** — Voice Backend Integration (integra con `voice-interface-service`)
>   - **S17** — XR Backend Integration (integra con `xr-interface-service`)
> - **Voice/XR full stack** se implementa en repositorios separados:
>   - Repo 15: `cloud-core/voice-interface-service` (STT/VAD/TTS/WebRTC)
>   - Repo 16: `cloud-core/xr-interface-service` (OpenXR/Spatial/Gesture/Render)

#### Meta
Congelar **contratos y tipos backend** para Voice/XR sin implementar STT/VAD/TTS/OpenXR en este repo, facilitando integración futura en S16/S17.

#### Protocolos y Endpoints Congelados (Backend API)

**Voice (backend endpoints para `voice-interface-service`)**:
```text
POST /api/v1/inference/voice:query       # Query LLM con contexto voice
POST /api/v1/inference/voice:stream      # SSE streaming para voice
GET  /api/v1/inference/voice/models      # Lista de modelos voice-capable
```

**Payload example**:
```json
{
  "query": "¿Cuál es el estado de mi pedido?",
  "voice_context": {
    "session_id": "voice_sess_123",
    "audio_metadata": {
      "sample_rate": 16000,
      "codec": "pcm16",
      "vad_confidence": 0.95
    },
    "conversation_history": [...]
  },
  "tenant_id": "t_12345",
  "tier": "tier_3",
  "model_preference": "gpt-4o-mini"  // Voice-optimized model
}
```

**XR (backend endpoints para `xr-interface-service`)**:
```text
POST /api/v1/inference/xr:query          # Query LLM con contexto XR (spatial/gesture)
POST /api/v1/inference/xr:stream         # SSE streaming para XR
GET  /api/v1/inference/xr/models         # Lista de modelos vision-capable
```

**Payload example**:
```json
{
  "query": "Muestra el layout 3D del warehouse",
  "xr_context": {
    "session_id": "xr_sess_456",
    "spatial_data": {
      "gaze_direction": [0.5, 0.2, 0.8],
      "hand_pose": {"left": {...}, "right": {...}},
      "anchor_id": "spatial_anchor_789"
    },
    "gesture_detected": "pinch_to_select",
    "camera_frame": null  // Opcional: vision input (base64 si aplica)
  },
  "tenant_id": "t_12345",
  "tier": "tier_3",
  "model_preference": "gpt-4o-vision"  // Vision-capable model
}
```

#### Contratos TypeScript (d.ts) - Backend

```typescript
// src/contracts/voice.d.ts

export interface VoiceQueryRequest {
  query: string;
  voice_context: {
    session_id: string;
    audio_metadata: {
      sample_rate: number;
      codec: "pcm16" | "opus";
      vad_confidence: number;
    };
    conversation_history?: Message[];
  };
  tenant_id: string;
  tier: "tier_1" | "tier_2" | "tier_3";
  model_preference?: string;
}

export interface VoiceQueryResponse {
  response: string;
  metadata: {
    model_used: string;
    latency_ms: number;
    tokens: { input: number; output: number };
    composition_used?: string[];  // ASM/CGN/AWE/SHIF si aplica
  };
  session_id: string;
  timestamp: string;
}

// src/contracts/xr.d.ts

export interface XRQueryRequest {
  query: string;
  xr_context: {
    session_id: string;
    spatial_data: {
      gaze_direction: [number, number, number];
      hand_pose?: {
        left?: HandPose;
        right?: HandPose;
      };
      anchor_id?: string;
    };
    gesture_detected?: string;
    camera_frame?: string;  // base64 encoded (opcional)
  };
  tenant_id: string;
  tier: "tier_1" | "tier_2" | "tier_3";
  model_preference?: string;
}

export interface XRQueryResponse {
  response: string;
  metadata: {
    model_used: string;
    latency_ms: number;
    tokens: { input: number; output: number };
    vision_processed: boolean;
    composition_used?: string[];
  };
  session_id: string;
  timestamp: string;
}
```

#### SDK Alpha (TypeScript)

```typescript
// @enis/client Alpha - Backend API client

import { ENISClient } from '@enis/client';

const client = new ENISClient({
  baseURL: 'https://inference.enis.svc.cluster.local',
  apiKey: process.env.ENIS_API_KEY,
  tier: 'tier_3'
});

// Voice backend API
const voiceResponse = await client.inference.voice.query({
  query: "¿Cuál es mi agenda de hoy?",
  voice_context: {
    session_id: "voice_sess_123",
    audio_metadata: { sample_rate: 16000, codec: "pcm16", vad_confidence: 0.95 }
  }
});

// XR backend API
const xrResponse = await client.inference.xr.query({
  query: "Muestra el producto en 3D",
  xr_context: {
    session_id: "xr_sess_456",
    spatial_data: { gaze_direction: [0.5, 0.2, 0.8] }
  }
});

// Hooks React (mocks for now)
import { useInferenceVoice, useInferenceXR } from '@enis/client/react';

function VoiceComponent() {
  const { query, isLoading, response } = useInferenceVoice();
  
  const handleQuery = () => {
    query({
      query: "Hola, ¿cómo estás?",
      voice_context: { session_id: "sess_123", audio_metadata: {...} }
    });
  };
  
  return <div>{response}</div>;
}
```

#### Ejemplos y Storybook

- **Ejemplos React + Vanilla**: 
  - `examples/voice-console/` — Mock de Voice Console usando backend APIs
  - `examples/xr-panel/` — Mock de XR Panel usando backend APIs
  - **NOTA**: STT/TTS/OpenXR son mocks (no implementados aquí)

- **Storybook**:
  - `<VoiceBackendClient/>` — Component que consume `/inference/voice:query`
  - `<XRBackendClient/>` — Component que consume `/inference/xr:query`
  - Mock responses del Sandbox (S7)

#### Tests y Resiliencia

- **Contract tests FE/BE** (Playwright headless):
  - Test: Backend `/inference/voice:query` responde schema correcto
  - Test: Backend `/inference/xr:query` responde schema correcto
  - Test: `resume_token` funciona en streaming SSE
  - Test: Errores (401/429/500) retornan formato estándar

- **CORS/Auth/Resiliencia**:
  - CORS allowlist por entorno (dev/staging/prod)
  - JWT refresh automático en SDK
  - WS ping 20-30s, SSE heartbeat 15s
  - Fallbacks: WS → SSE → long-poll (degraded but functional)

- **Métricas correladas**:
  - FE propaga `X-Request-Id` (S10) en todos los requests
  - Backend logs incluyen `X-Request-Id` para correlación E2E

#### DoD

- ✅ **SDK Alpha publicado** (`@enis/client` v0.1.0-alpha) con features:
  - ✅ Reconexión automática con `resume_token` (SSE)
  - ✅ Retry logic con exponential backoff
  - ✅ Auto-refresh JWT tokens
  - ✅ TypeScript + Python versions
- ✅ **Ejemplos corriendo contra Sandbox** (mocks de Voice/XR)
- ✅ **Storybook build en verde** (components backend client)
- ✅ **Tests de contrato FE/BE en CI** (Playwright headless)
- ✅ **Endpoints y tipos TS congelados en CI**: Breaking changes bloqueados
  - ✅ `/api/v1/inference/voice:query` | `/voice:stream` | `/voice/models`
  - ✅ `/api/v1/inference/xr:query` | `/xr:stream` | `/xr/models`
  - ✅ TypeScript types exportados (`VoiceQueryRequest`, `XRQueryRequest`, etc.)
- ✅ **Cross-refs explícitas**:
  - ✅ README explica que este sprint NO implementa STT/VAD/TTS/OpenXR
  - ✅ README referencia **S16** para Voice Backend Integration (repo 15)
  - ✅ README referencia **S17** para XR Backend Integration (repo 16)
  - ✅ OpenAPI comments linkan a S16/S17 en cada endpoint Voice/XR

## S7 — Sandbox Seguro (Multi-Tenant) con DGE Integration

### Meta
Budgets atómicos + auditoría + **PII/PHI/PCI delegada a DGE** (Data Governance Engine).

### Entregables

#### **1. Integración DGE** (cloud-core/data-governance-service)

> **Arquitectura**: Inference **NO clasifica/redacta PII** localmente. Delega a DGE service vía mTLS+JWT.

**Cliente DGE**:

```python
# src/integrations/dge_client.py

class DGEClient:
    """Client para Data Governance Engine (PII/PHI/PCI classification/redaction)."""
    
    def __init__(self):
        self.base_url = "https://data-governance-service.enis.svc.cluster.local:8443"
        self.timeout_ms = 5000  # Tier 3: fail-closed si >5s
        self.cache_ttl = 300  # 5 min cache para políticas
    
    async def classify(
        self,
        content: str,
        tenant_id: str,
        tier: str,
        correlation_id: str
    ) -> dict:
        """
        Clasificar contenido (PII/PHI/PCI).
        
        POST /api/v1/dge/classify
        
        Returns:
            {
                "labels": ["PII", "EMAIL"],
                "confidence": 0.98,
                "policy_action": "block",  # block | alert | redact | allow
                "cache_key": "sha256:abc..."
            }
        """
        # Fail-closed para Tier 3 si timeout >5s
        if tier == "tier_3":
            try:
                response = await self.request(
                    method="POST",
                    path="/api/v1/dge/classify",
                    json={"content": content, "tenant_id": tenant_id},
                    timeout_ms=self.timeout_ms,
                    correlation_id=correlation_id
                )
                return response
            except TimeoutError:
                # Fail-closed: Block si DGE no responde
                return {
                    "labels": ["TIMEOUT"],
                    "confidence": 1.0,
                    "policy_action": "block",
                    "error": "DGE timeout (fail-closed Tier 3)"
                }
        else:
            # Tier 1/2: Best-effort (no bloquea si DGE down)
            try:
                response = await self.request(...)
                return response
            except Exception as e:
                return {
                    "labels": [],
                    "confidence": 0,
                    "policy_action": "allow",
                    "error": str(e)
                }
    
    async def redact(
        self,
        content: str,
        labels: list[str],
        tenant_id: str
    ) -> str:
        """
        Redactar contenido según labels (PII → [REDACTED_EMAIL], PHI → [REDACTED_MEDICAL]).
        
        POST /api/v1/dge/redact
        """
        response = await self.request(
            method="POST",
            path="/api/v1/dge/redact",
            json={"content": content, "labels": labels, "tenant_id": tenant_id}
        )
        return response["redacted_content"]
```

**Configuración DGE**:

```yaml
# config/dge.yaml

dge_service:
  url: "https://data-governance-service.enis.svc.cluster.local:8443"
  timeout_ms: 5000  # Tier 3 fail-closed
  
  policies:
    tier_3:
      fail_mode: "closed"  # Block si DGE down o timeout
      pii_action: "block"
      phi_action: "block"
      pci_action: "block"
    
    tier_2:
      fail_mode: "open"  # Best-effort
      pii_action: "redact"
      phi_action: "block"
      pci_action: "block"
    
    tier_1:
      fail_mode: "open"
      pii_action: "allow"
      phi_action: "redact"
      pci_action: "redact"
  
  cache:
    enabled: true
    ttl_s: 300  # 5 min cache para políticas (no para contenido)
    max_size_mb: 100

mtls_config:
  cert_path: "/etc/inference/certs/tls.crt"
  key_path: "/etc/inference/certs/tls.key"
  ca_path: "/etc/inference/certs/ca.crt"

jwt_s2s:
  issuer: "inference-service"
  audience: ["data-governance-service"]
  scopes: ["dge.classify.execute", "dge.redact.execute"]
  expiration_s: 300
```

**Flujo de Validación DGE**:

```yaml
dge_validation_flow:
  paso_1_classify_prompt:
    cuando: "Antes de enviar prompt a LLM"
    llamada: "POST /api/v1/dge/classify"
    input: "{content: prompt, tenant_id, tier}"
    output: "{labels: [PII, EMAIL], policy_action: block, confidence: 0.98}"
    
  paso_2_enforce_policy:
    if: "policy_action == block AND tier == tier_3"
    action: "Return 403 Forbidden - PII detected in Tier 3"
    audit: "POST /api/v1/compliance/audit (event: dge.block)"
    
  paso_3_redact_if_needed:
    if: "policy_action == redact"
    llamada: "POST /api/v1/dge/redact"
    input: "{content: prompt, labels: [EMAIL, PHONE]}"
    output: "{redacted_content: 'Mi email es [REDACTED_EMAIL]'}"
    
  paso_4_llm_call:
    input: "Redacted prompt (si aplica)"
    output: "LLM response"
    
  paso_5_classify_output:
    cuando: "Después de LLM response"
    llamada: "POST /api/v1/dge/classify"
    input: "{content: llm_output, tenant_id, tier}"
    enforce: "Misma política que prompt (block/redact si aplica)"
```

#### **2. Budgets Atómicos** (Redis Lua)

```lua
-- redis_scripts/check_and_increment_budget.lua

-- Verificar y consumir budget de forma atómica
local tenant_key = KEYS[1]
local cost_usd = tonumber(ARGV[1])
local hard_limit_usd = tonumber(ARGV[2])
local soft_limit_usd = tonumber(ARGV[3])

local current = tonumber(redis.call('GET', tenant_key) or 0)
local new_total = current + cost_usd

if new_total > hard_limit_usd then
  return {-1, current}  -- Hard limit exceeded
elseif new_total > soft_limit_usd then
  redis.call('INCRBY', tenant_key, cost_usd)
  return {1, new_total}  -- Soft limit exceeded (allow but alert)
else
  redis.call('INCRBY', tenant_key, cost_usd)
  return {0, new_total}  -- OK
end
```

**Integración Budgets**:

```python
# src/engine/budget_guard.py

class BudgetGuard:
    """Guardas atómicas de coste por tenant."""
    
    async def check_and_increment(
        self,
        tenant_id: str,
        cost_usd: float,
        correlation_id: str
    ) -> dict:
        """
        Verificar budget antes de LLM call (atómico via Redis Lua).
        
        Returns:
            {
                "allowed": bool,
                "current_usage_usd": float,
                "limit_exceeded": "hard" | "soft" | null,
                "remaining_budget_usd": float
            }
        """
        # Lua script (atómico)
        result = await self.redis.eval(
            script=CHECK_AND_INCREMENT_SCRIPT,
            keys=[f"budget:{tenant_id}:monthly"],
            args=[cost_usd, hard_limit, soft_limit]
        )
        
        status, current_usage = result
        
        if status == -1:
            # Hard limit exceeded → Block
            await self.event_bus.publish(
                event="billing.budget_exceeded",
                payload={
                    "tenant_id": tenant_id,
                    "limit_type": "hard",
                    "current_usage_usd": current_usage,
                    "correlation_id": correlation_id
                }
            )
            return {"allowed": False, "limit_exceeded": "hard"}
        
        elif status == 1:
            # Soft limit exceeded → Allow pero alert
            await self.event_bus.publish(
                event="billing.budget_warning",
                payload={
                    "tenant_id": tenant_id,
                    "limit_type": "soft",
                    "current_usage_usd": current_usage,
                    "correlation_id": correlation_id
                }
            )
            return {"allowed": True, "limit_exceeded": "soft"}
        
        else:
            # OK
            return {"allowed": True, "limit_exceeded": None}
```

#### **3. Audit Logs** (compliance-service)

```python
# src/integrations/compliance_client.py

async def audit_log(
    event_type: str,
    tenant_id: str,
    metadata: dict,
    correlation_id: str
) -> None:
    """
    Enviar audit log a compliance-service (inmutable, 10+ años retención).
    
    POST /api/v1/compliance/audit
    """
    await compliance_client.request(
        method="POST",
        path="/api/v1/compliance/audit",
        json={
            "event_type": event_type,
            "tenant_id": tenant_id,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": metadata,
            "correlation_id": correlation_id
        }
    )
```

#### **4. Mock Providers** (para testing y Sandbox)

```python
# src/providers/mock_provider.py

class MockLLMProvider:
    """Mock provider para testing/sandbox (determinístico)."""
    
    async def complete(self, prompt: str, **kwargs) -> str:
        # Respuestas determinísticas para testing
        if "estado de mi pedido" in prompt.lower():
            return "Tu pedido #12345 está en camino. Llegará mañana."
        elif "análisis de ventas" in prompt.lower():
            return "Las ventas aumentaron 15% este mes. Top producto: Widget Pro."
        else:
            return f"Mock response para: {prompt[:50]}..."
```

### DoD

- ✅ **DGE Integration**:
  - ✅ Contract tests con DGE service (staging o comprehensive mocks)
  - ✅ Accuracy >95% en suite de >100 samples (PII/PHI/PCI detection)
  - ✅ Cache-hit >80% para políticas (overhead p95 <20ms con cache)
  - ✅ Fail-closed Tier 3: Si DGE timeout >5s → Block (403 Forbidden)
  - ✅ mTLS+JWT s2s verificado

- ✅ **Budgets Atómicos**:
  - ✅ Redis Lua script idempotente (retries con mismo `X-Request-Id` no duplican)
  - ✅ Hard limit → Block (403); Soft limit → Allow + alert event
  - ✅ Eventos a `billing-service` (event bus)
  - ✅ Métricas: `inference_budget_checks_total`, `inference_budget_exceeded_total`

- ✅ **Audit Logs**:
  - ✅ Todos los eventos críticos auditables: `dge.classify`, `dge.block`, `budget.exceeded`
  - ✅ Audit receipts con `X-Request-Id` para correlación E2E
  - ✅ Retención delegada a `compliance-service` (10+ años)

- ✅ **Mock Providers**:
  - ✅ OpenAI/Anthropic/Groq/DGE/Voice/XR mocks disponibles
  - ✅ Respuestas determinísticas para testing
  - ✅ Sandbox env contra mocks (no external APIs)

## S8 — Seguridad s2s (mTLS + JWT + Scopes + Rotaciones E2E)

### Meta
- mTLS, JWT y scopes con rotación de certs/JWT/HMAC keys sin downtime.

### Entregables

#### **1. Gestión de Certificados mTLS**
- Certificate loading desde `/etc/inference/certs/` o Secrets Manager
- mTLS handshake con macro-módulos (ASM/CGN/AWE/SHIF)
- Certificate validation (expiry, CN, SAN)

#### **2. Emisión/Validación JWT**
- JWT s2s con RSA-256 signing
- Scopes por ruta: `macro.compose.execute`, `dge.classify.execute`, etc.
- Token expiration: 5 min (short-lived)
- Token refresh automático antes de expiry

#### **3. Rotación Sin Downtime** 🔴 CRÍTICO

```python
# src/core/rotation_manager.py

class RotationManager:
    """Manage cert/JWT/HMAC rotation sin downtime."""
    
    async def rotate_certificates(self) -> dict:
        """
        Rotate mTLS certificates sin downtime.
        
        Process:
        1. Load new cert (cert.new, key.new)
        2. Dual-serve (accept old + new certs)
        3. Wait grace period (24h)
        4. Remove old cert
        5. Promote new → current
        """
    
    async def rotate_jwt_keys(self) -> dict:
        """
        Rotate JWT signing keys sin downtime.
        
        Process:
        1. Generate new key pair (private.new, public.new)
        2. Publish public.new to JWKS endpoint
        3. Sign new tokens con private.new (kid=v2)
        4. Accept tokens signed con old + new keys
        5. Wait grace period (TTL × 2 = 10 min)
        6. Remove old key
        """
    
    async def rotate_hmac_keys(self) -> dict:
        """
        Rotate HMAC keys (resume_token) sin downtime.
        
        Process:
        1. Add new key (kid=v2)
        2. Generate new resume_tokens con kid=v2
        3. Accept resume_tokens con kid=v1 + v2
        4. Wait grace period (TTL = 5 min)
        5. Remove kid=v1
        """
```

#### **4. Scopes por Ruta**

```yaml
# config/jwt_scopes.yaml

scopes_by_route:
  "/api/v1/inference":
    required_scopes: ["inference.execute"]
  
  "/api/v1/batch/submit":
    required_scopes: ["inference.batch.submit"]
  
  # Macro-modules
  asm_service:
    required_scopes: ["macro.compose.execute", "macro.state.read"]
  
  cgn_service:
    required_scopes: ["macro.compose.execute", "macro.reason.execute"]
  
  dge_service:
    required_scopes: ["dge.classify.execute", "dge.redact.execute"]
```

#### **5. Handshake WS/SSE**

```python
# src/api/v1/endpoints/streaming_auth.py

async def validate_sse_auth(request: Request) -> dict:
    """
    Validate JWT en SSE handshake.
    
    Headers:
      - Authorization: Bearer <JWT>
      - X-Request-Id: <UUID>
    
    Returns auth context o raise 401
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(401, "Missing or invalid Authorization header")
    
    token = auth_header[7:]  # Remove "Bearer "
    
    try:
        payload = await jwt_utils.verify_token(token)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")
```

### DoD (expandido con rotaciones E2E)

- [ ] **mTLS/JWT verificados**: Contract tests con macro-módulos
- [ ] **Rotación sin downtime**: 3 tipos (certs, JWT keys, HMAC keys)
  - [ ] Certificate rotation: Dual-serve old+new, grace period 24h
  - [ ] JWT key rotation: JWKS published, grace period 10min
  - [ ] HMAC key rotation: Multi-kid support, grace period 5min
- [ ] **Tests WS/SSE completos**:
  - [ ] Token válido → 200 OK + SSE stream
  - [ ] Token inválido → 401 Unauthorized
  - [ ] Token expirado → 401 Unauthorized (con refresh hint)
  - [ ] Sin Authorization header → 401
- [ ] **Runbook de rotaciones**: Documentado en `docs/runbooks/rotation_procedures.md`
- [ ] **Scopes por ruta**: Enforcement verificado (403 si scope missing)

## S9 — Observabilidad (OTel + SIEM + WAF + DLP + KMS)

### Meta
- Observabilidad enterprise con OTel + SIEM (retención ≥7 años) + WAF de borde + DLP hooks + KMS envelope encryption, sin filtrar contenido sensible.

### Entregables

#### **1. OpenTelemetry (OTel) con Scrubber**
- Spans con metadatos no sensibles (`prompt_id`, `content_sha`, slices, provider, `ttft_ms`)
- Scrubber OTel que elimina atributos con `content*` (PII/PHI/PCI prevention)
- Sampling 100% en errores (debug purposes)
- Correlación por `X-Request-Id` propagado E2E

#### **2. SIEM Sink (retención ≥7 años)** 🔴 CRÍTICO
- **SIEM Provider**: Splunk / ELK / Datadog (configurable)
- **Sink OTel → SIEM**: Traces, logs, metrics con scrubbing aplicado
- **Retención mínima**: 7 años para compliance (GDPR/CCPA/SOX)
- **Índices separados**:
  - `inference-traces-*` (spans OTel)
  - `inference-logs-*` (application logs)
  - `inference-metrics-*` (Prometheus metrics)
  - `inference-audit-*` (security events, retención 10+ años)
- **Correlación**: Por `X-Request-Id`, `tenant_id`, `session_id`
- **Alerting**: Dashboards + alertas (p95 latency, error rate, budget exceeded)

```yaml
# config/siem.yaml

siem:
  provider: "splunk"  # splunk | elk | datadog
  endpoint: "https://siem.enis.internal:8088/services/collector"
  auth: "HEC token (via Secrets Manager)"
  
  retention_policies:
    traces: "7_years"
    logs: "7_years"
    metrics: "7_years"
    audit: "10_years"  # Compliance-grade
  
  indexes:
    traces: "inference-traces"
    logs: "inference-logs"
    metrics: "inference-metrics"
    audit: "inference-audit"
  
  scrubbing:
    enabled: true
    drop_attributes: ["content", "content_raw", "prompt_text", "response_text"]
    keep_hashes: ["content_sha256", "prompt_sha256"]
  
  sampling:
    default: 0.1  # 10% traces
    errors: 1.0   # 100% error traces
    tier_3: 0.5   # 50% Tier 3 (higher compliance)
  
  event_mapping:
    # Mapa de eventos para SIEM correlation
    inference_events:
      - "inference.request.started"      # Request initiated
      - "inference.request.completed"    # Request completed successfully
      - "inference.request.failed"       # Request failed
      - "inference.batch.submitted"      # Batch job submitted
      - "inference.batch.completed"      # Batch completed
    
    dge_events:
      - "dge.classification.performed"   # PII/PHI/PCI classification
      - "dge.block.enforced"             # Content blocked by DGE
      - "dge.redaction.applied"          # PII redacted
    
    compliance_events:
      - "compliance.audit.created"       # Audit log created
      - "compliance.dlp.violation"       # DLP violation detected
      - "compliance.budget.exceeded"     # Budget hard limit hit
    
    security_events:
      - "security.auth.failed"           # Auth failure (401)
      - "security.token.expired"         # JWT expired
      - "security.signature.invalid"     # Invalid cosign signature
      - "security.waf.blocked"           # WAF blocked request
```

#### **3. WAF Pack (HTTP/SSE/WS protection)** 🔴 CRÍTICO
- **WAF de borde**: Cloudflare / AWS WAF / NGINX ModSecurity
- **Reglas OWASP Top 10**: SQL injection, XSS, path traversal, SSRF
- **API Security**: Rate limiting, IP allowlist/blocklist, geo-blocking
- **Anti-bot**: CAPTCHA challenge, fingerprinting, behavior analysis
- **DDoS Protection**: L7 DDoS mitigation, connection limits

```yaml
# config/waf.yaml

waf:
  provider: "cloudflare"  # cloudflare | aws_waf | nginx_modsecurity
  enabled: true
  
  rules:
    owasp_top_10: true
    sql_injection: "block"
    xss: "block"
    path_traversal: "block"
    ssrf: "block"
  
  rate_limiting:
    tier_1: "100 req/min"
    tier_2: "500 req/min"
    tier_3: "2000 req/min"
    burst_multiplier: 1.5
  
  ip_filtering:
    allowlist_enabled: false
    blocklist_enabled: true
    geo_blocking: ["CN", "RU", "KP"]  # Configurable por tenant
  
  anti_bot:
    captcha_threshold: 10  # After 10 failed requests
    fingerprinting: true
    behavior_analysis: true
```

#### **4. DLP Hooks (Data Loss Prevention)** 🔴 CRÍTICO
- **Integration con DGE** (S7): DLP hooks antes de egress a LLM providers
- **Pattern matching**: PII/PHI/PCI detection antes de llamadas externas
- **Policy enforcement**: Block/Alert/Redact según tier
- **Audit trail**: Todos los DLP events → compliance-service (inmutable)

```python
# src/integrations/dlp_hooks.py

async def dlp_check_egress(
    prompt: str,
    tenant_id: str,
    tier: str,
    correlation_id: str
) -> dict:
    """
    DLP check antes de egress a LLM provider.
    
    1. Classify con DGE (PII/PHI/PCI detection)
    2. Enforce policy (block/redact/allow)
    3. Audit event si violation
    """
    # Classify
    dge_result = await dge_client.classify(
        content=prompt,
        tenant_id=tenant_id,
        tier=tier,
        correlation_id=correlation_id
    )
    
    # Enforce DLP policy
    if dge_result["policy_action"] == "block":
        # Audit DLP violation
        await event_bus.publish(
            event="compliance.dlp.violation",
            payload={
                "tenant_id": tenant_id,
                "labels": dge_result["labels"],
                "tier": tier,
                "correlation_id": correlation_id,
                "action": "blocked"
            }
        )
        raise HTTPException(451, "DLP violation - egress blocked")
    
    return dge_result
```

#### **5. KMS Envelope Encryption** 🔴 CRÍTICO
- **Enterprise Encryption Platform**: AWS KMS / GCP KMS / Azure Key Vault / HashiCorp Vault
- **Envelope encryption**: Data keys (DEK) encrypted con Master Key (KEK)
- **Rotation automática**: Key rotation sin downtime (90 días)
- **Audit receipts encrypted**: Receipts en `compliance-service` con envelope encryption
- **Certificate management**: Secrets Manager para mTLS certs

```yaml
# config/kms.yaml

kms:
  provider: "aws_kms"  # aws_kms | gcp_kms | azure_keyvault | hashicorp_vault
  enabled: true
  
  master_keys:
    audit_receipts: "arn:aws:kms:us-east-1:123456789012:key/audit-master"
    billing_data: "arn:aws:kms:us-east-1:123456789012:key/billing-master"
    certificates: "arn:aws:kms:us-east-1:123456789012:key/certs-master"
  
  rotation:
    enabled: true
    interval_days: 90
    automatic: true
  
  envelope_encryption:
    enabled: true
    dek_algorithm: "AES-256-GCM"
    kek_algorithm: "RSA-4096"
```

### DoD (expandido para SEC enterprise)

- ✅ **OTel + Scrubber**:
  - ✅ Spans sin contenido sensible (`content*` attributes dropped)
  - ✅ Sampling 100% en errores, 10% default
  - ✅ TTFT por provider visible en Grafana

- ✅ **SIEM Integration** 🔴 CRÍTICO:
  - ✅ Sink OTel → SIEM configurado y funcional
  - ✅ Retención ≥7 años para traces/logs/metrics
  - ✅ Retención ≥10 años para audit events
  - ✅ Correlación por `X-Request-Id` funcional
  - ✅ Dashboards en SIEM (latency, errors, budgets)

- ✅ **WAF Pack** 🔴 CRÍTICO:
  - ✅ WAF de borde deployado (Cloudflare/AWS WAF)
  - ✅ Reglas OWASP Top 10 activas
  - ✅ Rate limiting por tier funcional
  - ✅ Anti-bot + DDoS protection verificado
  - ✅ Geo-blocking configurable por tenant

- ✅ **DLP Hooks** 🔴 CRÍTICO:
  - ✅ Integration con DGE para PII/PHI/PCI detection
  - ✅ DLP checks antes de egress a providers
  - ✅ Policy enforcement (block/alert/redact) por tier
  - ✅ Audit trail de DLP violations (inmutable)

- ✅ **KMS Envelope Encryption** 🔴 CRÍTICO:
  - ✅ Master keys configurados (audit/billing/certs)
  - ✅ Envelope encryption funcional (DEK + KEK)
  - ✅ Key rotation automática (90 días)
  - ✅ Audit receipts encrypted at rest
  - ✅ Secrets Manager integration para mTLS certs

## S10 — Performance & Cost (Budget Guard + X-Request-Id E2E)

### Meta
- Guardas atómicas + pricing + `X-Request-Id` obligatorio E2E.

### Entregables

#### **1. X-Request-Id Obligatorio E2E** 🔴 CRÍTICO

```python
# src/middleware/request_id.py

async def enforce_request_id(request: Request, call_next):
    """
    Enforce X-Request-Id en todos los requests.
    
    - Si presente: Validar UUID format
    - Si ausente: Auto-generar UUID4
    - Propagar a logs, traces, billing events, audit logs
    """
    request_id = request.headers.get("X-Request-Id")
    
    if not request_id:
        # Auto-generate
        request_id = str(uuid.uuid4())
        logger.info(f"Auto-generated X-Request-Id: {request_id}")
    else:
        # Validate UUID format
        try:
            uuid.UUID(request_id)
        except ValueError:
            raise HTTPException(400, "Invalid X-Request-Id format (must be UUID)")
    
    # Store en request state
    request.state.request_id = request_id
    
    # Propagate a response headers
    response = await call_next(request)
    response.headers["X-Request-Id"] = request_id
    
    return response
```

**Propagación E2E**:
- FastAPI middleware → All endpoints
- Logs estructurados → Include request_id
- OTel traces → Span attribute `request.id`
- Billing events → Include `correlation_id = request_id`
- Audit logs → Include `correlation_id = request_id`
- Provider calls → Propagate en headers custom

#### **2. Pricing YAML con Checksum**

```yaml
# config/pricing.yaml
# Checksum: sha256:abc123... (CI-validated)

pricing:
  openai:
    gpt-4o-mini:
      input: 0.15  # USD per 1M tokens
      output: 0.60
    gpt-4o:
      input: 2.50
      output: 10.00
    gpt-4:
      input: 30.00
      output: 60.00
  
  anthropic:
    claude-3-haiku:
      input: 0.25
      output: 1.25
    claude-3.5-sonnet:
      input: 3.00
      output: 15.00
    claude-3-opus:
      input: 15.00
      output: 75.00
  
  groq:
    llama-3.1-70b:
      input: 0.59
      output: 0.79
    mixtral-8x7b:
      input: 0.24
      output: 0.24

checksum_validation:
  enabled: true
  algorithm: "sha256"
  ci_verify: true  # Fail CI si checksum mismatch
```

#### **3. Lua Check-and-Increment Idempotente**

```lua
-- redis_scripts/check_and_increment_budget.lua

-- Atomic budget check + increment (idempotente por X-Request-Id)

local tenant_key = KEYS[1]          -- budget:t_123:monthly
local request_id_key = KEYS[2]      -- request_dedup:req_abc
local cost_usd = tonumber(ARGV[1])
local hard_limit = tonumber(ARGV[2])
local soft_limit = tonumber(ARGV[3])
local ttl = tonumber(ARGV[4])       -- 3600s (1h dedup window)

-- Check if already processed (idempotency)
local already_charged = redis.call('EXISTS', request_id_key)
if already_charged == 1 then
  -- Ya se cobró este request_id, return sin duplicar
  local current = tonumber(redis.call('GET', tenant_key) or 0)
  return {2, current}  -- Status 2 = already charged (no-op)
end

-- Check budget
local current = tonumber(redis.call('GET', tenant_key) or 0)
local new_total = current + cost_usd

if new_total > hard_limit then
  return {-1, current}  -- Hard limit exceeded (block)
elseif new_total > soft_limit then
  -- Soft limit exceeded (allow + alert)
  redis.call('INCRBY', tenant_key, cost_usd)
  redis.call('SETEX', request_id_key, ttl, cost_usd)  -- Mark as charged
  return {1, new_total}
else
  -- OK
  redis.call('INCRBY', tenant_key, cost_usd)
  redis.call('SETEX', request_id_key, ttl, cost_usd)
  return {0, new_total}
end
```

### DoD (expandido con X-Request-Id E2E)

- [ ] **X-Request-Id obligatorio E2E**: Todos los endpoints enforce
- [ ] **Retries (N=3) no duplican coste**: Mismo `X-Request-Id` → idempotent (Lua script)
- [ ] **Pricing YAML con checksum**: CI valida checksum en cada cambio
- [ ] **Lua script atómico**: Budget check + increment en single operation
- [ ] **Propagación E2E**: request_id en logs, traces, billing, audit
- [ ] **Alertas de presupuesto**: Soft limit → event, Hard limit → block
- [ ] **Métricas**: `inference_budget_checks_total`, `inference_budget_exceeded_total`

## S10.5 — Performance Framework (Optimización Sistemática) 🟡 **RECOMENDADO**

> **Estado**: ⏸️ **PLANIFICADO**  
> **Prioridad**: 🟡 **MEDIO** (ahorro 20-40% latencia/coste)  
> **Branch**: `feat/s10.5-performance-framework`  
> **Duración**: 2 semanas

### Meta
- Framework sistemático de performance con cachés L1/L2/L3, dynamic batching, connection pooling auto-tuned, quantization (INT8/FP16), y benchmarking continuo en CI.

### Entregables

#### **1. Cachés Multi-Layer (L1/L2/L3)**

```yaml
# Estrategia de caché en 3 niveles

L1_in_memory:
  tool: "Python dict + LRU"
  ttl: "60 seconds"
  size: "1000 items"
  uso: "Hot prompts (top-10 más usados)"
  hit_ratio_target: ">90%"

L2_redis:
  tool: "Redis (ya implementado en S2.5)"
  ttl: "900 seconds (15 min)"
  size: "10,000 items"
  uso: "Warm prompts + resultados recientes"
  hit_ratio_target: ">70%"

L3_persistent:
  tool: "PostgreSQL / S3"
  ttl: "permanent (con eviction LRU)"
  size: "unlimited"
  uso: "Cold storage para analytics y replay"
  hit_ratio_target: ">50%"

cache_warming:
  - "Preload top-N prompts en startup"
  - "Predictive caching basado en patrones (ML)"
  - "Cache invalidation inteligente (no flush completo)"
```

**Implementación**:

```python
# src/core/multi_layer_cache.py

class MultiLayerCache:
    """Caché L1/L2/L3 con fallback automático."""
    
    def __init__(self):
        self.l1 = LRUCache(maxsize=1000, ttl=60)       # In-memory
        self.l2 = AsyncTTLCache(ttl_seconds=900)       # Redis (S2.5)
        self.l3 = PersistentCache(backend="postgres")  # DB
    
    async def get(self, key: str) -> Optional[Any]:
        """Get con fallback L1 → L2 → L3."""
        
        # L1 (in-memory)
        value = self.l1.get(key)
        if value is not None:
            metrics.cache_hit_total.labels(layer="L1").inc()
            return value
        
        # L2 (Redis)
        value = await self.l2.get(key)
        if value is not None:
            metrics.cache_hit_total.labels(layer="L2").inc()
            self.l1.set(key, value)  # Promote to L1
            return value
        
        # L3 (Persistent)
        value = await self.l3.get(key)
        if value is not None:
            metrics.cache_hit_total.labels(layer="L3").inc()
            await self.l2.set(key, value)  # Promote to L2
            self.l1.set(key, value)        # Promote to L1
            return value
        
        metrics.cache_miss_total.inc()
        return None
```

#### **2. Dynamic Batching**

```python
# src/engine/dynamic_batching.py

class DynamicBatcher:
    """Batch requests dinámicamente para optimizar throughput."""
    
    def __init__(
        self,
        max_batch_size: int = 32,
        max_wait_ms: int = 50
    ):
        self.max_batch_size = max_batch_size
        self.max_wait_ms = max_wait_ms
        self._queue: asyncio.Queue = asyncio.Queue()
    
    async def add_request(self, request: InferenceRequest) -> InferenceResponse:
        """Agregar request al batch."""
        future = asyncio.Future()
        await self._queue.put((request, future))
        return await future
    
    async def process_batches(self):
        """Procesar batches dinámicamente."""
        while True:
            batch = []
            deadline = time.time() + (self.max_wait_ms / 1000.0)
            
            # Collect requests hasta max_batch_size o timeout
            while len(batch) < self.max_batch_size:
                timeout = max(0, deadline - time.time())
                try:
                    request, future = await asyncio.wait_for(
                        self._queue.get(),
                        timeout=timeout
                    )
                    batch.append((request, future))
                except asyncio.TimeoutError:
                    break
            
            if batch:
                # Process batch en paralelo
                await self._process_batch(batch)
```

#### **3. Connection Pooling Auto-Tuned**

```yaml
# Auto-tuning de connection pools basado en carga

pools:
  redis:
    min_connections: 10
    max_connections: 50
    auto_tune: true
    metrics:
      - pool_utilization: "70-90% target"
      - wait_time_p95: "<5ms target"
  
  http_providers:
    openai:
      min: 5
      max: 20
      keepalive: 60
      timeout: 30
    anthropic:
      min: 5
      max: 20
    groq:
      min: 3
      max: 10

auto_tuning:
  - "Monitor pool utilization cada 60s"
  - "Scale up si utilization >90% (add 10%)"
  - "Scale down si utilization <50% (remove 10%)"
  - "Limites: min/max configurables"
```

#### **4. Quantization (INT8/FP16 para Local Models)**

```python
# src/engine/quantization.py

class QuantizedModel:
    """Wrapper para modelos locales con quantization."""
    
    async def load_quantized(
        self,
        model_path: str,
        quantization: str = "int8"  # int8 | fp16 | int4
    ) -> Model:
        """
        Load modelo con quantization.
        
        Beneficios:
        - INT8: 4x memory reduction, 2x faster inference
        - FP16: 2x memory reduction, 1.5x faster inference
        - INT4: 8x memory reduction, 3x faster inference (accuracy trade-off)
        """
        if quantization == "int8":
            model = torch.quantization.quantize_dynamic(
                model, {torch.nn.Linear}, dtype=torch.qint8
            )
        elif quantization == "fp16":
            model = model.half()
        elif quantization == "int4":
            model = load_int4_model(model_path)
        
        return model
```

#### **5. Benchmarking Continuo en CI**

```yaml
# .github/workflows/performance-benchmark.yml

name: Performance Benchmarks

on:
  pull_request:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2AM

jobs:
  benchmark:
    runs-on: ubuntu-22.04
    steps:
      - name: Run benchmarks
        run: pytest tests/performance/ --benchmark-only
      
      - name: Compare with baseline
        run: |
          python scripts/compare_benchmarks.py \
            --current results.json \
            --baseline .baseline/performance.json \
            --threshold 10  # Fail si >10% regression
      
      - name: Update baseline (if approved)
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        run: cp results.json .baseline/performance.json

thresholds:
  - prompt_resolution_p95: "<15ms"
  - inference_latency_p95: "<200ms"
  - batch_throughput: ">100 req/s"
  - cache_hit_ratio_L1: ">90%"
  - memory_footprint: "<500MB"
```

### DoD

- [ ] **Cachés L1/L2/L3**: Hit ratio >80% global
- [ ] **Dynamic batching**: Throughput +30% vs sin batching
- [ ] **Connection pooling**: Auto-tuned, p95 wait time <5ms
- [ ] **Quantization**: INT8 models 4x faster (local runtimes)
- [ ] **Benchmarks CI**: Regression detection (<10% threshold)
- [ ] **Ahorro total**: 20-40% latencia y coste verificado

## S11 — Compliance & Audit (Trazabilidad Inmutable ≥10 años)

### Meta
- Trazabilidad inmutable con audit trails ≥10 años, billing ≥7 años, export auditable y integración completa con `compliance-service`.

### Entregables

#### **1. Integración Compliance Service** (mTLS+JWT)

**Cliente Compliance**:

```python
# src/integrations/compliance_client.py

class ComplianceClient:
    """Cliente para compliance-service (audit logs inmutables)."""
    
    def __init__(self):
        self.base_url = "https://compliance-service.enis.svc.cluster.local:8443"
        self.timeout_ms = 1000
    
    async def audit_log(
        self,
        event_type: str,
        tenant_id: str,
        metadata: dict,
        correlation_id: str
    ) -> dict:
        """
        Crear audit log inmutable (retención ≥10 años).
        
        POST /api/v1/compliance/audit
        
        Returns:
            {
                "audit_id": "aud_123abc...",
                "receipt_hash": "sha256:abc...",
                "timestamp": "2025-10-10T12:00:00Z",
                "stored": true
            }
        """
        response = await self.request(
            method="POST",
            path="/api/v1/compliance/audit",
            json={
                "event_type": event_type,
                "tenant_id": tenant_id,
                "timestamp": datetime.utcnow().isoformat(),
                "metadata": metadata,
                "correlation_id": correlation_id,
                "service": "inference-service",
                "version": "1.0.0"
            },
            timeout_ms=self.timeout_ms
        )
        return response
    
    async def export_audit_trail(
        self,
        tenant_id: str,
        start_date: str,
        end_date: str,
        format: str = "jsonl.gz"
    ) -> dict:
        """
        Exportar audit trail (JSONL.gz con manifiesto y checksums).
        
        GET /api/v1/audit/export
        
        Returns:
            {
                "export_id": "exp_456def...",
                "download_url": "https://...",
                "manifest": {
                    "total_records": 1234,
                    "checksum": "sha256:...",
                    "signed": true
                },
                "expires_at": "2025-10-11T12:00:00Z"
            }
        """
        response = await self.request(
            method="GET",
            path="/api/v1/audit/export",
            params={
                "tenant_id": tenant_id,
                "start_date": start_date,
                "end_date": end_date,
                "format": format
            },
            timeout_ms=30000  # 30s para exports grandes
        )
        return response
```

#### **2. Audit Receipts con Hash Chain**

```python
# src/core/audit_receipt.py

class AuditReceipt:
    """Audit receipt inmutable con hash chain."""
    
    def __init__(
        self,
        event_type: str,
        tenant_id: str,
        metadata: dict,
        correlation_id: str
    ):
        self.event_type = event_type
        self.tenant_id = tenant_id
        self.metadata = metadata
        self.correlation_id = correlation_id
        self.timestamp = datetime.utcnow().isoformat()
    
    def compute_hash(self, previous_hash: str = "") -> str:
        """Compute hash chain (inmutable)."""
        payload = {
            "event_type": self.event_type,
            "tenant_id": self.tenant_id,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
            "correlation_id": self.correlation_id,
            "previous_hash": previous_hash
        }
        canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        return f"sha256:{hashlib.sha256(canonical.encode('utf-8')).hexdigest()}"
```

#### **3. Políticas de Retención (Enterprise-grade)**

```yaml
# config/retention_policies.yaml

retention_policies:
  audit_trails:
    retention_years: 10  # GDPR/CCPA/SOX compliance
    storage_class: "GLACIER"  # AWS S3 Glacier / GCS Archive
    immutable: true
    encryption: "KMS_ENVELOPE"  # Encrypted at rest
    
  billing_data:
    retention_years: 7  # Financial compliance (SOX/IRS)
    storage_class: "STANDARD_IA"
    immutable: true
    encryption: "KMS_ENVELOPE"
    
  operational_logs:
    retention_days: 90  # Debug/troubleshooting
    storage_class: "STANDARD"
    immutable: false
    encryption: "SSE"
    
  security_events:
    retention_years: 10  # Security compliance
    storage_class: "GLACIER"
    immutable: true
    encryption: "KMS_ENVELOPE"
    priority: "HIGH"  # Never delete, even if tenant deleted

# Por tenant (configurable)
tenant_overrides:
  tier_3:
    audit_trails: "10_years"  # Enterprise
    billing_data: "10_years"
  
  tier_2:
    audit_trails: "7_years"  # Business
    billing_data: "7_years"
  
  tier_1:
    audit_trails: "3_years"  # Starter
    billing_data: "3_years"
```

#### **4. Tamper Detection**

```python
# src/core/tamper_detection.py

async def verify_audit_chain(
    tenant_id: str,
    audit_ids: list[str]
) -> dict:
    """
    Verificar integridad de audit chain (hash chain).
    
    Returns:
        {
            "valid": bool,
            "total_records": int,
            "broken_chain": list[str],  # IDs con hash inválido
            "checksum": "sha256:..."
        }
    """
    receipts = await compliance_client.get_audit_receipts(tenant_id, audit_ids)
    
    previous_hash = ""
    broken_chain = []
    
    for receipt in receipts:
        computed_hash = receipt.compute_hash(previous_hash)
        
        if computed_hash != receipt.receipt_hash:
            broken_chain.append(receipt.audit_id)
        
        previous_hash = receipt.receipt_hash
    
    return {
        "valid": len(broken_chain) == 0,
        "total_records": len(receipts),
        "broken_chain": broken_chain,
        "checksum": previous_hash
    }
```

#### **5. Export Endpoint con Manifiesto**

```python
# src/api/v1/endpoints/audit.py

@router.get("/audit/export")
async def export_audit_trail(
    tenant_id: str,
    start_date: str,
    end_date: str,
    format: str = "jsonl.gz"
) -> dict:
    """
    Exportar audit trail (JSONL.gz con manifiesto firmado).
    
    Returns:
        {
            "export_id": "exp_123",
            "download_url": "https://s3.../audit_export_123.jsonl.gz",
            "manifest": {
                "total_records": 5678,
                "size_bytes": 1234567,
                "checksum": "sha256:...",
                "signed": true,
                "signature": "RSA-SHA256:..."
            },
            "expires_at": "2025-10-11T12:00:00Z"
        }
    """
    # Delegar a compliance-service
    export_result = await compliance_client.export_audit_trail(
        tenant_id=tenant_id,
        start_date=start_date,
        end_date=end_date,
        format=format
    )
    
    return export_result
```

### DoD (expandido para compliance enterprise)

- ✅ **Audit Receipts Inmutables**:
  - ✅ Hash chain verificable (tamper detection)
  - ✅ Timestamp firmado (no repudiable)
  - ✅ Metadata completo (event_type, tenant_id, correlation_id)
  - ✅ Encrypted at rest (KMS envelope)

- ✅ **Retenciones Enterprise-grade** 🔴 CRÍTICO:
  - ✅ **Audit trails**: ≥10 años (GDPR/CCPA/SOX compliance)
  - ✅ **Billing data**: ≥7 años (Financial compliance: SOX/IRS)
  - ✅ **Security events**: ≥10 años (Security compliance)
  - ✅ **Operational logs**: 90 días (Debug/troubleshooting)
  - ✅ Storage class: GLACIER para audit/billing (cost-optimized)
  - ✅ Immutability enforced (no delete, no modify)

- ✅ **Integration Compliance Service** 🔴 CRÍTICO:
  - ✅ `POST /api/v1/compliance/audit` (mTLS+JWT) funcional
  - ✅ `GET /api/v1/audit/export` (JSONL.gz + manifest) funcional
  - ✅ Manifest con checksums SHA256 y firma digital
  - ✅ Export con TTL (expires_at: 24h)

- ✅ **Tamper Detection**:
  - ✅ Hash chain verificable (audit_id → previous_hash)
  - ✅ Broken chain detection (alerta si hash inválido)
  - ✅ Reproducción de decisiones (audit trail completo)

- ✅ **Export Auditable**:
  - ✅ JSONL.gz con compresión (1M records ~ 100MB compressed)
  - ✅ Manifest firmado (RSA-SHA256)
  - ✅ Checksums verificables (SHA256)
  - ✅ Download URL con expiration (S3 pre-signed URL, 24h TTL)

## S11.5 — SEC Integration (Signed Execution Contract) 🔴 **CRÍTICO PARA GA ENTERPRISE**

> **Estado**: ⏸️ **PLANIFICADO**  
> **Criticidad**: 🔴 **BLOQUEANTE PARA S15 (GA)**  
> **Branch**: `feat/s11.5-sec-integration`  
> **Duración**: 3-4 semanas

### Meta
- Firma digital de imágenes y artefactos (cosign), SBOM completo (Syft), verificación en CI/CD, trail de artefactos inmutable para **GA Enterprise** (SOC2/FedRAMP/FS compliance).

### Contexto y Justificación

**Problema**: Sin SEC (Signed Execution Contract), **NO se puede certificar GA Enterprise**:
- ❌ No hay firma digital de imágenes Docker
- ❌ No existe SBOM (Software Bill of Materials) verificable
- ❌ CI no valida firmas antes de deploy
- ❌ No hay trail de artefactos para auditoría

**Impacto Compliance**:
- 🔴 **SOC2**: Requiere artifact signing + SBOM
- 🔴 **FedRAMP**: Requiere chain of custody de artefactos
- 🔴 **FS (Financial Services)**: Requiere inmutabilidad + audit trail

**Solución**: S11.5 implementa SEC completo antes de S12 (NOPS Integration).

### Entregables Detallados

#### **1. Cosign Image Signing** 🔴 CRÍTICO

```yaml
# Firma digital de imágenes Docker con cosign

workflow:
  paso_1_build:
    comando: "docker build -t enis/inference-service:v1.0.0 ."
    output: "Image SHA256: sha256:abc123..."
  
  paso_2_sign:
    tool: "cosign sign"
    comando: "cosign sign --key cosign.key enis/inference-service:v1.0.0"
    output: "Signature stored in registry (OCI artifact)"
    key_management: "KMS-backed private key (AWS KMS / GCP KMS)"
  
  paso_3_verify:
    comando: "cosign verify --key cosign.pub enis/inference-service:v1.0.0"
    output: "Verification OK - Signature valid"
    ci_gate: "❌ FAIL if unsigned or invalid signature"
```

**Integración CI/CD**:

```yaml
# .github/workflows/sign-and-verify.yml

name: Sign & Verify Images

on:
  push:
    tags: ['v*']

jobs:
  sign-image:
    runs-on: ubuntu-22.04
    steps:
      - name: Build image
        run: docker build -t $IMAGE_TAG .
      
      - name: Install cosign
        uses: sigstore/cosign-installer@v3
      
      - name: Sign image with KMS
        run: |
          cosign sign \
            --key awskms:///$KMS_KEY_ID \
            $IMAGE_TAG
      
      - name: Verify signature
        run: |
          cosign verify \
            --key awskms:///$KMS_KEY_ID \
            $IMAGE_TAG
      
      - name: Audit signature
        run: |
          python scripts/audit_signature.py \
            --image $IMAGE_TAG \
            --signature $(cosign triangulate $IMAGE_TAG)

  verify-before-deploy:
    runs-on: ubuntu-22.04
    steps:
      - name: Verify signature before deploy
        run: |
          cosign verify --key cosign.pub $IMAGE_TAG || exit 1
      
      - name: Deploy only if verified
        run: helm upgrade inference-service ./deploy/helm
```

**Config Cosign**:

```yaml
# config/cosign.yaml

cosign:
  enabled: true
  key_provider: "kms"  # kms | file | keyless
  
  kms_config:
    provider: "aws"  # aws | gcp | azure
    key_id: "arn:aws:kms:us-east-1:123456789012:key/cosign-master"
    region: "us-east-1"
  
  registry:
    url: "ghcr.io/andaon-sa-de-cv"
    username: "enis-bot"
    password_secret: "GHCR_TOKEN"
  
  verification:
    enforce_in_ci: true
    enforce_in_k8s: true  # Admission controller
    fail_on_unsigned: true
  
  audit:
    log_to_compliance: true
    retention_years: 10
```

#### **2. SBOM Generation (Syft)** 🔴 CRÍTICO

```yaml
# SBOM (Software Bill of Materials) con Syft

formats:
  - CycloneDX (JSON)  # Industry standard
  - SPDX (JSON)       # Linux Foundation standard

generation:
  tool: "syft"
  comando: "syft enis/inference-service:v1.0.0 -o cyclonedx-json > sbom.cyclonedx.json"
  scope:
    - OS packages (apt/apk)
    - Python packages (pip)
    - Application code
    - Dependencies tree

verification:
  - Validate SBOM schema (CycloneDX/SPDX)
  - Check for vulnerable packages (Grype scan)
  - Verify checksums match
  - Store in artifact registry
```

**SBOM Workflow**:

```yaml
# .github/workflows/sbom-generation.yml

name: Generate & Verify SBOM

on:
  push:
    tags: ['v*']

jobs:
  generate-sbom:
    runs-on: ubuntu-22.04
    steps:
      - name: Install Syft
        run: |
          curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin
      
      - name: Generate CycloneDX SBOM
        run: |
          syft $IMAGE_TAG -o cyclonedx-json > sbom.cyclonedx.json
      
      - name: Generate SPDX SBOM
        run: |
          syft $IMAGE_TAG -o spdx-json > sbom.spdx.json
      
      - name: Validate SBOM
        run: |
          python scripts/validate_sbom.py \
            --cyclonedx sbom.cyclonedx.json \
            --spdx sbom.spdx.json
      
      - name: Scan for vulnerabilities
        uses: anchore/scan-action@v3
        with:
          sbom: sbom.cyclonedx.json
          fail-build: true
          severity-cutoff: high
      
      - name: Sign SBOM
        run: |
          cosign sign-blob \
            --key awskms:///$KMS_KEY_ID \
            sbom.cyclonedx.json > sbom.cyclonedx.json.sig
      
      - name: Upload to artifact registry
        run: |
          cosign attach sbom \
            --sbom sbom.cyclonedx.json \
            $IMAGE_TAG
      
      - name: Audit SBOM generation
        run: |
          python scripts/audit_sbom.py \
            --image $IMAGE_TAG \
            --sbom sbom.cyclonedx.json \
            --signature sbom.cyclonedx.json.sig
```

**SBOM Schema Validation**:

```python
# scripts/validate_sbom.py

import json
from jsonschema import validate

CYCLONEDX_SCHEMA = "https://cyclonedx.org/schema/bom-1.5.schema.json"
SPDX_SCHEMA = "https://spdx.org/schema/2.3/spdx-schema.json"

def validate_sbom(sbom_path: str, format: str) -> bool:
    """Validate SBOM against schema."""
    with open(sbom_path) as f:
        sbom = json.load(f)
    
    if format == "cyclonedx":
        # Validate against CycloneDX schema
        schema = requests.get(CYCLONEDX_SCHEMA).json()
        validate(sbom, schema)
    
    elif format == "spdx":
        # Validate against SPDX schema
        schema = requests.get(SPDX_SCHEMA).json()
        validate(sbom, schema)
    
    # Check required fields
    assert "components" in sbom or "packages" in sbom
    assert "metadata" in sbom or "creationInfo" in sbom
    
    return True
```

#### **3. CI/CD Verification Gates** 🔴 CRÍTICO

```yaml
# CI gates para verificación de firma y SBOM

gates:
  pre_build:
    - "Verify base image signature (python:3.11-slim)"
    - "Scan base image for CVEs (fail on HIGH/CRITICAL)"
  
  post_build:
    - "Sign built image with cosign"
    - "Generate SBOM (CycloneDX + SPDX)"
    - "Scan SBOM for vulnerabilities (Grype)"
    - "Sign SBOM with cosign"
    - "Attach SBOM to image (OCI artifact)"
  
  pre_deploy:
    - "Verify image signature (fail if unsigned)"
    - "Verify SBOM signature"
    - "Check SBOM for critical CVEs (block deploy)"
    - "Audit artifact deployment to compliance-service"
  
  kubernetes_admission:
    - "Policy Controller verifies signature antes de pod creation"
    - "Reject unsigned images (ImagePolicyWebhook)"
```

**Admission Controller (Kubernetes)**:

```yaml
# deploy/policy/image-verification.yaml

apiVersion: policy.sigstore.dev/v1beta1
kind: ClusterImagePolicy
metadata:
  name: inference-service-signed-images
spec:
  images:
  - glob: "ghcr.io/andaon-sa-de-cv/inference-service:*"
  authorities:
  - key:
      kms: "awskms:///arn:aws:kms:us-east-1:123456789012:key/cosign-master"
  policy:
    type: "cue"
    data: |
      // Require signature + SBOM
      predicateType: "cosign.sigstore.dev/attestation/v1"
```

#### **4. Artifact Trail Inmutable** 🔴 CRÍTICO

```python
# src/core/artifact_trail.py

class ArtifactTrail:
    """Trail inmutable de artefactos firmados."""
    
    async def register_artifact(
        self,
        artifact_type: str,  # image | sbom | helm_chart | binary
        artifact_digest: str,  # sha256:...
        signature: str,
        sbom_digest: str,
        metadata: dict
    ) -> dict:
        """
        Registrar artefacto firmado en compliance trail.
        
        POST /api/v1/compliance/audit
        
        Event type: "sec.artifact.signed"
        """
        await compliance_client.audit_log(
            event_type="sec.artifact.signed",
            tenant_id="system",  # System-level event
            metadata={
                "artifact_type": artifact_type,
                "artifact_digest": artifact_digest,
                "signature": signature,
                "sbom_digest": sbom_digest,
                "signed_at": datetime.utcnow().isoformat(),
                "signer": "cosign-kms",
                "key_id": metadata.get("key_id"),
                "vulnerabilities_count": metadata.get("vuln_count", 0)
            },
            correlation_id=f"artifact_{artifact_digest[:12]}"
        )
```

#### **5. Compliance Dashboard** 🟡 ALTO

```yaml
# Panel de cumplimiento SEC

metrics:
  - sec_signed_images_total (labels: version, environment)
  - sec_unsigned_images_blocked_total
  - sec_sbom_generated_total
  - sec_vulnerabilities_found_total (labels: severity)
  - sec_signature_verification_failures_total

dashboard_widgets:
  - "% Images signed (target: 100%)"
  - "SBOM coverage (target: 100%)"
  - "Critical CVEs count (target: 0)"
  - "Signature verification rate (target: 100%)"
  - "Artifact trail completeness (target: 100%)"
```

### DoD (100% para GA Enterprise)

#### **Firma Digital** ✅
- [ ] 100% imágenes Docker firmadas con cosign
- [ ] KMS-backed private keys (no file-based)
- [ ] Signature verification en CI (fail on unsigned)
- [ ] Kubernetes admission controller rechaza unsigned
- [ ] Helm charts firmados (provenance)

#### **SBOM** ✅
- [ ] SBOM generado por release (CycloneDX + SPDX)
- [ ] SBOM attached a image (OCI artifact)
- [ ] SBOM firmado con cosign
- [ ] Vulnerability scan (Grype) con threshold HIGH
- [ ] 0 CRITICAL vulnerabilities en producción

#### **CI/CD Gates** ✅
- [ ] Pre-build: Verify base image signature
- [ ] Post-build: Sign image + Generate SBOM
- [ ] Pre-deploy: Verify signature + SBOM + CVEs
- [ ] Kubernetes: Admission controller enforcing signatures
- [ ] CI fails si imagen unsigned o CVE CRITICAL

#### **Artifact Trail** ✅
- [ ] Registro en compliance-service de cada artefacto
- [ ] Trail inmutable (hash chain)
- [ ] Metadata: digest, signature, SBOM, vulnerabilities
- [ ] Retención ≥10 años (GLACIER storage)
- [ ] Export auditable (GET /audit/export)

#### **Compliance Certification** ✅
- [ ] SOC2 Type II: Artifact signing verificado
- [ ] FedRAMP: Chain of custody completo
- [ ] FS (Financial Services): Inmutabilidad + audit trail
- [ ] Panel de cumplimiento >95% coverage
- [ ] Documentación para auditores

### Comandos Principales

```bash
# Build y sign
make build-and-sign VERSION=v1.0.0

# Generar SBOM
make sbom-generate IMAGE=enis/inference-service:v1.0.0

# Verificar firma
make verify-signature IMAGE=enis/inference-service:v1.0.0

# Scan vulnerabilities
make scan-vulnerabilities IMAGE=enis/inference-service:v1.0.0

# Full SEC pipeline
make sec-pipeline VERSION=v1.0.0
# Ejecuta: build → sign → sbom → scan → verify → audit
```

### Versiones Tecnológicas

| Componente | Versión | Justificación |
|------------|---------|---------------|
| Cosign | 2.2.0+ | Sigstore standard, KMS support |
| Syft | 0.100.0+ | SBOM generation (CycloneDX/SPDX) |
| Grype | 0.74.0+ | Vulnerability scanning |
| Policy Controller | 0.8.0+ | Kubernetes admission control |

### Archivos a Crear

```text
config/
├─ cosign.yaml              # Cosign config (KMS keys)
├─ sbom_policy.yaml         # SBOM generation policy
└─ sec_gates.yaml           # CI/CD gates config

scripts/
├─ sign_image.sh            # Firma con cosign
├─ generate_sbom.sh         # Genera CycloneDX + SPDX
├─ verify_signature.sh      # Verifica firma
├─ scan_vulnerabilities.sh  # Grype scan
├─ validate_sbom.py         # Schema validation
├─ audit_signature.py       # Audit log de firmas
└─ audit_sbom.py            # Audit log de SBOMs

src/core/
└─ artifact_trail.py        # Trail inmutable de artefactos

deploy/policy/
├─ image-verification.yaml  # Kubernetes admission policy
└─ cosign-keys.yaml         # Public keys ConfigMap

.github/workflows/
├─ sign-and-verify.yml      # Sign workflow
└─ sbom-generation.yml      # SBOM workflow

Makefile (UPDATE)           # + sec-pipeline target

tests/
├─ test_artifact_trail.py   # Trail tests
└─ test_sec_compliance.py   # SEC compliance tests
```

### Preparado para S12 (NOPS Integration)

- ✅ 100% imágenes firmadas (no unsigned en producción)
- ✅ SBOM por release (vulnerability tracking)
- ✅ CI/CD gates enforcing signatures
- ✅ Kubernetes admission controller activo
- ✅ Artifact trail completo (auditable)
- ✅ Compliance dashboard >95%
- ✅ **GATE DESBLOQUEADO PARA S15 (GA)**

### Bloqueante para S15 (GA)

> ⚠️ **CRÍTICO**: Sin S11.5 completado al 100%, **NO se puede aprobar S15 (GA)** para clientes Enterprise que requieren SOC2/FedRAMP/FS certification.

**Gate de aprobación**:
```yaml
s15_ga_gate:
  sec_compliance:
    - signed_images_percentage: ">= 100%"
    - sbom_coverage: ">= 100%"
    - critical_cves: "== 0"
    - signature_verification_rate: ">= 100%"
    - artifact_trail_completeness: ">= 100%"
  
  verdict: "APPROVE GA si todos >= targets, REJECT si alguno falla"
```

## S12 — NOPS Integration + DGE + Macro-Módulos Composition

### Meta
E2E por tipo de agente con data-minimization, egress policy (DGE), y **composición macro-módulos** (ASM/CGN/AWE/SHIF) funcional.

### Composición Macro-Módulos (referencia a S2)

> **Patrón**: Inference decide si query requiere composición (ASM/CGN/AWE/SHIF) o LLM directo. Ver **S2** para implementación completa de `MacroModulesComposer`.

**Flujo simplificado**:
1. **Classify complexity** (ML-based o rules-based)
2. **Simple query** → LLM directo (fast path, p95 < 200ms)
3. **Complex query** → Parallel calls a macro-módulos (mTLS+JWT, p95 < 400ms)
   - **ASM**: `GET /api/v1/state/get` (**timeout 200ms**) - Adaptive state/memoria
   - **CGN**: `POST /api/v1/graph/reason` (**timeout 300ms**) - Razonamiento causal
   - **AWE**: `POST /api/v1/workflow/evolve` (**timeout 250ms**) - Workflow ML
   - **SHIF**: `POST /api/v1/integrations/execute` (**timeout 500ms**) - External APIs
4. **Compose enriched prompt** con resultados
5. **LLM call** con contexto completo

**Fallback a Fast-Path** 🔴 CRÍTICO:
```python
# Si algún macro-módulo falla (timeout/error):
if module_failed:
    logger.warning(f"Module {module_name} failed, fallback to LLM directo")
    metrics.composition_fallback_total.labels(module=module_name).inc()
    # Continuar con LLM directo (degraded but functional)
    return await llm_direct(query)  # No composition
```

**Orquestación Paralela**:
```python
# src/engine/macro_composer.py

async def orchestrate_modules(query: str, context: dict) -> dict:
    """
    Orchestrate ASM/CGN/AWE/SHIF en paralelo.
    
    Timeouts estrictos:
    - ASM: 200ms (state lookup rápido)
    - CGN: 300ms (reasoning puede tardar más)
    - AWE: 250ms (workflow generation)
    - SHIF: 500ms (external APIs lentas)
    
    Fallback: Si >1 módulo falla → LLM directo
    """
    tasks = {
        "asm": self.asm_client.get_state(context, timeout_ms=200),
        "cgn": self.cgn_client.reason(query, timeout_ms=300),
        "awe": self.awe_client.evolve(query, timeout_ms=250),
        "shif": self.shif_client.execute(query, timeout_ms=500),
    }
    
    results = await asyncio.gather(*tasks.values(), return_exceptions=True)
    
    # Check failures
    failed_modules = [k for k, v in zip(tasks.keys(), results) if isinstance(v, Exception)]
    
    if len(failed_modules) > 1:
        # Too many failures → fallback
        return await self.llm_direct(query)
    
    # Continue con partial results
    return self.compose_with_results(query, results)
```

**Configuración**: Ver `config/macro_modules.yaml` en S2.

**Métricas OTel**:
- `inference_macro_composition_requests_total` (labels: modules_used, tier)
- `inference_macro_composition_latency_ms` (breakdown por module: asm_ms, cgn_ms, awe_ms, shif_ms)
- `inference_macro_composition_errors_total` (labels: module, error_type)
- `inference_macro_composition_fallback_total` (labels: reason: timeout|error|unavailable)

### Integración NOPS Modules (eventos)

**Eventos emitidos a Event Bus (Redis Streams / NATS)**:

```yaml
nops_events:
  observability:
    - event: "inference.request.started"
      payload: "{request_id, tenant_id, tier, prompt_id, timestamp}"
    - event: "inference.request.completed"
      payload: "{request_id, latency_ms, provider, model, tokens, cost_usd, composition_used}"
    - event: "inference.request.failed"
      payload: "{request_id, error_type, error_message, retry_count}"
  
  scorecard:
    - event: "scorecard.quality.check"
      payload: "{request_id, sla_met: bool, p95_ms, error_rate}"
  
  billing:
    - event: "billing.cost.incurred"
      payload: "{tenant_id, cost_usd, tokens_input, tokens_output, provider, model, timestamp}"
    - event: "billing.budget_exceeded"
      payload: "{tenant_id, limit_type: hard|soft, current_usage_usd}"
  
  sandbox:
    - event: "sandbox.mock.used"
      payload: "{request_id, mock_type: openai|anthropic|groq|dge|voice|xr}"
  
  compliance:
    - event: "compliance.audit.created"
      payload: "{event_type, tenant_id, metadata, correlation_id}"
    - event: "compliance.dge.block"
      payload: "{tenant_id, labels: [PII, EMAIL], tier, correlation_id}"
```

### Integración DGE (egress validation)

```python
# src/integrations/dge_integration.py

async def validate_egress(
    prompt: str,
    tenant_id: str,
    tier: str,
    correlation_id: str
) -> dict:
    """
    Validar egress con DGE antes de LLM call.
    
    1. POST /api/v1/dge/classify (PII/PHI/PCI detection)
    2. Enforce policy (block/redact/allow según tier)
    3. Audit event si block o redact
    """
    # Classify
    dge_result = await dge_client.classify(
        content=prompt,
        tenant_id=tenant_id,
        tier=tier,
        correlation_id=correlation_id
    )
    
    # Enforce policy
    if dge_result["policy_action"] == "block":
        # Audit event
        await event_bus.publish(
            event="compliance.dge.block",
            payload={
                "tenant_id": tenant_id,
                "labels": dge_result["labels"],
                "tier": tier,
                "correlation_id": correlation_id
            }
        )
        raise HTTPException(403, "PII/PHI/PCI detected - blocked by DGE")
    
    elif dge_result["policy_action"] == "redact":
        # Redact
        redacted = await dge_client.redact(
            content=prompt,
            labels=dge_result["labels"],
            tenant_id=tenant_id
        )
        return {"allowed": True, "content": redacted, "redacted": True}
    
    else:
        return {"allowed": True, "content": prompt, "redacted": False}
```

### E2E Test Matrix (5 tipos de agentes)

```yaml
e2e_test_matrix:
  agent_types:
    - type: "Zero Agent"
      tier: "tier_1"
      tests:
        - name: "Registration + Heartbeat"
          steps: "POST /register → GET /healthz"
          expected: "200 OK"
        - name: "Simple Inference (no composition)"
          steps: "POST /inference (query: ¿Qué hora es?)"
          expected: "p95 < 200ms, LLM directo, no ASM/CGN/AWE/SHIF"
        - name: "Budget check (soft limit)"
          steps: "Consume 90% budget → soft warning event"
          expected: "Allowed + billing.budget_warning event"
    
    - type: "Shared Agent"
      tier: "tier_2"
      tests:
        - name: "Complex Inference (composition: ASM+CGN)"
          steps: "POST /inference (query: Analiza estado ventas)"
          expected: "p95 < 400ms, composition_used: [asm, cgn]"
        - name: "DGE redaction (PII)"
          steps: "POST /inference (prompt con email)"
          expected: "Redacted → [REDACTED_EMAIL], allow"
        - name: "Billing event emitted"
          steps: "POST /inference → verify event"
          expected: "billing.cost.incurred event en bus"
    
    - type: "Lite Agent"
      tier: "tier_2"
      tests:
        - name: "Streaming SSE + resume"
          steps: "POST /inference:stream → disconnect → resume"
          expected: "Resume OK, no data loss"
    
    - type: "Enterprise Agent"
      tier: "tier_3"
      tests:
        - name: "DGE block (PII Tier 3)"
          steps: "POST /inference (prompt con SSN)"
          expected: "403 Forbidden, compliance.dge.block event"
        - name: "Full composition (ASM+CGN+AWE+SHIF)"
          steps: "POST /inference (query complejo con workflow)"
          expected: "p95 < 400ms, 4 macro-módulos usados"
        - name: "Contract tests (macro-módulos)"
          steps: "Verify ASM/CGN/AWE/SHIF mTLS+JWT"
          expected: "200 OK, schemas válidos"
    
    - type: "Air-Gapped Agent"
      tier: "tier_3"
      tests:
        - name: "Zero egress (local models)"
          steps: "POST /inference → verify no external calls"
          expected: "Local PyTorch/ONNX, no OpenAI/Anthropic"
        - name: "DGE fail-closed"
          steps: "DGE timeout → verify block"
          expected: "403 Forbidden (fail-closed)"
```

### DoD (expandido)

- ✅ **E2E Test Matrix**: Suites por 5 tipos de agente (Zero/Shared/Lite/Enterprise/Air-Gapped) verdes
- ✅ **Composición Macro-Módulos funcional**:
  - ✅ mTLS+JWT s2s verificado (ASM/CGN/AWE/SHIF)
  - ✅ Contract tests con cada macro-módulo
  - ✅ Parallel calls optimizados (2-3 módulos en < 150ms p95)
  - ✅ Fallback graceful: Si macro-módulo down → LLM directo
  - ✅ Metrics: % queries usando composition (target: 20-30% Tier 2/3)
- ✅ **Integración DGE (egress policy)**:
  - ✅ Classify + enforce antes de LLM call
  - ✅ Fail-closed Tier 3 verificado
  - ✅ Redaction funcional (PII → [REDACTED_*])
- ✅ **Eventos a NOPS Modules**:
  - ✅ Observability: request.started/completed/failed
  - ✅ Scorecard: quality.check (SLA tracking)
  - ✅ Billing: cost.incurred, budget_exceeded
  - ✅ Compliance: audit.created, dge.block
- ✅ **Cero drift de contrato**: OpenAPI schemas validados en CI

## S12.5 — Edge Agent Patterns & Best Practices 🟢 **OPCIONAL (DX)**

> **Estado**: ⏸️ **PLANIFICADO**  
> **Prioridad**: 🟢 **BAJO** (mejora DX, no bloqueante)  
> **Branch**: `feat/s12.5-edge-patterns`  
> **Duración**: 1-2 semanas

### Meta
- Documentar patrones por tipo de agente (Zero/Shared/Lite/Enterprise/Air-Gapped), cuotas por tier, distribución offline, y ejemplos SDK para mejorar developer experience.

### Entregables

#### **1. Patrones por Tipo de Agente**

```yaml
# docs/patterns/agent_types.yaml

agent_patterns:
  zero_agent:
    tier: "tier_1"
    features:
      - "Registration + Heartbeat básico"
      - "Simple inference (no composition)"
      - "Budget soft limits (warnings, no block)"
    quotas:
      requests_per_day: 1000
      max_tokens_per_request: 500
      concurrent_requests: 5
    example_use_cases:
      - "Chatbot básico"
      - "FAQ automation"
      - "Simple Q&A"
  
  shared_agent:
    tier: "tier_2"
    features:
      - "Composition básica (ASM + CGN)"
      - "DGE redaction (PII → [REDACTED])"
      - "Billing events emitted"
    quotas:
      requests_per_day: 10000
      max_tokens_per_request: 2000
      concurrent_requests: 20
      composition_enabled: ["asm", "cgn"]
    example_use_cases:
      - "Business assistant con memoria"
      - "Análisis de datos simple"
      - "Workflow automation"
  
  lite_agent:
    tier: "tier_2"
    features:
      - "Streaming SSE + resume"
      - "Offline mode (sync cuando conectado)"
      - "Local cache (edge-side)"
    quotas:
      requests_per_day: 5000
      max_tokens_per_request: 1500
      concurrent_requests: 10
      offline_cache_mb: 100
    example_use_cases:
      - "Mobile app con offline mode"
      - "Field service agent"
      - "Low-bandwidth scenarios"
  
  enterprise_agent:
    tier: "tier_3"
    features:
      - "Full composition (ASM+CGN+AWE+SHIF)"
      - "DGE fail-closed (block PII/PHI/PCI Tier 3)"
      - "Contract tests con macro-módulos"
      - "mTLS+JWT s2s verified"
    quotas:
      requests_per_day: 100000
      max_tokens_per_request: 8000
      concurrent_requests: 100
      composition_enabled: ["asm", "cgn", "awe", "shif"]
    example_use_cases:
      - "Enterprise ERP integration"
      - "Healthcare PHI processing"
      - "Financial services (FS compliance)"
  
  air_gapped_agent:
    tier: "tier_3"
    features:
      - "Zero egress (local models)"
      - "NetworkPolicy DNS-only"
      - "DGE fail-closed"
      - "Offline distribution (USB/NFS)"
    quotas:
      requests_per_day: "unlimited (local)"
      max_tokens_per_request: 4000
      concurrent_requests: 50
      egress_allowed: false
    example_use_cases:
      - "Government/Defense"
      - "Healthcare (HIPAA isolated)"
      - "Financial trading floor"
```

#### **2. Cuotas por Tier (Configurables)**

```yaml
# config/tier_quotas.yaml

tier_quotas:
  tier_1:
    name: "Starter"
    price_usd_month: 0
    requests_per_day: 1000
    max_tokens_per_request: 500
    concurrent_requests: 5
    composition_allowed: false
    dge_mode: "best_effort"
    support_sla: "community"
  
  tier_2:
    name: "Business"
    price_usd_month: 99
    requests_per_day: 10000
    max_tokens_per_request: 2000
    concurrent_requests: 20
    composition_allowed: ["asm", "cgn"]
    dge_mode: "redact"
    support_sla: "business_hours"
  
  tier_3:
    name: "Enterprise"
    price_usd_month: 999
    requests_per_day: 100000
    max_tokens_per_request: 8000
    concurrent_requests: 100
    composition_allowed: ["asm", "cgn", "awe", "shif"]
    dge_mode: "fail_closed"
    support_sla: "24x7"
    dedicated_infrastructure: true
```

#### **3. Distribución Offline (Air-Gapped)**

```bash
# scripts/offline_distribution.sh

# Preparar distribución offline para air-gapped agents

# 1. Export Docker images
docker save \
  enis/inference-service:v1.0.0 \
  enis/nops-kernel:v1.0.0 \
  redis:7.4-alpine \
  > enis-airgapped-v1.0.0.tar

# 2. Bundle Helm charts
helm package deploy/helm -d dist/helm/

# 3. Bundle models (local runtimes)
tar -czf models-llama-3.1-7b.tar.gz models/llama-3.1-7b/

# 4. Generate SBOM
syft enis-airgapped-v1.0.0.tar -o cyclonedx-json > sbom.json

# 5. Sign bundle
cosign sign-blob \
  --key cosign.key \
  enis-airgapped-v1.0.0.tar > bundle.sig

# 6. Create manifest
cat > manifest.yaml <<EOF
version: v1.0.0
release_date: $(date -I)
bundle_checksum: $(sha256sum enis-airgapped-v1.0.0.tar | cut -d' ' -f1)
signature: $(cat bundle.sig)
components:
  - inference-service:v1.0.0
  - nops-kernel:v1.0.0
  - redis:7.4-alpine
  - llama-3.1-7b
EOF
```

#### **4. Ejemplos SDK por Tipo de Agente**

```python
# examples/zero_agent.py

from enis_client import ENISClient

# Zero Agent (Tier 1) - Simple Q&A
client = ENISClient(
    base_url="https://inference.enis.local",
    api_key="enis_tier1_abc123",
    tier="tier_1"
)

response = client.inference.create({
    "prompt": "¿Qué es ENIS?",
    "model": "gpt-4o-mini",
    "max_tokens": 500
})

print(response.text)
```

```python
# examples/enterprise_agent.py

from enis_client import ENISClient

# Enterprise Agent (Tier 3) - Full Composition
client = ENISClient(
    base_url="https://inference.enis.local",
    api_key="enis_tier3_xyz789",
    tier="tier_3",
    mtls_cert_path="/etc/enis/certs/client.crt",
    mtls_key_path="/etc/enis/certs/client.key"
)

response = client.inference.create({
    "prompt": "Analiza mis ventas Q4 y genera workflow de optimización",
    "composition_strategy": "full",  # ASM+CGN+AWE+SHIF
    "max_tokens": 8000
})

print(f"Response: {response.text}")
print(f"Composition used: {response.metadata.composition_used}")
print(f"Latency breakdown: {response.metadata.latency_breakdown}")
```

#### **5. Runbooks por Escenario**

```markdown
# docs/runbooks/

- zero_agent_setup.md       # Setup Tier 1 (5 min)
- shared_agent_setup.md     # Setup Tier 2 con composition (15 min)
- lite_agent_offline.md     # Offline mode + sync (20 min)
- enterprise_agent_mtls.md  # Full setup con mTLS+JWT (30 min)
- airgapped_deployment.md   # Air-gapped distribution (45 min)
```

### DoD

- [ ] **Patrones documentados**: 5 tipos de agente (Zero/Shared/Lite/Enterprise/Air-Gapped)
- [ ] **Cuotas por tier**: Configurables en `config/tier_quotas.yaml`
- [ ] **Distribución offline**: Script funcional para air-gapped
- [ ] **Ejemplos SDK**: 5 ejemplos completos (1 por tipo)
- [ ] **Runbooks**: 5 runbooks con tiempo estimado
- [ ] **Docs DX**: README actualizado con quick starts

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

## S16 — Voice Backend Integration (ProMaster 26)

> ⚠️ **NOTA ARQUITECTÓNICA**:
> - Este sprint **integra backend** con `voice-interface-service` (repo 15).
> - **NO implementa STT/VAD/TTS/WebRTC** en este repo (eso está en `cloud-core/voice-interface-service`).
> - Inference solo provee **LLM routing** para queries de voz con contexto enriquecido.

### Meta
Integración backend con `voice-interface-service`; TTFT <300ms (porción inference), barge-in <100ms a nivel E2E (voice-svc responsable).

### Entregables

#### **1. Cliente mTLS+JWT a voice-interface-service**

```python
# src/integrations/voice_client.py

class VoiceInterfaceClient:
    """Client para Voice Interface Service (repo 15)."""
    
    def __init__(self):
        self.base_url = "https://voice-interface-service.enis.svc.cluster.local:8443"
        self.timeout_ms = 300  # TTFT target <300ms
    
    async def route_voice_query(
        self,
        query: str,
        voice_context: dict,
        tenant_id: str,
        tier: str
    ) -> dict:
        """
        Routing LLM para voice query (voice-svc llama a este endpoint).
        
        Voice-svc maneja: STT → VAD → inference (este método) → TTS → WebRTC
        """
        # Backend LLM routing (sin STT/TTS)
        response = await self.request(
            method="POST",
            path="/api/v1/voice/llm_route",
            json={
                "query": query,
                "voice_context": voice_context,
                "tenant_id": tenant_id,
                "tier": tier
            },
            timeout_ms=self.timeout_ms
        )
        return response
```

**Scopes JWT**:
```yaml
jwt_s2s:
  issuer: "inference-service"
  audience: ["voice-interface-service"]
  scopes: ["voice.query.execute", "voice.stream.consume"]
  expiration_s: 300
```

#### **2. Métricas OTel**

```yaml
metrics:
  - inference_voice_requests_total (labels: tier, model)
  - inference_voice_latency_ms (p50/p95/p99)
  - inference_voice_tokens_total (labels: tier, model)
  - inference_voice_errors_total (labels: error_type)
```

#### **3. Congelar prompts/voice.yaml**

```yaml
# src/prompts/manifests/voice.yaml

voice_core:
  template: |
    System: Responde de forma concisa y natural para voz.
    Context: {voice_context}
    User: {query}
  max_tokens: 150  # Short answers para voice
  temperature: 0.7

short_answers:
  template: |
    System: Respuesta ultra-concisa (1-2 oraciones).
    User: {query}
  max_tokens: 50
  temperature: 0.5

guardrails:
  template: |
    System: Verifica que la respuesta sea apropiada para voz (no mencionar URLs, formato texto, etc.).
    User: {query}
  
barge_in:
  template: |
    System: Respuesta interrumpible, prioriza información clave al inicio.
    User: {query}
  max_tokens: 100
```

### DoD

- ✅ **p95 backend <100ms** (sólo inference, sin STT/TTS)
- ✅ **E2E funcional con mocks**: Voice Console demo contra mocks
- ✅ **Contract tests**: Verify `/api/v1/inference/voice:query` schema
- ✅ **Prompts voice.yaml congelados**: 4 slices (voice_core, short_answers, guardrails, barge_in)
- ✅ **Demo en staging**: Voice Console con mocks STT/TTS (inference backend funcional)
- ✅ **mTLS+JWT s2s**: Verificado con voice-interface-service (staging o mocks)
- ✅ **Métricas OTel**: `inference_voice_*` métricas visibles en Grafana
- ✅ **NO implementado en este repo**: STT/VAD/TTS/WebRTC (eso está en repo 15)

---

## S17 — XR Backend Integration (ProMaster 27)

> ⚠️ **NOTA ARQUITECTÓNICA**:
> - Este sprint **integra backend** con `xr-interface-service` (repo 16).
> - **NO implementa OpenXR/Spatial/Gesture/Render** en este repo (eso está en `cloud-core/xr-interface-service`).
> - Inference solo provee **LLM routing** para queries XR con contexto multimodal (spatial/gesture/gaze).

### Meta
Integrar backend con `xr-interface-service`; fusión multimodal la hace XR-svc (OpenXR adapters, spatial mapping, gesture recognition).

### Entregables

#### **1. Cliente mTLS+JWT a xr-interface-service**

```python
# src/integrations/xr_client.py

class XRInterfaceClient:
    """Client para XR Interface Service (repo 16)."""
    
    def __init__(self):
        self.base_url = "https://xr-interface-service.enis.svc.cluster.local:8443"
        self.timeout_ms = 500  # Vision processing puede ser más lento
    
    async def route_xr_query(
        self,
        query: str,
        xr_context: dict,  # {spatial_data, gesture_detected, gaze_direction, camera_frame}
        tenant_id: str,
        tier: str
    ) -> dict:
        """
        Routing LLM para XR query (xr-svc llama a este endpoint).
        
        XR-svc maneja: OpenXR → Spatial mapping → Gesture recognition → inference (este método) → Render → Haptics
        """
        # Backend LLM routing (sin OpenXR/Spatial)
        response = await self.request(
            method="POST",
            path="/api/v1/xr/llm_route",
            json={
                "query": query,
                "xr_context": xr_context,
                "tenant_id": tenant_id,
                "tier": tier,
                "model_preference": "gpt-4o-vision"  # Vision-capable model
            },
            timeout_ms=self.timeout_ms
        )
        return response
```

**Scopes JWT**:
```yaml
jwt_s2s:
  issuer: "inference-service"
  audience: ["xr-interface-service"]
  scopes: ["xr.query.execute", "xr.stream.consume"]
  expiration_s: 300
```

#### **2. Routing a modelos vision-capable**

```python
# src/engine/xr_routing.py

async def route_xr_model(xr_context: dict) -> str:
    """
    Decidir modelo según XR context.
    
    - Si tiene camera_frame → Vision-capable (GPT-4o-vision, Claude-3.5-sonnet)
    - Si solo spatial/gesture → Text-only (GPT-4, Claude-3-opus)
    """
    if xr_context.get("camera_frame"):
        return "gpt-4o-vision"  # Vision processing
    else:
        return "gpt-4"  # Text-only (spatial/gesture sin vision)
```

#### **3. Métricas OTel**

```yaml
metrics:
  - inference_xr_requests_total (labels: tier, model, vision_processed)
  - inference_xr_latency_ms (p50/p95/p99)
  - inference_xr_spatial_context_tokens (avg tokens de spatial data)
  - inference_xr_errors_total (labels: error_type)
```

#### **4. Congelar prompts/xr.yaml**

```yaml
# src/prompts/manifests/xr.yaml

xr_spatial:
  template: |
    System: Responde considerando contexto espacial 3D.
    Spatial Data: {spatial_data}
    Gaze: {gaze_direction}
    User: {query}
  max_tokens: 200

gesture_aware:
  template: |
    System: Interpreta gestos detectados en contexto.
    Gesture: {gesture_detected}
    Pose: {hand_pose}
    User: {query}
  max_tokens: 150

avatar_mode:
  template: |
    System: Respuesta para renderizar en avatar 3D (natural, conversacional).
    Context: {xr_context}
    User: {query}
  max_tokens: 100
```

### DoD

- ✅ **p95 backend <150ms** (sólo inference, sin OpenXR/Spatial)
- ✅ **E2E XR con mocks**: XR Panel demo contra mocks (spatial/gesture simulados)
- ✅ **Contract tests**: Verify `/api/v1/inference/xr:query` schema
- ✅ **Routing vision-capable**: Si `camera_frame` presente → GPT-4o-vision
- ✅ **Prompts xr.yaml congelados**: 3 slices (xr_spatial, gesture_aware, avatar_mode)
- ✅ **Demo XR Panel**: Staging con mocks OpenXR (inference backend funcional)
- ✅ **mTLS+JWT s2s**: Verificado con xr-interface-service (staging o mocks)
- ✅ **Métricas OTel**: `inference_xr_*` métricas visibles en Grafana
- ✅ **NO implementado en este repo**: OpenXR/Spatial mapping/Gesture recognition/Render/Haptics (eso está en repo 16)

## S18  MCP Gateway (postGA, flag OFF)

### Meta
- MCP bajo feature flag con fallback a providers nativos.

### Entregables
- `integrations/mcp/` + Helm `mcp.enabled=false`.
- mTLS + JWT scopes; fallback < 300ms.

### DoD
- Con flag ON: `invoke/stream/discover` OK; métricas/trazas visibles.

## 📊 Milestones & Gates

> ⚠️ **NOTA ARQUITECTÓNICA — Alcance de S16/S17**:
> - S16 (Voice) y S17 (XR) **NO implementan** STT/VAD/TTS/OpenXR/Spatial/Gesture/Render en este repo.
> - Estos sprints solo **integran backend** con servicios independientes:
>   - Repo 15: `cloud-core/voice-interface-service` (implementa STT/VAD/TTS/WebRTC)
>   - Repo 16: `cloud-core/xr-interface-service` (implementa OpenXR/Spatial/Gesture/Render/Haptics)
> - **Inference Service (este repo)** provee únicamente **LLM routing** para queries Voice/XR.

### Milestones

- **Foundations (S0→S5 + S1.5/S2.5)**: 
  - Core: Realtime/batch/streaming, prompts, hot-reload, **composición macro-módulos** (S2)
  - Infra: Batch infrastructure (S2.5), Contract validation (S1.5 opcional)
  
- **Providers (S6a→e + S6f)**: 3+ providers (OpenAI/Anthropic/Groq), fallback, air-gapped, SDK Alpha, **backend APIs Voice/XR congeladas** (S6f)

- **Production (S7→S11 + S10.5/S11.5)**: 
  - Seguridad: DGE integration, observability (SIEM/WAF/DLP/KMS), mTLS+JWT s2s
  - Compliance: Audit logs (≥10 años), billing (≥7 años)
  - Performance: Budgets atómicos, performance framework (S10.5 opcional)
  - **SEC Integration (S11.5)**: 🔴 **BLOQUEANTE GA** - cosign, SBOM, CI gates, artifact trail

- **Integración (S12→S14 + S12.5)**: 
  - NOPS + DGE + macro-módulos composition
  - SDKs Beta, SRE/DR readiness
  - Edge patterns (S12.5 opcional)

- **GA (S15)**: 
  - **Requiere S11.5 green**: 100% images signed, SBOM coverage, 0 CRITICAL CVEs
  - Gates de seguridad/coste/fiabilidad
  - Pentest, carga final, tag v1.0.0

- **Avanzado (S16→S18)**: Voice backend integration (repo 15), XR backend integration (repo 16), MCP Gateway (post-GA)

### Gates Críticos

| Gate | Descripción | Bloqueante para | Verificación |
|------|-------------|----------------|--------------|
| **S2 DoD** | Composición macro-módulos funcional | S12 (E2E) | Contract tests ASM/CGN/AWE/SHIF |
| **S2.5 DoD** | Batch infrastructure (Redis+Celery+DLQ) | S3 (Batch Workers) | 53 tests passing, infra healthy |
| **S6f DoD** | Backend APIs Voice/XR congeladas | S16/S17 | SDK Alpha publicado, schemas congelados |
| **S7 DoD** | DGE integration (Tier 3 fail-closed) | S15 (GA) | Accuracy >95%, contract tests |
| **S11.5 DoD** 🔴 | SEC Integration (cosign+SBOM+gates) | **S15 (GA)** | **100% images signed, 0 CRITICAL CVEs** |
| **S12 DoD** | E2E matrix 5 tipos agente + composición | S15 (GA) | Suites verdes, 0 regressions |
| **S15 DoD** | All gates (SEC/SLOs/Budget/Contract) | GA Launch | P0=0, **S11.5 green**, pentest, tag v1.0.0 |

> ⚠️ **NOTA CRÍTICA**: **S11.5 es BLOQUEANTE ABSOLUTO para S15 (GA)**. Sin SEC Integration (100% images signed, SBOM coverage, 0 CRITICAL CVEs), NO se puede aprobar GA para clientes Enterprise (SOC2/FedRAMP/FS).

## 🔗 Dependencias Externas (24 Repositorios ENIS v3.0)

### Dependencias Directas (mTLS+JWT s2s)

**Outbound (Inference → otros servicios)**:
```yaml
macro_modules:
  - repo: "cloud-core/asm-service"
    protocolo: "mTLS+JWT"
    endpoints: ["GET /api/v1/state/get", "PUT /api/v1/state/update"]
    uso: "Obtener/actualizar contexto y memoria del agent para enriched prompts"
    necesario_en: "S2 (Macro-Módulos Composition)"
    criticality: "🔴 CRITICAL (composición core)"
  
  - repo: "cloud-core/cgn-service"
    protocolo: "mTLS+JWT"
    endpoints: ["POST /api/v1/graph/reason"]
    uso: "Razonamiento causal y decisiones complejas (causal chains)"
    necesario_en: "S2 (Macro-Módulos Composition)"
    criticality: "🟡 MEDIUM (value-add feature)"
  
  - repo: "cloud-core/awe-service"
    protocolo: "mTLS+JWT"
    endpoints: ["POST /api/v1/workflow/evolve"]
    uso: "Generar workflows evolutivos basados en ML"
    necesario_en: "S2 (Macro-Módulos Composition)"
    criticality: "🟡 MEDIUM (value-add feature)"
  
  - repo: "cloud-core/shif-service"
    protocolo: "mTLS+JWT"
    endpoints: ["POST /api/v1/integrations/execute"]
    uso: "Integraciones con sistemas externos (ERP/CRM/APIs)"
    necesario_en: "S2 (Macro-Módulos Composition)"
    criticality: "🟡 MEDIUM (value-add feature)"

governance:
  - repo: "cloud-core/data-governance-service"
    protocolo: "mTLS+JWT"
    endpoints: ["POST /api/v1/dge/classify", "POST /api/v1/dge/redact"]
    uso: "Clasificación PII/PHI/PCI y redacción antes de egress"
    necesario_en: "S7 (Sandbox Seguro), S12 (NOPS Integration)"
    criticality: "🔴 CRITICAL (Tier 3 compliance)"

interfaces:
  - repo: "cloud-core/voice-interface-service"
    protocolo: "mTLS+JWT (bidireccional)"
    endpoints: ["POST /api/v1/inference/voice:query", "POST /api/v1/inference/voice:stream"]
    uso: "Voice-svc consume inference backend para LLM routing (STT/VAD/TTS en voice-svc)"
    necesario_en: "S16 (Voice Backend Integration)"
    criticality: "🟡 MEDIUM (post-GA)"
  
  - repo: "cloud-core/xr-interface-service"
    protocolo: "mTLS+JWT (bidireccional)"
    endpoints: ["POST /api/v1/inference/xr:query", "POST /api/v1/inference/xr:stream"]
    uso: "XR-svc consume inference backend para LLM routing + vision models (OpenXR en xr-svc)"
    necesario_en: "S17 (XR Backend Integration)"
    criticality: "🟡 MEDIUM (post-GA)"

nops_modules:
  - repo: "cloud-core/observability-service"
    protocolo: "mTLS+JWT + Event Bus"
    eventos: ["inference.request.started", "inference.request.completed", "inference.request.failed"]
    uso: "Métricas/trazas, Prometheus/Grafana/Jaeger"
    necesario_en: "S9 (Observabilidad)"
    criticality: "🔴 CRITICAL (production ops)"
  
  - repo: "cloud-core/billing-service"
    protocolo: "Event Bus (Redis Streams / NATS)"
    eventos: ["billing.cost.incurred", "billing.budget_exceeded"]
    uso: "Cost attribution, showback, FinOps"
    necesario_en: "S10 (Performance & Cost)"
    criticality: "🔴 CRITICAL (billing)"
  
  - repo: "cloud-core/compliance-service"
    protocolo: "mTLS+JWT"
    endpoints: ["POST /api/v1/compliance/audit"]
    uso: "Audit logs inmutables (10+ años retención)"
    necesario_en: "S11 (Compliance & Audit)"
    criticality: "🔴 CRITICAL (compliance)"
  
  - repo: "cloud-core/sandbox-service"
    protocolo: "mTLS+JWT"
    uso: "Mocks (OpenAI/Anthropic/Groq/DGE/Voice/XR) para testing"
    necesario_en: "S7 (Sandbox Seguro)"
    criticality: "🟢 LOW (testing/dev)"
  
  - repo: "cloud-core/scorecard-service"
    protocolo: "Event Bus"
    eventos: ["scorecard.quality.check"]
    uso: "SLA tracking, quality metrics"
    necesario_en: "S12 (NOPS Integration)"
    criticality: "🟡 MEDIUM (quality)"
  
  - repo: "cloud-core/rgm-service"
    protocolo: "mTLS+JWT"
    uso: "Resource Governance Module (fairness/quotas decisions)"
    necesario_en: "S12 (NOPS Integration)"
    criticality: "🟡 MEDIUM (fairness)"
  
  - repo: "cloud-core/alm-service"
    protocolo: "mTLS+JWT"
    uso: "Agent Lifecycle Manager (deploy/rollback decisions)"
    necesario_en: "S12 (NOPS Integration)"
    criticality: "🟡 MEDIUM (lifecycle)"
```

**Inbound (otros servicios → Inference)**:
```yaml
edge:
  - repo: "edge/nops-kernel"
    protocolo: "mTLS+JWT (scoped)"
    endpoints: ["POST /api/v1/inference", "POST /api/v1/inference:stream"]
    uso: "Kernel enruta agent requests a inference para LLM routing"
    necesario_en: "S12 (NOPS Integration)"
    criticality: "🔴 CRITICAL (hub central edge)"
```

### Dependencias Indirectas (external APIs)

```yaml
external_providers:
  - name: "OpenAI API"
    protocolo: "HTTPS (API-Key)"
    uso: "Llamadas a GPT-4/GPT-4o/GPT-4o-mini/GPT-3.5-turbo"
    necesario_en: "S6a (OpenAI Provider)"
    criticality: "🔴 CRITICAL (core functionality)"
  
  - name: "Anthropic API"
    protocolo: "HTTPS (API-Key)"
    uso: "Llamadas a Claude-3-opus/Claude-3.5-sonnet/Claude-3-haiku"
    necesario_en: "S6b (Anthropic Provider)"
    criticality: "🔴 CRITICAL (core functionality)"
  
  - name: "Groq API"
    protocolo: "HTTPS (API-Key)"
    uso: "Llamadas a Llama-3.1-70B/Mixtral-8x7B/Gemma-7B"
    necesario_en: "S6c (Groq Provider)"
    criticality: "🟡 MEDIUM (fast inference option)"
```

### Shared Repos (contratos y SDKs)

```yaml
shared:
  - repo: "shared/agent-contracts"
    uso: "Schemas OpenAPI/Protobuf/JSON Schema para inferencias, eventos, audit"
    necesario_en: "S1 (Contracts First), S12 (NOPS Integration)"
    criticality: "🔴 CRITICAL (contract-driven development)"
```

### Critical Path (Dependencias Sprint-a-Sprint)

```yaml
critical_path:
  - "✅ S0 (Kickoff) → ✅ S1 (Contracts)"
  - "✅ S1 → [S1.5 Contract Validation 🟡 OPCIONAL] → ✅ S2 (Engine Core)"
  - "✅ S2 → 🔄 S2.5 (Batch Infrastructure Prep)"
  - "S2.5 → S3 (Engine Batch & Workers - lógica batch)"
  - "S2 → S5 (Model Management)"
  - "S5 → S6a/S6b/S6c (Providers OpenAI/Anthropic/Groq)"
  - "S6a/S6b/S6c → S6f (FE Backend Readiness - Voice/XR APIs)"
  - "S6f → S7 (Sandbox Seguro + DGE)"
  - "S7 → S8 (Seguridad s2s - completa scaffold S2.5)"
  - "S8 → S9 ∥ S10 ∥ S11 (Observability/Cost/Compliance en paralelo)"
  - "S10 → [S10.5 Performance Framework 🟡 OPCIONAL]"
  - "S11 → S11.5 (SEC Integration) 🔴 CRÍTICO PARA GA"
  - "S11.5 → S12 (NOPS Integration + DGE + Composición)"
  - "S12 → [S12.5 Edge Patterns 🟢 OPCIONAL] → S13 ∥ S14"
  - "S13 + S14 → S15 (GA Gate & Launch)"

post_ga_path:
  - "S15 → S16 (Voice Backend Integration - repo 15)"
  - "S15 → S17 (XR Backend Integration - repo 16)"
  - "S15 → S18 (MCP Gateway - post-GA)"

parallel_tracks:
  - "S3 (Batch) — depende de S2.5, puede ir en paralelo con S4/S5"
  - "S4 (Streaming) — depende de S2, puede ir en paralelo con S3/S5"
  - "S9 (Observabilidad) ∥ S10 (Cost) ∥ S11 (Compliance) después de S8"
  - "S10.5 (Performance) — opcional tras S10"
  - "S13 (SDKs) ∥ S14 (DR/SRE) después de S12"

sprint_dependencies_summary:
  foundations:
    - "✅ S0 → ✅ S1 → ✅ S2 (secuencial, completado)"
  
  validation_optional:
    - "S1 → [S1.5] → S2 (opcional, recomendado)"
  
  batch_infrastructure:
    - "S2 → 🔄 S2.5 (infraestructura, próximo) → S3 (lógica)"
  
  engine_advanced:
    - "S2 → S4 (streaming) ∥ S5 (model mgmt)"
    - "S2.5 → S3 (batch workers)"
  
  providers:
    - "S5 → S6a ∥ S6b ∥ S6c (providers en paralelo)"
    - "S6a/S6b/S6c → S6f (Voice/XR backend APIs)"
  
  security_ops:
    - "S6f → S7 (DGE integration)"
    - "S7 → S8 (mTLS+JWT - completa S2.5 scaffold)"
    - "S8 → S9 ∥ S10 ∥ S11 (en paralelo)"
  
  performance_optional:
    - "S10 → [S10.5] (opcional, 20-40% ahorro)"
  
  sec_critical:
    - "S11 → S11.5 (SEC Integration) 🔴 BLOQUEANTE GA"
  
  integration:
    - "S11.5 + S9 + S10 → S12 (NOPS Integration E2E)"
    - "S12 → [S12.5] → S13 ∥ S14 (S12.5 opcional)"
  
  ga_launch:
    - "S13 + S14 + S11.5 (green) → S15 (GA Gate)"
  
  post_ga:
    - "S15 → S16 ∥ S17 ∥ S18 (Voice/XR/MCP en paralelo)"

critical_path_visual:
  core: "✅ S0 → ✅ S1 → ✅ S2 → 🔄 S2.5 → S3 → S5 → S6 → S7 → S8 → S11.5 🔴 → S12 → S15 ✅ GA"
  optional: "[S1.5 🟡] [S10.5 🟡] [S12.5 🟢]"
  blocker_for_ga: "S11.5 (SEC) must be 100% green before S15 approval"
```

### Resumen de Dependencias (24 repos totales)

- **Edge**: 3 repos (nops-kernel, edge-agents, edge-infrastructure)
- **Cloud-core**: 15 repos (4 macro-módulos + inference + 2 interfaces + 7 NOPS modules + 1 governance)
- **Platform**: 3 repos (marketplace, studio, developer-portal)
- **Cloud-ops**: 2 repos (cloud-infrastructure, enis-infrastructure)
- **Shared**: 1 repo (agent-contracts)

**Inference Service (este repo)** interactúa directamente con **12 de los 24 repos**:
- 4 macro-módulos (ASM/CGN/AWE/SHIF) — S2
- 1 governance (DGE) — S7
- 2 interfaces (Voice/XR) — S16/S17
- 7 NOPS modules (Obs/Billing/Compliance/Sandbox/Scorecard/RGM/ALM) — S9-S12
- 1 edge (NOPS Kernel) — S12
- 1 shared (agent-contracts) — S1

## ✅ Checklist de las 8 mejoras (integradas y expandidas)

- ✅ **OpenAPI streaming + `resume_token`** (S1/S4): HMAC format `v<kid>:<offset>:<mac_b64url>`, TTL 5m, compartido con Voice/XR (S6f/S16/S17)
- ✅ **Enum de errores homogéneo** (S6): Códigos consistentes (RATE_LIMIT, TIMEOUT, CONTENT_FILTER, QUOTA_EXCEEDED, UNAVAILABLE)
- ✅ **Anti-injection + tests** (S2/S7): 10+ patrones, role isolation, meta-stripping, DLP hooks con DGE
- ✅ **`mem_guard` cgroup v2** (S5): Memory headroom 1.3x, alerta `memory_headroom_low`
- ✅ **Idempotencia de coste con `x-request-id`** (S10): Redis Lua script atómico, retries no duplican
- ✅ **Tests DNS pos/neg en airgapped** (S6e): NetworkPolicy DNS-only, CI `docker --network=none`
- ✅ **SIEM + WAF + DLP + KMS** (S9): Retención ≥7 años SIEM, ≥10 años audit; WAF OWASP Top 10; DLP hooks; KMS envelope encryption
- ✅ **Compliance retenciones** (S11): Audit trails ≥10 años, Billing ≥7 años, endpoints `POST /compliance/audit` + `GET /audit/export`
- ✅ **Auth WS/SSE documentada y testeada** (S1/S4/S8): JWT bearerAuth, mTLS s2s, resume_token HMAC

---

## 📈 **ESTADO ACTUAL DE DESARROLLO - INFERENCE SERVICE v1.0**

### **✅ COMPLETADO (S0-S2) - 10% del Total**

#### **🏗️ FUNDACIONES (S0-S2) - 100% COMPLETO** ✅

- **S0** ✅ **Kickoff & Repo Bootstrap** — **COMPLETADO 2025-10-05**
  - ✅ Estructura production-ready (31 archivos)
  - ✅ CI/CD completo (Lint → Type → Test → Helm → Build)
  - ✅ Docker multi-stage <500MB
  - ✅ Health checks (/healthz, /livez, /readyz)
  - ✅ Helm chart K8s validado
  - ✅ Tooling (ruff, mypy, pytest, pre-commit)
  - ✅ Settings con timeouts configurables
  - **Branch**: `feature/s0-kickoff-bootstrap`
  - **Informe**: docs/sprints/S0_INFORME_IMPLEMENTACION.md

- **S1** ✅ **Contracts First** — **COMPLETADO 2025-10-07**
  - ✅ OpenAPI 3.0 con 2 endpoints (sync + streaming SSE)
  - ✅ 5 tipos de eventos SSE (data, resume, heartbeat, done, error)
  - ✅ Resume tokens HMAC (v<kid>:<offset>:<mac>, TTL 5m)
  - ✅ Autenticación JWT bearerAuth documentada
  - ✅ 3 manifiestos de prompts (default, voice, xr)
  - ✅ JSON Schema + checksums SHA256 automáticos
  - ✅ CI/CD pipeline (6 validaciones automáticas)
  - ✅ Breaking changes detection
  - ✅ 6 nuevos tests (56 tests totales)
  - **Branch**: `feat/s1-contracts`
  - **PR**: #8
  - **Informe**: docs/02-sprint/S1/S1-IMPLEMENTATION-REPORT.md

- **S2** ✅ **Engine Core** — **COMPLETADO**
  - ✅ PromptResolver con AsyncTTLCache in-memory (TTL 15m)
  - ✅ Anti-injection (10+ patrones, role isolation, sanitizers)
  - ✅ RealtimeEngine (semaphore, timeout, circuit breaker)
  - ✅ BaseProvider + MockProvider para tests E2E
  - ✅ FastAPI v1 router con endpoints funcionales
  - ✅ DX tooling (Windows .ps1, pre-commit, auto-fix)
  - ✅ 60+ tests (core, engine, api, e2e)
  - **Nota**: Versión simplificada con MockProvider; infra batch en S2.5

### **🔄 PRÓXIMO SPRINT (S2.5) - LISTO PARA INICIAR**

#### **🏗️ BATCH INFRASTRUCTURE PREP (S2.5) - INMEDIATO**

> **Dependencias**: ✅ S0 + S1 + S2 completados  
> **Desbloquea**: S3 (Engine Batch & Workers)

- **S2.5** ⏸️ **Batch Infrastructure Prep** — **PLANIFICADO**
  - Redis 7.4 Alpine production setup (connection pool)
  - Celery base configuration (broker + result backend)
  - Task serialization & idempotency (Redis hash, 24h TTL)
  - DLQ setup (exponential backoff: 1s, 2s, 4s)
  - Worker monitoring & metrics (Flower + API)
  - BONUS: mTLS + JWT scaffold (para S8/S12)
  - **Duración estimada**: 3-5 días
  - **Archivos**: 32 nuevos + 5 modificados
  - **Tests**: 53 tests (85%+ coverage)
  - **Bloqueante para**: S3 (Engine Batch & Workers)
  - **Branch**: `feat/s2.5-batch-infrastructure`
  - **Documentación**: docs/02-sprint/S2.5/

### **📋 PENDIENTE (S3 en adelante) - 85% PENDIENTE**

#### **🔧 ENGINE AVANZADO (S3-S5) - PENDIENTE**
- **S3** ⏳ **Engine Batch & Workers** - Celery/Redis, DLQ, idempotencia por tenant
- **S4** ⏳ **Engine Streaming (SSE)** - SSE estable con resume HMAC y auth
- **S5** ⏳ **Model Management (Hot-Reload)** - Swap sin downtime

#### **🌐 PROVIDERS & INTEGRATIONS (S6) - PENDIENTE**
- **S6a-S6e** ⏳ **Providers** - OpenAI, Anthropic, Groq, Local Runtimes, Air-Gapped
- **S6f** ⏳ **FE Backend Readiness** - Voice/XR backend APIs congeladas, SDK Alpha

#### **🔒 SEGURIDAD Y OBSERVABILIDAD (S7-S11) - PENDIENTE**
- **S7** ⏳ **Sandbox Seguro + DGE** - Budgets, auditoría, PII delegada a DGE
- **S8** ⏳ **Seguridad s2s** - mTLS + JWT + Scopes
- **S9** ⏳ **Observabilidad** - OTel + SIEM/WAF/DLP/KMS
- **S10** ⏳ **Performance & Cost** - Budget Guard atómico
- **S11** ⏳ **Compliance & Audit** - Trazabilidad inmutable

#### **🔗 INTEGRACIÓN Y PRODUCCIÓN (S12-S15) - PENDIENTE**
- **S12** ⏳ **NOPS Integration + DGE + Composición** - E2E matrix + macro-módulos
- **S13** ⏳ **SDKs & DevPortal** - SDKs Py/TS/Go + cookbook
- **S14** ⏳ **DR & SRE Readiness** - Multi-región, DR/BC, game days
- **S15** ⏳ **GA Gate & Launch** - Pentest, carga final, release

#### **🚀 INTERFACES AVANZADAS (S16-S18) - POST-GA**
- **S16** ⏳ **Voice Backend Integration** - Integración con repo 15 (voice-interface-service)
- **S17** ⏳ **XR Backend Integration** - Integración con repo 16 (xr-interface-service)
- **S18** ⏳ **MCP Gateway** - MCP post-GA con feature flag

### **📊 MÉTRICAS DE PROGRESO**

| Categoría | Completado | En Progreso | Pendiente | Total |
|-----------|------------|-------------|-----------|-------|
| **Fundaciones (S0-S2)** | 3/3 (100%) | 0/3 (0%) | 0/3 (0%) | 3 |
| **Contract Validation (S1.5)** | 0/1 (0%) | 0/1 (0%) | 1/1 (100%) | 1 |
| **Batch Infrastructure (S2.5)** | 0/1 (0%) | 1/1 (100%) | 0/1 (0%) | 1 |
| **Engine Avanzado (S3-S5)** | 0/3 (0%) | 0/3 (0%) | 3/3 (100%) | 3 |
| **Providers (S6)** | 0/6 (0%) | 0/6 (0%) | 6/6 (100%) | 6 |
| **Seguridad & Ops (S7-S11)** | 0/5 (0%) | 0/5 (0%) | 5/5 (100%) | 5 |
| **Performance Framework (S10.5)** | 0/1 (0%) | 0/1 (0%) | 1/1 (100%) | 1 |
| **SEC Integration (S11.5)** | 0/1 (0%) | 0/1 (0%) | 1/1 (100%) | 1 |
| **Integración (S12-S14)** | 0/4 (0%) | 0/4 (0%) | 4/4 (100%) | 4 |
| **Edge Patterns (S12.5)** | 0/1 (0%) | 0/1 (0%) | 1/1 (100%) | 1 |
| **GA (S15)** | 0/1 (0%) | 0/1 (0%) | 1/1 (100%) | 1 |
| **Interfaces Avanzadas (S16-S18)** | 0/3 (0%) | 0/3 (0%) | 3/3 (100%) | 3 |
| **TOTAL** | **3/30 (10%)** | **1/30 (3%)** | **26/30 (87%)** | **30** |

### **🎯 Progreso por Fase**

| Fase | Sprints | Completados | % Completado | Estado |
|------|---------|-------------|--------------|--------|
| **Foundations** | S0-S2 | 3/3 | 100% | ✅ **COMPLETADO** |
| **Validation** | S1.5 | 0/1 | 0% | ⏸️ Opcional (recomendado) |
| **Batch Infra** | S2.5 | 0/1 | 0% | 🔄 **EN PROGRESO** (Próximo) |
| **Engine** | S3-S5 | 0/3 | 0% | ⏸️ Pendiente (S3 tras S2.5) |
| **Providers** | S6a-f | 0/6 | 0% | ⏸️ Pendiente |
| **Production** | S7-S11 | 0/5 | 0% | ⏸️ Pendiente |
| **Performance** | S10.5 | 0/1 | 0% | ⏸️ Opcional (20-40% ahorro) |
| **SEC** | S11.5 | 0/1 | 0% | ⏸️ **BLOQUEANTE PARA GA** 🔴 |
| **Integration** | S12-S14 | 0/4 | 0% | ⏸️ Pendiente |
| **Edge Patterns** | S12.5 | 0/1 | 0% | ⏸️ Opcional (DX) |
| **GA** | S15 | 0/1 | 0% | ⏸️ Pendiente (requiere S11.5) |
| **Advanced** | S16-S18 | 0/3 | 0% | ⏸️ Pendiente |
| **TOTAL** | **S0-S18 + 4 subsprints** | **3/30** | **10%** | 🟢 **Foundations 100% + S2.5 Next** |

### **🎯 PRÓXIMOS HITOS**

1. ✅ **S0 (COMPLETADO 2025-10-05)**: Repo Bootstrap
   - 31 archivos, CI/CD completo, Docker + Helm validados
   - Velocity: 5x más rápido que estimado ⚡

2. ✅ **S1 (COMPLETADO 2025-10-07)**: Contracts First
   - OpenAPI 3.0 con 2 endpoints + 5 eventos SSE
   - 3 manifiestos de prompts con checksums SHA256
   - CI/CD pipeline con 6 validaciones automáticas
   - 29 archivos, 56 tests pasando
   - **Velocity**: 100% DoD cumplido en tiempo estimado

3. ✅ **S2 (COMPLETADO)**: Engine Core
   - PromptResolver con AsyncTTLCache in-memory (TTL 15m)
   - Anti-injection (10+ patrones, role isolation, sanitizers)
   - RealtimeEngine (semaphore, timeout, circuit breaker)
   - BaseProvider + MockProvider para tests E2E
   - FastAPI v1 router + endpoints funcionales
   - DX tooling (Windows .ps1, pre-commit, auto-fix)
   - 60+ tests (core, engine, api, e2e)
   - **Nota**: Versión simplificada; infra batch en S2.5

4. **🔄 S2.5 (INMEDIATO - PRÓXIMO SPRINT)**: Batch Infrastructure Prep
   - Redis 7.4 Alpine production setup (connection pool, max 50)
   - Celery base configuration (broker + result backend)
   - Task serialization & idempotency (Redis hash, 24h TTL)
   - DLQ setup (exponential backoff: 1s, 2s, 4s)
   - Worker monitoring & metrics (Flower + API)
   - BONUS: mTLS + JWT scaffold (para S8/S12)
   - **Dependencias**: ✅ S0 + S1 + S2 completados
   - **Duración estimada**: 3-5 días
   - **Archivos**: 32 nuevos + 5 modificados
   - **Tests**: 53 tests (85%+ coverage)
   - **Bloqueante para**: S3 (Engine Batch & Workers)
   - **Documentación**: docs/02-sprint/S2.5/

5. **📅 S3-S5 (CORTO PLAZO)**: Engine Avanzado
   - S3: Batch & Workers (Celery/Redis - lógica específica)
   - S4: Streaming SSE con resume HMAC
   - S5: Model Management (hot-reload)
   - **Nota**: S3 depende de S2.5 (infraestructura lista)

6. **📅 S6 (MEDIANO PLAZO)**: Providers & Integrations
   - S6a-c: OpenAI/Anthropic/Groq
   - S6f: Backend APIs Voice/XR (congelar contratos)
   - **Bloqueante para**: S12, S16-S17

7. **📅 S7-S11 (MEDIANO PLAZO)**: Production Readiness
   - S7: DGE integration (Tier 3 fail-closed)
   - S8: mTLS+JWT s2s (completar scaffold de S2.5)
   - S9: Observability (SIEM/WAF/DLP/KMS)
   - S10-S11: Cost & Compliance

8. **📅 S12-S15 (LARGO PLAZO)**: Integration & GA
   - S12: NOPS + DGE + Macro-Módulos E2E (usa scaffold S2.5)
   - S13-S14: SDKs & DR/SRE
   - S15: GA Gate (pentest, carga final)

9. **📅 S16-S18 (POST-GA)**: Advanced Interfaces
   - S16: Voice backend integration (repo 15)
   - S17: XR backend integration (repo 16)
   - S18: MCP Gateway (feature flag)

### **⚠️ RIESGOS Y DEPENDENCIAS**

**Dependencias Críticas (Critical Path)**:
- ✅ **S0 (DONE)** → ✅ **S1 (DONE)** → ✅ **S2 (DONE)** → 🔄 **S2.5 (NEXT)** → S3 → S5 → S6 → S7 → S8 → S11.5 (SEC) → S12 → S15 (GA)

**Bloqueantes Identificados**:
- ✅ **S1 bloqueante para S2**: Engine Core necesita contratos definidos → **RESUELTO (S1 completado)**
- 🔴 **S2.5 bloqueante para S3**: S3 necesita Redis + Celery + DLQ + Idempotency
- 🔴 **S2 bloqueante para S3-S5**: PromptResolver es base para batch/streaming
- 🔴 **S2 bloqueante para S12**: Composición macro-módulos necesaria para E2E
- 🔴 **S11.5 bloqueante para S15**: SEC (cosign + SBOM) es **GATE CRÍTICO para GA Enterprise** (SOC2/FedRAMP/FS)
- 🟡 **S6f bloqueante para S16-S17**: Backend APIs Voice/XR deben estar congeladas
- 🟡 **S7 bloqueante para S15**: DGE integration es gate Tier 3

**Subsprints Opcionales (Recomendados)**:
- 🟡 **S1.5**: Contract Validation (reduce deuda técnica, headers enforcement, fuzzing, SDKs autogenerados)
- 🟡 **S10.5**: Performance Framework (ahorro 20-40% latencia/coste con cachés L1/L2/L3, batching, quantization)
- 🟢 **S12.5**: Edge Agent Patterns (mejora DX con runbooks, ejemplos, offline distribution)

**Paralelización Posible**:
- ✅ S3 (Batch) || S4 (Streaming) después de S2
- ✅ S9 (Observability) || S10 (Cost) || S11 (Compliance) después de S8
- ✅ S13 (SDKs) || S14 (DR/SRE) después de S12

### **🚀 LOGROS DESTACADOS (S0 Completado)**

- ✅ **Infraestructura sólida**: 31 archivos, CI/CD completo en 1 sesión
- ✅ **Calidad de código**: ruff + mypy + pytest + pre-commit funcionando
- ✅ **Containerización**: Docker multi-stage <500MB con healthcheck robusto
- ✅ **Kubernetes ready**: Helm chart validado (deployment/service/hpa)
- ✅ **Developer experience**: Makefile, pre-commit hooks, documentación clara
- ✅ **0 deuda técnica**: 100% DoD cumplido, sin pendientes

### **📈 VELOCIDAD DE DESARROLLO**

- **Sprints completados**: 3/30 (10%)
- **Sprints totales**: 30 (18 core + 5 subsprints + 7 provider sub-sprints)
- **Fase actual**: ✅ **Foundations COMPLETADA** (S0-S2: 100%) + 🔄 **S2.5 Próximo**
- **Tiempo acumulado**: 
  - S0: 1 semana estimada → 1 sesión ejecutada (5x más rápido) ⚡
  - S1: 1-2 semanas estimadas → 2 días ejecutados (3.5x más rápido) ⚡
  - S2: 2-3 semanas estimadas → Completado (velocity sostenida) ⚡
- **Tiempo estimado restante**: 
  - **Mínimo**: ~27 sprints (incluye S11.5 obligatorio) → ~7-8 meses para GA
  - **Recomendado**: ~30 sprints (incluye S1.5 + S10.5 + S12.5) → ~7-8 meses (opcionales en paralelo)
- **Critical path actualizado**: ✅ S0 → ✅ S1 → ✅ S2 → 🔄 S2.5 → S3 → S5 → S6 → S7 → S8 → S11.5 🔴 → S12 → S15
- **Bottlenecks identificados**: 
  - 🟡 **S2.5** (Infraestructura batch - 3-5 días, preparación para S3)
  - 🟡 **S3** (Batch logic - tras S2.5, 1-2 semanas)
  - 🟡 **S6f** (Coordinar APIs Voice/XR con repos 15/16)
  - 🟡 **S12** (E2E testing matrix 5 tipos agente + composición)
  - 🟡 **S15** (Gates pentest/carga/SEC)

### **🎊 MOMENTUM ACTUAL**

**Velocity Foundations (S0-S2)**: ⚡ **EXCEPCIONAL**

| Sprint | Estimado | Ejecutado | Eficiencia | DoD |
|--------|----------|-----------|------------|-----|
| **S0** | 1 semana | 1 sesión | 5x más rápido ⚡ | 100% |
| **S1** | 1-2 semanas | 2 días | 3.5x más rápido ⚡ | 100% |
| **S2** | 2-3 semanas | Completado | Velocity sostenida ⚡ | 100% |
| **Promedio** | - | - | **4x+ más rápido** | **100%** |

**Análisis de Momentum**:
- ✅ **Velocity sostenida**: 3 sprints foundations completados
- ✅ **Calidad consistente**: 100% DoD en los 3 sprints
- ✅ **0 deuda técnica**: Sin pendientes o retrabajos
- ✅ **Team sync**: Workflow establecido (branch → PR → review → merge)

**Proyección S2.5**:
- **Complejidad**: Media-Alta (infraestructura batch completa)
- **Estimación realista**: 3-5 días
- **Preparación**: ✅ 100% lista (S0 + S1 + S2 completados)
- **Desbloquea**: S3 (Engine Batch & Workers) para lógica pura
- **Velocity esperada**: Sostenida (3-5 días reales)
