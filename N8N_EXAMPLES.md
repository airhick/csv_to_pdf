# 🔗 Exemples d'Intégration n8n

Guide pratique pour utiliser l'API PDF Generator dans n8n.

---

## 🚀 Configuration Initiale

### 1. Démarrer le Serveur

```bash
# Sans authentification (tests locaux)
./start_public.sh

# Avec authentification (recommandé)
./start_public_secure.sh
```

### 2. Trouver Votre URL

**Si n8n est sur le même ordinateur:**
```
http://localhost:8002/api/generate
```

**Si n8n est sur le même réseau:**
```bash
# Trouver votre IP
ipconfig getifaddr en0

# URL à utiliser
http://192.168.1.XXX:8002/api/generate
```

**Si n8n est dans le cloud:**
```bash
# Trouver votre IP publique
curl ifconfig.me

# URL à utiliser
http://YOUR_PUBLIC_IP:8002/api/generate
```

---

## 📋 Workflow n8n: Exemple Simple

### Configuration du Node HTTP Request

**Basic Settings:**
- **Method:** `POST`
- **URL:** `http://YOUR_IP:8002/api/generate`

**Headers:**
```json
{
  "Content-Type": "application/json",
  "X-API-Key": "your_api_key_here"
}
```
*(Supprimer X-API-Key si mode non sécurisé)*

**Body (JSON):**
```json
{
  "data": [
    {
      "name": "Jean Dupont",
      "address": "123 Rue de la République\n75001 Paris\nFrance"
    },
    {
      "name": "Marie Martin",
      "address": "45 Avenue des Champs-Élysées\n75008 Paris\nFrance"
    }
  ],
  "singleFile": true
}
```

**Response:**
- **Response Format:** `File`
- Le PDF sera disponible comme fichier binaire

---

## 🎯 Cas d'Usage: Google Sheets → PDF

### Workflow

1. **Google Sheets Trigger** - Détecte une nouvelle ligne
2. **HTTP Request** - Génère le PDF
3. **Email** - Envoie le PDF

### Configuration Détaillée

#### Node 1: Google Sheets Trigger
```
Trigger: On Row Added
Sheet: Clients
```

#### Node 2: HTTP Request
```javascript
// Method
POST

// URL
http://YOUR_IP:8002/api/generate

// Headers
{
  "Content-Type": "application/json",
  "X-API-Key": "{{ $env.PDF_API_KEY }}"
}

// Body
{
  "data": [{
    "name": "{{ $json.Name }}",
    "address": "{{ $json.Address }}"
  }],
  "singleFile": true,
  "namePosition": {
    "left": 20,
    "bottom": 250,
    "width": 80,
    "height": 30
  },
  "addressPosition": {
    "left": 95,
    "bottom": 20,
    "width": 100,
    "height": 40
  }
}

// Response Format
File
```

#### Node 3: Gmail (Send Email)
```
To: {{ $json.Email }}
Subject: Votre document
Attachments: data (from previous node)
```

---

## 🔄 Cas d'Usage: Webhook → Batch PDF

Génération de plusieurs PDFs à la demande.

### Configuration Webhook

```javascript
// Webhook Node - Reçoit des données
// POST /webhook/generate-pdfs

// Exemple de données reçues:
{
  "customers": [
    {"name": "Client 1", "address": "Addr 1"},
    {"name": "Client 2", "address": "Addr 2"},
    {"name": "Client 3", "address": "Addr 3"}
  ]
}
```

### HTTP Request Node

```javascript
// Transformer les données
{
  "data": {{ $json.customers }},
  "singleFile": false  // Un PDF par client
}
```

---

## 🎨 Cas d'Usage: Airtable → PDF Personnalisé

### Workflow

1. **Airtable Trigger** - Nouveau record
2. **Code Node** - Préparer l'adresse
3. **HTTP Request** - Générer PDF
4. **Airtable** - Update record avec lien PDF

### Code Node (Formatter)

```javascript
// items[0] contient les données d'Airtable
const record = items[0].json;

// Formater l'adresse sur plusieurs lignes
const address = [
  record.street,
  `${record.zipcode} ${record.city}`,
  record.country
].join('\n');

return [{
  json: {
    name: `${record.firstName} ${record.lastName}`,
    address: address,
    recordId: record.id
  }
}];
```

### HTTP Request

```javascript
{
  "data": [{
    "name": "{{ $json.name }}",
    "address": "{{ $json.address }}"
  }],
  "singleFile": true
}
```

---

## 🔢 Cas d'Usage: CSV Import → Bulk PDF

Générer des PDFs en masse depuis un CSV.

### Workflow

1. **Read Binary File** - Lire le CSV
2. **Spreadsheet File** - Parser CSV
3. **HTTP Request** - Générer tous les PDFs
4. **Write Binary File** - Sauvegarder le ZIP

### Configuration

#### Read Binary File
```
File Path: /path/to/customers.csv
```

#### Spreadsheet File
```
Operation: Read from File
File Format: CSV
```

