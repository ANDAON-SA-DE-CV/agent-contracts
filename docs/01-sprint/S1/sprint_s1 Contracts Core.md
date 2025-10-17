# S1 — Contracts Core ⏸️ **[PENDIENTE]**

> **🤖 DOCUMENTO OPTIMIZADO PARA CLAUDE CODE CLI v2.2**  
> Este documento contiene instrucciones ejecutables paso a paso  
> **Version:** 2.2 Complete (incluye DoD cuantificable, QA interno, ADRs, SLOs, Rollback, Cross-repo deps, PowerShell parity, Error pattern tests)
> 
> **AI Agent Role:** Staff Backend Engineer / Contract Architect
> 
> **Repo:** `agent-contracts`  
> **Branch:** `feature/s1-contracts-core` (base: `develop`)  
> **Duración estimada:** 2 semanas  
> **Owners:** Contract Architect + Platform Engineer  
> **KICKOFF_DATE:** 2025-01-27  
> **END_DATE:** 2025-02-10
> 
> **📋 Alineación con Roadmap:**  
> `docs/01-sprint/roadmaps/agent_contracts_roadmap_2025_2026_detallado.md` - Sprint S1

---

## 🛡️ Error Handling Best Practices

> **🎯 CRÍTICO v2.1:** Scripts robustos con manejo de errores completo

### Script Header Estándar
```bash
#!/usr/bin/env bash
# Script: [Nombre del script]
# Sprint: S1 - Contracts Core
# Author: [Author]
# Date: $(date)

# Error handling robusto
set -euo pipefail
trap 'echo "❌ ERROR at line $LINENO in $0"' ERR

# Logging functions with structured output
LOG_FILE="sprint-s1.log"

log_info() { 
  local message="[$(date +'%Y-%m-%d %H:%M:%S')] [INFO] $*"
  echo "ℹ️  INFO: $*"
  echo "$message" >> "$LOG_FILE"
}

log_warn() { 
  local message="[$(date +'%Y-%m-%d %H:%M:%S')] [WARN] $*"
  echo "⚠️  WARN: $*"
  echo "$message" >> "$LOG_FILE"
}

log_error() { 
  local message="[$(date +'%Y-%m-%d %H:%M:%S')] [ERROR] $*"
  echo "❌ ERROR: $*"
  echo "$message" >> "$LOG_FILE" >&2
}

log_success() { 
  local message="[$(date +'%Y-%m-%d %H:%M:%S')] [SUCCESS] $*"
  echo "✅ SUCCESS: $*"
  echo "$message" >> "$LOG_FILE"
}

log_debug() { 
  local message="[$(date +'%Y-%m-%d %H:%M:%S')] [DEBUG] $*"
  if [ "${DEBUG:-false}" = "true" ]; then
    echo "🔍 DEBUG: $*"
    echo "$message" >> "$LOG_FILE"
  fi
}

# Validation functions
check_command() {
  if ! command -v "$1" &> /dev/null; then
    log_error "Command '$1' not found"
    exit 1
  fi
}

check_file() {
  if [ ! -f "$1" ]; then
    log_error "File '$1' not found"
    exit 1
  fi
}

check_directory() {
  if [ ! -d "$1" ]; then
    log_error "Directory '$1' not found"
    exit 1
  fi
}
```

### Error Recovery Patterns
```bash
# Pattern 1: Retry with backoff
retry_with_backoff() {
  local max_attempts=3
  local delay=2
  local attempt=1
  
  while [ $attempt -le $max_attempts ]; do
    if "$@"; then
      return 0
    fi
    log_warn "Attempt $attempt failed, retrying in ${delay}s..."
    sleep $delay
    ((attempt++))
    ((delay *= 2))
  done
  
  log_error "All $max_attempts attempts failed"
  return 1
}

# Pattern 2: Graceful degradation
with_fallback() {
  if ! "$1"; then
    log_warn "Primary command failed, trying fallback..."
    "$2"
  fi
}

# Pattern 3: Cleanup on exit
cleanup() {
  log_info "Cleaning up temporary files..."
  rm -f /tmp/sprint-*.tmp 2>/dev/null || true
}
trap cleanup EXIT

# Pattern 4: Timeout wrapper
run_with_timeout() {
  local timeout_seconds="$1"
  local command="$2"
  local description="${3:-Command execution}"
  
  log_info "Running: $description (timeout: ${timeout_seconds}s)"
  
  if timeout "$timeout_seconds" bash -c "$command"; then
    log_success "$description completed successfully"
    return 0
  else
    local exit_code=$?
    if [ $exit_code -eq 124 ]; then
      log_error "$description timed out after ${timeout_seconds} seconds"
    else
      log_error "$description failed with exit code $exit_code"
    fi
    return $exit_code
  fi
}

# Pattern 5: Idempotent operations
idempotent_create() {
  local file_path="$1"
  local content="$2"
  local description="${3:-File creation}"
  
  if [ -f "$file_path" ]; then
    log_warn "$description skipped - file already exists: $file_path"
    return 0
  fi
  
  log_info "Creating: $description"
  cat > "$file_path" << 'EOF'
$content
EOF
  log_success "$description completed: $file_path"
}

idempotent_mkdir() {
  local dir_path="$1"
  local description="${2:-Directory creation}"
  
  if [ -d "$dir_path" ]; then
    log_warn "$description skipped - directory already exists: $dir_path"
    return 0
  fi
  
  log_info "Creating: $description"
  mkdir -p "$dir_path"
  log_success "$description completed: $dir_path"
}

# Pattern 6: Checkpoint system
CHECKPOINT_FILE=".sprint-checkpoint"

save_checkpoint() {
  local phase="$1"
  echo "$phase" > "$CHECKPOINT_FILE"
  log_info "Checkpoint saved: FASE $phase"
}

load_checkpoint() {
  if [ -f "$CHECKPOINT_FILE" ]; then
    cat "$CHECKPOINT_FILE"
  else
    echo "0"
  fi
}

clear_checkpoint() {
  rm -f "$CHECKPOINT_FILE"
  log_info "Checkpoint cleared"
}

# Pattern 7: Progress indicator
show_progress() {
  local phase="$1"
  local total="$2"
  local phase_name="${3:-FASE $phase}"
  
  local percent=$((phase * 100 / total))
  local filled=$((percent / 2))
  local empty=$((50 - filled))
  
  echo ""
  echo "📊 Progress: [$phase/$total] ($percent%) - $phase_name"
  printf '['
  printf '%*s' $filled | tr ' ' '='
  if [ $filled -lt 50 ]; then
    printf '>'
  fi
  printf '%*s' $empty | tr ' ' ' '
  printf ']'
  echo ""
  echo ""
}

# Pattern 8: Parallel execution
run_parallel() {
  local task1="$1"
  local task2="$2"
  local description1="${3:-Task 1}"
  local description2="${4:-Task 2}"
  
  log_info "Running independent tasks in parallel: $description1, $description2"
  
  # Run tasks in background
  eval "$task1" > "${description1// /_}.log" 2>&1 &
  local pid1=$!
  
  eval "$task2" > "${description2// /_}.log" 2>&1 &
  local pid2=$!
  
  # Wait for both tasks
  wait $pid1
  local exit1=$?
  
  wait $pid2
  local exit2=$?
  
  # Check results
  if [ $exit1 -eq 0 ] && [ $exit2 -eq 0 ]; then
    log_success "Both parallel tasks completed successfully"
    return 0
  else
    log_error "Some parallel tasks failed (exit codes: $exit1, $exit2)"
    return 1
  fi
}

# Timeout presets para comandos comunes
TIMEOUT_TESTS=300        # 5 minutos para tests
TIMEOUT_BUILD=600        # 10 minutos para builds
TIMEOUT_INSTALL=180      # 3 minutos para installs
TIMEOUT_VALIDATION=60    # 1 minuto para validaciones
TIMEOUT_GIT=30           # 30 segundos para operaciones git

# Pattern 9: Test suite para validar error patterns (v2.1)
# Ejecutar tests de validación de patterns
run_pattern_tests() {
  local test_dir="tests/error-patterns"
  local test_log="pattern-tests.log"
  
  log_info "Running error pattern validation tests..."
  
  # Crear directorio de tests si no existe
  mkdir -p "$test_dir"
  
  # Test 1: Validación de funciones de logging
  log_info "Testing logging functions..."
  if log_info "Test info message" && log_success "Test success message" && log_warn "Test warning message"; then
    log_success "Logging functions test: PASSED"
  else
    log_error "Logging functions test: FAILED"
    return 1
  fi
  
  # Test 2: Validación de funciones de validación
  log_info "Testing validation functions..."
  if check_command "ls" && check_file "/etc/passwd" && check_directory "/tmp"; then
    log_success "Validation functions test: PASSED"
  else
    log_error "Validation functions test: FAILED"
    return 1
  fi
  
  # Test 3: Validación de retry pattern
  log_info "Testing retry pattern..."
  local retry_attempts=0
  retry_test() {
    ((retry_attempts++))
    if [ $retry_attempts -eq 2 ]; then
      return 0
    fi
    return 1
  }
  
  if retry_with_backoff retry_test && [ $retry_attempts -eq 2 ]; then
    log_success "Retry pattern test: PASSED"
  else
    log_error "Retry pattern test: FAILED"
    return 1
  fi
  
  # Test 4: Validación de timeout pattern
  log_info "Testing timeout pattern..."
  if run_with_timeout 2 "echo 'timeout test'" "Timeout test"; then
    log_success "Timeout pattern test: PASSED"
  else
    log_error "Timeout pattern test: FAILED"
    return 1
  fi
  
  # Test 5: Validación de idempotencia
  log_info "Testing idempotent patterns..."
  local test_file="/tmp/test-idempotent-$$"
  local test_dir="/tmp/test-idempotent-dir-$$"
  
  # Test idempotent file creation
  idempotent_create "$test_file" "test content" "Test file"
  if [ -f "$test_file" ]; then
    log_success "Idempotent file creation: PASSED"
  else
    log_error "Idempotent file creation: FAILED"
    return 1
  fi
  
  # Test idempotent directory creation
  idempotent_mkdir "$test_dir" "Test directory"
  if [ -d "$test_dir" ]; then
    log_success "Idempotent directory creation: PASSED"
  else
    log_error "Idempotent directory creation: FAILED"
    return 1
  fi
  
  # Test 6: Validación de checkpoint system
  log_info "Testing checkpoint system..."
  save_checkpoint "5"
  local loaded_checkpoint=$(load_checkpoint)
  if [ "$loaded_checkpoint" = "5" ]; then
    log_success "Checkpoint system test: PASSED"
  else
    log_error "Checkpoint system test: FAILED"
    return 1
  fi
  
  # Test 7: Validación de parallel execution
  log_info "Testing parallel execution..."
  parallel_task1() { sleep 0.1; echo "task1 completed"; return 0; }
  parallel_task2() { sleep 0.1; echo "task2 completed"; return 0; }
  
  if run_parallel "parallel_task1" "parallel_task2" "Parallel Task 1" "Parallel Task 2"; then
    log_success "Parallel execution test: PASSED"
  else
    log_error "Parallel execution test: FAILED"
    return 1
  fi
  
  # Cleanup
  rm -f "$test_file"
  rm -rf "$test_dir"
  clear_checkpoint
  
  log_success "All error pattern tests completed successfully"
  return 0
}
```

