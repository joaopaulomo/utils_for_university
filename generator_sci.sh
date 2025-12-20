#!/bin/bash

clear

echo "=========================================="
echo "   INICIANDO O GERADOR DE GRADE - IGEO    "
echo "=========================================="
echo ""

if [ -f "gerador_horario.py" ]; then
    
    if command -v python3 &> /dev/null; then
        python3 gerador_horario.py
    else
        python gerador_horario.py
    fi

else
    echo "❌ ERRO: O arquivo 'gerador_horario.py' não foi encontrado nesta pasta."
    echo "Certifique-se de que o script Python e este arquivo .sh estão juntos."
fi

echo ""
echo "=========================================="
read -p "Pressione [ENTER] para encerrar..."