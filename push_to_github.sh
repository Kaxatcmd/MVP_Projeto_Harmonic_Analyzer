#!/bin/bash

# Script para fazer push para repositório GitHub
# Uso: ./push_to_github.sh <URL_DO_REPOSITORIO>
# Ex: ./push_to_github.sh https://github.com/Kaxatcmd/MVP_Projeto_Harmonic_Analyzer.git

if [ -z "$1" ]; then
    echo "❌ Erro: URL do repositório não fornecida"
    echo "Uso: ./push_to_github.sh <URL_DO_REPOSITORIO>"
    echo "Ex:  ./push_to_github.sh https://github.com/Kaxatcmd/MVP_Projeto_Harmonic_Analyzer.git"
    exit 1
fi

REPO_URL="$1"

echo "════════════════════════════════════════════════════════"
echo "🚀 PUSH PARA GITHUB"
echo "════════════════════════════════════════════════════════"
echo "URL: $REPO_URL"
echo ""

# Verificar se estamos num repositório Git
if [ ! -d ".git" ]; then
    echo "❌ Erro: Não está num repositório Git"
    exit 1
fi

# Remover remoto existente se houver
git remote remove origin 2>/dev/null

# Adicionar novo remoto
echo "📌 Adicionando remoto..."
git remote add origin "$REPO_URL"

# Fazer push
echo "📤 Fazendo push para GitHub..."
git push -u origin master

if [ $? -eq 0 ]; then
    echo ""
    echo "════════════════════════════════════════════════════════"
    echo "✅ Push realizado com sucesso!"
    echo ""
    echo "📊 Repositório em:"
    echo "$REPO_URL" | sed 's|.git||' | xargs echo
    echo ""
    echo "════════════════════════════════════════════════════════"
else
    echo ""
    echo "❌ Erro ao fazer push. Verifique:"
    echo "  1. Se a URL está correcta"
    echo "  2. Se tem permissões no repositório"
    echo "  3. Se tem autenticação configurada (token/SSH)"
    exit 1
fi