### PowerShell Equivalent Functions

```powershell
# PowerShell equivalent functions for Windows environments
# Add these to your PowerShell scripts for full parity

# Logging functions (PowerShell)
function Write-Info {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [INFO] $Message"
    Write-Host "ℹ️  INFO: $Message" -ForegroundColor Cyan
    Add-Content -Path "sprint-s1.log" -Value $logMessage
}

function Write-Warn {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [WARN] $Message"
    Write-Host "⚠️  WARN: $Message" -ForegroundColor Yellow
    Add-Content -Path "sprint-s1.log" -Value $logMessage
}

function Write-Error {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [ERROR] $Message"
    Write-Host "❌ ERROR: $Message" -ForegroundColor Red
    Add-Content -Path "sprint-s1.log" -Value $logMessage
}

function Write-Success {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [SUCCESS] $Message"
    Write-Host "✅ SUCCESS: $Message" -ForegroundColor Green
    Add-Content -Path "sprint-s1.log" -Value $logMessage
}

function Write-Debug {
    param([string]$Message)
    if ($env:DEBUG -eq "true") {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        $logMessage = "[$timestamp] [DEBUG] $Message"
        Write-Host "🔍 DEBUG: $Message" -ForegroundColor Magenta
        Add-Content -Path "sprint-s1.log" -Value $logMessage
    }
}

# Validation functions (PowerShell)
function Test-Command {
    param([string]$Command)
    if (-not (Get-Command $Command -ErrorAction SilentlyContinue)) {
        Write-Error "Command '$Command' not found"
        exit 1
    }
}

function Test-File {
    param([string]$Path)
    if (-not (Test-Path $Path -PathType Leaf)) {
        Write-Error "File '$Path' not found"
        exit 1
    }
}

function Test-Directory {
    param([string]$Path)
    if (-not (Test-Path $Path -PathType Container)) {
        Write-Error "Directory '$Path' not found"
        exit 1
    }
}

# Pattern 1: Retry with backoff (PowerShell)
function Invoke-RetryWithBackoff {
    param(
        [scriptblock]$Command,
        [int]$MaxAttempts = 3,
        [int]$InitialDelay = 2
    )
    
    $attempt = 1
    $delay = $InitialDelay
    
    while ($attempt -le $MaxAttempts) {
        try {
            & $Command
            return $true
        }
        catch {
            if ($attempt -eq $MaxAttempts) {
                Write-Error "All $MaxAttempts attempts failed: $_"
                return $false
            }
            Write-Warn "Attempt $attempt failed, retrying in ${delay}s... Error: $_"
            Start-Sleep -Seconds $delay
            $attempt++
            $delay *= 2
        }
    }
}

# Pattern 2: Graceful degradation (PowerShell)
function Invoke-WithFallback {
    param(
        [scriptblock]$PrimaryCommand,
        [scriptblock]$FallbackCommand
    )
    
    try {
        & $PrimaryCommand
    }
    catch {
        Write-Warn "Primary command failed, trying fallback... Error: $_"
        & $FallbackCommand
    }
}

# Pattern 3: Cleanup on exit (PowerShell)
function Register-Cleanup {
    param([scriptblock]$CleanupScript)
    
    $script:CleanupAction = $CleanupScript
    Register-EngineEvent -SourceIdentifier PowerShell.Exiting -Action {
        if ($script:CleanupAction) {
            & $script:CleanupAction
        }
    }
}

# Pattern 4: Timeout wrapper (PowerShell)
function Invoke-WithTimeout {
    param(
        [int]$TimeoutSeconds,
        [scriptblock]$Command,
        [string]$Description = "Command execution"
    )
    
    Write-Info "Running: $Description (timeout: ${TimeoutSeconds}s)"
    
    $job = Start-Job -ScriptBlock $Command
    $result = Wait-Job -Job $job -Timeout $TimeoutSeconds
    
    if ($result) {
        $output = Receive-Job -Job $job
        Remove-Job -Job $job
        Write-Success "$Description completed successfully"
        return $output
    }
    else {
        Stop-Job -Job $job
        Remove-Job -Job $job
        Write-Error "$Description timed out after $TimeoutSeconds seconds"
        return $false
    }
}

# Pattern 5: Idempotent operations (PowerShell)
function New-IdempotentFile {
    param(
        [string]$FilePath,
        [string]$Content,
        [string]$Description = "File creation"
    )
    
    if (Test-Path $FilePath -PathType Leaf) {
        Write-Warn "$Description skipped - file already exists: $FilePath"
        return
    }
    
    Write-Info "Creating: $Description"
    Set-Content -Path $FilePath -Value $Content -Encoding UTF8
    Write-Success "$Description completed: $FilePath"
}

function New-IdempotentDirectory {
    param(
        [string]$Path,
        [string]$Description = "Directory creation"
    )
    
    if (Test-Path $Path -PathType Container) {
        Write-Warn "$Description skipped - directory already exists: $Path"
        return
    }
    
    Write-Info "Creating: $Description"
    New-Item -Path $Path -ItemType Directory -Force | Out-Null
    Write-Success "$Description completed: $Path"
}

# Pattern 6: Checkpoint system (PowerShell)
$script:CheckpointFile = ".sprint-checkpoint"

function Save-Checkpoint {
    param([string]$Phase)
    Set-Content -Path $script:CheckpointFile -Value $Phase
    Write-Info "Checkpoint saved: FASE $Phase"
}

function Get-Checkpoint {
    if (Test-Path $script:CheckpointFile) {
        return Get-Content -Path $script:CheckpointFile
    }
    return "0"
}

function Clear-Checkpoint {
    if (Test-Path $script:CheckpointFile) {
        Remove-Item $script:CheckpointFile
        Write-Info "Checkpoint cleared"
    }
}

# Pattern 7: Progress indicator (PowerShell)
function Show-Progress {
    param(
        [int]$Phase,
        [int]$Total,
        [string]$PhaseName = "FASE $Phase"
    )
    
    $percent = [math]::Round(($Phase * 100) / $Total)
    $filled = [math]::Round($percent / 2)
    $empty = 50 - $filled
    
    Write-Host ""
    Write-Host "📊 Progress: [$Phase/$Total] ($percent%) - $PhaseName" -ForegroundColor Cyan
    Write-Host "[" -NoNewline
    Write-Host ("=" * $filled) -NoNewline -ForegroundColor Green
    if ($filled -lt 50) {
        Write-Host ">" -NoNewline -ForegroundColor Green
    }
    Write-Host (" " * $empty) -NoNewline
    Write-Host "]"
    Write-Host ""
}

# Pattern 8: Parallel execution (PowerShell)
function Invoke-Parallel {
    param(
        [scriptblock]$Task1,
        [scriptblock]$Task2,
        [string]$Description1 = "Task 1",
        [string]$Description2 = "Task 2"
    )
    
    Write-Info "Running independent tasks in parallel: $Description1, $Description2"
    
    $job1 = Start-Job -ScriptBlock $Task1
    $job2 = Start-Job -ScriptBlock $Task2
    
    $result1 = Wait-Job -Job $job1
    $result2 = Wait-Job -Job $job2
    
    $output1 = Receive-Job -Job $job1
    $output2 = Receive-Job -Job $job2
    
    $exit1 = $job1.State -eq "Completed"
    $exit2 = $job2.State -eq "Completed"
    
    Remove-Job -Job $job1, $job2
    
    if ($exit1 -and $exit2) {
        Write-Success "Both parallel tasks completed successfully"
        return $true
    }
    else {
        Write-Error "Some parallel tasks failed (exit codes: $exit1, $exit2)"
        return $false
    }
}

# Timeout presets (PowerShell)
$script:TIMEOUT_TESTS = 300        # 5 minutos para tests
$script:TIMEOUT_BUILD = 600        # 10 minutos para builds
$script:TIMEOUT_INSTALL = 180      # 3 minutos para installs
$script:TIMEOUT_VALIDATION = 60    # 1 minuto para validaciones
$script:TIMEOUT_GIT = 30           # 30 segundos para operaciones git
```

