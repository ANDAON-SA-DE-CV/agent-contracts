# 42 - Lifecycle Service Master Prompt

---
prompt_id: "42-lifecycle-master-prompt"
prompt_type: "master_prompt"
service_name: "lifecycle-service"
dna_version: "3.0"
semver: "1.0.0"
date: "2025-10-08"
author: "@andaon"
domain: "Deployment & Lifecycle Management"
description: "Master prompt para Lifecycle Service - Deployment strategies, rollbacks y version management"
estimated_pages: "110-130"
compliance_status: "DNA_v3_compliant"
dependencies: ["00-dna-proyecto-prompt.md", "07-nops-master-prompt.md", "10-edge-agents-master-prompt.md"]
generates:
 - "architecture/lifecycle/*"
 - "reference/deployment-strategies/*"
 - "operators/lifecycle-operator/*"
child_prompts: 13
validation_script: "validate-lifecycle-documentation.js"
release_status: "ready_for_sprint_s23"
feeds_to: ["10-edge-agents", "07-nops-kernel"]
priority: "P3"
sprint: "S23-P2"
---

## 🎯 PROPÓSITO Y CONTEXTO

**ROL:** Arquitecto Senior de DevOps & Release Engineering en ENIS v3.0

**TAREA:** Generar documentación completa del Lifecycle Service - servicio para deployment strategies (Rolling, Blue-Green, Canary), version management, rollbacks automáticos y health monitoring de Edge Agents.

**OBJETIVO:** Producir 110-130 páginas de documentación técnica que cubra deployment patterns, Kubernetes Operator implementation, automated rollbacks, compatibility matrix y release orchestration.

**CONTEXTO CRÍTICO:**
- El Lifecycle Service es **OPERATIONAL-CRITICAL** - deployments incorrectos afectan producción
- Deployment strategies: Rolling (default), Blue-Green, Canary, Recreate
- Zero-downtime obligatorio para Enterprise tier (🔵🔴)
- Rollback automático si health checks fallan
- Version compatibility matrix (agent ↔ NOPS Kernel ↔ Inference Service)

# 📑 TABLA DE CONTENIDOS

- 🏗️ Arquitectura del Lifecycle Service
- 🚀 Deployment Strategies
- 🔄 Rollback Mechanisms
- 📦 Version Management
- ⚕️ Health & Readiness Checks
- 🔧 APIs y SDKs
- 🎯 Kubernetes Operator
- 📁 Estructura de Documentación

## 🏗️ ARQUITECTURA DEL LIFECYCLE SERVICE

### **Componentes Core**

```yaml
lifecycle_architecture:
  deployment_controller:
    description: "Orquestador de deployments"
    technology: "Kubernetes Operator (Go)"
    features:
      - "Strategy selection (Rolling/Blue-Green/Canary)"
      - "Health monitoring durante deployment"
      - "Automatic rollback on failure"
      - "Progressive traffic shift (Canary)"
      - "Deployment hooks (pre/post)"
      
    deployment_strategies:
      rolling_update:
        description: "Gradual replacement"
        use_case: "Default para todos los tiers"
        zero_downtime: true
        rollback_speed: "fast"
        
      blue_green:
        description: "Dual environment swap"
        use_case: "Enterprise critical deployments"
        zero_downtime: true
        rollback_speed: "instant"
        
      canary:
        description: "Progressive rollout con traffic shift"
        use_case: "High-risk changes"
        zero_downtime: true
        rollback_speed: "automatic"
        phases:
          - "10% traffic → 30m monitoring"
          - "50% traffic → 1h monitoring"
          - "100% traffic → completion"
          
      recreate:
        description: "Stop old, start new (downtime)"
        use_case: "Emergency fixes, non-critical"
        zero_downtime: false
        rollback_speed: "fast"
        
  version_manager:
    description: "Gestión de versiones y compatibilidad"
    technology: "PostgreSQL + Semantic Versioning"
    features:
      - "Version registry"
      - "Compatibility matrix"
      - "Dependency resolution"
      - "Upgrade paths"
      
    compatibility_rules:
      nops_kernel:
        current_version: "1.5.0"
        compatible_edge_agents: [">=1.4.0", "<2.0.0"]
        compatible_inference_service: [">=2.0.0"]
        
      edge_agents:
        backward_compatibility: "1 minor version"
        forward_compatibility: "none"
        
  health_monitor:
    description: "Monitoreo de salud post-deployment"
    technology: "Prometheus + Custom checks"
    checks:
      liveness:
        endpoint: "/health"
        interval: "10s"
        timeout: "5s"
        failure_threshold: 3
        
      readiness:
        endpoint: "/ready"
        interval: "5s"
        timeout: "3s"
        failure_threshold: 2
        
      custom:
        - "error_rate < 1%"
        - "p95_latency < 500ms"
        - "success_rate > 95%"
        
    monitoring_window:
      rolling: "5 minutes"
      blue_green: "15 minutes"
      canary: "30 minutes per phase"
```

