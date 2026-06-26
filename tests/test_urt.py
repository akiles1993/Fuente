#!/usr/bin/env python3
"""
Test Suite para Universal Resource Token Protocol
Cobertura completa: unit, integration, security tests
"""

import pytest
import json
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '../core')

from urt import (
    UniversalResourceToken,
    ResourceType,
    HashAlgorithm,
    BlockchainNetwork,
    URTIdentity,
    URTHash,
    URTMetadata,
    URTSignature,
    URTLedger,
    URTURN
)


class TestURTIdentity:
    """Test RID Token generation"""
    
    def test_rid_generation(self):
        """Test que RID se genera correctamente"""
        rid = URTIdentity.generate("fuente", ResourceType.CERTIFICATE)
        
        assert rid.id.startswith("RID-")
        assert len(rid.id) == 12  # RID- + 8 hex chars
        assert rid.type == ResourceType.CERTIFICATE
        assert rid.namespace == "fuente"
    
    def test_rid_uniqueness(self):
        """Test que RIDs son únicos"""
        rids = set()
        for _ in range(1000):
            rid = URTIdentity.generate("fuente", ResourceType.CERTIFICATE)
            rids.add(rid.id)
        
        # Todas únicas
        assert len(rids) == 1000
    
    def test_rid_format_validation(self):
        """Test validación de formato RID"""
        rid = URTIdentity.generate("fuente", ResourceType.CERTIFICATE)
        
        # Verificar patrón
        import re
        pattern = r"^RID-[A-F0-9]{8}$"
        assert re.match(pattern, rid.id)


class TestURTHash:
    """Test HASH Token"""
    
    def test_hash_generation_sha256(self):
        """Test hash SHA-256"""
        data = b"Test document content"
        hash_token = URTHash.from_data(data, HashAlgorithm.SHA256)
        
        assert hash_token.algorithm == HashAlgorithm.SHA256
        assert len(hash_token.value) == 64  # SHA-256 = 64 hex chars
        assert hash_token.original_size == len(data)
    
    def test_hash_generation_sha512(self):
        """Test hash SHA-512"""
        data = b"Test document content"
        hash_token = URTHash.from_data(data, HashAlgorithm.SHA512)
        
        assert hash_token.algorithm == HashAlgorithm.SHA512
        assert len(hash_token.value) == 128  # SHA-512 = 128 hex chars
    
    def test_hash_deterministic(self):
        """Test que hash es determinístico"""
        data = b"Same content"
        hash1 = URTHash.from_data(data)
        hash2 = URTHash.from_data(data)
        
        assert hash1.value == hash2.value
    
    def test_hash_collision_resistance(self):
        """Test resistencia a colisiones"""
        data1 = b"Content 1"
        data2 = b"Content 2"
        
        hash1 = URTHash.from_data(data1)
        hash2 = URTHash.from_data(data2)
        
        assert hash1.value != hash2.value
    
    def test_hash_immutability(self):
        """Test que pequeño cambio = hash diferente"""
        data_original = b"Document content"
        data_modified = b"Document conteXt"  # Una letra cambiada
        
        hash_orig = URTHash.from_data(data_original)
        hash_mod = URTHash.from_data(data_modified)
        
        assert hash_orig.value != hash_mod.value


class TestURTMetadata:
    """Test META Token"""
    
    def test_metadata_creation(self):
        """Test creación de metadatos"""
        meta = URTMetadata(
            name="Test Certificate",
            description="A test certificate",
            tags=["test", "education"],
            owner="user@example.com"
        )
        
        assert meta.name == "Test Certificate"
        assert len(meta.tags) == 2
        assert meta.owner == "user@example.com"
        assert meta.created_at is not None
    
    def test_metadata_auto_timestamp(self):
        """Test que timestamp se crea automáticamente"""
        meta = URTMetadata(name="Test")
        
        # Parse ISO datetime
        dt = datetime.fromisoformat(meta.created_at.replace("Z", "+00:00"))
        now = datetime.now()
        
        # Dentro de 1 segundo
        assert abs((now - dt).total_seconds()) < 1


