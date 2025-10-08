# 40 - Sandbox Service Master Prompt

## Metadata

```yaml
prompt_id: "40"
prompt_name: "sandbox-master-prompt"
service_name: "sandbox-service"
version: "1.0.0"
category: "cloud-core"
dna_version: "3.0"
created: "2025-10-08"
status: "active"
priority: "P3"
sprint: "S23-P1"
```

---

## 🎯 Propósito del Servicio

El **Sandbox Service** proporciona ejecución aislada y segura para Edge Agents.

### Responsabilidades Core:

```yaml
responsabilidades:
  isolation:
    - "Container isolation (containerd)"
    - "VM-level isolation (gVisor/Kata Containers)"
    - "Network isolation (network namespaces)"
    - "Filesystem isolation (overlay FS)"
    
  security:
    - "Seccomp filtering (syscall whitelisting)"
    - "AppArmor/SELinux profiles"
    - "Capabilities dropping"
    - "No-new-privileges flag"
    
  resources:
    - "CPU limits (cgroups v2)"
    - "Memory limits (OOM protection)"
    - "Storage quotas"
    - "Network bandwidth limits"
    
  monitoring:
    - "Resource usage tracking"
    - "Security violations detection"
    - "Execution logs capture"
```

---

## 🏗️ Arquitectura del Servicio

### Stack Tecnológico:

```yaml
backend:
  framework: "Gin (Go)"
  runtime: "Go 1.21+"
  
container_runtime:
  base: "containerd"
  isolation: "gVisor (runsc) / Kata Containers"
  orchestration: "Kubernetes Jobs"
  
security:
  seccomp: "Custom profiles per agent type"
  mandatory_access_control: "AppArmor + SELinux"
  capabilities: "Minimal (drop all + whitelist)"
```

---

## 📡 APIs Principales

```yaml
POST /api/v1/sandbox/create:
  auth: "mTLS"
  payload:
    agent_id: string
    security_profile: "minimal|standard|strict"
    resources:
      cpu_limit: float
      memory_limit: string
      
POST /api/v1/sandbox/{id}/execute:
  auth: "mTLS"
  payload:
    code: string (base64)
    timeout: int
    
  response:
    execution_id: string
    output: string
    exit_code: int
```

---

*Master Prompt creado: 2025-10-08*

