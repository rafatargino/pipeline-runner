#!/bin/bash

echo "Configurando ambiente virtual..."
.env.example
source venv/bin/activate

echo "Instalando dependências..."
pip install -r requirements.txt

if [ ! -f .env ]; then
    echo "Criando arquivo .env..."
    cp .env.example .env
    echo "⚠️  ATENÇÃO: Edite o arquivo .env e coloque sua OPENAI_API_KEY."
else
    echo ".env já existe."
fi

echo "Pronto! Agora ative o ambiente com:"
echo "source venv/bin/activate"