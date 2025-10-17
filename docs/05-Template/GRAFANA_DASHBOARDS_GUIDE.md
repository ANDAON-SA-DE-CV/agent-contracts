# Guía: Dashboards Grafana por Sprint

**Versión:** 1.0  
**Fecha:** 2025-10-16  
**Contexto:** Plantilla v2.4 Enterprise

---

## 🎯 Objetivo

Documentar claramente **qué sprints necesitan dashboards Grafana** y **cuáles no**, evitando bloat innecesario mientras se garantiza observabilidad operacional.

---

## 📊 Matriz de Decisión por Sprint

| Sprint | Dashboard | Criterios Cumplidos | Justificación |
|--------|-----------|---------------------|---------------|
| **S0 - Bootstrap** | ❌ | 0/4 | Solo setup - no hay métricas runtime aún |
| **S1 - Contratos** | ❌ | 0/4 | Validación estática - no afecta runtime |
| **S2 - Realtime Engine** | ✅✅ | 4/4 | Latencia p95, concurrencia, SLOs críticos |
| **S3 - Batch Processing** | ✅✅ | 4/4 | Throughput, queue depth, async behavior |
| **S4 - Streaming SSE** | ✅✅ | 4/4 | Active clients, backpressure, drops |
| **S5 - Model Management** | ✅ | 3/4 | Swaps, loads, memory, latency por modelo |
| **S6 - Providers** | ✅✅ | 4/4 | Latencia por provider, error rates, multi-provider |
| **S7 - Cache** | ⚠️ | 2/4 | **Opcional** - puede usar métricas de S2/S6 |
| **S8 - Rate Limiting** | ❌ | 1/4 | Alertas simples suficientes - no requiere dashboard |
| **S9 - Observability** | ✅✅✅ | 4/4 | **Sprint maestro** - consolida todos los dashboards |
| **S10 - Performance** | ✅✅ | 4/4 | Benchmarks, L1-L3 cache, pool utilization |
| **S10.5 - Perf Framework** | ✅✅ | 4/4 | Optimización sistemática, comparación A/B |

---

## 🔍 Criterios de Decisión (≥2 para incluir Dashboard)

### 1. ✅ Introduce Métricas Runtime
**¿El sprint genera métricas operacionales en producción?**

- **SÍ**: Latencia, throughput, concurrencia, memoria, CPU
- **NO**: Configuración, contratos estáticos, documentación

**Ejemplos:**
- ✅ S2: `inference_latency_p95`, `concurrent_requests`
- ✅ S4: `sse_active_clients`, `sse_dropped_events`
- ❌ S1: Validación de schemas YAML (no produce métricas runtime)

---

### 2. ✅ Cambia Comportamiento Observable
**¿El sprint modifica cómo se comporta el sistema en producción?**

- **SÍ**: Streaming, batch, async, pooling, caching
- **NO**: Refactoring interno, documentación, tests

**Ejemplos:**
- ✅ S3: Cambia de sync a batch async
- ✅ S4: Agrega streaming SSE (nuevo patrón observable)
- ❌ S8: Rate limiting es transparente al usuario

---

### 3. ✅ Afecta SLOs
**¿El sprint tiene objetivos de performance cuantificables?**

- **SÍ**: p95 < Xms, error rate < Y%, throughput > Z req/s
- **NO**: Funcionalidad correcta sin SLOs específicos

**Ejemplos:**
- ✅ S2: SLO p95 < 200ms
- ✅ S6: SLO error rate < 1% por provider
- ❌ S1: No tiene SLOs de runtime (solo validación)

---

### 4. ✅ Requiere Debug Operacional
**¿Los logs son suficientes para debuggear issues en producción?**

- **SÍ necesita dashboard**: Correlación temporal, percentiles, multi-tenant
- **NO necesita dashboard**: Errores puntuales, trazas lineales

**Ejemplos:**
- ✅ S4: "¿Por qué se están dropeando eventos SSE?" → Necesita correlación entre `queue_size` y `active_clients`
- ✅ S6: "¿Qué provider está fallando?" → Dashboard con breakdown por provider
- ❌ S8: "¿Se está rate-limitando?" → Log simple + alerta basta

