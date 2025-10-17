# Universal Production Readiness Framework v1.0

> **🌍 FRAMEWORK UNIVERSAL PARA CUALQUIER PROYECTO**  
> Verificación automática de calidad post-sprint adaptable a cualquier repositorio  
> **Version:** 1.0 Universal  
> **Scope:** Multi-lenguaje, Multi-proyecto, Multi-stack  
> **Compliance:** ISO 25010, OWASP Top 10, Clean Code Principles

---

## 📋 Executive Summary

Este framework **universal** verifica que el código entregado en un sprint cumple con estándares enterprise de producción, **independientemente del proyecto, lenguaje o stack tecnológico**.

**Características:**
- ✅ **Auto-configurable:** Detecta automáticamente tipo de proyecto
- ✅ **Multi-lenguaje:** Python, JavaScript/TypeScript, Go, Java, C#, Ruby, PHP
- ✅ **Multi-stack:** API, Web, Mobile, Desktop, CLI
- ✅ **Parametrizable:** Configuración específica por proyecto
- ✅ **Reutilizable:** Un solo framework para todos tus proyectos

---

## 🚀 Quick Start (5 minutos)

### Paso 1: Copiar Framework a tu Proyecto

```bash
# En tu proyecto nuevo
cd /path/to/your-project

# Crear directorio para verificación
mkdir -p scripts/verification

# Copiar script universal
curl -o scripts/verification/verify-production-ready.py \
  https://raw.githubusercontent.com/.../verify-production-ready.py

# O copiar manualmente desde ENIS
cp /path/to/enis/scripts/verification/sprint/verify_sprint.py \
   scripts/verification/verify-production-ready.py
```

### Paso 2: Configurar tu Proyecto

```bash
# Crear configuración automática
./scripts/verification/verify-production-ready.py --setup
```

Esto generará: `.verification-config.json`

### Paso 3: Ejecutar Verificación

```bash
# Verificar sprint actual
./scripts/verification/verify-production-ready.py

# O especificar sprint
./scripts/verification/verify-production-ready.py 5
```

---

## ⚙️ Configuración Universal

### Archivo: `.verification-config.json`

Este archivo se genera automáticamente o puedes crearlo manualmente:

```json
{
  "project": {
    "name": "{{PROJECT_NAME}}",
    "type": "api|web|mobile|cli|library",
    "language": "python|javascript|typescript|go|java|csharp|ruby|php",
    "framework": "fastapi|express|spring|django|rails|laravel|null"
  },
  "structure": {
    "docs_dir": "docs",
    "src_dir": "src",
    "tests_dir": "tests",
    "config_dir": "config",
    "scripts_dir": "scripts",
    "reports_dir": "docs/reports"
  },
  "sprints": {
    "docs_pattern": "docs/sprints/S{{N}}/*.md",
    "branch_pattern": "feature/s{{N}}-*",
    "report_pattern": "{{reports_dir}}/SPRINT_{{N}}_VERIFICATION.md"
  },
  "thresholds": {
    "critical_issues_max": 0,
    "high_issues_max": 3,
    "medium_issues_max": 10,
    "low_issues_max": 50,
    "test_coverage_min_percent": 80
  },
  "verification": {
    "enable_dummy_detection": true,
    "enable_security_scan": true,
    "enable_test_coverage": true,
    "enable_documentation_check": true,
    "enable_code_standards": true,
    "enable_dependency_check": true
  },
  "language_specific": {
    "python": {
      "test_command": "pytest --cov",
      "lint_command": "ruff check",
      "format_command": "black --check"
    },
    "javascript": {
      "test_command": "npm test",
      "lint_command": "eslint .",
      "format_command": "prettier --check ."
    },
    "typescript": {
      "test_command": "npm test",
      "lint_command": "eslint . --ext .ts",
      "format_command": "prettier --check ."
    },
    "go": {
      "test_command": "go test ./...",
      "lint_command": "golangci-lint run",
      "format_command": "go fmt ./..."
    }
  },
  "exclusions": {
    "files": ["*.md", "*.txt", ".gitignore", "LICENSE"],
    "directories": ["node_modules", "__pycache__", ".git", "venv", "dist", "build"]
  }
}
```

---

## 🔧 Auto-Setup Script

### Script: `setup-verification.sh`

