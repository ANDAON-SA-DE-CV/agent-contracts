<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
Índice

- [🏗️ ENIS-INFRASTRUCTURE - MASTER PROMPT v3.0](#-enis-infrastructure---master-prompt-v30)
  - [🎯 **OBJETIVO PRINCIPAL**](#-objetivo-principal)
  - [📋 **ARQUITECTURA DEL REPOSITORIO**](#-arquitectura-del-repositorio)
    - [**Estructura de Directorios**](#estructura-de-directorios)
  - [🔧 **ESPECIFICACIONES TÉCNICAS**](#-especificaciones-t%C3%89cnicas)
    - [**Terraform Modules**](#terraform-modules)
    - [**Kubernetes Manifests**](#kubernetes-manifests)
    - [**Helm Charts**](#helm-charts)
    - [**Docker Compose**](#docker-compose)
    - [**GitHub Actions Workflows**](#github-actions-workflows)
    - [**Security Pipeline**](#security-pipeline)
  - [🧪 **TESTING**](#-testing)
    - [**Terraform Tests**](#terraform-tests)
    - [**Kubernetes Tests**](#kubernetes-tests)
  - [📊 **MÉTRICAS DE ÉXITO**](#-m%C3%89tricas-de-%C3%89xito)
    - [**Métricas Técnicas**](#m%C3%A9tricas-t%C3%A9cnicas)
    - [**Métricas de Calidad**](#m%C3%A9tricas-de-calidad)
  - [🚀 **PRÓXIMOS PASOS**](#-pr%C3%93ximos-pasos)
    - [**Inmediato (Semana 1-2)**](#inmediato-semana-1-2)
    - [**Corto Plazo (Semana 3-4)**](#corto-plazo-semana-3-4)
    - [**Mediano Plazo (Semana 5-6)**](#mediano-plazo-semana-5-6)
    - [**Largo Plazo (Mes 2+)**](#largo-plazo-mes-2)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# 🏗️ ENIS-INFRASTRUCTURE - MASTER PROMPT v3.0

**Propósito:** Infrastructure as Code unificado y CI/CD para ENIS v3.0
**Tecnología:** Terraform, Kubernetes, Helm, Docker, GitHub Actions
**Estado:** 📋 Planificado - Infraestructura consolidada

---

## 🎯 **OBJETIVO PRINCIPAL**

Crear un repositorio que consolide toda la infraestructura como código y CI/CD para ENIS v3.0, incluyendo:

1. **Terraform Modules** - Infraestructura cloud modular
2. **Kubernetes Manifests** - Configuraciones K8s base y overlays
3. **Helm Charts** - Charts para todos los servicios ENIS
4. **Docker Configurations** - Dockerfiles y docker-compose
5. **CI/CD Workflows** - GitHub Actions reutilizables
6. **Security Pipeline** - Cosign, SBOM, SAST, CVE policy

---

## 📋 **ARQUITECTURA DEL REPOSITORIO**

### **Estructura de Directorios**
```
enis-infrastructure/
├── terraform/                  # Infrastructure as Code
│   ├── modules/                # Terraform modules
│   │   ├── vpc/               # VPC module
│   │   ├── eks/               # EKS cluster
│   │   ├── rds/               # RDS database
│   │   ├── redis/             # Redis cluster
│   │   ├── s3/                # S3 buckets
│   │   ├── monitoring/        # Monitoring stack
│   │   ├── security/          # Security modules
│   │   └── networking/        # Networking modules
│   ├── environments/           # Environment configs
│   │   ├── dev/               # Development
│   │   ├── staging/           # Staging
│   │   └── prod/              # Production
│   └── README.md
├── kubernetes/                 # K8s manifests
│   ├── base/                  # Base configurations
│   │   ├── namespaces/
│   │   ├── rbac/
│   │   ├── configmaps/
│   │   └── secrets/
│   ├── overlays/              # Environment overlays
│   │   ├── dev/
│   │   ├── staging/
│   │   └── prod/
│   └── README.md
├── helm/                       # Helm charts
│   ├── charts/                # Helm charts
│   │   ├── nops-kernel/
│   │   ├── inference-service/
│   │   ├── asm-service/
│   │   ├── cgn-service/
│   │   ├── awe-service/
│   │   ├── shif-service/
│   │   ├── edge-infrastructure/
│   │   ├── cloud-infrastructure/
│   │   ├── agent-marketplace/
│   │   └── enis-frontend/
│   └── README.md
├── docker/                     # Docker configs
│   ├── compose/               # Docker Compose files
│   │   ├── dev.yml
│   │   ├── staging.yml
│   │   └── prod.yml
│   └── Dockerfiles/           # Dockerfiles
├── .github/                    # GitHub Actions
│   └── workflows/             # CI/CD workflows
│       ├── ci-reusable.yml   # CI reutilizable
│       ├── cd-reusable.yml   # CD reutilizable
│       ├── security-scan.yml # SAST, CVE policy
│       ├── sbom-generation.yml # SBOM
│       ├── cosign-signing.yml # Cosign
│       └── terraform-apply.yml # Terraform
├── scripts/                    # Scripts de utilidad
│   ├── setup-dev.sh
│   ├── deploy-staging.sh
│   ├── deploy-prod.sh
│   ├── backup.sh
│   └── cleanup.sh
├── docs/                       # Documentación
│   ├── deployment/            # Deployment guides
│   ├── security/              # Security guides
│   ├── troubleshooting/       # Troubleshooting
│   └── runbooks/              # Operational runbooks
├── tests/                      # Tests
│   ├── terraform/             # Terraform tests
│   ├── kubernetes/            # K8s tests
│   └── integration/           # Integration tests
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## 🔧 **ESPECIFICACIONES TÉCNICAS**

### **Terraform Modules**
```hcl
# terraform/modules/eks/main.tf
resource "aws_eks_cluster" "enis_cluster" {
  name     = var.cluster_name
  role_arn = aws_iam_role.cluster.arn
  version  = var.kubernetes_version

  vpc_config {
    subnet_ids              = var.subnet_ids
    endpoint_private_access = true
    endpoint_public_access  = true
    public_access_cidrs     = var.public_access_cidrs
  }

  enabled_cluster_log_types = [
    "api",
    "audit",
    "authenticator",
    "controllerManager",
    "scheduler"
  ]

  depends_on = [
    aws_iam_role_policy_attachment.cluster_AmazonEKSClusterPolicy,
    aws_cloudwatch_log_group.cluster,
  ]

  tags = var.tags
}

resource "aws_eks_node_group" "enis_nodes" {
  cluster_name    = aws_eks_cluster.enis_cluster.name
  node_group_name = var.node_group_name
  node_role_arn   = aws_iam_role.node.arn
  subnet_ids      = var.subnet_ids
  instance_types  = var.instance_types

  scaling_config {
    desired_size = var.desired_size
    max_size     = var.max_size
    min_size     = var.min_size
  }

  update_config {
    max_unavailable_percentage = var.max_unavailable_percentage
  }

  depends_on = [
    aws_iam_role_policy_attachment.node_AmazonEKSWorkerNodePolicy,
    aws_iam_role_policy_attachment.node_AmazonEKS_CNI_Policy,
    aws_iam_role_policy_attachment.node_AmazonEC2ContainerRegistryReadOnly,
  ]

  tags = var.tags
}
```

### **Kubernetes Manifests**
```yaml
# kubernetes/base/namespaces/enis.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: enis
  labels:
    name: enis
    environment: base
---
# kubernetes/base/rbac/cluster-admin.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: enis-admin
rules:
- apiGroups: [""]
  resources: ["*"]
  verbs: ["*"]
- apiGroups: ["apps"]
  resources: ["*"]
  verbs: ["*"]
- apiGroups: ["networking.k8s.io"]
  resources: ["*"]
  verbs: ["*"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: enis-admin-binding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: enis-admin
subjects:
- kind: ServiceAccount
  name: enis-admin
  namespace: enis
```

### **Helm Charts**
```yaml
# helm/charts/nops-kernel/values.yaml
replicaCount: 3

image:
  repository: enis/nops-kernel
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 8000

ingress:
  enabled: true
  className: nginx
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
  hosts:
    - host: nops-kernel.enis.local
      paths:
        - path: /
          pathType: Prefix

resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80

persistence:
  enabled: true
  storageClass: gp2
  accessMode: ReadWriteOnce
  size: 10Gi

env:
  REDIS_HOST: redis
  REDIS_PORT: 6379
  DATABASE_URL: postgresql://user:pass@postgres:5432/enis

monitoring:
  enabled: true
  prometheus:
    enabled: true
  grafana:
    enabled: true
```

### **Docker Compose**
```yaml
# docker/compose/dev.yml
version: '3.8'

services:
  nops-kernel:
    build:
      context: ../../nops-kernel
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - DATABASE_URL=postgresql://user:pass@postgres:5432/enis
    depends_on:
      - redis
      - postgres
    volumes:
      - ../../nops-kernel:/app
    networks:
      - enis-network

  inference-service:
    build:
      context: ../../inference-service
      dockerfile: Dockerfile
    ports:
      - "8001:8000"
    environment:
      - NOPS_KERNEL_URL=http://nops-kernel:8000
    depends_on:
      - nops-kernel
    networks:
      - enis-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - enis-network

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: enis
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - enis-network

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    networks:
      - enis-network

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana
    networks:
      - enis-network

volumes:
  redis-data:
  postgres-data:
  grafana-data:

networks:
  enis-network:
    driver: bridge
```

### **GitHub Actions Workflows**
```yaml
# .github/workflows/ci-reusable.yml
name: CI Reusable

on:
  workflow_call:
    inputs:
      service-name:
        description: 'Service name'
        required: true
        type: string
      dockerfile-path:
        description: 'Dockerfile path'
        required: false
        type: string
        default: './Dockerfile'
      test-command:
        description: 'Test command'
        required: false
        type: string
        default: 'pytest'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run tests
        run: ${{ inputs.test-command }}
      
      - name: Run linting
        run: |
          flake8 .
          black --check .
          isort --check-only .

  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          file: ${{ inputs.dockerfile-path }}
          push: true
          tags: |
            enis/${{ inputs.service-name }}:latest
            enis/${{ inputs.service-name }}:${{ github.sha }}
```

### **Security Pipeline**
```yaml
# .github/workflows/security-scan.yml
name: Security Scan

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  sbom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          path: .
          format: spdx-json
          output-file: sbom.spdx.json
      
      - name: Upload SBOM
        uses: actions/upload-artifact@v3
        with:
          name: sbom
          path: sbom.spdx.json

  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run CodeQL Analysis
        uses: github/codeql-action/analyze@v2
        with:
          languages: python

  cve-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

  cosign:
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      
      - name: Install Cosign
        uses: sigstore/cosign-installer@v2
      
      - name: Sign container image
        run: |
          echo "${{ secrets.COSIGN_PRIVATE_KEY }}" > cosign.key
          cosign sign --key cosign.key enis/${{ inputs.service-name }}:${{ github.sha }}
```

---

## 🧪 **TESTING**

### **Terraform Tests**
```python
# tests/terraform/test_eks_module.py
import pytest
import terraform_compliance


class TestEKSModule:
    def test_eks_cluster_created(self):
        """Test EKS cluster is created"""
        assert terraform_compliance.check_resource_exists("aws_eks_cluster")
    
    def test_eks_cluster_version(self):
        """Test EKS cluster version"""
        cluster = terraform_compliance.get_resource("aws_eks_cluster")
        assert cluster.version == "1.28"
    
    def test_eks_cluster_logging_enabled(self):
        """Test EKS cluster logging is enabled"""
        cluster = terraform_compliance.get_resource("aws_eks_cluster")
        assert "api" in cluster.enabled_cluster_log_types
        assert "audit" in cluster.enabled_cluster_log_types
    
    def test_eks_node_group_created(self):
        """Test EKS node group is created"""
        assert terraform_compliance.check_resource_exists("aws_eks_node_group")
    
    def test_eks_node_group_scaling(self):
        """Test EKS node group scaling configuration"""
        node_group = terraform_compliance.get_resource("aws_eks_node_group")
        assert node_group.scaling_config.desired_size >= 1
        assert node_group.scaling_config.max_size >= node_group.scaling_config.desired_size
```

### **Kubernetes Tests**
```python
# tests/kubernetes/test_manifests.py
import pytest
import yaml
from pathlib import Path

class TestKubernetesManifests:
    def test_namespace_created(self):
        """Test namespace manifest is valid"""
        manifest_path = Path("kubernetes/base/namespaces/enis.yaml")
        with open(manifest_path, 'r') as f:
            manifest = yaml.safe_load(f)
        
        assert manifest['kind'] == 'Namespace'
        assert manifest['metadata']['name'] == 'enis'
    
    def test_rbac_created(self):
        """Test RBAC manifests are valid"""
        rbac_path = Path("kubernetes/base/rbac/cluster-admin.yaml")
        with open(rbac_path, 'r') as f:
            manifests = list(yaml.safe_load_all(f))
        
        # Check ClusterRole
        cluster_role = manifests[0]
        assert cluster_role['kind'] == 'ClusterRole'
        assert cluster_role['metadata']['name'] == 'enis-admin'
        
        # Check ClusterRoleBinding
        cluster_role_binding = manifests[1]
        assert cluster_role_binding['kind'] == 'ClusterRoleBinding'
        assert cluster_role_binding['metadata']['name'] == 'enis-admin-binding'
    
    def test_manifests_syntax(self):
        """Test all manifests have valid YAML syntax"""
        manifests_dir = Path("kubernetes/base")
        
        for manifest_file in manifests_dir.rglob("*.yaml"):
            with open(manifest_file, 'r') as f:
                try:
                    yaml.safe_load_all(f)
                except yaml.YAMLError as e:
                    pytest.fail(f"Invalid YAML in {manifest_file}: {e}")
```

---

## 📊 **MÉTRICAS DE ÉXITO**

### **Métricas Técnicas**
- **Infrastructure Coverage**: 100% of services covered
- **Deployment Time**: < 30 minutes for full deployment
- **Rollback Time**: < 5 minutes for rollback
- **Security Compliance**: 100% of security policies enforced

### **Métricas de Calidad**
- **Test Coverage**: > 90% for infrastructure code
- **Documentation**: 100% of components documented
- **Automation**: 100% of processes automated
- **Reliability**: 99.9% deployment success rate

---

## 🚀 **PRÓXIMOS PASOS**

### **Inmediato (Semana 1-2)**
1. ✅ Crear repositorio enis-infrastructure
2. ✅ Consolidar archivos dispersos
3. ✅ Implementar Terraform modules base

### **Corto Plazo (Semana 3-4)**
1. 🔨 Implementar Kubernetes manifests
2. 🔨 Implementar Helm charts
3. 🔨 Configurar CI/CD workflows

### **Mediano Plazo (Semana 5-6)**
1. 🔨 Implementar security pipeline
2. 🔨 Configurar monitoring stack
3. 🔨 Implementar backup strategies

### **Largo Plazo (Mes 2+)**
1. 🔨 Optimizar deployment processes
2. 🔨 Implementar multi-region support
3. 🔨 Expandir automation

---

*Master Prompt generado para ENIS v3.0 - ENIS Infrastructure - Enero 2025*
