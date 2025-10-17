# 📋 Propuesta de Numeración para Nuevos Master Prompts

## 📊 Estado Actual de Numeraciones (00-29)

### **Numeraciones Existentes:**

```yaml
00-dna:
  - 00-dna-master-prompt.md

01-fundacionales:
  - 01-overview-master-prompt.md
  - 06-orchestrator-master-prompt.md

02-arquitectura:
  - 02-architecture-master-prompt.md
  - 07-nops-master-prompt.md
  - 10-edge-master-prompt.md
  - 11-nops-complete-master-prompt.md
  - 12-inference-master-prompt.md

03-macro-modulos:
  - 13-asm-master-prompt.md
  - 14-cgn-master-prompt.md
  - 15-awe-master-prompt.md
  - 16-shif-master-prompt.md

04-desarrollo:
  - 04-implementation-master-prompt.md
  - 09-dev-generation-master-prompt.md
  - 20-integration-master-prompt.md
  - 21-testing-master-prompt.md

05-negocio:
  - 03-business-master-prompt.md
  - 08-marketplace-master-prompt.md
  - 25-cost-optimization-master-prompt.md

06-operaciones:
  - 18-security-master-prompt.md
  - 19-performance-master-prompt.md
  - 22-monitoring-master-prompt.md
  - 24-disaster-recovery-master-prompt.md

07-interfaz:
  - 05-reference-master-prompt.md
  - 17-uiux-dashboard-master-prompt.md
  - 23-data-management-master-prompt.md
  - 26-natural-interface-master-prompt.md
  - 27-xr-interface-master-prompt.md
  - 28-edge-hub-master-prompt.md
  - 29-future-vision-enis-master-prompt.md
```

**Total numeraciones usadas:** 00-29 (30 numeraciones)

---

## 🆕 Propuesta de Numeración para Nuevos Master Prompts (30-36)

### **Master Prompts a Numerar:**

```yaml
nuevos_master_prompts:
  desarrollo:
    - nombre: "AGENT_CONTRACTS_MASTER_PROMPT.md"
      numero_propuesto: 30
      nuevo_nombre: "30-agent-contracts-master-prompt.md"
      carpeta_destino: "04-desarrollo"
      justificacion: "Gestión de contratos y APIs - Core de desarrollo"
      
    - nombre: "AGENT_SDKS_MASTER_PROMPT.md"
      numero_propuesto: 32
      nuevo_nombre: "32-agent-sdks-master-prompt.md"
      carpeta_destino: "04-desarrollo"
      justificacion: "Generación de SDKs multi-lenguaje - Herramientas de desarrollo"
  
  negocio:
    - nombre: "AGENT_MARKETPLACE_MASTER_PROMPT.md"
      numero_propuesto: 31
      nuevo_nombre: "31-agent-marketplace-master-prompt.md"
      carpeta_destino: "05-negocio"
      justificacion: "Marketplace de agentes - Modelo de negocio y comercialización"
  
  operaciones:
    - nombre: "CLOUD_INFRASTRUCTURE_MASTER_PROMPT.md"
      numero_propuesto: 33
      nuevo_nombre: "33-cloud-infrastructure-master-prompt.md"
      carpeta_destino: "06-operaciones"
      justificacion: "Infraestructura cloud - Operaciones y deployment"
      
    - nombre: "EDGE_INFRASTRUCTURE_MASTER_PROMPT.md"
      numero_propuesto: 34
      nuevo_nombre: "34-edge-infrastructure-master-prompt.md"
      carpeta_destino: "06-operaciones"
      justificacion: "Infraestructura edge - Operaciones distribuidas"
      
    - nombre: "ENIS_INFRASTRUCTURE_MASTER_PROMPT.md"
      numero_propuesto: 36
      nuevo_nombre: "36-enis-infrastructure-master-prompt.md"
      carpeta_destino: "06-operaciones"
      justificacion: "Infraestructura general ENIS - IaC y CI/CD"
  
  interfaz:
    - nombre: "ENIS_FRONTEND_MASTER_PROMPT.md"
      numero_propuesto: 35
      nuevo_nombre: "35-enis-frontend-master-prompt.md"
      carpeta_destino: "07-interfaz"
      justificacion: "Frontend completo - Dashboard, DevPortal, Studio"
```