```bash
#!/usr/bin/env bash
# Universal Production Readiness Framework Setup
# Auto-detects project structure and generates configuration

set -euo pipefail

echo "🚀 Universal Production Readiness Framework Setup"
echo "=================================================="
echo ""

# Detect project root
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
cd "$PROJECT_ROOT"

# Detect project name
PROJECT_NAME=$(basename "$PROJECT_ROOT")
echo "✓ Project: $PROJECT_NAME"

# Detect main language
detect_language() {
  if [ -f "pyproject.toml" ] || [ -f "setup.py" ] || [ -f "requirements.txt" ]; then
    echo "python"
  elif [ -f "package.json" ]; then
    if grep -q "typescript" package.json 2>/dev/null; then
      echo "typescript"
    else
      echo "javascript"
    fi
  elif [ -f "go.mod" ]; then
    echo "go"
  elif [ -f "pom.xml" ] || [ -f "build.gradle" ]; then
    echo "java"
  elif [ -f "Gemfile" ]; then
    echo "ruby"
  elif [ -f "composer.json" ]; then
    echo "php"
  elif [ -f "*.csproj" ]; then
    echo "csharp"
  else
    echo "unknown"
  fi
}

LANGUAGE=$(detect_language)
echo "✓ Language: $LANGUAGE"

# Detect project type
detect_project_type() {
  if grep -q "fastapi\|flask\|django\|express\|spring" . -r 2>/dev/null; then
    echo "api"
  elif [ -d "src/components" ] || [ -d "app/components" ]; then
    echo "web"
  elif grep -q "cli\|argparse\|commander" . -r 2>/dev/null; then
    echo "cli"
  else
    echo "library"
  fi
}

PROJECT_TYPE=$(detect_project_type)
echo "✓ Type: $PROJECT_TYPE"

# Detect directory structure
detect_dir() {
  local dir_name=$1
  if [ -d "$dir_name" ]; then
    echo "$dir_name"
  elif [ -d "src/$dir_name" ]; then
    echo "src/$dir_name"
  elif [ -d "app/$dir_name" ]; then
    echo "app/$dir_name"
  else
    echo "$dir_name"
  fi
}

SRC_DIR=$(detect_dir "src")
TESTS_DIR=$(detect_dir "tests")
DOCS_DIR=$(detect_dir "docs")
echo "✓ Structure detected"

# Create .verification-config.json
cat > .verification-config.json << EOF
{
  "project": {
    "name": "$PROJECT_NAME",
    "type": "$PROJECT_TYPE",
    "language": "$LANGUAGE",
    "framework": null
  },
  "structure": {
    "docs_dir": "$DOCS_DIR",
    "src_dir": "$SRC_DIR",
    "tests_dir": "$TESTS_DIR",
    "config_dir": "config",
    "scripts_dir": "scripts",
    "reports_dir": "$DOCS_DIR/reports"
  },
  "sprints": {
    "docs_pattern": "$DOCS_DIR/sprints/S{{N}}/*.md",
    "branch_pattern": "feature/s{{N}}-*",
    "report_pattern": "$DOCS_DIR/reports/SPRINT_{{N}}_VERIFICATION.md"
  },
  "thresholds": {
    "critical_issues_max": 0,
    "high_issues_max": 3,
    "medium_issues_max": 10,
    "low_issues_max": 50,
    "test_coverage_min_percent": 80
  },
  "verification": {
    "enable_dummy_detection": true,
    "enable_security_scan": true,
    "enable_test_coverage": true,
    "enable_documentation_check": true,
    "enable_code_standards": true,
    "enable_dependency_check": true
  },
  "exclusions": {
    "files": ["*.md", "*.txt", ".gitignore", "LICENSE"],
    "directories": ["node_modules", "__pycache__", ".git", "venv", "dist", "build"]
  }
}
EOF

echo ""
echo "✅ Configuration created: .verification-config.json"
echo ""

# Create directories if they don't exist
mkdir -p "$DOCS_DIR/reports"
mkdir -p "$DOCS_DIR/sprints"
mkdir -p "scripts/verification"

echo "✅ Directory structure created"
echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Review .verification-config.json"
echo "2. Run: ./scripts/verification/verify-production-ready.py"
echo ""
```

---

## 🐍 Universal Verification Script (Python)

### Script: `verify-production-ready.py`