---

## 🤖 AI Agent Configuration

> **🎯 Novedad v2.0:** Configuración estructurada para Claude Code CLI

### Sprint Configuration JSON

```json
{
  "sprint": {
    "number": "1",
    "name": "Contracts Core",
    "slug": "contracts-core",
    "repo": "agent-contracts",
    "service_name": "agent-contracts",
    "branch_base": "develop",
    "branch_feature": "feature/s1-contracts-core",
    "owner_primary": "Contract Architect",
    "owner_secondary": "Platform Engineer",
    "kickoff_date": "2025-01-27",
    "end_date": "2025-02-10"
  },
  "targets": {
    "duration_weeks": 2,
    "files_to_create": 15,
    "files_to_modify": 8,
    "tests_target": 12,
    "coverage_target_percent": 85,
    "ci_time_max_minutes": 10,
    "loc_estimate": 2500
  },
  "slos": {
    "latency_p95_ms": 100,
    "throughput_rps": 1000,
    "error_rate_percent": 0.1,
    "build_time_minutes": 5
  },
  "flags": {
    "has_db_migrations": false,
    "requires_mocks": true,
    "needs_security_review": true,
    "cross_repo_deps": false,
    "breaking_changes": false,
    "requires_baseline_update": true
  },
  "dependencies": {
    "agent_contracts_version": "1.0.0",
    "nops_kernel_api": "v1/health",
    "other_repos": []
  },
  "artifacts": {
    "docs_dir": "docs/01-sprint/S1",
    "tracking_file": "S1_SPRINT_TRACKING.md",
    "completion_report": "S1_COMPLETION_REPORT.md",
    "rollback_info": "ROLLBACK_INFO.txt"
  }
}
```

### Uso de la Configuración

Los placeholders en este documento deben reemplazarse usando los valores del JSON:
- `[1]` → `sprint.number`
- `[Contracts Core]` → `sprint.name`
- `[agent-contracts]` → `sprint.repo`
- `[contracts-core]` → extraído de `sprint.branch_feature`
- Etc.

**Comando de inicio sugerido para Claude Code CLI:**
```bash
# Iniciar sprint con configuración
claude-code-cli execute-sprint \
  --config sprint-config.json \
  --document "docs/01-sprint/S1/S1-contracts-core.md"
```

---

## 📁 Ubicación de Artefactos del Sprint

> **🎯 Novedad v2.0:** Estructura estandarizada de documentación

Todos los artefactos del sprint deben crearse siguiendo esta estructura:

```
docs/01-sprint/S1/
├── README.md                           # Resumen ejecutivo del sprint
├── S1-IMPLEMENTATION-GUIDE.md          # Guía técnica de implementación
├── S1-TROUBLESHOOTING.md               # Guía de resolución de problemas
├── HOWTO_S1.md                         # Quick start / comandos útiles
├── dod-checklist.md                    # Checklist del Definition of Done
├── ADR-1-001-contract-design.md        # Architecture Decision Records
├── ADR-1-002-error-handling.md
└── patches/                            # Patches opcionales (si aplica)
    ├── patch-001-spectral-fix.diff
    └── patch-002-schema-update.diff
```

**Archivos generados automáticamente (raíz del repo):**
```
[repo-root]/
├── S1_SPRINT_TRACKING.md               # Tracking de progreso (FASE 1)
├── S1_COMPLETION_REPORT.md             # Reporte final (FASE 13)
├── PR_CHECKLIST.md                     # Checklist para PR (FASE 13)
├── PR_DESCRIPTION.md                   # Descripción de PR (FASE 13)
└── ROLLBACK_INFO.txt                   # Info de rollback (FASE 12.5)
```

**Convención de nombres:**
- Usar `S1` con número del sprint (ej: `S1`)
- Slugs en kebab-case (ej: `contracts-core`)
- Dates en formato ISO 8601 (ej: `2025-01-27`)

---

## 🎯 Meta
Definir y validar los **Contratos Core** para ENIS (OpenAPI, JSON Schema, Protobuf) de **Inference**, **Agents**, **Events** y **NOPS**, incluyendo **catálogo de errores** y **política de cambios (FREEZE/Deprecation/Emergency RFC)**, con verificación automática en CI (Spectral/AJV/Buf) y smoke local (Prism/WireMock).

### 📈 SLOs del Sprint (Service Level Objectives)

> **🎯 Novedad v2.0:** Métricas técnicas medibles para declarar éxito

| Métrica | Target | Medición | Criticidad |
|---------|--------|----------|------------|
| **CI Validation Time** | < 5 min | Spectral/AJV/Buf | 🔴 Crítico |
| **Contract Errors** | 0 errors | Spectral/AJV/Buf (severity ≥ warn) | 🔴 Crítico |
| **Endpoint Documentation** | 100% | Request/response examples | 🔴 Crítico |
| **Build Time** | < 5 min | CI pipeline | 🟡 Importante |
| **Test Coverage** | ≥ 85% | pytest --cov | 🔴 Crítico |
| **API Response Time** | < 100ms | Load test | 🟡 Importante |

**Criterio de éxito técnico:** 
- Todos los SLOs 🔴 Críticos deben cumplirse
- Al menos 80% de los 🟡 Importantes deben cumplirse
- Los 🟢 Nice-to-have son opcionales pero deseables

---

## ⚙️ Prerrequisitos (verificar antes de ejecutar)
- Git ≥ 2.30, Node 20 LTS, Python 3.11+, Go 1.21+
- Herramientas: `@stoplight/spectral` 6.11.0, `ajv-cli` 5.x (AJV 8.12), `buf` 1.28.1, `oasdiff` 1.10.x, **cosign 2.2.x**
- Acceso a GitHub Actions, permisos para crear branches, Docker/Compose local
- Pre-commit instalado y hooks activos
- **Secrets requeridos** (en GitHub): `PACT_BROKER_BASE_URL`, `PACT_BROKER_TOKEN`, `SLACK_WEBHOOK_URL`, **`COSIGN_KEY`**

### Cross-Repository Dependencies

> **🎯 Novedad v2.0:** Dependencias con otros repositorios de ENIS

**Dependencias identificadas:**
- [ ] **agent-contracts:** Versión 1.0.0 de contratos requerida
- [ ] **nops-kernel:** API v1/health disponible
- [ ] **edge-infrastructure:** [Feature/componente] desplegado
- [ ] **[otro-repo]:** [Dependencia específica]

**Orden de sincronización:**
1. Si modificas contratos → Actualizar `agent-contracts` **PRIMERO**
2. Si usas módulos NOPS → Verificar compatibilidad de versión
3. Si integras con edge → Coordinar con team de edge-infrastructure

**Checklist de validación cross-repo:**
```bash
# Verificar versión de contratos disponible
curl -s http://localhost:8080/api/contracts/version | jq .

# Verificar NOPS kernel accesible
curl -s http://localhost:9090/health

# Verificar dependencias en package.json/requirements.txt
grep "@enis/agent-contracts" package.json

# [Otros checks específicos del sprint]
```

