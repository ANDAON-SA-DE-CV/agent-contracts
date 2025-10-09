# 43 - Resource Governance Service Master Prompt

---
prompt_id: "43-resource-governance-master-prompt"
prompt_type: "master_prompt"
service_name: "resource-governance-service"
dna_version: "3.0"
semver: "1.0.0"
date: "2025-10-09"
author: "@andaon"
domain: "Resource Management & Fairness"
description: "Master prompt para Resource Governance Service - Quotas, fairness algorithms y cost optimization"
estimated_pages: "140-160"
compliance_status: "DNA_v3_compliant"
dependencies: ["00-dna-proyecto-prompt.md", "07-nops-master-prompt.md", "39-billing-master-prompt.md"]
generates:
 - "architecture/resource-governance/*"
 - "reference/governance-api/*"
 - "ml-models/fairness/*"
 - "cost-optimization/*"
child_prompts: 16
validation_script: "validate-governance-documentation.js"
release_status: "ready_for_sprint_s23"
feeds_to: ["07-nops-kernel", "39-billing-service"]
priority: "P2"
sprint: "S23-S24 (Q2 2025)"
---

## 🎯 PROPÓSITO Y CONTEXTO

**ROL:** Arquitecto Senior de Resource Management & Platform Engineering en ENIS v3.0

**TAREA:** Generar documentación completa del Resource Governance Service - servicio avanzado para quotas multi-tenant, fairness algorithms, cost optimization y resource forecasting.

**OBJETIVO:** Producir 140-160 páginas de documentación técnica que cubra arquitectura, fairness algorithms (ML-based), multi-tenant optimization, cost analytics, APIs y deployment patterns.

**CONTEXTO CRÍTICO:**
- El Resource Governance Service es **FAIRNESS-CRITICAL** - garantiza equidad entre tenants
- Nivel básico **YA EXISTE** en NOPS Kernel (Policy Engine con rate limits)
- Nivel avanzado **Q2 2025**: ML fairness, multi-tenant optimization, forecasting
- Integración estrecha con Billing Service (cost optimization)
- Previene "noisy neighbor" problem en ambientes multi-tenant
- Forecasting de resource needs (capacity planning)

# 📑 TABLA DE CONTENIDOS

- 🏗️ Arquitectura del Resource Governance Service
- ⚖️ Fairness Algorithms (ML-Based)
- 📊 Multi-Tenant Resource Optimization
- 💰 Cost Optimization & Forecasting
- 🚦 Advanced Throttling & Quotas
- 🔧 APIs y SDKs
- 🔗 Integración con NOPS Kernel
- 🚀 Deployment Patterns
- 📁 Estructura de Documentación

## 🏗️ ARQUITECTURA DEL RESOURCE GOVERNANCE SERVICE

### **Principios Arquitectónicos Fundamentales**

El Resource Governance Service de ENIS v3.0 se basa en cinco principios clave:

- **Fairness First**: Distribución equitativa de recursos entre tenants
- **ML-Driven Optimization**: Algoritmos inteligentes de asignación
- **Cost Aware**: Optimización considerando costos reales
- **Predictive Planning**: Forecasting de necesidades futuras
- **Graceful Degradation**: Throttling progresivo (no kill)

### **Componentes Core del Sistema**

