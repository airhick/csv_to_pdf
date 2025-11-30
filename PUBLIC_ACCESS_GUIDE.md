# 🌐 Guide d'Accès Public - Configuration Externe

Ce guide explique comment rendre votre API accessible depuis l'extérieur (n8n, Zapier, Make, etc.)

---

## 🚀 Démarrage Rapide

### Option 1: Sans Authentification (Tests/Réseau Local)

```bash
chmod +x start_public.sh
./start_public.sh
```

### Option 2: Avec Authentification (Recommandé pour Internet)

```bash
chmod +x start_public_secure.sh
./start_public_secure.sh
```

L'API Key sera automatiquement générée et sauvegardée dans `.env`

---

## 📍 Trouver Votre IP

### IP Locale (Réseau Local)

```bash
# macOS
ifconfig | grep "inet " | grep -v 127.0.0.1

# Ou plus simple
ipconfig getifaddr en0  # Wi-Fi
ipconfig getifaddr en1  # Ethernet
```

Exemple: `192.168.1.100`

### IP Publique (Internet)

```bash
curl ifconfig.me
# ou
curl ipinfo.io/ip
```

Exemple: `203.0.113.45`

---

## 🔧 Configuration selon votre Scénario

### Scénario 1: n8n sur le MÊME ordinateur

**Configuration:**
- Démarrer avec: `./start_public.sh`
- URL dans n8n: `http://localhost:8002/api/generate`

**Pas besoin de configuration réseau!**

---

### Scénario 2: n8n sur le MÊME réseau local (Wi-Fi/LAN)

**Configuration:**
1. Démarrer avec: `./start_public.sh`
2. Trouver votre IP locale: `ipconfig getifaddr en0`
3. URL dans n8n: `http://192.168.1.XXX:8002/api/generate`

**Pas besoin de configuration routeur/firewall!**

---

### Scénario 3: n8n Cloud / Serveur distant (Internet)

**Configuration réseau nécessaire:**

#### Étape 1: Ouvrir le port sur votre routeur

1. Accédez à l'interface de votre routeur (généralement `192.168.1.1`)
2. Allez dans **Port Forwarding** ou **NAT**
3. Ajoutez une règle:
   - Port externe: `8002`
   - Port interne: `8002`
   - IP locale: Votre IP locale (ex: `192.168.1.100`)
   - Protocole: `TCP`

#### Étape 2: Configurer votre firewall macOS

```bash
# Autoriser le port 8002
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add $(which python3)
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --unblockapp $(which python3)
```

#### Étape 3: Démarrer le serveur en mode sécurisé

```bash
./start_public_secure.sh
```

#### Étape 4: Trouver votre IP publique

```bash
curl ifconfig.me
```

#### Étape 5: Utiliser dans n8n

URL: `http://VOTRE_IP_PUBLIQUE:8002/api/generate`

⚠️ **Note:** Votre IP publique peut changer si vous n'avez pas d'IP fixe.

---

## 🔐 Authentification API Key

### Activer l'Authentification

```bash
./start_public_secure.sh
```

L'API Key est sauvegardée dans `.env`

### Voir votre API Key

```bash
cat .env
```

### Utiliser l'API Key

#### Dans curl:

```bash
curl -X POST http://YOUR_IP:8002/api/generate \
  -H "X-API-Key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"data":[{"name":"Test","address":"Addr"}]}' \
  -o output.zip
```

#### Dans n8n (HTTP Request Node):

**Headers:**
```
X-API-Key: your_api_key_here
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "data": [
    {"name": "Client 1", "address": "Address 1"},
    {"name": "Client 2", "address": "Address 2"}
  ],
  "singleFile": true
}
```

---

## 🔍 Vérifier que ça fonctionne

### Test 1: Health Check (Sans API Key)

```bash
curl http://YOUR_IP:8002/health
```

**Réponse attendue:**
```json
{
  "status": "ok",
  "service": "PDF Generator API",
  "version": "2.1"
}
```

### Test 2: Status API

```bash
curl http://YOUR_IP:8002/api/status
```

### Test 3: Génération PDF

```bash
curl -X POST http://YOUR_IP:8002/api/generate \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"data":[{"name":"Test","address":"Test Addr"}]}' \
  -o test.zip
```

---

## 📱 Configuration n8n

### Workflow n8n Simple

1. **HTTP Request Node:**
   - **Method:** POST
   - **URL:** `http://YOUR_IP:8002/api/generate`
   - **Headers:**
     - `X-API-Key`: `your_api_key`
     - `Content-Type`: `application/json`
   - **Body:**
     ```json
     {
       "data": [
         {
           "name": "{{ $json.customer_name }}",
           "address": "{{ $json.customer_address }}"
         }
       ],
       "singleFile": true
     }
     ```
   - **Response Format:** File

