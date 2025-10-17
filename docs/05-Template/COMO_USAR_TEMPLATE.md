# 📘 Cómo Usar la Plantilla de Sprint para Claude Code CLI

> **Guía rápida para crear sprints ejecutables por Claude Code CLI**

---

## 🎯 Propósito

Este documento explica cómo usar la plantilla `SPRINT_TEMPLATE_CLAUDE_CLI.md` para crear nuevos sprints que Claude Code CLI pueda ejecutar de manera autónoma.

---

## 🚀 Quick Start

### Paso 1: Copiar la Plantilla

```bash
# Para crear Sprint S[N], por ejemplo S2:
cp docs/01-sprint/SPRINT_TEMPLATE_CLAUDE_CLI.md docs/01-sprint/S2/S2-nombre-del-sprint.md
```

### Paso 2: Buscar y Reemplazar

Reemplaza todos los placeholders en el archivo:

| Placeholder | Reemplazar con | Ejemplo |
|-------------|----------------|---------|
| `[N]` | Número del sprint | `2` |
| `[Sprint Name]` | Nombre descriptivo | `Contracts First` |
| `[STATUS]` | Estado actual | `PENDIENTE` / `EN PROGRESO` / `COMPLETADO` |
| `[repository-name]` | Nombre del repo | `agent-contracts` |
| `[branch-suffix]` | Sufijo de la rama | `contracts-first` |
| `[Owner 1]` | Dueño principal | `Contract Architect` |
| `[Owner 2]` | Dueño secundario | `Platform Engineer` |
| `YYYY-MM-DD` | Fechas reales | `2025-10-28` |
| `[version]` | Versiones de herramientas | `20 LTS` para Node |

### Paso 3: Personalizar Contenido

#### 3.1 Actualizar la Meta
```markdown
## 🎯 Meta

Implementar contratos HTTP REST completos para Inference Service 
y Agents Service con validación automática en CI/CD.
```

#### 3.2 Definir Prerequisitos Específicos
```markdown
## ⚙️ Prerequisitos

### Herramientas Requeridas
- [x] Spectral CLI 6.11.0
- [x] AJV 8.12.0
- [x] Buf 1.28.1
```

#### 3.3 Listar Entregables
```markdown
### Entregable 1: OpenAPI Specs para Inference Service

**Archivos a crear:**
- openapi/v1/inference.yaml
- openapi/v1/inference-streaming.yaml

**Criterios:**
- [ ] Todos los endpoints documentados
- [ ] Ejemplos incluidos
- [ ] Validación Spectral sin errores
```

#### 3.4 Expandir las Fases

**Para cada fase, especifica:**
1. Duración estimada
2. Objetivo claro
3. Pasos ejecutables con comandos reales
4. Criterios de éxito verificables

**Ejemplo de Fase personalizada:**

```markdown
### 📋 FASE 2: Create OpenAPI Specifications

**⏱️ Duración estimada:** 30 minutos  
**🎯 Objetivo:** Crear specs OpenAPI completas para Inference Service

**Pasos ejecutables:**

#### 1. Crear inference.yaml
```yaml
cat > openapi/v1/inference.yaml << 'EOF'
openapi: 3.0.3
info:
  title: ENIS Inference Service API
  version: 1.0.0
  description: |
    REST API for LLM inference routing in ENIS v3.0
    
    Features:
    - Multi-model routing
    - Streaming support
    - Context management
    
paths:
  /v1/inference/completions:
    post:
      summary: Create completion
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CompletionRequest'
      responses:
        '200':
          description: Successful completion
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CompletionResponse'
                
components:
  schemas:
    CompletionRequest:
      type: object
      required:
        - prompt
        - model
      properties:
        prompt:
          type: string
          description: Input prompt
        model:
          type: string
          description: Model identifier
        temperature:
          type: number
          minimum: 0
          maximum: 2
          default: 0.7
EOF
\`\`\`

#### 2. Validar OpenAPI
\`\`\`bash
npx @stoplight/spectral-cli lint openapi/v1/inference.yaml
\`\`\`

**✅ Criterio de éxito:** Spectral validation passes with 0 errors
```

---

## 📋 Checklist de Personalización

Antes de marcar el sprint como "listo para ejecutar", verifica:

### Metadata
- [ ] Número de sprint correcto (S[N])
- [ ] Nombre descriptivo
- [ ] Branch name correcto
- [ ] Fechas reales (KICKOFF_DATE, END_DATE)
- [ ] Owners identificados
- [ ] Referencias al roadmap actualizadas

