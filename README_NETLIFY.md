# Déploiement sur Netlify

Ce guide explique comment déployer l'application de génération de PDFs sur Netlify.

## Prérequis

- Un compte Netlify (gratuit)
- Git installé
- Les fichiers du projet

## Méthode 1 : Déploiement via Git (Recommandé)

### 1. Initialiser Git (si pas déjà fait)

```bash
git init
git add .
git commit -m "Initial commit"
```

### 2. Créer un repository sur GitHub/GitLab/Bitbucket

1. Créez un nouveau repository sur votre plateforme Git préférée
2. Poussez votre code :

```bash
git remote add origin <URL_DE_VOTRE_REPO>
git push -u origin main
```

### 3. Déployer sur Netlify

1. Connectez-vous à [Netlify](https://app.netlify.com)
2. Cliquez sur "Add new site" > "Import an existing project"
3. Choisissez votre plateforme Git (GitHub, GitLab, etc.)
4. Sélectionnez votre repository
5. Configurez les paramètres de build :
   - **Build command** : (laisser vide ou `echo "No build required"`)
   - **Publish directory** : `.` (point)
6. Cliquez sur "Deploy site"

### 4. Configuration des fonctions

Netlify détectera automatiquement les fonctions dans `netlify/functions/`. 

**Important** : Netlify Functions avec Python nécessite que les dépendances soient installées. Vous devrez peut-être :

1. Créer un fichier `runtime.txt` dans `netlify/functions/` :
```
python-3.9
```

2. Ou utiliser le plugin Netlify Functions (déjà configuré dans `netlify.toml`)

## Méthode 2 : Déploiement via Netlify CLI

### 1. Installer Netlify CLI

```bash
npm install -g netlify-cli
```

### 2. Se connecter

```bash
netlify login
```

### 3. Déployer

```bash
netlify deploy --prod
```

## Configuration

Le fichier `netlify.toml` contient la configuration :

```toml
[build]
  publish = "."
  functions = "netlify/functions"

[build.environment]
  PYTHON_VERSION = "3.9"
```

## Limitations de Netlify Functions

⚠️ **Important** : Netlify Functions a certaines limitations :

- **Timeout** : 10 secondes (gratuit) ou 26 secondes (pro)
- **Taille de payload** : 6 MB maximum
- **Mémoire** : Limitée selon le plan

Pour des fichiers CSV/PDF volumineux, vous pourriez rencontrer des limitations. Dans ce cas, considérez :
- Utiliser un service backend dédié (Vercel, Railway, etc.)
- Traiter les fichiers par lots
- Utiliser la version locale de l'application

## Structure des fichiers

```
.
├── index.html              # Interface web
├── netlify.toml           # Configuration Netlify
├── package.json           # Configuration npm
├── netlify/
│   └── functions/
│       ├── generate-pdfs.py    # Fonction serverless
│       └── requirements.txt    # Dépendances Python
└── add_addresses_to_pdf.py    # Module principal
```

## Test local

Pour tester localement avant de déployer :

```bash
# Installer Netlify CLI
npm install -g netlify-cli

# Démarrer le serveur de développement
netlify dev
```

Cela lancera un serveur local avec les fonctions Netlify.

## Dépannage

### Erreur : "Module not found"

Assurez-vous que `requirements.txt` est présent dans `netlify/functions/` et contient toutes les dépendances.

### Erreur : "Timeout"

Les fichiers sont trop volumineux ou le traitement prend trop de temps. Considérez :
- Réduire la taille des fichiers
- Traiter par lots
- Utiliser un service backend dédié

### Erreur : "Function not found"

Vérifiez que :
- Le fichier `generate-pdfs.py` est dans `netlify/functions/`
- Le fichier `netlify.toml` est correctement configuré
- Les fonctions sont déployées (vérifiez dans le dashboard Netlify)

## Support

Pour plus d'informations, consultez :
- [Documentation Netlify Functions](https://docs.netlify.com/functions/overview/)
- [Netlify Python Functions](https://docs.netlify.com/functions/language-support/#python)

