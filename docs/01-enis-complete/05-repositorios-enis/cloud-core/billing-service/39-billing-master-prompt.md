# 39 - Billing Service Master Prompt

## Metadata

```yaml
prompt_id: "39"
prompt_name: "billing-master-prompt"
service_name: "billing-service"
version: "1.0.0"
category: "cloud-core"
dna_version: "3.0"
created: "2025-10-08"
status: "active"
priority: "P1 - CRÍTICO"
sprint: "S22-P3"
compliance: ["PCI-DSS Level 1"]
```

---

## 🎯 Propósito del Servicio

El **Billing Service** gestiona facturación, metering y revenue para ENIS v3.0.

### Responsabilidades Core:

```yaml
responsabilidades:
  metering:
    - "Usage tracking en tiempo real"
    - "Agregación por tenant y tier (🟤🟡🟢🔵🔴)"
    - "Métricas de uso: CPU, memoria, storage, network, executions"
    
  pricing:
    - "Modelos multi-tier configurables"
    - "Pay-as-you-go + Reserved + Spot pricing"
    - "Volume discounts y enterprise contracts"
    - "Credits management"
    
  invoicing:
    - "Generación automática de invoices"
    - "PDF generation con templates"
    - "Multi-currency support"
    - "Tax calculation por región"
    
  payments:
    - "Integración Stripe API"
    - "Integración PayPal API"
    - "Webhook handling de payment events"
    - "PCI-DSS compliance"
    
  reporting:
    - "Revenue analytics"
    - "Usage forecasting"
    - "Churn prediction"
```

---

## 🏗️ Arquitectura del Servicio

### Stack Tecnológico:

```yaml
backend:
  framework: "FastAPI"
  runtime: "Python 3.11+"
  async: "asyncio + uvloop"
  
storage:
  database: "PostgreSQL (transaccional ACID)"
  queue: "Redis Streams (usage events)"
  cache: "Redis (hot data)"
  
payments:
  stripe: "Stripe Python SDK"
  paypal: "PayPal REST API"
  
invoicing:
  pdf: "WeasyPrint"
  templates: "Jinja2"
  
security:
  pci_compliance: "PCI-DSS Level 1"
  encryption: "AES-256-GCM"
  secrets: "HashiCorp Vault"
```

---

## 📡 APIs Principales

### 1. Usage Tracking

```yaml
POST /api/v1/usage:
  auth: "mTLS + JWT s2s (solo NOPS Kernel)"
  payload:
    tenant_id: string
    timestamp: ISO8601
    usage:
      cpu_seconds: float
      memory_gb_hours: float
      storage_gb_hours: float
      network_gb: float
      executions: int
  
  response:
    status: 202
    queued: true
```

### 2. Invoice Generation

```yaml
POST /api/v1/invoices:
  auth: "JWT + RBAC"
  payload:
    tenant_id: string
    period_start: ISO8601
    period_end: ISO8601
    
  response:
    invoice_id: string
    total: decimal
    pdf_url: string
```

### 3. Payment Processing

```yaml
POST /api/v1/payments:
  auth: "JWT + RBAC"
  payload:
    invoice_id: string
    payment_method: "stripe|paypal|wire"
    
  response:
    payment_id: string
    status: "pending|completed|failed"
    transaction_id: string
```

---

## 💰 Pricing Models

```yaml
pricing_tiers:
  🟤_zero:
    model: "Pay-per-execution"
    pricing:
      executions: "$0.001 por ejecución"
      data_egress: "$0.10 por GB"
    
  🟡_shared:
    model: "Pay-as-you-go"
    pricing:
      cpu: "$0.05 por CPU-hora"
      memory: "$0.01 por GB-hora"
      
  🟢_lite:
    model: "Reserved capacity"
    pricing:
      base: "$99/mes"
      overage: "Pay-as-you-go"
      
  🔵_enterprise:
    model: "Enterprise contract"
    pricing:
      custom: "Negotiable"
      minimum: "$5,000/mes"
      
  🔴_airgapped:
    model: "Perpetual license"
    pricing:
      one_time: "$50,000+"
      support: "$10,000/año"
```

---

## 🔗 Cross-References

```yaml
master_prompts_relacionados:
  - "02-architecture-master-prompt.md"
  - "18-security-master-prompt.md"
  - "19-performance-master-prompt.md"
  - "37-observability-master-prompt.md" (usage metrics)
  - "38-scorecard-master-prompt.md" (cost efficiency scoring)"
```

---

*Master Prompt creado: 2025-10-08*  
*Estado: Active - P1 CRÍTICO*

