# S[N] — [Sprint Name] ⏸️ **[STATUS]**

> **🤖 DOCUMENTO OPTIMIZADO PARA CLAUDE CODE CLI v2.2**  
> Este documento contiene instrucciones ejecutables paso a paso  
> **Version:** 2.2 Complete (incluye DoD cuantificable, QA interno, ADRs, SLOs, Rollback, Cross-repo deps, PowerShell parity, Error pattern tests)
> 
> **AI Agent Role:** [Staff Backend Engineer / Platform Engineer / Contract Architect]
> 
> **Repo:** `[repository-name]`  
> **Branch:** `feature/s[n]-[branch-suffix]` (base: `develop`)  
> **Duración estimada:** [N] semanas  
> **Owners:** [Owner 1] + [Owner 2]  
> **KICKOFF_DATE:** YYYY-MM-DD  
> **END_DATE:** YYYY-MM-DD
> 
> **📋 Alineación con Roadmap:**  
> `docs/01-sprint/roadmaps/agent_contracts_roadmap_2025_2026_detallado.md` - Sprint S[N]

---

## 🛡️ Error Handling Best Practices

> **🎯 CRÍTICO v2.1:** Scripts robustos con manejo de errores completo

### Script Header Estándar
```bash
#!/usr/bin/env bash
# Script: [Nombre del script]
# Sprint: S[N] - [Sprint Name]
# Author: [Author]
# Date: $(date)

# Error handling robusto
set -euo pipefail
trap 'echo "❌ ERROR at line $LINENO in $0"' ERR

# Logging functions with structured output
LOG_FILE="sprint-s[n].log"

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

# Pattern 10: PowerShell test suite equivalente (v2.1)
# Función para ejecutar tests en PowerShell
Test-ErrorPatterns() {
  Write-Info "Running error pattern validation tests (PowerShell)..."
  
  # Test 1: Validación de funciones de logging
  Write-Info "Testing logging functions..."
  try {
    Write-Info "Test info message"
    Write-Success "Test success message"
    Write-Warn "Test warning message"
    Write-Success "Logging functions test: PASSED"
  }
  catch {
    Write-Error "Logging functions test: FAILED - $_"
    return $false
  }
  
  # Test 2: Validación de funciones de validación
  Write-Info "Testing validation functions..."
  try {
    Test-Command "Get-Command"
    Test-File "C:\Windows\System32\notepad.exe"
    Test-Directory "C:\Windows"
    Write-Success "Validation functions test: PASSED"
  }
  catch {
    Write-Error "Validation functions test: FAILED - $_"
    return $false
  }
  
  # Test 3: Validación de retry pattern
  Write-Info "Testing retry pattern..."
  $script:retryAttempts = 0
  $retryTest = {
    $script:retryAttempts++
    if ($script:retryAttempts -eq 2) {
      return $true
    }
    return $false
  }
  
  if (Invoke-RetryWithBackoff $retryTest) {
    Write-Success "Retry pattern test: PASSED"
  } else {
    Write-Error "Retry pattern test: FAILED"
    return $false
  }
  
  # Test 4: Validación de timeout pattern
  Write-Info "Testing timeout pattern..."
  $timeoutTest = { Write-Output "timeout test" }
  if (Invoke-WithTimeout 2 $timeoutTest "Timeout test") {
    Write-Success "Timeout pattern test: PASSED"
  } else {
    Write-Error "Timeout pattern test: FAILED"
    return $false
  }
  
  # Test 5: Validación de idempotencia
  Write-Info "Testing idempotent patterns..."
  $testFile = "C:\temp\test-idempotent.txt"
  $testDir = "C:\temp\test-idempotent-dir"
  
  try {
    New-IdempotentFile $testFile "test content" "Test file"
    New-IdempotentDirectory $testDir "Test directory"
    
    if ((Test-Path $testFile) -and (Test-Path $testDir)) {
      Write-Success "Idempotent patterns test: PASSED"
    } else {
      Write-Error "Idempotent patterns test: FAILED"
      return $false
    }
  }
  finally {
    Remove-Item $testFile -ErrorAction SilentlyContinue
    Remove-Item $testDir -ErrorAction SilentlyContinue
  }
  
  # Test 6: Validación de checkpoint system
  Write-Info "Testing checkpoint system..."
  Save-Checkpoint "5"
  $loadedCheckpoint = Get-Checkpoint
  if ($loadedCheckpoint -eq "5") {
    Write-Success "Checkpoint system test: PASSED"
  } else {
    Write-Error "Checkpoint system test: FAILED"
    return $false
  }
  
  # Test 7: Validación de parallel execution
  Write-Info "Testing parallel execution..."
  $parallelTask1 = { Start-Sleep 0.1; Write-Output "task1 completed" }
  $parallelTask2 = { Start-Sleep 0.1; Write-Output "task2 completed" }
  
  if (Invoke-Parallel $parallelTask1 $parallelTask2 "Parallel Task 1" "Parallel Task 2") {
    Write-Success "Parallel execution test: PASSED"
  } else {
    Write-Error "Parallel execution test: FAILED"
    return $false
  }
  
  Write-Success "All error pattern tests completed successfully (PowerShell)"
  return $true
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
    Add-Content -Path "sprint-s[n].log" -Value $logMessage
}

function Write-Warn {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [WARN] $Message"
    Write-Host "⚠️  WARN: $Message" -ForegroundColor Yellow
    Add-Content -Path "sprint-s[n].log" -Value $logMessage
}

function Write-Error {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [ERROR] $Message"
    Write-Host "❌ ERROR: $Message" -ForegroundColor Red
    Add-Content -Path "sprint-s[n].log" -Value $logMessage
}

function Write-Success {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [SUCCESS] $Message"
    Write-Host "✅ SUCCESS: $Message" -ForegroundColor Green
    Add-Content -Path "sprint-s[n].log" -Value $logMessage
}

function Write-Debug {
    param([string]$Message)
    if ($env:DEBUG -eq "true") {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        $logMessage = "[$timestamp] [DEBUG] $Message"
        Write-Host "🔍 DEBUG: $Message" -ForegroundColor Magenta
        Add-Content -Path "sprint-s[n].log" -Value $logMessage
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
    "number": "[N]",
    "name": "[Sprint Name]",
    "slug": "[sprint-name-kebab-case]",
    "repo": "[repository-name]",
    "service_name": "[service-name]",
    "branch_base": "develop",
    "branch_feature": "feature/s[n]-[branch-suffix]",
    "owner_primary": "[Owner 1]",
    "owner_secondary": "[Owner 2]",
    "kickoff_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD"
  },
  "targets": {
    "duration_weeks": [N],
    "files_to_create": [N],
    "files_to_modify": [M],
    "tests_target": [N],
    "coverage_target_percent": [X],
    "ci_time_max_minutes": [N],
    "loc_estimate": [~N]
  },
  "slos": {
    "latency_p95_ms": [N],
    "throughput_rps": [N],
    "error_rate_percent": [X],
    "build_time_minutes": [N]
  },
  "flags": {
    "has_db_migrations": false,
    "requires_mocks": true,
    "needs_security_review": true,
    "cross_repo_deps": true,
    "breaking_changes": false,
    "requires_baseline_update": false
  },
  "dependencies": {
    "agent_contracts_version": "[X.Y.Z]",
    "nops_kernel_api": "[version/endpoint]",
    "other_repos": []
  },
  "artifacts": {
    "docs_dir": "docs/01-sprint/S[N]",
    "tracking_file": "S[N]_SPRINT_TRACKING.md",
    "completion_report": "S[N]_COMPLETION_REPORT.md",
    "rollback_info": "ROLLBACK_INFO.txt"
  }
}
```

