# 🏗️ Sprint Builder — Sistema de Construcción y Verificación

> **Sistema Dual: GPT-5 Genera → Claude Verifica → Claude Ejecuta**

---

## 📁 Estructura de Directorios

```
docs/03-sprint-builder/
├── README.md                          ← Este archivo (índice principal)
├── README_SISTEMA_DUAL.md             ← Guía completa de uso
│
├── generators/                        ← Prompts para GENERAR sprints
│   ├── PROMPT_GENERATOR_ALL_SPRINTS.md
│   └── README.md
│
└── verifiers/                         ← Prompts para VERIFICAR sprints
    ├── PROMPT_VERIFICADOR_ALL_SPRINTS.md
    └── README.md
```

---

## 🎯 ¿Qué es el Sprint Builder?

Un **sistema de dos pasos** que combina las fortalezas de GPT-5 y Claude para crear documentos de sprint de alta calidad:

### 1️⃣ **GENERACIÓN** (GPT-5)
- **Rápido**: Genera documento completo en 5-10 minutos
- **Autocontenido**: No requiere acceso al proyecto
- **Creativo**: Propone soluciones innovadoras
- **Completo**: >2500 líneas con todo el código necesario

### 2️⃣ **VERIFICACIÓN** (Claude)
- **Exhaustivo**: Verifica 7 dimensiones de calidad
- **Contextual**: Consulta roadmap, template y sprints anteriores
- **Preciso**: Genera patches específicos del proyecto
- **Ejecutable**: Produce comandos listos para correr

---

## 🚀 Inicio Rápido

### Para generar cualquier Sprint:

```bash
# PASO 1: Generar con GPT-5
# ------------------------
# 1. Abrir: generators/PROMPT_GENERATOR_ALL_SPRINTS.md
# 2. Copiar contenido desde "---INICIO DEL PROMPT---"
# 3. Pegar en https://chat.openai.com (GPT-5)
# 4. Copiar resultado completo

# PASO 2: Guardar archivo generado
# ---------------------------------
mkdir -p docs/01-sprint/S[N]
# Pegar en: docs/01-sprint/S[N]/S[N]_[nombre_sprint].md

# PASO 3: Verificar con Claude
# -----------------------------
# 1. Abrir: verifiers/PROMPT_VERIFICADOR_ALL_SPRINTS.md
# 2. Copiar contenido desde "---INICIO DEL PROMPT---"
# 3. Pegar en Cursor AI (Claude)
# 4. Responder: "Léelo desde docs/01-sprint/S[N]/S[N]_[nombre_sprint].md"

# PASO 4: Ejecutar (si aprobado ✅)
# ----------------------------------
make s[N]-preflight && make s[N]-all
```

---

## 📚 Documentación Completa

Para guía detallada, ver: **[README_SISTEMA_DUAL.md](./README_SISTEMA_DUAL.md)**

---

## 📋 Archivos Disponibles

### 🔨 **Generadores** (`generators/`)

| Archivo | Uso | Estado |
|---------|-----|--------|
| `PROMPT_GENERATOR_ALL_SPRINTS.md` | Generador universal para todos los sprints | ✅ Listo |
| `README.md` | Guía de uso de generadores | ✅ Listo |

### ✅ **Verificadores** (`verifiers/`)

| Archivo | Uso | Estado |
|---------|-----|--------|
| `PROMPT_VERIFICADOR_ALL_SPRINTS.md` | Verificador universal para todos los sprints | ✅ Listo |
| `README.md` | Guía de uso de verificadores | ✅ Listo |

---

## 🔄 Flujo de Trabajo Visual

```
┌─────────────────────────────────────────┐
│  📁 generators/                         │
│  PROMPT_GENERATOR_ALL_SPRINTS.md        │
└──────────────┬──────────────────────────┘
               │
               ▼
        ┌─────────────┐
        │   GPT-5     │ Genera documento completo
        │ (ChatGPT)   │ Siguiendo roadmap + template
        └──────┬──────┘
               │
               ▼
        📄 S[N]_[nombre_sprint].md
        (>2500 líneas)
               │
               ▼
┌──────────────────────────────────────────┐
│  📁 verifiers/                           │
│  PROMPT_VERIFICADOR_ALL_SPRINTS.md       │
└──────────────┬───────────────────────────┘
               │
               ▼
        ┌─────────────┐
        │   Claude    │ Lee base de conocimiento
        │ (Cursor AI) │ Verifica exhaustivamente
        └──────┬──────┘
               │
               ▼
        📊 Reporte: ✅ / ⚠️ / ❌
               │
               ▼
        🚀 Ejecución (si aprobado)
```

