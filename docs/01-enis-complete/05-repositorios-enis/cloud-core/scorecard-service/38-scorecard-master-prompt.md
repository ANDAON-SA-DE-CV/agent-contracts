# 38 - Scorecard Service Master Prompt

---
prompt_id: "38-scorecard-master-prompt"
prompt_type: "master_prompt"
service_name: "scorecard-service"
dna_version: "3.0"
semver: "1.0.0"
date: "2025-10-08"
author: "@andaon"
domain: "Analytics & Scoring"
description: "Master prompt para Scorecard Service - Agent scoring, performance analytics y ML benchmarks"
estimated_pages: "120-140"
compliance_status: "DNA_v3_compliant"
dependencies: ["00-dna-proyecto-prompt.md", "07-nops-master-prompt.md", "08-agent-marketplace-master-prompt.md"]
generates:
 - "architecture/scorecard/*"
 - "reference/scoring-algorithms/*"
 - "ml-models/benchmarks/*"
child_prompts: 15
validation_script: "validate-scorecard-documentation.js"
release_status: "ready_for_sprint_s23"
feeds_to: ["08-agent-marketplace", "ENIS-Frontend"]
priority: "P2"
sprint: "S23-P1"
---

## 🎯 PROPÓSITO Y CONTEXTO

**ROL:** Arquitecto Senior de Analytics & ML en ENIS v3.0

**TAREA:** Generar documentación completa del Scorecard Service - servicio para scoring de Edge Agents, analytics de performance, benchmarking y ML models predictivos.

**OBJETIVO:** Producir 120-140 páginas de documentación técnica que cubra scoring algorithms, performance analytics, ML models (calidad predictiva), leaderboards, certificación de agents y APIs.

**CONTEXTO CRÍTICO:**
- El Scorecard Service es **QUALITY-CRITICAL** - determina qué agents son confiables
- Scoring multi-dimensional: accuracy, latency, cost, reliability, security
- ML models predictivos para calidad de agents
- Leaderboards públicos por vertical (🟤🟡🟢🔵🔴)
- Integración con Agent Marketplace (certificación)

# 📑 TABLA DE CONTENIDOS

- 🏗️ Arquitectura del Scorecard Service
- 📊 Scoring Algorithms
- 🤖 ML Models (Predictive Quality)
- 📈 Performance Analytics
- 🏆 Leaderboards & Rankings
- ✅ Agent Certification
- 🔧 APIs y SDKs
- 🚀 Deployment Patterns
- 📁 Estructura de Documentación

## 🏗️ ARQUITECTURA DEL SCORECARD SERVICE

### **Componentes Core**

```yaml
scorecard_architecture:
  scoring_engine:
    description: "Motor de scoring multi-dimensional de agents"
    technology: "Python + Pandas + scikit-learn"
    dimensions:
      accuracy:
        weight: 0.35
        metrics:
          - "task_success_rate"
          - "output_quality_score"
          - "hallucination_rate"
          
      latency:
        weight: 0.25
        metrics:
          - "p50_execution_time"
          - "p95_execution_time"
          - "timeout_rate"
          
      cost:
        weight: 0.15
        metrics:
          - "tokens_per_task"
          - "cost_per_execution"
          - "efficiency_ratio"
          
      reliability:
        weight: 0.15
        metrics:
          - "uptime_percentage"
          - "error_rate"
          - "retry_rate"
          
      security:
        weight: 0.10
        metrics:
          - "sec_validation_pass_rate"
          - "audit_compliance_score"
          - "vulnerability_count"
    
    aggregation:
      formula: "weighted_sum(dimensions)"
      range: "0-100"
      update_frequency: "hourly"
      
  analytics_engine:
    description: "Performance analytics y trending"
    technology: "Python + TimescaleDB + Plotly"
    features:
      - "Time-series performance tracking"
      - "Comparative analysis (agent vs baseline)"
      - "Anomaly detection (performance degradation)"
      - "Root cause analysis"
      - "Forecasting (next 7 days performance)"
      
  ml_models:
    description: "ML models para predicción de calidad"
    technology: "Python + scikit-learn + XGBoost"
    models:
      quality_predictor:
        type: "Gradient Boosting Classifier"
        target: "will_succeed (binary)"
        features:
          - "agent_historical_success_rate"
          - "task_complexity_score"
          - "input_length"
          - "time_of_day"
          - "agent_load"
        accuracy: "> 85%"
        
      performance_forecaster:
        type: "LSTM Time Series"
        target: "latency_next_hour"
        features:
          - "historical_latency (24h)"
          - "agent_load"
          - "time_features"
        mae: "< 200ms"
        
  leaderboard_engine:
    description: "Rankings públicos de agents"
    technology: "Redis (sorted sets) + PostgreSQL"
    leaderboards:
      global:
        scope: "All agents"
        metric: "overall_score"
        
      per_vertical:
        scopes:
          - "🟤 Infrastructure"
          - "🟡 Energy"
          - "🟢 Education"
          - "🔵 Health"
          - "🔴 Emergency"
        metric: "vertical_specific_score"
        
      per_tier:
        scopes: ["Zero", "Shared", "Lite", "Enterprise"]
        metric: "tier_normalized_score"
        
    update_frequency: "every 15 minutes"
    cache_ttl: "5 minutes"
```

