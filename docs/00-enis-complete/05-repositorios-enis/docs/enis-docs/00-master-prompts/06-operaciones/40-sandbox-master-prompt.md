# 40 - Sandbox Service Master Prompt

---
prompt_id: "40-sandbox-master-prompt"
prompt_type: "master_prompt"
service_name: "sandbox-service"
dna_version: "3.0"
semver: "1.0.0"
date: "2025-10-08"
author: "@andaon"
domain: "Sandbox & Testing"
description: "Master prompt para Sandbox Service - Entorno aislado para testing de Edge Agents"
estimated_pages: "100-120"
compliance_status: "DNA_v3_compliant"
dependencies: ["00-dna-proyecto-prompt.md", "07-nops-master-prompt.md", "08-agent-marketplace-master-prompt.md"]
generates:
 - "architecture/sandbox/*"
 - "reference/sandbox-api/*"
 - "isolation-strategies/*"
child_prompts: 12
validation_script: "validate-sandbox-documentation.js"
release_status: "ready_for_sprint_s23"
feeds_to: ["08-agent-marketplace", "10-edge-agents"]
priority: "P3"
sprint: "S23-P2"
---

## 🎯 PROPÓSITO Y CONTEXTO

**ROL:** Arquitecto Senior de Security & Isolation en ENIS v3.0

**TAREA:** Generar documentación completa del Sandbox Service - entorno de ejecución aislado y seguro para testing de Edge Agents antes de despliegue productivo.

**OBJETIVO:** Producir 100-120 páginas de documentación técnica que cubra isolation strategies, security boundaries, resource limits, testing frameworks y APIs.

**CONTEXTO CRÍTICO:**
- El Sandbox Service es **SECURITY-CRITICAL** - previene código malicioso
- Isolation multi-nivel: containers + namespaces + seccomp + AppArmor
- Resource limits estrictos (CPU, memory, network, disk I/O)
- Testing automatizado de agents antes de certificación
- Integration con Agent Marketplace (pre-approval testing)

# 📑 TABLA DE CONTENIDOS

- 🏗️ Arquitectura del Sandbox Service
- 🔒 Isolation Strategies
- ⚙️ Resource Limits & Quotas
- 🧪 Testing Framework
- 🔧 APIs y SDKs
- 🚀 Deployment Patterns
- 📁 Estructura de Documentación

## 🏗️ ARQUITECTURA DEL SANDBOX SERVICE

### **Componentes Core**

```yaml
sandbox_architecture:
  execution_engine:
    description: "Motor de ejecución aislado para agents"
    technology: "gVisor + Kubernetes RuntimeClass"
    isolation_levels:
      level_1_process:
        technology: "Linux namespaces (PID, NET, MNT, UTS, IPC)"
        use_case: "Basic isolation"
        
      level_2_container:
        technology: "Docker/Containerd con runtime=runsc (gVisor)"
        use_case: "Standard sandbox"
        
      level_3_vm:
        technology: "Firecracker microVMs"
        use_case: "High-security (Enterprise tier)"
        
  resource_governor:
    description: "Control de recursos por sandbox"
    technology: "cgroups v2 + eBPF"
    limits:
      cpu:
        max_cores: 2
        max_cpu_percent: 80
        throttling: "enabled"
        
      memory:
        max_ram_mb: 512
        max_swap_mb: 0  # No swap
        oom_kill: "enabled"
        
      network:
        max_bandwidth_mbps: 10
        allowed_egress: ["inference-service", "agent-registry"]
        blocked_egress: ["internet", "internal-services"]
        
      disk:
        max_storage_mb: 1024
        max_iops: 1000
        ephemeral: true  # Destroyed after execution
        
  security_monitor:
    description: "Monitoreo de comportamiento sospechoso"
    technology: "Falco + custom rules"
    monitored_events:
      - "unauthorized_syscalls"
      - "network_connection_attempts"
      - "file_access_outside_workspace"
      - "privilege_escalation_attempts"
      - "resource_limit_breaches"
      
    response:
      detection: "Real-time"
      action: "Kill sandbox + alert security team"
      logging: "Audit trail en Compliance Service"
```

---

## 🔒 ISOLATION STRATEGIES

### **Multi-Layer Security**