---

## 🚀 DEPLOYMENT STRATEGIES

### **1. Rolling Update (Default)**

```yaml
rolling_update_strategy:
  description: "Gradual replacement of old pods with new ones"
  
  configuration:
    max_surge: 1  # Max 1 extra pod during update
    max_unavailable: 0  # No pods down (zero downtime)
    
  process:
    1_create_new_pod:
      action: "Start 1 new pod with new version"
      wait_for: "Readiness probe success"
      
    2_shift_traffic:
      action: "Add new pod to load balancer"
      
    3_terminate_old:
      action: "Terminate 1 old pod"
      
    4_repeat:
      action: "Repeat until all pods replaced"
      
  rollback_trigger:
    - "Readiness check fails after 3 attempts"
    - "Error rate > 5% in new pods"
    - "Manual rollback command"
    
  example_kubernetes:
    yaml: |
      apiVersion: apps/v1
      kind: Deployment
      spec:
        replicas: 3
        strategy:
          type: RollingUpdate
          rollingUpdate:
            maxSurge: 1
            maxUnavailable: 0
```

### **2. Blue-Green Deployment**

```yaml
blue_green_strategy:
  description: "Deploy to new environment, instant switch"
  
  phases:
    1_deploy_green:
      action: "Deploy new version to 'green' environment"
      target: "green-deployment (separate from blue)"
      replicas: "Same as blue"
      
    2_validate_green:
      checks:
        - "All pods healthy"
        - "Smoke tests pass"
        - "Integration tests pass"
      duration: "15 minutes"
      
    3_switch_traffic:
      action: "Update Service selector to 'green'"
      effect: "Instant traffic shift (atomic)"
      
    4_monitor_green:
      duration: "30 minutes"
      rollback_if:
        - "Error rate > 1%"
        - "P95 latency > 2x baseline"
        
    5_decommission_blue:
      action: "Scale down blue deployment to 0"
      timing: "After 1 hour of stable green"
      keep_for_rollback: "24 hours"
```

### **3. Canary Deployment**

```yaml
canary_strategy:
  description: "Progressive rollout con traffic percentage"
  technology: "Flagger + Istio/Linkerd"
  
  phases:
    phase_1_10_percent:
      traffic_weight:
        canary: 10%
        stable: 90%
      duration: "30 minutes"
      success_criteria:
        - "error_rate_canary < 1%"
        - "latency_p95_canary < 1.2x stable"
        - "no_critical_alerts"
        
    phase_2_50_percent:
      traffic_weight:
        canary: 50%
        stable: 50%
      duration: "1 hour"
      success_criteria: "same as phase 1"
      
    phase_3_100_percent:
      traffic_weight:
        canary: 100%
        stable: 0%
      duration: "30 minutes final monitoring"
      
  automated_rollback:
    trigger: "Any success criteria fails"
    action: "Shift 100% traffic back to stable"
    alert: "PagerDuty P1"
```