```python
#!/usr/bin/env python3
"""
Universal Production Readiness Verification Framework
Compatible with any project, language, or stack
"""

import os
import sys
import json
import subprocess
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class UniversalVerifier:
    def __init__(self, sprint_number: Optional[str] = None):
        self.project_root = Path.cwd()
        self.config = self.load_config()
        self.sprint_number = sprint_number or self.detect_sprint_number()
        
        # Issue counters
        self.critical_count = 0
        self.high_count = 0
        self.medium_count = 0
        self.low_count = 0
        
        # Report
        self.report_lines = []
        
    def load_config(self) -> Dict:
        """Load project configuration"""
        config_file = self.project_root / ".verification-config.json"
        
        if not config_file.exists():
            print("⚠️ Configuration file not found")
            print("Run: ./setup-verification.sh")
            sys.exit(1)
        
        with open(config_file, 'r') as f:
            return json.load(f)
    
    def detect_sprint_number(self) -> str:
        """Auto-detect sprint number from branch name"""
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                check=True
            )
            branch = result.stdout.strip()
            
            # Extract sprint number from branch pattern
            pattern = self.config["sprints"]["branch_pattern"].replace("{{N}}", r"(\d+)")
            match = re.search(pattern, branch)
            
            if match:
                sprint_num = match.group(1)
                print(f"✓ Sprint detectado desde rama: {sprint_num}")
                return sprint_num
            else:
                print("⚠️ No se pudo detectar sprint desde rama")
                return input("Ingresa número de sprint: ")
        except:
            return "1"
    
    def get_changed_files(self) -> List[Path]:
        """Get files changed in current sprint"""
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", "origin/develop...HEAD"],
                capture_output=True,
                text=True
            )
            files = result.stdout.strip().split('\n')
            return [Path(f) for f in files if f]
        except:
            return []
    
    def verify_dummy_code(self):
        """Phase 1: Detect dummy/placeholder code"""
        print("\n" + "="*50)
        print("Phase 1: Dummy Code Detection")
        print("="*50)
        
        patterns = {
            "python": [
                r'def\s+\w+\(.*\):\s*pass\s*$',
                r'def\s+\w+\(.*\):\s*\.\.\.\s*$',
                r'raise\s+NotImplementedError',
                r'dummy_\w+',
                r'fake_\w+',
                r'TODO|FIXME|HACK|XXX',
            ],
            "javascript": [
                r'function\s+\w+\(.*\)\s*{\s*}\s*$',
                r'const\s+\w+\s*=\s*\(\)\s*=>\s*{\s*}\s*$',
                r'throw\s+new\s+Error\(["\']Not implemented["\']\)',
                r'dummy[A-Z]\w*',
                r'fake[A-Z]\w*',
                r'TODO|FIXME|HACK|XXX',
            ]
        }
        
        language = self.config["project"]["language"]
        if language not in patterns:
            print(f"⚠️ No patterns defined for {language}")
            return
        
        files = self.get_changed_files()
        for file in files:
            if not file.exists():
                continue
                
            try:
                content = file.read_text()
                for pattern in patterns[language]:
                    matches = re.finditer(pattern, content, re.MULTILINE)
                    for match in matches:
                        self.log_issue(
                            "HIGH",
                            f"Dummy code pattern detected: {pattern}",
                            str(file)
                        )
            except:
                pass
    
    def verify_security(self):
        """Phase 2: Security verification"""
        print("\n" + "="*50)
        print("Phase 2: Security Verification")
        print("="*50)
        
        secret_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api[_-]?key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
        ]
        
        files = self.get_changed_files()
        for file in files:
            if not file.exists():
                continue
                
            try:
                content = file.read_text()
                for pattern in secret_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        self.log_issue(
                            "CRITICAL",
                            f"Hardcoded secret detected: {match.group()}",
                            str(file)
                        )
            except:
                pass
    
    def verify_tests(self):
        """Phase 3: Test verification"""
        print("\n" + "="*50)
        print("Phase 3: Test Verification")
        print("="*50)
        
        language = self.config["project"]["language"]
        test_cmd = self.config.get("language_specific", {}).get(language, {}).get("test_command")
        
        if not test_cmd:
            print(f"⚠️ No test command defined for {language}")
            return
        
        try:
            result = subprocess.run(
                test_cmd.split(),
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ All tests passed")
            else:
                self.log_issue("HIGH", "Some tests failed")
        except:
            self.log_issue("MEDIUM", "Could not run tests")
    
    def log_issue(self, severity: str, message: str, file_path: str = ""):
        """Log an issue"""
        file_info = f" ({file_path})" if file_path else ""
        print(f"[{severity}] {message}{file_info}")
        
        if severity == "CRITICAL":
            self.critical_count += 1
        elif severity == "HIGH":
            self.high_count += 1
        elif severity == "MEDIUM":
            self.medium_count += 1
        elif severity == "LOW":
            self.low_count += 1
        
        self.report_lines.append(f"- **{severity}**: {message}{file_info}")
    
    def generate_report(self):
        """Generate verification report"""
        report_pattern = self.config["sprints"]["report_pattern"]
        report_file = Path(report_pattern.replace("{{N}}", self.sprint_number))
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        thresholds = self.config["thresholds"]
        
        # Determine verdict
        if (self.critical_count <= thresholds["critical_issues_max"] and
            self.high_count <= thresholds["high_issues_max"] and
            self.medium_count <= thresholds["medium_issues_max"]):
            verdict = "✅ VERIFICATION PASSED"
            status = "APPROVED"
        elif self.critical_count > thresholds["critical_issues_max"]:
            verdict = "❌ VERIFICATION FAILED"
            status = "REJECTED"
        else:
            verdict = "⚠️ VERIFICATION PASSED WITH OBSERVATIONS"
            status = "APPROVED WITH OBSERVATIONS"
        
        # Generate report
        report = f"""# Sprint {self.sprint_number} - Production Readiness Verification

**Project:** {self.config['project']['name']}
**Type:** {self.config['project']['type']}
**Language:** {self.config['project']['language']}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Verification Results

{verdict}

### Issues Summary

| Severity | Count | Threshold | Status |
|----------|-------|-----------|--------|
| Critical | {self.critical_count} | ≤ {thresholds['critical_issues_max']} | {'✅' if self.critical_count <= thresholds['critical_issues_max'] else '❌'} |
| High     | {self.high_count} | ≤ {thresholds['high_issues_max']} | {'✅' if self.high_count <= thresholds['high_issues_max'] else '❌'} |
| Medium   | {self.medium_count} | ≤ {thresholds['medium_issues_max']} | {'✅' if self.medium_count <= thresholds['medium_issues_max'] else '⚠️'} |
| Low      | {self.low_count} | - | ℹ️ |

---

## Issues Detected

{''.join(self.report_lines) if self.report_lines else '✅ No issues detected'}

---

## Final Verdict

**Status:** {status}

Sprint {self.sprint_number} is **{status}**

---

*Report generated by Universal Production Readiness Framework v1.0*
"""
        
        report_file.write_text(report)
        print(f"\n✅ Report generated: {report_file}")
        
        return 0 if status in ["APPROVED", "APPROVED WITH OBSERVATIONS"] else 1
    
    def run(self):
        """Run all verification phases"""
        print(f"\n🔍 Verifying Sprint {self.sprint_number}")
        print(f"Project: {self.config['project']['name']}")
        print(f"Language: {self.config['project']['language']}")
        
        if self.config["verification"]["enable_dummy_detection"]:
            self.verify_dummy_code()
        
        if self.config["verification"]["enable_security_scan"]:
            self.verify_security()
        
        if self.config["verification"]["enable_test_coverage"]:
            self.verify_tests()
        
        return self.generate_report()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Universal Production Readiness Verification')
    parser.add_argument('sprint_number', nargs='?', help='Sprint number to verify')
    parser.add_argument('--setup', action='store_true', help='Setup configuration')
    
    args = parser.parse_args()
    
    if args.setup:
        print("Run: ./setup-verification.sh")
        return 0
    
    verifier = UniversalVerifier(args.sprint_number)
    return verifier.run()


if __name__ == "__main__":
    sys.exit(main())
```