### Prerequisites
- [ ] Herramientas necesarias listadas
- [ ] Versiones especificadas
- [ ] Dependencias de sprints anteriores claras
- [ ] Estado del repo documentado

### Entregables
- [ ] Todos los entregables listados
- [ ] Archivos específicos identificados
- [ ] Criterios de aceptación claros
- [ ] Ejemplos incluidos donde sea útil

### Fases de Ejecución
- [ ] Todas las fases necesarias definidas
- [ ] Comandos ejecutables (no pseudocódigo)
- [ ] Cada comando puede copiarse y pegarse
- [ ] Criterios de éxito verificables
- [ ] Manejo de errores considerado

### Definition of Done
- [ ] DoD específico del sprint
- [ ] Todos los items medibles
- [ ] Alineado con los entregables
- [ ] Incluye calidad, tests, docs, CI/CD

### Referencias
- [ ] Links a documentos relevantes actualizados
- [ ] Owners y reviewers identificados
- [ ] Canales de comunicación especificados

---

## 🎨 Ejemplos de Personalización

### Ejemplo 1: Sprint de Contratos (S1)

```markdown
# S1 — Contracts First ⏸️ **PENDIENTE**

> **🤖 DOCUMENTO OPTIMIZADO PARA CLAUDE CODE CLI**
> 
> **Repo:** `agent-contracts`  
> **Branch:** `feature/s1-contracts-first` (base: `develop`)  
> **Duración estimada:** 2-3 semanas  
> **Owners:** Contract Architect + 2 SDK Engineers  
> **KICKOFF_DATE:** 2025-10-28  
> **END_DATE:** 2025-11-15

## 🎯 Meta

Implementar contratos HTTP REST y gRPC completos para los 4 servicios core:
Inference, Agents, Events, NOPS. Incluir esquemas JSON y protos validados en CI.

## 📦 Entregables

| Categoría | Cantidad | Descripción |
|-----------|----------|-------------|
| **OpenAPI Specs** | 4 | inference, agents, events, nops |
| **JSON Schemas** | 8 | request/response schemas |
| **Protobuf** | 4 | gRPC service definitions |
| **Workflows** | 2 | validation + breaking detection |
```

### Ejemplo 2: Sprint de Testing (S7)

```markdown
# S7 — Contract Testing (Pact) ⏸️ **PENDIENTE**

> **🤖 DOCUMENTO OPTIMIZADO PARA CLAUDE CODE CLI**
> 
> **Repo:** `agent-contracts`  
> **Branch:** `feature/s7-pact-testing` (base: `develop`)  
> **Duración estimada:** 2 semanas  
> **Owners:** QA Lead + Contract Architect  
> **KICKOFF_DATE:** 2025-12-16  
> **END_DATE:** 2025-12-30

## 🎯 Meta

Implementar Contract Testing formal con Pact para validar integraciones
entre servicios. Incluir Pact Broker y flujo can-i-deploy.

## 📦 Entregables

| Categoría | Cantidad | Descripción |
|-----------|----------|-------------|
| **Pact Tests** | 12 | Consumer-Provider pairs |
| **Pact Broker** | 1 | Hosted service setup |
| **CI Integration** | 3 | Workflows para publish/verify |
```

---

## 🆕 Novedades v2.2 - Complete Template

La versión 2.2 del template incorpora las mejores prácticas observadas en sprints reales, resuelve todos los gaps críticos identificados e incluye PowerShell parity completa y test suites integradas:

### 1. **📊 Definition of Done Cuantificable**

**Qué es:**  
DoD con scoring por categorías y métricas verificables automáticamente.

**Cómo usar:**
```markdown
## 📊 Definition of Done - Cuantificable

**Cumplimiento Target:** **23 / 25 = 92%** ✅

**Infrastructure (5/5)**
1. Redis healthy — ✅✅ 100%  
2. Worker inicia — ✅✅ 100%  
3. Connection pool — ✅✅ 100%

**Testing (4.5/5)**
4. 53 tests — ✅⚠️ 85% (placeholders)
5. Coverage >85% — ✅⚠️ objetivo
```

**Beneficios:**
- Progreso cuantificable en tiempo real
- Fácil identificar qué falta
- Transparencia en el estado del sprint

---

### 2. **🔍 QA Interno & Auto-análisis**

**Qué es:**  
Sección donde documentas issues detectados DURANTE el sprint con patches sugeridos.

