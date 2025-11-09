#!/bin/bash
# Script de lancement pour macOS
# Double-cliquez sur ce fichier pour lancer l'application

cd "$(dirname "$0")"

# Activer l'environnement virtuel si il existe
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Lancer l'application
python3 gui_app.py

# Garder la fenêtre ouverte en cas d'erreur
if [ $? -ne 0 ]; then
    echo ""
    echo "Appuyez sur Entrée pour fermer..."
    read
fi

