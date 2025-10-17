# 🔍 PROMPT VERIFICADOR GENÉRICO — Todos los Sprints Agent-Contracts v3.0

> **📋 Plantilla de Verificación Técnica Post-Generación GPT-5**  
> Versión: 2.4 Enterprise Universal  
> Compatible con: Claude (Cursor AI / Claude Code CLI)  
> Proyecto: Agent-Contracts v3.0 (ENIS Compliant)

---

## 🎯 PROPÓSITO

Este prompt permite que **Claude** actúe como **revisor técnico senior** del documento de sprint generado por ChatGPT-5, verificando:

- ✅ Conformidad con plantilla v2.4
- ✅ Completitud de secciones obligatorias
- ✅ Calidad técnica del código
- ✅ Coherencia con roadmap y arquitectura Agent-Contracts
- ✅ Ejecutabilidad real de comandos
- ✅ Cobertura de DoD y SLOs
- ✅ Verificación específica por sprint

**Flujo de trabajo:**
```
GPT-5 (Genera) → Claude (Verifica) → Usuario (Aprueba) → Claude CLI (Ejecuta)
```

---

## 📄 PROMPT PARA CLAUDE (CURSOR AI / CHAT)

```markdown
---INICIO DEL PROMPT---

# VERIFICADOR DE SPRINT AGENT-CONTRACTS v3.0 — Solicitud a Claude

Eres un **Staff Platform Engineer y Technical Reviewer** experto en Agent-Contracts v3.0. Tu rol es **verificar exhaustivamente** el documento de sprint generado por ChatGPT-5 para asegurar que cumple al 100% con los estándares de calidad del proyecto.

---

## 📋 CONTEXTO

**Documento a verificar**: Sprint [NÚMERO] — [NOMBRE] [STATUS]

**Fuentes de verdad** (consultar tu base de conocimiento):
1. `agent_contracts_roadmap_2025_2026_detallado.md` — Especificación oficial del Sprint [NÚMERO]
2. `SPRINT_TEMPLATE_CLAUDE_CLI.md` — Plantilla v2.4 Enterprise Universal
3. `docs/01-sprint/S10.5/s_10_5_performance_framework_optimizacion_sistematica_v_2.md` — Sprint 10.5 (modelo de calidad v2.4)

---

## 🔍 INSTRUCCIONES DE VERIFICACIÓN

### PASO 1: Lectura y Análisis Preliminar

**Primero, lee estos archivos de tu base de conocimiento (fuentes de verdad):**

```bash
# Leer roadmap completo (sección específica del sprint)
read_file agent_contracts_roadmap_2025_2026_detallado.md

# Leer plantilla oficial v2.4 (estructura requerida)
read_file SPRINT_TEMPLATE_CLAUDE_CLI.md

# Leer S0 como referencia de calidad (benchmark)
read_file S0_kickoff_repo_bootstrap.md
```

**Luego, solicita al usuario que comparta el archivo generado:**
> "📄 Por favor, comparte el **archivo markdown completo del Sprint [NÚMERO]** generado por ChatGPT-5. Puedes:
> 
> 1. **Pegar el contenido completo** aquí en el chat, O
> 2. **Guardarlo primero** en `docs/01-sprint/S[NÚMERO]/S[NÚMERO]_[nombre].md` y yo lo leeré desde ahí
> 
> Una vez que lo tenga, lo verificaré exhaustivamente contra el roadmap, la template v2.4 y el Sprint S0."

---

### PASO 2: Verificación Estructural (Checklist de Secciones)

**Verifica que el documento incluya TODAS estas secciones obligatorias:**

#### ✅ **Auto-detección de Stack Tecnológico**
- [ ] Stack detectado automáticamente (Python/Node.js/Go/Rust/Terraform/K8s)
- [ ] Configuración por tipo de repositorio
- [ ] Comandos adaptativos según stack detectado

#### ✅ **Header y Metadata**
- [ ] Título: `# S[NÚMERO] — [Nombre] [STATUS]`
- [ ] Bloque metadata con: Version, AI Agent Role, Repo, Branch, Duración, Owners, KICKOFF_DATE, END_DATE
- [ ] Alineación con roadmap mencionada

