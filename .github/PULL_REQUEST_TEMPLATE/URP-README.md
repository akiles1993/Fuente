feat(urp): add URP-BINANCE-ETH-2026-000001 universal resource package

This PR adds a Universal Resource Package (URP) for the Binance Ethereum address registry. The package is designed as a portable, verifiable resource bundle following the URP-3.0 conceptual schema.

Files added under packages/URP-BINANCE-ETH-2026-000001/
- manifest.json
- ledger/resource_ledger.json
- registry/binance_addresses.json
- cryptography/verification.json
- tokens/resource_token.json
- README.txt

Recommended next steps:
1. Calculate SHA-256 for manifest.json and the package ZIP and populate manifest.integrity fields.
2. Generate checksums for all files and compute a Merkle root; populate cryptography/merkle_root and manifest.integrity.merkle_root.
3. Sign the manifest (ECDSA-secp256k1) and add public_key and signature to cryptography/verification.json.
4. (Optional) Anchor the package_hash on a public blockchain and add txid to manifest.anchor.

If you want me to also generate keys, Merkle root and package ZIP automatically, I can do that next.
