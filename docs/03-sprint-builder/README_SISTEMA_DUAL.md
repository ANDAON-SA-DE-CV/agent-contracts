# 🤖 Sistema Dual de Generación y Verificación de Sprints

> **GPT-5 Genera → Claude Verifica → Usuario Aprueba → Claude Ejecuta**

---

## 🎯 Resumen Ejecutivo

Este sistema permite **generar documentos de sprint** de alta calidad usando la colaboración entre dos LLMs especializados:

1. **GPT-5 (ChatGPT)** — Generador rápido y creativo
2. **Claude (Cursor AI)** — Verificador técnico con acceso al proyecto

---

## 📁 Archivos del Sistema

| Archivo | Propósito | Usuario |
|---------|-----------|---------|
| `PROMPT_GENERATOR_ALL_SPRINTS.md` | Prompt universal para generar cualquier sprint | ChatGPT-5 Web |
| `PROMPT_VERIFICADOR_ALL_SPRINTS.md` | Prompt universal para verificar cualquier sprint | Claude (Cursor AI) |
| `README_SISTEMA_DUAL.md` | Este documento (guía de uso) | Desarrollador |

---

## 🔄 Flujo de Trabajo

```
┌─────────────────────────────────────────────────────────────┐
│  PASO 1: GENERACIÓN (GPT-5)                                 │
│  ───────────────────────────                                 │
│  Input:  PROMPT_GENERATOR_ALL_SPRINTS.md                    │
│  Output: Archivo S[N]_[nombre_sprint].md (>2500 lines)      │
│  Tiempo: 5-10 minutos                                        │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
              📄 Archivo markdown del sprint
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  PASO 2: VERIFICACIÓN (Claude)                              │
│  ────────────────────────────                                │
│  Input:  PROMPT_VERIFICADOR_ALL_SPRINTS.md                  │
│          + Archivo generado por GPT-5                        │
│  Output: Reporte de verificación                            │
│          Score: X/Y = Z%                                     │
│          Veredicto: ✅ / ⚠️ / ❌                            │
│  Tiempo: 3-5 minutos                                         │
└────────────────────────────┬────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
         ✅ APROBADO              ❌ CORRECCIONES
                │                         │
                │                         └──> Aplicar patches
                │                                    │
                │                                    └──> PASO 2
                │
                ▼
┌─────────────────────────────────────────────────────────────┐
│  PASO 3: EJECUCIÓN (Claude)                                 │
│  ─────────────────────────                                   │
│  Input:  Documento aprobado                                 │
│  Output: Sprint ejecutado completamente                     │
│  Tiempo: Variable (depende del sprint)                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📖 Guía Rápida de Uso

### 1️⃣ **Generar con GPT-5**

```bash
# 1. Ir a ChatGPT-5
open https://chat.openai.com

# 2. Abrir el prompt generador
code docs/03-sprint-builder/generators/PROMPT_GENERATOR_ALL_SPRINTS.md

# 3. Copiar desde "---INICIO DEL PROMPT---" hasta "---FIN DEL PROMPT---"
# 4. Pegar en ChatGPT-5 y enviar
# 5. Esperar 5-10 minutos (documento completo)
# 6. Copiar resultado completo
```

### 2️⃣ **Guardar Archivo Generado**

```bash
# Crear directorio si no existe
mkdir -p docs/01-sprint/S[N]

# Guardar contenido generado por GPT-5
# Pegar en: docs/01-sprint/S[N]/S[N]_[nombre_sprint].md
```

### 3️⃣ **Verificar con Claude**

```bash
# 1. Abrir Cursor AI en el proyecto
cursor .

# 2. Abrir el prompt verificador
# docs/03-sprint-builder/verifiers/PROMPT_VERIFICADOR_ALL_SPRINTS.md

# 3. Copiar desde "---INICIO DEL PROMPT---" hasta "---FIN DEL PROMPT---"
# 4. Pegar en chat de Claude
# 5. Cuando Claude pida el archivo, responder:
#    "Léelo desde docs/01-sprint/S[N]/S[N]_[nombre_sprint].md"
```

### 4️⃣ **Revisar Reporte**

Claude generará un reporte con:

```markdown
# 🔍 REPORTE DE VERIFICACIÓN — Sprint S[N]

**Veredicto General**: ✅ APROBADO

**Score Global**: 47/50 = 94%

## ✅ ASPECTOS POSITIVOS
1. Estructura completa y bien organizada
2. Código Python con type hints y docstrings
3. Scripts bash con error handling robusto
...

## 🔴 ISSUES CRÍTICOS
[Si hay issues bloqueantes]

## 🟡 ISSUES IMPORTANTES
[Issues recomendados pero no bloqueantes]