**Contacts para coordinación:**
- Agent Contracts: @contracts-team (Slack: #contracts-rfcs)
- NOPS Kernel: @nops-team (Slack: #nops-development)
- Edge Infrastructure: @edge-team (Slack: #edge-ops)

---

## 🔍 QA Interno & Auto-análisis

> **🎯 Novedad v2.0:** Sección de auto-validación del sprint

### Issues Detectados & Severidad

#### ISSUE 1 — Contract Validation Errors (🔴 crítico)

**Problema:**  
Posibles inconsistencias entre OpenAPI, JSON Schema y Protocol Buffers que podrían causar errores de validación en CI.

**Impacto:**  
Bloquea el cumplimiento del SLO "Contract Errors: 0 errors" y puede causar fallos en integración.

**Patch sugerido:**
```diff
*** Begin Patch
*** Update File: .github/workflows/contracts-validate.yml
@@
+    - name: Cross-validate contracts
+      run: |
+        # Validar consistencia entre OpenAPI y Proto
+        python3 scripts/validate-cross-format.py
+        # Verificar referencias entre OpenAPI y JSON Schema
+        python3 scripts/validate-schema-refs.py
*** End Patch
```

**Beneficio:**  
Eleva DoD item "Contract validation" de 80% a 100% y previene errores de integración.

---

#### ISSUE 2 — Missing Error Handling Patterns (🟡 medio)

**Problema:**  
Los scripts de validación no incluyen manejo robusto de errores según los patrones definidos en la plantilla v2.2.

**Impacto:**  
Puede causar fallos silenciosos en CI y dificultar el debugging.

**Patch sugerido:**
```diff
*** Begin Patch
*** Update File: scripts/validate-contracts.sh
@@
+#!/usr/bin/env bash
+set -euo pipefail
+trap 'echo "❌ ERROR at line $LINENO in $0"' ERR
+
+source scripts/error-handling.sh
*** End Patch
```

**Beneficio:**  
Eleva DoD item "Error handling" de 60% a 100% y mejora la robustez del sprint.

---

### ✅ Acciones para Cerrar 100% del DoD

1. Aplicar **Patch Cross-validation** (ISSUE 1)  
2. Implementar **Error Handling Patterns** (ISSUE 2)  
3. Agregar **tests de integración faltantes** para cobertura 85%

> **Tras completar estas acciones:** DoD = 12/15 = 100%

---

## 📚 ADRs (Architecture Decision Records)

> **🎯 Novedad v2.0:** Decisiones arquitectónicas documentadas

### ADR Template

Cada ADR debe incluir:
- **Contexto:** Por qué necesitamos decidir esto
- **Decisión:** Qué decidimos hacer
- **Consecuencias:** Implicaciones (positivas y negativas)
- **Alternativas consideradas:** Qué más evaluamos

---

### ADR-1-001 — OpenAPI 3.0.3 vs 3.1.0

**Contexto:**  
Necesitamos decidir entre OpenAPI 3.0.3 y 3.1.0 para los contratos de ENIS. La diferencia principal está en el soporte de JSON Schema y características avanzadas.

**Decisión:**  
Usar OpenAPI 3.0.3 para máxima compatibilidad con herramientas existentes.

**Razón:**
- [Razón 1: Mejor soporte en Spectral y herramientas de validación]
- [Razón 2: Compatibilidad con Prism para mocking]
- [Razón 3: Menor curva de aprendizaje para el equipo]

**Consecuencias:**
- ✅ **Positivas:** [Herramientas estables, documentación abundante, compatibilidad amplia]
- ⚠️ **Negativas:** [Menos características avanzadas de JSON Schema, limitaciones en tipos complejos]

**Alternativas consideradas:**
1. OpenAPI 3.1.0: Rechazado (herramientas inmaduras)
2. OpenAPI 2.0: Rechazado (deprecated, limitaciones severas)
3. AsyncAPI: Rechazado (no aplica para APIs síncronas)

**Archivo:** `docs/01-sprint/S1/ADR-1-001-openapi-version.md`

---

### ADR-1-002 — Error Handling Strategy

**Contexto:**  
Necesitamos definir una estrategia consistente para manejo de errores en todos los contratos de ENIS.

**Decisión:**  
Implementar error responses estandarizados con códigos de error canónicos (AC-XXXX) y estructura uniforme.

**Razón:**
- [Razón 1: Consistencia entre servicios]
- [Razón 2: Facilita debugging y monitoreo]
- [Razón 3: Mejora experiencia de desarrolladores]

**Consecuencias:**
- ✅ **Positivas:** [Debugging simplificado, monitoreo consistente, mejor UX]
- ⚠️ **Negativas:** [Overhead de implementación, migración de servicios existentes]

**Alternativas consideradas:**
1. HTTP status codes únicamente: Rechazado (insuficiente granularidad)
2. Error messages libres: Rechazado (inconsistencia)
3. Códigos numéricos simples: Rechazado (menos descriptivos)

**Archivo:** `docs/01-sprint/S1/ADR-1-002-error-handling.md`

---

## 🧪 Plan de Cobertura de Pruebas

> **🎯 Novedad v2.0:** Plan detallado de testing

### Objetivo de Cobertura

- **Target:** 12 tests totales
- **Coverage:** ≥85%
- **Distribución:** Unit (60%), Integration (30%), E2E (10%)

### Breakdown por Módulo

| Módulo/Feature | Tests | Tipo | Prioridad | Status |
|----------------|-------|------|-----------|--------|
| OpenAPI Validation | 4 | unit | 🔴 alta | ⏸️ |
| JSON Schema Validation | 3 | integration | 🟡 media | ⏸️ |
| Protocol Buffer Validation | 2 | unit | 🟡 media | ⏸️ |
| Contract Integration | 2 | integration | 🔴 alta | ⏸️ |
| Error Handling | 1 | unit | 🟢 baja | ⏸️ |

### Tests Detallados

#### Módulo: OpenAPI Validation
**Archivo:** `tests/contracts/test_openapi_validation.py`  
**Tests:** 4

1. `test_inference_openapi_structure` - Valida estructura básica de inference.yaml
2. `test_streaming_endpoints` - Verifica endpoints de streaming con SSE
3. `test_error_responses` - Valida respuestas de error estandarizadas
4. `test_examples_completeness` - Verifica que todos los endpoints tengan ejemplos

**Cobertura esperada:** ≥85%

---

#### Módulo: JSON Schema Validation
**Archivo:** `tests/contracts/test_schema_validation.py`  
**Tests:** 3

1. `test_schema_compilation` - Valida que todos los schemas compilen
2. `test_schema_references` - Verifica referencias desde OpenAPI a schemas
3. `test_schema_examples` - Valida ejemplos contra schemas

**Cobertura esperada:** ≥85%

---

#### Módulo: Protocol Buffer Validation
**Archivo:** `tests/contracts/test_proto_validation.py`  
**Tests:** 2

1. `test_proto_compilation` - Valida compilación de archivos .proto
2. `test_proto_openapi_consistency` - Verifica consistencia con OpenAPI

**Cobertura esperada:** ≥80%

---

#### Módulo: Contract Integration
**Archivo:** `tests/integration/test_contract_integration.py`  
**Tests:** 2 E2E

1. `test_full_contract_validation_flow` - Flujo completo de validación
2. `test_mock_server_compatibility` - Compatibilidad con Prism/WireMock

**Cobertura esperada:** ≥90%

### Integration Tests

**Archivo:** `tests/integration/test_contracts_e2e.py`  
**Tests:** 1 E2E

1. `test_contracts_end_to_end` - Validación completa de todos los contratos

### Test Markers

```python
@pytest.mark.unit        # Tests unitarios rápidos
@pytest.mark.integration # Tests que requieren servicios externos
@pytest.mark.slow        # Tests que toman >1s
@pytest.mark.contracts   # Tests específicos de contratos
```

---

## 📦 Entregables
**Contratos**
- `openapi/v1/inference.yaml` (sync) y `openapi/v1/inference-streaming.yaml` (stream)
- `openapi/v1/agents.yaml`, `openapi/v1/events.yaml`, `openapi/v1/nops.yaml`
- `schemas/{agent-registration.json, inference-request.json, event-schema.json, policy-schema.json}`
- `proto/{inference.proto, agents.proto, events.proto, federation.proto}`

**Documentación S1**
- `docs/01-sprint/S1/errors.md` (catálogo canónico de códigos de error)  
- `docs/01-sprint/S1/CONTRACTS-GUIDE.md` (estilo y convenciones)  
- `docs/01-sprint/S1/CHANGE-POLICY.md` (FREEZE/Deprecation/Emergency RFC)
> **Nota:** usar siempre la ruta canónica `\docs\01-sprint\S1\...` (no `docs/ERROR_CODES.md`).

**Testing & Mocks**
- `tests/contracts/{test_openapi_contract.py, test_schema_validation.py}`
- `tests/pact/test_pact_consumer.py` (esqueleto)
- Mocks vivos: Prism (OpenAPI) y WireMock (NOPS) actualizados

**CI/CD**
- Workflows existentes de S0 extendidos para nuevos archivos (lint/breaking/examples)  
- **Baseline firmado**: pipeline `contracts-baseline.yml` con **Cosign**

---

## 🤖 AI EXECUTION PLAN — Claude Code CLI Work Order

> **🎯 INSTRUCCIONES PARA EL AGENTE AI:**  
> 
> 1. **Ejecutar en orden secuencial** - No saltar fases ni pasos
> 2. **Verificar cada fase** - Confirmar éxito antes de continuar
> 3. **Reportar estado** - Usar ✅ Completado / ⚠️ Advertencias / ❌ Falló
> 4. **Documentar errores** - Si algo falla, documentar y decidir si continuar
> 5. **Generar reportes** - Al finalizar, crear reportes completos
>
> **Formato de reporte por fase:**
> ```
> FASE [N]: [Nombre] - [STATUS]
> - Pasos completados: [X]/[Total]
> - Tiempo estimado: [N] min
> - Issues encontrados: [Descripción o "Ninguno"]
> ```

### 🔍 Dry-Run Mode (Opcional)

> **🎯 v2.1:** Validar plan sin ejecutar cambios

Para validar el plan de ejecución sin hacer cambios reales:

```bash
# Activar modo dry-run
export DRY_RUN=true

# El agente mostrará qué haría sin ejecutar
if [ "$DRY_RUN" = "true" ]; then
  echo "🔍 DRY RUN MODE - No changes will be made"
  echo ""
  echo "Would execute:"
  echo "  1. FASE 0: Pre-flight checks"
  echo "  2. FASE 1: Branch setup" 
  echo "  3. FASE 2: [Nombre de la fase]"
  echo "  ..."
  echo ""
  echo "Run without DRY_RUN=true to execute"
  exit 0
fi
```

**Uso recomendado:**
- Validar configuración antes del sprint real
- Debugging de problemas de prerequisitos
- Training de nuevos desarrolladores

---

## 🧭 Plan de Ejecución (Fases)

### 📋 FASE 0: Pre-flight Checks & Environment Verification

**⏱️ Duración estimada:** 10 minutos  
**🎯 Objetivo:** Verificar que el entorno está listo y cumple todos los prerequisitos

**Pasos ejecutables:**

#### 1. Verificar directorio de trabajo

**Bash/Linux/macOS:**
```bash
# Confirmar que estamos en el directorio correcto
pwd
# Debe estar en: C:\Users\Public\ANDAON\ENIS\ENIS\agent-contracts

# Verificar que es un repositorio Git
git rev-parse --git-dir
```

**PowerShell (Windows):**
```powershell
# PS> Confirmar directorio correcto
Get-Location
# Debe estar en: C:\Users\Public\ANDAON\ENIS\ENIS\agent-contracts

# Verificar que es un repositorio Git
git rev-parse --git-dir
# O verificar existencia de .git
Test-Path .git
```

**✅ Criterio de éxito:** Estamos en el directorio correcto del repositorio

---

#### 2. Verificar estado de Git

**Bash/Linux/macOS:**
```bash
# Ver estado actual
git status

# Ver rama actual
git branch --show-current

# Ver últimos commits
git log --oneline -n 5

# Verificar que no hay cambios sin commitear
git diff-index --quiet HEAD -- || echo "⚠️ WARNING: Hay cambios sin commitear"
```

**PowerShell (Windows):**
```powershell
# PS> Ver estado actual
git status

# Ver rama actual
git branch --show-current

# Ver últimos commits
git log --oneline -n 5

# Verificar cambios sin commitear
if (git diff-index --quiet HEAD --) {
  Write-Host "✅ No hay cambios sin commitear" -ForegroundColor Green
} else {
  Write-Host "⚠️ WARNING: Hay cambios sin commitear" -ForegroundColor Yellow
}
```

**✅ Criterio de éxito:** Repositorio en estado limpio, no hay cambios pendientes

#### 3. Verificar herramientas requeridas
```bash
# Configurar error handling
set -euo pipefail
trap 'echo "❌ ERROR at line $LINENO in FASE 0.3"' ERR

# Función robusta para verificar versión mínima
check_version() {
  local tool="$1"
  local current_version="$2"
  local required_major="$3"
  local required_minor="$4"
  local required_patch="${5:-0}"
  
  if ! command -v "$tool" &> /dev/null; then
    log_error "Tool '$tool' not found"
    return 1
  fi
  
  # Extraer componentes de versión
  local major=$(echo "$current_version" | cut -d'.' -f1)
  local minor=$(echo "$current_version" | cut -d'.' -f2)
  local patch=$(echo "$current_version" | cut -d'.' -f3 | sed 's/[^0-9].*//')
  
  # Validar que sean números
  if ! [[ "$major" =~ ^[0-9]+$ ]] || ! [[ "$minor" =~ ^[0-9]+$ ]] || ! [[ "$patch" =~ ^[0-9]+$ ]]; then
    log_error "Tool '$tool' version '$current_version' has invalid format"
    return 1
  fi
  
  # Comparar versiones
  if [ "$major" -lt "$required_major" ] || 
     ([ "$major" -eq "$required_major" ] && [ "$minor" -lt "$required_minor" ]) ||
     ([ "$major" -eq "$required_major" ] && [ "$minor" -eq "$required_minor" ] && [ "$patch" -lt "$required_patch" ]); then
    log_error "Tool '$tool' version $current_version is below required $required_major.$required_minor.$required_patch"
    return 1
  fi
  
  log_success "Tool '$tool' version $current_version meets requirement >= $required_major.$required_minor.$required_patch"
  return 0
}

# Verificar Node.js >= 18.0.0
NODE_VERSION=$(node --version | sed 's/v//')
if ! check_version "node" "$NODE_VERSION" "18" "0" "0"; then
  log_error "Node.js version check failed"
  exit 1
fi

# Verificar Python >= 3.11.0
PYTHON_VERSION=$(python --version | cut -d' ' -f2)
if ! check_version "python" "$PYTHON_VERSION" "3" "11" "0"; then
  log_error "Python version check failed"
  exit 1
fi

# Verificar Git >= 2.30.0
GIT_VERSION=$(git --version | cut -d' ' -f3)
if ! check_version "git" "$GIT_VERSION" "2" "30" "0"; then
  log_error "Git version check failed"
  exit 1
fi

# Verificar herramientas específicas de ENIS
log_info "Validating ENIS-specific tools..."

# Spectral
if command -v npx &> /dev/null; then
  SPECTRAL_VERSION=$(npx @stoplight/spectral-cli --version 2>/dev/null | head -n1 | cut -d' ' -f2 || echo "unknown")
  log_success "Spectral $SPECTRAL_VERSION available"
else
  log_warn "npx not found (required for Spectral)"
fi

# AJV CLI
if command -v npx &> /dev/null; then
  AJV_VERSION=$(npx ajv-cli --version 2>/dev/null || echo "unknown")
  log_success "AJV CLI available"
else
  log_warn "AJV CLI not available via npx"
fi

# Buf
if command -v buf &> /dev/null; then
  BUF_VERSION=$(buf --version | cut -d' ' -f2)
  if check_version "buf" "$BUF_VERSION" "1" "28" "1"; then
    log_success "Buf $BUF_VERSION available"
  else
    log_warn "Buf version $BUF_VERSION below recommended 1.28.1 (continuing...)"
  fi
else
  log_warn "Buf not found (optional for Protocol Buffer validation)"
fi

# Cosign
if command -v cosign &> /dev/null; then
  COSIGN_VERSION=$(cosign version | head -n1 | cut -d' ' -f2)
  log_success "Cosign $COSIGN_VERSION available"
else
  log_warn "Cosign not found (required for baseline signing)"
fi

# Docker (opcional pero recomendado)
if command -v docker &> /dev/null; then
  DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | cut -d',' -f1)
  if check_version "docker" "$DOCKER_VERSION" "20" "10" "0"; then
    log_success "Docker $DOCKER_VERSION available"
  else
    log_warn "Docker version $DOCKER_VERSION below recommended 20.10.0 (continuing...)"
  fi
else
  log_warn "Docker not found (optional for local development)"
fi

# Test 8: Validar error patterns (v2.1 - Nuevo)
log_info "Running error pattern validation tests..."
if run_pattern_tests; then
  log_success "Error pattern tests: PASSED"
else
  log_error "Error pattern tests: FAILED"
  log_warn "Continuing with sprint execution (tests are non-blocking)"
fi

# Generar reporte detallado de validación
cat > PHASE0_ENVIRONMENT_CHECK.md << 'EOF'
# Environment Check Report - Sprint S1

**Date:** $(date)
**Sprint:** S1 - Contracts Core
**Status:** ✅ VALIDATED
**Validation Level:** Comprehensive (v2.1)

## Required Tools (Critical)

EOF

# Agregar herramientas críticas verificadas
echo "- Node.js: $(node --version) ✅ (>= 18.0.0 required)" >> PHASE0_ENVIRONMENT_CHECK.md
echo "- Python: $(python --version) ✅ (>= 3.11.0 required)" >> PHASE0_ENVIRONMENT_CHECK.md
echo "- Git: $(git --version) ✅ (>= 2.30.0 required)" >> PHASE0_ENVIRONMENT_CHECK.md

cat >> PHASE0_ENVIRONMENT_CHECK.md << 'EOF'

## Optional Tools (Recommended)

EOF

# Agregar herramientas opcionales
if command -v npx &> /dev/null; then
  echo "- Spectral: Available via npx ✅" >> PHASE0_ENVIRONMENT_CHECK.md
else
  echo "- Spectral: Not available ⚠️ (critical for contract validation)" >> PHASE0_ENVIRONMENT_CHECK.md
fi

if command -v npx &> /dev/null; then
  echo "- AJV CLI: Available via npx ✅" >> PHASE0_ENVIRONMENT_CHECK.md
else
  echo "- AJV CLI: Not available ⚠️ (critical for schema validation)" >> PHASE0_ENVIRONMENT_CHECK.md
fi

if command -v buf &> /dev/null; then
  echo "- Buf: $(buf --version) ✅" >> PHASE0_ENVIRONMENT_CHECK.md
else
  echo "- Buf: Not found ⚠️ (optional for proto validation)" >> PHASE0_ENVIRONMENT_CHECK.md
fi

if command -v cosign &> /dev/null; then
  echo "- Cosign: $(cosign version | head -n1) ✅" >> PHASE0_ENVIRONMENT_CHECK.md
else
  echo "- Cosign: Not found ⚠️ (required for baseline signing)" >> PHASE0_ENVIRONMENT_CHECK.md
fi

if command -v docker &> /dev/null; then
  echo "- Docker: $(docker --version) ✅" >> PHASE0_ENVIRONMENT_CHECK.md
else
  echo "- Docker: Not found ⚠️ (optional)" >> PHASE0_ENVIRONMENT_CHECK.md
fi

cat >> PHASE0_ENVIRONMENT_CHECK.md << 'EOF'

## Validation Summary

### Critical Requirements
- ✅ Node.js >= 18.0.0: PASSED
- ✅ Python >= 3.11.0: PASSED  
- ✅ Git >= 2.30.0: PASSED

### Optional Recommendations
- [ ] Spectral CLI: [Status]
- [ ] AJV CLI: [Status]
- [ ] Buf >= 1.28.1: [Status]
- [ ] Cosign >= 2.2.x: [Status]
- [ ] Docker >= 20.10.0: [Status]

### Environment Status
- ✅ All critical tools available
- ✅ All version requirements met
- ✅ Environment ready for sprint execution
- ⚠️ [Optional tools status]

## Next Steps

1. Proceed to FASE 1: Branch Setup
2. Verify cross-repository dependencies
3. Begin sprint implementation

## Troubleshooting

If validation failed:
1. Install missing tools using package manager
2. Update tools to required versions
3. Re-run FASE 0 validation
4. Contact platform team if issues persist

EOF

log_success "Environment validation completed successfully"
log_info "Report generated: PHASE0_ENVIRONMENT_CHECK.md"
```

**✅ Criterio de éxito:** Todas las herramientas instaladas con versiones correctas

#### 4. Verificar prerequisitos de sprints anteriores
```bash
# Verificar que develop está actualizado
git fetch origin develop
git log HEAD..origin/develop --oneline

# Verificar archivos/directorios esperados del sprint anterior
test -d openapi && echo "✅ openapi/ exists" || echo "❌ openapi/ missing"
test -d schemas && echo "✅ schemas/ exists" || echo "❌ schemas/ missing"
test -d proto && echo "✅ proto/ exists" || echo "❌ proto/ missing"

# Listar archivos existentes relevantes
echo "" >> PHASE0_ENVIRONMENT_CHECK.md
echo "## Existing Files Check" >> PHASE0_ENVIRONMENT_CHECK.md
ls -la . >> PHASE0_ENVIRONMENT_CHECK.md
```

**✅ Criterio de éxito:** Todos los prerequisitos del sprint anterior están presentes

#### 5. Mostrar resumen de Pre-flight
```bash
cat PHASE0_ENVIRONMENT_CHECK.md

echo ""
echo "✅ =========================================="
echo "✅  PHASE 0: PRE-FLIGHT CHECKS COMPLETE"
echo "✅ =========================================="
echo ""
echo "📁 Working directory: $(pwd)"
echo "🔀 Current branch: $(git branch --show-current)"
echo "🛠️  All tools: VERIFIED"
echo "📋 Prerequisites: CHECKED"
echo ""
echo "🚀 Ready to proceed with Phase 1"
echo ""
```

**✅ Criterios de éxito globales de FASE 0:**
- [ ] Directorio correcto confirmado
- [ ] Git status limpio
- [ ] Todas las herramientas disponibles
- [ ] Prerequisites del sprint anterior verificados
- [ ] Reporte PHASE0_ENVIRONMENT_CHECK.md generado

---

### 🌱 FASE 1 — Rama & scaffolding (10 min)
**Objetivo:** Crear rama y placeholders mínimos.

**Pasos:**
1) `git switch -c feature/s1-contracts-core`
2) Crear archivos vacíos para OpenAPI/Schema/Proto listados en Entregables
3) Añadir encabezados/boilerplate (OpenAPI 3.0.3, JSON Schema 2020-12, buf package)

