# 🛡️ DPIA Template — ENIS v3.0
# Data Protection Impact Assessment

```yaml
doc_version: "3.0.0"
doc_type: "DPIA Template"
doc_author: "ANDAON Legal & Compliance Team"
doc_date: "2025-01-09"
compliance: "GDPR Art. 35, ISO 27001, SOC2"
status: "production_ready"
aplicable_a:
  - "Tier 3 Enterprise (obligatorio)"
  - "Tier 2 Growth (recomendado)"
  - "Air-Gapped deployments (obligatorio)"
renovacion: "Anual o ante cambios arquitectónicos significativos"
```

---

## 📋 INFORMACIÓN GENERAL

### 1. Proyecto / Sistema

**Nombre del Sistema**: [Nombre del tenant/proyecto]  
**Versión ENIS**: v3.0.0  
**Tier Contractual**: [ ] Tier 1 SMB | [ ] Tier 2 Growth | [✓] Tier 3 Enterprise  
**Región Principal**: [ ] US | [ ] EU | [ ] APAC | [ ] LATAM  

**Descripción del Procesamiento**:  
_Descripción breve del uso de ENIS (ej: "Agentes de IA para atención al cliente con procesamiento de voz")_

**Fecha de Inicio**: YYYY-MM-DD  
**Responsable DPO**: [Nombre] | [Email] | [Teléfono]  
**Responsable Técnico**: [Nombre] | [Email] | [Teléfono]

---

## 🔍 NECESSITY AND PROPORTIONALITY

### 2. Justificación del Procesamiento

**Propósito del Procesamiento de Datos Personales**:  
_Explicar por qué es necesario procesar datos personales (ej: "Identificación de usuarios, personalización de respuestas")_

**Base Legal (GDPR Art. 6)**:
- [ ] Consentimiento explícito (Art. 6.1.a)
- [ ] Ejecución de contrato (Art. 6.1.b)
- [ ] Obligación legal (Art. 6.1.c)
- [ ] Interés vital (Art. 6.1.d)
- [ ] Interés público (Art. 6.1.e)
- [ ] Interés legítimo (Art. 6.1.f)

**Proporcionalidad**:  
_¿Se procesan solo los datos mínimos necesarios? Justificar._

---

## 📊 DATA INVENTORY

### 3. Tipos de Datos Procesados

| Categoría | Ejemplos | Volumen Estimado | Clasificación DGE |
|-----------|----------|------------------|-------------------|
| PII Básico | Nombre, email, teléfono | [N usuarios] | `PII_PERSONAL` |
| PII Sensible | Datos de salud, biométricos | [N registros] | `PII_SENSITIVE` |
| Datos Transaccionales | Logs de conversaciones, billing | [N registros/mes] | `BUSINESS_DATA` |
| Datos de Voz | Streams de audio (NO almacenados) | [N min/mes] | `STREAMING_ONLY` |
| Datos XR | Posición espacial, gestos | [N sesiones] | `SPATIAL_DATA` |

**Categorías Especiales (GDPR Art. 9)**:  
_¿Se procesan datos sensibles (salud, biométricos, etc.)? Si SÍ, base legal:_
- [ ] N/A (no se procesan datos sensibles)
- [ ] Consentimiento explícito (Art. 9.2.a)
- [ ] Otra base legal: [Especificar]

---

## 🌍 DATA RESIDENCY & RETENTION

### 4. Residencia de Datos

**Región de Almacenamiento Principal**:
- [ ] us-east-1 (Virginia, USA) → CCPA compliance
- [ ] eu-west-1 (Irlanda, EU) → GDPR compliance
- [ ] ap-southeast-1 (Singapur, APAC) → PDPA compliance
- [ ] sa-east-1 (São Paulo, LATAM) → LGPD compliance

**Transferencias Internacionales**:  
_¿Se transfieren datos fuera de la región del tenant?_
- [ ] NO: Todos los datos permanecen en región del tenant
- [ ] SÍ: Solo metadata operacional (non-PII) a US para monitoring
  - **Mecanismo**: Standard Contractual Clauses (SCCs) + Encryption