#### ✅ **Error Handling Best Practices**
- [ ] Script header estándar (bash con `set -euo pipefail`, trap)
- [ ] Logging functions (log_info, log_warn, log_error, log_success, log_debug)
- [ ] Validation functions (check_command, check_file, check_directory)
- [ ] Error recovery patterns (retry_with_backoff, with_fallback, cleanup, timeout, idempotent, checkpoint, progress, parallel)
- [ ] PowerShell equivalents para TODOS los patterns bash
- [ ] Test suite `run_pattern_tests()` con validación completa
- [ ] Timeout presets definidos

#### ✅ **AI Agent Configuration**
- [ ] Sprint Configuration JSON completo
- [ ] Instrucciones de uso del JSON

#### ✅ **Meta y SLOs**
- [ ] Meta claramente definida
- [ ] Tabla de SLOs con métricas cuantificables
- [ ] Criterio de éxito técnico definido

#### ✅ **Ubicación de Artefactos**
- [ ] Estructura de directorios `docs/01-sprint/S[NÚMERO]/`
- [ ] Archivos generados automáticamente listados
- [ ] Convención de nombres explicada

#### ✅ **Prerequisitos**
- [ ] Herramientas requeridas (críticas)
- [ ] Herramientas recomendadas (opcionales)
- [ ] Validación automática explicada
- [ ] Dependencias de sprints anteriores
- [ ] Estado del repositorio
- [ ] Cross-Repository Dependencies con checklist

#### ✅ **Entregables**
- [ ] Resumen ejecutivo con tabla
- [ ] Cada entregable con: Descripción, Archivos, Criterios de aceptación, Ejemplos

#### ✅ **Definition of Done (DoD)**
- [ ] Cumplimiento target calculado (X/Y = Z%)
- [ ] Categorizado (Infrastructure, Core Features, Testing, Documentation, Monitoring, Security)
- [ ] Scoring guide (✅✅ 100%, ✅⚠️ 80-99%, ⚠️ 50-79%, ❌ 0-49%)
- [ ] Métricas de éxito con tabla

#### ✅ **QA Interno & Auto-análisis**
- [ ] Issues detectados con severidad (🔴🟡🟢)
- [ ] Patches sugeridos en formato diff
- [ ] Acciones para cerrar 100% del DoD

#### ✅ **ADRs (Architecture Decision Records)**
- [ ] ADR template explicado
- [ ] Mínimo 4 ADRs con: Contexto, Decisión, Razón, Consecuencias, Alternativas

#### ✅ **Plan de Cobertura de Pruebas**
- [ ] Objetivo de cobertura definido (≥85% gate)
- [ ] Breakdown por módulo con tabla
- [ ] Tests detallados por módulo
- [ ] Integration tests listados
- [ ] Test markers explicados

#### ✅ **Coverage Gate ≥85% (v2.4)**
- [ ] Gate de cobertura ≥85% en CI
- [ ] Jobs separados unit/integration
- [ ] `--cov-fail-under=85` configurado
- [ ] Redis/PostgreSQL como services en CI

#### ✅ **Rollback Robusto (v2.4)**
- [ ] Backup de configuración antes de cambios
- [ ] Pre/post health checks implementados
- [ ] Verificación de rollout con timeouts
- [ ] Restauración automática si falla
- [ ] Logging detallado del proceso

#### ✅ **AI EXECUTION PLAN — Fases Ejecutables**
- [ ] Dry-run mode explicado
- [ ] **FASE 0**: Pre-flight checks con validaciones robustas
- [ ] **FASE 1**: Branch setup con error handling
- [ ] **FASE 2-N**: Implementación de entregables específicos del sprint
- [ ] **FASE N-0.5**: Rollback plan con scripts
- [ ] **FASE N**: Final verification & reporting
- [ ] Cada fase con: Duración, Objetivo, Pasos ejecutables, Criterios de éxito