#### HTTP Request
```javascript
// Body
{
  "data": {{ $json.map(row => ({
    name: row.Name,
    address: row.Address
  })) }},
  "singleFile": false
}
```

---

## 🔐 Gestion de l'API Key dans n8n

### Méthode 1: Credentials (Recommandé)

1. **Créer un Credential:**
   - Type: `Header Auth`
   - Name: `PDF Generator API`
   - Header Name: `X-API-Key`
   - Header Value: `your_api_key_here`

2. **Utiliser dans HTTP Request:**
   - Authentication: `Generic Credential Type`
   - Credential Type: `Header Auth`
   - Select: `PDF Generator API`

### Méthode 2: Environment Variable

```javascript
// Dans le HTTP Request Node
{
  "X-API-Key": "{{ $env.PDF_API_KEY }}"
}
```

Définir dans n8n:
- Settings → Environment Variables
- `PDF_API_KEY` = `your_actual_key`

---

## 🔍 Debug dans n8n

### Vérifier la Connexion

Créez un workflow simple pour tester:

```javascript
// HTTP Request Node
Method: GET
URL: http://YOUR_IP:8002/health

// Réponse attendue:
{
  "status": "ok",
  "service": "PDF Generator API",
  "version": "2.1"
}
```

### Vérifier l'API Status

```javascript
// HTTP Request Node
Method: GET
URL: http://YOUR_IP:8002/api/status

// Réponse:
{
  "status": "operational",
  "api_key_required": true/false,
  "host": "..."
}
```

---

## 🎭 Exemples Avancés

### Positions Dynamiques

```javascript
// Code Node pour calculer les positions
const positions = items[0].json;

return [{
  json: {
    data: [{
      name: positions.name,
      address: positions.address
    }],
    namePosition: {
      left: positions.template === 'standard' ? 20 : 30,
      bottom: positions.template === 'standard' ? 250 : 260,
      width: 80,
      height: 30
    },
    addressPosition: {
      left: positions.template === 'standard' ? 95 : 100,
      bottom: 20,
      width: 100,
      height: 40
    },
    singleFile: true
  }
}];
```

### Gestion des Erreurs

```javascript
// Dans le workflow, après HTTP Request
// Ajouter un "Error Trigger"

// Error Trigger
On Error: This Workflow

// IF Node - Vérifier le type d'erreur
Expression: {{ $json.error.includes('API Key') }}

// Branch 1: Erreur d'authentification
→ Send Alert to Slack

// Branch 2: Autre erreur
→ Retry with exponential backoff
```

### Retry Logic

```javascript
// HTTP Request Settings
Retry On Fail: Yes
Max Tries: 3
Wait Between Tries (ms): 1000
```

---

## 📊 Monitoring avec n8n

### Workflow de Monitoring

```javascript
// Schedule Trigger (Every 5 minutes)
↓
// HTTP Request - Health Check
Method: GET
URL: http://YOUR_IP:8002/health
↓
// IF Node - Check Status
{{ $json.status !== 'ok' }}
↓
// True: Send Alert
→ Slack/Email Alert
↓
// False: Log Success
→ Airtable/Google Sheets
```

---

## 🌐 URLs Utiles

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/health` | GET | Vérifier que l'API fonctionne |
| `/api/status` | GET | Statut et configuration |
| `/api/generate` | POST | Générer les PDFs |

---

## 🎯 Checklist de Déploiement

- [ ] Serveur démarré (`./start_public_secure.sh`)
- [ ] IP locale/publique identifiée
- [ ] Port 8002 accessible
- [ ] API Key configurée dans n8n
- [ ] Health check fonctionnel
- [ ] Test de génération réussi
- [ ] Gestion des erreurs configurée
- [ ] Monitoring en place (optionnel)

---

## 💡 Tips & Astuces

### Performance

- Utilisez `singleFile: false` pour traiter des lots importants
- Le serveur traite les requêtes en parallèle (threaded)
- Timeout par défaut: 300 secondes

### Sécurité

- **Local:** Pas besoin d'API Key
- **Internet:** Toujours utiliser une API Key
- Changez l'API Key régulièrement
- Ne partagez jamais votre API Key publiquement

### Limites

- Taille maximale CSV: ~10,000 lignes recommandé
- Pas de limite stricte de requêtes
- Le serveur est single-threaded mais gère plusieurs connexions

---

## 🆘 Problèmes Courants

### "Connection refused"
```
Solution: Vérifier que le serveur est démarré
→ ./start_public.sh
```

### "API Key invalide"
```
Solution: Vérifier l'API Key
→ cat .env
```

### "Timeout"
```
Solution: Augmenter le timeout dans n8n
→ Settings → Timeout: 120000 (2 minutes)
```

### "Cannot read binary file"
```
Solution: Changer Response Format
→ HTTP Request Node → Response Format: File
```

---

**🎉 Vous êtes prêt pour n8n!**

Pour plus d'exemples, consultez: `API_DOCUMENTATION.md`


