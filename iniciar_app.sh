#!/bin/bash

# Define ROOT como o diretório onde o script está localizado
ROOT="$(cd "$(dirname "$0")" && pwd)"

# Mata o processo do Chromium
killall chromium-browser

# Ativa o ambiente virtual do Python
source "$ROOT/.venv/bin/activate"

# Executa o script Python
python -B "$ROOT/app.py"