---

## 📊 SCORING ALGORITHMS

### **Multi-Dimensional Scoring**

```python
# scorecard_service/scoring/engine.py
from typing import Dict, List, Any
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class ScoringEngine:
    """
    Motor de scoring multi-dimensional
    
    Calcula score global y por dimensión para Edge Agents
    """
    
    DIMENSION_WEIGHTS = {
        "accuracy": 0.35,
        "latency": 0.25,
        "cost": 0.15,
        "reliability": 0.15,
        "security": 0.10
    }
    
    def __init__(self, db_session):
        self.session = db_session
        
    async def calculate_agent_score(
        self,
        agent_id: str,
        time_window: timedelta = timedelta(days=7)
    ) -> Dict[str, Any]:
        """
        Calcula score completo de un agent
        
        Returns:
            {
                "overall_score": 0-100,
                "dimensions": {
                    "accuracy": {...},
                    "latency": {...},
                    ...
                },
                "rank": int,
                "percentile": float
            }
        """
        # 1. Obtener métricas del agent
        metrics = await self._fetch_agent_metrics(agent_id, time_window)
        
        # 2. Calcular scores por dimensión
        dimension_scores = {}
        
        dimension_scores["accuracy"] = await self._score_accuracy(metrics)
        dimension_scores["latency"] = await self._score_latency(metrics)
        dimension_scores["cost"] = await self._score_cost(metrics)
        dimension_scores["reliability"] = await self._score_reliability(metrics)
        dimension_scores["security"] = await self._score_security(metrics)
        
        # 3. Calcular score global (weighted sum)
        overall_score = sum(
            score["normalized"] * self.DIMENSION_WEIGHTS[dim]
            for dim, score in dimension_scores.items()
        ) * 100
        
        # 4. Calcular ranking y percentile
        rank, percentile = await self._calculate_ranking(agent_id, overall_score)
        
        return {
            "agent_id": agent_id,
            "overall_score": round(overall_score, 2),
            "dimensions": dimension_scores,
            "rank": rank,
            "percentile": percentile,
            "calculated_at": datetime.utcnow().isoformat()
        }
    
    async def _score_accuracy(self, metrics: Dict) -> Dict[str, Any]:
        """
        Scoring de accuracy
        
        Metrics:
        - task_success_rate (0-1)
        - output_quality_score (0-100)
        - hallucination_rate (0-1, lower is better)
        """
        success_rate = metrics.get("task_success_rate", 0)
        quality_score = metrics.get("output_quality_score", 0) / 100.0
        hallucination_rate = metrics.get("hallucination_rate", 0)
        
        # Formula: weighted average con penalización por hallucinations
        normalized = (
            0.5 * success_rate +
            0.3 * quality_score +
            0.2 * (1 - hallucination_rate)  # Invertir (menos es mejor)
        )
        
        return {
            "normalized": normalized,
            "raw_metrics": {
                "success_rate": success_rate,
                "quality_score": quality_score,
                "hallucination_rate": hallucination_rate
            },
            "grade": self._score_to_grade(normalized)
        }
    
    async def _score_latency(self, metrics: Dict) -> Dict[str, Any]:
        """
        Scoring de latency
        
        Metrics:
        - p50_execution_time (seconds)
        - p95_execution_time (seconds)
        - timeout_rate (0-1, lower is better)
        """
        p50 = metrics.get("p50_execution_time", 10)
        p95 = metrics.get("p95_execution_time", 30)
        timeout_rate = metrics.get("timeout_rate", 0)
        
        # Targets (baseline)
        p50_target = 2.0  # 2s
        p95_target = 5.0  # 5s
        
        # Normalized scores (closer to target = better)
        p50_score = max(0, 1 - (p50 - p50_target) / p50_target)
        p95_score = max(0, 1 - (p95 - p95_target) / p95_target)
        
        normalized = (
            0.4 * p50_score +
            0.4 * p95_score +
            0.2 * (1 - timeout_rate)
        )
        
        return {
            "normalized": normalized,
            "raw_metrics": {
                "p50_ms": p50 * 1000,
                "p95_ms": p95 * 1000,
                "timeout_rate": timeout_rate
            },
            "grade": self._score_to_grade(normalized)
        }
    
    async def _score_cost(self, metrics: Dict) -> Dict[str, Any]:
        """
        Scoring de cost-efficiency
        
        Metrics:
        - tokens_per_task (lower is better)
        - cost_per_execution (USD, lower is better)
        - efficiency_ratio (output_quality / cost)
        """
        tokens = metrics.get("tokens_per_task", 10000)
        cost = metrics.get("cost_per_execution", 0.10)
        efficiency = metrics.get("efficiency_ratio", 1.0)
        
        # Targets (baseline - GPT-3.5 turbo equivalent)
        tokens_target = 5000
        cost_target = 0.05
        
        tokens_score = max(0, 1 - (tokens - tokens_target) / tokens_target)
        cost_score = max(0, 1 - (cost - cost_target) / cost_target)
        
        normalized = (
            0.3 * tokens_score +
            0.3 * cost_score +
            0.4 * min(1.0, efficiency)  # Cap at 1.0
        )
        
        return {
            "normalized": normalized,
            "raw_metrics": {
                "tokens_per_task": tokens,
                "cost_per_execution_usd": cost,
                "efficiency_ratio": efficiency
            },
            "grade": self._score_to_grade(normalized)
        }
    
    async def _score_reliability(self, metrics: Dict) -> Dict[str, Any]:
        """
        Scoring de reliability
        
        Metrics:
        - uptime_percentage (0-100)
        - error_rate (0-1, lower is better)
        - retry_rate (0-1, lower is better)
        """
        uptime = metrics.get("uptime_percentage", 99.0) / 100.0
        error_rate = metrics.get("error_rate", 0.01)
        retry_rate = metrics.get("retry_rate", 0.05)
        
        normalized = (
            0.5 * uptime +
            0.3 * (1 - error_rate) +
            0.2 * (1 - retry_rate)
        )
        
        return {
            "normalized": normalized,
            "raw_metrics": {
                "uptime_percentage": uptime * 100,
                "error_rate": error_rate,
                "retry_rate": retry_rate
            },
            "grade": self._score_to_grade(normalized)
        }
    
    async def _score_security(self, metrics: Dict) -> Dict[str, Any]:
        """
        Scoring de security
        
        Metrics:
        - sec_validation_pass_rate (0-1)
        - audit_compliance_score (0-100)
        - vulnerability_count (lower is better)
        """
        sec_pass_rate = metrics.get("sec_validation_pass_rate", 0.95)
        compliance_score = metrics.get("audit_compliance_score", 80) / 100.0
        vulnerabilities = metrics.get("vulnerability_count", 0)
        
        # Penalty por vulnerabilities
        vuln_penalty = min(1.0, vulnerabilities * 0.1)  # -10% per vuln
        
        normalized = (
            0.5 * sec_pass_rate +
            0.3 * compliance_score +
            0.2 * (1 - vuln_penalty)
        )
        
        return {
            "normalized": normalized,
            "raw_metrics": {
                "sec_pass_rate": sec_pass_rate,
                "compliance_score": compliance_score * 100,
                "vulnerability_count": vulnerabilities
            },
            "grade": self._score_to_grade(normalized)
        }
    
    def _score_to_grade(self, score: float) -> str:
        """Convierte score normalized a grade (A-F)"""
        if score >= 0.95:
            return "A+"
        elif score >= 0.90:
            return "A"
        elif score >= 0.85:
            return "A-"
        elif score >= 0.80:
            return "B+"
        elif score >= 0.75:
            return "B"
        elif score >= 0.70:
            return "B-"
        elif score >= 0.65:
            return "C+"
        elif score >= 0.60:
            return "C"
        elif score >= 0.55:
            return "C-"
        else:
            return "F"
```

