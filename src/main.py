"""
ENIS v3.0 Agent Contracts - FastAPI Application

Aplicación principal para el servidor de contratos de agentes.
Proporciona endpoints para validación de contratos, esquemas y definiciones.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List
import json
import yaml
from pathlib import Path

# Configuración de la aplicación
app = FastAPI(
    title="ENIS v3.0 Agent Contracts API",
    description="Centralized API contracts, schemas, and definitions serving as Source of Truth for the ENIS v3.0 platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class ContractValidationRequest(BaseModel):
    """Solicitud de validación de contrato"""
    contract_type: str  # "openapi", "json_schema", "protobuf"
    content: str
    format: str = "yaml"  # "yaml", "json", "proto"

class ValidationResponse(BaseModel):
    """Respuesta de validación"""
    is_valid: bool
    errors: List[str] = []
    warnings: List[str] = []
    contract_info: Dict[str, Any] = {}

class HealthResponse(BaseModel):
    """Respuesta de health check"""
    status: str
    version: str
    timestamp: str
    services: Dict[str, str]

# Rutas principales
@app.get("/", response_model=Dict[str, str])
async def root():
    """Endpoint raíz con información básica"""
    return {
        "message": "ENIS v3.0 Agent Contracts API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    import datetime
    
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.datetime.utcnow().isoformat(),
        services={
            "contracts": "available",
            "schemas": "available",
            "validation": "available"
        }
    )

@app.get("/contracts", response_model=Dict[str, List[str]])
async def list_contracts():
    """Listar todos los contratos disponibles"""
    contracts_dir = Path("contracts")
    
    if not contracts_dir.exists():
        return {"contracts": [], "message": "Directorio de contratos no encontrado"}
    
    contracts = {
        "openapi": [],
        "json_schemas": [],
        "protobuf": []
    }
    
    # Buscar archivos OpenAPI
    for file_path in contracts_dir.glob("*.yaml"):
        contracts["openapi"].append(str(file_path))
    for file_path in contracts_dir.glob("*.yml"):
        contracts["openapi"].append(str(file_path))
    
    # Buscar esquemas JSON
    schemas_dir = Path("schemas")
    if schemas_dir.exists():
        for file_path in schemas_dir.glob("*.json"):
            contracts["json_schemas"].append(str(file_path))
    
    # Buscar archivos Protobuf
    proto_dir = Path("proto")
    if proto_dir.exists():
        for file_path in proto_dir.glob("*.proto"):
            contracts["protobuf"].append(str(file_path))
    
    return contracts

@app.post("/validate", response_model=ValidationResponse)
async def validate_contract(request: ContractValidationRequest):
    """Validar un contrato (OpenAPI, JSON Schema, o Protobuf)"""
    errors = []
    warnings = []
    contract_info = {}
    
    try:
        if request.contract_type == "openapi":
            # Validar OpenAPI
            try:
                if request.format == "yaml":
                    spec_data = yaml.safe_load(request.content)
                else:  # json
                    spec_data = json.loads(request.content)
                
                # Validación básica de OpenAPI
                required_fields = ["openapi", "info", "paths"]
                for field in required_fields:
                    if field not in spec_data:
                        errors.append(f"Campo requerido '{field}' no encontrado")
                
                if not errors:
                    contract_info = {
                        "openapi_version": spec_data.get("openapi"),
                        "title": spec_data.get("info", {}).get("title"),
                        "version": spec_data.get("info", {}).get("version"),
                        "paths_count": len(spec_data.get("paths", {}))
                    }
                    
            except yaml.YAMLError as e:
                errors.append(f"Error de sintaxis YAML: {str(e)}")
            except json.JSONDecodeError as e:
                errors.append(f"Error de sintaxis JSON: {str(e)}")
        
        elif request.contract_type == "json_schema":
            # Validar JSON Schema
            try:
                schema_data = json.loads(request.content)
                
                # Validación básica de JSON Schema
                if "$schema" not in schema_data:
                    warnings.append("Campo '$schema' no especificado")
                
                contract_info = {
                    "schema_version": schema_data.get("$schema"),
                    "title": schema_data.get("title"),
                    "type": schema_data.get("type"),
                    "properties_count": len(schema_data.get("properties", {}))
                }
                
            except json.JSONDecodeError as e:
                errors.append(f"Error de sintaxis JSON: {str(e)}")
        
        elif request.contract_type == "protobuf":
            # Para Protobuf, solo validación básica de sintaxis
            if "syntax" not in request.content:
                warnings.append("Sintaxis de protobuf no especificada")
            
            contract_info = {
                "type": "protobuf",
                "size": len(request.content)
            }
        
        else:
            errors.append(f"Tipo de contrato no soportado: {request.contract_type}")
    
    except Exception as e:
        errors.append(f"Error inesperado: {str(e)}")
    
    return ValidationResponse(
        is_valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
        contract_info=contract_info
    )

@app.get("/docs/contracts/{contract_name}")
async def get_contract_docs(contract_name: str):
    """Obtener documentación de un contrato específico"""
    # Implementación futura para servir documentación de contratos
    return {
        "contract_name": contract_name,
        "message": "Documentación de contratos en desarrollo",
        "available_endpoints": [
            "/contracts",
            "/validate",
            "/health"
        ]
    }

# Configuración para desarrollo
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