---

## 🔄 ROLLBACK MECHANISMS

### **Automated Rollback Implementation**

```go
// lifecycle_service/operators/deployment_controller.go
package operators

import (
	"context"
	"time"
	appsv1 "k8s.io/api/apps/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
)

type DeploymentController struct {
	clientset *kubernetes.Clientset
	namespace string
}

// MonitorDeploymentHealth monitors deployment and triggers rollback if needed
func (dc *DeploymentController) MonitorDeploymentHealth(
	ctx context.Context,
	deploymentName string,
	strategy string,
) error {
	// 1. Get deployment
	deployment, err := dc.clientset.AppsV1().Deployments(dc.namespace).Get(
		ctx,
		deploymentName,
		metav1.GetOptions{},
	)
	if err != nil {
		return err
	}
	
	// 2. Monitor based on strategy
	var monitorDuration time.Duration
	switch strategy {
	case "rolling":
		monitorDuration = 5 * time.Minute
	case "blue-green":
		monitorDuration = 15 * time.Minute
	case "canary":
		monitorDuration = 30 * time.Minute
	}
	
	ticker := time.NewTicker(10 * time.Second)
	defer ticker.Stop()
	
	timeout := time.After(monitorDuration)
	
	for {
		select {
		case <-ticker.C:
			// 3. Check health metrics
			healthy, reason := dc.checkDeploymentHealth(ctx, deployment)
			
			if !healthy {
				// ROLLBACK TRIGGERED
				log.Errorf("Health check failed: %s. Triggering rollback.", reason)
				
				err := dc.RollbackDeployment(ctx, deploymentName)
				if err != nil {
					return fmt.Errorf("rollback failed: %w", err)
				}
				
				// Alert security/ops team
				dc.sendAlert("deployment_rolled_back", map[string]interface{}{
					"deployment": deploymentName,
					"reason":     reason,
					"strategy":   strategy,
				})
				
				return fmt.Errorf("deployment rolled back due to: %s", reason)
			}
			
		case <-timeout:
			log.Infof("Monitoring period completed successfully for %s", deploymentName)
			return nil
			
		case <-ctx.Done():
			return ctx.Err()
		}
	}
}

// RollbackDeployment performs automated rollback to previous revision
func (dc *DeploymentController) RollbackDeployment(
	ctx context.Context,
	deploymentName string,
) error {
	// 1. Get current deployment
	deployment, err := dc.clientset.AppsV1().Deployments(dc.namespace).Get(
		ctx,
		deploymentName,
		metav1.GetOptions{},
	)
	if err != nil {
		return err
	}
	
	// 2. Get revision history
	revisions, err := dc.clientset.AppsV1().ReplicaSets(dc.namespace).List(
		ctx,
		metav1.ListOptions{
			LabelSelector: metav1.FormatLabelSelector(deployment.Spec.Selector),
		},
	)
	if err != nil {
		return err
	}
	
	// 3. Find previous stable revision
	var previousRevision *appsv1.ReplicaSet
	for _, rs := range revisions.Items {
		if rs.Annotations["deployment.kubernetes.io/revision"] == 
		   fmt.Sprintf("%d", deployment.Annotations["deployment.kubernetes.io/revision"]-1) {
			previousRevision = &rs
			break
		}
	}
	
	if previousRevision == nil {
		return fmt.Errorf("no previous revision found for rollback")
	}
	
	// 4. Perform rollback (kubectl rollout undo equivalent)
	deployment.Spec.Template = previousRevision.Spec.Template
	
	_, err = dc.clientset.AppsV1().Deployments(dc.namespace).Update(
		ctx,
		deployment,
		metav1.UpdateOptions{},
	)
	
	if err != nil {
		return err
	}
	
	log.Infof("Rollback initiated for deployment %s to revision %d",
		deploymentName,
		previousRevision.Annotations["deployment.kubernetes.io/revision"],
	)
	
	return nil
}

// checkDeploymentHealth validates deployment health
func (dc *DeploymentController) checkDeploymentHealth(
	ctx context.Context,
	deployment *appsv1.Deployment,
) (healthy bool, reason string) {
	// 1. Check pod readiness
	if deployment.Status.ReadyReplicas < deployment.Status.Replicas {
		return false, fmt.Sprintf(
			"not all replicas ready: %d/%d",
			deployment.Status.ReadyReplicas,
			deployment.Status.Replicas,
		)
	}
	
	// 2. Check Prometheus metrics (error rate)
	errorRate := dc.queryPrometheus(
		fmt.Sprintf(
			`rate(http_requests_total{deployment="%s",status=~"5.."}[5m]) / rate(http_requests_total{deployment="%s"}[5m])`,
			deployment.Name,
			deployment.Name,
		),
	)
	
	if errorRate > 0.05 {  // 5% error rate threshold
		return false, fmt.Sprintf("error rate too high: %.2f%%", errorRate*100)
	}
	
	// 3. Check latency (p95)
	p95Latency := dc.queryPrometheus(
		fmt.Sprintf(
			`histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{deployment="%s"}[5m]))`,
			deployment.Name,
		),
	)
	
	if p95Latency > 2.0 {  // 2s p95 threshold
		return false, fmt.Sprintf("latency too high: %.2fs", p95Latency)
	}
	
	return true, ""
}
```

