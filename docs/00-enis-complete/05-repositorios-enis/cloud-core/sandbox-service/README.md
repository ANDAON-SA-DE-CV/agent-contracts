# 🧪 Sandbox Service - ENIS v3.0

## 📋 Metadata

```yaml
service_name: "sandbox-service"
service_type: "Platform Service"
category: "cloud-core"
priority: "P3 - BAJA"
status: "📋 Planned - Sprint S23-P1"
stack: "Go / containerd"
dependencies: ["containerd", "gVisor", "Kubernetes"]
dna_version: "3.0"
```

---

## 🎯 Propósito

Servicio de ejecución aislada para agentes (arquitectura SLIM).

Proporciona:
- **Container isolation** (Docker/Kata Containers)
- **Security profiles** (Seccomp/AppArmor/SELinux)
- **Resource limits** enforcement
- **Network isolation** policies
- **Execution monitoring**

---

## 🏗️ Arquitectura

### Principio SLIM:
Este servicio es usado por **Edge Agents** (NO por NOPS Kernel directamente).

```yaml
comunicacion:
  edge_agents:
    protocolo: "mTLS"
    endpoint: "POST /api/v1/sandbox/{id}/execute"
    uso: "Ejecución de código en sandbox aislado"
    
  nops_kernel:
    via: "Eventos (no API directa)"
    trigger: "Puede solicitar ejecución sandboxed via eventos"
```

---

## 📦 Stack Tecnológico

```yaml
backend:
  framework: "Gin (Go)"
  runtime: "Go 1.21+"
  
runtime:
  containers: "containerd + gVisor/Kata Containers"
  security: "Seccomp + AppArmor + SELinux"
  orchestration: "Kubernetes Jobs"
  
security:
  isolation: "Container + VM-level (gVisor/Kata)"
  network: "Network namespaces"
  syscall: "Seccomp filtering"
```

---

## 🚀 Sprint de Implementación

**Sprint:** S23-P1  
**Duración:** 2 semanas  
**Prioridad:** P3 (BAJA - Post-GA)

---

*Servicio creado: 2025-10-08*  
*Estado: Planned - Sprint S23-P1*

