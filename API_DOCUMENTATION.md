# 🚀 API Documentation - PDF Generator

## Base URL
```
http://localhost:8002
```

## Endpoints

### 1. `POST /api/generate` - Générer des PDFs avec nom et adresse

Endpoint principal pour générer des PDFs recto-verso avec positionnement personnalisé du nom et de l'adresse.

---

## 📋 Modes d'Utilisation

### Mode 1️⃣ : JSON Direct (Recommandé)

Envoyez directement les données en JSON sans avoir besoin de fichiers CSV.

**Headers:**
```
Content-Type: application/json
```

**Body Structure:**
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
  },
  "singleFile": false
}
```

**Paramètres:**

| Paramètre | Type | Requis | Description |
|-----------|------|---------|-------------|
| `data` | Array | ✅ Oui | Liste d'objets avec `name` et `address` |
| `data[].name` | String | Non | Nom à afficher sur le verso |
| `data[].address` | String | Non | Adresse à afficher sur le verso |
| `namePosition` | Object | Non | Position de la zone nom (voir ci-dessous) |
| `addressPosition` | Object | Non | Position de la zone adresse (voir ci-dessous) |
| `singleFile` | Boolean | Non | `true` pour un seul PDF, `false` pour un PDF par entrée (défaut: `false`) |

**Position Object:**
```json
{
  "left": 20,      // Distance depuis la gauche (mm)
  "bottom": 250,   // Distance depuis le bas (mm)
  "width": 80,     // Largeur de la zone (mm)
  "height": 30     // Hauteur de la zone (mm)
}
```

**Positions par défaut si non spécifiées:**

- **Name:** `{"left": 20, "bottom": 250, "width": 80, "height": 30}`
- **Address:** `{"left": 95, "bottom": 20, "width": 100, "height": 40}`

**Response:**
- Si `singleFile: false` → Retourne un **ZIP** avec tous les PDFs
- Si `singleFile: true` → Retourne un **PDF unique** avec toutes les pages

---

### Mode 2️⃣ : Form-Data avec CSV

Uploadez des fichiers CSV comme avec l'interface web.

**Headers:**
```
Content-Type: multipart/form-data
```

**Form Fields:**

| Field | Type | Requis | Description |
|-------|------|---------|-------------|
| `csvFiles` | File(s) | ✅ Oui | Un ou plusieurs fichiers CSV |
| `pdfFile` | File | Non | PDF recto personnalisé (sinon utilise `recto.pdf`) |
| `namePosition` | String (JSON) | Non | Position de la zone nom (JSON stringifié) |
| `addressPosition` | String (JSON) | Non | Position de la zone adresse (JSON stringifié) |
| `singleFile` | String | Non | `"true"` ou `"false"` |

**Format CSV:**
```csv
name,address
"Jean Dupont","123 Rue de la République\n75001 Paris\nFrance"
"Marie Martin","45 Avenue des Champs-Élysées\n75008 Paris\nFrance"
```

Les colonnes peuvent aussi être nommées : `nom`, `adresse`, `firstname`, `lastname`, etc.

---

## 📝 Exemples d'Utilisation

### Exemple 1: JSON Simple (Positions par défaut)

```bash
curl -X POST http://localhost:8002/api/generate \
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
  -o output.zip
```

### Exemple 2: JSON avec Positions Personnalisées

```bash
curl -X POST http://localhost:8002/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {
        "name": "Pierre Durand",
        "address": "78 Boulevard Saint-Germain\n75006 Paris\nFrance"
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
  -o output.pdf
```

### Exemple 3: JSON avec Single File

```bash
curl -X POST http://localhost:8002/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {"name": "Client 1", "address": "Adresse 1"},
      {"name": "Client 2", "address": "Adresse 2"},
      {"name": "Client 3", "address": "Adresse 3"}
    ],
    "singleFile": true
  }' \
  -o all_clients.pdf
```

Ce fichier contiendra 6 pages : Recto1, Verso1, Recto2, Verso2, Recto3, Verso3

### Exemple 4: Form-Data avec CSV

```bash
curl -X POST http://localhost:8002/api/generate \
  -F "csvFiles=@clients1.csv" \
  -F "csvFiles=@clients2.csv" \
  -F 'namePosition={"left":20,"bottom":250,"width":80,"height":30}' \
  -F 'addressPosition={"left":95,"bottom":20,"width":100,"height":40}' \
  -o output.zip
```

### Exemple 5: Form-Data avec PDF Recto Personnalisé

```bash
curl -X POST http://localhost:8002/api/generate \
  -F "csvFiles=@data.csv" \
  -F "pdfFile=@mon_template.pdf" \
  -F 'singleFile=true' \
  -o result.pdf
```

### Exemple 6: Python avec Requests

```python
import requests
import json

url = "http://localhost:8002/api/generate"

data = {
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
    },
    "singleFile": False
}

response = requests.post(url, json=data)

if response.status_code == 200:
    with open('output.zip', 'wb') as f:
        f.write(response.content)
    print("✓ ZIP généré avec succès")
else:
    print(f"✗ Erreur: {response.json()}")
