chore(cryptography): add checksums, merkle root and public key (private key not uploaded)

Generated artifacts:
- cryptography/checksums.json
- cryptography/merkle_root.hash
- cryptography/verification.json (updated with manifest/package hashes and signature)
- cryptography/public_key.pem (public key only)

Notes:
- The private key was generated locally and NOT uploaded to the repository.
- Signature was produced with the local private key and attached in verification.json. Verify signature with the public key in public_key.pem.