```yaml
governance_architecture:
  quota_manager:
    description: "Gestor de quotas multi-dimensional"
    technology: "Python + Redis + PostgreSQL"
    features:
      - "Quotas por tenant/tier/vertical"
      - "Multi-dimensional limits (CPU, memory, storage, API calls)"
      - "Soft limits (warning) vs Hard limits (block)"
      - "Temporal quotas (burst allowance)"
      - "Hierarchical quotas (organization → team → user)"
      
    quota_dimensions:
      compute:
        - "cpu_cores_limit"
        - "memory_gb_limit"
        - "gpu_hours_limit"
        
      api:
        - "requests_per_minute"
        - "requests_per_day"
        - "concurrent_requests"
        
      storage:
        - "total_storage_gb"
        - "hot_storage_gb"
        - "objects_count"
        
      executions:
        - "agent_executions_per_hour"
        - "agent_executions_per_day"
        - "concurrent_executions"
        
  fairness_engine:
    description: "Motor de fairness ML-driven"
    technology: "Python + scikit-learn + OR-Tools"
    algorithms:
      weighted_fair_queueing:
        description: "WFQ adaptado para cloud resources"
        weights_by_tier:
          🟤_zero: 1
          🟡_shared: 5
          🟢_lite: 10
          🔵_enterprise: 50
          
      max_min_fairness:
        description: "Garantiza mínimo resource para todos"
        min_guaranteed:
          🟤_zero: "10% shared pool"
          🟡_shared: "20% shared pool"
          🟢_lite: "dedicated slice"
          🔵_enterprise: "dedicated nodes"
          
      proportional_share:
        description: "Recursos proporcionales a tier + historial"
        factors:
          - "tier_level (40%)"
          - "payment_history (30%)"
          - "resource_efficiency (20%)"
          - "time_of_day (10%)"
          
  cost_optimizer:
    description: "Optimizador de costos en tiempo real"
    technology: "Python + Linear Programming + ML forecasting"
    features:
      - "Spot instance optimization"
      - "Auto-scaling basado en costo"
      - "Resource right-sizing recommendations"
      - "Cost anomaly detection"
      - "Budget alerts & forecasting"
      
    optimization_strategies:
      spot_instances:
        savings: "60-80% vs on-demand"
        risk_mitigation: "Fallback automático a on-demand"
        
      reserved_capacity:
        commitment: "1-3 años"
        discount: "30-50%"
        applicable_tiers: ["🔵 Enterprise"]
        
      auto_scaling:
        scale_down_aggressive: "Off-peak hours"
        scale_up_predictive: "ML forecasting"
        
  resource_forecaster:
    description: "Predictor ML de necesidades futuras"
    technology: "Python + Prophet + LSTM"
    models:
      resource_demand:
        type: "Facebook Prophet (time-series)"
        target: "cpu_demand_next_7d"
        features:
          - "historical_usage (90d)"
          - "seasonal_patterns"
          - "trend_component"
          - "holiday_effects"
        accuracy: "MAE < 15%"
        
      cost_forecast:
        type: "LSTM Neural Network"
        target: "monthly_cost_next_3m"
        features:
          - "usage_patterns"
          - "pricing_trends"
          - "growth_rate"
        accuracy: "MAPE < 10%"
```

---

## ⚖️ FAIRNESS ALGORITHMS (ML-BASED)

### **Weighted Fair Queueing (WFQ)**

```python
# resource_governance/fairness/wfq.py
from typing import Dict, List, Any
from collections import defaultdict
import heapq
from dataclasses import dataclass
import time

@dataclass
class TenantRequest:
    tenant_id: str
    tier: str
    request_id: str
    resource_cost: float  # CPU-seconds equivalente
    priority: int
    timestamp: float
    
class WeightedFairQueueing:
    """
    Weighted Fair Queueing para asignación justa de recursos
    
    Garantiza que tenants de tier superior obtienen más recursos,
    pero TODOS los tiers obtienen servicio (no starvation)
    """
    
    TIER_WEIGHTS = {
        "🟤": 1,
        "🟡": 5,
        "🟢": 10,
        "🔵": 50,
        "🔴": 100  # Máxima prioridad
    }
    
    def __init__(self):
        self.queues = defaultdict(list)  # tier → [requests]
        self.virtual_time = defaultdict(float)  # tier → virtual_time
        
    def enqueue_request(self, request: TenantRequest):
        """Agrega request a la cola correspondiente"""
        tier = request.tier
        
        # Calcular virtual finish time
        weight = self.TIER_WEIGHTS[tier]
        virtual_start = max(self.virtual_time[tier], time.time())
        virtual_finish = virtual_start + (request.resource_cost / weight)
        
        # Agregar a heap (priority queue) ordenado por virtual_finish
        heapq.heappush(
            self.queues[tier],
            (virtual_finish, request)
        )
        
        self.virtual_time[tier] = virtual_finish
    
    def dequeue_next_request(self) -> TenantRequest:
        """
        Obtiene siguiente request a ejecutar (fairness)
        
        Selecciona el request con menor virtual_finish_time
        entre todas las colas
        """
        min_virtual_finish = float('inf')
        selected_tier = None
        
        # Encontrar tier con menor virtual_finish_time
        for tier, queue in self.queues.items():
            if queue:
                virtual_finish, _ = queue[0]
                if virtual_finish < min_virtual_finish:
                    min_virtual_finish = virtual_finish
                    selected_tier = tier
        
        if selected_tier is None:
            return None  # No hay requests
        
        # Dequeue del tier seleccionado
        virtual_finish, request = heapq.heappop(self.queues[selected_tier])
        
        return request
    
    def get_queue_depth(self, tier: str) -> int:
        """Obtiene número de requests en cola para un tier"""
        return len(self.queues.get(tier, []))
```

---

### **Max-Min Fairness**