**Éxito:** Árbol de archivos creado, build CI verde con placeholders.

---

### 📜 FASE 2 — OpenAPI: Inference (sync/stream) (60–90 min)
**Objetivo:** Especificar endpoints críticos de Inference.

**Alcance mínimo:**
- `POST /v1/inference` (sync) — prompt/inputs, selección de modelo, parámetros, límites
- `POST /v1/inference/stream` (SSE o WS) — **Streaming chunks** con esquema canónico
- `GET /v1/models` — listado con metadatos (capabilities, context_window, pricing hints)

**Componentes requeridos:**
- `components.schemas.InferenceRequest` y `InferenceResponse`
- **`components.schemas.StreamChunk`** con: `id` (string, ulid), `index` (integer), `delta` (string), `finish_reason` (enum: `stop|length|error`)

**Ejemplos obligatorios:**
- `200` sync y **SSE** (`text/event-stream`) con ejemplo de 2–3 eventos (data: JSON encoded chunk)
- **Errores** (4xx/5xx) con `error.code`, `error.message`, `trace_id`

**Resolución de $ref a Schemas:** usar rutas relativas correctas desde `openapi/v1/` a `schemas/`, p. ej.:  
`$ref: '../../schemas/inference-request.json'`

**Comandos:**
```bash
npx spectral lint openapi/v1/inference*.yaml -r .spectral.yaml --fail-severity warn
```
**Éxito:** Lint 0 errores; ejemplos incl. stream chunk y error body.

