#!/bin/bash
# Démarrer le serveur en mode PUBLIC avec authentification API Key

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🔐 Démarrage du serveur en mode PUBLIC SÉCURISÉ          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Activer l'environnement virtuel
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Environnement virtuel activé"
else
    echo "⚠️  Environnement virtuel non trouvé"
fi

# Générer une API key si elle n'existe pas dans .env
if [ -f ".env" ] && grep -q "API_KEY=" .env; then
    source .env
    echo "✓ API Key chargée depuis .env"
else
    # Générer une nouvelle API key
    API_KEY=$(openssl rand -hex 32 2>/dev/null || python3 -c "import secrets; print(secrets.token_hex(32))")
    echo "API_KEY=$API_KEY" > .env
    echo "REQUIRE_API_KEY=True" >> .env
    echo "✓ Nouvelle API Key générée et sauvegardée dans .env"
fi

# Charger les variables
source .env

# Variables d'environnement
export HOST="0.0.0.0"
export PORT="8002"
export DEBUG="False"
export API_KEY="$API_KEY"
export REQUIRE_API_KEY="True"

# Détecter l'IP locale
LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1)

echo ""
echo "📡 Configuration réseau:"
echo "   Host: $HOST (toutes les interfaces)"
echo "   Port: $PORT"
echo "   IP locale: $LOCAL_IP"
echo ""
echo "🔐 Sécurité:"
echo "   API Key: $API_KEY"
echo "   Authentification: ACTIVÉE"
echo ""

# Vérifier si le port est déjà utilisé
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Le port $PORT est déjà utilisé!"
    echo "   Arrêt du processus existant..."
    lsof -ti:$PORT | xargs kill -9 2>/dev/null
    sleep 1
fi

echo ""
echo "🌐 URLs d'accès:"
echo "   Local:        http://localhost:$PORT"
echo "   Réseau local: http://$LOCAL_IP:$PORT"
echo "   API:          http://$LOCAL_IP:$PORT/api/generate"
echo ""
echo "📝 Exemple curl avec API Key:"
echo "   curl -X POST http://$LOCAL_IP:$PORT/api/generate \\"
echo "     -H 'X-API-Key: $API_KEY' \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"data\":[{\"name\":\"Test\",\"address\":\"Addr\"}]}' \\"
echo "     -o output.zip"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Démarrer le serveur
python app.py