---

## 📈 Análisis Detallado por Sprint

### ❌ S0 - Bootstrap
**Criterios:** 0/4

- ❌ **Runtime**: No hay métricas aún
- ❌ **Observable**: Solo estructura de código
- ❌ **SLOs**: No aplica
- ❌ **Debug**: No hay nada que debuggear

**Decisión:** NO incluir dashboard

---

### ❌ S1 - Contratos
**Criterios:** 0/4

- ❌ **Runtime**: Validación estática (CI/test time)
- ❌ **Observable**: No afecta comportamiento en producción
- ❌ **SLOs**: Validación binaria (pasa/falla)
- ❌ **Debug**: Errores claros en tests

**Decisión:** NO incluir dashboard

---

### ✅✅ S2 - Realtime Engine
**Criterios:** 4/4

- ✅ **Runtime**: `inference_latency_ms`, `concurrent_requests`, `queue_depth`
- ✅ **Observable**: Sync request/response con concurrencia
- ✅ **SLOs**: p95 < 200ms, error rate < 0.5%
- ✅ **Debug**: Necesita correlación latencia vs concurrencia

**Métricas clave:**
- `inference_request_latency_ms` (histogram)
- `inference_concurrent_requests` (gauge)
- `inference_queue_depth` (gauge)
- `inference_errors_total` (counter)

**Dashboard:** `deploy/grafana/dashboards/s2-realtime.json`

---

### ✅✅ S3 - Batch Processing
**Criterios:** 4/4

- ✅ **Runtime**: `batch_throughput_rps`, `batch_queue_depth`, `batch_processing_time`
- ✅ **Observable**: Cambia de sync a batch async
- ✅ **SLOs**: Throughput > 1000 req/s, p95 < 500ms
- ✅ **Debug**: Cuellos de botella en queue

**Métricas clave:**
- `batch_requests_total` (counter)
- `batch_queue_depth` (gauge)
- `batch_processing_duration_seconds` (histogram)
- `batch_failed_requests_total` (counter)

**Dashboard:** `deploy/grafana/dashboards/s3-batch.json`

---

### ✅✅ S4 - Streaming SSE
**Criterios:** 4/4

- ✅ **Runtime**: `sse_active_clients`, `sse_queue_size`, `sse_dropped_events`
- ✅ **Observable**: Streaming long-lived connections
- ✅ **SLOs**: Drops < 0.1%, backpressure < 80%
- ✅ **Debug**: Correlación drops vs active_clients vs queue_size

**Métricas clave:**
- `inference_sse_active_clients` (gauge)
- `inference_sse_queue_size` (histogram)
- `inference_sse_dropped_events_total` (counter)
- `inference_sse_event_latency_ms` (histogram)

**Dashboard:** `ops/grafana/dashboards/sse_overview.json` (ya existe en S4)

---

### ✅ S5 - Model Management
**Criterios:** 3/4

- ✅ **Runtime**: `model_swap_total`, `model_load_latency`, `model_memory_bytes`
- ✅ **Observable**: Swaps A/B, warm-up, eviction
- ✅ **SLOs**: Load latency < 2s, swap sin drops
- ❌ **Debug**: Relativamente simple (solo load/unload)

**Métricas clave:**
- `enis_inference_model_swap_total` (counter)
- `enis_inference_model_load_total` (counter)
- `enis_provider_invoke_latency_ms` (histogram) - por modelo
- `enis_inference_model_errors_total` (counter)

**Dashboard:** `docs/observability/s5-model-mgmt-dashboard.json` (ya existe en S5)

---

### ✅✅ S6 - Providers
**Criterios:** 4/4

- ✅ **Runtime**: Latencia y errores **por provider** (OpenAI, Anthropic, Groq, OSS)
- ✅ **Observable**: Multi-provider routing, fallback
- ✅ **SLOs**: p95 por provider, error rate < 1%
- ✅ **Debug**: "¿Qué provider está fallando?" requiere breakdown