**Cumplimiento GDPR/Schrems II**:
- [✓] Datos EU permanecen en EU (no acceso US gov sin orden judicial)
- [✓] Metadata anonimizado (non-PII) puede transitar US
- [✓] Audit logs cifrados con cross-region replication

### 5. Retención de Datos

| Tipo de Dato | Retención Hot | Retención Cold | Razón Legal |
|--------------|---------------|----------------|-------------|
| PII Personal | 2 años post-churn | N/A | GDPR Art. 17 |
| Agent State | 90 días post-deletion | N/A | Operacional |
| Conversational History | 30 días (configurable) | N/A | Configurable tenant |
| Voice Recordings | **0 días** (streaming only) | N/A | Privacy by design |
| XR Spatial Data | 7 días (cache) | N/A | Privacy by design |
| Audit Logs | 90 días (hot) | 10 años (cold) | SOC2/ISO 27001 |
| Billing Records | Hot: 1 año | 7 años | Tax compliance |

**Derecho al Olvido (GDPR Art. 17)**:
- **SLA**: < 30 días para purge completo
- **Proceso**: Compliance Module + DGE automation
- **Certificado**: Emitido automáticamente post-purge
- **Excepciones**: Audit logs anonimizados (10 años), billing (7 años)

---

## 🔐 SECURITY MEASURES

### 6. Medidas Técnicas y Organizativas

**Cifrado**:
- [✓] Datos en reposo: AES-256 (PG, Redis, S3)
- [✓] Datos en tránsito: TLS 1.3 end-to-end
- [✓] Backups cifrados: AES-256 + access controls

**Autenticación y Autorización**:
- [✓] mTLS obligatorio (comunicaciones s2s)
- [✓] JWT + MFA (empleados + Tier 3 admins)
- [✓] RBAC/ABAC granular (Policy Engine)
- [✓] Audit trails inmutables (10 años)

**DGE (Data Governance Engine)**:
- [✓] Clasificación automática (regex, NER/NLP, ML)
- [✓] Redacción automática (logs/metrics)
- [✓] Egress Guard (fail-closed en Kernel)
- [✓] PII never leaves tenant region (enforced)

**SEC (Supply Chain Security)**:
- [✓] SBOM + firmas cosign
- [✓] Attestations SLSA
- [✓] Runtime verification (init-container)
- [✓] Key rotation (90 días automática)

**ZAG (Zero Agent Gateway)**:
- [✓] HMAC + anti-replay
- [✓] Rate-limiting por tenant
- [✓] DDoS protection (WAF)

**Backup & DR**:
- [✓] Hot backup: replicación síncrona (RPO = 0)
- [✓] Warm backup: snapshots cada 6h
- [✓] Cold backup: Tape/Glacier mensual
- [✓] Geo-redundancia: 3+ AZs, 2+ regiones

---

## 🚨 RISK ASSESSMENT

### 7. Identificación de Riesgos

| Riesgo | Probabilidad | Impacto | Mitigación | Riesgo Residual |
|--------|--------------|---------|-----------|-----------------|
| **Data Breach (exfiltración)** | Media | Alto | DGE + Egress Guard + Network Policies | Bajo |
| **PII leak vía logs** | Media | Alto | DGE redacción automática | Bajo |
| **Insider threat** | Baja | Alto | RBAC + MFA + Audit trails + Anomaly detection | Medio |
| **Supply chain attack** | Baja | Alto | SEC (SBOM + firmas + runtime verification) | Bajo |
| **Ransomware** | Media | Alto | Backups cifrados + Immutable infrastructure | Bajo |
| **Cert expiration (mTLS fail)** | Baja | Medio | cert-manager + alertas 15 días antes | Muy Bajo |
| **GDPR non-compliance** | Baja | Muy Alto | DPIA + DGE + Compliance Module | Bajo |
| **Cross-border transfer violation** | Baja | Alto | Residencia enforced por región + SCCs | Bajo |