```

### Exemple 7: JavaScript/Node.js

```javascript
const axios = require('axios');
const fs = require('fs');

const data = {
  data: [
    {
      name: "Jean Dupont",
      address: "123 Rue de la République\\n75001 Paris\\nFrance"
    },
    {
      name: "Marie Martin",
      address: "45 Avenue des Champs-Élysées\\n75008 Paris\\nFrance"
    }
  ],
  namePosition: {
    left: 20,
    bottom: 250,
    width: 80,
    height: 30
  },
  addressPosition: {
    left: 95,
    bottom: 20,
    width: 100,
    height: 40
  },
  singleFile: false
};

axios.post('http://localhost:8002/api/generate', data, {
  responseType: 'arraybuffer'
})
.then(response => {
  fs.writeFileSync('output.zip', response.data);
  console.log('✓ ZIP généré avec succès');
})
.catch(error => {
  console.error('✗ Erreur:', error.response?.data || error.message);
});
```

---

## 📤 Réponses

### Succès (200 OK)

**Single File:**
```
Content-Type: application/pdf
Content-Disposition: attachment; filename="generated.pdf"

[PDF Binary Data]
```

**Multiple Files:**
```
Content-Type: application/zip
Content-Disposition: attachment; filename="generated_pdfs.zip"

[ZIP Binary Data]
```

### Erreurs

**400 Bad Request:**
```json
{
  "error": "Le champ \"data\" est requis"
}
```

**500 Internal Server Error:**
```json
{
  "error": "Message d'erreur détaillé",
  "log": "Logs du traitement (si disponible)"
}
```

---

## 🎯 Cas d'Usage

### 1. Service Web Intégré
Intégrez l'API dans votre application web pour générer des PDFs à la volée :
```javascript
// Frontend envoie les données
const response = await fetch('/api/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ data: customers })
});

const blob = await response.blob();
// Télécharger ou afficher le PDF
```

### 2. Traitement Batch
Générez des PDFs en masse depuis un script :
```bash
#!/bin/bash
for file in data/*.csv; do
  curl -X POST http://localhost:8002/api/generate \
    -F "csvFiles=@$file" \
    -o "output/$(basename $file .csv).zip"
done
```

### 3. Microservice
Déployez l'API comme microservice et appelez-la depuis d'autres services :
```python
# Service A génère les données
customers = fetch_customers_from_db()

# Appel au microservice PDF
response = requests.post(
    'http://pdf-service:8002/api/generate',
    json={'data': customers}
)

# Envoyer le PDF par email
send_email(attachment=response.content)
```

---

## 🔧 Configuration Avancée

### PDF Recto par Défaut

Par défaut, l'API utilise le fichier **`recto.pdf`** comme template recto.

Pour utiliser un autre fichier par défaut :
1. Remplacez le fichier `recto.pdf` dans le dossier de l'application
2. Ou uploadez un PDF personnalisé via le champ `pdfFile` (mode form-data)

### Positions Optimales

Pour une **fenêtre d'enveloppe standard** (DL avec fenêtre à droite) :

**Adresse:**
```json
{
  "left": 95,
  "bottom": 20,
  "width": 100,
  "height": 40
}
```

Pour un **positionnement nom + adresse complet** :

**Nom (en haut à gauche):**
```json
{
  "left": 20,
  "bottom": 250,
  "width": 80,
  "height": 30
}
```

**Adresse (milieu à droite):**
```json
{
  "left": 95,
  "bottom": 20,
  "width": 100,
  "height": 40
}
```

---

## 📊 Limites et Performances

- **Taille maximale CSV**: Aucune limite stricte, mais recommandé < 10 000 lignes par requête
- **Timeout**: 300 secondes (5 minutes) par défaut
- **Format adresse**: Les sauts de ligne `\n` sont supportés
- **Encodage**: UTF-8 requis pour les caractères spéciaux

---

## 🔒 Sécurité

⚠️ **Important**: Cette API est conçue pour un usage **local** ou en **réseau privé**.

Pour une utilisation en production :
1. Ajoutez une **authentification** (API Key, JWT, OAuth)
2. Configurez des **rate limits**
3. Validez et sanitisez toutes les entrées
4. Utilisez HTTPS
5. Ajoutez des logs d'audit

---

## 🆘 Support

### Logs
Pour voir les logs détaillés :
```bash
# Dans le terminal où le serveur tourne
# Les logs s'affichent en temps réel
```

### Debug
Activez le mode debug dans `app.py` :
```python
app.run(host='127.0.0.1', port=8002, debug=True)
```

### Vérifier le service
```bash
curl -I http://localhost:8002/
# Doit retourner: HTTP/1.1 200 OK
```

---

## 📜 Changelog API

**Version 2.0** (Novembre 2025)
- ✅ Ajout endpoint `/api/generate`
- ✅ Support JSON direct
- ✅ Support form-data avec CSV
- ✅ Utilisation automatique de `recto.pdf` par défaut
- ✅ Support positions personnalisées
- ✅ Mode single file ou multiple files

---

**API ready to use! 🚀**

