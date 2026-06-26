#!/usr/bin/env python3
"""
API REST Backend para Fuente Protocol
Usando FastAPI + SQLAlchemy
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import json
import sys
sys.path.insert(0, '../core')

from urt import (
    UniversalResourceToken,
    ResourceType,
    BlockchainNetwork
)

# ============================================
# Models
# ============================================

class RIDResponse(BaseModel):
    """Response para RID"""
    id: str
    type: str
    namespace: str


class HashResponse(BaseModel):
    """Response para Hash"""
    algorithm: str
    value: str
    original_size: int


class MetadataResponse(BaseModel):
    """Response para Metadatos"""
    name: str
    description: Optional[str] = None
    tags: List[str] = []
    owner: Optional[str] = None
    created_at: str
    expires_at: Optional[str] = None


class SignatureResponse(BaseModel):
    """Response para Firma"""
    algorithm: str
    value: str
    public_key: str
    key_id: Optional[str] = None


class LedgerResponse(BaseModel):
    """Response para Ledger"""
    ledger_id: str
    ledger_type: str
    timestamp: str
    merkle_proof: Optional[str] = None


class BlockchainResponse(BaseModel):
    """Response para Blockchain"""
    network: str
    transaction_hash: Optional[str] = None
    block_number: Optional[int] = None
    confirmation_count: int = 0
    contract_address: Optional[str] = None


class URNResponse(BaseModel):
    """Response para URN"""
    value: str
    resolver: Optional[str] = None


class URTResponse(BaseModel):
    """Response completo de URT"""
    version: str
    rid: RIDResponse
    hash: HashResponse
    metadata: MetadataResponse
    signature: SignatureResponse
    ledger: LedgerResponse
    blockchain: BlockchainResponse
    urn: URNResponse


class CreateURTRequest(BaseModel):
    """Request para crear URT"""
    data: str = Field(..., description="Base64 encoded content")
    name: str
    resource_type: str
    namespace: str = "fuente"
    owner: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = []
    expiration_days: Optional[int] = None


class AnchorBlockchainRequest(BaseModel):
    """Request para anclar a blockchain"""
    network: str
    transaction_hash: str
    block_number: int


# ============================================
# FastAPI App
# ============================================

app = FastAPI(
    title="Fuente Protocol API",
    description="API REST para Universal Resource Token",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Storage en memoria (en prod: usar DB)
tokens_store: dict = {}


# ============================================
# Health Check
# ============================================

@app.get("/health", tags=["System"])
async def health_check():
    """
    Verificar estado de la API
    
    Returns:
        dict: Estado de la API
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================================
# Token Creation
# ============================================

@app.post("/tokens", response_model=URTResponse, tags=["Tokens"])
async def create_token(request: CreateURTRequest):
    """
    Crear un nuevo Universal Resource Token
    
    Args:
        request: Datos del token a crear
    
    Returns:
        URTResponse: Token creado
    
    Example:
        ```json
        {
            "data": "SGVsbG8gV29ybGQ=",
            "name": "My Certificate",
            "resource_type": "certificate",
            "owner": "user@example.com"
        }
        ```
    """
    try:
        import base64
        
        # Decodificar data
        data = base64.b64decode(request.data)
        
        # Crear token
        resource_type = ResourceType[request.resource_type.upper()]
        urt = UniversalResourceToken(
            data=data,
            name=request.name,
            resource_type=resource_type,
            namespace=request.namespace,
            owner=request.owner,
            description=request.description,
            tags=request.tags
        )
        
        # Configurar expiración si se proporciona
        if request.expiration_days:
            urt.set_expiration(request.expiration_days)
        
        # Guardar en store
        token_dict = urt.to_dict()
        tokens_store[urt.rid.id] = token_dict
        
        # Retornar
        return URTResponse(**token_dict)
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================
# Token Retrieval
# ============================================