**Métricas clave:**
- `provider_requests_total{provider,model}` (counter)
- `provider_errors_total{provider,code}` (counter)
- `provider_latency_seconds{provider,model}` (histogram)
- `tokens_consumed_total{provider,model,tenant}` (counter)

**Dashboard:** `monitoring/grafana/dashboards/s6-providers.json` (mencionado en S6)

---

### ⚠️ S7 - Cache (CONDICIONAL)
**Criterios:** 2/4

- ✅ **Runtime**: `cache_hit_ratio`, `cache_latency_ms`
- ⚠️ **Observable**: Mejora latencia pero es transparente
- ✅ **SLOs**: Hit ratio > 70%, latency reduction > 50%
- ❌ **Debug**: Logs + métricas de S2 pueden bastar

**Decisión:** **OPCIONAL** - Puede usar paneles de S2 agregando:
- `inference_cache_hit_ratio` (gauge)
- `inference_cache_miss_ratio` (gauge)
- `inference_cache_latency_ms` (histogram)

**Alternativa:** Agregar 1-2 paneles al dashboard de S2 en lugar de dashboard completo

---

### ❌ S8 - Rate Limiting
**Criterios:** 1/4

- ✅ **Runtime**: `rate_limit_exceeded_total`
- ❌ **Observable**: Transparente (429 errors)
- ❌ **SLOs**: Binario (permite/rechaza)
- ❌ **Debug**: Log simple + alerta basta

**Decisión:** NO incluir dashboard - alertas simples suficientes

**Métricas recomendadas:**
- `rate_limit_exceeded_total{tenant,tier}` (counter)
- Alerta: `rate(rate_limit_exceeded_total[5m]) > 10`

---

### ✅✅✅ S9 - Observability (CRÍTICO)
**Criterios:** 4/4 + Sprint Maestro

- ✅ **Runtime**: Todas las métricas anteriores
- ✅ **Observable**: Consolida observabilidad completa
- ✅ **SLOs**: SLOs globales del sistema
- ✅ **Debug**: Dashboard unificado + drill-down

**Decisión:** **OBLIGATORIO** - Este sprint:
1. Consolida todos los dashboards de S2-S6
2. Agrega dashboard de overview general
3. Provisiona alertas
4. Configura logging/tracing

**Dashboards:**
- `observability/dashboards/enis-overview.json` (general)
- Upgrade de dashboards S2-S6 con drill-downs
- Dashboard de SLOs

---

### ✅✅ S10 - Performance
**Criterios:** 4/4

- ✅ **Runtime**: Benchmarks, L1-L3 cache, pool utilization
- ✅ **Observable**: Optimizaciones medibles
- ✅ **SLOs**: Mejoras cuantificables (p95, throughput)
- ✅ **Debug**: Comparación before/after

**Métricas clave:**
- Métricas de S2-S6 con optimizaciones
- `l1_cache_hit_ratio`, `l2_cache_hit_ratio`, `l3_cache_hit_ratio`
- `db_pool_utilization`
- `request_budget_cost_usd`

**Dashboard:** Dashboard de performance con comparación temporal

---

### ✅✅ S10.5 - Performance Framework
**Criterios:** 4/4

- ✅ **Runtime**: Framework de benchmarking continuo
- ✅ **Observable**: Optimización sistemática A/B
- ✅ **SLOs**: Targets de mejora por categoría
- ✅ **Debug**: Comparación entre variantes

**Dashboard:** Ya implementado en S10.5 con:
- Variables `tenant`, `tier`
- Thresholds por panel
- Comparación A/B

---

## 🎨 Tipos de Dashboards

### 1. Dashboard de Feature (S2-S6, S10)
**Propósito:** Monitorear funcionalidad específica

**Estructura:**
- 4-6 paneles clave
- Variables: tenant, tier, instance
- Thresholds alineados a SLOs del sprint

**Ejemplos:**
- S2: Realtime Engine (latencia, concurrencia)
- S4: Streaming SSE (clients, drops)
- S6: Providers (latency por provider)

---

### 2. Dashboard de Overview (S9)
**Propósito:** Vista general del sistema