---

## 🤖 ML MODELS (PREDICTIVE QUALITY)

### **Quality Predictor Model**

```python
# scorecard_service/ml/quality_predictor.py
from typing import Dict, List, Any
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
import joblib

class QualityPredictor:
    """
    ML model para predecir probabilidad de éxito de ejecución de agent
    
    Target: will_succeed (binary: 0 o 1)
    Model: Gradient Boosting Classifier
    Expected Accuracy: > 85%
    """
    
    def __init__(self):
        self.model = None
        self.feature_names = [
            "agent_historical_success_rate",
            "task_complexity_score",
            "input_length_chars",
            "hour_of_day",
            "day_of_week",
            "agent_current_load",
            "agent_avg_latency_1h",
            "agent_error_rate_24h"
        ]
        
    async def train(
        self,
        training_data: pd.DataFrame,
        test_size: float = 0.2
    ) -> Dict[str, Any]:
        """
        Entrena el modelo con datos históricos
        
        Args:
            training_data: DataFrame con features + target (will_succeed)
            test_size: Proporción para test set
            
        Returns:
            Métricas de evaluación
        """
        # 1. Split train/test
        X = training_data[self.feature_names]
        y = training_data["will_succeed"]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # 2. Train model
        self.model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        # 3. Evaluate
        y_pred = self.model.predict(X_test)
        
        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred),
            "recall": recall_score(y_test, y_pred),
            "training_samples": len(X_train),
            "test_samples": len(X_test)
        }
        
        # 4. Feature importance
        feature_importance = dict(zip(
            self.feature_names,
            self.model.feature_importances_
        ))
        
        metrics["feature_importance"] = feature_importance
        
        return metrics
    
    async def predict_success_probability(
        self,
        agent_id: str,
        task_features: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Predice probabilidad de éxito para una ejecución específica
        
        Returns:
            {
                "probability_success": 0.0-1.0,
                "confidence": 0.0-1.0,
                "recommendation": "proceed|warn|block"
            }
        """
        if self.model is None:
            raise ValueError("Model not trained")
        
        # 1. Construir feature vector
        features = await self._build_feature_vector(agent_id, task_features)
        X = pd.DataFrame([features], columns=self.feature_names)
        
        # 2. Predict probability
        proba = self.model.predict_proba(X)[0]
        probability_success = proba[1]  # Class 1 (success)
        
        # 3. Calculate confidence
        confidence = max(proba) - min(proba)  # Separation between classes
        
        # 4. Recommendation based on probability
        if probability_success >= 0.80:
            recommendation = "proceed"
        elif probability_success >= 0.50:
            recommendation = "warn"
        else:
            recommendation = "block"
        
        return {
            "probability_success": float(probability_success),
            "confidence": float(confidence),
            "recommendation": recommendation,
            "features_used": features
        }
    
    async def _build_feature_vector(
        self,
        agent_id: str,
        task_features: Dict[str, Any]
    ) -> Dict[str, float]:
        """Construye vector de features para predicción"""
        # Fetch agent historical metrics
        agent_metrics = await self._fetch_agent_metrics(agent_id)
        
        return {
            "agent_historical_success_rate": agent_metrics["success_rate"],
            "task_complexity_score": task_features["complexity_score"],
            "input_length_chars": len(task_features["input_text"]),
            "hour_of_day": datetime.utcnow().hour,
            "day_of_week": datetime.utcnow().weekday(),
            "agent_current_load": agent_metrics["current_load"],
            "agent_avg_latency_1h": agent_metrics["avg_latency_1h"],
            "agent_error_rate_24h": agent_metrics["error_rate_24h"]
        }
```