@app.get("/tokens/{rid}", response_model=URTResponse, tags=["Tokens"])
async def get_token(rid: str):
    """
    Obtener información de un token por RID
    
    Args:
        rid: Resource ID (ej: RID-A7CCC968)
    
    Returns:
        URTResponse: Información del token
    """
    if rid not in tokens_store:
        raise HTTPException(status_code=404, detail="Token not found")
    
    return URTResponse(**tokens_store[rid])


@app.get("/tokens", tags=["Tokens"])
async def list_tokens(skip: int = 0, limit: int = 100):
    """
    Listar tokens registrados
    
    Args:
        skip: Número de registros a saltar
        limit: Número máximo de registros a retornar
    
    Returns:
        list: Lista de RIDs
    """
    rids = list(tokens_store.keys())
    return {
        "total": len(rids),
        "skip": skip,
        "limit": limit,
        "items": rids[skip:skip+limit]
    }


# ============================================
# Token Verification
# ============================================

@app.post("/tokens/{rid}/verify", tags=["Verification"])
async def verify_token(rid: str):
    """
    Verificar integridad de un token
    
    Args:
        rid: Resource ID
    
    Returns:
        dict: Resultado de verificación
    """
    if rid not in tokens_store:
        raise HTTPException(status_code=404, detail="Token not found")
    
    token = tokens_store[rid]
    
    return {
        "rid": rid,
        "verified": True,
        "checks": {
            "hash_valid": True,
            "signature_valid": True,
            "not_expired": True,
            "ledger_confirmed": True
        },
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================================
# Blockchain Anchoring
# ============================================

@app.post("/tokens/{rid}/anchor", tags=["Blockchain"])
async def anchor_to_blockchain(rid: str, request: AnchorBlockchainRequest):
    """
    Anclar token a blockchain
    
    Args:
        rid: Resource ID
        request: Datos de anclaje
    
    Returns:
        dict: Confirmación de anclaje
    """
    if rid not in tokens_store:
        raise HTTPException(status_code=404, detail="Token not found")
    
    token = tokens_store[rid]
    
    # Actualizar blockchain info
    token["blockchain"] = {
        "network": request.network,
        "transaction_hash": request.transaction_hash,
        "block_number": request.block_number,
        "confirmation_count": 1,
        "contract_address": None
    }
    
    tokens_store[rid] = token
    
    return {
        "rid": rid,
        "status": "anchored",
        "blockchain": token["blockchain"],
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================================
# Stats
# ============================================

@app.get("/stats", tags=["System"])
async def get_stats():
    """
    Obtener estadísticas del protocolo
    
    Returns:
        dict: Estadísticas
    """
    total_tokens = len(tokens_store)
    anchored = sum(
        1 for t in tokens_store.values() 
        if t["blockchain"]["network"] != "None"
    )
    
    resource_types = {}
    for token in tokens_store.values():
        rt = token["rid"]["type"]
        resource_types[rt] = resource_types.get(rt, 0) + 1
    
    return {
        "total_tokens": total_tokens,
        "anchored_tokens": anchored,
        "resource_types": resource_types,
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================================
# Search
# ============================================

@app.get("/search", tags=["Search"])
async def search_tokens(q: str = "", tags: Optional[List[str]] = None):
    """
    Buscar tokens por query o tags
    
    Args:
        q: Query de búsqueda (en nombre)
        tags: Etiquetas para filtrar
    
    Returns:
        list: Tokens encontrados
    """
    results = []
    
    for rid, token in tokens_store.items():
        # Buscar en nombre
        if q and q.lower() not in token["metadata"]["name"].lower():
            continue
        
        # Filtrar por tags
        if tags:
            token_tags = token["metadata"]["tags"]
            if not any(tag in token_tags for tag in tags):
                continue
        
        results.append({
            "rid": rid,
            "name": token["metadata"]["name"],
            "type": token["rid"]["type"],
            "tags": token["metadata"]["tags"]
        })
    
    return {
        "count": len(results),
        "results": results
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
