"""
Universal Resource Token (URT) Protocol Implementation
Core module for creating and validating URT tokens
"""

import json
import hashlib
import secrets
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum
import base64


class ResourceType(Enum):
    """Tipos de recursos soportados por URT"""
    DOCUMENT = "document"
    DIGITAL_ASSET = "digital_asset"
    CERTIFICATE = "certificate"
    CREDENTIAL = "credential"
    IDENTITY = "identity"
    CONTRACT = "contract"
    DATA_PACKAGE = "data_package"
    NFT = "nft"
    OTHER = "other"


class HashAlgorithm(Enum):
    """Algoritmos de hash soportados"""
    SHA256 = "SHA-256"
    SHA512 = "SHA-512"
    BLAKE2B = "Blake2b"


class SignatureAlgorithm(Enum):
    """Algoritmos de firma soportados"""
    ECDSA = "ECDSA"
    EDDSA = "EdDSA"
    RSA = "RSA-2048"


class BlockchainNetwork(Enum):
    """Redes blockchain soportadas"""
    BITCOIN = "Bitcoin"
    ETHEREUM = "Ethereum"
    SOLANA = "Solana"
    POLYGON = "Polygon"
    NONE = "None"


@dataclass
class URTIdentity:
    """RID Token - Resource ID Token"""
    id: str  # RID-XXXXXXXX
    type: ResourceType
    namespace: str
    
    @staticmethod
    def generate(namespace: str, resource_type: ResourceType) -> 'URTIdentity':
        """Genera un nuevo RID único"""
        random_hex = secrets.token_hex(4).upper()
        return URTIdentity(
            id=f"RID-{random_hex}",
            type=resource_type,
            namespace=namespace.lower()
        )


@dataclass
class URTHash:
    """HASH Token - Integridad del recurso"""
    algorithm: HashAlgorithm
    value: str  # Hash hexadecimal
    original_size: int  # Tamaño en bytes
    
    @staticmethod
    def from_data(data: bytes, algorithm: HashAlgorithm = HashAlgorithm.SHA256) -> 'URTHash':
        """Calcula hash de datos"""
        if algorithm == HashAlgorithm.SHA256:
            hash_value = hashlib.sha256(data).hexdigest()
        elif algorithm == HashAlgorithm.SHA512:
            hash_value = hashlib.sha512(data).hexdigest()
        else:
            hash_value = hashlib.blake2b(data).hexdigest()
        
        return URTHash(
            algorithm=algorithm,
            value=hash_value,
            original_size=len(data)
        )


