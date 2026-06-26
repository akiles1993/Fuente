# Fuente Protocol - Setup Completo

## Requisitos del Sistema

- Python 3.8+
- Node.js 16+
- npm o yarn
- Git

## Instalación Rápida

### 1. Clonar repositorio

```bash
git clone https://github.com/akiles1993/Fuente.git
cd Fuente
```

### 2. Ejecutar script de setup

```bash
chmod +x run.sh
./run.sh
```

Esto instalará todas las dependencias e iniciará:
- ✓ Backend API (Puerto 8000)
- ✓ Frontend React (Puerto 3000)

## Acceso

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Estructura del Proyecto

```
Fuente/
├── core/
│   └── urt.py                 # Implementación core de URT
├── contracts/
│   └── URTToken.sol           # Smart contracts Solidity
├── tests/
│   ├── test_urt.py            # Tests unitarios
│   └── test_contracts.py      # Tests de contratos
├── examples/
│   ├── basic_token.py         # Ejemplo básico
│   ├── blockchain_anchor.py   # Anclaje blockchain
│   └── distributed_ledger.py  # Ledger distribuido
├── api/
│   ├── backend.py             # API REST FastAPI
│   ├── config.py              # Configuración
│   └── requirements.txt        # Dependencias Python
├── frontend/
│   ├── src/
│   │   ├── components/        # Componentes React
│   │   ├── services/          # Servicios API y Web3
│   │   └── App.jsx            # App principal
│   └── package.json           # Dependencias Node
├── spec/
│   └── URT-v1.0.json          # Especificación
├── TOKENOMICS.md              # Economía del token
├── WHITEPAPER.md              # Documento técnico
├── ROADMAP.md                 # Plan de desarrollo
├── GOVERNANCE.md              # Estructura DAO
├── SECURITY.md                # Política de seguridad
└── DEPLOYMENT.md              # Guía de deployment
```

## Flujo de Desarrollo

### 1. Crear un Token URT

```bash
python3 examples/basic_token.py
```

### 2. Ejecutar Tests

```bash
# Tests Python
pytest tests/test_urt.py -v

# Tests contratos
pytest tests/test_contracts.py -v
```

### 3. Usar API REST

```bash
# Crear token
curl -X POST http://localhost:8000/tokens \
  -H "Content-Type: application/json" \
  -d '{
    "data": "SGVsbG8gV29ybGQ=",
    "name": "Mi Token",
    "resource_type": "certificate"
  }'

# Obtener token
curl http://localhost:8000/tokens/RID-XXXXXXXX

# Verificar token
curl -X POST http://localhost:8000/tokens/RID-XXXXXXXX/verify
```

### 4. Interfaz Web

Acceder a http://localhost:3000 en navegador

## Variables de Entorno

### Backend (.env)

```bash
DATABASE_URL=postgresql://user:password@localhost/fuente
ETHERSCAN_API_KEY=your_key
INFURA_API_KEY=your_key
URT_TOKEN_ADDRESS=0x...
```

### Frontend (.env)

```bash
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WEB3_PROVIDER=https://mainnet.infura.io/v3/KEY
```

## Deployment

Ver `DEPLOYMENT.md` para:
- Testnet (Sepolia)
- Mainnet Ethereum
- Polygon
- Configuración de liquidez DEX

## Testing

```bash
# Cobertura completa
pytest tests/ --cov=core --cov-report=html

# Tests específicos
pytest tests/test_urt.py::TestURTIdentity -v
```

## Documentación

- [Whitepaper](WHITEPAPER.md) - Especificación técnica completa
- [Tokenomics](TOKENOMICS.md) - Economía del token
- [Roadmap](ROADMAP.md) - Plan de desarrollo
- [Governance](GOVERNANCE.md) - Estructura DAO
- [Security](SECURITY.md) - Política de seguridad
- [Deployment](DEPLOYMENT.md) - Guía de deployment

## Comunidad

- GitHub: https://github.com/akiles1993/Fuente
- Twitter: @FuenteProtocol
- Discord: https://discord.gg/fuente
- Email: support@fuente.io

## Licencia

MIT License - Protocolo abierto para uso global

## Contribuir

1. Fork el repositorio
2. Crear rama: `git checkout -b feature/AmazingFeature`
3. Commit cambios: `git commit -m 'Add AmazingFeature'`
4. Push rama: `git push origin feature/AmazingFeature`
5. Abrir Pull Request

---

**Hecho con ❤️ para la comunidad blockchain**

*Última actualización: Junio 26, 2026*