```python
# resource_governance/fairness/max_min.py
from typing import Dict, List
import numpy as np
from scipy.optimize import linprog

class MaxMinFairness:
    """
    Max-Min Fairness Allocator
    
    Garantiza:
    1. Todos los tenants reciben su mínimo garantizado
    2. Recursos sobrantes se distribuyen equitativamente
    3. Ningún tenant puede monopolizar recursos
    """
    
    MINIMUM_GUARANTEES = {
        "🟤": 0.05,  # 5% del pool compartido
        "🟡": 0.10,  # 10% del pool compartido
        "🟢": 0.20,  # 20% del pool (dedicated slice)
        "🔵": 1.00,  # Dedicated nodes (fuera del pool)
        "🔴": 1.00   # Dedicated air-gapped
    }
    
    def allocate_resources(
        self,
        total_capacity: float,
        demands: Dict[str, float],  # tenant_id → demand
        tenant_tiers: Dict[str, str]  # tenant_id → tier
    ) -> Dict[str, float]:
        """
        Calcula asignación óptima de recursos
        
        Returns:
            tenant_id → allocated_resources
        """
        # 1. Garantizar mínimos
        allocations = {}
        remaining_capacity = total_capacity
        
        for tenant_id, tier in tenant_tiers.items():
            if tier in ["🔵", "🔴"]:
                # Dedicated - no compete en pool compartido
                allocations[tenant_id] = demands[tenant_id]
            else:
                # Shared pool - garantizar mínimo
                min_guarantee = total_capacity * self.MINIMUM_GUARANTEES[tier]
                allocations[tenant_id] = min_guarantee
                remaining_capacity -= min_guarantee
        
        # 2. Distribuir excedente equitativamente
        shared_tenants = [
            t for t, tier in tenant_tiers.items() 
            if tier not in ["🔵", "🔴"]
        ]
        
        if remaining_capacity > 0 and shared_tenants:
            # Calcular demandas insatisfechas
            unsatisfied_demands = {
                t: max(0, demands[t] - allocations[t])
                for t in shared_tenants
            }
            
            # Algoritmo max-min fairness iterativo
            while remaining_capacity > 0 and any(unsatisfied_demands.values()):
                # Fair share = remaining / número de tenants con demanda
                active_tenants = [
                    t for t, d in unsatisfied_demands.items() if d > 0
                ]
                
                if not active_tenants:
                    break
                
                fair_share = remaining_capacity / len(active_tenants)
                
                # Asignar fair_share o demanda (lo que sea menor)
                allocated_this_round = 0
                satisfied_tenants = []
                
                for tenant_id in active_tenants:
                    allocation = min(fair_share, unsatisfied_demands[tenant_id])
                    allocations[tenant_id] += allocation
                    unsatisfied_demands[tenant_id] -= allocation
                    allocated_this_round += allocation
                    
                    if unsatisfied_demands[tenant_id] == 0:
                        satisfied_tenants.append(tenant_id)
                
                remaining_capacity -= allocated_this_round
                
                # Remover tenants satisfechos
                for t in satisfied_tenants:
                    del unsatisfied_demands[t]
        
        return allocations
```

---

## 📊 MULTI-TENANT RESOURCE OPTIMIZATION

### **Noisy Neighbor Detection**