---

### 👥 FASE 3 — OpenAPI: Agents (45–60 min)
**Objetivo:** Contratos para lifecycle y capacidades de agentes.

**Alcance mínimo:**
- `POST /v1/agents/register` — metadata, scopes, capabilities
- `POST /v1/agents/heartbeat` — estado/telemetría mínima
- `GET /v1/agents/{agent_id}` — detalle
- `POST /v1/agents/{agent_id}/capabilities:grant|revoke`

**Comandos:** `npx spectral lint openapi/v1/agents.yaml`
**Éxito:** Lint OK + ejemplos request/response.

---

### 📣 FASE 4 — OpenAPI: Events (30–45 min)
**Objetivo:** Contrato de publicación/consumo de eventos (estilo CloudEvents).

**Alcance mínimo:**
- `POST /v1/events/publish` — envelope estándar (`id`, `source`, `type`, `specversion`, `time`, `data`)
- `GET /v1/events/types` — catálogo canónico

**Comandos:** `npx spectral lint openapi/v1/events.yaml`
**Éxito:** Lint OK + ejemplos para 2–3 tipos de evento.

---

### 🛡️ FASE 5 — OpenAPI: NOPS (30–45 min)
**Objetivo:** Contratos mínimos para policy/rate limits y health.

**Alcance mínimo:**
- `GET /v1/nops/health` — estado
- `POST /v1/nops/policies/evaluate` — entrada (subject, resource, action, context) → decisión (allow/deny, reason)

**Comandos:** `npx spectral lint openapi/v1/nops.yaml`
**Éxito:** Lint OK con ejemplos de decisiones allow/deny.

---

### 📐 FASE 6 — JSON Schemas (60 min)
**Objetivo:** Definir esquemas canónicos referenciados desde OpenAPI.

**Alcance mínimo:**
- `agent-registration.json` (id, name, kind, scopes, capabilities)
- `inference-request.json` (input, model, params, tenant)
- `event-schema.json` (envelope + `data` as `$defs` por tipo)
- `policy-schema.json` (ABAC claims / resource patterns)

**Comandos:**
```bash
npx ajv compile -s schemas/*.json --strict=true
npx ajv validate -s schemas/*.json
```
**Éxito:** compile/validate sin errores; `$id` y `$schema` presentes.

---

### 🔷 FASE 7 — Protobuf (45–60 min)
**Objetivo:** Protos espejo de OpenAPI para gRPC/streaming.

**Alcance mínimo:**
- `inference.proto`: `rpc Predict(PredictRequest) returns (PredictResponse)` y `rpc StreamPredict(PredictRequest) returns (stream PredictChunk)`
- `agents.proto`: registro, heartbeat, capabilities
- `events.proto`: `PublishEvent` y tipos
- `federation.proto`: extensiones multi-tenant (placeholders)

**Comandos:**
```bash
buf lint proto/
buf format --diff --exit-code
```
**Éxito:** lint/format OK; `package enis.agentcontracts.v1` consistente.

---

### 🧭 FASE 8 — Catálogo de Errores (60 min)
**Objetivo:** Publicar `docs/01-sprint/S1/errors.md` con taxonomía y mapeo.

**Contenido mínimo:**
- Formato: `AC-XXXX` (p. ej. `AC-0001 INVALID_ARGUMENT`, `AC-0403 PERMISSION_DENIED`, `AC-0504 RATE_LIMITED`)
- Mapeo: HTTP status + `error.code`, `error.message`, `error.details`
- Sección de **cómo versionar errores** y política de compatibilidad

**Éxito:** documento listo con tabla de errores comunes y ejemplos.

---

### 🧭 FASE 9 — CONTRACTS-GUIDE (45 min)
**Objetivo:** `docs/01-sprint/S1/CONTRACTS-GUIDE.md` con **principios de diseño**.

**Puntos mínimos:**
- Naming, versionado (`/v1`), **idempotencia**, **id** canónicos (ULID), **pagination** estándar
- **Errores**: estructura uniforme, `trace_id`, `correlation_id`
- **Compatibilidad**: reglas de **non-breaking** (añadir campos opcionales),
- Guía de ejemplos: request/response realistas

**Éxito:** guía validada por Arquitectura.

---

### 🔁 FASE 10 — CHANGE-POLICY (45 min)
**Objetivo:** `docs/01-sprint/S1/CHANGE-POLICY.md` con **FREEZE / Deprecation / Emergency RFC**.

**Puntos mínimos:**
- **FREEZE** de contratos tras S1 (solo adiciones compatibles)
- Ventana de **Deprecation** y señalización en OpenAPI (`deprecated: true`)
- Flujo **Emergency RFC** (aprobación rápida, etiqueta, comunicado)

**Éxito:** política aprobada por Governance.

---

### 🧪 FASE 11 — Tests & Mocks (60–90 min)
**Objetivo:** asegurar validación y ejemplos ejecutables.

**Pasos:**
- Unit: `tests/contracts/test_openapi_contract.py` (carga OpenAPI + invariantes)
- Schema: `tests/contracts/test_schema_validation.py` (AJV via subprocess o jsonschema)
- Pact: `tests/pact/test_pact_consumer.py` (esqueleto + publish si hay broker)
- Mocks: actualizar `docker-compose.mocks.yml` con nuevas rutas y healthchecks

**Éxito:** `pytest -q` OK; mocks responden a `/v1/inference` y `/v1/nops/health`.

---

### 🔗 FASE 12 — CI/CD Gates (30–45 min)
**Objetivo:** extender workflows para cubrir nuevos contratos y **firmar baseline**.

**Pasos:**
- `contracts-validate.yml`: incluir `openapi/v1/*`, `schemas/*.json`, `proto/*` y usar `.spectral.yaml`
- `contracts-breaking.yml`: `oasdiff breaking` (contra baseline/snapshot) y `buf breaking`
- `examples-smoke.yml`: probar Prism/WireMock con curl básico
- `contracts-baseline.yml`: **generar baseline y firmarlo** con Cosign (`COSIGN_KEY`)

**Ejemplo (step Cosign):**
```yaml
- name: Compute & Sign baseline
  run: |
    python3 scripts/baseline/compute-baseline.py --write
    echo "$COSIGN_KEY" > cosign.key
    cosign sign-blob --key cosign.key --output-signature baseline.sig openapi/v1/.baseline/inference.yaml
```

**Éxito:** pipelines verdes; gates activos en PR; baseline firmado disponible como artefacto.

---

### 📋 FASE 12.5: Rollback Plan & Safety Verification

> **🎯 Novedad v2.0:** Plan de reversión antes del merge

**⏱️ Duración estimada:** 5 minutos  
**🎯 Objetivo:** Preparar procedimiento de rollback en caso de issues post-merge

**Pasos ejecutables:**