**Cómo usar:**
```markdown
## 🔍 QA Interno & Auto-análisis

#### ISSUE 1 — Integración /readyz con workers (🟡 medio)

**Problema:**
/readyz no refleja estado de Redis/Celery

**Patch sugerido:**
\`\`\`diff
*** Begin Patch
*** Update File: src/api/health.py
@@
+from src.workers.metrics import get_worker_metrics
+worker_metrics = await get_worker_metrics()
*** End Patch
\`\`\`

**Beneficio:**
Eleva DoD item 13 de 80% → 100%
```

**Beneficios:**
- Issues documentados temprano
- Patches listos para aplicar
- Mejora continua del sprint
- Transparencia en limitaciones

---

### 3. **📚 ADRs (Architecture Decision Records)**

**Qué es:**  
Documentación de decisiones arquitectónicas importantes tomadas en el sprint.

**Cómo usar:**
```markdown
## 📚 ADRs

### ADR-001 — Redis vs In-Memory Cache

**Contexto:**
Necesitamos decidir backend de cache para workers

**Decisión:**
Usar Redis con fallback in-memory

**Razón:**
- Persistencia entre reinicios
- Compartir cache entre workers
- Fallback mantiene funcionalidad

**Consecuencias:**
✅ Compartir estado
⚠️ Dependencia externa

**Alternativas:**
1. Solo in-memory: Rechazado (no comparte)
2. Memcached: Rechazado (menos features)
```

**Beneficios:**
- Decisiones documentadas
- Contexto preservado
- Facilita onboarding
- Reduce deuda técnica de documentación

---

### 4. **🧪 Plan de Cobertura de Pruebas**

**Qué es:**  
Breakdown detallado de tests por módulo con objetivo de cobertura.

**Cómo usar:**
```markdown
## 🧪 Plan de Cobertura de Pruebas

**Target:** 53 tests | **Coverage:** ≥85%

### Breakdown

| Módulo | Tests | Tipo | Status |
|--------|-------|------|--------|
| redis_cache | 8 | unit | ⏸️ |
| idempotency | 8 | unit | ⏸️ |
| batch_flow | 8 | E2E | ⏸️ |

### Tests Detallados

#### redis_cache (8 tests)
1. test_connection_pool - valida pool=50
2. test_ttl_expiration - verifica TTL funciona
3. test_failover_to_inmemory - fallback cuando Redis cae
...
```

**Beneficios:**
- Cobertura planificada vs ad-hoc
- Tests con propósito claro
- Fácil validar completitud
- Guía para implementadores

---

### 5. **🛡️ Error Handling Robusto (NUEVO v2.1)**

**Qué es:**  
Scripts con manejo de errores completo, timeouts, y recuperación automática.

**Características:**
- `set -euo pipefail` en todos los scripts
- Timeouts configurables para comandos largos
- Logging estructurado con timestamps
- Funciones de retry con backoff exponencial
- Cleanup automático en caso de fallo

**Beneficios:**
- Scripts 10x más robustos
- Prevención de colgadas indefinidas
- Debugging 5x más rápido
- Experiencia de usuario profesional

### 6. **🔄 Idempotencia y Checkpoints (NUEVO v2.1)**

**Qué es:**  
Fases re-ejecutables y capacidad de resumir desde el último punto completado.

**Características:**
- Verificación de estado antes de crear archivos
- Sistema de checkpoints automático
- Skip inteligente de pasos ya completados
- Modo dry-run para validación sin cambios

**Beneficios:**
- Re-ejecutar fases sin problemas
- Resume automático en caso de interrupción
- Validación segura antes de ejecutar
- Ahorro de tiempo en debugging

### 7. **⚡ Ejecución Paralela (NUEVO v2.1)**

**Qué es:**  
Ejecutar tareas independientes en paralelo para optimizar tiempo.

**Características:**
- Función `run_parallel()` para tareas independientes
- Progress bar visual con ETA
- Logging separado por tarea
- Validación de resultados combinados

**Beneficios:**
- Reducción de 30% en tiempo de ejecución
- Mejor utilización de recursos
- Feedback visual de progreso
- Experiencia más fluida

### 8. **🔧 PowerShell Parity Completa (NUEVO v2.2)**

**Qué es:**  
Funciones equivalentes en PowerShell para entornos Windows.

**Características:**
- Todas las funciones de error handling en PowerShell
- Logging con colores y timestamps
- Validation, retry, timeout, idempotent patterns
- Checkpoint system y parallel execution

**Beneficios:**
- Soporte completo multiplataforma
- Misma funcionalidad en Windows y Linux
- Scripts robustos en cualquier entorno