```yaml
isolation_strategies:
  layer_1_namespaces:
    description: "Linux kernel namespaces"
    namespaces:
      pid:
        description: "Process ID isolation"
        effect: "Sandbox sees only its own processes"
        
      net:
        description: "Network isolation"
        effect: "Private network namespace"
        
      mnt:
        description: "Filesystem mount isolation"
        effect: "Cannot see host filesystem"
        
      uts:
        description: "Hostname/domain isolation"
        effect: "Separate hostname"
        
      ipc:
        description: "Inter-process communication isolation"
        effect: "Cannot access host IPC"
        
  layer_2_seccomp:
    description: "Syscall filtering"
    profile: "runtime/default"
    blocked_syscalls:
      - "mount"
      - "umount"
      - "reboot"
      - "init_module"
      - "delete_module"
      - "ptrace"
      
  layer_3_apparmor:
    description: "Mandatory Access Control"
    profile: "enis-sandbox-strict"
    restrictions:
      filesystem:
        allowed_read: ["/workspace", "/tmp"]
        allowed_write: ["/workspace/output", "/tmp"]
        denied: ["/**"]  # Everything else
        
      network:
        allowed_connect: ["inference-service:443"]
        denied: ["*:*"]
        
      capabilities:
        denied_all: true
        allowed: []  # No Linux capabilities
```

---

## ⚙️ RESOURCE LIMITS & QUOTAS

### **cgroups Configuration**

```yaml
# kubernetes/sandbox-service/pod-template.yaml
apiVersion: v1
kind: Pod
metadata:
  name: sandbox-execution
  annotations:
    container.apparmor.security.beta.kubernetes.io/sandbox: "localhost/enis-sandbox-strict"
spec:
  runtimeClassName: gvisor  # Use gVisor for enhanced isolation
  
  containers:
    - name: sandbox
      image: enis/agent-sandbox:latest
      
      securityContext:
        runAsNonRoot: true
        runAsUser: 10000
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        seccompProfile:
          type: RuntimeDefault
          
      resources:
        requests:
          cpu: "500m"
          memory: "256Mi"
          ephemeral-storage: "512Mi"
        limits:
          cpu: "2000m"
          memory: "512Mi"
          ephemeral-storage: "1Gi"
          
      volumeMounts:
        - name: workspace
          mountPath: /workspace
        - name: tmp
          mountPath: /tmp
          
  volumes:
    - name: workspace
      emptyDir:
        sizeLimit: "512Mi"
    - name: tmp
      emptyDir:
        sizeLimit: "256Mi"
        
  # Network policy - only allow egress to inference-service
  networkPolicy:
    egress:
      - to:
          - podSelector:
              matchLabels:
                app: inference-service
        ports:
          - protocol: TCP
            port: 443
```

---

## 🧪 TESTING FRAMEWORK

### **Automated Agent Testing**

```python
# sandbox_service/testing/agent_tester.py
from typing import Dict, Any, List
import asyncio
import docker
from dataclasses import dataclass

@dataclass
class TestResult:
    passed: bool
    test_name: str
    duration_ms: float
    output: Any
    error: str = None

class AgentTester:
    """
    Framework automatizado para testing de agents en sandbox
    
    Tests ejecutados antes de certificación en marketplace
    """
    
    def __init__(self, docker_client: docker.DockerClient):
        self.docker = docker_client
        
    async def run_agent_test_suite(
        self,
        agent_id: str,
        agent_code: str
    ) -> Dict[str, Any]:
        """
        Ejecuta suite completo de tests para un agent
        
        Returns:
            {
                "overall_result": "pass|fail",
                "tests": [list of TestResult],
                "security_score": 0-100,
                "performance_score": 0-100
            }
        """
        test_results = []
        
        # 1. Security tests
        test_results.append(await self._test_malicious_code_detection(agent_code))
        test_results.append(await self._test_unauthorized_network_access(agent_id))
        test_results.append(await self._test_privilege_escalation_attempt(agent_id))
        
        # 2. Performance tests
        test_results.append(await self._test_execution_time(agent_id))
        test_results.append(await self._test_resource_usage(agent_id))
        
        # 3. Functionality tests
        test_results.append(await self._test_basic_functionality(agent_id))
        test_results.append(await self._test_error_handling(agent_id))
        
        # 4. Calculate scores
        security_tests = [t for t in test_results if "security" in t.test_name]
        performance_tests = [t for t in test_results if "performance" in t.test_name]
        
        security_score = (sum(t.passed for t in security_tests) / len(security_tests)) * 100
        performance_score = (sum(t.passed for t in performance_tests) / len(performance_tests)) * 100
        
        overall_pass = all(t.passed for t in test_results if "critical" in t.test_name)
        
        return {
            "agent_id": agent_id,
            "overall_result": "pass" if overall_pass else "fail",
            "tests": [t.__dict__ for t in test_results],
            "security_score": security_score,
            "performance_score": performance_score,
            "tested_at": datetime.utcnow().isoformat()
        }
    
    async def _test_malicious_code_detection(
        self,
        agent_code: str
    ) -> TestResult:
        """
        Test: Detecta código potencialmente malicioso
        
        Critical: True
        """
        start_time = time.time()
        
        malicious_patterns = [
            r"os\.system",
            r"subprocess\..*call",
            r"eval\(",
            r"exec\(",
            r"__import__",
            r"open\(.*(\/etc\/passwd|\/etc\/shadow)"
        ]
        
        import re
        detected = []
        
        for pattern in malicious_patterns:
            if re.search(pattern, agent_code):
                detected.append(pattern)
        
        duration = (time.time() - start_time) * 1000
        
        return TestResult(
            passed=len(detected) == 0,
            test_name="security_malicious_code_detection_critical",
            duration_ms=duration,
            output={"detected_patterns": detected},
            error=f"Malicious patterns detected: {detected}" if detected else None
        )
    
    async def _test_unauthorized_network_access(
        self,
        agent_id: str
    ) -> TestResult:
        """
        Test: Intenta acceso no autorizado a red
        
        Expect: Network request should be blocked
        """
        start_time = time.time()
        
        # Ejecutar agent en sandbox con intento de acceso a internet
        try:
            sandbox = await self._create_sandbox(agent_id)
            
            # Inject test code that tries to access google.com
            test_code = """
import requests
try:
    response = requests.get('https://google.com', timeout=5)
    print('VIOLATION: Network access succeeded')
except Exception as e:
    print(f'EXPECTED: Network blocked - {e}')
"""
            
            output = await sandbox.execute(test_code, timeout=10)
            
            passed = "EXPECTED" in output and "VIOLATION" not in output
            
            duration = (time.time() - start_time) * 1000
            
            return TestResult(
                passed=passed,
                test_name="security_unauthorized_network_critical",
                duration_ms=duration,
                output={"sandbox_output": output},
                error=None if passed else "Network access was NOT blocked"
            )
            
        except Exception as e:
            return TestResult(
                passed=False,
                test_name="security_unauthorized_network_critical",
                duration_ms=0,
                output={},
                error=str(e)
            )
        finally:
            await sandbox.cleanup()
```

