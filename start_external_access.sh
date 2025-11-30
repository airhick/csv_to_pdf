#!/bin/bash
# Script interactif pour démarrer l'accès externe à l'API

set -e

clear
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║     🌐 Configuration Accès Externe API PDF               ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Ce script vous aide à choisir et configurer l'accès externe."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Sélectionnez votre cas d'usage:"
echo ""
echo "  1. 🧪 Test rapide (ngrok)"
echo "     → Pour tester maintenant, URL temporaire"
echo "     → Temps: 30 secondes"
echo "     → Gratuit (sessions de 2h)"
echo ""
echo "  2. 🏗️  Développement continu (Cloudflare Tunnel)"
echo "     → URL permanente gratuite"
echo "     → Temps: 10 min setup"
echo "     → Nécessite Mac allumé"
echo ""
echo "  3. 🚀 Production (Railway Cloud)"
echo "     → Déploiement cloud professionnel"
echo "     → Temps: 5 min"
echo "     → 500h/mois gratuit puis $5/mois"
echo ""
echo "  4. 🏠 Self-hosted (Port Forwarding)"
echo "     → Contrôle total, votre infrastructure"
echo "     → Temps: 30-60 min"
echo "     → Nécessite accès routeur"
echo ""
echo "  5. 📚 Voir le guide complet"
echo "     → Comparaison détaillée de toutes les options"
echo ""
echo "  6. ℹ️  Afficher les informations système"
echo "     → IPs, ports, statut du serveur"
echo ""
echo "  0. ❌ Quitter"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "Votre choix [1-6]: " choice
echo ""