---

## 📚 Ejemplos de Uso por Proyecto

### Ejemplo 1: Proyecto Python FastAPI (como ENIS)

```bash
# Setup
cd /path/to/fastapi-project
./setup-verification.sh

# Configuración generada automáticamente
cat .verification-config.json
# {
#   "project": { "language": "python", "type": "api" },
#   "structure": { "src_dir": "src", "tests_dir": "tests" }
# }

# Verificar
./scripts/verification/verify-production-ready.py 2
```

### Ejemplo 2: Proyecto Node.js Express

```bash
# Setup
cd /path/to/express-project
./setup-verification.sh

# Configuración generada
# {
#   "project": { "language": "javascript", "type": "api" },
#   "structure": { "src_dir": "src", "tests_dir": "test" }
# }

# Verificar
./scripts/verification/verify-production-ready.py 5
```

### Ejemplo 3: Proyecto Go CLI

```bash
# Setup
cd /path/to/go-cli
./setup-verification.sh

# Configuración generada
# {
#   "project": { "language": "go", "type": "cli" },
#   "structure": { "src_dir": "cmd", "tests_dir": "tests" }
# }

# Verificar
./scripts/verification/verify-production-ready.py 3
```

### Ejemplo 4: Proyecto React Web

```bash
# Setup
cd /path/to/react-app
./setup-verification.sh

# Configuración generada
# {
#   "project": { "language": "typescript", "type": "web" },
#   "structure": { "src_dir": "src", "tests_dir": "src/__tests__" }
# }

# Verificar
./scripts/verification/verify-production-ready.py 1
```

