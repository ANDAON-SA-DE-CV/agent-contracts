# Migration Guide - Universal Production Readiness Framework

**De ENIS a Cualquier Proyecto en 10 Minutos**

---

## 🎯 Objetivo

Llevar el framework de verificación de producción de ENIS a cualquier otro proyecto con configuración automática.

---

## 📋 Requisitos Previos

- Git instalado
- Python 3.8+ (para el script de verificación)
- Bash (para el script de setup)

---

## 🚀 Proceso de Migración (3 Pasos)

### **Paso 1: Copiar Archivos al Nuevo Proyecto**

```bash
# 1. En tu proyecto nuevo
cd /path/to/your-new-project

# 2. Crear estructura de directorios
mkdir -p scripts/verification
mkdir -p docs/04-sprint-builder/verifiers

# 3. Copiar desde ENIS
ENIS_PATH="/path/to/ENIS/inference-service"

# Copiar framework universal
cp "$ENIS_PATH/docs/04-sprint-builder/verifiers/UNIVERSAL_PRODUCTION_READY_FRAMEWORK.md" \
   docs/04-sprint-builder/verifiers/

# Copiar script de setup
cp "$ENIS_PATH/scripts/verification/setup-verification.sh" \
   scripts/verification/

# Copiar script de verificación (base)
cp "$ENIS_PATH/scripts/verification/sprint/verify_sprint.py" \
   scripts/verification/verify-production-ready.py

# Dar permisos de ejecución
chmod +x scripts/verification/setup-verification.sh
chmod +x scripts/verification/verify-production-ready.py
```

### **Paso 2: Configurar Automáticamente**

```bash
# Ejecutar setup automático
./scripts/verification/setup-verification.sh
```

**Esto generará automáticamente:**
- ✅ `.verification-config.json` con configuración del proyecto
- ✅ Estructura de directorios necesaria
- ✅ Auto-detección de lenguaje, tipo y estructura

**Ejemplo de salida:**
```
🚀 Universal Production Readiness Framework Setup
==================================================

✓ Project: my-awesome-api
✓ Language: python
✓ Type: api
✓ Structure detected

✅ Configuration created: .verification-config.json
✅ Directory structure created

🎉 Setup completed successfully!

Next steps:
1. Review .verification-config.json
2. Run: python scripts/verification/verify-production-ready.py
```

### **Paso 3: Verificar y Personalizar**

```bash
# 1. Revisar configuración generada
cat .verification-config.json

# 2. Ajustar según necesidades (opcional)
vim .verification-config.json

# 3. Ejecutar primera verificación
python scripts/verification/verify-production-ready.py

# O con número de sprint específico
python scripts/verification/verify-production-ready.py 1
```

---

## 📝 Configuración Generada

El setup automático genera un archivo `.verification-config.json`:

```json
{
  "project": {
    "name": "my-project",           // Auto-detectado del directorio
    "type": "api",                   // Auto-detectado (api/web/cli/library)
    "language": "python",            // Auto-detectado (python/js/ts/go/etc)
    "framework": null                // Puedes configurar manualmente
  },
  "structure": {
    "docs_dir": "docs",              // Auto-detectado
    "src_dir": "src",                // Auto-detectado
    "tests_dir": "tests",            // Auto-detectado
    "reports_dir": "docs/reports"    // Generado automáticamente
  },
  "thresholds": {
    "critical_issues_max": 0,        // Personalizable
    "high_issues_max": 3,
    "medium_issues_max": 10
  }
}
```

---

## 🔧 Personalizaciones Comunes

### **1. Ajustar Thresholds**

```json
{
  "thresholds": {
    "critical_issues_max": 0,    // Más estricto
    "high_issues_max": 5,        // Más permisivo
    "medium_issues_max": 20
  }
}
```

### **2. Configurar Comandos Específicos**

```json
{
  "language_specific": {
    "python": {
      "test_command": "pytest --cov --cov-report=html",
      "lint_command": "pylint src/",
      "format_command": "black --check src/"
    }
  }
}
```

### **3. Ajustar Rutas de Reportes**

```json
{
  "sprints": {
    "docs_pattern": "documentation/sprints/S{{N}}/*.md",
    "report_pattern": "reports/sprint-{{N}}-verification.md"
  }
}
```

### **4. Configurar Exclusiones**

```json
{
  "exclusions": {
    "files": ["*.md", "*.txt", ".env", "LICENSE"],
    "directories": ["node_modules", "venv", "dist", "build", "coverage"]
  }
}
```

---

## 📊 Ejemplos por Tipo de Proyecto

### **Proyecto Python FastAPI (Similar a ENIS)**

