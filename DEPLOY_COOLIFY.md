# 🚀 Déploiement sur Coolify

Guide simple pour déployer votre API PDF Generator sur Coolify.

## 📋 Prérequis

- Un VPS avec Coolify installé
- Votre code dans un repository Git (GitHub, GitLab, etc.)
- Accès à votre instance Coolify

## 🎯 Étapes de Déploiement

### 1. Préparer votre Repository

Assurez-vous que votre code est poussé sur GitHub/GitLab :

```bash
git add .
git commit -m "Ready for Coolify deployment"
git push
```

### 2. Créer une Application dans Coolify

1. Connectez-vous à votre instance Coolify
2. Allez dans **Projects** → **Create a new Application**
3. Sélectionnez votre repository Git
4. Cliquez sur **Load Repository**

### 3. Configuration dans Coolify

**Repository:** Votre repo (ex: `csv_to_pdf`)

**Configuration:**
- **Branch:** `main` (ou votre branche par défaut)
- **Build Pack:** `Dockerfile` ⚠️ **IMPORTANT:** Sélectionnez explicitement "Dockerfile" (ne pas laisser sur "Nixpacks")
- **Base Directory:** `/` (laisser vide ou `/`)
- **Port:** `8002` ⚠️ **IMPORTANT:** Changez de 3000 à 8002
- **Is it a static site?:** ❌ Non (décocher)

### 4. Variables d'Environnement

Dans Coolify, ajoutez ces variables d'environnement :

| Variable | Valeur | Description |
|----------|--------|-------------|
| `PORT` | `8002` | Port de l'application (Coolify peut aussi le définir automatiquement) |
| `HOST` | `0.0.0.0` | Écouter sur toutes les interfaces |
| `DEBUG` | `false` | Désactiver le mode debug en production |
| `REQUIRE_API_KEY` | `true` | Activer la protection par API key |
| `API_KEY` | `votre-cle-secrete` | **Générer une clé sécurisée** (voir ci-dessous) |

**Générer une API Key sécurisée:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. Déployer

1. Cliquez sur **Continue**
2. Coolify va :
   - Cloner votre repository
   - Construire l'image Docker
   - Démarrer le conteneur
3. Attendez 2-3 minutes pour le premier déploiement

### 6. Accéder à votre Application

Une fois déployé, Coolify vous donnera une URL comme :
```
https://votre-app.votre-domaine.com
```

**Endpoints disponibles:**
- Interface web: `https://votre-app.votre-domaine.com/`
- Health check: `https://votre-app.votre-domaine.com/health`
- API: `https://votre-app.votre-domaine.com/api/generate`

## 🧪 Tester l'API

### Health Check
```bash
curl https://votre-app.votre-domaine.com/health
```

### Générer un PDF
```bash
curl -X POST https://votre-app.votre-domaine.com/api/generate \
  -H "X-API-Key: VOTRE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {
        "name": "Test User",
        "address": "123 Main Street\nCity, State\nCountry"
      }
    ],
    "singleFile": true
  }' \
  -o test.pdf
```

## 🔧 Configuration Avancée

### Port Personnalisé

Si vous voulez utiliser un port différent, modifiez la variable `PORT` dans Coolify. L'application utilise automatiquement la variable d'environnement `PORT`.

### Fichiers PDF Templates

Les fichiers `recto.pdf` ou `rescto.pdf` doivent être dans votre repository pour être utilisés comme templates par défaut. Sinon, vous pouvez toujours uploader un PDF via l'interface web ou l'API.

### Redéploiement Automatique

Coolify peut redéployer automatiquement quand vous poussez sur votre branche :
1. Allez dans les **Settings** de votre application
2. Activez **Auto Deploy** pour votre branche

## 🐛 Dépannage

### Coolify détecte Node.js au lieu de Python

**Symptôme:** Les logs montrent `npm ci` ou `npm run build` au lieu de `pip install`

**Solution:**
1. Dans Coolify, allez dans les **Settings** de votre application
2. Changez **Build Pack** de "Nixpacks" à **"Dockerfile"**
3. Redéployez

### L'application ne démarre pas

1. Vérifiez les **Logs** dans Coolify
2. Vérifiez que toutes les variables d'environnement sont définies
3. Vérifiez que le port est `8002` (pas 3000)
4. Vérifiez que le Build Pack est bien "Dockerfile"

### Erreur "Module not found"

Vérifiez que `requirements.txt` contient toutes les dépendances :
- Flask>=3.0.0
- PyPDF2>=3.0.0
- ReportLab>=4.0.0

### L'API ne répond pas

1. Vérifiez que `REQUIRE_API_KEY=true` et `API_KEY` sont définis
2. Testez avec `/health` (pas besoin d'API key)
3. Vérifiez les logs dans Coolify

## 📚 Documentation API

Voir `API_DOCUMENTATION.md` pour la documentation complète de l'API.

---

**C'est tout ! Votre API est maintenant déployée sur Coolify.** 🎉