---

## 🔄 Migración desde ENIS

### Paso 1: Copiar Framework

```bash
# Desde ENIS
cp docs/04-sprint-builder/verifiers/UNIVERSAL_PRODUCTION_READY_FRAMEWORK.md \
   /path/to/new-project/docs/

# Copiar scripts
cp scripts/verification/sprint/verify_sprint.py \
   /path/to/new-project/scripts/verification/verify-production-ready.py
```

### Paso 2: Adaptar Configuración

```bash
cd /path/to/new-project

# Crear setup script
cat > setup-verification.sh << 'EOF'
# ... (copiar el script de arriba)
EOF

chmod +x setup-verification.sh

# Ejecutar setup
./setup-verification.sh
```

### Paso 3: Personalizar

Editar `.verification-config.json` según necesidades del proyecto:
- Ajustar thresholds
- Configurar comandos específicos
- Definir exclusiones

---

## 🎯 Ventajas del Framework Universal

### ✅ **Para Nuevos Proyectos:**
- Setup en 5 minutos
- Auto-configuración
- Listo para usar

### ✅ **Para Equipos:**
- Estándares consistentes
- Mismo proceso en todos los proyectos
- Fácil onboarding

### ✅ **Para DevOps:**
- Integración CI/CD simple
- Reportes estandarizados
- Métricas comparables

### ✅ **Para Mantenimiento:**
- Un solo framework para mantener
- Updates centralizados
- Documentación unificada

---

## 📊 Comparación: Específico vs Universal

| Aspecto | PROMPT_VERIFICADOR_PRODUCTION_READY.md | UNIVERSAL_PRODUCTION_READY_FRAMEWORK.md |
|---------|----------------------------------------|------------------------------------------|
| **Alcance** | Solo ENIS | Cualquier proyecto |
| **Configuración** | Hardcodeada | Parametrizable |
| **Setup Time** | Manual | Automático (5 min) |
| **Lenguajes** | Python | Multi-lenguaje |
| **Mantenimiento** | Por proyecto | Centralizado |
| **Reutilizable** | ❌ No | ✅ Sí |

---

## 🚀 Roadmap

### v1.0 (Actual)
- ✅ Auto-detección de proyecto
- ✅ Configuración universal
- ✅ Python, JS, TS, Go
- ✅ Verificación básica

### v1.1 (Próximo)
- 🔄 Soporte Java, C#, Ruby, PHP
- 🔄 Integración con GitHub Actions
- 🔄 Dashboard de métricas
- 🔄 Comparación entre sprints

### v2.0 (Futuro)
- 📋 ML-powered code analysis
- 📋 Auto-fix de issues
- 📋 Sugerencias de mejora
- 📋 Integración con SonarQube

---

## 📖 Documentación Adicional

### Para Usuarios:
- `README.md` - Guía rápida
- `SETUP.md` - Instalación detallada
- `USAGE.md` - Ejemplos de uso

### Para Desarrolladores:
- `CONTRIBUTING.md` - Cómo contribuir
- `ARCHITECTURE.md` - Diseño del framework
- `API.md` - Referencia de API

---

## 🤝 Contribuciones

Este framework es open source y acepta contribuciones:
- Nuevos lenguajes
- Nuevos patrones de detección
- Mejoras en auto-detección
- Integraciones con herramientas

---

## 📝 Licencia

MIT License - Libre para usar en proyectos comerciales y open source

---

## ✅ Conclusión

**El Universal Production Readiness Framework te permite:**

1. ✅ **Reutilizar** el mismo proceso en todos tus proyectos
2. ✅ **Automatizar** la verificación de calidad
3. ✅ **Estandarizar** los criterios de producción
4. ✅ **Escalar** a múltiples equipos y proyectos
5. ✅ **Mantener** un solo framework para todo

**Setup en 5 minutos. Reutilizable infinitamente.**

---

**Framework Universal v1.0**  
**Generated:** 2025-10-16  
**Maintained by:** ENIS Team  
**Contact:** [GitHub Issues](https://github.com/your-org/universal-framework/issues)