```bash
# Setup automático detecta:
# - Language: python
# - Type: api
# - Structure: src/, tests/, docs/

./scripts/verification/setup-verification.sh
# Genera configuración óptima para FastAPI

python scripts/verification/verify-production-ready.py 2
```

### **Proyecto Node.js Express**

```bash
# Setup automático detecta:
# - Language: javascript (o typescript)
# - Type: api
# - Structure: src/, test/, docs/

./scripts/verification/setup-verification.sh

# Ajustar comandos de test (opcional)
# "test_command": "npm run test:coverage"

node scripts/verification/verify-production-ready.js 3
```

### **Proyecto Go CLI**

```bash
# Setup automático detecta:
# - Language: go
# - Type: cli
# - Structure: cmd/, internal/, tests/

./scripts/verification/setup-verification.sh

# Verificar
python scripts/verification/verify-production-ready.py 1
```

### **Proyecto React Frontend**

```bash
# Setup automático detecta:
# - Language: typescript
# - Type: web
# - Structure: src/, src/__tests__/

./scripts/verification/setup-verification.sh

# Ajustar para frontend
# "test_command": "npm run test -- --coverage"

npm run verify-sprint 2
```

---

## 🔄 Integración con CI/CD

### **GitHub Actions**

```yaml
# .github/workflows/sprint-verification.yml
name: Sprint Verification

on:
  pull_request:
    branches: [develop, main]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Run Sprint Verification
        run: |
          python scripts/verification/verify-production-ready.py
      
      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: verification-report
          path: docs/reports/SPRINT_*_VERIFICATION.md
```

### **GitLab CI**

```yaml
# .gitlab-ci.yml
sprint-verification:
  stage: test
  script:
    - python scripts/verification/verify-production-ready.py
  artifacts:
    paths:
      - docs/reports/SPRINT_*_VERIFICATION.md
    expire_in: 30 days
```

---

## ✅ Checklist de Migración

- [ ] **Paso 1:** Copiar archivos del framework
- [ ] **Paso 2:** Ejecutar `./scripts/verification/setup-verification.sh`
- [ ] **Paso 3:** Revisar `.verification-config.json` generado
- [ ] **Paso 4:** Ajustar thresholds según proyecto
- [ ] **Paso 5:** Configurar comandos específicos del lenguaje
- [ ] **Paso 6:** Ejecutar primera verificación
- [ ] **Paso 7:** Revisar reporte generado
- [ ] **Paso 8:** Integrar con CI/CD (opcional)
- [ ] **Paso 9:** Documentar proceso para el equipo
- [ ] **Paso 10:** Celebrar 🎉

---

## 🆘 Troubleshooting

### **Problema: "Configuration file not found"**

```bash
# Solución: Ejecutar setup primero
./scripts/verification/setup-verification.sh
```

### **Problema: "No se pudo detectar el lenguaje"**

```bash
# Solución: Configurar manualmente
cat > .verification-config.json << EOF
{
  "project": {
    "language": "python",  # Especificar manualmente
    "type": "api"
  }
}
EOF
```

### **Problema: "Test command not found"**

```bash
# Solución: Configurar comando correcto en .verification-config.json
{
  "language_specific": {
    "python": {
      "test_command": "pytest"  # Ajustar comando
    }
  }
}
```

### **Problema: "Permission denied"**

```bash
# Solución: Dar permisos de ejecución
chmod +x scripts/verification/setup-verification.sh
chmod +x scripts/verification/verify-production-ready.py
```

---

## 📚 Recursos Adicionales

- **Framework Universal:** `docs/04-sprint-builder/verifiers/UNIVERSAL_PRODUCTION_READY_FRAMEWORK.md`
- **Framework ENIS:** `docs/04-sprint-builder/verifiers/PROMPT_VERIFICADOR_PRODUCTION_READY.md`
- **Scripts:** `scripts/verification/`

---

## 🎯 Resultado Esperado

Después de la migración tendrás:

✅ **Framework universal** instalado en tu proyecto  
✅ **Configuración automática** adaptada a tu proyecto  
✅ **Verificación de calidad** lista para usar  
✅ **Reportes estandarizados** en cada sprint  
✅ **Integración CI/CD** opcional configurada  

**Tiempo total: 10 minutos**  
**Complejidad: Baja**  
**Mantenimiento: Mínimo**

---

## 💡 Tips Finales

1. **Empieza simple:** Usa configuración auto-generada primero
2. **Ajusta gradualmente:** Personaliza según necesidades
3. **Documenta cambios:** Mantén un registro de ajustes
4. **Comparte con el equipo:** Asegura que todos usen el framework
5. **Mantén actualizado:** Sincroniza mejoras de ENIS

---

**¡Listo para migrar! 🚀**