### Uso de la Configuración

Los placeholders en este documento deben reemplazarse usando los valores del JSON:
- `[N]` → `sprint.number`
- `[Sprint Name]` → `sprint.name`
- `[repository-name]` → `sprint.repo`
- `[branch-suffix]` → extraído de `sprint.branch_feature`
- Etc.

**Comando de inicio sugerido para Claude Code CLI:**
```bash
# Iniciar sprint con configuración
claude-code-cli execute-sprint \
  --config sprint-config.json \
  --document "docs/01-sprint/S[N]/S[N]-[name].md"
```

---

## 🎯 Meta

[Descripción breve y clara del objetivo principal del sprint. Qué debe lograrse al final.]

**Ejemplo:**
> Implementar contratos HTTP y streaming completos con esquemas JSON y protos validados en CI con baseline firmado.

### 📈 SLOs del Sprint (Service Level Objectives)

> **🎯 Novedad v2.0:** Métricas técnicas medibles para declarar éxito

| Métrica | Target | Medición | Criticidad |
|---------|--------|----------|------------|
| **Latencia p95** | < [N]ms | Load test (k6/wrk) | 🔴 Crítico |
| **Coverage** | ≥ [X]% | pytest --cov / jest --coverage | 🔴 Crítico |
| **Throughput** | ≥ [N] req/s | Load test | 🟡 Importante |
| **Error rate** | < [X]% | Logs/métricas | 🔴 Crítico |
| **Build time** | < [N] min | CI pipeline | 🟢 Nice-to-have |
| **API response time** | < [N]ms | Postman/curl | 🟡 Importante |

**Criterio de éxito técnico:** 
- Todos los SLOs 🔴 Críticos deben cumplirse
- Al menos 80% de los 🟡 Importantes deben cumplirse
- Los 🟢 Nice-to-have son opcionales pero deseables

---

## 📁 Ubicación de Artefactos del Sprint

> **🎯 Novedad v2.0:** Estructura estandarizada de documentación

Todos los artefactos del sprint deben crearse siguiendo esta estructura:

```
docs/01-sprint/S[N]/
├── README.md                           # Resumen ejecutivo del sprint
├── S[N]-IMPLEMENTATION-GUIDE.md        # Guía técnica de implementación
├── S[N]-TROUBLESHOOTING.md             # Guía de resolución de problemas
├── HOWTO_S[N].md                       # Quick start / comandos útiles
├── dod-checklist.md                    # Checklist del Definition of Done
├── ADR-[N]-001-[decision-slug].md      # Architecture Decision Records
├── ADR-[N]-002-[otra-decision].md
└── patches/                            # Patches opcionales (si aplica)
    ├── patch-001-[descripcion].diff
    └── patch-002-[otra].diff
```

**Archivos generados automáticamente (raíz del repo):**
```
[repo-root]/
├── S[N]_SPRINT_TRACKING.md             # Tracking de progreso (FASE 1)
├── S[N]_COMPLETION_REPORT.md           # Reporte final (FASE [N])
├── PR_CHECKLIST.md                     # Checklist para PR (FASE [N])
├── PR_DESCRIPTION.md                   # Descripción de PR (FASE [N])
└── ROLLBACK_INFO.txt                   # Info de rollback (FASE [N-0.5])
```

**Convención de nombres:**
- Usar `S[N]` con número del sprint (ej: `S0`, `S1`, `S2`)
- Slugs en kebab-case (ej: `redis-vs-inmemory`)
- Dates en formato ISO 8601 (ej: `2025-10-13`)

---

## ⚙️ Prerequisitos (Verificar antes de ejecutar)

### Herramientas Requeridas (Críticas)
- [ ] **Git >= 2.30.0** instalado y configurado
- [ ] **Node.js >= 18.0.0** instalado
- [ ] **Python >= 3.11.0** instalado
- [ ] Acceso a GitHub Actions
- [ ] Permisos para crear branches

### Herramientas Recomendadas (Opcionales)
- [ ] **Docker >= 20.10.0** (para testing local)
- [ ] **Docker Compose** (para servicios locales)
- [ ] **jq >= 1.6.0** (para procesamiento JSON)
- [ ] **curl** (para health checks)
- [ ] [Otra herramienta específica del proyecto]

### Validación Automática
> **🎯 v2.1:** La FASE 0 valida automáticamente todas las versiones requeridas y error patterns
> 
> **Comando de validación manual:**
> ```bash
> # Ejecutar solo la validación de prerequisitos
> bash -c 'source <(grep -A 50 "Verificar herramientas requeridas" docs/01-sprint/Template/SPRINT_TEMPLATE_CLAUDE_CLI.md | grep -A 50 "check_version")'
> 
> # Ejecutar tests de error patterns
> bash -c 'source <(grep -A 200 "run_pattern_tests" docs/01-sprint/Template/SPRINT_TEMPLATE_CLAUDE_CLI.md | grep -A 200 "run_pattern_tests")'
> ```

### Dependencias de Sprints Anteriores
- [ ] **S[N-1]** completado y merged a `develop`
- [ ] [Otro prerequisito específico]
- [ ] [Artefactos necesarios del sprint anterior]

### Estado del Repositorio
- [ ] Branch `develop` actualizado
- [ ] No hay cambios sin commitear
- [ ] CI/CD pipelines funcionando
- [ ] [Otro requisito de estado]

### Cross-Repository Dependencies

> **🎯 Novedad v2.0:** Dependencias con otros repositorios de ENIS

**Dependencias identificadas:**
- [ ] **agent-contracts:** Versión [X.Y.Z] de contratos requerida
- [ ] **nops-kernel:** API [endpoint/version] disponible
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

## 📦 Entregables

### Resumen Ejecutivo

| Categoría | Cantidad | Descripción |
|-----------|----------|-------------|
| **Contratos** | [N] | [Tipo de contratos] |
| **Schemas** | [N] | [Tipo de schemas] |
| **Scripts** | [N] | [Scripts de automatización] |
| **Tests** | [N] | [Tipos de tests] |
| **Docs** | [N] | [Documentación] |
| **Workflows** | [N] | [CI/CD workflows] |

---

### Entregable 1: [Nombre del Entregable]

**Descripción**: [Descripción detallada de qué es este entregable]

**Archivos a crear/modificar:**
```
[path]/[file1]
[path]/[file2]
[path]/[file3]
```

**Criterios de aceptación:**
- [ ] [Criterio 1]
- [ ] [Criterio 2]
- [ ] [Criterio 3]

**Ejemplos/Referencias:**
```yaml
# Ejemplo de contenido esperado
[código de ejemplo]
```

---

### Entregable 2: [Nombre del Entregable]

