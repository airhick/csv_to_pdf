#!/bin/bash
# Setup Cloudflare Tunnel for PDF API
# This creates a permanent, free external URL for your API

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   🌐 Setup Cloudflare Tunnel for PDF API                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if cloudflared is installed
if ! command -v cloudflared &> /dev/null; then
    echo "📦 Installing cloudflared..."
    brew install cloudflared
    echo "✓ cloudflared installed"
else
    echo "✓ cloudflared already installed"
fi

echo ""
echo "📋 ÉTAPES À SUIVRE:"
echo ""
echo "1. Authentification (va ouvrir votre navigateur):"
echo "   cloudflared tunnel login"
echo ""
echo "2. Créer un tunnel (une seule fois):"
echo "   cloudflared tunnel create pdf-api"
echo ""
echo "3. Obtenir l'ID du tunnel:"
echo "   cloudflared tunnel list"
echo ""
echo "4. Créer la configuration:"
echo "   Créez le fichier ~/.cloudflared/config.yml avec:"
echo ""
cat << 'EOF'
tunnel: YOUR_TUNNEL_ID
credentials-file: /Users/YOUR_USERNAME/.cloudflared/YOUR_TUNNEL_ID.json

ingress:
  - hostname: YOUR_SUBDOMAIN.cfargotunnel.com
    service: http://localhost:8002
  - service: http_status:404
EOF
echo ""
echo "5. Créer une route DNS:"
echo "   cloudflared tunnel route dns pdf-api YOUR_SUBDOMAIN.cfargotunnel.com"
echo ""
echo "6. Démarrer le tunnel:"
echo "   cloudflared tunnel run pdf-api"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🚀 DÉMARRAGE RAPIDE (après configuration):"
echo ""
echo "# Terminal 1: Démarrer l'API"
echo "./start_public_secure.sh"
echo ""
echo "# Terminal 2: Démarrer le tunnel"
echo "cloudflared tunnel run pdf-api"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📚 Documentation: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/"
echo ""

