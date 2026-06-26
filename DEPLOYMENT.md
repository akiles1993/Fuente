# Guía de Deployment - URT Token

## Requisitos Previos

```bash
# Node.js y npm
node --version  # v18.0.0 o superior
npm --version   # v9.0.0 o superior

# Solidity compiler
npm install -g hardhat

# Git
git --version
```

## 1. Instalación del Entorno de Desarrollo

### 1.1 Clonar repositorio

```bash
git clone https://github.com/akiles1993/Fuente.git
cd Fuente
```

### 1.2 Instalar dependencias

```bash
npm install
pip install -r requirements.txt
```

### 1.3 Configurar variables de entorno

```bash
cp .env.example .env

# Editar .env con:
PRIVATE_KEY=tu_clave_privada_aqui
INFURA_API_KEY=tu_infura_key
ETHERSCAN_API_KEY=tu_etherscan_key
```

## 2. Compilar Smart Contracts

```bash
cd contracts
hardhat compile
```

Salida esperada:
```
Compiled 2 Solidity files successfully
✓ URTToken.sol
✓ URTFactory.sol
```

## 3. Testing en Red Local

### 3.1 Iniciar Hardhat Network

```bash
hardhat node
```

### 3.2 Ejecutar tests (en otra terminal)

```bash
hardhat test

# Salida esperada:
# ✓ URTToken
#   ✓ Deployment (123ms)
#   ✓ Transfer tokens (89ms)
#   ✓ Issue UR Token (156ms)
#   ✓ Verify UR Token (95ms)
# ✓ URTFactory
#   ✓ Create URT Token (110ms)
#   ✓ Get token count (45ms)
```

## 4. Deploy en Testnet (Sepolia)

### 4.1 Obtener ETH de testnet

Visita https://sepoliafaucet.com/ y obtén 0.5 ETH

### 4.2 Desplegar contrato

```bash
hardhat run scripts/deploy.js --network sepolia
```

Salida:
```
Deploying URTToken with initial supply of 1,000,000,000...
URTToken deployed to: 0x1234567890123456789012345678901234567890
Deploying URTFactory...
URTFactory deployed to: 0x0987654321098765432109876543210987654321
```

### 4.3 Verificar en Etherscan

```bash
hardhat verify --network sepolia 0x1234567890123456789012345678901234567890 "1000000000"
```

## 5. Deploy en Mainnet Ethereum

### 5.1 Preparar deployment

```bash
# Asegurar que tienes suficiente ETH en cartera
# Estimar gas:
hardhat gas-report
```

### 5.2 Desplegar

```bash
hardhat run scripts/deploy.js --network mainnet
```

### 5.3 Verificación

```bash
hardhat verify --network mainnet <CONTRACT_ADDRESS> "<CONSTRUCTOR_ARGS>"
```

## 6. Deploy en Polygon

```bash
# Configurar en hardhat.config.js
polygon: {
  url: process.env.POLYGON_RPC_URL,
  accounts: [process.env.PRIVATE_KEY]
}

# Desplegar
hardhat run scripts/deploy.js --network polygon
```

## 7. Configurar DEX Liquidity

### 7.1 Uniswap V3 (Ethereum)

```javascript
// scripts/add-liquidity.js
const uniswapRouter = new ethers.Contract(
  UNISWAP_ROUTER_ADDRESS,
  uniswapABI,
  signer
);

await uniswapRouter.addLiquidity(
  URT_ADDRESS,
  USDC_ADDRESS,
  ethers.parseEther("80000000"),  // 80M URT
  ethers.parseUnits("8000000", 6), // 8M USDC
  0,
  0,
  signer.address,
  Math.floor(Date.now() / 1000) + 60 * 20
);
```

### 7.2 Ejecutar

```bash
hardhat run scripts/add-liquidity.js --network mainnet
```

## 8. Configurar Governance DAO

### 8.1 Desplegar contratos de gobernanza

```bash
hardhat run scripts/deploy-dao.js --network mainnet
```

### 8.2 Configurar parámetros

```javascript
// Voting delay: 1 bloque
// Voting period: 50,000 bloques (~1 semana)
// Proposal threshold: 100,000 URT
```

## 9. Monitoreo y Mantenimiento

### 9.1 Configurar alertas

```bash
# Usando OpenZeppelin Defender
npm install @openzeppelin/defender-sdk
```

### 9.2 Verificar estado

```bash
node scripts/check-contract-status.js

# Output:
# Token name: Universal Resource Token
# Symbol: URT
# Total supply: 1,000,000,000
# Decimals: 18
# Owner: 0x...
# Paused: false
# Registry size: 1,234
```

## 10. Checklist Final de Deployment

- [ ] Código auditado por tercero
- [ ] Tests con 95%+ cobertura
- [ ] Gas optimizado
- [ ] Verificado en Etherscan
- [ ] Liquidez inicial en DEX
- [ ] DAO Governance funcional
- [ ] Frontend conectado
- [ ] Documentación actualizada
- [ ] Soporte técnico listo
- [ ] Plan de comunicación ejecutado

## Troubleshooting

### Error: "Insufficient balance"
```bash
# Solución: Obtener más ETH del faucet
```

### Error: "Nonce too high"
```bash
# Solución: Resetear nonce
node scripts/reset-nonce.js
```

### Contrato no verifica en Etherscan
```bash
# Asegurar constructor args están codificados correctamente
hardhat verify --network sepolia <ADDRESS> --constructor-args arguments.js
```

## Recursos

- [Hardhat Documentation](https://hardhat.org/)
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/)
- [Etherscan Verification](https://docs.etherscan.io/)
- [Uniswap V3 Docs](https://docs.uniswap.org/)

## Soporte

Escribe a: support@fuente.io