---

## 🔧 APIS Y SDKS

```yaml
sandbox_api:
  POST /api/v1/sandbox/create:
    description: "Create isolated sandbox"
    auth: "mTLS + JWT s2s"
    request:
      agent_id: "string"
      isolation_level: "standard|high"
      resource_limits: "object"
    response:
      sandbox_id: "uuid"
      access_token: "jwt"
      
  POST /api/v1/sandbox/{id}/execute:
    description: "Execute agent in sandbox"
    auth: "Sandbox access token"
    request:
      code: "string"
      input: "object"
      timeout_seconds: "int (max: 300)"
    response:
      execution_id: "uuid"
      output: "object"
      metrics:
        duration_ms: "float"
        memory_peak_mb: "float"
        
  DELETE /api/v1/sandbox/{id}:
    description: "Destroy sandbox"
    auth: "mTLS + JWT s2s"
```

---

## 🚀 DEPLOYMENT PATTERNS

```yaml
deployment:
  runtime:
    primary: "gVisor (runsc)"
    fallback: "Kata Containers"
    high_security: "Firecracker microVMs"
    
  scaling:
    min_sandboxes: 5  # Warm pool
    max_sandboxes: 100
    autoscaling: "Based on queue depth"
    
  cleanup:
    max_lifetime: "1 hour"
    idle_timeout: "5 minutes"
    force_cleanup: "After execution"
```

---

## 📁 ESTRUCTURA DE DOCUMENTACIÓN

```yaml
documentation_structure:
  sandbox_service/:
    - "README.md"
    - "40-sandbox-master-prompt.md"
    - "ISOLATION_STRATEGIES.md"
    - "SECURITY_BEST_PRACTICES.md"
    
  testing/:
    - "agent-test-suite.py"
    - "security-tests.py"
    - "performance-tests.py"
```

---

## 📋 METADATA DE CIERRE

```yaml
service_summary:
  nombre: "Sandbox Service"
  proposito: "Isolated testing environment para Edge Agents"
  prioridad: "P3"
  
  componentes_principales:
    - "gVisor isolation engine"
    - "Resource governor (cgroups)"
    - "Security monitor (Falco)"
    - "Automated testing framework"
    
  stack_tecnologico:
    - "gVisor + Kubernetes"
    - "eBPF + Falco"
    - "Docker/Containerd"
    - "Firecracker (Enterprise)"
    
estado: "ready_for_sprint_s23-p2"
estimated_completion: "1 semana"
total_lines: "~1,100 líneas"
```

---

*Master Prompt Sandbox Service v1.0 - Creado 2025-10-08*  
*Estado: Versión profesional completa*  
*Security-critical: Prevents malicious code execution*