#### ✅ **Execution Summary**
- [ ] Checklist de estructura y archivos
- [ ] Validación y testing
- [ ] Documentación
- [ ] Git y PR
- [ ] Definition of Done

#### ✅ **Notas para el Agente AI**
- [ ] Ejecución (orden secuencial, verificación, manejo de errores, reportes)
- [ ] Consideraciones técnicas (paths, comandos, archivos existentes, herramientas opcionales)
- [ ] Formato de reportes (status reporting, final report requirements)
- [ ] Estilo y convenciones

#### ✅ **Contactos & Soporte (OBLIGATORIO v2.4)**
- [ ] Matriz de escalación L1-L4 completa
- [ ] SLAs específicos por nivel
- [ ] Canales de comunicación definidos
- [ ] Owners del sprint claramente identificados

#### ✅ **Secciones Finales**
- [ ] Referencias y links
- [ ] Apéndice: Comandos útiles
- [ ] Instrucción final para Claude Code CLI

---

### PASO 3: Verificación de Contenido Técnico (Calidad)

**Para cada sección verificada, evalúa:**

#### 🔬 **Código y Scripts**

**Scripts Bash:**
- [ ] ¿Usan `set -euo pipefail`?
- [ ] ¿Tienen trap para errores?
- [ ] ¿Funciones de logging están completas?
- [ ] ¿Validaciones robustas (check_command, check_file)?
- [ ] ¿Retry con backoff exponencial?
- [ ] ¿Timeouts configurados?
- [ ] ¿Operaciones idempotentes?
- [ ] ¿Sistema de checkpoints?
- [ ] ¿Tests de error patterns ejecutables?

**Scripts PowerShell:**
- [ ] ¿Equivalentes COMPLETOS de todos los patterns bash?
- [ ] ¿Funciones de logging (Write-Info, Write-Success, etc.)?
- [ ] ¿Validación (Test-Command, Test-File, Test-Directory)?
- [ ] ¿Retry con backoff (Invoke-RetryWithBackoff)?
- [ ] ¿Timeout (Invoke-WithTimeout)?
- [ ] ¿Idempotencia (New-IdempotentFile, New-IdempotentDirectory)?
- [ ] ¿Sistema de checkpoints (Save-Checkpoint, Get-Checkpoint)?
- [ ] ¿Tests PowerShell (Test-ErrorPatterns)?

#### 🏗️ **Arquitectura y Diseño**

**Código Python:**
- [ ] ¿Type hints completos?
- [ ] ¿Docstrings en todas las funciones públicas?
- [ ] ¿Error handling robusto?
- [ ] ¿Logging estructurado?
- [ ] ¿Configuración externalizada?
- [ ] ¿Tests unitarios incluidos?
- [ ] ¿Patrones de diseño apropiados?

**Configuraciones:**
- [ ] ¿YAML/JSON válidos sintácticamente?
- [ ] ¿Variables de entorno documentadas?
- [ ] ¿Valores por defecto apropiados?
- [ ] ¿Validación de configuración?

#### 📊 **Métricas y Observabilidad**

- [ ] ¿Métricas Prometheus definidas?
- [ ] ¿Logs estructurados?
- [ ] ¿Trazas OpenTelemetry?
- [ ] ¿Health checks implementados?

#### ✅ **Dashboard Grafana (CONDICIONAL v2.4)**
- [ ] Criterios de inclusión evaluados (≥2 cumplidos):
  - [ ] Métricas runtime introducidas
  - [ ] Cambios en comportamiento observable
  - [ ] Afecta SLOs del sprint
  - [ ] Requiere debug/monitoring
- [ ] Dashboard JSON provisionado si aplica

