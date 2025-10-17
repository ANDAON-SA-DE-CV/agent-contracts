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