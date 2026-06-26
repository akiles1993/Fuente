# Governance Framework - Fuente Protocol

## 1. Estructura de Gobernanza

### 1.1 Pilares

```
┌─────────────────────────────────────────┐
│    FUENTE PROTOCOL GOVERNANCE          │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────┐│
│  │ Comunidad│  │ Tesorería│  │ Técnico││
│  │   (DAO)  │  │ (Multi)  │  │ (Core)││
│  └──────────┘  └──────────┘  └──────┘│
│                                         │
└─────────────────────────────────────────┘
```

## 2. DAO Governance

### 2.1 Votación Cuadrada (Quadratic Voting)

```
Costo de voto = (número_votos)^2

Ejemplos:
1 voto = 1 URT
2 votos = 4 URT
3 votos = 9 URT
5 votos = 25 URT
10 votos = 100 URT
```

**Ventajas**:
- Previene captura por ballenas
- Da poder a la mayoría
- Incentiva participación honesta

### 2.2 Tipos de Propuestas

#### Propuestas Técnicas (TCP - Technical Change Proposal)
- Cambios de protocolo
- Nuevos tipos de recursos
- Actualizaciones de contratos
- Quórum: 10%
- Aprobación: >66%

#### Propuestas de Tesorería (TrP - Treasury Proposal)
- Asignación de fondos
- Presupuesto de marketing
- Programas de incentivos
- Quórum: 5%
- Aprobación: >50%

#### Propuestas de Gobernanza (GP - Governance Proposal)
- Cambios en el proceso de votación
- Modificaciones del DAO
- Parámetros de consenso
- Quórum: 15%
- Aprobación: >75%

### 2.3 Proceso de Votación

```
1. PROPUESTA
   └─ Autor publica en GitHub (RFC)
   └─ Comunidad discute (5 días)
   
2. PRESENTACIÓN FORMAL
   └─ Propuesta en cadena
   └─ Snapshot votación (2 días)
   
3. VOTACIÓN ONCHAIN
   └─ Voting delay: 1 bloque
   └─ Voting period: 50,000 bloques (~1 semana)
   └─ Voting mechanism: Quadratic
   
4. EJECUCIÓN
   └─ Timelock: 2 días
   └─ Implementación automática
```

### 2.4 Requisitos de Participación

```
Votante mínimo: 1,000 URT
Proponent mínimo: 100,000 URT
Fee de propuesta: 10 URT (quemado)
Votación por delegación: Permitida
```

## 3. Tesorería Multisig

### 3.1 Estructura

```
Tesorería Principal: 200,000,000 URT
├─ 2/3 Multisig Core Team (3 de 5)
├─ 2/5 Multisig Comunidad (2 de 3)
└─ Requerimientos: Ambos
```

### 3.2 Signatarios Core Team

- CEO Protocol
- CTO Technical
- CFO Finance
- (2 rotados anualmente)

### 3.3 Signatarios Comunidad

- Top DAO contributor
- Community manager
- (1 rotado cada 6 meses)

### 3.4 Límites de Transacción

```
Diario:    < $1M USD
Semanal:   < $10M USD
Mensual:   < $50M USD
Anual:     < $500M USD

Por encima de límites: Requiere votación
```

## 4. Comités Técnicos

### 4.1 Core Developers

**Responsabilidades**:
- Revisión de código
- Auditoría de cambios
- Mantenimiento de infraestructura
- Respuesta a seguridad

**Requisitos**:
- 2+ años experiencia blockchain
- Contribuciones verificadas
- Aprobación DAO

**Compensación**:
- 100k-300k URT/año
- + bonus de rendimiento

### 4.2 Security Council

**Responsabilidades**:
- Auditoría de vulnerabilidades
- Respuesta a incidentes
- Responsabilidad de divulgación
- Bug bounty administration

**Miembros**: 5 expertos independientes
**Compensación**: 50k URT/año + honorarios

### 4.3 Community Grants

**Presupuesto**: 5M URT/año
**Categorías**:
- Desarrollo (máx 500k URT)
- Investigación (máx 300k URT)
- Marketing (máx 200k URT)
- Educación (máx 150k URT)

**Criterios de Aprobación**:
- Alineación con roadmap
- Equipo calificado
- Hitos claros
- Reporte de progreso

## 5. RFC Process (Request for Comments)

### 5.1 Fases

```
DRAFT (GitHub Issue)
  ↓
REVIEW (Discusión abierta 7 días)
  ↓
ACCEPTED (Votación propuesta)
  ↓
IMPLEMENTED (Cambio en código)
  ↓
CLOSED (Documentado)
```

### 5.2 Template RFC

```markdown
# RFC-XXX: Título

## Motivación
¿Por qué hacer este cambio?

## Propuesta
Qué cambiar y cómo

## Alternativas
Otras opciones consideradas

## Impacto
Cómo afecta a usuarios/desarrolladores

## Cronograma
Implementación estimada
```

## 6. Delegación de Voto

### 6.1 Mecanismo

```solidity
function delegate(address delegatee) public {
    _delegate(_msgSender(), delegatee);
}
```

### 6.2 Delegados Recomendados

- **Core Team**: Para votaciones técnicas
- **DAO Coordinators**: Para propuestas generales
- **Community Leaders**: Expertise específica
- **Oneself**: Participación directa

## 7. Resolución de Conflictos

### 7.1 Escalation Path

```
Desacuerdo Comunitario
  ↓
Mediación por Core Team
  ↓
Arbitrador independiente
  ↓
Votación comunitaria
```

### 7.2 Arbitrador

- Neutral, respetado
- Elegido por DAO
- Compensado por Tesorería
- Mandato anual renovable

## 8. Enmiendas a la Gobernanza

Cambios a este documento requieren:
- RFC formal
- Discusión 14 días
- Votación: >75% aprobación
- Quórum: 15%

## 9. Parámetros Ajustables por DAO

```
✓ Tasas de reward
✓ Límites de staking
✓ Parámetros de votación
✓ Presupuesto de tesorería
✓ Tipos de recursos certificables
✓ Fees de transacción
✓ Programas de incentivos
✗ Distribución inicial (locked)
✗ Direcciones de contrato (locked)
```

## 10. Transparencia y Reportes

### 10.1 Reportes Regulares

**Mensual**:
- Propuestas activas
- Resultados de votación
- Cambios técnicos

**Trimestral**:
- Estado de tesorería
- KPIs de gobernanza
- Participación comunitaria

**Anual**:
- Revisión de rendimiento
- Ajustes de parámetros
- Estrategia siguiente año

### 10.2 Públicamente Disponible

- Snapshot: https://snapshot.org/#/fuente
- Tesorería: https://etherscan.io
- GitHub: https://github.com/FuenteProtocol
- Forum: https://forum.fuente.io

## 11. Evolución de la Gobernanza

### Fase 1 (Centralizado)
- Core team toma decisiones
- Comunidad consulta
- Transición: 6 meses

### Fase 2 (Híbrido)
- DAO vota propuestas
- Core team ejecuta
- Transición: 12 meses

### Fase 3 (Descentralizado)
- DAO autónomo
- Ejecución automática
- Smart contract governance

---

**Adoptado**: Junio 26, 2026  
**Vigencia**: Indefinida hasta enmienda  
**Próxima revisión**: Diciembre 31, 2026
