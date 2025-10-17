# Universal Production Readiness Framework Setup (PowerShell)
# Auto-detects project structure and generates configuration

param(
    [switch]$Debug
)

Write-Host "🚀 Universal Production Readiness Framework Setup" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Detect project root
try {
    $PROJECT_ROOT = git rev-parse --show-toplevel 2>$null
    if (-not $PROJECT_ROOT) {
        $PROJECT_ROOT = Get-Location
    }
} catch {
    $PROJECT_ROOT = Get-Location
}

Set-Location $PROJECT_ROOT

# Detect project name
$PROJECT_NAME = Split-Path -Leaf $PROJECT_ROOT
Write-Host "✓ Project: $PROJECT_NAME" -ForegroundColor Green

# Detect main language
function Detect-Language {
    if (Test-Path "pyproject.toml" -or Test-Path "setup.py" -or Test-Path "requirements.txt") {
        return "python"
    } elseif (Test-Path "package.json") {
        $packageContent = Get-Content "package.json" -Raw -ErrorAction SilentlyContinue
        if ($packageContent -and $packageContent -match "typescript") {
            return "typescript"
        } else {
            return "javascript"
        }
    } elseif (Test-Path "go.mod") {
        return "go"
    } elseif (Test-Path "pom.xml" -or Test-Path "build.gradle") {
        return "java"
    } elseif (Test-Path "Gemfile") {
        return "ruby"
    } elseif (Test-Path "composer.json") {
        return "php"
    } elseif (Get-ChildItem -Filter "*.csproj" -ErrorAction SilentlyContinue) {
        return "csharp"
    } else {
        return "unknown"
    }
}

$LANGUAGE = Detect-Language
Write-Host "✓ Language: $LANGUAGE" -ForegroundColor Green

# Detect project type
function Detect-ProjectType {
    $searchPatterns = @("fastapi", "flask", "django", "express", "spring")
    foreach ($pattern in $searchPatterns) {
        $found = Get-ChildItem -Recurse -Include "*.py", "*.js", "*.ts", "*.java" -ErrorAction SilentlyContinue | 
                 Select-String -Pattern $pattern -Quiet
        if ($found) {
            return "api"
        }
    }
    
    if ((Test-Path "src/components") -or (Test-Path "app/components")) {
        return "web"
    }
    
    $cliPatterns = @("cli", "argparse", "commander")
    foreach ($pattern in $cliPatterns) {
        $found = Get-ChildItem -Recurse -Include "*.py", "*.js", "*.ts" -ErrorAction SilentlyContinue | 
                 Select-String -Pattern $pattern -Quiet
        if ($found) {
            return "cli"
        }
    }
    
    return "library"
}

$PROJECT_TYPE = Detect-ProjectType
Write-Host "✓ Type: $PROJECT_TYPE" -ForegroundColor Green

# Detect directory structure
function Detect-Dir {
    param($dirName)
    
    if (Test-Path $dirName) {
        return $dirName
    } elseif (Test-Path "src/$dirName") {
        return "src/$dirName"
    } elseif (Test-Path "app/$dirName") {
        return "app/$dirName"
    } else {
        return $dirName
    }
}

$SRC_DIR = Detect-Dir "src"
$TESTS_DIR = Detect-Dir "tests"
$DOCS_DIR = Detect-Dir "docs"
Write-Host "✓ Structure detected" -ForegroundColor Green

# Create .verification-config.json
$config = @{
    project = @{
        name = $PROJECT_NAME
        type = $PROJECT_TYPE
        language = $LANGUAGE
        framework = $null
    }
    structure = @{
        docs_dir = $DOCS_DIR
        src_dir = $SRC_DIR
        tests_dir = $TESTS_DIR
        config_dir = "config"
        scripts_dir = "scripts"
        reports_dir = "$DOCS_DIR/reports"
    }
    sprints = @{
        docs_pattern = "$DOCS_DIR/01-sprint/S{{N}}/*.md"
        branch_pattern = "feature/s{{N}}-*"
        report_pattern = "$DOCS_DIR/reports/SPRINT_{{N}}_VERIFICATION.md"
    }
    thresholds = @{
        critical_issues_max = 0
        high_issues_max = 3
        medium_issues_max = 10
        low_issues_max = 50
        test_coverage_min_percent = 80
    }
    verification = @{
        enable_dummy_detection = $true
        enable_security_scan = $true
        enable_test_coverage = $true
        enable_documentation_check = $true
        enable_code_standards = $true
        enable_dependency_check = $true
    }
    exclusions = @{
        files = @("*.md", "*.txt", ".gitignore", "LICENSE")
        directories = @("node_modules", "__pycache__", ".git", "venv", "dist", "build")
    }
    language_specific = @{
        python = @{
            test_command = "python -m pytest --cov=src --cov-report=term-missing"
        }
        javascript = @{
            test_command = "npm test"
        }
        typescript = @{
            test_command = "npm test"
        }
    }
}

$configJson = $config | ConvertTo-Json -Depth 10
$configJson | Out-File -FilePath ".verification-config.json" -Encoding UTF8

Write-Host ""
Write-Host "✅ Configuration created: .verification-config.json" -ForegroundColor Green
Write-Host ""

# Create directories if they don't exist
$directories = @(
    "$DOCS_DIR/reports",
    "$DOCS_DIR/sprints", 
    "scripts/verification"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

Write-Host "✅ Directory structure created" -ForegroundColor Green
Write-Host ""
Write-Host "🎉 Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Review .verification-config.json" -ForegroundColor Yellow
Write-Host "2. Run: python scripts/verification/verify-production-ready.py" -ForegroundColor Yellow
Write-Host ""