```python
# resource_governance/optimization/noisy_neighbor.py
from typing import Dict, List, Any, Tuple
import pandas as pd
from sklearn.ensemble import IsolationForest
import structlog

logger = structlog.get_logger()

class NoisyNeighborDetector:
    """
    Detector de "noisy neighbors" (tenants que abusan de recursos)
    
    Usa ML (Isolation Forest) para detectar patrones anómalos
    """
    
    def __init__(self, contamination: float = 0.05):
        self.model = IsolationForest(
            contamination=contamination,  # 5% esperado como anomalías
            random_state=42
        )
        self.logger = logger.bind(component="noisy_neighbor")
        
    async def detect_noisy_neighbors(
        self,
        resource_usage: pd.DataFrame,
        window_minutes: int = 60
    ) -> List[Dict[str, Any]]:
        """
        Detecta tenants con uso anómalo de recursos
        
        Args:
            resource_usage: DataFrame con columnas:
                - tenant_id
                - cpu_usage
                - memory_usage
                - network_bandwidth
                - api_requests
                - timestamp
            window_minutes: Ventana de análisis
            
        Returns:
            Lista de tenants con comportamiento anómalo
        """
        # 1. Filtrar últimos N minutos
        cutoff_time = pd.Timestamp.now() - pd.Timedelta(minutes=window_minutes)
        recent_usage = resource_usage[resource_usage['timestamp'] >= cutoff_time]
        
        if len(recent_usage) == 0:
            return []
        
        # 2. Agregar por tenant
        tenant_aggregated = recent_usage.groupby('tenant_id').agg({
            'cpu_usage': ['mean', 'max', 'std'],
            'memory_usage': ['mean', 'max', 'std'],
            'network_bandwidth': ['mean', 'max'],
            'api_requests': 'sum'
        }).reset_index()
        
        # 3. Flatten multi-level columns
        tenant_aggregated.columns = [
            '_'.join(col).strip('_') if col[1] else col[0] 
            for col in tenant_aggregated.columns.values
        ]
        
        # 4. Preparar features para ML
        features = tenant_aggregated[[
            'cpu_usage_mean', 'cpu_usage_max', 'cpu_usage_std',
            'memory_usage_mean', 'memory_usage_max', 'memory_usage_std',
            'network_bandwidth_mean', 'network_bandwidth_max',
            'api_requests_sum'
        ]].fillna(0)
        
        # 5. Detectar anomalías
        predictions = self.model.fit_predict(features)
        anomaly_scores = self.model.score_samples(features)
        
        # 6. Identificar noisy neighbors (prediction = -1)
        noisy_neighbors = []
        
        for idx, pred in enumerate(predictions):
            if pred == -1:
                tenant_id = tenant_aggregated.iloc[idx]['tenant_id']
                
                anomaly = {
                    "tenant_id": tenant_id,
                    "anomaly_score": float(anomaly_scores[idx]),
                    "metrics": {
                        "cpu_mean": float(tenant_aggregated.iloc[idx]['cpu_usage_mean']),
                        "cpu_max": float(tenant_aggregated.iloc[idx]['cpu_usage_max']),
                        "memory_mean": float(tenant_aggregated.iloc[idx]['memory_usage_mean']),
                        "api_requests": int(tenant_aggregated.iloc[idx]['api_requests_sum'])
                    },
                    "detected_at": pd.Timestamp.now().isoformat()
                }
                
                noisy_neighbors.append(anomaly)
                
                self.logger.warning(
                    "noisy_neighbor_detected",
                    tenant_id=tenant_id,
                    anomaly_score=anomaly["anomaly_score"]
                )
        
        return noisy_neighbors
    
    async def apply_throttling(
        self,
        tenant_id: str,
        severity: str = "moderate"  # low, moderate, severe
    ):
        """
        Aplica throttling gradual a noisy neighbor
        
        Niveles:
        - low: -10% resources
        - moderate: -30% resources
        - severe: -50% resources (nunca 100% - siempre mínimo garantizado)
        """
        throttling_levels = {
            "low": 0.90,
            "moderate": 0.70,
            "severe": 0.50
        }
        
        multiplier = throttling_levels[severity]
        
        # Actualizar quotas en Redis
        await self._update_tenant_quotas(tenant_id, multiplier)
        
        # Log en Compliance Service
        await self._log_throttling_action(tenant_id, severity, multiplier)
        
        # Notificar al tenant
        await self._notify_tenant_throttled(tenant_id, severity)
```

---

## 💰 COST OPTIMIZATION & FORECASTING

### **Cost Optimizer**