---

## 📈 PERFORMANCE ANALYTICS

### **Time-Series Analytics**

```python
# scorecard_service/analytics/performance_analyzer.py
import pandas as pd
from prophet import Prophet  # Facebook Prophet for forecasting
import matplotlib.pyplot as plt

class PerformanceAnalyzer:
    """
    Análisis de performance time-series y forecasting
    """
    
    async def analyze_agent_trend(
        self,
        agent_id: str,
        metric: str = "overall_score",
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Analiza tendencia de performance de un agent
        
        Returns:
            {
                "trend": "improving|declining|stable",
                "change_percentage": float,
                "anomalies": [list of detected anomalies],
                "forecast_7d": [predicted values]
            }
        """
        # 1. Fetch historical data
        df = await self._fetch_timeseries_data(agent_id, metric, days)
        
        # 2. Calculate trend (linear regression)
        from scipy.stats import linregress
        slope, intercept, r_value, p_value, std_err = linregress(
            range(len(df)),
            df[metric]
        )
        
        # Interpret trend
        if slope > 0.5:
            trend = "improving"
        elif slope < -0.5:
            trend = "declining"
        else:
            trend = "stable"
        
        change_percentage = (df[metric].iloc[-1] - df[metric].iloc[0]) / df[metric].iloc[0] * 100
        
        # 3. Anomaly detection (Z-score method)
        df["z_score"] = (df[metric] - df[metric].mean()) / df[metric].std()
        anomalies = df[df["z_score"].abs() > 2.5].to_dict("records")
        
        # 4. Forecast next 7 days (Prophet)
        forecast_df = await self._forecast_metric(df, metric, periods=7)
        
        return {
            "agent_id": agent_id,
            "metric": metric,
            "trend": trend,
            "change_percentage": round(change_percentage, 2),
            "anomalies": anomalies,
            "forecast_7d": forecast_df["yhat"].tolist()
        }
    
    async def _forecast_metric(
        self,
        df: pd.DataFrame,
        metric: str,
        periods: int = 7
    ) -> pd.DataFrame:
        """Forecasting usando Facebook Prophet"""
        # Prepare data for Prophet
        prophet_df = df.rename(columns={"timestamp": "ds", metric: "y"})
        
        # Train Prophet model
        model = Prophet(
            daily_seasonality=True,
            weekly_seasonality=True
        )
        model.fit(prophet_df)
        
        # Generate future dates
        future = model.make_future_dataframe(periods=periods)
        
        # Predict
        forecast = model.predict(future)
        
        return forecast
```