**Estructura:**
- 8-12 paneles consolidados
- Drill-down a dashboards específicos
- SLOs globales
- Alerting guidance

---

### 3. Dashboard de Performance (S10+)
**Propósito:** Comparación temporal y A/B

**Estructura:**
- Métricas before/after
- Comparación de variantes
- Análisis de cuellos de botella
- Cost tracking

---

## 📝 Plantilla: Decisión de Dashboard

Cuando crees un nuevo sprint, usa este checklist:

```markdown
## ¿Incluir Dashboard Grafana?

### Criterios (necesita ≥2 ✅):
- [ ] **Runtime**: ¿Genera métricas operacionales? (latencia, throughput, concurrencia)
- [ ] **Observable**: ¿Cambia comportamiento en producción? (streaming, batch, async)
- [ ] **SLOs**: ¿Tiene objetivos cuantificables? (p95 < Xms, error rate < Y%)
- [ ] **Debug**: ¿Logs no son suficientes? (necesita correlación, percentiles)

### Decisión:
- **✅ SÍ incluir dashboard** (≥2 criterios) → Usar plantilla v2.4 completa
- **❌ NO incluir dashboard** (<2 criterios) → Omitir sección de Grafana
- **⚠️ OPCIONAL** (2 criterios justos) → Evaluar si agregar paneles a dashboard existente

### Alternativas si NO:
- Usar métricas de sprint anterior (ej: S7 usa S2/S6)
- Configurar alertas simples sin dashboard
- Diferir a S9 (Observability sprint)
```

---

## 🚀 Implementación

### Para incluir Dashboard en un sprint:

1. **Usar sección completa de plantilla v2.4:**
   ```markdown
   ## 📊 Dashboard Grafana Provisionado (v2.4)
   
   [Incluir JSON completo con paneles específicos del sprint]
   ```

2. **Definir métricas específicas:**
   - Nomenclatura: `{service}_{feature}_{metric}_total`
   - Labels: `tenant`, `tier`, `model`, etc.
   - Tipos: Counter, Gauge, Histogram, Summary

3. **Configurar thresholds por SLO:**
   ```json
   "thresholds": {
     "steps": [
       { "color": "green", "value": null },
       { "color": "yellow", "value": 800 },  // Warning
       { "color": "red", "value": 1200 }     // Critical
     ]
   }
   ```

4. **Crear ConfigMap K8s:**
   ```yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: grafana-dashboard-s[n]
   data:
     s[n]-dashboard.json: |
       [JSON del dashboard]
   ```

### Para NO incluir Dashboard:

1. **Omitir sección de Grafana de la plantilla**

2. **Documentar alternativa en "Monitoring":**
   ```markdown
   ## 📊 Monitoring
   
   Este sprint NO requiere dashboard dedicado porque [razón].
   
   **Alternativas:**
   - Usar métricas de dashboard S[X]
   - Configurar alertas simples: [ejemplos]
   - Diferir observabilidad detallada a S9
   ```

---

## 📚 Referencias

- **Plantilla v2.4:** `docs/03-Template/SPRINT_TEMPLATE_CLAUDE_CLI.md`
- **Sprint S4 (ejemplo completo):** `docs/01-sprint/S4/S4-engine_streaming_sse.md` (líneas 2592-2613)
- **Sprint S10.5 (performance):** `docs/01-sprint/S10.5/s_10_5_performance_framework_optimizacion_sistematica_v_2.md`
- **Grafana Provisioning:** https://grafana.com/docs/grafana/latest/administration/provisioning/

---

## ✅ Checklist Final

Antes de crear un sprint, confirma:

- [ ] ¿He evaluado los 4 criterios de decisión?
- [ ] ¿He decidido si incluir dashboard o no?
- [ ] Si SÍ: ¿He definido las métricas clave (≥4)?
- [ ] Si SÍ: ¿He configurado thresholds por SLO?
- [ ] Si NO: ¿He documentado alternativa de monitoring?
- [ ] ¿He verificado que otros sprints no cubren ya esto?

---

**Última actualización:** 2025-10-16  
**Versión:** 1.0  
**Mantenedor:** Platform Engineering Team