## 🟢 MEJORAS SUGERIDAS
[Mejoras opcionales]
```

### 5️⃣ **Ejecutar o Corregir**

**Si está APROBADO ✅:**
```bash
# Ejecutar sprint
make s[N]-preflight
make s[N]-all
```

**Si REQUIERE CORRECCIONES ❌:**
```bash
# Aplicar patches sugeridos por Claude
# Re-verificar con PASO 3
```

---

## 🎨 Personalización para Otros Sprints

### Para generar cualquier sprint:

**1. Usar el prompt universal `PROMPT_GENERATOR_ALL_SPRINTS.md`:**

```markdown
## 🎯 SPRINT A GENERAR: S[N]  ← Cambiar número

### **Información del Sprint**

**Nombre**: [Nombre del sprint del roadmap]  ← Copiar del roadmap

**Meta**: [Meta del roadmap]  ← Copiar del roadmap

[... resto de información del sprint del roadmap ...]
```

**2. Usar el verificador universal `PROMPT_VERIFICADOR_ALL_SPRINTS.md`:**

```markdown
**Documento a verificar**: Sprint S[N] — [Nombre]  ← Actualizar

read_file docs/01-sprint/S[N]/S[N]_*.md  ← Cambiar path
```

**3. Todo lo demás se mantiene igual**

---

## 🔍 Qué Verifica Claude

### ✅ **7 Dimensiones de Calidad:**

1. **Estructura y Secciones** (14+ secciones obligatorias)
   - Header, metadata, error handling, ADRs, etc.

2. **Calidad de Código**
   - Bash: `set -euo pipefail`, trap, retry, timeout
   - PowerShell: Equivalentes completos
   - Python: Type hints, docstrings, error handling

3. **Alineación con Roadmap**
   - Todos los entregables presentes
   - DoD completo
   - Flujos documentados

4. **Conformidad con Template v2.2**
   - Estructura idéntica
   - Todas las secciones presentes
   - Formato correcto

5. **Ejecutabilidad Real**
   - Comandos funcionan sin modificación
   - Paths relativos
   - Variables correctas

6. **SLOs y Métricas**
   - Cuantificables
   - Verificables
   - Targets realistas

7. **Seguridad**
   - mTLS, JWT, fail-closed
   - No secrets hardcodeados
   - Validación de inputs

---

## 📊 Ventajas vs Desventajas

### ✅ **Ventajas del Sistema Dual**

| Aspecto | Beneficio |
|---------|-----------|
| **Velocidad** | GPT-5 genera en minutos |
| **Calidad** | Claude verifica contra estándares |
| **Flexibilidad** | Funciona sin acceso al proyecto (GPT-5) |
| **Precisión** | Claude tiene contexto completo del proyecto |
| **Patches** | Claude genera correcciones específicas |
| **Reutilizable** | Prompts sirven para todos los sprints |

### ⚠️ **Consideraciones**

| Aspecto | Mitigación |
|---------|------------|
| **Dos pasos** | Automatizable en el futuro |
| **Requiere dos LLMs** | Pero maximiza fortalezas de cada uno |
| **Copy-paste manual** | Compensado por calidad del resultado |

---

## 🎓 Casos de Uso

### ✅ **Usar este sistema cuando:**

- Necesitas generar sprints completos rápido
- Quieres asegurar calidad antes de ejecutar
- El sprint está bien definido en el roadmap
- Prefieres separar generación de verificación

### 🔧 **Usar solo Claude cuando:**

- Estás en Cursor AI con acceso al proyecto
- Quieres iteración rápida (generar + ejecutar)
- El sprint es complejo y requiere contexto profundo

### 🌐 **Usar solo GPT-5 cuando:**

- Solo necesitas un borrador inicial
- Vas a revisar manualmente
- No tienes acceso a Claude/Cursor

---

## 📚 Archivos de Referencia

Estos archivos son la "fuente de verdad" que Claude consulta:

| Archivo | Propósito |
|---------|-----------|
| `agent_contracts_roadmap_2025_2026_detallado.md` | Especificación oficial de todos los sprints |
| `SPRINT_TEMPLATE_CLAUDE_CLI.md` | Plantilla v2.2 (estructura requerida) |
| `PROMPT_GENERATOR_ALL_SPRINTS.md` | Generador universal para todos los sprints |

---

## 🚀 Próximos Pasos

1. **Probar el sistema** con cualquier sprint (S1-S19)
2. **Adaptar para nuevos sprints** siguiendo guía de personalización
3. **Documentar aprendizajes** para mejorar el proceso
4. **Crear biblioteca de reportes** de ejemplo

---

## 📞 Soporte

**Para issues o mejoras:**
- Slack: #agent-contracts-dev
- Repo: agent-contracts
- Owner: Platform Engineering Team

---

**Versión:** 2.0  
**Fecha:** 2025-01-27  
**Mantenedor:** Platform Engineering  
**License:** Proprietary - ANDAON SA DE CV

