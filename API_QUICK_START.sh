#!/bin/bash
# Quick Start - API Examples
# Usage: chmod +x API_QUICK_START.sh && ./API_QUICK_START.sh

echo "================================================"
echo "  🚀 API Quick Start - PDF Generator"
echo "================================================"
echo ""

BASE_URL="http://localhost:8002"

# Vérifier que le serveur est actif
echo "⏳ Vérification du serveur..."
if ! curl -s -f "$BASE_URL/" > /dev/null; then
    echo "❌ Erreur: Le serveur n'est pas actif sur $BASE_URL"
    echo "   Lancez le serveur avec: python app.py"
    exit 1
fi
echo "✓ Serveur actif"
echo ""

# Test 1: JSON Simple
echo "📋 Test 1: JSON Simple (2 entrées, positions par défaut)"
curl -X POST "$BASE_URL/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {
        "name": "Jean Dupont",
        "address": "123 Rue de la République\n75001 Paris\nFrance"
      },
      {
        "name": "Marie Martin",
        "address": "45 Avenue des Champs-Élysées\n75008 Paris\nFrance"
      }
    ]
  }' \
  -o example_output.zip 2>/dev/null

if [ -f "example_output.zip" ]; then
    echo "✓ ZIP généré: example_output.zip ($(du -h example_output.zip | cut -f1))"
    unzip -l example_output.zip | tail -n +4 | head -n -2
else
    echo "❌ Échec"
fi
echo ""

# Test 2: Single File
echo "📋 Test 2: Single File (PDF unique avec toutes les pages)"
curl -X POST "$BASE_URL/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {
        "name": "Pierre Durand",
        "address": "78 Boulevard Saint-Germain\n75006 Paris\nFrance"
      },
      {
        "name": "Sophie Bernard",
        "address": "12 Rue de Rivoli\n75004 Paris\nFrance"
      },
      {
        "name": "Luc Moreau",
        "address": "34 Rue du Faubourg Saint-Honoré\n75008 Paris\nFrance"
      }
    ],
    "singleFile": true
  }' \
  -o example_single.pdf 2>/dev/null

if [ -f "example_single.pdf" ]; then
    echo "✓ PDF généré: example_single.pdf ($(du -h example_single.pdf | cut -f1))"
    # Compter les pages
    PAGES=$(python3 -c "from PyPDF2 import PdfReader; print(len(PdfReader('example_single.pdf').pages))" 2>/dev/null)
    echo "  Nombre de pages: $PAGES (3 recto + 3 verso)"
else
    echo "❌ Échec"
fi
echo ""

# Test 3: Positions Personnalisées
echo "📋 Test 3: Positions Personnalisées"
curl -X POST "$BASE_URL/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {
        "name": "Custom Position Test",
        "address": "Custom Address Position\n12345 Test City\nTest Country"
      }
    ],
    "namePosition": {
      "left": 30,
      "bottom": 260,
      "width": 90,
      "height": 25
    },
    "addressPosition": {
      "left": 100,
      "bottom": 30,
      "width": 95,
      "height": 35
    },
    "singleFile": true
  }' \
  -o example_custom_positions.pdf 2>/dev/null

if [ -f "example_custom_positions.pdf" ]; then
    echo "✓ PDF généré: example_custom_positions.pdf ($(du -h example_custom_positions.pdf | cut -f1))"
else
    echo "❌ Échec"
fi
echo ""

# Test 4: CSV Upload (si fichiers disponibles)
if [ -f "test_csv1.csv" ] && [ -f "test_csv2.csv" ]; then
    echo "📋 Test 4: Upload CSV via API"
    curl -X POST "$BASE_URL/api/generate" \
      -F "csvFiles=@test_csv1.csv" \
      -F "csvFiles=@test_csv2.csv" \
      -F 'singleFile=true' \
      -o example_from_csv.pdf 2>/dev/null
    
    if [ -f "example_from_csv.pdf" ]; then
        echo "✓ PDF généré: example_from_csv.pdf ($(du -h example_from_csv.pdf | cut -f1))"
    else
        echo "❌ Échec"
    fi
    echo ""
fi

echo "================================================"
echo "  ✅ Tests terminés!"
echo "================================================"
echo ""
echo "Fichiers générés:"
ls -lh example_*.{zip,pdf} 2>/dev/null || echo "  (aucun fichier)"
echo ""
echo "Pour nettoyer:"
echo "  rm -f example_*.zip example_*.pdf"
echo ""