[Repetir estructura para cada entregable]

---

## 📊 Definition of Done - Cuantificable (DoD)

> **🎯 Novedad v2.0:** DoD con métricas verificables y scoring automático

**Cumplimiento Target:** **[X] / [Y] = [Z%]** ✅

### Ejemplo de Categorización:

**Infrastructure ([A]/[B])**
1. [Servicio/componente 1] healthy — ✅✅ 100%  
2. [Configuración 2] implementada — ✅⚠️ 80% (issue menor)  
3. [Feature 3] funcional — ❌ 0% (bloqueado)

**Core Features ([C]/[D])**
4. [Feature principal 1] — ✅✅ 100%  
5. [Feature principal 2] — ✅⚠️ 90% (falta edge case)  
6. [Feature principal 3] — ✅✅ 100%

**Testing & CI ([E]/[F])**
7. [N] tests implementados — ✅⚠️ 85% (placeholders pendientes)  
8. Coverage ≥ [X]% — ✅⚠️ objetivo  
9. CI verde — ✅✅ 100%  
10. Integration tests — ✅✅ 100%

**Documentation ([G]/[H])**
11. HOWTO actualizado — ✅✅ 100%  
12. README actualizado — ✅✅ 100%  
13. Troubleshooting — ✅✅ 100%  
14. Docstrings — ✅⚠️ 80% (básicos)

**Monitoring & Operations ([I]/[J])**
15. Métricas expuestas — ✅✅ 100%  
16. Dashboards configurados — ✅⚠️ 80%  
17. Alertas definidas — ✅✅ 100%

**Security & Compliance ([K]/[L])**
18. SBOM generado (Syft/CycloneDX) — ✅⚠️ 80%  
19. Firmas digitales (Cosign) — ✅✅ 100%  
20. mTLS/JWT configurado (si S2S) — ✅✅ 100%  
21. Egress Guard (fail-closed) — ✅⚠️ 90%  
22. Rate-limit headers presentes — ✅✅ 100%  
23. Secrets no hardcodeados (verified) — ✅✅ 100%  
24. Security scan sin críticos — ✅✅ 100%

> **⚠️ Crítico:** Items 19, 23, 24 son **bloqueantes** para merge a main

### Scoring Guide

- ✅✅ **100%** - Completo y validado
- ✅⚠️ **80-99%** - Completo con issues menores
- ⚠️ **50-79%** - Parcial, requiere trabajo
- ❌ **0-49%** - No implementado o bloqueado

### Métricas de Éxito

| Métrica | Target | Actual | Status |
|---------|--------|--------|--------|
| **Archivos creados** | [N] | [M] | ✅/⚠️/❌ |
| **Tests implementados** | [N] | [M] | ✅/⚠️/❌ |
| **Coverage** | ≥[X]% | [Y]% | ✅/⚠️/❌ |
| **CI Pipeline** | < [N] min | [M] min | ✅/⚠️/❌ |
| **LOC añadidas** | ~[N] | [M] | ℹ️ |

---

## 🔍 QA Interno & Auto-análisis

> **🎯 Novedad v2.0:** Sección de auto-validación del sprint

### Issues Detectados & Severidad

#### ISSUE 1 — [Título del issue] ([🔴 crítico / 🟡 medio / 🟢 menor])

**Problema:**  
[Descripción del problema detectado]

**Impacto:**  
[Qué afecta este issue, qué funcionalidad o métrica]

**Patch sugerido:**
```diff
*** Begin Patch
*** Update File: [ruta/archivo]
@@
+[cambios sugeridos]
-[líneas a remover]
*** End Patch
```

**Beneficio:**  
[Qué mejora aplicar este patch, ej: "eleva DoD item 13 de 80% a 100%"]

---

#### ISSUE 2 — [Otro issue]

[Repetir estructura]

---

### ✅ Acciones para Cerrar 100% del DoD

1. Aplicar **Patch [nombre]** (ISSUE 1)  
2. Completar **[tarea pendiente]** (ISSUE 2)  
3. Agregar **[documentación/tests faltantes]** (ISSUE 3)

> **Tras completar estas acciones:** DoD = [X+Y]/[Total] = 100%

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

### ADR-[N]-001 — [Título de la decisión]

**Contexto:**  
[Por qué se necesita esta decisión. Ej: "Necesitamos decidir entre Redis y en-memory para cache"]

**Decisión:**  
[Qué se decidió. Ej: "Usar Redis con fallback in-memory para resiliencia"]

**Razón:**
- [Razón 1: Persistencia entre reinicios]
- [Razón 2: Compartir cache entre workers]
- [Razón 3: Fallback mantiene funcionalidad básica]

**Consecuencias:**
- ✅ **Positivas:** [Lista de beneficios]
- ⚠️ **Negativas:** [Lista de trade-offs]

**Alternativas consideradas:**
1. Solo in-memory: Rechazado (no comparte estado)
2. Solo Redis: Rechazado (SPOF sin fallback)
3. Memcached: Rechazado (menos features que Redis)

**Archivo:** `docs/01-sprint/S[N]/ADR-[N]-001-[slug].md`

---

### ADR-[N]-002 — [Otra decisión importante]

[Repetir estructura]

---

## 🧪 Plan de Cobertura de Pruebas

> **🎯 Novedad v2.0:** Plan detallado de testing

### Objetivo de Cobertura

- **Target:** [N] tests totales
- **Coverage:** ≥[X]%
- **Distribución:** Unit ([N]%), Integration ([M]%), E2E ([P]%)

### Breakdown por Módulo

| Módulo/Feature | Tests | Tipo | Prioridad | Status |
|----------------|-------|------|-----------|--------|
| [modulo1] | [N] | unit | 🔴 alta | ⏸️ |
| [modulo2] | [M] | integration | 🟡 media | ⏸️ |
| [modulo3] | [P] | unit | 🟢 baja | ⏸️ |

### Tests Detallados

#### Módulo: [Nombre del módulo]
**Archivo:** `tests/test_[nombre].py`  
**Tests:** [N]

1. `test_[nombre_1]` - [Descripción: valida que...]
2. `test_[nombre_2]` - [Descripción: verifica que...]
3. `test_[nombre_3]` - [Descripción: edge case...]
4. `test_[nombre_4_error_handling]` - [Descripción: falla cuando...]
5. [Etc.]

**Cobertura esperada:** ≥[X]%

---

#### Módulo: [Otro módulo]

[Repetir estructura]

---

### Integration Tests

**Archivo:** `tests/integration/test_[feature]_flow.py`  
**Tests:** [N] E2E

1. `test_complete_[feature]_flow` - [Descripción del flujo completo]
2. `test_[feature]_with_errors` - [Descripción de manejo de errores]
3. `test_[feature]_idempotency` - [Descripción de comportamiento idempotente]

### Test Markers

```python
@pytest.mark.unit        # Tests unitarios rápidos
@pytest.mark.integration # Tests que requieren servicios externos
@pytest.mark.slow        # Tests que toman >1s
@pytest.mark.smoke       # Tests críticos de smoke
```

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

### 📋 FASE 0: Pre-flight Checks & Environment Verification

