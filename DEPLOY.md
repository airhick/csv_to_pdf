# Guide de déploiement rapide sur Netlify

## 🚀 Déploiement en 5 étapes

### 1. Préparer le projet

```bash
# Exécuter le script de préparation
./prepare_netlify.sh
```

### 2. Initialiser Git (si pas déjà fait)

```bash
git init
git add .
git commit -m "Initial commit - PDF Generator"
```

### 3. Créer un repository sur GitHub

1. Allez sur [GitHub](https://github.com/new)
2. Créez un nouveau repository (ex: `pdf-generator`)
3. **Ne cochez PAS** "Initialize with README"
4. Copiez l'URL du repository

### 4. Pousser le code

```bash
git remote add origin <URL_DE_VOTRE_REPO>
git branch -M main
git push -u origin main
```

### 5. Déployer sur Netlify

1. Allez sur [Netlify](https://app.netlify.com)
2. Cliquez sur **"Add new site"** > **"Import an existing project"**
3. Choisissez **GitHub** (ou votre plateforme Git)
4. Autorisez Netlify à accéder à vos repositories
5. Sélectionnez votre repository `pdf-generator`
6. **Paramètres de build** :
   - **Build command** : (laisser vide)
   - **Publish directory** : `.` (un point)
7. Cliquez sur **"Deploy site"**

## ✅ C'est tout !

Netlify va :
- Détecter automatiquement les fonctions dans `netlify/functions/`
- Installer les dépendances Python
- Déployer votre site

Votre application sera disponible à l'URL : `https://votre-site.netlify.app`

## 📝 Notes importantes

- **Premier déploiement** : Peut prendre 2-3 minutes
- **Fonctions Python** : Netlify installera automatiquement les dépendances depuis `netlify/functions/requirements.txt`
- **Limitations** : 
  - Timeout : 10 secondes (gratuit)
  - Taille max : 6 MB par requête

## 🔧 Test local (optionnel)

Pour tester avant de déployer :

```bash
# Installer Netlify CLI
npm install -g netlify-cli

# Démarrer le serveur local
netlify dev
```

Puis ouvrez http://localhost:8888

## 🐛 Dépannage

### Erreur "Module not found"
- Vérifiez que `add_addresses_to_pdf.py` est dans `netlify/functions/`
- Exécutez `./prepare_netlify.sh` à nouveau

### Erreur "Timeout"
- Les fichiers sont trop volumineux
- Réduisez la taille des CSV/PDF ou utilisez la version locale

### Fonction ne répond pas
- Vérifiez les logs dans le dashboard Netlify
- Section "Functions" > "Logs"

## 📚 Documentation complète

Voir `README_NETLIFY.md` pour plus de détails.

