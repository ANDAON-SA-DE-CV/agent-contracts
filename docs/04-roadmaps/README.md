# 🎯 Roadmap Visual - Agent Contracts

Este directorio contiene visualizaciones interactivas del roadmap de Agent-Contracts para ENIS v3.0.

---

## 📂 Archivos

### `agent-contracts-roadmap-visual.html`

**Visualización interactiva** del roadmap completo (S0-S19) con:
- ✅ Timeline visual con cards alternados
- ✅ Estados por sprint (Completado, En Progreso, Planificado, Crítico, Opcional)
- ✅ Secuencia de ejecución clickeable
- ✅ Collapsible details por sprint
- ✅ Barra de progreso
- ✅ Responsive design
- ✅ Metadata completa (fechas, estimaciones, gates, artefactos)

### `agent_contracts_roadmap_2025_2026_detallado.md`

**Documentación completa** en formato Markdown (4,244 líneas):
- Ubicación: `docs/00-enis-complete/05-repositorios-enis/shared/agent-contracts/agent_contracts_roadmap_2025_2026_detallado.md`
- Versión: 1.5.0
- Incluye: Gaps por sprint, glosario, dependencias, hitos, KPIs, RACI, presupuesto

---

## 🚀 Cómo Usar el HTML

### Opción 1: Abrir Localmente (Recomendado)

```bash
# Desde la raíz del repo
cd docs/01-sprint/roadmaps/
open agent-contracts-roadmap-visual.html  # macOS
# o
start agent-contracts-roadmap-visual.html  # Windows
# o
xdg-open agent-contracts-roadmap-visual.html  # Linux
```

### Opción 2: Servidor Local

```bash
# Con Python
python -m http.server 8000

# Abrir en navegador
# http://localhost:8000/docs/01-sprint/roadmaps/agent-contracts-roadmap-visual.html
```

### Opción 3: Live Server (VS Code)

1. Instalar extensión "Live Server"
2. Right-click en `agent-contracts-roadmap-visual.html`
3. Seleccionar "Open with Live Server"

---

## 🎨 Características del HTML

### Estados de Sprints

| Estado | Color | Descripción |
|--------|-------|-------------|
| **Completado** | 🟢 Verde | Sprint finalizado con DoD 100% |
| **En Progreso** | 🟡 Amarillo | Sprint activo actualmente |
| **Planificado** | 🔵 Azul | Sprint pendiente de iniciar |
| **Crítico** | 🔴 Rojo | Sprint con dependencias bloqueantes |
| **Opcional** | ⚫ Gris | Sprint post-GA opcional (MCP) |

### Navegación

- **Click en secuencia de sprints** → Scroll automático al sprint correspondiente
- **Hover en sprint cards** → Efecto de elevación visual
- **Click en "Entregables"** → Expande/colapsa detalles

### Información por Sprint

Cada sprint card muestra:
- 📅 **Fechas**: Inicio → Fin (duración)
- 🎯 **Meta**: Objetivo principal del sprint
- ⏱️ **Estimación**: Días hábiles esperados
- 📦 **Entregables**: Lista de agregados/modificados
- 🔒 **Gates**: Bloqueadores y checks obligatorios
- 📂 **Artefactos**: Paths específicos de documentos
- ⚠️ **Riesgos**: Identificados con mitigación

---

## 📊 Progreso Tracking

El HTML incluye:
- **Barra de progreso** - Actualizable manualmente (0% inicial)
- **Contador de sprints** - X/20 sprints completados
- **Visual de secuencia** - Sprints completados marcados en verde

### Actualizar Progreso

Editar en línea 234:

```html
<div class="progress-bar" style="width: 15%;">Progreso: 15% (3/20 sprints)</div>
```

Y marcar sprints completados en la secuencia (líneas 128-154):

```html
<div class="sequence-item completed">S0</div>  <!-- Agregar clase 'completed' -->
<div class="sequence-item current">S1</div>    <!-- Agregar clase 'current' para en progreso -->
```

---

## 🔗 Referencias

### Documentación Relacionada

| Documento | Ubicación | Propósito |
|-----------|-----------|-----------|
| **Roadmap Detallado** | `docs/00-enis-complete/.../agent_contracts_roadmap_2025_2026_detallado.md` | Fuente completa (4,244 líneas) |
| **Master Prompt 30** | `docs/00-enis-complete/MASTER_PROMPT_30_ARQUITECTURA.md` | Arquitectura ENIS v3.0 |
| **Changelog** | `docs/00-enis-complete/.../CHANGELOG_ROADMAP_v1.1.0.md` | Historial de cambios |
| **Tabla de Mapeo** | Roadmap líneas 19-98 | 97 documentos mapeados |

### Enlaces Rápidos a Sprints

- **Críticos**: S0, S1, S2, S3, S6, S7, S12, S14, S15
- **Importantes**: S4, S5, S8, S9, S10
- **Normales**: S11, S16
- **Opcionales**: S17, S18, S19 (MCP Post-GA)

---

## 🛠️ Customización

### Cambiar Colores

Editar el CSS en `<style>` (líneas 8-83):

```css
/* Gradiente principal */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Estados de sprints */
.completed { background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); }
.critical { background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); }
```

### Agregar Nuevos Sprints

Copiar template de sprint card y modificar:

```html
<div class="sprint-card left planned">
    <h2 class="sprint-title">S20 — Nuevo Sprint <span class="status-tag tag-planned">PLANIFICADO</span></h2>
    <p class="sprint-meta">
        <strong>📅 Fechas:</strong> YYYY-MM-DD → YYYY-MM-DD<br>
        <strong>🎯 Meta:</strong> [Objetivo]<br>
        <strong>⏱️ Estimación:</strong> [Días]
    </p>
    <!-- ... resto del contenido ... -->
</div>
```

---

## 📝 Notas

- El HTML es **standalone** (no requiere assets externos)
- Compatible con todos los navegadores modernos
- Responsive design para móviles/tablets
- Print-friendly (quitar background gradients en @media print)

---

**Versión**: 1.0.0  
**Última actualización**: 2025-10-11  
**Maintainer**: Contract Architect  
**Software Propietario © 2025 ANDAON SA DE CV**

