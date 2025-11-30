# 🎉 API REST Intégrée - Résumé

## ✅ Implémentation Complète

L'API REST a été **intégrée avec succès** dans votre application PDF Generator !

---

## 🚀 Quick Start

### 1. Le serveur tourne déjà sur le port 8002

```bash
# Vérifier le statut
curl -I http://localhost:8002/
# Devrait retourner: HTTP/1.1 200 OK
```

### 2. Exemple Simple - JSON

```bash
curl -X POST http://localhost:8002/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {
        "name": "Jean Dupont",
        "address": "123 Rue de la République\n75001 Paris\nFrance"
      }
    ]
  }' \
  -o output.zip
```

### 3. Test Automatique

```bash
# Lancer tous les tests
./API_QUICK_START.sh
```

---

## 📋 Endpoints Disponibles

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Interface web interactive |
| `/preview` | POST | Prévisualisation CSV (form-data) |
| `/upload` | POST | Upload CSV + génération (form-data) |
| **`/api/generate`** | POST | **API REST principale** (JSON ou form-data) |

---

## 🎯 Fonctionnalités API

### ✅ Ce que l'API fait

1. **Accepte des données JSON directes** → Pas besoin de CSV !
2. **Utilise `recto.pdf` par défaut** → Pas besoin d'uploader le recto à chaque fois
3. **Positions personnalisables** → Contrôle total sur le placement
4. **Mode Single File** → Un seul PDF avec toutes les pages
5. **Mode Multiple Files** → Un PDF par entrée dans un ZIP

### 🔧 Modes d'Utilisation

#### Mode 1: JSON (Recommandé) ✨

```bash
curl -X POST http://localhost:8002/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {"name": "Client 1", "address": "Adresse 1"},
      {"name": "Client 2", "address": "Adresse 2"}
    ],
    "namePosition": {
      "left": 20, "bottom": 250, "width": 80, "height": 30
    },
    "addressPosition": {
      "left": 95, "bottom": 20, "width": 100, "height": 40
    },
    "singleFile": true
  }' \
  -o result.pdf
```

#### Mode 2: Form-Data avec CSV

```bash
curl -X POST http://localhost:8002/api/generate \
  -F "csvFiles=@data.csv" \
  -F 'singleFile=true' \
  -o result.pdf
```

---

## 📊 Tests Réalisés

Tous les scénarios ont été testés avec succès ✅

| Test | Statut | Description |
|------|--------|-------------|
| JSON Simple | ✅ | 2 entrées, positions par défaut → ZIP avec 2 PDFs |
| Single File | ✅ | 3 entrées, mode singleFile → 1 PDF avec 6 pages |
| Positions Custom | ✅ | Positions personnalisées → PDF généré correctement |
| CSV Upload | ✅ | 2 CSV uploadés → 4 PDFs générés (concatenation OK) |

---

## 📁 Fichiers Créés

