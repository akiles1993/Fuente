# URT Token Tokenomics

## Visión General

El **URT Token** (Universal Resource Token) es una criptomoneda diseñada para incentivar la creación, verificación y uso de recursos digitales verificables en la red Fuente.

## Suministro Total

```
Total Supply (TS):      1,000,000,000 URT
Decimals:               18
Smallest Unit:          1 Wei (0.000000000000000001 URT)
```

## Distribución de Token

### 1. Asignación Inicial (100% = 1B URT)

| Categoría | % | Cantidad | Descripción |
|-----------|---|----------|-------------|
| **Minería/Rewards** | 30% | 300,000,000 | Incentivos para validadores y creadores de tokens |
| **Equipo Fundador** | 15% | 150,000,000 | (20% bloqueados por 2 años, luego liberación lineal) |
| **Tesoro del Protocolo** | 20% | 200,000,000 | Desarrollo, marketing, operaciones |
| **Investors/VC** | 15% | 150,000,000 | (Vesting 12 meses con cliff de 3 meses) |
| **Comunidad/Airdrop** | 12% | 120,000,000 | Distribución comunitaria |
| **Liquidez Inicial** | 8% | 80,000,000 | DEX, AMM liquidity pools |

## Mecánicas de Generación de Valor

### 1. **Minería de Recursos (Resource Mining)**

Los usuarios ganan URT al crear y verificar tokens URT:

```python
Reward Base = 10 URT por token verificado
Multiplicadores:
  - Tipo de recurso: 0.5x - 2.0x
  - Antigüedad: +5% por año (máx 50%)
  - Verificaciones adicionales: +10% por verificador

Ejemplo:
  Token de Diploma (2.0x) + 1 año antigüedad (5%) = 10 * 2.0 * 1.05 = 21 URT
```

### 2. **Staking de Validadores**

```
Staking Mínimo:         1,000 URT
APY (Annual Percentage Yield): 8-15% (según cantidad stakeada)
Lockup Period:          30 días (pueden hacer unstaking pero con penalidad)
Penalidad Early Unstaking: -5% de rewards
```

### 3. **Gobernanza de Protocolo**

```
URT holders pueden:
  - Votar en propuestas de mejora del protocolo
  - Decidir sobre asignación de fondos de tesorería
  - Proponer nuevos tipos de recursos certificables
  - Modificar parámetros de recompensa

Voto Cuadrado (Quadratic Voting):
  - Costo de voto: número_votos^2 URT
  - Previene captura por ballenas
```

### 4. **Transacciones de Recursos**

```
Fee por transacción de token URT: 0.1% - 0.5%
  - 50% quemado (deflationary)
  - 50% a validadores

Fee por transferencia de recurso verificado: 0.05%
```

## Schedule de Vesting

### Equipo Fundador
```
Año 1: 0% (completamente bloqueado)
Año 2: 0% (completamente bloqueado)
Año 3-4: Liberación lineal mensual 4.17% del total
Año 5: Completamente desbloqueado

Total desbloqueado después de 5 años: 150,000,000 URT
```

### Inversores/VC
```
Cliff: 3 meses (sin desbloques)
Vesting: 12 meses total
  - Mes 4-16: 8.33% mensual
Total desbloqueado después de 16 meses: 150,000,000 URT
```

## Inflación y Deflación

### Inflación (Mint Events)

```
Año 1:  +3% anual (30M URT nuevos)
Año 2:  +2% anual (20M URT nuevos)
Año 3+: +1% anual (10M URT nuevos)

Cap máximo: Después de 10 años, emisión se estabiliza en 10M/año
```

### Deflación (Burn Events)

```
- 50% de fees de transacción
- Penalidades por comportamiento malicioso
- Rewards no reclamados después de 1 año
- Objetivo: Reducir 0.5% anual después del año 5
```

## Casos de Uso del Token

### 1. **Pago por Verificación**
```
Verificador recibe URT por validar nuevos recursos:
  - Diploma: 20 URT
  - Contrato: 30 URT
  - Activo Digital: 50 URT
  - Credencial: 25 URT
```

### 2. **Almacenamiento de Recursos**
```
Premio mensual por almacenar en ledger:
  - 1-100 recursos: Gratis
  - 101-1000 recursos: 10 URT/mes
  - 1001+ recursos: 50 URT/mes
```

### 3. **Acceso a Servicios Premium**
```
- API Enterprise: 1,000 URT/mes
- Verificación acelerada: 100 URT/token
- Anclaje blockchain garantizado: 50 URT
```

### 4. **Incentivos de Liquidez**
```
Proveedores de liquidez reciben:
  - LP Fees: 0.3% del volumen
  - URT Rewards: 50,000 URT/mes distribuidos
  - Boost multiplicador: 1x-2.5x según tiempo de lock
```

## Economía de Red

### Previsión de Usuarios

```
Año 1:  10,000 usuarios → ~100K tokens registrados
Año 2:  100,000 usuarios → ~1M tokens registrados
Año 3:  500,000 usuarios → ~5M tokens registrados
Año 5:  2,000,000 usuarios → ~20M tokens registrados
```

### Volumen de Transacciones Esperado

```
Año 1: $5M USD
Año 2: $50M USD
Año 3: $200M USD
Año 5: $1B+ USD
```

## Liquidez y Exchange

### DEX Listings

```
Fase 1 (Mes 1): Uniswap V3, QuickSwap (Polygon)
Fase 2 (Mes 3): Curve Finance, Aave
Fase 3 (Mes 6): Centralized Exchanges (Binance, Coinbase)
```

### Pair Inicial

```
URT/USDC: 80,000,000 URT + $8M USDC (80M iniciales)
URT/ETH: 20,000,000 URT + 5,000 ETH (otros 20M)
```

## Seguridad y Protecciones

### Anti-Whale Measures

```
Tx Limit por bloque: Máximo 0.1% del total supply
Slippage mínimo: 0.5%
Rate limit: 10 transacciones grandes por hora
```

### Price Floor

```
Si precio cae 50% en 7 días:
  - Quema automática de 1M URT
  - Activación de "Circuit Breaker" (pausa de 24h)
```

## Gobernanza de Recompensas

### DAO (Decentralized Autonomous Organization)

```
Votación para ajustar:
  - Tasas de staking APY
  - Recompensas de minería
  - Fees de transacción
  - Nuevos tipos de recursos
  - Estrategia de tesorería

Quórum: Mínimo 10% de votantes participando
Aprobación: >50% en favor
```

## Hoja de Ruta de Tokenomics

### Q3 2026 (Año 1)
- Launch token en testnet
- Distribución de airdrop comunitario
- Listar en DEX

### Q4 2026
- Mining rewards activo
- Staking funcional
- Integración con recursos

### Q1 2027
- Listado en CEX
- DAO gobernanza activa
- 100K usuarios objetivo

### Q2-Q4 2027
- Expansión de protocolos integrados
- 500K usuarios objetivo
- $200M volumen anual

## Disclaimer

Esta tokenomía es propuesta inicial y puede ser modificada por votación de la comunidad. Las proyecciones son estimativas y están sujetas a cambios en el mercado.
