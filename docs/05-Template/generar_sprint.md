Genera el Sprint S[N] - [Nombre del Sprint] siguiendo EXACTAMENTE el template v2.2 Complete que adjunto.

## 📊 Datos del Sprint

**Información Básica:**
- Sprint: S[N] - [Nombre del Sprint]
- Repositorio: [nombre-repo]
- Branch: feature/s[n]-[branch-suffix]
- Duración: [N] semanas
- Kickoff: YYYY-MM-DD
- End Date: YYYY-MM-DD
- Owner Principal: [Owner 1]
- Owner Secundario: [Owner 2]

**Objetivo del Sprint:**
[Descripción detallada de 2-3 líneas sobre qué se busca lograr]

## 📦 Entregables Principales

1. **[Categoría 1]**
   - [Entregable específico 1.1]
   - [Entregable específico 1.2]
   - [Archivos a crear: ruta/archivo1, ruta/archivo2]

2. **[Categoría 2]**
   - [Entregable específico 2.1]
   - [Entregable específico 2.2]
   - [Archivos a crear: ruta/archivo3, ruta/archivo4]

3. **[Categoría 3]**
   - [Entregable específico 3.1]
   - [Archivos a crear: ruta/archivo5]

## 📈 SLOs Específicos

| Métrica | Target | Medición | Criticidad |
|---------|--------|----------|------------|
| [Nombre métrica 1] | < [N]ms / ≥ [X]% | [Herramienta medición] | 🔴 Crítico |
| [Nombre métrica 2] | < [N]ms / ≥ [X]% | [Herramienta medición] | 🔴 Crítico |
| [Nombre métrica 3] | ≥ [N] req/s | [Herramienta medición] | 🟡 Importante |
| [Nombre métrica 4] | < [N] min | [Herramienta medición] | 🟡 Importante |

## 🎯 Instrucciones CRÍTICAS

### ✅ MANTENER del Template (NO modificar estas secciones)

1. **🛡️ Error Handling Best Practices** (COMPLETO)
   - Script header estándar con set -euo pipefail
   - Las 10 funciones de logging (log_info, log_warn, log_error, log_success, log_debug)
   - Las 3 funciones de validación (check_command, check_file, check_directory)
   - Pattern 1: retry_with_backoff
   - Pattern 2: with_fallback
   - Pattern 3: cleanup on exit
   - Pattern 4: run_with_timeout
   - Pattern 5: idempotent_create + idempotent_mkdir
   - Pattern 6: checkpoint system (save_checkpoint, load_checkpoint, clear_checkpoint)
   - Pattern 7: show_progress
   - Pattern 8: run_parallel
   - Pattern 9: run_pattern_tests() - Test suite Bash (8 tests)
   - Pattern 10: Test-ErrorPatterns() - Test suite PowerShell (7 tests)
   - Timeout presets (TIMEOUT_TESTS, TIMEOUT_BUILD, etc.)

2. **PowerShell Equivalent Functions** (TODAS)
   - Write-Info, Write-Warn, Write-Error, Write-Success, Write-Debug
   - Test-Command, Test-File, Test-Directory
   - Invoke-RetryWithBackoff
   - Invoke-WithFallback
   - Register-Cleanup
   - Invoke-WithTimeout
   - New-IdempotentFile, New-IdempotentDirectory
   - Save-Checkpoint, Get-Checkpoint, Clear-Checkpoint
   - Show-Progress
   - Invoke-Parallel
   - Timeout presets PowerShell

3. **🤖 AI Agent Configuration** (JSON completo con 6 secciones)
````json
   {
     "sprint": { ... },      // 10 campos
     "targets": { ... },     // 7 campos
     "slos": { ... },        // 4+ campos ← IMPORTANTE
     "flags": { ... },       // 6 campos
     "dependencies": { ... }, // 3 campos ← IMPORTANTE (aunque esté vacío)
     "artifacts": { ... }    // 4 campos
   }
````

4. **📋 FASE 0: Pre-flight Checks** (5 pasos completos)
   - Verificar directorio
   - Verificar Git
   - Verificar herramientas (con check_version function)
   - Verificar prerequisites
   - Mostrar resumen
   - **CRÍTICO:** Incluir run_pattern_tests() en paso 3

5. **📋 FASE 1: Branch Setup** (3 pasos completos)
   - Actualizar develop
   - Crear feature branch
   - Documentar inicio

6. **📋 FASE [N-1]: Git Commit & Push** (5 pasos completos)
   - Verificar cambios
   - Agregar archivos
   - Crear commit (con conventional commits)
   - Push branch
   - Generar URL para PR

7. **📋 FASE [N-0.5]: Rollback Plan** (5 pasos completos)
   - Documentar estado pre-sprint
   - Crear rollback script (Bash + PowerShell)
   - Verificar reversibilidad
   - Documentar cambios críticos
   - Crear backup

8. **📋 FASE [N]: Final Verification & Reporting** (5 pasos completos)
   - Generar reporte de cambios
   - Verificar DoD
   - Generar PR Checklist
   - Generar PR Description
   - Mostrar resumen final