**⏱️ Duración estimada:** 5 minutos  
**🎯 Objetivo:** Verificar que el entorno está listo y cumple todos los prerequisitos

**Pasos ejecutables:**

#### 1. Verificar directorio de trabajo

**Bash/Linux/macOS:**
```bash
# Confirmar que estamos en el directorio correcto
pwd
# Debe estar en: [ruta esperada]

# Verificar que es un repositorio Git
git rev-parse --git-dir
```

**PowerShell (Windows):**
```powershell
# PS> Confirmar directorio correcto
Get-Location
# Debe estar en: [ruta esperada]

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

# Docker Compose (opcional)
if command -v docker-compose &> /dev/null; then
  COMPOSE_VERSION=$(docker-compose --version | cut -d' ' -f3 | cut -d',' -f1)
  log_success "Docker Compose $COMPOSE_VERSION available"
elif command -v docker &> /dev/null && docker compose version &> /dev/null; then
  log_success "Docker Compose (plugin) available"
else
  log_warn "Docker Compose not found (optional for local development)"
fi

# jq (para procesamiento JSON)
if command -v jq &> /dev/null; then
  JQ_VERSION=$(jq --version | cut -d'-' -f2)
  if check_version "jq" "$JQ_VERSION" "1" "6" "0"; then
    log_success "jq $JQ_VERSION available"
  else
    log_warn "jq version $JQ_VERSION below recommended 1.6.0 (continuing...)"
  fi
else
  log_warn "jq not found (optional for JSON processing)"
fi

# curl (para health checks)
if command -v curl &> /dev/null; then
  CURL_VERSION=$(curl --version | head -n1 | cut -d' ' -f2)
  log_success "curl $CURL_VERSION available"
else
  log_warn "curl not found (optional for health checks)"
fi

# Verificar herramientas opcionales del proyecto
log_info "Validating project-specific tools..."
for tool in "[herramienta-proyecto-1]" "[herramienta-proyecto-2]"; do
  if ! command -v "$tool" &> /dev/null; then
    log_warn "Project tool '$tool' not found (continuing...)"
  else
    log_success "Project tool '$tool' available"
  fi
done

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
# Environment Check Report - Sprint S[N]

**Date:** $(date)
**Sprint:** S[N] - [Sprint Name]
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
if command -v docker &> /dev/null; then
  echo "- Docker: $(docker --version) ✅" >> PHASE0_ENVIRONMENT_CHECK.md
else
  echo "- Docker: Not found ⚠️ (optional)" >> PHASE0_ENVIRONMENT_CHECK.md
fi

if command -v docker-compose &> /dev/null; then
  echo "- Docker Compose: $(docker-compose --version) ✅" >> PHASE0_ENVIRONMENT_CHECK.md
elif command -v docker &> /dev/null && docker compose version &> /dev/null; then
  echo "- Docker Compose: Plugin available ✅" >> PHASE0_ENVIRONMENT_CHECK.md
else
  echo "- Docker Compose: Not found ⚠️ (optional)" >> PHASE0_ENVIRONMENT_CHECK.md
fi

if command -v jq &> /dev/null; then
  echo "- jq: $(jq --version) ✅" >> PHASE0_ENVIRONMENT_CHECK.md
else
  echo "- jq: Not found ⚠️ (optional)" >> PHASE0_ENVIRONMENT_CHECK.md
fi

if command -v curl &> /dev/null; then
  echo "- curl: $(curl --version | head -n1) ✅" >> PHASE0_ENVIRONMENT_CHECK.md
else
  echo "- curl: Not found ⚠️ (optional)" >> PHASE0_ENVIRONMENT_CHECK.md
fi

cat >> PHASE0_ENVIRONMENT_CHECK.md << 'EOF'

## Validation Summary

### Critical Requirements
- ✅ Node.js >= 18.0.0: PASSED
- ✅ Python >= 3.11.0: PASSED  
- ✅ Git >= 2.30.0: PASSED

### Optional Recommendations
- [ ] Docker >= 20.10.0: [Status]
- [ ] Docker Compose: [Status]
- [ ] jq >= 1.6.0: [Status]
- [ ] curl: [Status]

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
test -d [directorio_esperado] && echo "✅ [directorio_esperado] exists" || echo "❌ [directorio_esperado] missing"
test -f [archivo_esperado] && echo "✅ [archivo_esperado] exists" || echo "❌ [archivo_esperado] missing"

# Listar archivos existentes relevantes
echo "" >> PHASE0_ENVIRONMENT_CHECK.md
echo "## Existing Files Check" >> PHASE0_ENVIRONMENT_CHECK.md
ls -la [directorio_relevante] >> PHASE0_ENVIRONMENT_CHECK.md
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

### 📋 FASE 1: Branch Setup & Initialization

**⏱️ Duración estimada:** 3 minutos  
**🎯 Objetivo:** Crear rama de trabajo y preparar entorno

**Pasos ejecutables:**

#### 1. Actualizar develop
```bash
# Configurar error handling robusto
set -euo pipefail
trap 'echo "❌ ERROR at line $LINENO in FASE 1.1"' ERR

# Cambiar a develop
if ! git checkout develop; then
  echo "❌ ERROR: Failed to checkout develop branch"
  exit 1
fi

# Actualizar desde origin con timeout
if ! run_with_timeout $TIMEOUT_GIT "git pull origin develop" "Git pull from origin"; then
  log_error "Failed to pull develop from origin"
  log_info "Suggestion: Check network connection and repository access"
  exit 1
fi

# Verificar que está actualizado
if ! git log --oneline -n 3; then
  echo "❌ ERROR: Failed to verify git log"
  exit 1
fi

echo "✅ Develop branch updated successfully"
```

**✅ Criterio de éxito:** Branch develop actualizado

#### 2. Crear feature branch
```bash
# Configurar error handling para creación de branch
set -euo pipefail
trap 'echo "❌ ERROR at line $LINENO in FASE 1.2"' ERR

# Verificar que no existe la rama
if git show-ref --verify --quiet refs/heads/feature/s[n]-[branch-suffix]; then
  echo "⚠️  WARNING: Branch feature/s[n]-[branch-suffix] already exists"
  echo "💡 Suggestion: Delete existing branch or use different suffix"
  exit 1
fi

# Crear y cambiar a nueva rama
if ! git checkout -b feature/s[n]-[branch-suffix]; then
  echo "❌ ERROR: Failed to create branch feature/s[n]-[branch-suffix]"
  exit 1
fi

# Verificar rama actual
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "feature/s[n]-[branch-suffix]" ]; then
  echo "❌ ERROR: Expected branch feature/s[n]-[branch-suffix], got $CURRENT_BRANCH"
  exit 1
fi

# Verificar que está basada en develop
if ! git log --oneline --graph --all -n 10; then
  echo "❌ ERROR: Failed to verify branch history"
  exit 1
fi

echo "✅ Feature branch created successfully: $CURRENT_BRANCH"
```

**✅ Criterio de éxito:** Nueva rama creada y activa

#### 3. Documentar inicio del sprint
```bash
# Crear archivo de tracking del sprint (idempotent)
if [ ! -f "S[N]_SPRINT_TRACKING.md" ]; then
  log_info "Creating sprint tracking file"