class TestUniversalResourceToken:
    """Test URT principal"""
    
    @pytest.fixture
    def sample_urt(self):
        """Fixture URT para tests"""
        data = b"Sample certificate document"
        return UniversalResourceToken(
            data=data,
            name="Test Certificate",
            resource_type=ResourceType.CERTIFICATE,
            namespace="fuente",
            owner="test@fuente.io",
            tags=["test", "blockchain"]
        )
    
    def test_urt_creation(self, sample_urt):
        """Test creación básica de URT"""
        assert sample_urt.rid.id.startswith("RID-")
        assert sample_urt.hash.value is not None
        assert sample_urt.metadata.name == "Test Certificate"
        assert sample_urt.urn.value.startswith("urn:resource:")
    
    def test_urt_to_dict(self, sample_urt):
        """Test serialización a diccionario"""
        token_dict = sample_urt.to_dict()
        
        assert "version" in token_dict
        assert "rid" in token_dict
        assert "hash" in token_dict
        assert "metadata" in token_dict
        assert "signature" in token_dict
        assert "ledger" in token_dict
        assert "blockchain" in token_dict
        assert "urn" in token_dict
    
    def test_urt_to_json(self, sample_urt):
        """Test serialización a JSON"""
        json_str = sample_urt.to_json(pretty=False)
        
        # Validar que es JSON válido
        parsed = json.loads(json_str)
        assert parsed["rid"]["id"].startswith("RID-")
    
    def test_urt_to_compact(self, sample_urt):
        """Test formato compacto"""
        compact = sample_urt.to_compact()
        
        assert compact.startswith("URT-RID-")
        assert "-" in compact  # Múltiples separadores
    
    def test_urt_expiration_setting(self, sample_urt):
        """Test establecer expiración"""
        sample_urt.set_expiration(days=365)
        
        assert sample_urt.metadata.expires_at is not None
        assert not sample_urt.is_expired()
    
    def test_urt_expiration_check(self):
        """Test verificación de expiración"""
        data = b"Test"
        urt = UniversalResourceToken(
            data=data,
            name="Expiring Token",
            resource_type=ResourceType.CREDENTIAL,
            namespace="fuente"
        )
        
        # Establecer expiración a ayer
        urt.metadata.expires_at = (datetime.utcnow() - timedelta(days=1)).isoformat() + "Z"
        
        assert urt.is_expired()
    
    def test_urt_blockchain_anchor(self, sample_urt):
        """Test anclaje a blockchain"""
        sample_urt.anchor_to_blockchain(
            BlockchainNetwork.ETHEREUM,
            "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            19500000
        )
        
        assert sample_urt.blockchain.network == BlockchainNetwork.ETHEREUM
        assert sample_urt.blockchain.transaction_hash is not None
        assert sample_urt.blockchain.block_number == 19500000
    
    def test_urt_merkle_proof(self, sample_urt):
        """Test agregar Merkle proof"""
        proof = "0x9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d"
        sample_urt.add_merkle_proof(proof)
        
        assert sample_urt.ledger.merkle_proof == proof


class TestURTIntegration:
    """Tests de integración"""
    
    def test_full_token_lifecycle(self):
        """Test ciclo de vida completo del token"""
        # 1. Crear
        data = b"Complete lifecycle test"
        urt = UniversalResourceToken(
            data=data,
            name="Full Lifecycle Token",
            resource_type=ResourceType.CERTIFICATE,
            namespace="fuente",
            owner="lifecycle@test.io",
            tags=["integration", "test"]
        )
        
        # 2. Verificar componentes
        assert urt.rid is not None
        assert urt.hash is not None
        
        # 3. Anclar a blockchain
        urt.anchor_to_blockchain(
            BlockchainNetwork.ETHEREUM,
            "0x" + "a" * 64,
            19500000
        )
        
        # 4. Agregar prueba
        urt.add_merkle_proof("0x" + "b" * 64)
        
        # 5. Establecer expiración
        urt.set_expiration(days=365)
        
        # 6. Serializar
        json_str = urt.to_json()
        token_dict = json.loads(json_str)
        
        # 7. Verificar todo está presente
        assert token_dict["rid"]["id"].startswith("RID-")
        assert token_dict["blockchain"]["network"] == "Ethereum"
        assert token_dict["ledger"]["merkle_proof"] is not None
        assert not urt.is_expired()
    
    def test_multiple_tokens_isolation(self):
        """Test que múltiples tokens no interfieren"""
        urt1 = UniversalResourceToken(
            b"Token 1",
            "Token One",
            ResourceType.CERTIFICATE,
            namespace="fuente"
        )
        
        urt2 = UniversalResourceToken(
            b"Token 2",
            "Token Two",
            ResourceType.CREDENTIAL,
            namespace="fuente"
        )
        
        # Verificar que son independientes
        assert urt1.rid.id != urt2.rid.id
        assert urt1.hash.value != urt2.hash.value
        assert urt1.metadata.name != urt2.metadata.name
    
    def test_json_deserialization(self):
        """Test deserialización de JSON"""
        data = b"Deserialize test"
        original = UniversalResourceToken(
            data=data,
            name="Deserialize Test",
            resource_type=ResourceType.DOCUMENT,
            namespace="fuente"
        )
        
        json_str = original.to_json()
        
        # Deserializar
        restored = UniversalResourceToken.from_json(json_str)
        
        # Verificar que metadatos coinciden
        assert restored.metadata.name == original.metadata.name
        assert restored.hash.value == original.hash.value