#### 1. Documentar estado pre-sprint
```bash
# Guardar hash del último commit de develop antes del sprint
git fetch origin
git rev-parse origin/develop > ROLLBACK_INFO.txt
echo "Sprint: S1" >> ROLLBACK_INFO.txt
echo "Branch: feature/s1-contracts-core" >> ROLLBACK_INFO.txt
echo "Date: $(date -Iseconds)" >> ROLLBACK_INFO.txt
echo "Author: $(git config user.name)" >> ROLLBACK_INFO.txt
```

#### 2. Crear script de rollback
```bash
cat > rollback-s1.sh << 'EOF'
#!/usr/bin/env bash
# Rollback script for Sprint S1
set -euo pipefail

echo "🔄 Rolling back Sprint S1..."
echo "⚠️  This will revert changes from this sprint"
read -p "Continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
  echo "Aborted."
  exit 1
fi

# Opción 1: Revert merge commit (si ya está merged)
# git revert -m 1 <merge-commit-hash>

# Opción 2: Restaurar baseline de contratos (si aplica)
if [ -d "openapi/v1/.baseline" ]; then
  echo "Restaurando baseline de contratos..."
  cp openapi/v1/.baseline/*.yaml openapi/v1/ 2>/dev/null || true
fi

# Opción 3: Rollback de migraciones de BD (si aplica)
# python manage.py migrate [app] [previous_migration]

# Opción 4: Restaurar configuración (si aplica)
# git restore --source=HEAD~1 config/

# Opción 5: Limpiar artefactos generados del sprint
log_info "🧹 Cleaning up sprint artifacts..."
rm -f S1_*.md PR_*.md ROLLBACK_INFO.txt 2>/dev/null || true

# Limpiar branches locales huérfanas
log_info "🧹 Cleaning up orphaned branches..."
git branch -D feature/s1-* 2>/dev/null || true

# Limpiar build artifacts
log_info "🧹 Cleaning up build artifacts..."
rm -rf dist/ build/ node_modules/.cache/ .pytest_cache/ __pycache__/ 2>/dev/null || true

# Limpiar archivos temporales
log_info "🧹 Cleaning up temporary files..."
rm -f /tmp/sprint-*.tmp .sprint-checkpoint 2>/dev/null || true

# Limpiar logs antiguos
log_info "🧹 Cleaning up old logs..."
rm -f sprint-s1.log 2>/dev/null || true

log_success "✅ Rollback and cleanup completed"
echo "⚠️  Verificar manualmente que todo funciona correctamente"
EOF

chmod +x rollback-s1.sh
```

**PowerShell (Windows):**
```powershell
# PS> Equivalente del rollback script
@'
# Rollback script for Sprint S1 (PowerShell)
Write-Host "🔄 Rolling back Sprint S1..." -ForegroundColor Yellow

$confirm = Read-Host "Continue? (yes/no)"
if ($confirm -ne "yes") {
  Write-Host "Aborted." -ForegroundColor Red
  exit 1
}

# Restaurar baseline si aplica
if (Test-Path "openapi/v1/.baseline") {
  Write-Host "Restaurando baseline..."
  Copy-Item "openapi/v1/.baseline/*.yaml" "openapi/v1/" -Force
}

# Limpiar artefactos
Remove-Item "S1_*.md", "PR_*.md", "ROLLBACK_INFO.txt" -ErrorAction SilentlyContinue

Write-Host "✅ Rollback completado" -ForegroundColor Green
'@ | Out-File -FilePath rollback-s1.ps1 -Encoding UTF8
```

#### 3. Verificar reversibilidad (Checklist manual)
```bash
echo ""
echo "⚠️  VERIFICACIÓN DE REVERSIBILIDAD"
echo "=================================="
echo ""
echo "Confirmar manualmente estos puntos ANTES de merge:"
echo ""
echo "  [ ] No hay migraciones de BD sin procedimiento de rollback"
echo "  [ ] No hay datos eliminados permanentemente sin backup"
echo "  [ ] Cambios de config son reversibles"
echo "  [ ] Baseline guardado correctamente (si aplica)"
echo "  [ ] No hay cambios destructivos en esquemas/contratos"
echo "  [ ] Dependencias versionadas (no latest/floating)"
echo "  [ ] Rollback script probado en entorno de test"
echo ""
echo "Guardar esta verificación:"
cat >> ROLLBACK_INFO.txt << 'VERIFY'

## Reversibility Checklist
- [ ] DB migrations reversible
- [ ] No permanent data deletion
- [ ] Config changes reversible
- [ ] Baseline saved
- [ ] No breaking contract changes
- [ ] Dependencies pinned
- [ ] Rollback tested

VERIFY
```

#### 4. Documentar cambios críticos
```bash
cat >> ROLLBACK_INFO.txt << 'CRITICAL'

## Critical Changes (Require Special Attention)
- Contract baseline signing: Procedimiento de rollback específico para Cosign
- OpenAPI schema changes: Verificar compatibilidad con servicios dependientes
- Error code changes: Actualizar documentación de códigos de error

## Contacts for Emergency Rollback
- On-call: [PagerDuty link / phone]
- Platform Team: @platform-team (Slack)
- Sprint Owner: Contract Architect

CRITICAL

echo "✅ ROLLBACK_INFO.txt actualizado con cambios críticos"
```

#### 5. Crear backup de estado actual (opcional pero recomendado)
```bash
# Crear backup de archivos críticos
mkdir -p .backup-s1
cp -r openapi/ .backup-s1/openapi/ 2>/dev/null || true
cp -r schemas/ .backup-s1/schemas/ 2>/dev/null || true
cp -r proto/ .backup-s1/proto/ 2>/dev/null || true
tar -czf backup-s1-$(date +%Y%m%d-%H%M%S).tar.gz .backup-s1/

echo "✅ Backup creado: backup-s1-*.tar.gz"
```

**✅ Criterios de éxito globales de FASE 12.5:**
- [ ] ROLLBACK_INFO.txt creado con hash de develop
- [ ] rollback-s1.sh ejecutable y documentado
- [ ] Checklist de reversibilidad completado
- [ ] Cambios críticos documentados
- [ ] Backup creado (opcional)
- [ ] Script de rollback probado en local (recomendado)

---

### 🚀 FASE 13 — Smoke & Reportes (30–45 min)
**Objetivo:** smoke local + reportes estándar.

**Comandos:**
```bash
docker compose -f docker-compose.mocks.yml up -d --build
curl -s localhost:4010 -I || true
pytest -q
```
**Reportes:**
- `S1_SPRINT_TRACKING.md`, `S1_COMPLETION_REPORT.md`, `PR_CHECKLIST.md`, `PR_DESCRIPTION.md`, `ROLLBACK_INFO.txt`

**Éxito:** todos los checks OK y reportes generados.

---

## 📊 Definition of Done - Cuantificable (DoD)

> **🎯 Novedad v2.0:** DoD con métricas verificables y scoring automático

**Cumplimiento Target:** **15 / 15 = 100%** ✅

### Ejemplo de Categorización:

**Infrastructure (3/3)**
1. Spectral/AJV/Buf validation healthy — ✅✅ 100%  
2. CI pipelines configurados — ✅✅ 100%  
3. Baseline firmado con Cosign — ✅✅ 100%  

**Core Features (6/6)**
4. OpenAPI contracts completos — ✅✅ 100%  
5. JSON Schema validados — ✅✅ 100%  
6. Protocol Buffers compilando — ✅✅ 100%  
7. Error catalog publicado — ✅✅ 100%  
8. Contracts guide completo — ✅✅ 100%  
9. Change policy definida — ✅✅ 100%  

**Testing & CI (3/3)**
10. 12 tests implementados — ✅✅ 100%  
11. Coverage ≥ 85% — ✅✅ objetivo  
12. CI verde — ✅✅ 100%  
13. Integration tests — ✅✅ 100%  

**Documentation (2/2)**
14. HOWTO actualizado — ✅✅ 100%  
15. README actualizado — ✅✅ 100%  

**Monitoring & Operations (1/1)**
16. Mocks Prism/WireMock healthy — ✅✅ 100%  

> **⚠️ Crítico:** Todos los items son **bloqueantes** para merge a main

### Scoring Guide

- ✅✅ **100%** - Completo y validado
- ✅⚠️ **80-99%** - Completo con issues menores
- ⚠️ **50-79%** - Parcial, requiere trabajo
- ❌ **0-49%** - No implementado o bloqueado

### Métricas de Éxito

| Métrica | Target | Actual | Status |
|---------|--------|--------|--------|
| **Archivos creados** | 15 | 15 | ✅ |
| **Tests implementados** | 12 | 12 | ✅ |
| **Coverage** | ≥85% | 85%+ | ✅ |
| **CI Pipeline** | < 5 min | < 5 min | ✅ |
| **LOC añadidas** | ~2500 | ~2500 | ℹ️ |

---

## 📊 Execution Summary

Al finalizar todas las fases, el agente AI debe haber:

### ✅ Estructura y Archivos
- [ ] 15 archivos/directorios creados
- [ ] 8 archivos modificados
- [ ] Toda la estructura según especificación

### ✅ Validación y Testing
- [ ] Tests unitarios pasando
- [ ] Validaciones de contratos exitosas
- [ ] Smoke tests completados
- [ ] CI/CD workflows configurados

### ✅ Documentación
- [ ] README actualizado
- [ ] Guías técnicas escritas
- [ ] Ejemplos incluidos
- [ ] Reportes generados

### ✅ Git y PR
- [ ] Cambios commiteados con mensaje descriptivo
- [ ] Branch pusheado a origin
- [ ] PR checklist completo
- [ ] PR description lista

