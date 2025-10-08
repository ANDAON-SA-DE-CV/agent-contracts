# 41 - Compliance Service Master Prompt

## Metadata

```yaml
prompt_id: "41"
prompt_name: "compliance-master-prompt"
service_name: "compliance-service"
version: "1.0.0"
category: "cloud-core"
dna_version: "3.0"
created: "2025-10-08"
status: "active"
priority: "P1 - CRÍTICO"
sprint: "S22-P4"
compliance: ["SOC2 Type II", "GDPR", "HIPAA", "ISO27001"]
```

---

## 🎯 Propósito del Servicio

El **Compliance Service** gestiona audit trails, SEC validation y compliance regulatorio para ENIS v3.0.

### Responsabilidades Core:

```yaml
responsabilidades:
  audit_trail:
    - "Almacenamiento inmutable de eventos de auditoría"
    - "Append-only storage (no deletes, no updates)"
    - "Redundancia geográfica"
    - "Retention configurable (1-7 años)"
    
  sec_validation:
    - "Validación de firmas criptográficas (S13.5)"
    - "SBOM (Software Bill of Materials) verification"
    - "Provenance validation (SLSA framework)"
    - "Supply chain integrity checks"
    
  regulatory:
    - "SOC2 Type II compliance"
    - "GDPR data protection"
    - "HIPAA healthcare compliance"
    - "ISO27001 information security"
    - "PCI-DSS (coordination con billing)"
    
  forensics:
    - "Investigation support"
    - "Timeline reconstruction"
    - "Anomaly detection"
    - "Evidence export"
```

---

## 🏗️ Arquitectura del Servicio

### Stack Tecnológico:

```yaml
backend:
  framework: "FastAPI"
  runtime: "Python 3.11+"
  
storage:
  primary: "PostgreSQL (append-only tables)"
  immutable: "AWS S3 / MinIO (WORM - Write Once Read Many)"
  blockchain: "Hyperledger Fabric (opcional)"
  backup: "Geo-redundant backups"
  
sec_validation:
  signing: "Cosign / Sigstore"
  verification: "OpenSSL + HSM"
  sbom: "CycloneDX / SPDX parsers"
  provenance: "SLSA attestation verification"
  
security:
  encryption_at_rest: "AES-256-GCM + HSM"
  encryption_in_transit: "TLS 1.3"
  key_management: "AWS KMS / HashiCorp Vault"
  
compliance_frameworks:
  - "SOC2 Type II"
  - "GDPR"
  - "HIPAA"
  - "ISO27001"
  - "PCI-DSS (partial)"
```

---

## 📡 APIs Principales

### 1. Audit Trail

```yaml
POST /api/v1/audit:
  descripcion: "Recibir eventos de auditoría del NOPS Kernel"
  auth: "mTLS + JWT s2s"
  payload:
    event_type: string
    tenant_id: string
    timestamp: ISO8601
    severity: "DEBUG|INFO|WARNING|ERROR|CRITICAL"
    details: object
    
  response:
    status: 201
    event_id: string (UUID)
    stored: true
    
  garantias:
    - "NUNCA se pierde un evento (fallback local)"
    - "Inmutable (append-only)"
    - "Redundante (multi-region)"
```

### 2. SEC Validation

```yaml
POST /api/v1/sec/validate:
  descripcion: "Validar firma SEC de binario/contenedor"
  auth: "mTLS + JWT s2s"
  payload:
    artifact_hash: string (SHA256)
    signature: string (base64)
    signing_cert: string (PEM)
    sbom: object (CycloneDX/SPDX)
    
  response:
    valid: boolean
    validation_details:
      signature_valid: boolean
      cert_trusted: boolean
      sbom_verified: boolean
      provenance_valid: boolean
    validation_timestamp: ISO8601
    
  enforcement:
    🟤🟡🟢: "warning (log only)"
    🔵🔴: "block (reject execution)"
```

### 3. Compliance Reports

```yaml
GET /api/v1/compliance/report:
  auth: "JWT + RBAC (admin only)"
  parameters:
    tenant_id: string
    framework: "soc2|gdpr|hipaa|iso27001"
    period: ISO8601 range
    
  response:
    format: "PDF|CSV|JSON"
    report:
      compliance_score: float (0-100)
      violations: array
      evidence: array
      recommendations: array
```

---

## 🔐 Seguridad y Compliance

```yaml
security:
  audit_trail_immutability:
    method: "Append-only PostgreSQL + S3 Object Lock"
    verification: "Hash chain (Merkle tree)"
    tamper_detection: "Continuous monitoring"
    
  sec_enforcement:
    by_tier:
      basic: "Logging only (🟤🟡🟢)"
      strict: "Blocking execution (🔵🔴)"
    
  regulatory:
    soc2:
      controls: "CC6.1, CC7.2, CC7.3"
      evidence: "Automated collection"
    gdpr:
      rights: "Right to access, right to erasure (audit logs exempt)"
    hipaa:
      phi: "Audit logs encrypted + access controlled"
```

---

## 🚀 Deployment

```yaml
deployment:
  platform: "Kubernetes"
  replicas: "3 (HA + geo-distributed)"
  resources:
    cpu: "1-2 cores"
    memory: "2-4 GB"
    storage: "10-100 TB (S3)"
    
  dependencies:
    - "PostgreSQL cluster (HA)"
    - "S3 / MinIO"
    - "HSM (AWS KMS / YubiHSM)"
    - "Vault (secrets)"
```

---

## 🔗 Cross-References

```yaml
master_prompts_relacionados:
  - "18-security-master-prompt.md"
  - "07-nops-master-prompt.md" (ComplianceAPIClient)
  - "ROADMAP_SPRINTS_NOPS_KERNEL.md" (S13.5 SEC)
```

---

*Master Prompt creado: 2025-10-08*  
*Estado: Active - P1 CRÍTICO (SEC)*