class TestURTSecurity:
    """Tests de seguridad"""
    
    def test_hash_tampering_detection(self):
        """Test detección de modificación de hash"""
        data = b"Important document"
        urt = UniversalResourceToken(
            data=data,
            name="Tamper Test",
            resource_type=ResourceType.DOCUMENT,
            namespace="fuente"
        )
        
        original_hash = urt.hash.value
        
        # Intentar modificar (simular)
        modified_data = b"Modified document"
        new_hash = URTHash.from_data(modified_data).value
        
        # Deberían ser diferentes
        assert original_hash != new_hash
    
    def test_rid_entropy(self):
        """Test que RID tiene suficiente entropía"""
        rids = []
        for _ in range(10000):
            rid = URTIdentity.generate("fuente", ResourceType.CERTIFICATE)
            rids.append(rid.id)
        
        # Todas únicas
        assert len(set(rids)) == 10000
        
        # Distribución de caracteres
        from collections import Counter
        all_chars = ''.join(rids)
        char_counts = Counter(all_chars)
        
        # Todos caracteres hex presente
        hex_chars = set('0123456789ABCDEF')
        present_chars = set(char_counts.keys()) - {'-'}
        assert hex_chars.issubset(present_chars)
    
    def test_urn_format_validation(self):
        """Test validación formato URN"""
        urn = URTURN.generate("fuente", "RID-A7CCC968")
        
        # Verificar formato
        assert urn.value.startswith("urn:resource:")
        assert "fuente" in urn.value
        assert "A7CCC968" in urn.value
    
    def test_large_data_handling(self):
        """Test manejo de datos grandes"""
        # 10 MB de datos
        large_data = b"x" * (10 * 1024 * 1024)
        
        urt = UniversalResourceToken(
            data=large_data,
            name="Large Data Token",
            resource_type=ResourceType.DATA_PACKAGE,
            namespace="fuente"
        )
        
        assert urt.hash.original_size == len(large_data)
        assert urt.hash.value is not None


class TestURTPerformance:
    """Tests de rendimiento"""
    
    def test_token_creation_speed(self):
        """Test velocidad de creación de token"""
        import time
        
        start = time.time()
        for _ in range(100):
            UniversalResourceToken(
                b"Test",
                "Token",
                ResourceType.CERTIFICATE,
                namespace="fuente"
            )
        elapsed = time.time() - start
        
        # Menos de 1 segundo para 100 tokens
        assert elapsed < 1.0
    
    def test_json_serialization_speed(self):
        """Test velocidad de serialización JSON"""
        import time
        
        urt = UniversalResourceToken(
            b"Test",
            "Token",
            ResourceType.CERTIFICATE,
            namespace="fuente"
        )
        
        start = time.time()
        for _ in range(1000):
            urt.to_json()
        elapsed = time.time() - start
        
        # Menos de 5 segundos para 1000 serializaciones
        assert elapsed < 5.0
    
    def test_hash_computation_speed(self):
        """Test velocidad de cálculo de hash"""
        import time
        
        data = b"x" * (1 * 1024 * 1024)  # 1 MB
        
        start = time.time()
        for _ in range(100):
            URTHash.from_data(data)
        elapsed = time.time() - start
        
        # 100 x 1MB hashes en < 10 segundos
        assert elapsed < 10.0


if __name__ == "__main__":
    # Ejecutar tests
    pytest.main([__file__, "-v", "--tb=short"])
