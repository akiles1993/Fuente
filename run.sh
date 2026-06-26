#!/bin/bash
# ./run.sh - Script para ejecutar todo el stack Fuente

echo "🚀 Iniciando Fuente Protocol Stack..."

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar dependencias
echo -e "${YELLOW}📋 Verificando dependencias...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 no está instalado${NC}"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ Node.js/npm no está instalado${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Dependencias OK${NC}"

# Instalar dependencias Python
echo -e "${YELLOW}📦 Instalando dependencias Python...${NC}"
cd api
pip install -r requirements.txt
cd ..

# Instalar dependencias Frontend
echo -e "${YELLOW}📦 Instalando dependencias Frontend...${NC}"
cd frontend
npm install
cd ..

echo -e "${GREEN}✓ Dependencias instaladas${NC}"

# Crear directorio de logs
mkdir -p logs

# Iniciar servicios
echo -e "${YELLOW}🔧 Iniciando servicios...${NC}"

# Backend en background
echo -e "${GREEN}▶ Iniciando Backend API (puerto 8000)...${NC}"
cd api
python3 -m uvicorn backend:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Frontend en background
echo -e "${GREEN}▶ Iniciando Frontend (puerto 3000)...${NC}"
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo -e "${GREEN}✓ Stack iniciado${NC}"
echo ""
echo "┌─────────────────────────────────────────┐"
echo "│  Fuente Protocol Stack Running          │"
echo "├─────────────────────────────────────────┤"
echo "│  Backend:  http://localhost:8000        │"
echo "│  Frontend: http://localhost:3000        │"
echo "│  Docs:     http://localhost:8000/docs   │"
echo "├─────────────────────────────────────────┤"
echo "│  Backend PID:  $BACKEND_PID"
echo "│  Frontend PID: $FRONTEND_PID"
echo "└─────────────────────────────────────────┘"
echo ""
echo "Presiona Ctrl+C para detener todos los servicios"

# Esperar señal de terminación
wait
