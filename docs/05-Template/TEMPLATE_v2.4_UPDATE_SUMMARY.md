# Plantilla Sprint v2.4 Enterprise Universal - Resumen de Actualización

**Fecha:** 2025-10-16  
**Versión Anterior:** v2.2 Complete (solo inference-service)  
**Versión Nueva:** v2.4 Enterprise Universal (24 repositorios ENIS)  
**Estado:** ✅ Completado

---

## 🎯 Objetivo de la Actualización

Mejorar la plantilla de sprints ENIS con funcionalidades enterprise **y hacerla universal** para los 24 repositorios ENIS:

### Funcionalidades Enterprise:
- Trazabilidad objetiva (ADRs automáticos)
- Operabilidad real (Dashboards provisionados)
- Calidad garantizada (Coverage gates)
- Seguridad operacional (Rollback robusto)
- Escalación clara (Contactos obligatorios)

### Universalidad:
- Compatible con Python, Node.js, Next.js, Go, Rust, Terraform, Kubernetes
- Auto-detección de stack tecnológico
- Comandos adaptativos por lenguaje/framework
- Ejemplos específicos por tipo de repositorio
- Guía de SLOs por categoría de servicio

---

## ✅ Cambios Implementados

### 0. Plantilla Universal para 24 Repositorios ENIS 🆕

**Qué se agregó:**
- Sección "Configuración por Tipo de Repositorio" con auto-detección
- Tabla de comandos por stack (Python, Node.js, Next.js, Go, Rust, Terraform, Kubernetes)
- Estructura de directorios por tipo de repositorio
- Ejemplos específicos para cada stack
- Variables de entorno por tipo
- AI Agent Configuration con `repo_category` y `stack`
- Guía completa `UNIVERSAL_TEMPLATE_GUIDE.md`

**24 Repositorios Soportados:**
- **Cloud-Core (4)**: inference-service, observability-service, compliance-service, billing-service
- **Macro-Modules (4)**: asm-service, cgn-service, awe-service, shif-service
- **Shared (3)**: agent-contracts, agent-sdks, nops-sdk
- **NOPS (2)**: nops-kernel, nops-dashboard
- **Edge (2)**: edge-agents, edge-lite
- **Interfaces (2)**: voice-interface-service, xr-interface-service
- **Frontend (3)**: enis-dashboard, agent-portal, dev-portal
- **Infrastructure (2)**: k8s-manifests, terraform-modules
- **Docs (2)**: enis-docs, enis-specs

**Comandos Adaptativos:**
```bash
# Auto-detección de stack
detect_repo_type() {
  if [ -f "pyproject.toml" ]; then echo "python"
  elif [ -f "package.json" ]; then echo "nodejs"
  elif [ -f "go.mod" ]; then echo "go"
  fi
}

# Ejecutar comandos según stack detectado
REPO_TYPE=$(detect_repo_type)
case "$REPO_TYPE" in
  python) pip install -e . && pytest ;;
  nodejs) npm install && npm test ;;
  go) go test ./... ;;
esac
```

**Por qué es importante:**
- **Escalabilidad**: Un solo archivo para 24 repos en lugar de 24 plantillas
- **Consistencia**: Misma estructura en todos los repos ENIS
- **Mantenibilidad**: Actualizaciones centralizadas
- **Flexibilidad**: Adapta automáticamente comandos según stack
- **Onboarding**: Nuevos devs entienden patrón universal

**Ubicación:** Líneas 39-225 del template + `UNIVERSAL_TEMPLATE_GUIDE.md`

---

### 1. ADRs con Métricas de Validación Automáticas

**Qué se agregó:**
- Tool `tools/update_adr_metrics.py` para actualizar tablas de métricas desde `bench_out.json`
- Hook de CI para actualización automática post-benchmark
- Estructura de ADR con sección "Métricas de Validación"
- Tablas con: Métrica, Target, Actual, Estado, Baseline, Commit, Fecha

**Beneficio:**
- Elimina drift manual entre métricas y documentación
- Trazabilidad automática de mejoras de performance
- Evidencia objetiva para decisiones arquitectónicas

**Ubicación:** Líneas 1191-1356 del template

---

### 2. Dashboard Grafana Provisionado (**CONDICIONAL**)

