# Fuente - Universal Resource Token (URT) Protocol

Un protocolo de tokenización de recursos que integra criptografía, blockchain y estándares abiertos para crear activos digitales verificables e interoperables.

## Concepto Core

**URT (Universal Resource Token)** es un contenedor de información verificable que transforma cualquier recurso digital en un activo criptográficamente asegurado.

```
URT-RID-A7CCC968-HASH-META-SIG-LEDGER-CHAIN-URN
```

### Capas del Token

- **RID Token**: Identificador único del recurso
- **HASH Token**: Integridad criptográfica (SHA-256)
- **META Token**: Clasificación y metadatos del recurso
- **SIG Token**: Autenticación (ECDSA/EdDSA)
- **LEDGER Token**: Registro en ledger distribuido
- **CHAIN Token**: Anclaje en blockchain (Bitcoin/Ethereum)
- **URN Token**: Referencia URN global única

## Estructura del Proyecto

```
Fuente/
├── spec/
│   ├── URT-v1.0.json          # Especificación JSON de URT
│   └── URT-Standard.md         # Documento de estándar
├── core/
│   ├── urt.py                  # Implementación core en Python
│   ├── crypto.py               # Funciones criptográficas
│   └── blockchain.py           # Integración blockchain
├── contracts/
│   ├── URT.sol                 # Contrato Solidity para Ethereum
│   └── URTToken.sol            # Token ERC-20 basado en URT
├── examples/
│   ├── basic_token.py          # Ejemplo básico
│   ├── blockchain_anchor.py    # Anclaje blockchain
│   └── distributed_ledger.py   # Ledger distribuido
└── tests/
    ├── test_crypto.py          # Tests criptográficos
    └── test_urt.py             # Tests de tokens

```

## Características

✅ **Identidad Verificable**: Cada recurso tiene RID único + URN global
✅ **Integridad Garantizada**: Hash criptográfico inmutable
✅ **Autenticidad Comprobable**: Firma digital ECDSA/EdDSA
✅ **Trazabilidad Completa**: Registro en ledger distribuido
✅ **Anclaje Blockchain**: Verificación externa en redes públicas
✅ **Interoperabilidad**: Estándar abierto independiente de plataforma

## Roadmap

- [ ] v0.1: Especificación JSON y validación
- [ ] v0.2: Implementación core en Python
- [ ] v0.3: Integración Blockchain (Bitcoin/Ethereum)
- [ ] v0.4: Smart Contracts ERC-20/BEP-20
- [ ] v1.0: Lanzamiento de protocolo
- [ ] v1.1: APIs REST y SDKs
- [ ] v2.0: Mercado descentralizado (DEX)

## Licencia

MIT License - Protocolo abierto para uso global
