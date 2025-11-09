#!/bin/bash
# Script pour préparer le déploiement sur Netlify

echo "Préparation du déploiement Netlify..."

# Copier le module principal dans le dossier functions
echo "Copie du module add_addresses_to_pdf.py..."
cp add_addresses_to_pdf.py netlify/functions/

echo "✓ Préparation terminée!"
echo ""
echo "Vous pouvez maintenant:"
echo "1. Initialiser Git: git init"
echo "2. Ajouter les fichiers: git add ."
echo "3. Commit: git commit -m 'Initial commit'"
echo "4. Pousser sur GitHub/GitLab"
echo "5. Déployer sur Netlify via le dashboard"

