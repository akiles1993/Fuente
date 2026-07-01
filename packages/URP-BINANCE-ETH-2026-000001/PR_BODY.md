### URP-BINANCE-ETH-2026-000001 - Universal Resource Package

This PR adds a Universal Resource Package (URP) for the Binance Ethereum address registry. The package is designed as a portable, verifiable resource bundle following the URP-3.0 conceptual schema.

Files added under packages/URP-BINANCE-ETH-2026-000001/
- manifest.json
- ledger/resource_ledger.json
- registry/binance_addresses.json
- cryptography/checksums.json
- cryptography/merkle_root.hash
- cryptography/verification.json
- cryptography/public_key.pem
- tokens/resource_token.json
- README.txt

Verification and next steps
1. The manifest and package hashes, Merkle root and signature were generated locally; private key was NOT uploaded. Public key and signature are in cryptography/verification.json and cryptography/public_key.pem.
2. Recommended: verify signature locally with standard ECDSA-secp256k1 tools and optionally anchor package_hash on blockchain.
3. If you want the private key exported, request it separately via a secure channel.