#### 🔒 **Seguridad**

- [ ] ¿Validación de entrada?
- [ ] ¿Autenticación/autorización?
- [ ] ¿Secrets management?
- [ ] ¿Rate limiting?
- [ ] ¿Cifrado en tránsito/reposo?
- [ ] ¿Audit logging?

---

### PASO 4: Métricas de Calidad v2.4

**Verifica que el sprint cumple con los siguientes targets actualizados:**

#### 📊 **Métricas Cuantitativas**
- [ ] Líneas de código: X (target: >2500)
- [ ] Cobertura de tests: X% (target: ≥85% gate)
- [ ] ADRs con métricas: X/4 (target: 4 con métricas automáticas)
- [ ] SLOs cuantificables: X/Y (target: 100%)
- [ ] Comandos adaptativos: X/Y (target: 100% según stack)

#### 🎯 **Métricas Cualitativas**
- [ ] Dashboard Grafana: ✅/❌ (target: según criterios v2.4)
- [ ] Rollback robusto: ✅/❌ (target: backup + health checks)
- [ ] Contactos obligatorios: ✅/❌ (target: matriz L1-L4 completa)
- [ ] Auto-detección stack: ✅/❌ (target: comandos adaptados)

### PASO 5: Verificación Específica por Sprint

**Verifica que el sprint cumple con los requisitos específicos del roadmap:**

#### 🎯 **Sprint S0 - Kickoff & Repo Bootstrap**
- [ ] Monorepo structure con directorios contracts/, schemas/, proto/
- [ ] GitHub Actions workflows (CI/CD, validation, security)
- [ ] Pre-commit hooks configurados
- [ ] Docker setup con multi-stage builds
- [ ] Tooling versions (Node.js, Python, Git, Docker)
- [ ] Package.json y tsconfig.json configurados

#### 🎯 **Sprint S1 - Contracts Core**
- [ ] OpenAPI 3.1 schema base
- [ ] Protocol Buffers v3 base
- [ ] JSON Schema base
- [ ] Validación cruzada entre formatos
- [ ] CI/CD pipeline para validación
- [ ] Documentación de contratos

#### 🎯 **Sprint S2 - Validation Framework**
- [ ] Framework de validación en TypeScript
- [ ] Reglas de validación configurables
- [ ] Tests unitarios y de integración
- [ ] CI/CD pipeline para validación
- [ ] Documentación del framework

#### 🎯 **Sprint S3 - Code Generation**
- [ ] Generadores de código TypeScript
- [ ] Generadores de código Python
- [ ] Generadores de código Go
- [ ] CI/CD pipeline para generación
- [ ] Documentación de generadores

#### 🎯 **Sprint S4 - Mock Services**
- [ ] Mock services en TypeScript
- [ ] Mock services en Python
- [ ] Mock services en Go
- [ ] CI/CD pipeline para mocks
- [ ] Documentación de mocks

#### 🎯 **Sprint S5 - SDK Beta**
- [ ] SDK Go implementado
- [ ] SDK Java implementado
- [ ] SDK Rust implementado
- [ ] SDK Ruby implementado
- [ ] CI/CD pipeline para SDKs
- [ ] Documentación de SDKs

#### 🎯 **Sprint S6 - Security Hardening**
- [ ] Security Controls implementados
- [ ] Compliance Framework
- [ ] Penetration Testing Framework
- [ ] Security Monitoring & Alerting
- [ ] Documentación de seguridad

#### 🎯 **Sprint S7 - Contract Testing**
- [ ] Pact Testing Framework
- [ ] Consumer-Driven Contracts
- [ ] E2E Testing Framework
- [ ] CI/CD Integration
- [ ] Documentación de testing

#### 🎯 **Sprint S8 - Performance Optimization**
- [ ] Caching Strategy
- [ ] Load Testing Framework
- [ ] Profiling & Monitoring
- [ ] Performance Optimization
- [ ] Documentación de performance