**Qué se agregó:**
- JSON completo de dashboard con 6 paneles:
  - Request Latency p95
  - L1/L2/L3 Cache Hit Ratios (gauges)
  - Request Rate (RPS)
  - DB Pool Utilization
  - Cache Hit Ratios by Tenant (tabla audit)
- Variables de templating (tenant, tier)
- Thresholds configurados por panel
- Annotations para deploys
- ConfigMap de Kubernetes para provisioning
- Queries PromQL listas para copiar/pegar
- **🆕 Guía clara de cuándo incluir dashboards**

**¿Cuándo incluir Dashboard Grafana?**
Solo si el sprint cumple **≥2 criterios**:
- ✅ Introduce métricas runtime (latencia, throughput, concurrencia)
- ✅ Cambia comportamiento observable (streaming, batch, async)
- ✅ Afecta SLOs (p95, error rate, availability)
- ✅ Requiere debug operacional (logs no bastan)

**Sprints que SÍ:** S2, S3, S4, S5, S6, S9, S10+  
**Sprints que NO:** S0, S1, S7, S8

**Beneficio:**
- Dashboards listos post-deploy sin configuración manual
- Visibilidad multi-tenant desde día 1
- Thresholds alineados a SLOs
- **Evita bloat**: Solo dashboards necesarios

**Ubicación:** Líneas 1497-1712 del template

---

### 3. Coverage Gate ≥85%

**Qué se agregó:**
- Tests con coverage en Bash (Node.js, Python, Go)
- GitHub Actions workflow completo:
  - Servicios Redis y PostgreSQL para integration tests
  - Jobs separados unit/integration
  - Flag `--cov-fail-under=85`
  - Upload a Codecov
  - Comentario automático en PR con resultado
- Configuración pytest.ini con markers
- Configuración .coveragerc con exclusiones

**Beneficio:**
- Calidad garantizada en CI/CD
- Evidencia trazable de cobertura
- No más debates sobre "suficiente coverage"

**Ubicación:** Líneas 2284-2518 del template

---

### 4. DoD Cuantificable Mejorado

**Qué se agregó:**
- Matriz de cumplimiento con columnas:
  - ID, Categoría, Criterio, Target, Actual, Score, Estado, Bloqueante
- 7 categorías (Infraestructura, Core Features, Testing, Observabilidad, Seguridad, Documentación, Rollback)
- Scoring guide con estados ✅⚠️❌
- Criticidad por ítem (🔴🟡🟢)
- Criterio de aprobación explícito:
  - ≥85% + todos 🔴 → APROBADO
  - ≥75% → CONDICIONAL
  - <75% → RECHAZADO
- Script `tools/verify_dod.py` para verificación automática

**Beneficio:**
- Objetividad total en evaluación de sprints
- Criterios claros de aprobación/rechazo
- Automatización de scoring

**Ubicación:** Líneas 1035-1176 del template

---

### 5. Rollback Robusto

**Qué se agregó:**
- Backup completo pre-sprint (config, deploy, docs) con tarball timestamped
- Script `scripts/rollback/rollback-s[n].sh` con:
  - Pre/post health checks
  - Restauración de archivos desde backup
  - Rollback de K8s deployments
  - Rollback de DB migrations (Alembic/Django)
  - Restauración de API baselines
  - Limpieza de artefactos
  - Logging completo a archivo timestamped
  - Verificación de éxito post-rollback
- Test de integridad del backup
- Checklist de reversibilidad

**Beneficio:**
- Seguridad operacional en despliegues
- Rollback verificado y automatizado
- Trazabilidad completa de operaciones

**Ubicación:** Líneas 2818-3104 del template

---

### 6. Contactos & Soporte Obligatorios

**Qué se agregó:**
- Tabla de Owners (Principal, Secundario, Tech Lead) con email/Slack/disponibilidad
- Matriz de escalación (L1-L4) con SLA response y canales
- Reviewers por especialidad (7 áreas)
- Canales de comunicación (Slack, Email, Meetings, Docs)
- Contactos de emergencia (formato ASCII box con teléfonos)
- Procedimiento de escalación con diagrama Mermaid
- Criterios de severidad (Low/Medium/High/Critical)
- Información de rollback de emergencia
- Tools & Links útiles (Grafana, PagerDuty, GitHub, etc.)
- Timezone & Availability Matrix

**Beneficio:**
- Escalación clara en incidentes
- No más "a quién llamo en emergencia"
- SLAs explícitos por nivel
- Matriz de disponibilidad por timezone

