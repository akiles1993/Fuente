#!/usr/bin/env python3
"""
Configuracion de API Backend
Variables de entorno y configuración
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ============================================
# Database
# ============================================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost/fuente_db"
)

# ============================================
# Blockchain
# ============================================

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
INFURA_API_KEY = os.getenv("INFURA_API_KEY")
WEB3_PROVIDER = os.getenv(
    "WEB3_PROVIDER",
    f"https://mainnet.infura.io/v3/{INFURA_API_KEY}"
)

# Contratos
URT_TOKEN_ADDRESS = os.getenv(
    "URT_TOKEN_ADDRESS",
    "0x0000000000000000000000000000000000000000"
)
URT_FACTORY_ADDRESS = os.getenv(
    "URT_FACTORY_ADDRESS",
    "0x0000000000000000000000000000000000000000"
)

# ============================================
# API
# ============================================

API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
API_WORKERS = int(os.getenv("API_WORKERS", 4))

# CORS
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,http://localhost:8000"
).split(",")

# ============================================
# Security
# ============================================

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-prod")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ============================================
# Storage
# ============================================

IPFS_GATEWAY = os.getenv(
    "IPFS_GATEWAY",
    "https://gateway.pinata.cloud/ipfs"
)
ARWEAVE_GATEWAY = os.getenv(
    "ARWEAVE_GATEWAY",
    "https://arweave.net"
)

# ============================================
# Email
# ============================================

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# ============================================
# Logging
# ============================================

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/fuente.log")

print("""
╔════════════════════════════════════════╗
║  Fuente Protocol - Backend Config      ║
╠════════════════════════════════════════╣
║ API:       http://{}:{}
║ Database:  {}
║ IPFS:      {}
║ Network:   {}
╚════════════════════════════════════════╝
""".format(
    API_HOST,
    API_PORT,
    "PostgreSQL" if "postgresql" in DATABASE_URL else "SQLite",
    IPFS_GATEWAY[:30] + "...",
    "Mainnet" if "mainnet" in WEB3_PROVIDER else "Testnet"
))