9. **Secciones Auxiliares** (mantener todas)
   - Dry-Run Mode
   - Execution Summary
   - Notas Importantes para el Agente AI
   - Referencias y Links
   - Contactos y Soporte
   - Apéndice: Comandos Útiles
   - Instrucción Final para Claude Code CLI

### 🔧 PERSONALIZAR (modificar según este sprint)

1. **🎯 Meta**
   - Usar el objetivo que proporcioné arriba

2. **📈 SLOs del Sprint**
   - Usar la tabla de SLOs que proporcioné
   - Mantener estructura de tabla
   - Incluir en JSON config también

3. **⚙️ Prerequisites**
   - Agregar herramientas específicas de este sprint
   - Mantener estructura base del template
   - Versiones específicas si son diferentes

4. **📦 Entregables**
   - Usar los entregables que proporcioné
   - Para cada entregable usar estructura:
````markdown
     ### Entregable N: [Nombre]
     **Descripción**: [Detalle]
     **Archivos a crear/modificar:**
````
     [lista de archivos]
````
     **Criterios de aceptación:**
     - [ ] [Criterio específico y verificable 1]
     - [ ] [Criterio específico y verificable 2]
````

5. **✅ Definition of Done**
   - Personalizar items según entregables
   - Mantener categorización (Infrastructure, Testing, Documentation, etc.)
   - Mantener scoring guide (✅✅, ✅⚠️, ⚠️, ❌)

6. **📋 FASE 2 a FASE [N-3]** (implementación específica)
   - Crear 6-10 fases personalizadas para este sprint
   - Cada fase debe tener:
````markdown
     ### 📋 FASE X: [Nombre Descriptivo]
     **⏱️ Duración estimada:** [N] minutos
     **🎯 Objetivo:** [Descripción clara]
     
     **Pasos ejecutables:**
     
     #### 1. [Nombre del paso]
```bash
     # Comentario explicativo
     comando_ejecutable_real
     
     # Validación
     comando_de_verificacion
```
     
     **✅ Criterio de éxito:** [Cómo verificar que funcionó]
````
   - **MUY IMPORTANTE:** Usar comandos EJECUTABLES, no pseudocódigo
   - Ejemplos:
     - ✅ BIEN: `cat > file.txt << 'EOF' ... EOF`
     - ❌ MAL: "Crear archivo file.txt con contenido X"

7. **🧪 Plan de Cobertura de Pruebas**
   - Personalizar módulos específicos del sprint
   - Definir cantidad de tests
   - Listar tests específicos por módulo

8. **📚 ADRs**
   - Agregar 2-3 decisiones arquitectónicas específicas
   - Usar estructura del template (Contexto, Decisión, Razón, Consecuencias, Alternativas)

## ⚠️ ERRORES CRÍTICOS A EVITAR

1. ❌ **NO omitir** Error Handling completo (los 10 patterns)
2. ❌ **NO omitir** PowerShell equivalent functions (todas)
3. ❌ **NO omitir** Test Suite v2.2 (Pattern 9 y 10)
4. ❌ **NO omitir** campos slos y dependencies en JSON
5. ❌ **NO omitir** FASE 0 completa (incluyendo run_pattern_tests)
6. ❌ **NO omitir** FASE N-0.5 (Rollback Plan)
7. ❌ **NO simplificar** fases críticas (0, 1, N-2, N-1, N-0.5, N)
8. ❌ **NO usar** placeholders genéricos en comandos (usar comandos reales)
9. ❌ **NO omitir** Dry-Run Mode
10. ❌ **NO omitir** timeout presets

## ✅ Validación del Resultado

El sprint generado DEBE cumplir:

- [ ] Header con "v2.2 Complete" presente
- [ ] Error Handling: Buscar "Pattern 1" hasta "Pattern 10" (debe haber 10)
- [ ] PowerShell: Buscar "Write-Info" (debe estar presente con todas las funciones)
- [ ] Test Suite: Buscar "run_pattern_tests()" y "Test-ErrorPatterns()" (ambos presentes)
- [ ] JSON Config: Debe tener 6 secciones (sprint, targets, slos, flags, dependencies, artifacts)
- [ ] FASE 0: Debe incluir llamada a run_pattern_tests()
- [ ] Mínimo 13 fases totales (0, 1, 2-X, N-2, N-1, N-0.5, N)
- [ ] Cada fase 2-X tiene comandos bash ejecutables (no pseudocódigo)
- [ ] DoD con scoring (✅✅, ✅⚠️, ⚠️, ❌)
- [ ] Dry-Run Mode presente
- [ ] Rollback Plan completo (Bash + PowerShell)

## 📁 Template Base

[ADJUNTAR AQUÍ EL ARCHIVO: SPRINT_TEMPLATE_CLAUDE_CLI.md v2.2 Complete]

O si está en tu knowledge base:
"Usa el archivo SPRINT_TEMPLATE_CLAUDE_CLI.md v2.2 Complete de tu knowledge base"

## 🎯 Formato de Salida

Devuelve el sprint completo en formato Markdown, listo para guardar como:
`S[N] — [Nombre del Sprint].md`

**Expectativa de calidad:**
- Conformidad con template: ≥ 98%
- Score vs template: 98-100/100
- Status: Production Ready
- Tier: Gold 🏆