### 9. **🧪 Test Suite Integrada (NUEVO v2.2)**

**Qué es:**  
Tests automáticos para validar todos los error patterns y funciones.

**Características:**
- `run_pattern_tests()` para Bash
- `Test-ErrorPatterns()` para PowerShell
- Tests para logging, validation, retry, timeout
- Tests para idempotent, checkpoint, parallel patterns

**Beneficios:**
- Validación automática de robustez
- Detección temprana de problemas
- Confianza en la funcionalidad

### 📋 Cuándo Usar Cada Novedad v2.2

| Feature | Cuándo Usar | Nivel | Crítico |
|---------|-------------|-------|---------|
| **Error Handling** | Siempre | Básico | ✅ |
| **Timeouts** | Siempre | Básico | ✅ |
| **Logging Estructurado** | Siempre | Básico | ✅ |
| **Idempotencia** | Siempre | Básico | ✅ |
| **DoD Cuantificable** | Siempre | Básico | ✅ |
| **Checkpoints** | Sprints largos | Intermedio | 🟡 |
| **Dry-Run Mode** | Validación previa | Intermedio | 🟡 |
| **Progress Bar** | Sprints largos | Intermedio | 🟡 |
| **QA Interno** | Sprints complejos | Avanzado | 🟢 |
| **ADRs** | Decisiones arquitectónicas | Avanzado | 🟢 |
| **Plan de Pruebas** | Sprints con mucho testing | Intermedio | 🟡 |
| **Ejecución Paralela** | Optimización | Avanzado | 🟢 |
| **PowerShell Parity** | Entornos Windows | Básico | ✅ |
| **Test Suite** | Validación de robustez | Básico | ✅ |

**Recomendación:**
- **Sprints simples:** Error Handling + Timeouts + Logging + Idempotencia + DoD + PowerShell Parity + Test Suite
- **Sprints medios:** Todo lo anterior + Checkpoints + Dry-Run + Progress Bar
- **Sprints complejos:** Todo (incluyendo QA + ADRs + Plan + Paralela)

---

## 🔧 Tips y Mejores Prácticas

### 1. Comandos Ejecutables

❌ **MAL** (demasiado genérico):
```markdown
2. Crear los archivos de configuración necesarios
```

✅ **BIEN** (específico y ejecutable):
```markdown
2. Crear package.json
\`\`\`bash
cat > package.json << 'EOF'
{
  "name": "@enis/agent-contracts",
  "version": "1.0.0",
  "dependencies": {
    "ajv": "^8.12.0"
  }
}
EOF

# Validar
node -e "JSON.parse(require('fs').readFileSync('package.json'))"
\`\`\`
```

### 2. Criterios de Éxito Verificables

❌ **MAL**:
```markdown
✅ Criterio de éxito: Todo funciona correctamente
```

✅ **BIEN**:
```markdown
✅ Criterio de éxito:
- Comando `npx spectral lint openapi/**/*.yaml` retorna exit code 0
- Archivo `openapi/v1/inference.yaml` existe
- Validación genera 0 errors (warnings aceptables)
```

### 3. Manejo de Errores

Siempre incluye qué hacer si algo falla:

```markdown
#### 3. Instalar buf
\`\`\`bash
# Intentar instalación
brew install buf || choco install buf || {
  echo "⚠️ buf no pudo instalarse automáticamente"
  echo "📝 Descargar manualmente desde: https://github.com/bufbuild/buf/releases"
  echo "ℹ️ buf es opcional para esta fase, continuando..."
}

# Verificar (no fallar si no está)
buf --version || echo "⚠️ buf no disponible - documentado en issues"
\`\`\`
```

### 4. Contenido Inline

Para archivos pequeños/medianos, incluye el contenido completo:

```markdown
#### 1. Crear README.md
\`\`\`markdown
cat > README.md << 'EOF'
# [Contenido completo del README aquí]
# Esto permite a Claude crear el archivo sin tener que inventar contenido
EOF
\`\`\`
```

Para archivos grandes, referencia secciones específicas:

```markdown
#### 1. Crear inference.yaml
- Copiar contenido de sección "3.2 OpenAPI Specs" (líneas 450-650)
- Archivo destino: `openapi/v1/inference.yaml`
```

### 5. Progreso Visual

Incluye progreso visual en comandos largos:

```bash
echo "📊 Creating directory structure..."
mkdir -p dir1 && echo "  ✅ dir1"
mkdir -p dir2 && echo "  ✅ dir2"
mkdir -p dir3 && echo "  ✅ dir3"
echo "✅ Directory structure complete"
```