**Evaluación de Impacto en Data Subjects**:  
_¿Qué daño podría causar a los usuarios un incidente?_
- Acceso no autorizado → Pérdida de privacidad
- Data breach → Robo de identidad, fraude
- Non-compliance → Multas regulatorias (hasta 4% revenue global)

---

## 🛡️ PRIVACY BY DESIGN

### 8. Medidas de Privacy by Design

- [✓] **Data Minimization**: Solo se procesa PII mínimo necesario
- [✓] **Purpose Limitation**: Datos usados solo para propósito declarado
- [✓] **Storage Limitation**: Retención limitada (30-90 días hot, 2-10 años cold)
- [✓] **Pseudonymization**: Agent IDs hasheados en logs
- [✓] **Transparency**: Portal de usuario con acceso a sus datos
- [✓] **Consent Management**: Consentimiento explícito para datos sensibles
- [✓] **Right to Access**: Portal self-service para data subjects
- [✓] **Right to Erasure**: Proceso automatizado (< 30 días)
- [✓] **Data Portability**: Export JSON/CSV disponible en portal

---

## 👥 DATA SUBJECT RIGHTS

### 9. Ejercicio de Derechos (GDPR Art. 12-23)

| Derecho | SLA | Proceso Automatizado | Responsable |
|---------|-----|----------------------|-------------|
| **Acceso (Art. 15)** | < 30 días | Portal self-service | Compliance Module |
| **Rectificación (Art. 16)** | < 7 días | Portal + API | ASM Service |
| **Supresión (Art. 17)** | < 30 días | DGE + Compliance automation | DGE + Compliance |
| **Limitación (Art. 18)** | < 7 días | Flag "processing_limited" | ASM Service |
| **Portabilidad (Art. 20)** | < 30 días | Export JSON/CSV | Compliance Module |
| **Oposición (Art. 21)** | < 7 días | Opt-out flag | Compliance Module |

**Punto de Contacto para Data Subjects**:  
- **Email**: dpo@enis.io  
- **Portal**: https://privacy.enis.io  
- **Teléfono**: +1 (XXX) XXX-XXXX

---

## 🏢 DATA PROCESSORS & THIRD PARTIES

### 10. Subprocesadores

| Subprocesador | Servicio | Región | DPA Firmado | Certificación |
|---------------|----------|--------|-------------|---------------|
| AWS | Hosting (EC2, S3, RDS) | us-east-1 / eu-west-1 | ✓ | SOC2, ISO 27001 |
| Cloudflare | WAF + DDoS | Global (anycast) | ✓ | SOC2, ISO 27001 |
| PagerDuty | Incident response | US | ✓ | SOC2 |
| Confluent | Schema Registry (Kafka) | US | ✓ | SOC2 |

**Data Processing Agreements (DPAs)**:  
_Todos los subprocesadores tienen DPA firmado con cláusulas GDPR Art. 28_

**Subprocessor Changes**:  
_30 días notice a clientes Tier 3 ante cambio de subprocesador_

---

## 📜 COMPLIANCE VALIDATION

### 11. Checklist DPIA

- [✓] **Residencia de datos documentada** (4 regiones: US/EU/APAC/LATAM)
- [✓] **Retención por tipo de dato** (7-10 años según compliance)
- [✓] **Derecho al olvido** (< 30 días, proceso automatizado)
- [✓] **DGE clasificación/redacción** (automática, fail-closed)
- [✓] **Egress control** (Egress Guard en Kernel, fail-closed)
- [✓] **Audit trails inmutables** (10 años retention, SOC2/ISO)
- [✓] **Backup/restore con cifrado** (AES-256, geo-redundancia)
- [✓] **Incident response** (P0 < 15 min, runbooks validados)

### 12. Proceso de Aprobación

