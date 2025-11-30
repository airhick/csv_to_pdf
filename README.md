# 📄 PDF Generator API - Recto-Verso avec Nom et Adresse

Application web pour générer des PDFs recto-verso personnalisés avec nom et adresse à partir de fichiers CSV.

## ✨ Fonctionnalités

- **Upload multiple de CSV** - Plusieurs fichiers CSV simultanément
- **Détection automatique des colonnes** - Détecte `name`/`nom` et `address`/`adresse`
- **Prévisualisation des données** - Visualisez les données avant génération
- **Positionnement visuel interactif** - Drag & drop pour positionner nom et adresse
- **Génération PDF recto-verso** - Structure: Recto → Verso → Recto → Verso...
- **API REST** - Utilisable depuis n'importe quelle application

## 🚀 Installation Locale

```bash
# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur
python app.py
```

L'application sera accessible sur `http://localhost:8002`

## 📦 Déploiement

### Coolify (VPS)

Voir `DEPLOY_COOLIFY.md` pour le guide complet de déploiement sur Coolify.

## 📋 Format CSV

Vos CSV doivent contenir au minimum une de ces colonnes :

**Pour le nom:**
- `name`, `nom`, `prenom`, `firstname`, `lastname`

**Pour l'adresse:**
- `address`, `adresse`, `addr`

**Exemple:**
```csv
name,address
"Jean Dupont","123 Rue de la République\n75001 Paris\nFrance"
"Marie Martin","45 Avenue des Champs-Élysées\n75008 Paris\nFrance"
```

## 🔌 API

### Endpoint Principal

```
POST /api/generate
```

**Headers:**
```
X-API-Key: YOUR_API_KEY
Content-Type: application/json
```

**Body:**
```json
{
  "data": [
    {
      "name": "John Doe",
      "address": "123 Main Street\nNew York, NY 10001\nUSA"
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
  "singleFile": true
}
```

Voir `API_DOCUMENTATION.md` pour la documentation complète.

## 📚 Documentation

- `API_DOCUMENTATION.md` - Documentation complète de l'API
- `API_POSITIONING_GUIDE.md` - Guide de positionnement nom/adresse
- `DEPLOY_COOLIFY.md` - Guide de déploiement Coolify

## 🔒 Sécurité

Pour un usage en production, configurez :
- `REQUIRE_API_KEY=true`
- `API_KEY` avec une valeur sécurisée
- `DEBUG=false`

## 📝 Dépendances

- Python 3.11+
- Flask 3.0.0+
- PyPDF2 3.0.0+
- ReportLab 4.0.0+

---

**Version:** 2.1