**Ubicación:** Líneas 3636-3806 del template

---

## 📊 Métricas de la Actualización

| Métrica | Valor |
|---------|-------|
| **Líneas agregadas** | ~1,200 |
| **Secciones nuevas** | 6 |
| **Scripts nuevos** | 2 (update_adr_metrics.py, verify_dod.py) |
| **Workflows CI** | 1 (test-coverage.yml completo) |
| **Dashboards** | 1 (6 paneles Grafana) |
| **Tiempo de actualización** | ~45 minutos |
| **Archivos modificados** | 1 (SPRINT_TEMPLATE_CLAUDE_CLI.md) |
| **Archivos nuevos** | 2 (backup v2.2, este resumen) |

---

## 🔄 Comparativa v2.2 vs v2.4

| Aspecto | v2.2 Complete | v2.4 Enterprise |
|---------|---------------|-----------------|
| **ADRs** | Manuales | ✅ Automáticos con métricas |
| **Dashboards** | Referencias genéricas | ✅ JSON completo provisionado |
| **Coverage** | Sugerido | ✅ Gate obligatorio ≥85% |
| **DoD** | Lista de checkboxes | ✅ Matriz cuantificable + scoring |
| **Rollback** | Script básico | ✅ Robusto con health checks |
| **Contactos** | Lista simple | ✅ Matriz escalación + emergency |

---

## 📁 Archivos Generados

```
docs/03-Template/
├── SPRINT_TEMPLATE_CLAUDE_CLI.md          # ✅ Actualizado a v2.4
├── SPRINT_TEMPLATE_CLAUDE_CLI_v2.2_backup.md  # ✅ Backup v2.2
└── TEMPLATE_v2.4_UPDATE_SUMMARY.md        # ✅ Este documento
```

---

## 🚀 Próximos Pasos

### Para usar la plantilla v2.4:

1. **Crear nuevo sprint:**
   ```bash
   cp docs/03-Template/SPRINT_TEMPLATE_CLAUDE_CLI.md docs/01-sprint/S[N]/S[N]-[name].md
   ```

2. **Rellenar placeholders:**
   - `[N]` → Número del sprint
   - `[Sprint Name]` → Nombre del sprint
   - `[Owner 1]`, `[Owner 2]` → Nombres reales
   - Sección de Contactos (OBLIGATORIO)

3. **Implementar tools:**
   - `tools/update_adr_metrics.py`
   - `tools/verify_dod.py`
   - `scripts/rollback/rollback-s[n].sh`

4. **Configurar CI:**
   - `.github/workflows/test-coverage.yml`
   - `pytest.ini` con coverage gate
   - `.coveragerc` con exclusiones

5. **Provisionar dashboard:**
   - `deploy/grafana/dashboards/sprint-s[n]-dashboard.json`
   - `deploy/grafana/provisioning/dashboards.yaml`

---

## ✅ Validación de la Actualización

- [x] Backup de v2.2 creado
- [x] Header actualizado a v2.4
- [x] Sección ADRs automáticos agregada
- [x] Sección Dashboard Grafana agregada
- [x] Sección Coverage gate agregada
- [x] Sección DoD mejorada
- [x] Sección Rollback robusto agregada
- [x] Sección Contactos mejorada
- [x] Footer actualizado con cambios v2.4
- [x] Todos los TODOs completados

---

## 📝 Notas Adicionales

### Compatibilidad

La plantilla v2.4 es **compatible hacia atrás** con sprints que usen v2.2:
- Las secciones nuevas son opcionales
- Los sprints existentes no necesitan migración
- Se recomienda adoptar v2.4 para sprints nuevos

### Mantenimiento

La plantilla debe actualizarse cuando:
- Se agreguen nuevas mejores prácticas
- Cambien estándares del proyecto
- Se identifiquen puntos de mejora en retrospectivas

### Referencias

- Sprint S10.5: Ejemplo real de uso de v2.4 (performance framework)
- Sprint S7: Modelo de calidad (sandbox seguro)
- Roadmap: `docs/02-roadmaps/ROADMAP_INFERENCE_SERVICE.md`

---

**Autor:** AI Assistant (Claude Sonnet 4.5)  
**Aprobado por:** [Pending review]  
**Fecha de implementación:** 2025-10-16