---

## 📦 VERSION MANAGEMENT

### **Compatibility Matrix**

```yaml
version_compatibility:
  nops_kernel_1_5_0:
    release_date: "2025-09-01"
    compatible_agents:
      min_version: "1.4.0"
      max_version: "1.9.9"
      
    compatible_inference_service:
      min_version: "2.0.0"
      
    breaking_changes:
      - "API v2 deprecation (use v3)"
      - "Event schema v1 removed"
      
  edge_agent_1_6_0:
    release_date: "2025-09-15"
    requires_nops_kernel: ">=1.5.0"
    
    new_features:
      - "Multi-model routing"
      - "Streaming responses"
      
    backward_compatible: true
    
  upgrade_paths:
    from_1_4_to_1_5:
      safe: true
      steps:
        - "Upgrade NOPS Kernel first"
        - "Rolling update Edge Agents"
        - "Verify compatibility"
        
    from_1_3_to_1_5:
      safe: false
      reason: "Must upgrade to 1.4 first"
      required_steps:
        - "1.3 → 1.4 (with data migration)"
        - "1.4 → 1.5 (standard rolling)"
```

---

## ⚕️ HEALTH & READINESS CHECKS

### **Health Check Endpoints**

```python
# edge_agents/shared/health.py
from fastapi import FastAPI, Response
from typing import Dict, Any

app = FastAPI()

@app.get("/health")
async def liveness_check() -> Dict[str, str]:
    """
    Liveness probe - Is the service alive?
    
    Used by Kubernetes to restart dead containers
    Returns 200 if process is running
    """
    return {"status": "alive"}

@app.get("/ready")
async def readiness_check() -> Response:
    """
    Readiness probe - Is the service ready to serve traffic?
    
    Used by Kubernetes to add/remove from load balancer
    Returns 200 only if all dependencies are ready
    """
    checks = {
        "database": await check_database_connection(),
        "redis": await check_redis_connection(),
        "inference_service": await check_inference_service(),
    }
    
    all_ready = all(checks.values())
    
    if all_ready:
        return Response(
            content=json.dumps({"status": "ready", "checks": checks}),
            status_code=200
        )
    else:
        return Response(
            content=json.dumps({"status": "not_ready", "checks": checks}),
            status_code=503  # Service Unavailable
        )

async def check_database_connection() -> bool:
    """Check if database is accessible"""
    try:
        await db.execute("SELECT 1")
        return True
    except Exception:
        return False

async def check_redis_connection() -> bool:
    """Check if Redis is accessible"""
    try:
        await redis.ping()
        return True
    except Exception:
        return False

async def check_inference_service() -> bool:
    """Check if Inference Service is accessible"""
    try:
        response = await httpx_client.get(
            "https://inference-service/health",
            timeout=5
        )
        return response.status_code == 200
    except Exception:
        return False
```

