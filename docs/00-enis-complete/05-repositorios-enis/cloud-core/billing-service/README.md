# 💰 Billing Service - ENIS v3.0

## 📋 Metadata

```yaml
service_name: "billing-service"
service_type: "Platform Service (CRITICAL)"
category: "cloud-core"
priority: "P1 - CRÍTICA"
status: "📋 Planned - Sprint S22-P3"
stack: "Python 3.11+ / FastAPI"
dependencies: ["Stripe API", "PostgreSQL", "Redis Streams"]
dna_version: "3.0"
```

---

## 🎯 Propósito

Servicio de facturación y metering extraído del NOPS Kernel (arquitectura SLIM).

Proporciona:
- **Usage tracking** en tiempo real
- **Metering multi-tier** (🟤🟡🟢🔵🔴)
- **Generación de invoices**
- **Integración con payment gateways** (Stripe/PayPal)
- **Credits y discounts management**
- **Revenue analytics**

---

## 🏗️ Arquitectura

### Principio SLIM:
Este servicio es **EXTERNO** al NOPS Kernel. El kernel usa `BillingAPIClient` para enviar eventos de uso.

```yaml
comunicacion:
  nops_kernel:
    protocolo: "mTLS + JWT s2s"
    endpoint: "POST /api/v1/usage"
    queue_local: "Redis (7 días retención)"
    degraded_mode: "Queue local para retry"
    
  payment_gateways:
    stripe: "API REST"
    paypal: "API REST"
    
  frontend:
    dashboard: "Billing analytics"
    invoices: "PDF generation"
```

---

## 📦 Stack Tecnológico

```yaml
backend:
  framework: "FastAPI"
  runtime: "Python 3.11+"
  async: "asyncio + uvloop"
  
storage:
  database: "PostgreSQL (transaccional)"
  queue: "Redis Streams"
  cache: "Redis"
  
integrations:
  payment: "Stripe API / PayPal API"
  invoicing: "WeasyPrint (PDF generation)"
  reporting: "Metabase / Superset"
  
security:
  pci_compliance: "PCI-DSS Level 1"
  encryption: "AES-256-GCM"
  audit: "Immutable billing logs"
```

---

## 📡 APIs Principales

### POST /api/v1/usage
Recibir eventos de uso del kernel

### POST /api/v1/invoices
Generar invoice

### POST /api/v1/payments
Procesar pago

### GET /api/v1/usage/{tenant_id}
Query de uso

---

## 🚀 Sprint de Implementación

**Sprint:** S22-P3  
**Duración:** 1.5 semanas  
**Prioridad:** P1 (CRÍTICA - CRITICAL PATH)

---

*Servicio creado: 2025-10-08*  
*Estado: Planned - Sprint S22-P3*