---

## 🎨 Generar Nuevo Sprint

### 1. Usar el prompt universal:

```bash
# Abrir el generador universal
code generators/PROMPT_GENERATOR_ALL_SPRINTS.md
```

### 2. Actualizar sección de configuración:

```markdown
## 🎯 SPRINT A GENERAR: S[N]

### **Información del Sprint**

**Nombre**: [Nombre del sprint del roadmap]
**Meta**: [Meta del roadmap]
[... resto de información del sprint del roadmap ...]
```

### 3. Todo lo demás se mantiene igual ✅

---

## 📊 Qué Verifica el Sistema

Claude verifica **7 dimensiones de calidad**:

| Dimensión | Criterios |
|-----------|-----------|
| 🏗️ **Estructura** | 14+ secciones obligatorias (header, error handling, ADRs, etc.) |
| 💻 **Código** | Bash (set -euo pipefail), PowerShell (equivalentes), Python (type hints) |
| 🎯 **Roadmap** | Todos los entregables presentes, DoD completo |
| 📐 **Template** | Conformidad 100% con template v2.2 |
| ⚙️ **Ejecutabilidad** | Comandos funcionan sin modificación, paths correctos |
| 📊 **SLOs** | Métricas cuantificables y verificables |
| 🔐 **Seguridad** | mTLS, JWT, fail-closed, no secrets hardcodeados |

---

## ✅ Ventajas del Sistema Dual

| Aspecto | GPT-5 (Generador) | Claude (Verificador) |
|---------|-------------------|----------------------|
| **Velocidad** | ⚡ 5-10 min | 🔍 3-5 min |
| **Acceso proyecto** | ❌ No necesita | ✅ Lee archivos |
| **Creatividad** | 🎨 Alta | 📐 Enfocada en estándares |
| **Patches** | 🤔 Genéricos | ✅ Específicos del proyecto |
| **Base conocimiento** | 📋 Prompt autocontenido | 📚 Consulta roadmap/template |

---

## 🎓 Recursos Adicionales

### Documentación:
- **[README_SISTEMA_DUAL.md](./README_SISTEMA_DUAL.md)** — Guía completa paso a paso
- **[../01-sprint/Template/SPRINT_TEMPLATE_CLAUDE_CLI.md](../01-sprint/Template/SPRINT_TEMPLATE_CLAUDE_CLI.md)** — Template v2.2 oficial
- **[../roadmaps/agent_contracts_roadmap_2025_2026_detallado.md](../roadmaps/agent_contracts_roadmap_2025_2026_detallado.md)** — Roadmap completo

---

## 🔧 Troubleshooting

### ❓ GPT-5 genera documento incompleto
**Solución**: Asegúrate de copiar el prompt COMPLETO desde "---INICIO DEL PROMPT---" hasta "---FIN DEL PROMPT---"

### ❓ Claude no puede leer los archivos de referencia
**Solución**: Verifica que los paths en el prompt verificador sean correctos y relativos al proyecto

### ❓ Reporte de verificación muestra muchos issues críticos
**Solución**: 
1. Revisa los patches sugeridos por Claude
2. Aplica las correcciones
3. Vuelve a verificar

### ❓ ¿Cómo adaptar para otro repositorio?
**Solución**:
1. Actualiza la sección "CONTEXTO DEL PROYECTO" en el generador
2. Actualiza los paths de archivos de referencia en el verificador
3. Personaliza SLOs según el dominio del servicio

---

## 📞 Soporte

**Para issues o mejoras del sistema:**
- **Slack**: #agent-contracts-dev
- **Repo**: agent-contracts
- **Owner**: Platform Engineering Team

---

## 📈 Estado del Sistema

| Sprint | Estado | Generador | Verificador |
|--------|--------|-----------|-------------|
| **S1-S19** | ✅ | Universal | Universal |

---

**Versión:** 2.0  
**Última actualización:** 2025-01-27  
**Mantenedor**: Platform Engineering Team  
**License**: Proprietary - ANDAON SA DE CV