#### 🎯 **Sprint S9 - Observability**
- [ ] Metrics Implementation
- [ ] Distributed Tracing
- [ ] Structured Logging
- [ ] Alerting & Dashboards
- [ ] Documentación de observabilidad

#### 🎯 **Sprint S10 - Disaster Recovery**
- [ ] Backup System
- [ ] Restore System
- [ ] Failover System
- [ ] Monitoring & Alerting
- [ ] Documentación de DR

#### 🎯 **Sprint S11 - SDK Release**
- [ ] SDK Production Release
- [ ] Documentation Release
- [ ] Support Infrastructure
- [ ] Quality Assurance
- [ ] Documentación de release

#### 🎯 **Sprint S12 - Monitoring & Analytics**
- [ ] Metrics Collection System
- [ ] Analytics Dashboard
- [ ] Alerting System
- [ ] Analytics Engine
- [ ] Documentación de analytics

#### 🎯 **Sprint S13 - Enterprise Integration**
- [ ] SSO Integration
- [ ] LDAP Integration
- [ ] Active Directory Integration
- [ ] Integration Testing
- [ ] Documentación de integración

#### 🎯 **Sprint S14 - Compliance & Audit**
- [ ] Compliance Framework
- [ ] Audit System
- [ ] Evidence Collection
- [ ] Report Generation
- [ ] Documentación de compliance

#### 🎯 **Sprint S15 - Internationalization**
- [ ] i18n Framework
- [ ] Translation Management
- [ ] RTL Support
- [ ] Formatting System
- [ ] Documentación de i18n

#### 🎯 **Sprint S16 - Versioning**
- [ ] Version Management
- [ ] Migration System
- [ ] Compatibility Layer
- [ ] Testing Framework
- [ ] Documentación de versioning

#### 🎯 **Sprint S17 - Scalability**
- [ ] Load Balancing System
- [ ] Auto-scaling System
- [ ] Sharding System
- [ ] Monitoring & Alerting
- [ ] Documentación de scalability

#### 🎯 **Sprint S18 - Multi-Region**
- [ ] Geo-Distribution System
- [ ] Replication System
- [ ] Failover System
- [ ] Monitoring & Alerting
- [ ] Documentación de multi-region

#### 🎯 **Sprint S19 - Marketplace**
- [ ] Marketplace System
- [ ] SDK Management
- [ ] API Management
- [ ] Plugin Management
- [ ] Documentación de marketplace

---

### PASO 5: Reporte de Verificación

**Genera un reporte detallado con:**

1. **Resumen Ejecutivo**
   - Status general (✅ PASS / ⚠️ WARN / ❌ FAIL)
   - Porcentaje de cumplimiento
   - Issues críticos encontrados

2. **Checklist Detallado**
   - Secciones verificadas
   - Problemas encontrados
   - Sugerencias de mejora

3. **Recomendaciones**
   - Acciones requeridas
   - Mejoras sugeridas
   - Próximos pasos

4. **Conclusión**
   - Decisión final (APROBAR / RECHAZAR)
   - Justificación
   - Siguientes acciones

---

### PASO 6: Instrucciones para el Usuario

**Basado en la verificación, proporciona instrucciones claras:**

1. Si el sprint **PASA** la verificación:
   > "✅ El sprint cumple con todos los requisitos. Puedes proceder con la ejecución usando Claude Code CLI."

2. Si el sprint tiene **WARNINGS**:
   > "⚠️ El sprint tiene algunos issues menores que deberían corregirse. Te recomiendo:"
   > [Lista de correcciones sugeridas]

3. Si el sprint **FALLA**:
   > "❌ El sprint tiene issues críticos que deben resolverse antes de continuar:"
   > [Lista de issues críticos]
   > "Por favor, corrige estos issues y vuelve a generar el sprint con GPT-5."

---FINAL DEL PROMPT---
```