```python
# resource_governance/cost/optimizer.py
from typing import Dict, List, Any
import pandas as pd
from scipy.optimize import linprog
import structlog

logger = structlog.get_logger()

class CostOptimizer:
    """
    Optimizador de costos basado en Linear Programming
    
    Minimiza costo total sujeto a:
    - SLA requirements (latency, availability)
    - Resource constraints
    - Tenant quotas
    """
    
    # Pricing (ejemplo - AWS us-east-1)
    PRICING = {
        "on_demand_cpu": 0.05,  # $/vCPU-hour
        "spot_cpu": 0.015,      # $/vCPU-hour (70% discount)
        "reserved_cpu": 0.035,  # $/vCPU-hour (30% discount)
        "on_demand_memory": 0.005,  # $/GB-hour
        "spot_memory": 0.0015,
        "reserved_memory": 0.0035
    }
    
    def __init__(self):
        self.logger = logger.bind(component="cost_optimizer")
        
    async def optimize_allocation(
        self,
        demand: Dict[str, float],  # tenant_id → cpu_hours_needed
        budget_constraint: float,   # Max $/hour
        sla_requirements: Dict[str, float]  # tenant_id → availability_sla
    ) -> Dict[str, Any]:
        """
        Optimiza asignación de recursos minimizando costo
        
        Formula:
            Minimize: total_cost
            Subject to:
                - demand satisfied
                - SLA requirements met
                - budget constraint
                
        Returns:
            Optimal allocation plan
        """
        # 1. Variables de decisión
        # x[i][j] = recursos de tipo j asignados a tenant i
        # j: 0=on-demand, 1=spot, 2=reserved
        
        num_tenants = len(demand)
        num_types = 3  # on-demand, spot, reserved
        
        # 2. Función objetivo (minimizar costo)
        c = []
        for tenant_id in demand.keys():
            c.extend([
                self.PRICING["on_demand_cpu"],
                self.PRICING["spot_cpu"],
                self.PRICING["reserved_cpu"]
            ])
        
        # 3. Constraints
        
        # Constraint 1: Satisfacer demanda de cada tenant
        A_eq = []
        b_eq = []
        
        for i, (tenant_id, cpu_needed) in enumerate(demand.items()):
            row = [0] * (num_tenants * num_types)
            row[i*num_types:(i+1)*num_types] = [1, 1, 1]  # Sum all types
            A_eq.append(row)
            b_eq.append(cpu_needed)
        
        # Constraint 2: Budget total
        A_ub = [c]  # Costo total
        b_ub = [budget_constraint]
        
        # Constraint 3: SLA requirements (availability)
        # Spot instances tienen menor availability → limitar para high-SLA tenants
        for i, (tenant_id, sla) in enumerate(sla_requirements.items()):
            if sla > 0.999:  # High SLA - limitar spot
                row = [0] * (num_tenants * num_types)
                row[i*num_types + 1] = 1  # Spot column
                A_ub.append(row)
                # Max 20% spot para high-SLA
                b_ub.append(demand[tenant_id] * 0.20)
        
        # 4. Resolver Linear Programming
        result = linprog(
            c=c,
            A_eq=A_eq,
            b_eq=b_eq,
            A_ub=A_ub,
            b_ub=b_ub,
            bounds=(0, None),  # No negative allocations
            method='highs'
        )
        
        if not result.success:
            self.logger.error("optimization_failed", message=result.message)
            return await self._fallback_allocation(demand)
        
        # 5. Parse resultados
        allocations = {}
        x = result.x
        
        for i, tenant_id in enumerate(demand.keys()):
            allocations[tenant_id] = {
                "on_demand": x[i*num_types + 0],
                "spot": x[i*num_types + 1],
                "reserved": x[i*num_types + 2],
                "total": sum(x[i*num_types:(i+1)*num_types]),
                "estimated_cost": sum(
                    x[i*num_types + j] * c[i*num_types + j]
                    for j in range(num_types)
                )
            }
        
        total_cost = result.fun
        
        self.logger.info(
            "cost_optimization_completed",
            total_cost=total_cost,
            budget_constraint=budget_constraint,
            savings=budget_constraint - total_cost
        )
        
        return {
            "allocations": allocations,
            "total_cost": total_cost,
            "budget_used_percentage": (total_cost / budget_constraint) * 100,
            "optimization_status": "success"
        }
```

---

## 🚦 ADVANCED THROTTLING & QUOTAS

### **Adaptive Throttling**

