# Resource Governance Service

## 🎯 Propósito

El **Resource Governance Service** es el servicio avanzado de ENIS v3.0 para gestión inteligente de recursos, fairness multi-tenant y optimización de costos.

## 📊 Características Principales

- ⚖️ **Fairness Algorithms** - Weighted Fair Queueing + Max-Min Fairness
- 🚦 **Advanced Throttling** - Adaptive throttling basado en ML
- 💰 **Cost Optimization** - Linear Programming para minimizar costos
- 📈 **Forecasting** - Prophet + LSTM para predicción de costos
- 🔍 **Noisy Neighbor Detection** - Isolation Forest (ML)

## 🏗️ Arquitectura

```yaml
stack_tecnologico:
  backend: "FastAPI (Python 3.11+)"
  cache: "Redis"
  database: "PostgreSQL + TimescaleDB"
  ml_frameworks: "scikit-learn, Prophet, scipy"
  
componentes:
  - "Quota Manager"
  - "Fairness Engine"
  - "Cost Optimizer"
  - "Resource Forecaster"
  - "Noisy Neighbor Detector"
```

## 🔗 Integración

### Con NOPS Kernel
- **Tipo:** Extiende Policy Engine básico del kernel
- **Comunicación:** mTLS + JWT s2s
- **Degraded Mode:** Kernel usa quotas estáticas si servicio no disponible

### Con Billing Service
- **Tipo:** Consume usage data para cost optimization
- **Comunicación:** API bidireccional

## 📋 Master Prompts

- **43-resource-governance-master-prompt.md** - Master prompt principal (~1,400 líneas)
- **02-architecture-master-prompt.md** - Arquitectura general
- **18-security-master-prompt.md** - Seguridad
- **19-performance-master-prompt.md** - Performance

## 🚀 Sprint

- **Sprint:** S23-S24 (Q2 2025)
- **Prioridad:** P2
- **Blocker for:** Multi-tenant fairness optimization

## 📊 Métricas de Éxito

- **Fairness Index:** > 0.90 (Jain's Fairness Index)
- **Cost Savings:** > 20% vs baseline on-demand
- **Forecast Accuracy:** MAE < 15%
- **Throttle Decision:** < 50ms p95

---

*Creado: 2025-10-09*  
*Estado: Ready for Sprint S23-S24*  
*Módulo #5 de los 7 Módulos NOPS*