### ✅ Definition of Done
- [ ] Todos los contratos completos
- [ ] Validaciones sin errores
- [ ] Documentación completa
- [ ] Tests con cobertura objetivo
- [ ] Baseline firmado
- [ ] Todos los criterios del sprint cumplidos

---

## ⚠️ Notas Importantes para el Agente AI

### 🎯 Ejecución

1. **Orden secuencial obligatorio**
   - Ejecutar las fases en orden estricto
   - No saltar pasos a menos que estén marcados como opcionales
   - Verificar éxito de cada paso antes de continuar

2. **Verificación continua**
   - Después de cada fase, ejecutar verificaciones
   - Documentar el estado en el tracking file
   - Si algo falla, evaluar criticidad antes de continuar

3. **Manejo de errores**
   - **Error crítico** (ej: Git no disponible, prerequisitos faltantes)
     → Detener ejecución y reportar
   - **Error no crítico** (ej: warning de linter, herramienta opcional)
     → Documentar, continuar, reportar al final
   - **Error recuperable** (ej: archivo ya existe)
     → Intentar solución automática, documentar

4. **Reportes y documentación**
   - Actualizar `S1_SPRINT_TRACKING.md` al completar cada fase
   - Documentar issues en el tracking file
   - Generar reportes completos en FASE final
   - No eliminar archivos de reporte

### 🔧 Consideraciones Técnicas

5. **Paths y plataformas**
   - Usar paths relativos cuando sea posible
   - En Windows PowerShell: algunos comandos bash no funcionan
     → Adaptar o documentar alternativas
   - `chmod +x` no funciona en Windows
     → Documentar pero no fallar

6. **Comandos de shell**
   - Preferir comandos multiplataforma cuando sea posible
   - Usar `&&` para encadenar comandos críticos
   - Usar `||` para fallbacks no críticos
   - Escapar variables: usar `"${VAR}"` no `$VAR`

7. **Archivos existentes**
   - Verificar si archivo existe antes de crearlo
   - No sobrescribir archivos importantes sin avisar
   - Hacer backup si se va a modificar archivo crítico

8. **Herramientas opcionales**
   - Algunas herramientas pueden no estar disponibles
   - Documentar si falta algo no crítico
   - Solo fallar si es herramienta crítica para el sprint

### 📋 Formato de Reportes

9. **Status reporting**
   - Al completar cada fase, reportar:
     ```
     FASE [N]: [Nombre] - ✅ COMPLETED
     - Steps completed: [X]/[Y]
     - Time taken: ~[N] minutes
     - Issues: [None / List]
     - Next: FASE [N+1]
     ```

10. **Final report requirements**
    - Debe incluir:
      - Summary ejecutivo
      - Lista completa de archivos cambiados
      - Estadísticas (files, lines, commits)
      - DoD verification
      - Issues log
      - Next steps
      - Artifacts list

### 🎨 Estilo y Convenciones

11. **Código y commits**
    - Seguir estándares del proyecto (.cursorrules)
    - Usar Conventional Commits
    - Escribir en español (según .cursorrules)
    - Incluir emojis donde sea apropiado para legibilidad

12. **Documentación**
    - Escribir en español
    - Usar markdown correctamente
    - Incluir ejemplos de código
    - Cross-referenciar archivos relacionados

---

## 🔗 Referencias y Links

### Documentación del Proyecto
- [Roadmap General](../roadmaps/agent_contracts_roadmap_2025_2026_detallado.md)
- [Sprint Anterior: S0](../S0/S0 — Kickoff & Repo Bootstrap.md)
- [Sprint Siguiente: S2](../S2/)

### Especificaciones Técnicas
- [Master Prompt de Arquitectura](../../00-enis-complete/05-repositorios-enis/shared/agent-contracts/02-architecture-master-prompt.md)
- [DNA v3.0 Specification](../../00-enis-complete/DNA_V3_SPECIFICATION.md)
- [ENIS Architecture](../../00-enis-complete/ENIS_COMPLETE_ARCHITECTURE_REPORT.md)

### Guías y Estándares
- [Contract Design Guide](../S1/CONTRACTS-GUIDE.md)
- [Change Policy](../S1/CHANGE-POLICY.md)
- [Security Guidelines](../S6/SECURITY_ARCHITECTURE.md)
- [Testing Standards](../S7/TESTING_STANDARDS.md)

### Herramientas
- [Spectral Rules](.spectral.yml)
- [AJV Configuration](ajv.config.js)
- [Buf Configuration](buf.yaml)

---

## 📞 Contactos y Soporte

### Owners del Sprint
- **Contract Architect**: Design & Approval - [contacto]
- **Platform Engineer**: Tooling & CI - [contacto]

### Reviewers Sugeridos
- **Arquitectura**: @architecture-team
- **Contratos**: @contracts-team
- **Seguridad**: @security-team
- **Platform**: @platform-team

### Canales de Comunicación
- **Slack**: #contracts-rfcs
- **Meetings**: [Link a calendar]
- **Docs**: [Link a Confluence/Notion]

---

## 🎓 Apéndice: Comandos Útiles

### Git
```bash
# Ver diferencias con develop (symmetric diff con remote)
git diff origin/develop...HEAD

# Ver archivos modificados
git diff --name-only origin/develop...HEAD

# Ver estadísticas
git diff --stat origin/develop...HEAD

# Crear commit amend
git commit --amend --no-edit

# Ver log gráfico
git log --graph --oneline --all -n 20
```

### Validación
```bash
# Validar OpenAPI
npx @stoplight/spectral-cli lint openapi/**/*.yaml

# Validar JSON Schema
npx ajv-cli validate -s schemas/*.json

# Validar Proto
buf lint proto/

# Validar YAML
python -c "import yaml; yaml.safe_load(open('file.yaml'))"

# Validar JSON
jq . file.json
```

### Testing
```bash
# Run all tests with timeout
timeout 300 npm test

# Run specific test with timeout
timeout 300 npm test -- --grep "test name"

# Run with coverage and timeout
timeout 300 npm run test:coverage

# Run linter with timeout
timeout 60 npm run lint

# Fix linter issues with timeout
timeout 60 npm run lint:fix

# Python tests with timeout
timeout 300 pytest tests/ -v

# Go tests with timeout
timeout 300 go test ./...
```

### Docker
```bash
# Build image
docker build -t enis/agent-contracts:s1 .

# Run container
docker run -it enis/agent-contracts:s1

# Docker compose up
docker compose up -d

# Docker compose down
docker compose down

# View logs
docker compose logs -f
```

---

**Última actualización:** 2025-01-27  
**Versión de plantilla:** 2.2 Complete  
**Mantenedor:** Platform Engineering Team  
**License:** Proprietary - ANDAON SA DE CV

---

## 🤖 Instrucción Final para Claude Code CLI

```
Para ejecutar este sprint:

1. Lee este documento completo primero
2. Verifica que entiendes cada fase
3. Ejecuta: FASE 0 → FASE 1 → ... → FASE 13
4. Reporta el progreso después de cada fase
5. Genera todos los reportes en la fase final
6. No te detengas hasta completar o encontrar un blocker crítico

Comando de inicio sugerido:
"Claude, ejecuta el Sprint S1 siguiendo el documento 
docs/01-sprint/S1/sprint_s1 Contracts Core.md paso por paso. 
Reporta el progreso de cada fase."
```

---

## ✅ Definition of Done (DoD)
- OpenAPI/JSON Schema/Proto **completos** para Inference/Agents/Events/NOPS
- Lint/validate/format **sin errores** (Spectral/AJV/Buf)
- `errors.md`, `CONTRACTS-GUIDE.md`, `CHANGE-POLICY.md` publicados bajo `\docs\01-sprint\S1\`
- Mocks Prism/WireMock actualizados y **healthy**
- CI con gates activos y PR listo con checklist
- **Baseline generado y firmado con Cosign** (artefactos: `baseline.*`)

---

## ⚠️ Riesgos & Mitigación
- **Deriva de contratos** → Gate `oasdiff` + revisión Arquitectura
- **Inconsistencia entre OpenAPI/Proto** → tabla de equivalencia en `CONTRACTS-GUIDE.md`
- **Errores no estandarizados** → `errors.md` como **fuente de verdad**

---

## 👥 Owners y Canales
- **Contract Architect** (design/approval)
- **Platform Engineer** (tooling/CI/mocks)
- Slack: `#contracts-rfcs` — Revisión/consenso

---

## 📎 Anexos (snippets útiles)
**OpenAPI header (plantilla)**
```yaml
openapi: 3.0.3
info:
  title: ENIS [Service] API
  version: 1.0.0
servers:
  - url: https://api.enis.ai
paths: {}
components:
  schemas: {}
```

**JSON Schema header (2020-12)**
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://enis.ai/schemas/[name].json",
  "type": "object",
  "properties": {}
}
```

**buf.yaml (esqueleto)**
```yaml
version: v1
breaking:
  use:
    - FILE
lint:
  use:
    - DEFAULT
```

**$ref correcto desde OpenAPI → Schemas**
```yaml
# Dentro de openapi/v1/inference.yaml
components:
  schemas:
    InferenceRequest:
      $ref: '../../schemas/inference-request.json'
```

**StreamChunk (SSE) — esquema sugerido**
```yaml
components:
  schemas:
    StreamChunk:
      type: object
      required: [id, index, delta]
      properties:
        id: { type: string, description: 'ulid' }
        index: { type: integer, minimum: 0 }
        delta: { type: string }
        finish_reason: { type: string, enum: [stop, length, error] }
```

**.spectral.yaml — regla de examples obligatorios (ejemplo)**
```yaml
rules:
  oas3-examples-required:
    description: Each operation MUST provide at least one example
    given: $.paths[*][*]
    severity: warn
    then:
      field: responses
      function: truthy
```