```python
# resource_governance/throttling/adaptive.py
from typing import Dict, Any
import asyncio
from datetime import datetime, timedelta
import structlog

logger = structlog.get_logger()

class AdaptiveThrottler:
    """
    Throttling adaptativo basado en métricas en tiempo real
    
    Ajusta throttling dinámicamente según:
    - System load
    - Tenant behavior
    - Time of day
    - Cost constraints
    """
    
    def __init__(self, redis_client):
        self.redis = redis_client
        self.logger = logger.bind(component="adaptive_throttler")
        
    async def calculate_throttle_rate(
        self,
        tenant_id: str,
        tier: str,
        current_metrics: Dict[str, float]
    ) -> float:
        """
        Calcula rate de throttling adaptativo
        
        Returns:
            Multiplier (0.0-1.0)
            - 1.0 = sin throttling
            - 0.5 = 50% throttled
            - 0.0 = completamente bloqueado (nunca - mínimo 0.1)
        """
        # 1. Obtener baseline del tenant
        baseline = await self._get_tenant_baseline(tenant_id)
        
        # 2. Factores de throttling
        factors = {}
        
        # Factor 1: System load (0.7-1.0)
        system_load = await self._get_system_load()
        factors["system_load"] = self._calculate_load_factor(system_load)
        
        # Factor 2: Tenant behavior (0.5-1.0)
        behavior_score = await self._calculate_behavior_score(
            tenant_id,
            current_metrics,
            baseline
        )
        factors["behavior"] = behavior_score
        
        # Factor 3: Cost constraints (0.8-1.0)
        cost_factor = await self._calculate_cost_factor(tenant_id)
        factors["cost"] = cost_factor
        
        # Factor 4: Time of day (0.9-1.0)
        tod_factor = self._calculate_time_of_day_factor()
        factors["time_of_day"] = tod_factor
        
        # 3. Calcular throttle rate combinado
        throttle_rate = (
            factors["system_load"] * 0.40 +
            factors["behavior"] * 0.30 +
            factors["cost"] * 0.20 +
            factors["time_of_day"] * 0.10
        )
        
        # 4. Aplicar mínimo garantizado según tier
        min_guarantees = {
            "🟤": 0.10,  # 10% mínimo
            "🟡": 0.20,
            "🟢": 0.30,
            "🔵": 0.70,
            "🔴": 0.90
        }
        
        throttle_rate = max(throttle_rate, min_guarantees.get(tier, 0.10))
        
        self.logger.info(
            "throttle_rate_calculated",
            tenant_id=tenant_id,
            tier=tier,
            throttle_rate=throttle_rate,
            factors=factors
        )
        
        return throttle_rate
    
    def _calculate_load_factor(self, system_load: float) -> float:
        """
        Calcula factor según carga del sistema
        
        - Load < 50%: factor = 1.0 (sin throttling)
        - Load 50-80%: factor decrece linealmente 1.0 → 0.8
        - Load > 80%: factor = 0.7 (throttling agresivo)
        """
        if system_load < 0.50:
            return 1.0
        elif system_load < 0.80:
            # Linear interpolation
            return 1.0 - (system_load - 0.50) / 0.30 * 0.20
        else:
            return 0.70
    
    async def _calculate_behavior_score(
        self,
        tenant_id: str,
        current_metrics: Dict[str, float],
        baseline: Dict[str, float]
    ) -> float:
        """
        Calcula score de comportamiento
        
        Penaliza:
        - Spikes súbitos de uso
        - Patrones abusivos
        - Violaciones previas de quotas
        """
        # Comparar con baseline
        cpu_ratio = current_metrics["cpu_usage"] / baseline["cpu_usage"] if baseline["cpu_usage"] > 0 else 1.0
        memory_ratio = current_metrics["memory_usage"] / baseline["memory_usage"] if baseline["memory_usage"] > 0 else 1.0
        
        # Penalizar spikes > 3x baseline
        if cpu_ratio > 3.0 or memory_ratio > 3.0:
            return 0.50  # Throttle agresivo
        elif cpu_ratio > 2.0 or memory_ratio > 2.0:
            return 0.70  # Throttle moderado
        else:
            return 1.0   # Sin throttling
```

---

## 💰 COST FORECASTING

### **Prophet-Based Forecaster**