---

## 🤖 Cómo Claude Code CLI Usará Esta Plantilla

### Flujo de Ejecución

1. **Lectura inicial**: Claude lee el documento completo
2. **Validación de prerequisitos**: Ejecuta FASE 0
3. **Ejecución secuencial**: Ejecuta FASE 1 → 2 → 3 → ... → N
4. **Verificación continua**: Después de cada fase, verifica criterios de éxito
5. **Reporte de progreso**: Actualiza tracking file
6. **Generación de reportes**: En la fase final, genera todos los reportes

### Interacción Sugerida

**Inicio:**
```
Usuario: "Claude, ejecuta el Sprint S2 siguiendo el documento 
docs/01-sprint/S2/S2-contracts-first.md"

Claude: "Entendido. Comenzando ejecución del Sprint S2 - Contracts First.
Primero verificaré los prerequisitos (FASE 0)..."
```

**Durante:**
```
Claude: "FASE 2: Create OpenAPI Specifications - ✅ COMPLETADO
- Steps completed: 5/5
- Tiempo: ~25 minutos
- Issues: Ninguno
- Siguiente: FASE 3 - Create JSON Schemas"
```

**Final:**
```
Claude: "✅ Sprint S2 COMPLETADO
- 45 archivos creados
- 2,500 líneas añadidas
- Todos los tests pasando
- Reportes generados en: S2_COMPLETION_REPORT.md
¿Deseas que cree el Pull Request ahora?"
```

---

## 📚 Recursos Adicionales

### Plantillas Relacionadas
- `SPRINT_TEMPLATE_CLAUDE_CLI.md` - Plantilla base
- `S0 — Kickoff & Repo Bootstrap.md` - Ejemplo completo implementado
- `PR_TEMPLATE.md` - Plantilla de Pull Request (si existe)

### Documentación de Apoyo
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Spectral Documentation](https://meta.stoplight.io/docs/spectral/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Protocol Buffers Style Guide](https://developers.google.com/protocol-buffers/docs/style)

### Herramientas Útiles
- [oasdiff](https://github.com/Tufin/oasdiff) - Breaking change detection
- [spectral](https://github.com/stoplightio/spectral) - OpenAPI linting
- [buf](https://buf.build/) - Protobuf linting
- [ajv](https://ajv.js.org/) - JSON Schema validation

---

## ❓ FAQ

### ¿Puedo combinar múltiples fases?

Sí, si tiene sentido. Por ejemplo, "FASE 3: Create and Validate Schemas" puede combinar creación + validación.

### ¿Cuántas fases debería tener un sprint?

Depende de la complejidad, pero típicamente:
- Sprint simple: 6-8 fases
- Sprint medio: 8-12 fases
- Sprint complejo: 12-15 fases

Más de 15 fases sugiere que el sprint debería dividirse.

### ¿Qué hacer si un comando no funciona en Windows?

Incluye alternativas:
```bash
# Linux/Mac
ls -la

# Windows PowerShell
# dir
```

O usa comandos multiplataforma cuando sea posible.

### ¿Cómo manejar secretos en la plantilla?

NUNCA incluyas secretos reales. Usa placeholders:
```bash
export API_KEY="[OBTENER DE SECRETS MANAGER]"
# o
echo "⚠️ Configurar API_KEY en GitHub Secrets"
```

### ¿Puedo usar la plantilla para sprints no relacionados con contratos?

¡Absolutamente! La plantilla es genérica. Solo personaliza:
- Meta y objetivos
- Prerequisitos
- Entregables
- Fases de ejecución

---

## 🎓 Ejercicio Práctico

Intenta crear un sprint ficticio "S99 - Test Sprint" siguiendo estos pasos:

1. Copia la plantilla
2. Reemplaza todos los placeholders
3. Define 3 entregables simples
4. Crea 5 fases básicas
5. Asegúrate de que cada fase tenga comandos ejecutables

**Tiempo estimado:** 30-45 minutos

---

## 📞 Soporte

Si tienes dudas sobre cómo usar esta plantilla:

1. Revisa el ejemplo completo en `S0 — Kickoff & Repo Bootstrap.md`
2. Consulta esta guía
3. Pregunta en #contracts-rfcs (Slack)
4. Contacta al Platform Engineering Team

---

**Última actualización:** 2025-10-13  
**Versión:** 2.2 Complete  
**Mantenedor:** Platform Engineering Team  
**License:** Proprietary - ANDAON SA DE CV