**Paso 1: Legal Review**  
**Responsable**: DPO + Compliance Team  
**Fecha**: YYYY-MM-DD  
**Resultado**: [ ] Aprobado | [ ] Requiere ajustes  
**Comentarios**: _[Notas del DPO]_

**Paso 2: Technical Validation**  
**Responsable**: Security Team + CISO  
**Fecha**: YYYY-MM-DD  
**Resultado**: [ ] Aprobado | [ ] Requiere ajustes  
**Comentarios**: _[Notas del CISO]_

**Paso 3: Business Approval**  
**Responsable**: C-level (CEO/CTO/CFO)  
**Fecha**: YYYY-MM-DD  
**Resultado**: [ ] Aprobado | [ ] Requiere ajustes  
**Comentarios**: _[Notas de C-level]_

**Paso 4: Customer Signature (Tier 3)**  
**Responsable**: Tenant (Customer DPO)  
**Fecha**: YYYY-MM-DD  
**Firma Digital**: _[Hash SHA-256 del documento firmado]_

---

## 📝 MONITORING & REVIEW

### 13. Monitoreo Continuo

**Dashboard de Compliance** (Grafana):  
- **URL**: https://compliance.enis.io/dashboards/gdpr-compliance  
- **Métricas**:
  - GDPR deletion requests (pending/completed/failed)
  - DGE classification accuracy (> 95% target)
  - Egress policy violations (should be 0)
  - Audit trail completeness (100% target)
  - SLA compliance (< 30 días deletion)

**Alertas PagerDuty**:
- **Deletion request > 25 días**: Alerta a Compliance Team
- **DGE classification failure**: Alerta a Security Team
- **Egress policy violation**: Alerta inmediata a CISO + DPO

### 14. Renovación DPIA

**Frecuencia**: Anual o ante cambios arquitectónicos significativos  
**Próxima Revisión**: YYYY-MM-DD (12 meses)  
**Trigger para Revisión Ad-Hoc**:
- Cambio de subprocesador
- Nueva categoría de datos personales procesados
- Cambio de región de almacenamiento
- Incidente de seguridad P0
- Nuevo requerimiento regulatorio

---

## 📚 ANEXOS

### Anexo A: Compliance Statements
- `GDPR_Compliance_Statement_2025.pdf`
- `CCPA_Compliance_Statement_2025.pdf`
- `PDPA_Compliance_Statement_2025.pdf`
- `LGPD_Compliance_Statement_2025.pdf`

### Anexo B: Data Flow Diagrams
- `ENIS_v3_Data_Flow_Diagram.pdf`
- `DGE_Classification_Pipeline.pdf`

### Anexo C: Security Certifications
- `SOC2_Type_II_Report_2024.pdf`
- `ISO_27001_Certificate_2024.pdf`

### Anexo D: Incident Response Plan
- `IR_Runbook_Data_Breach.md`
- `IR_Runbook_GDPR_Violation.md`

---

## ✍️ FIRMAS

**DPO (Data Protection Officer)**  
Nombre: ____________________  
Firma: ____________________  
Fecha: YYYY-MM-DD

**CISO (Chief Information Security Officer)**  
Nombre: ____________________  
Firma: ____________________  
Fecha: YYYY-MM-DD

**CTO (Chief Technology Officer)**  
Nombre: ____________________  
Firma: ____________________  
Fecha: YYYY-MM-DD

**Customer DPO (Tier 3 Tenant)**  
Nombre: ____________________  
Firma: ____________________  
Fecha: YYYY-MM-DD

---

## 📌 VERSION HISTORY

| Versión | Fecha | Cambios | Autor |
|---------|-------|---------|-------|
| 3.0.0 | 2025-01-09 | Initial release DPIA Template ENIS v3.0 | ANDAON Legal |
| 2.5.0 | 2024-10-15 | Added Tier 3 Enterprise requirements | ANDAON Legal |

---

**Documento confidencial — Propiedad de ANDAON SA DE CV**  
**Clasificación**: INTERNAL — Compartir solo con personal autorizado y clientes Tier 3 bajo NDA.