---

## 📋 Resumen de Acciones Requeridas

### **Renombrar y Mover Archivos:**

```bash
# 04-desarrollo/
mv AGENT_CONTRACTS_MASTER_PROMPT-with-operational-docs-20251008-050011.md \
   04-desarrollo/30-agent-contracts-master-prompt.md

mv AGENT_SDKS_MASTER_PROMPT.md \
   04-desarrollo/32-agent-sdks-master-prompt.md

# 05-negocio/
mv AGENT_MARKETPLACE_MASTER_PROMPT.md \
   05-negocio/31-agent-marketplace-master-prompt.md

# 06-operaciones/
mv CLOUD_INFRASTRUCTURE_MASTER_PROMPT.md \
   06-operaciones/33-cloud-infrastructure-master-prompt.md

mv EDGE_INFRASTRUCTURE_MASTER_PROMPT.md \
   06-operaciones/34-edge-infrastructure-master-prompt.md

mv ENIS_INFRASTRUCTURE_MASTER_PROMPT.md \
   06-operaciones/36-enis-infrastructure-master-prompt.md

# 07-interfaz/
mv ENIS_FRONTEND_MASTER_PROMPT.md \
   07-interfaz/35-enis-frontend-master-prompt.md
```

---

## 🎯 Estructura Final Propuesta

### **04-desarrollo/ (4 archivos):**
- 04-implementation-master-prompt.md
- 09-dev-generation-master-prompt.md
- 20-integration-master-prompt.md
- 21-testing-master-prompt.md
- **30-agent-contracts-master-prompt.md** ⬅️ NUEVO
- **32-agent-sdks-master-prompt.md** ⬅️ NUEVO

### **05-negocio/ (4 archivos):**
- 03-business-master-prompt.md
- 08-marketplace-master-prompt.md
- 25-cost-optimization-master-prompt.md
- **31-agent-marketplace-master-prompt.md** ⬅️ NUEVO

### **06-operaciones/ (7 archivos):**
- 18-security-master-prompt.md
- 19-performance-master-prompt.md
- 22-monitoring-master-prompt.md
- 24-disaster-recovery-master-prompt.md
- **33-cloud-infrastructure-master-prompt.md** ⬅️ NUEVO
- **34-edge-infrastructure-master-prompt.md** ⬅️ NUEVO
- **36-enis-infrastructure-master-prompt.md** ⬅️ NUEVO

### **07-interfaz/ (8 archivos):**
- 05-reference-master-prompt.md
- 17-uiux-dashboard-master-prompt.md
- 23-data-management-master-prompt.md
- 26-natural-interface-master-prompt.md
- 27-xr-interface-master-prompt.md
- 28-edge-hub-master-prompt.md
- 29-future-vision-enis-master-prompt.md
- **35-enis-frontend-master-prompt.md** ⬅️ NUEVO

---

## ✅ Validación de Numeración

### **Numeraciones Usadas (Total: 37):**
00, 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, **30**, **31**, **32**, **33**, **34**, **35**, **36**

### **Numeraciones Disponibles:**
37 en adelante

### **Conflictos Detectados:**
❌ Ninguno - Todas las numeraciones propuestas (30-36) están libres

---

## 🚀 Próximos Pasos

1. **Revisar y aprobar** la propuesta de numeración
2. **Ejecutar comandos de renombrado** y movimiento de archivos
3. **Actualizar cross-references** en archivos relacionados
4. **Actualizar README.md** de cada carpeta con los nuevos archivos
5. **Actualizar índices** y documentación general

---

*Propuesta generada: 2025-10-08*
*Total de Master Prompts después de la integración: 37*