### Documentation
- ✅ **`API_DOCUMENTATION.md`** → Documentation complète (60+ lignes d'exemples)
- ✅ **`API_README.md`** → Ce fichier (résumé rapide)
- ✅ **`API_QUICK_START.sh`** → Script de test automatique

### Fichiers Template
- ✅ **`recto.pdf`** → PDF recto par défaut pour l'API
- ✅ **`rescto.pdf`** → PDF recto original (toujours disponible)

### Code
- ✅ **`app.py`** → Endpoint `/api/generate` ajouté (170 lignes de code API)

---

## 🔍 Paramètres Détaillés

### Structure JSON

```json
{
  "data": [
    {
      "name": "string (optionnel)",
      "address": "string (optionnel)"
    }
  ],
  "namePosition": {
    "left": "number (mm)",
    "bottom": "number (mm)",
    "width": "number (mm)",
    "height": "number (mm)"
  },
  "addressPosition": {
    "left": "number (mm)",
    "bottom": "number (mm)",
    "width": "number (mm)",
    "height": "number (mm)"
  },
  "singleFile": "boolean (default: false)"
}
```

### Valeurs par Défaut

**Si `namePosition` non fourni:**
```json
{"left": 20, "bottom": 250, "width": 80, "height": 30}
```

**Si `addressPosition` non fourni:**
```json
{"left": 95, "bottom": 20, "width": 100, "height": 40}
```

**PDF Recto:** `recto.pdf` (automatiquement utilisé)

---

## 💡 Exemples d'Intégration

### Python

```python
import requests

data = {
    "data": [
        {"name": "Client 1", "address": "Adresse 1"},
        {"name": "Client 2", "address": "Adresse 2"}
    ],
    "singleFile": True
}

response = requests.post(
    "http://localhost:8002/api/generate",
    json=data
)

with open('output.pdf', 'wb') as f:
    f.write(response.content)
```

### JavaScript/Node.js

```javascript
const axios = require('axios');
const fs = require('fs');

const data = {
  data: [
    { name: "Client 1", address: "Adresse 1" },
    { name: "Client 2", address: "Adresse 2" }
  ],
  singleFile: true
};

axios.post('http://localhost:8002/api/generate', data, {
  responseType: 'arraybuffer'
})
.then(response => {
  fs.writeFileSync('output.pdf', response.data);
  console.log('✓ PDF généré');
});
```

### PHP

```php
<?php
$data = [
    'data' => [
        ['name' => 'Client 1', 'address' => 'Adresse 1'],
        ['name' => 'Client 2', 'address' => 'Adresse 2']
    ],
    'singleFile' => true
];

$ch = curl_init('http://localhost:8002/api/generate');
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$result = curl_exec($ch);
file_put_contents('output.pdf', $result);
curl_close($ch);

echo "✓ PDF généré\n";
?>
```

---

## 🎨 Use Cases

### 1. Service de Mailing Automatisé
```python
# Récupérer les clients depuis la DB
clients = fetch_clients_from_database()

# Générer les PDFs
response = requests.post('/api/generate', json={
    'data': [{'name': c.name, 'address': c.address} for c in clients],
    'singleFile': False
})

# Télécharger le ZIP et envoyer par email
send_bulk_mail(response.content)
```

### 2. Génération à la Volée
```javascript
// Frontend → Backend → API PDF
app.post('/generate-invoice', async (req, res) => {
  const pdfData = {
    data: [{
      name: req.body.customerName,
      address: req.body.customerAddress
    }],
    singleFile: true
  };
  
  const pdf = await axios.post('http://pdf-service:8002/api/generate', pdfData);
  res.set('Content-Type', 'application/pdf');
  res.send(pdf.data);
});
```

### 3. Traitement Batch
```bash
#!/bin/bash
# Script pour traiter plusieurs listes de clients

for customer_list in data/*.json; do
  output_name=$(basename "$customer_list" .json)
  
  curl -X POST http://localhost:8002/api/generate \
    -H "Content-Type: application/json" \
    -d @"$customer_list" \
    -o "output/${output_name}.zip"
  
  echo "✓ Traité: $customer_list"
done
```

---

## 📦 Structure des Réponses

### Succès - Single File
```
HTTP/1.1 200 OK
Content-Type: application/pdf
Content-Disposition: attachment; filename="generated.pdf"

[Binary PDF Data]
```

### Succès - Multiple Files
```
HTTP/1.1 200 OK
Content-Type: application/zip
Content-Disposition: attachment; filename="generated_pdfs.zip"

[Binary ZIP Data]
```

### Erreur
```json
{
  "error": "Message d'erreur détaillé",
  "log": "Logs du processus (si disponible)"
}
```

---

## 🔐 Considérations de Production

L'API actuelle est configurée pour un **usage local/développement**.

### Pour la Production
- [ ] Ajouter une authentification (API Key / JWT)
- [ ] Implémenter du rate limiting
- [ ] Configurer HTTPS
- [ ] Valider/sanitiser toutes les entrées
- [ ] Ajouter des logs d'audit
- [ ] Gérer les timeouts pour gros volumes
- [ ] Mettre en place un système de queue pour traitements longs

---

## 📞 Support

### Documentation Complète
```bash
cat API_DOCUMENTATION.md
```

### Tests Automatiques
```bash
./API_QUICK_START.sh
```

### Logs en Temps Réel
```bash
# Dans le terminal où tourne le serveur
# Les logs s'affichent automatiquement
```

---

## ✨ Résumé

🎯 **Objectif atteint:** API REST complète et fonctionnelle

✅ **Fonctionnalités:**
- JSON direct → Pas besoin de CSV
- PDF recto par défaut (`recto.pdf`)
- Positions personnalisables
- Single file ou multiple files
- Compatible CSV pour rétrocompatibilité

🧪 **Tests:** Tous passent ✓

📚 **Documentation:** Complète avec 20+ exemples

🚀 **Prêt à l'emploi!**

---

**Version:** 2.1  
**Date:** Novembre 2025  
**Endpoint:** `http://localhost:8002/api/generate`

