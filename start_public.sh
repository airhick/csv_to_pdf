#!/bin/bash
# Démarrer le serveur accessible depuis l'extérieur (IP publique)

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🌐 Démarrage du serveur en mode PUBLIC                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Activer l'environnement virtuel
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Environnement virtuel activé"
else
    echo "⚠️  Environnement virtuel non trouvé"
fi

# Variables d'environnement
export HOST="0.0.0.0"
export PORT="8002"
export DEBUG="False"  # IMPORTANT: Debug désactivé en production

# Détecter l'IP locale
LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1)

echo ""
echo "📡 Configuration réseau:"
echo "   Host: $HOST (toutes les interfaces)"
echo "   Port: $PORT"
echo "   IP locale: $LOCAL_IP"
echo ""

# Vérifier si le port est déjà utilisé
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Le port $PORT est déjà utilisé!"
    echo "   Arrêt du processus existant..."
    lsof -ti:$PORT | xargs kill -9 2>/dev/null
    sleep 1
fi

echo ""
echo "🔓 Mode: SANS authentification (pour tests)"
echo "   Pour activer l'API Key, utiliser: ./start_public_secure.sh"
echo ""
echo "🌐 URLs d'accès:"
echo "   Local:        http://localhost:$PORT"
echo "   Réseau local: http://$LOCAL_IP:$PORT"
echo "   API:          http://$LOCAL_IP:$PORT/api/generate"
echo ""
echo "⚠️  ATTENTION: Le serveur est accessible depuis votre réseau!"
echo "   Pour n8n/externe, utilisez: http://$LOCAL_IP:$PORT/api/generate"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Démarrer le serveur
python app.py