case $choice in
    1)
        echo "╔════════════════════════════════════════════════════════════╗"
        echo "║   🧪 Démarrage avec ngrok (Test Rapide)                  ║"
        echo "╚════════════════════════════════════════════════════════════╝"
        echo ""
        
        # Vérifier si ngrok est installé
        if ! command -v ngrok &> /dev/null; then
            echo "⚠️  ngrok n'est pas installé"
            echo ""
            read -p "Voulez-vous l'installer maintenant? (o/n): " install_ngrok
            if [ "$install_ngrok" = "o" ] || [ "$install_ngrok" = "O" ]; then
                echo "📦 Installation de ngrok..."
                brew install ngrok
                echo "✓ ngrok installé"
            else
                echo "❌ Installation annulée"
                exit 1
            fi
        fi
        
        echo "📋 Instructions:"
        echo ""
        echo "1. Ce script va démarrer votre API en mode sécurisé"
        echo "2. Ouvrez un DEUXIÈME TERMINAL et exécutez:"
        echo ""
        echo "   ngrok http 8002"
        echo ""
        echo "3. Copiez l'URL https://xxxx.ngrok-free.app qui s'affiche"
        echo "4. Utilisez cette URL dans n8n/Zapier/etc:"
        echo ""
        echo "   https://xxxx.ngrok-free.app/api/generate"
        echo ""
        read -p "Appuyez sur Entrée pour démarrer l'API..."
        echo ""
        
        # Démarrer l'API
        ./start_public_secure.sh
        ;;
        
    2)
        echo "╔════════════════════════════════════════════════════════════╗"
        echo "║   🏗️  Configuration Cloudflare Tunnel                     ║"
        echo "╚════════════════════════════════════════════════════════════╝"
        echo ""
        
        # Vérifier si cloudflared est installé
        if ! command -v cloudflared &> /dev/null; then
            echo "⚠️  cloudflared n'est pas installé"
            echo ""
            read -p "Voulez-vous l'installer maintenant? (o/n): " install_cf
            if [ "$install_cf" = "o" ] || [ "$install_cf" = "O" ]; then
                echo "📦 Installation de cloudflared..."
                brew install cloudflared
                echo "✓ cloudflared installé"
            else
                echo "❌ Installation annulée"
                exit 1
            fi
        fi
        
        echo "📚 Pour configurer Cloudflare Tunnel, suivez ces étapes:"
        echo ""
        echo "1. Authentification:"
        echo "   cloudflared tunnel login"
        echo ""
        echo "2. Créer le tunnel:"
        echo "   cloudflared tunnel create pdf-api"
        echo ""
        echo "3. Voir le guide complet:"
        echo "   cat EXTERNAL_ACCESS_COMPLETE_GUIDE.md"
        echo ""
        echo "Ou lancez le script d'aide:"
        echo "   ./setup_cloudflare_tunnel.sh"
        echo ""
        read -p "Appuyez sur Entrée pour continuer..."
        ;;
        
    3)
        echo "╔════════════════════════════════════════════════════════════╗"
        echo "║   🚀 Déploiement sur Railway (Production)                ║"
        echo "╚════════════════════════════════════════════════════════════╝"
        echo ""
        
        # Vérifier si railway CLI est installé
        if ! command -v railway &> /dev/null; then
            echo "⚠️  Railway CLI n'est pas installé"
            echo ""
            read -p "Voulez-vous l'installer maintenant? (o/n): " install_railway
            if [ "$install_railway" = "o" ] || [ "$install_railway" = "O" ]; then
                echo "📦 Installation de Railway CLI..."
                npm install -g @railway/cli
                echo "✓ Railway CLI installé"
            else
                echo "❌ Installation annulée"
                echo "Vous pouvez l'installer plus tard avec:"
                echo "  npm install -g @railway/cli"
                exit 1
            fi
        fi
        
        echo "📚 Guide complet de déploiement Railway:"
        echo ""
        echo "   cat DEPLOY_RAILWAY.md"
        echo ""
        echo "🚀 Quick Start:"
        echo ""
        echo "1. Se connecter:"
        echo "   railway login"
        echo ""
        echo "2. Initialiser:"
        echo "   railway init"
        echo ""
        echo "3. Configurer l'API Key:"
        echo "   railway variables set REQUIRE_API_KEY=true"
        echo "   railway variables set API_KEY=\$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')"
        echo ""
        echo "4. Déployer:"
        echo "   railway up"
        echo ""
        echo "5. Générer un domaine:"
        echo "   railway domain"
        echo ""
        read -p "Voulez-vous démarrer l'assistant Railway maintenant? (o/n): " start_railway
        if [ "$start_railway" = "o" ] || [ "$start_railway" = "O" ]; then
            echo ""
            echo "🚂 Lancement de Railway..."
            railway login
            echo ""
            echo "✓ Connecté à Railway"
            echo ""
            echo "Maintenant, lancez:"
            echo "  railway init"
            echo "  railway up"
        fi
        ;;
        
    4)
        echo "╔════════════════════════════════════════════════════════════╗"
        echo "║   🏠 Configuration Port Forwarding                        ║"
        echo "╚════════════════════════════════════════════════════════════╝"
        echo ""
        
        # Détection de l'IP locale
        LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1)
        
        # Détection de l'IP du routeur (gateway)
        ROUTER_IP=$(netstat -nr | grep default | grep -v ":" | awk '{print $2}' | head -n 1)
        
        echo "📡 Informations réseau détectées:"
        echo ""
        echo "   IP de votre Mac: $LOCAL_IP"
        echo "   IP du routeur:   $ROUTER_IP"
        echo ""
        echo "📋 Étapes de configuration:"
        echo ""
        echo "1. Accédez à votre routeur:"
        echo "   → Ouvrez: http://$ROUTER_IP dans votre navigateur"
        echo ""
        echo "2. Connectez-vous avec vos identifiants routeur"
        echo ""
        echo "3. Trouvez la section 'Port Forwarding' ou 'NAT'"
        echo ""
        echo "4. Ajoutez cette règle:"
        echo "   Port externe:  8002"
        echo "   Port interne:  8002"
        echo "   IP locale:     $LOCAL_IP"
        echo "   Protocole:     TCP"
        echo ""
        echo "5. Trouvez votre IP publique:"
        echo "   $(curl -s ifconfig.me)"
        echo ""
        echo "6. Utilisez cette URL:"
        echo "   http://$(curl -s ifconfig.me):8002/api/generate"
        echo ""
        echo "📚 Guide détaillé disponible dans:"
        echo "   PUBLIC_ACCESS_GUIDE.md"
        echo ""
        read -p "Appuyez sur Entrée pour démarrer l'API en mode public..."
        ./start_public_secure.sh
        ;;
        
    5)
        echo "╔════════════════════════════════════════════════════════════╗"
        echo "║   📚 Guide Complet                                        ║"
        echo "╚════════════════════════════════════════════════════════════╝"
        echo ""
        
        if [ -f "EXTERNAL_ACCESS_COMPLETE_GUIDE.md" ]; then
            echo "📖 Ouverture du guide complet..."
            echo ""
            
            # Essayer d'ouvrir avec un éditeur
            if command -v code &> /dev/null; then
                code EXTERNAL_ACCESS_COMPLETE_GUIDE.md
                echo "✓ Ouvert dans VS Code"
            elif command -v open &> /dev/null; then
                open EXTERNAL_ACCESS_COMPLETE_GUIDE.md
                echo "✓ Ouvert dans l'éditeur par défaut"
            else
                echo "📄 Contenu du guide:"
                echo ""
                cat EXTERNAL_ACCESS_COMPLETE_GUIDE.md | head -100
                echo ""
                echo "... (voir le fichier complet pour plus de détails)"
            fi
        else
            echo "❌ Guide non trouvé"
        fi
        
        echo ""
        echo "📚 Autres documentations disponibles:"
        echo ""
        echo "   - EXTERNAL_ACCESS_COMPLETE_GUIDE.md  (Comparaison complète)"
        echo "   - DEPLOY_RAILWAY.md                  (Déploiement cloud)"
        echo "   - PUBLIC_ACCESS_GUIDE.md             (Config réseau)"
        echo "   - API_DOCUMENTATION.md               (API reference)"
        echo "   - N8N_EXAMPLES.md                    (Exemples n8n)"
        echo ""
        ;;
        
    6)
        echo "╔════════════════════════════════════════════════════════════╗"
        echo "║   ℹ️  Informations Système                                ║"
        echo "╚════════════════════════════════════════════════════════════╝"
        echo ""
        
        # IP locale
        LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1)
        
        # IP publique
        PUBLIC_IP=$(curl -s ifconfig.me)
        
        # Gateway
        ROUTER_IP=$(netstat -nr | grep default | grep -v ":" | awk '{print $2}' | head -n 1)
        
        # Vérifier si le port 8002 est utilisé
        PORT_STATUS=$(lsof -i :8002 -sTCP:LISTEN 2>/dev/null)
        
        echo "🌐 Configuration réseau:"
        echo ""
        echo "   IP locale (Mac):        $LOCAL_IP"
        echo "   IP publique:            $PUBLIC_IP"
        echo "   Passerelle (routeur):   $ROUTER_IP"
        echo ""
        echo "📡 Port 8002:"
        echo ""
        if [ -n "$PORT_STATUS" ]; then
            echo "   ✅ UTILISÉ - L'API semble tourner"
            echo ""
            echo "   Détails:"
            echo "$PORT_STATUS" | awk '{print "   " $0}'
        else
            echo "   ❌ LIBRE - L'API ne tourne pas"
        fi
        echo ""
        echo "🔗 URLs disponibles:"
        echo ""
        echo "   Local:           http://localhost:8002"
        echo "   Réseau local:    http://$LOCAL_IP:8002"
        echo "   Public (si port forwarding): http://$PUBLIC_IP:8002"
        echo ""
        echo "🛠️  Outils installés:"
        echo ""
        command -v ngrok &> /dev/null && echo "   ✅ ngrok" || echo "   ❌ ngrok (installer: brew install ngrok)"
        command -v cloudflared &> /dev/null && echo "   ✅ cloudflared" || echo "   ❌ cloudflared (installer: brew install cloudflared)"
        command -v railway &> /dev/null && echo "   ✅ railway" || echo "   ❌ railway (installer: npm install -g @railway/cli)"
        echo ""
        
        # Tester la connectivité
        echo "🔍 Test de connectivité:"
        echo ""
        if [ -n "$PORT_STATUS" ]; then
            echo "   Test local..."
            if curl -s http://localhost:8002/health > /dev/null 2>&1; then
                echo "   ✅ API accessible en local"
            else
                echo "   ⚠️  Port utilisé mais API ne répond pas"
            fi
        else
            echo "   ⏸️  API non démarrée"
            echo "   Lancez: ./start_public_secure.sh"
        fi
        echo ""
        
        read -p "Appuyez sur Entrée pour continuer..."
        ;;
        
    0)
        echo "👋 Au revoir !"
        exit 0
        ;;
        
    *)
        echo "❌ Choix invalide"
        exit 1
        ;;
esac

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Configuration terminée !"
echo ""
echo "📚 Pour plus d'informations:"
echo "   cat EXTERNAL_ACCESS_COMPLETE_GUIDE.md"
echo ""

