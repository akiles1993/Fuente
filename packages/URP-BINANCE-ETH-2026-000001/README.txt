Binance Ethereum Resource Package (URP-BINANCE-ETH-2026-000001)

Contenido:
- manifest.json
- ledger/resource_ledger.json
- registry/binance_addresses.json
- cryptography/verification.json
- tokens/resource_token.json

Instrucciones:
1. Calcular el hash del manifest.json y package.zip (SHA-256).
2. Generar Merkle root sobre checksums de archivos y rellenar cryptography/verification.json.
3. Firmar el manifest con ECDSA-secp256k1 y añadir public_key + signature.
4. (Opcional) Anclar el package_hash en blockchain pública y añadir txid en manifest.anchor.