---

## 🏆 LEADERBOARDS & RANKINGS

### **Redis-Based Leaderboard**

```python
# scorecard_service/leaderboards/manager.py
import redis.asyncio as aioredis
from typing import List, Dict, Any

class LeaderboardManager:
    """
    Gestión de leaderboards con Redis sorted sets
    
    Performance: O(log N) para inserción/actualización
    """
    
    def __init__(self, redis_client: aioredis.Redis):
        self.redis = redis_client
        
    async def update_agent_score(
        self,
        agent_id: str,
        score: float,
        leaderboard_key: str = "leaderboard:global"
    ):
        """Actualiza score de agent en leaderboard"""
        await self.redis.zadd(leaderboard_key, {agent_id: score})
        
    async def get_top_agents(
        self,
        leaderboard_key: str = "leaderboard:global",
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Obtiene top N agents del leaderboard"""
        # Redis ZREVRANGE (descending order)
        results = await self.redis.zrevrange(
            leaderboard_key,
            0,
            limit - 1,
            withscores=True
        )
        
        top_agents = []
        for rank, (agent_id, score) in enumerate(results, start=1):
            agent_info = await self._fetch_agent_info(agent_id)
            
            top_agents.append({
                "rank": rank,
                "agent_id": agent_id.decode(),
                "agent_name": agent_info["name"],
                "score": score,
                "tier": agent_info["tier"],
                "vertical": agent_info["vertical"]
            })
        
        return top_agents
    
    async def get_agent_rank(
        self,
        agent_id: str,
        leaderboard_key: str = "leaderboard:global"
    ) -> int:
        """Obtiene rank de un agent específico"""
        rank = await self.redis.zrevrank(leaderboard_key, agent_id)
        return (rank + 1) if rank is not None else None
```