```python
# resource_governance/forecasting/cost_forecaster.py
from typing import Dict, Any
import pandas as pd
from prophet import Prophet
import structlog

logger = structlog.get_logger()

class CostForecaster:
    """
    Forecaster de costos usando Facebook Prophet
    
    Predice costos futuros basado en:
    - Tendencias históricas
    - Estacionalidad (día de semana, hora del día)
    - Eventos especiales
    - Crecimiento de tenants
    """
    
    def __init__(self):
        self.model = None
        self.logger = logger.bind(component="cost_forecaster")
        
    async def forecast_monthly_cost(
        self,
        historical_costs: pd.DataFrame,
        months_ahead: int = 3
    ) -> Dict[str, Any]:
        """
        Forecast de costos mensuales
        
        Args:
            historical_costs: DataFrame con columnas:
                - date (datetime)
                - cost (float)
            months_ahead: Número de meses a predecir
            
        Returns:
            {
                "forecast": [predicted costs],
                "lower_bound": [confidence interval lower],
                "upper_bound": [confidence interval upper],
                "trend": "increasing|stable|decreasing"
            }
        """
        # 1. Preparar datos para Prophet
        df_prophet = historical_costs.rename(columns={
            "date": "ds",
            "cost": "y"
        })
        
        # 2. Train model
        model = Prophet(
            daily_seasonality=True,
            weekly_seasonality=True,
            yearly_seasonality=True,
            changepoint_prior_scale=0.05  # Sensibilidad a cambios
        )
        
        model.fit(df_prophet)
        
        # 3. Generate future dates (monthly)
        future_dates = pd.date_range(
            start=df_prophet['ds'].max() + pd.Timedelta(days=1),
            periods=months_ahead * 30,
            freq='D'
        )
        
        future_df = pd.DataFrame({'ds': future_dates})
        
        # 4. Predict
        forecast = model.predict(future_df)
        
        # 5. Aggregate by month
        forecast['month'] = forecast['ds'].dt.to_period('M')
        monthly_forecast = forecast.groupby('month').agg({
            'yhat': 'sum',
            'yhat_lower': 'sum',
            'yhat_upper': 'sum'
        }).reset_index()
        
        # 6. Calculate trend
        trend = "stable"
        if len(monthly_forecast) >= 2:
            first_month = monthly_forecast.iloc[0]['yhat']
            last_month = monthly_forecast.iloc[-1]['yhat']
            change_pct = ((last_month - first_month) / first_month) * 100
            
            if change_pct > 10:
                trend = "increasing"
            elif change_pct < -10:
                trend = "decreasing"
        
        return {
            "forecast": monthly_forecast['yhat'].tolist(),
            "lower_bound": monthly_forecast['yhat_lower'].tolist(),
            "upper_bound": monthly_forecast['yhat_upper'].tolist(),
            "trend": trend,
            "change_percentage": change_pct if len(monthly_forecast) >= 2 else 0,
            "forecasted_at": datetime.utcnow().isoformat()
        }
    
    async def recommend_reserved_capacity(
        self,
        usage_history: pd.DataFrame,
        discount_rate: float = 0.30
    ) -> Dict[str, Any]:
        """
        Recomienda compra de reserved capacity
        
        Calcula ROI de comprar capacidad reservada vs on-demand
        """
        # 1. Calcular baseline usage (percentile 50)
        baseline_cpu = usage_history['cpu_usage'].quantile(0.50)
        baseline_memory = usage_history['memory_usage'].quantile(0.50)
        
        # 2. Calcular costo on-demand actual
        hours_per_month = 730
        
        cost_on_demand = (
            baseline_cpu * hours_per_month * self.PRICING["on_demand_cpu"] +
            baseline_memory * hours_per_month * self.PRICING["on_demand_memory"]
        )
        
        # 3. Calcular costo con reserved capacity
        cost_reserved = (
            baseline_cpu * hours_per_month * self.PRICING["reserved_cpu"] +
            baseline_memory * hours_per_month * self.PRICING["reserved_memory"]
        )
        
        # 4. Savings
        monthly_savings = cost_on_demand - cost_reserved
        annual_savings = monthly_savings * 12
        
        # 5. Recommendation
        if monthly_savings > 100:  # > $100/month savings
            recommendation = "strongly_recommend"
        elif monthly_savings > 50:
            recommendation = "recommend"
        else:
            recommendation = "not_worth_it"
        
        return {
            "baseline_cpu_cores": baseline_cpu,
            "baseline_memory_gb": baseline_memory,
            "cost_on_demand_monthly": cost_on_demand,
            "cost_reserved_monthly": cost_reserved,
            "monthly_savings": monthly_savings,
            "annual_savings": annual_savings,
            "roi_months": 12,  # Reserved capacity es 1 año commitment
            "recommendation": recommendation
        }
```

---

## 🔧 APIS Y SDKS

### **Core API Endpoints**

```yaml
governance_api:
  GET /api/v1/quotas/{tenant_id}:
    description: "Get current quotas and usage"
    auth: "JWT user or mTLS s2s"
    response:
      quotas:
        cpu_cores_limit: 100
        current_cpu_usage: 45
        memory_gb_limit: 200
        current_memory_usage: 120
        
  POST /api/v1/quotas/{tenant_id}:
    description: "Update tenant quotas"
    auth: "Admin JWT"
    request:
      cpu_cores_limit: 200
      memory_gb_limit: 400
      
  GET /api/v1/fairness/noisy-neighbors:
    description: "Detect noisy neighbors"
    auth: "mTLS s2s (ops team)"
    response:
      noisy_neighbors: "[array of tenants]"
      
  POST /api/v1/cost/forecast:
    description: "Forecast future costs"
    auth: "JWT user"
    request:
      months_ahead: 3
    response:
      forecast: "[monthly costs]"
      trend: "increasing|stable|decreasing"
```

---

## 🔗 INTEGRACIÓN CON NOPS KERNEL

### **Policy Engine Integration**

El Resource Governance Service **extiende** el Policy Engine básico del NOPS Kernel:

```yaml
integration_model:
  nops_kernel_policy_engine:
    nivel: "Básico (built-in)"
    responsabilidades:
      - "Rate limiting simple por tier"
      - "Quotas estáticas (configuradas en deployment)"
      - "Enforcement inmediato (allow/deny)"
      
  resource_governance_service:
    nivel: "Avanzado (cloud-core)"
    responsabilidades:
      - "ML-based fairness"
      - "Dynamic quota adjustment"
      - "Cost optimization"
      - "Forecasting"
      - "Noisy neighbor detection"
      
  comunicacion:
    direccion: "NOPS Kernel → Resource Governance Service"
    frecuencia: "On-demand (cuando necesita ajustar quotas)"
    protocolo: "mTLS + JWT s2s"
    
    ejemplo_flujo:
      1: "NOPS detecta tenant excediendo quota"
      2: "Query a Governance Service: ¿aplicar throttling?"
      3: "Governance analiza fairness + cost"
      4: "Responde con nueva quota ajustada"
      5: "NOPS aplica nueva quota localmente"
```