2. **Save Binary Node** (optionnel):
   - Pour sauvegarder le PDF généré

### Exemple Workflow Complet n8n

```json
{
  "nodes": [
    {
      "name": "HTTP Request",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "http://YOUR_IP:8002/api/generate",
        "method": "POST",
        "headerParameters": {
          "parameter": [
            {
              "name": "X-API-Key",
              "value": "your_api_key_here"
            },
            {
              "name": "Content-Type",
              "value": "application/json"
            }
          ]
        },
        "bodyParameters": {
          "data": [
            {
              "name": "Jean Dupont",
              "address": "123 Rue\\nParis\\nFrance"
            }
          ],
          "singleFile": true
        },
        "responseFormat": "file"
      }
    }
  ]
}
```

---

## 🛡️ Sécurité

### Pour Usage Local/Tests
- ✅ Utilisez `./start_public.sh` (sans authentification)
- ✅ Accès limité au réseau local

### Pour Usage Internet
- ✅ **OBLIGATOIRE:** Utilisez `./start_public_secure.sh`
- ✅ Changez l'API Key régulièrement
- ✅ Utilisez HTTPS (voir section ci-dessous)
- ✅ Configurez un reverse proxy (nginx/caddy)
- ✅ Ajoutez rate limiting

### Activer HTTPS (Optionnel mais recommandé)

Pour HTTPS, utilisez un reverse proxy comme **Caddy**:

```bash
# Installer Caddy
brew install caddy

# Créer un Caddyfile
cat > Caddyfile << EOF
your-domain.com {
    reverse_proxy localhost:8002
}
EOF

# Démarrer Caddy (obtient automatiquement un certificat SSL)
sudo caddy run
```

---

## 🐛 Dépannage

### Le serveur ne démarre pas

```bash
# Vérifier si le port est libre
lsof -i :8002

# Tuer le processus
lsof -ti:8002 | xargs kill -9
```

### Impossible d'accéder depuis l'extérieur

1. **Vérifier le firewall:**
   ```bash
   sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
   ```

2. **Vérifier le port forwarding:**
   - Connectez-vous à votre routeur
   - Vérifiez que la règle de port forwarding est active

3. **Tester depuis l'extérieur:**
   - Utilisez votre téléphone (en 4G, pas en Wi-Fi)
   - Ou utilisez un service comme: https://www.yougetsignal.com/tools/open-ports/

### L'API Key ne fonctionne pas

```bash
# Vérifier l'API Key dans .env
cat .env

# Regénérer une nouvelle clé
rm .env
./start_public_secure.sh
```

### Erreur "Connection refused"

- Le serveur n'est pas démarré, lancez `./start_public.sh`
- Le pare-feu bloque la connexion
- Mauvaise IP/port

---

## 📊 IP Dynamique vs IP Fixe

### Si votre IP change souvent

**Solution 1: DynDNS**
- Utilisez un service comme **No-IP** ou **DuckDNS**
- Crée un nom de domaine qui suit votre IP

**Solution 2: Tunnel (recommandé)**
- **ngrok**: `ngrok http 8002`
- **Cloudflare Tunnel**: Gratuit et sécurisé
- **LocalTunnel**: `npx localtunnel --port 8002`

### Exemple avec ngrok

```bash
# Installer ngrok
brew install ngrok

# Démarrer le tunnel
ngrok http 8002

# Utiliser l'URL générée dans n8n
# Exemple: https://abc123.ngrok.io/api/generate
```

---

## 📝 Exemple Complet avec n8n

### Cas d'usage: Générer des PDFs depuis Google Sheets

1. **Trigger:** Google Sheets - On Row Added
2. **Node HTTP Request:**
   - URL: `http://YOUR_IP:8002/api/generate`
   - Headers: `X-API-Key: your_key`
   - Body:
     ```json
     {
       "data": [{
         "name": "{{ $json.Name }}",
         "address": "{{ $json.Address }}"
       }],
       "singleFile": true
     }
     ```
3. **Node Gmail:** Send Email with PDF attachment

---

## 🎯 URLs de Référence Rapide

| Service | URL |
|---------|-----|
| Interface Web | `http://YOUR_IP:8002/` |
| Health Check | `http://YOUR_IP:8002/health` |
| API Status | `http://YOUR_IP:8002/api/status` |
| API Generate | `http://YOUR_IP:8002/api/generate` |

---

## ⚡ Quick Commands

```bash
# Démarrer (local)
./start_public.sh

# Démarrer (sécurisé)
./start_public_secure.sh

# Voir mon IP locale
ipconfig getifaddr en0

# Voir mon IP publique
curl ifconfig.me

# Voir l'API Key
cat .env

# Tester l'API
curl http://localhost:8002/health

# Arrêter le serveur
lsof -ti:8002 | xargs kill -9
```

---

**🎉 Votre API est maintenant accessible depuis n'importe où!**


