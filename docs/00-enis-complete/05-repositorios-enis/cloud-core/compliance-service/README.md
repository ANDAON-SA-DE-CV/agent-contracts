# 🔐 Compliance Service - ENIS v3.0

## 📋 Metadata

```yaml
service_name: "compliance-service"
service_type: "Platform Service (CRITICAL)"
category: "cloud-core"
priority: "P1 - CRÍTICA"
status: "📋 Planned - Sprint S22-P4"
stack: "Python 3.11+ / FastAPI"
dependencies: ["PostgreSQL", "S3", "HSM", "Blockchain (opcional)"]
dna_version: "3.0"
```

---

## 🎯 Propósito

Servicio de compliance y auditoría extraído del NOPS Kernel (arquitectura SLIM).

Proporciona:
- **Audit trail inmutable** (append-only storage)
- **SEC (Signed Execution Contract) validation**
- **Regulatory compliance** (SOC2, GDPR, HIPAA, ISO27001)
- **Forensics** y análisis de seguridad
- **Export de evidencias** para auditorías externas

---

## 🏗️ Arquitectura

### Principio SLIM:
Este servicio es **EXTERNO** al NOPS Kernel. El kernel usa `ComplianceAPIClient` con **fallback local obligatorio**.

```yaml
comunicacion:
  nops_kernel:
    protocolo: "mTLS + JWT s2s"
    endpoint: "POST /api/v1/audit"
    timeout: "10s (más largo, crítico)"
    fallback: "SIEMPRE persiste localmente en /var/log/nops/audit.jsonl"
    
  sec_validation:
    endpoint: "POST /api/v1/sec/validate"
    protocolo: "mTLS"
    uso: "Validar firmas de binarios (S13.5)"
    
  regulatory:
    export: "GET /api/v1/compliance/report"
    formatos: ["PDF", "CSV", "JSON"]
```

---

## 📦 Stack Tecnológico

```yaml
backend:
  framework: "FastAPI"
  runtime: "Python 3.11+"
  
storage:
  database: "PostgreSQL (append-only tables)"
  immutable_storage: "AWS S3 / MinIO (write-once-read-many)"
  blockchain: "Hyperledger Fabric (opcional para audit proofs)"
  
security:
  encryption: "AES-256-GCM + HSM"
  signing: "ECDSA/RSA + Hardware Security Module"
  compliance: "SOC2 Type II, HIPAA, GDPR, ISO27001"
  
sec_validation:
  signing: "Cosign / Sigstore"
  sbom: "CycloneDX / SPDX"
  provenance: "SLSA framework"
```

---

## 📡 APIs Principales

### POST /api/v1/audit
Recibir eventos de auditoría

### POST /api/v1/sec/validate
Validar firmas SEC

### GET /api/v1/compliance/report
Generar reportes de compliance

### POST /api/v1/forensics/investigate
Análisis forense

---

## 🚀 Sprint de Implementación

**Sprint:** S22-P4  
**Duración:** 1.5 semanas  
**Prioridad:** P1 (CRÍTICA - SEC VALIDATION)

**Blocker para:**
- S13.5 SEC (Supply Chain Integrity)
- S14 Pre-GA Gate

---

*Servicio creado: 2025-10-08*  
*Estado: Planned - Sprint S22-P4*