@dataclass
class URTMetadata:
    """META Token - Clasificación y contexto"""
    name: str
    description: Optional[str] = None
    tags: List[str] = None
    owner: Optional[str] = None
    created_at: Optional[str] = None
    expires_at: Optional[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.created_at is None:
            self.created_at = datetime.utcnow().isoformat() + "Z"


@dataclass
class URTSignature:
    """SIG Token - Autenticación"""
    algorithm: SignatureAlgorithm
    value: str  # Firma en base64
    public_key: str  # Clave pública
    key_id: Optional[str] = None
    
    @staticmethod
    def placeholder(key_id: str = "key-001") -> 'URTSignature':
        """Crea una firma de placeholder para ejemplo"""
        return URTSignature(
            algorithm=SignatureAlgorithm.ECDSA,
            value="MEYCIQCl8zqb4xW4T...",  # Placeholder
            public_key="04a1f33a9be315b84f...",  # Placeholder
            key_id=key_id
        )


@dataclass
class URTLedger:
    """LEDGER Token - Registro distribuido"""
    ledger_id: str  # ULR-XXXXXXXX
    ledger_type: str
    timestamp: str
    merkle_proof: Optional[str] = None
    
    @staticmethod
    def generate(resource_id: str) -> 'URTLedger':
        """Genera registro en ledger"""
        random_hex = secrets.token_hex(4).upper()
        return URTLedger(
            ledger_id=f"ULR-{random_hex}",
            ledger_type="IPFS",
            timestamp=datetime.utcnow().isoformat() + "Z"
        )


@dataclass
class URTBlockchain:
    """CHAIN Token - Anclaje blockchain"""
    network: BlockchainNetwork = BlockchainNetwork.NONE
    transaction_hash: Optional[str] = None
    block_number: Optional[int] = None
    confirmation_count: int = 0
    contract_address: Optional[str] = None


@dataclass
class URTURN:
    """URN Token - Referencia global única (RFC 8141)"""
    value: str  # urn:resource:namespace:RID
    resolver: Optional[str] = None
    
    @staticmethod
    def generate(namespace: str, rid: str) -> 'URTURN':
        """Genera URN global único"""
        # Extraer solo el ID sin el prefijo RID-
        rid_value = rid.replace("RID-", "")
        return URTURN(
            value=f"urn:resource:{namespace}:{rid_value}",
            resolver=f"https://resolver.fuente.io/urn/"
        )


class UniversalResourceToken:
    """
    Universal Resource Token (URT) - Token criptográfico que representa
    un recurso verificable con identidad, integridad, autenticidad y trazabilidad
    """
    
    VERSION = "1.0.0"
    
    def __init__(
        self,
        data: bytes,
        name: str,
        resource_type: ResourceType,
        namespace: str = "fuente",
        owner: Optional[str] = None,
        description: Optional[str] = None,
        tags: List[str] = None,
    ):
        """
        Crea un nuevo Universal Resource Token
        
        Args:
            data: Contenido del recurso (bytes)
            name: Nombre descriptivo
            resource_type: Tipo de recurso
            namespace: Espacio de nombres del emisor
            owner: Propietario del recurso
            description: Descripción detallada
            tags: Lista de etiquetas
        """
        self.version = self.VERSION
        
        # Generar RID
        self.rid = URTIdentity.generate(namespace, resource_type)
        
        # Calcular hash
        self.hash = URTHash.from_data(data)
        
        # Metadatos
        self.metadata = URTMetadata(
            name=name,
            description=description,
            tags=tags or [],
            owner=owner or namespace
        )
        
        # Firma (placeholder - debe ser implementada con criptografía real)
        self.signature = URTSignature.placeholder()
        
        # Ledger distribuido
        self.ledger = URTLedger.generate(self.rid.id)
        
        # Blockchain (inicialmente sin ancla)
        self.blockchain = URTBlockchain()
        
        # URN global
        self.urn = URTURN.generate(namespace, self.rid.id)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el token a diccionario"""
        return {
            "version": self.version,
            "rid": {
                "id": self.rid.id,
                "type": self.rid.type.value,
                "namespace": self.rid.namespace
            },
            "hash": {
                "algorithm": self.hash.algorithm.value,
                "value": self.hash.value,
                "original_size": self.hash.original_size
            },
            "metadata": {
                "name": self.metadata.name,
                "description": self.metadata.description,
                "tags": self.metadata.tags,
                "owner": self.metadata.owner,
                "created_at": self.metadata.created_at,
                "expires_at": self.metadata.expires_at
            },
            "signature": {
                "algorithm": self.signature.algorithm.value,
                "value": self.signature.value,
                "public_key": self.signature.public_key,
                "key_id": self.signature.key_id
            },
            "ledger": {
                "ledger_id": self.ledger.ledger_id,
                "ledger_type": self.ledger.ledger_type,
                "timestamp": self.ledger.timestamp,
                "merkle_proof": self.ledger.merkle_proof
            },
            "blockchain": {
                "network": self.blockchain.network.value,
                "transaction_hash": self.blockchain.transaction_hash,
                "block_number": self.blockchain.block_number,
                "confirmation_count": self.blockchain.confirmation_count,
                "contract_address": self.blockchain.contract_address
            },
            "urn": {
                "value": self.urn.value,
                "resolver": self.urn.resolver
            }
        }
    
    def to_json(self, pretty: bool = True) -> str:
        """Serializa el token a JSON"""
        if pretty:
            return json.dumps(self.to_dict(), indent=2)
        return json.dumps(self.to_dict())
    
    def to_compact(self) -> str:
        """
        Formato compacto de URT
        URT-RID-HASH-META-SIG-LEDGER-CHAIN-URN
        """
        rid = self.rid.id
        hash_short = self.hash.value[:16]
        meta = self.metadata.name[:8].upper().replace(" ", "_")
        sig = self.signature.value[:8]
        ledger = self.ledger.ledger_id
        chain = self.blockchain.network.value[:3]
        urn = self.urn.value
        
        return f"URT-{rid}-{hash_short}-{meta}-{sig}-{ledger}-{chain}-{urn}"
    
    def anchor_to_blockchain(
        self,
        network: BlockchainNetwork,
        tx_hash: str,
        block_number: int
    ) -> None:
        """Ancla el token a una blockchain"""
        self.blockchain.network = network
        self.blockchain.transaction_hash = tx_hash
        self.blockchain.block_number = block_number
        self.blockchain.confirmation_count = 1
    
    def add_merkle_proof(self, proof: str) -> None:
        """Agrega prueba de Merkle al ledger"""
        self.ledger.merkle_proof = proof
    
    def set_expiration(self, days: int) -> None:
        """Establece fecha de expiración"""
        expiry = datetime.utcnow() + timedelta(days=days)
        self.metadata.expires_at = expiry.isoformat() + "Z"
    
    def is_expired(self) -> bool:
        """Verifica si el token ha expirado"""
        if not self.metadata.expires_at:
            return False
        expires = datetime.fromisoformat(self.metadata.expires_at.replace("Z", "+00:00"))
        return datetime.utcnow() > expires.replace(tzinfo=None)
    
    @staticmethod
    def from_json(json_str: str) -> 'UniversalResourceToken':
        """Deserializa un token desde JSON"""
        data = json.loads(json_str)
        
        # Crear token básico (requiere datos de referencia)
        urt = UniversalResourceToken(
            data=b"",  # Placeholder
            name=data["metadata"]["name"],
            resource_type=ResourceType[data["rid"]["type"].upper()],
            namespace=data["rid"]["namespace"],
            owner=data["metadata"]["owner"],
            description=data["metadata"]["description"],
            tags=data["metadata"]["tags"]
        )
        
        # Restaurar componentes
        urt.version = data["version"]
        
        return urt


# Ejemplo de uso
if __name__ == "__main__":
    # Crear un token URT
    recurso = b"Este es un documento importante que debe ser verificable"
    
    urt = UniversalResourceToken(
        data=recurso,
        name="Certificado Digital",
        resource_type=ResourceType.CERTIFICATE,
        namespace="fuente",
        owner="usuario@fuente.io",
        description="Certificado de logros académicos",
        tags=["educacion", "verificable", "diploma"]
    )
    
    # Mostrar representación JSON
    print("=== Universal Resource Token (URT) ===\n")
    print(urt.to_json())
    
    # Formato compacto
    print("\n=== Formato Compacto ===")
    print(urt.to_compact())
    
    # Anclar a blockchain
    urt.anchor_to_blockchain(
        BlockchainNetwork.ETHEREUM,
        "0x123abc456def789...",
        19200000
    )
    
    print("\n=== Con Anclaje Blockchain ===")
    print(json.dumps(urt.to_dict()["blockchain"], indent=2))