cat > S[N]_SPRINT_TRACKING.md << 'EOF'
# Sprint S[N] - [Sprint Name] - Tracking

**Started:** $(date)
**Branch:** feature/s[n]-[branch-suffix]
**Status:** In Progress

## Progress Tracker

### Fases Completadas
- [x] FASE 0 - Pre-flight Checks
- [x] FASE 1 - Branch Setup
- [ ] FASE 2 - [Nombre]
- [ ] FASE 3 - [Nombre]
[... resto de fases]

## Issues Log
(Se actualizará durante la ejecución)

EOF
  log_success "Sprint tracking file created"
else
  log_warn "Sprint tracking file already exists, skipping"
fi
```

**✅ Criterios de éxito globales de FASE 1:**
- [ ] Branch develop actualizado
- [ ] Feature branch creado
- [ ] Branch correcto activo
- [ ] Tracking file creado

---

### 📋 FASE 2: [Nombre de la Fase - Ej: "Create Core Files"]

**⏱️ Duración estimada:** [N] minutos  
**🎯 Objetivo:** [Descripción del objetivo de esta fase]

**Pasos ejecutables:**

#### 1. [Nombre del paso]
```bash
# [Descripción de qué hace este comando]
[comando ejecutable]
```

**Contexto adicional:**
[Si es necesario, explicar por qué este paso es importante]

**✅ Criterio de éxito:** [Cómo verificar que este paso se completó correctamente]

#### 2. [Siguiente paso]
```bash
[comando ejecutable]
```

**✅ Criterio de éxito:** [Verificación]

#### 3. Verificar fase completa
```bash
# Verificar que todos los archivos esperados existen
test -f [archivo1] && echo "✅ [archivo1]" || echo "❌ [archivo1] MISSING"
test -f [archivo2] && echo "✅ [archivo2]" || echo "❌ [archivo2] MISSING"

# Validar sintaxis/contenido si aplica
[comando de validación]
```

**✅ Criterios de éxito globales de FASE 2:**
- [ ] [Criterio 1]
- [ ] [Criterio 2]
- [ ] [Criterio 3]
- [ ] Todos los archivos creados
- [ ] Todas las validaciones pasan

---

### 📋 FASE 3: [Otra Fase]

[Repetir estructura de FASE 2 para cada fase necesaria]

**Fases típicas a incluir:**
- FASE N: Create/Modify [Tipo de Archivos]
- FASE N+1: Configure [Herramienta/Sistema]
- FASE N+2: Write Tests
- FASE N+3: Validate & Verify
- FASE N+4: Generate Documentation
- FASE N+5: Git Commit & Push
- FASE N+6: Final Report

---

### 📋 FASE [N-2]: Testing & Validation

**⏱️ Duración estimada:** [N] minutos  
**🎯 Objetivo:** Ejecutar todas las validaciones y tests necesarios

**Pasos ejecutables:**

#### 1. Ejecutar tests unitarios
```bash
# Configurar error handling para tests
set -euo pipefail
trap 'echo "❌ ERROR at line $LINENO in FASE [N-2].1"' ERR

# Detectar tipo de proyecto y ejecutar tests con timeout
if [ -f "package.json" ]; then
  log_info "Detected Node.js project, running npm test"
  if ! run_with_timeout $TIMEOUT_TESTS "npm test" "Unit tests (npm)"; then
    log_error "npm test failed or timed out"
    exit 1
  fi
