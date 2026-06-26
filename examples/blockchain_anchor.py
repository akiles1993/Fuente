#!/usr/bin/env python3
"""
Ejemplo: Anclar URT Token a blockchain
Simula la integración con contratos inteligentes Ethereum
"""

import json
import sys
sys.path.insert(0, '../core')

from urt import (
    UniversalResourceToken,
    ResourceType,
    BlockchainNetwork
)


class BlockchainSimulator:
    """Simula interacciones con blockchain"""
    
    def __init__(self):
        self.anchored_tokens = []
        self.next_block = 19500000
    
    def anchor_urt_token(self, urt: UniversalResourceToken) -> dict:
        """Simula el anclaje de un token URT a Ethereum"""
        
        # Simular transacción
        tx_hash = self._generate_tx_hash(urt)
        block_number = self.next_block
        self.next_block += 1
        
        # Anclar a blockchain
        urt.anchor_to_blockchain(
            network=BlockchainNetwork.ETHEREUM,
            tx_hash=tx_hash,
            block_number=block_number
        )
        
        # Registrar
        self.anchored_tokens.append({
            'urt': urt,
            'tx_hash': tx_hash,
            'block_number': block_number,
            'timestamp': urt.ledger.timestamp
        })
        
        return {
            'success': True,
            'rid': urt.rid.id,
            'tx_hash': tx_hash,
            'block_number': block_number,
            'network': 'Ethereum'
        }
    
    def _generate_tx_hash(self, urt: UniversalResourceToken) -> str:
        """Genera un hash de transacción simulado"""
        # En realidad, esto sería el hash real de la transacción
        import hashlib
        data = f"{urt.rid.id}{urt.hash.value}".encode()
        return "0x" + hashlib.sha256(data).hexdigest()
    
    def verify_anchor(self, tx_hash: str) -> dict:
        """Verifica que un token esté anclado"""
        for token_data in self.anchored_tokens:
            if token_data['tx_hash'] == tx_hash:
                return {
                    'found': True,
                    'rid': token_data['urt'].rid.id,
                    'block_number': token_data['block_number'],
                    'confirmations': 12  # Simulado
                }
        return {'found': False}


def main():
    print("=" * 70)
    print("EJEMPLO 2: Anclar URT Token a Blockchain")
    print("=" * 70)
    
    # Crear simulador de blockchain
    blockchain = BlockchainSimulator()
    
    # ============================================
    # 1. Crear múltiples recursos
    # ============================================
    print("\n1. CREANDO TOKENS URT:")
    print("-" * 70)
    
    tokens = []
    resources = [
        {
            'name': 'Licencia de Conducir',
            'data': b'Licencia DL-2026-001 válida hasta 2031',
            'type': ResourceType.CREDENTIAL,
            'owner': 'juan@example.com'
        },
        {
            'name': 'Diploma Universitario',
            'data': b'Grado en Ingeniería en Sistemas - Universidad XYZ',
            'type': ResourceType.CERTIFICATE,
            'owner': 'maria@example.com'
        },
        {
            'name': 'Obra de Arte Digital',
            'data': b'Pintura Digital #001 - Autor: Carlos López',
            'type': ResourceType.NFT,
            'owner': 'carlos@example.com'
        }
    ]
    
    for resource in resources:
        urt = UniversalResourceToken(
            data=resource['data'],
            name=resource['name'],
            resource_type=resource['type'],
            namespace='fuente-registry',
            owner=resource['owner'],
            tags=['verified', 'blockchain-anchored']
        )
        tokens.append(urt)
        print(f"✓ {resource['name']:<30} -> {urt.rid.id}")
    
    # ============================================
    # 2. Anclar todos los tokens
    # ============================================
    print("\n2. ANCLANDO A BLOCKCHAIN:")
    print("-" * 70)
    
    for urt in tokens:
        result = blockchain.anchor_urt_token(urt)
        print(f"""
✓ Token anclado exitosamente:
  RID:           {result['rid']}
  TX Hash:       {result['tx_hash'][:16]}...
  Block:         {result['block_number']}
  Network:       {result['network']}
    """)
    
    # ============================================
    # 3. Verificar anclajes
    # ============================================
    print("\n3. VERIFICANDO ANCLAJES:")
    print("-" * 70)
    
    for token in tokens:
        verification = blockchain.verify_anchor(token.blockchain.transaction_hash)
        status = "✓ VERIFICADO" if verification['found'] else "✗ NO ENCONTRADO"
        print(f"""
{status}:
  RID:           {verification['rid']}
  Block:         {verification['block_number']}
  Confirmaciones: {verification.get('confirmations', 0)}
    """)
    
    # ============================================
    # 4. Mostrar detalles completos de un token anclado
    # ============================================
    print("\n4. DETALLES DEL TOKEN ANCLADO (Ejemplo):")
    print("-" * 70)
    
    urt_ejemplo = tokens[0]
    detalles = urt_ejemplo.to_dict()
    
    print(json.dumps(detalles, indent=2))
    
    # ============================================
    # 5. Cadena de custodia
    # ============================================
    print("\n5. CADENA DE CUSTODIA:")
    print("-" * 70)
    
    print(f"""
    Flujo de Verificación:
    
    1. RECURSO ORIGINAL
       └─> Datos: {len(tokens[0].hash.original_size)} bytes
    
    2. HASH CRIPTOGRÁFICO
       └─> Algoritmo: {tokens[0].hash.algorithm.value}
       └─> Hash: {tokens[0].hash.value[:32]}...
    
    3. FIRMA DIGITAL
       └─> Algoritmo: {tokens[0].signature.algorithm.value}
       └─> Key ID: {tokens[0].signature.key_id}
    
    4. REGISTRO DISTRIBUIDO
       └─> Ledger ID: {tokens[0].ledger.ledger_id}
       └─> Tipo: {tokens[0].ledger.ledger_type}
    
    5. ANCLAJE BLOCKCHAIN
       └─> Network: {tokens[0].blockchain.network.value}
       └─> TX: {tokens[0].blockchain.transaction_hash[:16]}...
       └─> Block: {tokens[0].blockchain.block_number}
    
    6. REFERENCIA GLOBAL
       └─> URN: {tokens[0].urn.value}
       └─> Resolver: {tokens[0].urn.resolver}
    
    RESULTADO: Token verificable en cadena inmutable
    """)
    
    # ============================================
    # 6. Estadísticas de blockchain
    # ============================================
    print("\n6. ESTADÍSTICAS BLOCKCHAIN:")
    print("-" * 70)
    
    print(f"""
    Total de tokens anclados:      {len(blockchain.anchored_tokens)}
    Rango de bloques:              {19500000} - {blockchain.next_block - 1}
    Red blockchain:                Ethereum
    Confirmaciones promedio:       12
    
    Tokens registrados:
    """)
    
    for i, token_data in enumerate(blockchain.anchored_tokens, 1):
        urt = token_data['urt']
        print(f"    {i}. {urt.metadata.name:<30} [{urt.rid.id}]")


if __name__ == "__main__":
    main()