---

## ✅ AGENT CERTIFICATION

### **Certification Criteria**

```yaml
certification_levels:
  bronze:
    requirements:
      overall_score: "> 60"
      executions: "> 100"
      success_rate: "> 80%"
      sec_validation: "100% pass"
      
  silver:
    requirements:
      overall_score: "> 75"
      executions: "> 500"
      success_rate: "> 90%"
      p95_latency: "< 5s"
      
  gold:
    requirements:
      overall_score: "> 85"
      executions: "> 1000"
      success_rate: "> 95%"
      p95_latency: "< 2s"
      audit_compliance: "100%"
      
  platinum:
    requirements:
      overall_score: "> 95"
      executions: "> 5000"
      success_rate: "> 99%"
      p95_latency: "< 1s"
      featured_in_marketplace: true
```

---

## 🔧 APIS Y SDKS

```yaml
scorecard_api:
  GET /api/v1/agents/{agent_id}/score:
    description: "Get current score"
    auth: "JWT user or s2s"
    
  GET /api/v1/leaderboard/{vertical}:
    description: "Get leaderboard"
    params:
      limit: "int (default: 10)"
      tier: "optional filter"
      
  POST /api/v1/predict/quality:
    description: "Predict execution quality"
    auth: "mTLS + JWT s2s"
    request:
      agent_id: "string"
      task_features: "object"
```

---

## 🚀 DEPLOYMENT PATTERNS

```yaml
deployment:
  ml_models:
    storage: "S3 (versioned models)"
    serving: "FastAPI + scikit-learn"
    update_frequency: "weekly retraining"
    
  leaderboards:
    cache: "Redis sorted sets"
    persistence: "PostgreSQL (backup)"
    update: "every 15 minutes"
```

---

## 📁 ESTRUCTURA DE DOCUMENTACIÓN

```yaml
documentation_structure:
  scorecard_service/:
    - "README.md"
    - "38-scorecard-master-prompt.md"
    - "SCORING_ALGORITHMS.md"
    - "ML_MODELS.md"
    
  ml-models/:
    - "quality-predictor.pkl"
    - "performance-forecaster.pkl"
    - "training-pipeline.py"
```

---

## 📋 METADATA DE CIERRE

```yaml
service_summary:
  nombre: "Scorecard Service"
  proposito: "Agent scoring, analytics, ML benchmarks"
  prioridad: "P2"
  
  componentes_principales:
    - "Multi-dimensional scoring engine"
    - "ML quality predictor (85%+ accuracy)"
    - "Performance analytics & forecasting"
    - "Leaderboards (Redis sorted sets)"
    
  stack_tecnologico:
    - "Python + Pandas + scikit-learn"
    - "Redis (leaderboards)"
    - "TimescaleDB (time-series)"
    - "Prophet (forecasting)"
    
estado: "ready_for_sprint_s23-p1"
estimated_completion: "1 semana"
total_lines: "~1,200 líneas"
```

---

*Master Prompt Scorecard Service v1.0 - Creado 2025-10-08*  
*Estado: Versión profesional completa*  
*Quality-critical: Determines agent trustworthiness*