elif [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then
  log_info "Detected Python project, running pytest"
  if ! run_with_timeout $TIMEOUT_TESTS "pytest tests/ -v" "Unit tests (pytest)"; then
    log_error "pytest failed or timed out"
    exit 1
  fi
elif [ -f "go.mod" ]; then
  log_info "Detected Go project, running go test"
  if ! run_with_timeout $TIMEOUT_TESTS "go test ./..." "Unit tests (go test)"; then
    log_error "go test failed or timed out"
    exit 1
  fi
else
  log_warn "No test framework detected, skipping unit tests"
fi
```

**✅ Criterio de éxito:** Todos los tests pasan o no hay tests disponibles

#### 2. Ejecutar validaciones de contratos
```bash
# Configurar error handling para validaciones
set -euo pipefail
trap 'echo "❌ ERROR at line $LINENO in FASE [N-2].2"' ERR

# Validar OpenAPI con timeout
if [ -d "openapi" ] && find openapi -name "*.yaml" -o -name "*.yml" | grep -q .; then
  log_info "Validating OpenAPI specifications"
  if ! run_with_timeout $TIMEOUT_VALIDATION "npx @stoplight/spectral-cli lint openapi/**/*.yaml" "OpenAPI validation"; then
    log_error "OpenAPI validation failed or timed out"
    exit 1
  fi
else
  log_info "No OpenAPI files found, skipping validation"
fi

# Validar JSON Schemas con timeout
if [ -d "schemas" ] && find schemas -name "*.json" | grep -q .; then
  log_info "Validating JSON Schemas"
  if ! run_with_timeout $TIMEOUT_VALIDATION "npx ajv-cli validate -s schemas/*.json" "JSON Schema validation"; then
    log_error "JSON Schema validation failed or timed out"
    exit 1
  fi
else
  log_info "No JSON Schema files found, skipping validation"
fi

# Validar Protocol Buffers con timeout
if [ -d "proto" ] && find proto -name "*.proto" | grep -q .; then
  log_info "Validating Protocol Buffers"
  if ! run_with_timeout $TIMEOUT_VALIDATION "buf lint proto/" "Protocol Buffer validation"; then
    log_error "Protocol Buffer validation failed or timed out"
    exit 1
  fi
else
  log_info "No Protocol Buffer files found, skipping validation"
fi
```

**✅ Criterio de éxito:** Todas las validaciones pasan o no hay archivos para validar

#### 3. Ejecutar smoke tests
```bash
# Configurar error handling para smoke tests
set -euo pipefail
trap 'echo "❌ ERROR at line $LINENO in FASE [N-2].3"' ERR

# Ejecutar smoke tests con timeout
if [ -f "scripts/smoke-tests.sh" ]; then
  log_info "Running smoke tests"
  if ! run_with_timeout $TIMEOUT_TESTS "bash scripts/smoke-tests.sh" "Smoke tests"; then
    log_error "Smoke tests failed or timed out"
    exit 1
  fi
elif [ -f "package.json" ] && grep -q "smoke" package.json; then
  log_info "Running npm smoke tests"
  if ! run_with_timeout $TIMEOUT_TESTS "npm run smoke" "Smoke tests (npm)"; then
    log_error "Smoke tests failed or timed out"
    exit 1
  fi
else
  log_info "No smoke tests found, skipping"
fi
```

**✅ Criterio de éxito:** Smoke tests completos exitosamente o no disponibles

#### 4. Verificar CI/CD workflows (si aplica)
```bash
# Configurar error handling para validación de workflows
set -euo pipefail
trap 'echo "❌ ERROR at line $LINENO in FASE [N-2].4"' ERR

# Validar sintaxis de workflows con timeout
if [ -d ".github/workflows" ] && find .github/workflows -name "*.yml" -o -name "*.yaml" | grep -q .; then
  log_info "Validating CI/CD workflows"
  for file in .github/workflows/*.yml .github/workflows/*.yaml; do
    if [ -f "$file" ]; then
      log_info "Validating $file"
      if ! run_with_timeout $TIMEOUT_VALIDATION "python -c \"import yaml; yaml.safe_load(open('$file'))\"" "YAML validation for $file"; then
        log_error "Workflow validation failed for $file"
        exit 1
      fi
    fi
  done
  log_success "All workflows validated successfully"
else
  log_info "No CI/CD workflows found, skipping validation"
fi
```

**✅ Criterios de éxito globales de FASE [N-2]:**
- [ ] Tests unitarios pasan
- [ ] Validaciones de contratos pasan
- [ ] Smoke tests exitosos
- [ ] Workflows válidos (si aplica)

---

### 📋 FASE [N-1]: Git Commit & Push

**⏱️ Duración estimada:** 5 minutos  
**🎯 Objetivo:** Commitear cambios y pushear la rama

**Pasos ejecutables:**

#### 1. Verificar cambios
```bash
# Ver estado de Git
git status

# Ver diff de cambios
git diff --stat

# Ver archivos nuevos
git ls-files --others --exclude-standard

# Contar archivos modificados/nuevos
echo "Files modified: $(git diff --name-only | wc -l)"
echo "Files added: $(git ls-files --others --exclude-standard | wc -l)"
```

#### 2. Agregar archivos
```bash
# Agregar todos los archivos
git add .

# Verificar staging area
git status
```

#### 3. Crear commit
```bash
# Commit con mensaje descriptivo siguiendo Conventional Commits
git commit -m "feat(s[n]): [descripción breve del sprint]

[Descripción más detallada:]
- [Cambio principal 1]
- [Cambio principal 2]
- [Cambio principal 3]
- [Etc.]

Sprint: S[N] - [Sprint Name]
Status: Ready for review
DoD: [Criterios clave completados]

Refs: #[issue-number] (si aplica)"
```

**Plantilla de commit message:**
```
[tipo](s[n]): [descripción de máx 50 chars]

[Cuerpo del commit explicando QUÉ y POR QUÉ]
- Bullet point 1
- Bullet point 2
- Bullet point 3

Sprint: S[N] - [Sprint Name]
Status: [Ready for review / WIP / etc]
DoD: [Brief DoD summary]

[Footer opcional con referencias]
Refs: #123
Breaking-change: [Si aplica]
```

**Tipos de commit válidos:**
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Documentación
- `refactor`: Refactorización
- `test`: Tests
- `chore`: Mantenimiento
- `ci`: CI/CD
- `perf`: Mejoras de performance

#### 4. Push branch
```bash
# Push a origin con timeout
if ! run_with_timeout $TIMEOUT_GIT "git push -u origin feature/s[n]-[branch-suffix]" "Git push to origin"; then
  log_error "Failed to push branch to origin"
  exit 1
fi

# Verificar push exitoso
if ! run_with_timeout $TIMEOUT_GIT "git log origin/feature/s[n]-[branch-suffix] --oneline -n 3" "Verify push success"; then
  log_error "Failed to verify push success"
  exit 1
fi
```

#### 5. Generar URL para PR
```bash
# Mostrar URL para crear Pull Request
REPO_URL=$(git config --get remote.origin.url | sed 's/\.git$//')
BRANCH_NAME=$(git branch --show-current)
echo ""
echo "🎉 =========================================="
echo "🎉  BRANCH PUSHED SUCCESSFULLY!"
echo "🎉 =========================================="
echo ""
echo "📝 Create Pull Request at:"
echo "${REPO_URL}/compare/develop...${BRANCH_NAME}"
echo ""
echo "Or use GitHub CLI:"
echo "gh pr create --base develop --head ${BRANCH_NAME} --title \"[Sprint S[N]] [Sprint Name]\" --body-file PR_DESCRIPTION.md"
echo ""
```

**✅ Criterios de éxito globales de FASE [N-1]:**
- [ ] Todos los cambios commiteados
- [ ] Commit message sigue convenciones
- [ ] Branch pusheado exitosamente
- [ ] URL de PR generada

---

### 📋 FASE [N-0.5]: Rollback Plan & Safety Verification

> **🎯 Novedad v2.0:** Plan de reversión antes del merge

**⏱️ Duración estimada:** 5 minutos  
**🎯 Objetivo:** Preparar procedimiento de rollback en caso de issues post-merge

**Pasos ejecutables:**

#### 1. Documentar estado pre-sprint
```bash
# Guardar hash del último commit de develop antes del sprint
git fetch origin
git rev-parse origin/develop > ROLLBACK_INFO.txt
echo "Sprint: S[N]" >> ROLLBACK_INFO.txt
echo "Branch: feature/s[n]-[branch-suffix]" >> ROLLBACK_INFO.txt
echo "Date: $(date -Iseconds)" >> ROLLBACK_INFO.txt
echo "Author: $(git config user.name)" >> ROLLBACK_INFO.txt
```

#### 2. Crear script de rollback
```bash
cat > rollback-s[n].sh << 'EOF'
#!/usr/bin/env bash
# Rollback script for Sprint S[N]
set -euo pipefail

echo "🔄 Rolling back Sprint S[N]..."
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
rm -f S[N]_*.md PR_*.md ROLLBACK_INFO.txt 2>/dev/null || true

# Limpiar branches locales huérfanas
log_info "🧹 Cleaning up orphaned branches..."
git branch -D feature/s[n]-* 2>/dev/null || true

# Limpiar build artifacts
log_info "🧹 Cleaning up build artifacts..."
rm -rf dist/ build/ node_modules/.cache/ .pytest_cache/ __pycache__/ 2>/dev/null || true

# Limpiar archivos temporales
log_info "🧹 Cleaning up temporary files..."
rm -f /tmp/sprint-*.tmp .sprint-checkpoint 2>/dev/null || true

# Limpiar logs antiguos
log_info "🧹 Cleaning up old logs..."
rm -f sprint-s[n].log 2>/dev/null || true

log_success "✅ Rollback and cleanup completed"
echo "⚠️  Verificar manualmente que todo funciona correctamente"
EOF

chmod +x rollback-s[n].sh
```

**PowerShell (Windows):**
```powershell
# PS> Equivalente del rollback script
@'
# Rollback script for Sprint S[N] (PowerShell)
Write-Host "🔄 Rolling back Sprint S[N]..." -ForegroundColor Yellow

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
Remove-Item "S[N]_*.md", "PR_*.md", "ROLLBACK_INFO.txt" -ErrorAction SilentlyContinue

Write-Host "✅ Rollback completado" -ForegroundColor Green
'@ | Out-File -FilePath rollback-s[n].ps1 -Encoding UTF8
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
- [Cambio crítico 1]: [Procedimiento de rollback específico]
- [Cambio crítico 2]: [Procedimiento de rollback específico]
- [Etc.]

## Contacts for Emergency Rollback
- On-call: [PagerDuty link / phone]
- Platform Team: @platform-team (Slack)
- Sprint Owner: [Owner name]

CRITICAL

echo "✅ ROLLBACK_INFO.txt actualizado con cambios críticos"
```

#### 5. Crear backup de estado actual (opcional pero recomendado)
```bash
# Crear backup de archivos críticos
mkdir -p .backup-s[n]
cp -r config/ .backup-s[n]/config/ 2>/dev/null || true
cp -r openapi/ .backup-s[n]/openapi/ 2>/dev/null || true
tar -czf backup-s[n]-$(date +%Y%m%d-%H%M%S).tar.gz .backup-s[n]/

echo "✅ Backup creado: backup-s[n]-*.tar.gz"
```

**✅ Criterios de éxito globales de FASE [N-0.5]:**
- [ ] ROLLBACK_INFO.txt creado con hash de develop
- [ ] rollback-s[n].sh ejecutable y documentado
- [ ] Checklist de reversibilidad completado
- [ ] Cambios críticos documentados
- [ ] Backup creado (opcional)
- [ ] Script de rollback probado en local (recomendado)

---

### 📋 FASE [N]: Final Verification & Reporting

**⏱️ Duración estimada:** 10 minutos  
**🎯 Objetivo:** Generar reportes completos y verificar Definition of Done

**Pasos ejecutables:**

#### 1. Generar reporte de cambios
```bash
# Crear reporte principal
cat > S[N]_COMPLETION_REPORT.md << 'EOF'
# Sprint S[N] - [Sprint Name] - Completion Report

**Completed:** $(date)
**Branch:** feature/s[n]-[branch-suffix]
**Base Branch:** develop
**Status:** ✅ COMPLETE - Ready for Review

---

## Executive Summary

[Breve resumen de lo logrado en el sprint]

---

## Files Changed

EOF

# Agregar lista de archivos (usando origin/develop para mayor robustez)
git diff --name-only origin/develop...HEAD >> S[N]_COMPLETION_REPORT.md

echo "" >> S[N]_COMPLETION_REPORT.md
echo "---" >> S[N]_COMPLETION_REPORT.md
echo "" >> S[N]_COMPLETION_REPORT.md
echo "## Statistics" >> S[N]_COMPLETION_REPORT.md
echo "" >> S[N]_COMPLETION_REPORT.md
echo "- **Total files changed:** $(git diff --name-only origin/develop...HEAD | wc -l)" >> S[N]_COMPLETION_REPORT.md
echo "- **Lines added:** $(git diff --stat origin/develop...HEAD | tail -1 | awk '{print $4}')" >> S[N]_COMPLETION_REPORT.md
echo "- **Lines removed:** $(git diff --stat origin/develop...HEAD | tail -1 | awk '{print $6}')" >> S[N]_COMPLETION_REPORT.md
echo "- **Commits:** $(git rev-list --count origin/develop..HEAD)" >> S[N]_COMPLETION_REPORT.md
```

#### 2. Verificar Definition of Done
```bash
cat >> S[N]_COMPLETION_REPORT.md << 'EOF'

---

## Definition of Done (DoD)

### Entregables
- [ ] [Entregable 1] - [Status]
- [ ] [Entregable 2] - [Status]
- [ ] [Entregable 3] - [Status]

### Calidad
- [ ] Tests ejecutados y pasando
- [ ] Validaciones de contratos pasando
- [ ] Documentación actualizada
- [ ] No hay linter errors críticos
- [ ] Code review checklist completo

### CI/CD (si aplica)
- [ ] Workflows configurados
- [ ] Pipelines pasando
- [ ] No hay breaking changes no documentados

### Documentación
- [ ] README actualizado
- [ ] Guías técnicas escritas
- [ ] Ejemplos incluidos
- [ ] CHANGELOG actualizado (si aplica)

---

## Issues Encountered

[Documentar cualquier issue encontrado durante el sprint]
- Issue 1: [Descripción] - Status: [Resuelto/Pendiente]
- Issue 2: [Descripción] - Status: [Resuelto/Pendiente]

---

## Next Steps

1. [ ] Create Pull Request to `develop`
2. [ ] Request reviews from: [Lista de reviewers]
3. [ ] Address review comments
4. [ ] Merge to develop
5. [ ] Begin Sprint S[N+1]

---

## Artifacts Generated

- `S[N]_COMPLETION_REPORT.md` - Este reporte
- `PR_CHECKLIST.md` - Checklist para PR
- `S[N]_SPRINT_TRACKING.md` - Tracking del sprint
- [Otros artefactos]

EOF
```

#### 3. Generar PR Checklist
```bash
cat > PR_CHECKLIST.md << 'EOF'
# Pull Request Checklist - Sprint S[N]

## 📋 Pre-Submit Checklist

### Code Quality
- [ ] All files follow project code standards
- [ ] No commented code left behind
- [ ] No debug statements or console.logs
- [ ] No hardcoded values (use config/env vars)
- [ ] No secrets or sensitive data in code

### Testing
- [ ] All unit tests pass locally
- [ ] Integration tests pass (if applicable)
- [ ] Manual testing completed
- [ ] No regression in existing functionality
- [ ] New tests added for new functionality

### Documentation
- [ ] Code is self-documenting or has comments
- [ ] README updated if needed
- [ ] API documentation updated
- [ ] CHANGELOG updated
- [ ] Migration guide included (if breaking changes)

### Contracts & Validation (if applicable)
- [ ] OpenAPI specs validated
- [ ] JSON Schemas validated
- [ ] Protocol Buffers validated
- [ ] No breaking changes OR breaking changes documented

### CI/CD
- [ ] All GitHub Actions workflows pass
- [ ] No new linter errors introduced
- [ ] Build completes successfully
- [ ] Docker images build (if applicable)

---

## 👥 Review Checklist (for Reviewers)

### Architecture
- [ ] Changes align with ENIS v3.0 architecture
- [ ] Follows DNA v3.0 standards
- [ ] No architectural anti-patterns
- [ ] Scalability considerations addressed

### Security
- [ ] No security vulnerabilities introduced
- [ ] Input validation present
- [ ] Authentication/Authorization handled correctly
- [ ] No sensitive data exposure

### Performance
- [ ] No obvious performance issues
- [ ] Appropriate use of caching
- [ ] Database queries optimized (if applicable)
- [ ] Resource usage reasonable

### Maintainability
- [ ] Code is readable and maintainable
- [ ] Appropriate abstractions used
- [ ] No duplication of code
- [ ] Error handling is comprehensive

---

## 🚀 Deployment Checklist (for Merge)

- [ ] All reviews approved
- [ ] CI/CD pipelines green
- [ ] No merge conflicts with develop
- [ ] Version numbers updated (if applicable)
- [ ] Release notes prepared (if applicable)

---

## 📝 Notes for Reviewers

[Cualquier contexto adicional que los reviewers deben saber]

---

**Sprint:** S[N] - [Sprint Name]
**Branch:** feature/s[n]-[branch-suffix]
**Author:** [Tu nombre]
**Date:** $(date)

EOF
```

#### 4. Generar PR Description
```bash
cat > PR_DESCRIPTION.md << 'EOF'
# [Sprint S[N]] [Sprint Name]

## 🎯 Objetivo

[Descripción breve del objetivo del sprint]

## 📦 Entregables

- ✅ [Entregable 1]
- ✅ [Entregable 2]
- ✅ [Entregable 3]

## 🔄 Cambios Principales

### [Categoría 1]
- [Cambio específico 1]
- [Cambio específico 2]

### [Categoría 2]
- [Cambio específico 1]
- [Cambio específico 2]

## 🧪 Testing

- ✅ Unit tests: [X passing]
- ✅ Integration tests: [X passing]
- ✅ Smoke tests: Passed
- ✅ Manual testing: Completed

## 📊 Métricas

- **Files changed:** [N]
- **Lines added:** [N]
- **Lines removed:** [N]
- **Tests added:** [N]

## ⚠️ Breaking Changes

[Si hay breaking changes, listarlos aquí. Si no, poner "None"]

## 📋 Definition of Done

- [x] All entregables completed
- [x] Tests passing
- [x] Documentation updated
- [x] Code reviewed
- [x] No linter errors

## 🔗 Related Issues

Closes #[issue-number]
Refs #[issue-number]

## 📝 Additional Notes

[Cualquier nota adicional para los reviewers]

---

**Checklist completo en:** [PR_CHECKLIST.md](./PR_CHECKLIST.md)
**Reporte completo en:** [S[N]_COMPLETION_REPORT.md](./S[N]_COMPLETION_REPORT.md)

EOF
```

#### 5. Mostrar resumen final
```bash
echo ""
echo "✅ =========================================="
echo "✅  SPRINT S[N] COMPLETED SUCCESSFULLY!"
echo "✅ =========================================="
echo ""
echo "📊 Summary:"
echo "  • Files changed: $(git diff --name-only origin/develop...HEAD | wc -l)"
echo "  • Commits: $(git rev-list --count origin/develop..HEAD)"
echo "  • Branch: $(git branch --show-current)"
echo "  • Status: ✅ READY FOR PR"
echo ""
echo "📄 Reports Generated:"
echo "  • S[N]_COMPLETION_REPORT.md"
echo "  • PR_CHECKLIST.md"
echo "  • PR_DESCRIPTION.md"
echo "  • S[N]_SPRINT_TRACKING.md"
echo ""
echo "📝 Next Actions:"
echo "  1. Review all generated reports"
echo "  2. Create Pull Request using PR_DESCRIPTION.md"
echo "  3. Request reviews from: [Reviewers]"
echo "  4. Share in #contracts-rfcs Slack channel"
echo ""
echo "🔗 Create PR:"
REPO_URL=$(git config --get remote.origin.url | sed 's/\.git$//')
BRANCH_NAME=$(git branch --show-current)
echo "  ${REPO_URL}/compare/develop...${BRANCH_NAME}"
echo ""
echo "🎉 Great work! Sprint S[N] is complete!"
echo ""

# Actualizar tracking file
echo "Updated: $(date)" >> S[N]_SPRINT_TRACKING.md
echo "Status: COMPLETED ✅" >> S[N]_SPRINT_TRACKING.md
```

**✅ Criterios de éxito globales de FASE [N]:**
- [ ] Completion report generado
- [ ] DoD verificado y documentado
- [ ] PR checklist creado
- [ ] PR description creada
- [ ] Resumen final mostrado
- [ ] Todos los artefactos listos

---

## 📊 Execution Summary

Al finalizar todas las fases, el agente AI debe haber:

### ✅ Estructura y Archivos
- [ ] [N] archivos/directorios creados
- [ ] [N] archivos modificados
- [ ] Toda la estructura según especificación

### ✅ Validación y Testing
- [ ] Tests unitarios pasando
- [ ] Validaciones de contratos exitosas
- [ ] Smoke tests completados
- [ ] CI/CD workflows configurados (si aplica)

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
- [ ] [DoD Item 1]
- [ ] [DoD Item 2]
- [ ] [DoD Item 3]
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
   - Actualizar `S[N]_SPRINT_TRACKING.md` al completar cada fase
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

## ✅ Definition of Done (DoD)

**Este sprint se considera completo cuando:**

### Entregables Principales
- [ ] [Entregable 1 específico del sprint]
- [ ] [Entregable 2 específico del sprint]
- [ ] [Entregable 3 específico del sprint]

### Calidad del Código
- [ ] Código sigue estándares del proyecto
- [ ] No hay errores de linter críticos
- [ ] Toda funcionalidad testeada
- [ ] Cobertura de tests ≥ [X]%

### Testing
- [ ] Tests unitarios: [N] creados, todos pasando
- [ ] Tests de integración: [N] creados, todos pasando
- [ ] Smoke tests: Ejecutados y pasando
- [ ] Tests manuales: Completados

### Validación de Contratos (si aplica)
- [ ] OpenAPI specs validados sin errores
- [ ] JSON Schemas válidos
- [ ] Protocol Buffers compilando sin errores
- [ ] Breaking changes documentados
- [ ] Baseline actualizado y firmado

### CI/CD (si aplica)
- [ ] Workflows configurados
- [ ] Todos los pipelines en verde
- [ ] Docker images buildean correctamente
- [ ] Deployments testeados

### Documentación
- [ ] README actualizado con cambios
- [ ] Guías técnicas escritas
- [ ] Ejemplos de uso incluidos
- [ ] Comentarios en código donde sea necesario
- [ ] CHANGELOG actualizado

### Git & PR
- [ ] Branch creado desde develop
- [ ] Commits siguen Conventional Commits
- [ ] Branch pusheado a origin
- [ ] PR checklist completo
- [ ] PR description lista

### Reportes y Artefactos
- [ ] S[N]_COMPLETION_REPORT.md generado
- [ ] PR_CHECKLIST.md generado
- [ ] PR_DESCRIPTION.md generado
- [ ] S[N]_SPRINT_TRACKING.md actualizado
- [ ] Todos los issues documentados

### Preparación para Merge
- [ ] No hay conflictos con develop
- [ ] Todas las verificaciones pasan
- [ ] Reviewers identificados
- [ ] Lista para crear PR

---

## 🔗 Referencias y Links

### Documentación del Proyecto
- [Roadmap General](../roadmaps/agent_contracts_roadmap_2025_2026_detallado.md)
- [Sprint Anterior: S[N-1]](../S[N-1]/S[N-1]_docs.md)
- [Sprint Siguiente: S[N+1]](../S[N+1]/S[N+1]_docs.md)

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
- **[Owner 1]**: [rol] - [contacto]
- **[Owner 2]**: [rol] - [contacto]

### Reviewers Sugeridos
- **Arquitectura**: @architecture-team
- **Contratos**: @contracts-team
- **Seguridad**: @security-team
- **[Otro rol]**: @[team]

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
docker build -t enis/agent-contracts:s[n] .

# Run container
docker run -it enis/agent-contracts:s[n]

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
3. Ejecuta: FASE 0 → FASE 1 → ... → FASE N
4. Reporta el progreso después de cada fase
5. Genera todos los reportes en la fase final
6. No te detengas hasta completar o encontrar un blocker crítico

Comando de inicio sugerido:
"Claude, ejecuta el Sprint S[N] siguiendo el documento 
docs/01-sprint/S[N]/S[N]-[name].md paso por paso. 
Reporta el progreso de cada fase."
```

---