---

## 🔧 APIS Y SDKS

```yaml
lifecycle_api:
  POST /api/v1/deployments:
    description: "Create new deployment"
    auth: "mTLS + JWT (CI/CD pipeline)"
    request:
      agent_id: "string"
      version: "string (semver)"
      strategy: "rolling|blue-green|canary"
      target_replicas: "int"
    response:
      deployment_id: "uuid"
      status: "pending|in_progress|completed|failed"
      
  POST /api/v1/deployments/{id}/rollback:
    description: "Rollback deployment"
    auth: "mTLS + JWT"
    response:
      rollback_status: "completed|in_progress"
      
  GET /api/v1/deployments/{id}/status:
    description: "Get deployment status"
    auth: "JWT"
    response:
      status: "string"
      current_phase: "string"
      health_checks: "object"
```

---

## 🎯 KUBERNETES OPERATOR

### **Lifecycle CRD (Custom Resource Definition)**

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: agentdeployments.enis.andaon.com
spec:
  group: enis.andaon.com
  names:
    kind: AgentDeployment
    plural: agentdeployments
    singular: agentdeployment
    shortNames:
      - agentdeploy
  scope: Namespaced
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                agentId:
                  type: string
                version:
                  type: string
                strategy:
                  type: string
                  enum: [rolling, blue-green, canary, recreate]
                replicas:
                  type: integer
                  minimum: 1
                healthCheck:
                  type: object
                  properties:
                    endpoint:
                      type: string
                    interval:
                      type: string
            status:
              type: object
              properties:
                phase:
                  type: string
                  enum: [pending, deploying, healthy, unhealthy, rolled_back]
                currentReplicas:
                  type: integer
                readyReplicas:
                  type: integer
```

---

## 📁 ESTRUCTURA DE DOCUMENTACIÓN

```yaml
documentation_structure:
  lifecycle_service/:
    - "README.md"
    - "42-lifecycle-master-prompt.md"
    - "DEPLOYMENT_STRATEGIES.md"
    - "ROLLBACK_GUIDE.md"
    
  operators/:
    - "lifecycle-operator.go"
    - "deployment-controller.go"
    - "health-monitor.go"
    
  helm-charts/:
    - "lifecycle-service/"
    - "agent-deployment/"
```

---

## 📋 METADATA DE CIERRE

```yaml
service_summary:
  nombre: "Lifecycle Service"
  proposito: "Deployment strategies, rollbacks, version management"
  prioridad: "P3"
  
  componentes_principales:
    - "Deployment Controller (K8s Operator)"
    - "Version Manager"
    - "Health Monitor"
    - "Automated Rollback Engine"
    
  deployment_strategies:
    - "Rolling Update (default)"
    - "Blue-Green (Enterprise)"
    - "Canary (progressive)"
    - "Recreate (emergency)"
    
  stack_tecnologico:
    - "Kubernetes Operator (Go)"
    - "Helm charts"
    - "Prometheus (health monitoring)"
    - "Flagger (Canary)"
    
estado: "ready_for_sprint_s23-p2"
estimated_completion: "1 semana"
total_lines: "~1,200 líneas"
```

---

*Master Prompt Lifecycle Service v1.0 - Creado 2025-10-08*  
*Estado: Versión profesional completa*  
*Operational-critical: Zero-downtime deployments*
