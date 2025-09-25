#!/bin/bash

# Script de inicialização do Sistema de Pesquisa de Satisfação
# Hospital Santa Clara

echo "🏥 Iniciando Sistema de Pesquisa de Satisfação - Hospital Santa Clara"
echo "=================================================================="

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.8 ou superior."
    exit 1
fi

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "🔄 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "⬇️ Instalando dependências..."
pip install -r requirements.txt

# Verificar se arquivo .env existe
if [ ! -f ".env" ]; then
    echo "⚙️ Criando arquivo .env a partir do exemplo..."
    cp .env.example .env
    echo "⚠️  IMPORTANTE: Configure o arquivo .env com suas credenciais!"
fi

# Executar aplicação
echo "🚀 Iniciando aplicação..."
echo ""
echo "📱 Interface da Pesquisa: http://localhost:8000"
echo "📊 Dashboard de Insights: http://localhost:8000/dashboard"
echo "🔧 Documentação da API: http://localhost:8000/docs"
echo ""
echo "Para parar a aplicação, pressione Ctrl+C"
echo ""

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
