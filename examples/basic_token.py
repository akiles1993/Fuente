#!/usr/bin/env python3
"""
Ejemplo básico: Crear un Universal Resource Token
"""

import json
import sys
sys.path.insert(0, '../core')

from urt import (
    UniversalResourceToken,
    ResourceType,
    BlockchainNetwork
)


def main():
    print("=" * 70)
    print("EJEMPLO 1: Crear un Token URT Básico")
    print("=" * 70)
    
    # ============================================
    # 1. Crear un recurso (en este caso, texto)
    # ============================================
    documento = b"""
    CERTIFICADO DE LOGRO
    
    Se certifica que Juan Pérez ha completado exitosamente
    el curso "Criptografía Aplicada" con una calificación
    de Excelente.
    
    Emitido el 26 de junio de 2026
    Institución: Universidad Digital
    """
    
    # ============================================
    # 2. Crear el token URT
    # ============================================
    urt = UniversalResourceToken(
        data=documento,
        name="Certificado de Logro Académico",
        resource_type=ResourceType.CERTIFICATE,
        namespace="universidad-digital",
        owner="juan.perez@email.com",
        description="Certificado de finalización de curso de criptografía",
        tags=["educacion", "certificado", "criptografia", "blockchain"]
    )
    
    # ============================================
    # 3. Mostrar el token en JSON completo
    # ============================================
    print("\n1. REPRESENTACIÓN JSON COMPLETA:")
    print("-" * 70)
    print(urt.to_json())
    
    # ============================================
    # 4. Mostrar formato compacto
    # ============================================
    print("\n2. FORMATO COMPACTO:")
    print("-" * 70)
    compact = urt.to_compact()
    print(compact)
    
    # ============================================
    # 5. Acceder a componentes individuales
    # ============================================
    print("\n3. COMPONENTES DEL TOKEN:")
    print("-" * 70)
    print(f"RID (Resource ID):        {urt.rid.id}")
    print(f"Tipo de Recurso:          {urt.rid.type.value}")
    print(f"Namespace:                {urt.rid.namespace}")
    print(f"")
    print(f"Hash (Integridad):        {urt.hash.value[:32]}...")
    print(f"Algoritmo:                {urt.hash.algorithm.value}")
    print(f"Tamaño Original:          {urt.hash.original_size} bytes")
    print(f"")
    print(f"Firma:                    {urt.signature.algorithm.value}")
    print(f"Clave Pública:            {urt.signature.public_key[:32]}...")
    print(f"")
    print(f"Ledger ID:                {urt.ledger.ledger_id}")
    print(f"Tipo de Ledger:           {urt.ledger.ledger_type}")
    print(f"")
    print(f"URN Global:               {urt.urn.value}")
    
    # ============================================
    # 6. Anclar a blockchain
    # ============================================
    print("\n4. ANCLAJE A BLOCKCHAIN:")
    print("-" * 70)
    urt.anchor_to_blockchain(
        network=BlockchainNetwork.ETHEREUM,
        tx_hash="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        block_number=19500000
    )
    print(f"Network:                  {urt.blockchain.network.value}")
    print(f"Transaction Hash:         {urt.blockchain.transaction_hash[:32]}...")
    print(f"Block Number:             {urt.blockchain.block_number}")
    print(f"Confirmations:            {urt.blockchain.confirmation_count}")
    
    # ============================================
    # 7. Agregar prueba de Merkle
    # ============================================
    print("\n5. MERKLE PROOF:")
    print("-" * 70)
    urt.add_merkle_proof("0x9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f")
    print(f"Merkle Proof:             {urt.ledger.merkle_proof[:32]}...")
    
    # ============================================
    # 8. Establecer expiración
    # ============================================
    print("\n6. EXPIRACIÓN:")
    print("-" * 70)
    urt.set_expiration(days=365)
    print(f"Expira el:                {urt.metadata.expires_at}")
    print(f"¿Expirado?:               {urt.is_expired()}")
    
    # ============================================
    # 9. Guardar en archivo JSON
    # ============================================
    print("\n7. GUARDANDO EN ARCHIVO:")
    print("-" * 70)
    filename = f"token_{urt.rid.id}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(urt.to_json())
    print(f"✓ Token guardado en: {filename}")
    
    # ============================================
    # 10. Resumen ejecutivo
    # ============================================
    print("\n8. RESUMEN EJECUTIVO:")
    print("-" * 70)
    print(f"""
    ┌─────────────────────────────────────────────────┐
    │ UNIVERSAL RESOURCE TOKEN (URT)                  │
    ├─────────────────────────────────────────────────┤
    │ Versión:              {urt.version:<30} │
    │ Nombre:               {urt.metadata.name:<30} │
    │ RID:                  {urt.rid.id:<30} │
    │ URN:                  {urt.urn.value:<30} │
    │ Hash:                 {urt.hash.value[:25]}... │
    │ Algoritmo Firma:      {urt.signature.algorithm.value:<30} │
    │ Red Blockchain:       {urt.blockchain.network.value:<30} │
    │ Ledger:               {urt.ledger.ledger_id:<30} │
    │ Propietario:          {urt.metadata.owner:<30} │
    │ Creado:               {urt.metadata.created_at:<30} │
    │ Expira:               {urt.metadata.expires_at:<30} │
    └─────────────────────────────────────────────────┘
    """)


if __name__ == "__main__":
    main()