---

## 🚀 DEPLOYMENT PATTERNS

```yaml
# kubernetes/resource-governance-service/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: resource-governance-service
  namespace: enis-cloud-core
spec:
  replicas: 2
  template:
    spec:
      containers:
        - name: governance-service
          image: enis/resource-governance-service:1.0.0
          
          env:
            - name: BILLING_SERVICE_URL
              value: "http://billing-service:8080"
              
            - name: REDIS_URL
              value: "redis://redis-cluster:6379"
              
          resources:
            requests:
              cpu: "1000m"
              memory: "2Gi"
            limits:
              cpu: "2000m"
              memory: "4Gi"
```

---

## 📁 ESTRUCTURA DE DOCUMENTACIÓN

```yaml
documentation_structure:
  resource_governance_service/:
    - "README.md"
    - "43-resource-governance-master-prompt.md"
    - "FAIRNESS_ALGORITHMS.md"
    - "COST_OPTIMIZATION.md"
    
  ml-models/:
    - "noisy-neighbor-detector.pkl"
    - "cost-forecaster.pkl"
    
  algorithms/:
    - "weighted-fair-queueing.py"
    - "max-min-fairness.py"
    - "adaptive-throttling.py"
```

---

## ✅ VALIDACIÓN Y QUALITY GATES

```yaml
validation_criteria:
  fairness:
    - "Todos los tenants reciben mínimo garantizado"
    - "No starvation (ningún tenant bloqueado indefinidamente)"
    - "Proportional share funcional"
    
  cost_optimization:
    - "Savings > 20% vs baseline on-demand"
    - "SLA requirements cumplidos"
    - "Forecast accuracy MAE < 15%"
    
  performance:
    - "Throttle decision < 50ms p95"
    - "Quota check < 10ms p95"
    - "Fairness calculation < 100ms p95"
```

---

## 🎯 INSTRUCCIONES DE GENERACIÓN

1. **Scaffold Service** - FastAPI + Redis + scikit-learn
2. **Fairness Engine** - WFQ + Max-Min algorithms
3. **Cost Optimizer** - Linear Programming (scipy)
4. **Forecasting** - Prophet + LSTM models
5. **Noisy Neighbor Detection** - Isolation Forest
6. **Testing** - Unit + Integration + Fairness simulation
7. **Deployment** - Kubernetes + Helm

---

## 📋 METADATA DE CIERRE

```yaml
service_summary:
  nombre: "Resource Governance Service"
  proposito: "Advanced fairness, cost optimization, forecasting"
  prioridad: "P2"
  sprint: "S23-S24 (Q2 2025)"
  
  componentes_principales:
    - "Quota Manager (multi-dimensional)"
    - "Fairness Engine (WFQ + Max-Min)"
    - "Cost Optimizer (Linear Programming)"
    - "Noisy Neighbor Detector (ML)"
    - "Resource Forecaster (Prophet)"
    
  algoritmos_ml:
    - "Weighted Fair Queueing"
    - "Max-Min Fairness"
    - "Isolation Forest (anomaly detection)"
    - "Facebook Prophet (forecasting)"
    - "Linear Programming (cost optimization)"
    
  stack_tecnologico:
    - "FastAPI (Python 3.11+)"
    - "Redis (quota cache)"
    - "PostgreSQL (usage history)"
    - "scikit-learn (ML)"
    - "scipy (optimization)"
    - "Prophet (forecasting)"
    
  metricas_clave:
    fairness_index: "> 0.90 (Jain's Fairness Index)"
    cost_savings: "> 20% vs baseline"
    forecast_accuracy: "MAE < 15%"
    throttle_decision_latency: "< 50ms p95"
    
  integracion:
    nops_kernel:
      tipo: "Extiende Policy Engine básico"
      comunicacion: "mTLS + JWT s2s"
      degraded_mode: "Kernel usa quotas estáticas si servicio down"
      
    billing_service:
      tipo: "Consume usage data para cost optimization"
      comunicacion: "API calls bidireccionales"
      
estado: "ready_for_sprint_s23-s24"
estimated_completion: "2 semanas"
total_lines: "~1,400 líneas"
```

---

*Master Prompt Resource Governance Service v1.0 - Creado 2025-10-09*  
*Estado: Versión profesional completa*  
*Fairness-critical: Multi-tenant equity guarantee*

