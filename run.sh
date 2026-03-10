#!/bin/bash

# DJ Harmonic Analyzer MVP - Script auxiliar
# Este script ativa o venv automaticamente e executa comandos

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Diretório do script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Ativar venv
source "$SCRIPT_DIR/venv/bin/activate"

# Se nenhum argumento foi passado, mostrar ajuda
if [ $# -eq 0 ]; then
    echo -e "${BLUE}"
    echo "============================================================"
    echo "🎧 DJ HARMONIC ANALYZER - MVP"
    echo "============================================================"
    echo -e "${NC}"
    echo ""
    echo -e "${YELLOW}Uso:${NC}"
    echo "  ./run.sh analyze <arquivo.mp3>"
    echo "  ./run.sh mixes <chave_camelot>"
    echo "  ./run.sh compatible <chave1> <chave2>"
    echo "  ./run.sh help"
    echo ""
    echo -e "${YELLOW}Exemplos:${NC}"
    echo "  ./run.sh analyze minha_musica.mp3"
    echo "  ./run.sh mixes 8A"
    echo "  ./run.sh compatible 8A 7A"
    echo ""
    echo -e "${BLUE}============================================================${NC}"
    echo ""
    exit 0
fi

# Executar comando
python "$SCRIPT_DIR/main.py" "$@"
