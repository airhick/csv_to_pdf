# 🚂 Déploiement sur Railway

Railway est **la meilleure option pour déployer votre API Flask** sur le cloud avec un accès permanent.

## Pourquoi Railway ?

- ✅ **Gratuit** : 500 heures/mois (suffisant pour usage régulier)
- ✅ **URL permanente** : `https://your-app.up.railway.app`
- ✅ **HTTPS inclus** : Sécurité automatique
- ✅ **Déploiement simple** : 5 minutes chrono
- ✅ **Auto-redéploiement** : Push sur Git → déploie automatiquement
- ✅ **Logs en temps réel** : Monitoring facile
- ✅ **Environnement variables** : API Key sécurisée

---

## 🚀 Déploiement en 5 Minutes

### Étape 1 : Créer un compte Railway

1. Allez sur [railway.app](https://railway.app)
2. Inscrivez-vous avec GitHub (recommandé)
3. Vérifiez votre email

### Étape 2 : Préparer le repository Git

```bash
# Si pas déjà fait, initialiser Git
git init
git add .
git commit -m "Ready for Railway deployment"

# Créer un repo sur GitHub (si nécessaire)
# Puis:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Étape 3 : Déployer sur Railway

#### Option A : Via Dashboard (Plus Simple)

1. Connectez-vous à [Railway Dashboard](https://railway.app/dashboard)
2. Cliquez sur **"New Project"**
3. Sélectionnez **"Deploy from GitHub repo"**
4. Choisissez votre repository
5. Railway détectera automatiquement Python et Flask
6. Cliquez **"Deploy"**

#### Option B : Via CLI (Plus Rapide)

```bash
# Installer Railway CLI
npm install -g @railway/cli

# Ou avec brew
brew install railway

# Se connecter
railway login

# Initialiser le projet
railway init

# Déployer
railway up
```

### Étape 4 : Configuration

Une fois déployé, configurez les variables d'environnement :

1. Dans le dashboard Railway, allez dans **"Variables"**
2. Ajoutez :
```
REQUIRE_API_KEY=true
API_KEY=your_secure_api_key_here
HOST=0.0.0.0
PORT=8002
DEBUG=False
```

3. Railway redémarrera automatiquement avec la nouvelle config

### Étape 5 : Obtenir votre URL

1. Dans le dashboard, allez dans **"Settings"**
2. Section **"Domains"**
3. Cliquez **"Generate Domain"**
4. Vous obtiendrez une URL comme : `https://your-app.up.railway.app`

---

## 🎯 Utilisation de votre API Railway

### URL de base

```
https://your-app.up.railway.app
```

### Endpoints

```bash
# Health Check
curl https://your-app.up.railway.app/health

# API Status
curl https://your-app.up.railway.app/api/status

# Generate PDF
curl -X POST https://your-app.up.railway.app/api/generate \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {"name": "Jean Dupont", "address": "123 Rue Paris"}
    ],
    "singleFile": true
  }' \
  -o output.pdf
```

### Dans n8n

**HTTP Request Node:**
- **URL:** `https://your-app.up.railway.app/api/generate`
- **Method:** POST
- **Headers:**
  - `X-API-Key`: `your_api_key`
  - `Content-Type`: `application/json`
- **Body:**
```json
{
  "data": [
    {
      "name": "{{ $json.name }}",
      "address": "{{ $json.address }}"
    }
  ],
  "singleFile": true
}
```
- **Response Format:** File

---

## 📊 Monitoring & Logs

### Voir les logs en temps réel

**Via Dashboard:**
1. Ouvrez votre projet Railway
2. Allez dans l'onglet **"Deployments"**
3. Cliquez sur le déploiement actif
4. Les logs s'affichent en temps réel

**Via CLI:**
```bash
railway logs
```

### Métriques

Railway affiche automatiquement :
- CPU usage
- Memory usage
- Network traffic
- Request count

---

## 🔐 Sécurité

### API Key

**Générer une API Key sécurisée:**

```bash
# Méthode 1: Python
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Méthode 2: OpenSSL
openssl rand -base64 32

# Méthode 3: UUID
uuidgen
```

Ajoutez-la dans les variables d'environnement Railway.

### HTTPS

- ✅ Railway fournit **automatiquement** HTTPS
- ✅ Certificats SSL gérés automatiquement
- ✅ Renouvellement automatique

### Variables Sensibles

**Ne jamais** committer `.env` dans Git. Toujours utiliser les variables Railway.

---

## 🔄 Mises à Jour Automatiques

### Configuration du Auto-Deploy

Railway redéploie automatiquement quand vous poussez sur Git :

```bash
# Faire des modifications
vim app.py

# Committer et pousser
git add .
git commit -m "Update API"
git push origin main

# Railway redéploie automatiquement ! 🎉
```

### Voir l'historique des déploiements

Dans le dashboard :
- Onglet **"Deployments"**
- Liste de tous les déploiements
- Possibilité de rollback à une version précédente

---

## 💰 Coûts

### Plan Gratuit (Trial)

- ✅ **500 heures d'exécution/mois**
- ✅ **1 GB RAM**
- ✅ **1 GB stockage**
- ✅ **Parfait pour développement et usage modéré**

**Calcul:**
- Si votre API tourne 24/7 : ~720h/mois → dépassement
- Si vous démarrez/arrêtez : largement suffisant
- Si usage occasionnel : parfait

### Optimisation

**Activer le "Sleep on Idle"** (si usage occasionnel):
1. Settings → Sleep Application
2. L'app se met en veille après 5 min d'inactivité
3. Se réveille automatiquement à la première requête
4. **Économise vos heures gratuites**

### Plan Hobby ($5/mois)

Si vous dépassez :
- ✅ Usage illimité
- ✅ Meilleure priorité
- ✅ Pas de limitations

---

## 🐛 Dépannage

### L'application ne démarre pas

**Vérifier les logs:**
```bash
railway logs
```

**Causes communes:**
1. Mauvais `PORT` : Railway utilise `$PORT` automatiquement
2. Dépendances manquantes : Vérifier `requirements.txt`
3. Erreurs Python : Voir les logs

**Solution:**

Dans `app.py`, ligne 350, assurez-vous d'avoir :

```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8002))  # Railway fournit PORT
    host = os.environ.get('HOST', '0.0.0.0')
    # ...
    app.run(host=host, port=port, debug=debug_mode, threaded=True)
```

### Timeout / 502 Bad Gateway

**Causes:**
- Le serveur met trop de temps à répondre
- Traitement de gros PDFs/CSV

**Solutions:**
1. Optimiser le traitement
2. Augmenter le timeout Railway (dans les settings)
3. Traiter par lots

### Build Failed

**Vérifier:**
1. `requirements.txt` est complet et à jour
2. Python version compatible (Railway supporte 3.9+)
3. Pas de dépendances système manquantes

### Variable d'environnement non définie

```bash
# Via CLI
railway variables set REQUIRE_API_KEY=true
railway variables set API_KEY=your_key

# Ou via le dashboard
```

---

## 📚 Commandes Utiles

```bash
# Se connecter
railway login

# Lier un projet existant
railway link

# Déployer
railway up

# Voir les logs
railway logs

# Ouvrir le dashboard
railway open

# Ouvrir l'URL de l'app
railway open --app

# Exécuter une commande sur Railway
railway run python --version

# Lister les variables
railway variables

# Définir une variable
railway variables set KEY=VALUE

# Redémarrer
railway restart

# État du projet
railway status
```

---

## 🎨 Custom Domain (Optionnel)

Si vous avez votre propre domaine (ex: `api.monsite.com`) :

1. Dans Railway : Settings → Domains → **"Add Custom Domain"**
2. Entrez : `api.monsite.com`
3. Railway vous donne un CNAME
4. Allez chez votre registrar de domaine (OVH, Cloudflare, etc.)
5. Ajoutez un CNAME record :
   ```
   api.monsite.com → your-app.up.railway.app
   ```
6. Attendez la propagation DNS (5-30 minutes)
7. ✅ Votre API est accessible sur votre domaine !

---

## 🆚 Comparaison avec autres services

| Feature | Railway | Netlify | Render | Heroku |
|---------|---------|---------|--------|--------|
| Gratuit | 500h/mois | Limité (timeout 10s) | 750h/mois | Non (plus gratuit) |
| Setup | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Python Flask | ✅ Excellent | ⚠️ Limité | ✅ Bon | ✅ Bon |
| HTTPS | ✅ Auto | ✅ Auto | ✅ Auto | ✅ Auto |
| Custom Domain | ✅ Gratuit | ✅ Gratuit | ✅ Gratuit | 💰 Payant |
| Logs | ✅ Temps réel | ⚠️ Basique | ✅ Temps réel | ✅ Temps réel |
| Prix (paid) | $5/mois | $19/mois | $7/mois | $7/mois |

**Verdict:** Railway est le meilleur choix pour votre API Flask.

---

## ✅ Checklist Finale

Avant de mettre en production :

- [ ] Code poussé sur GitHub
- [ ] Projet créé sur Railway
- [ ] Déploiement réussi
- [ ] Variables d'environnement configurées (API_KEY, etc.)
- [ ] URL générée et testée
- [ ] API Key testée
- [ ] Endpoint `/health` fonctionne
- [ ] Endpoint `/api/generate` fonctionne
- [ ] Test avec n8n réussi
- [ ] Monitoring/logs vérifiés

---

## 🎉 Résultat Final

Une fois déployé, vous aurez :

✅ **URL permanente:** `https://your-app.up.railway.app`  
✅ **Accessible de partout:** n8n, Zapier, Make, etc.  
✅ **HTTPS sécurisé:** Automatique  
✅ **Logs en temps réel:** Monitoring facile  
✅ **Mises à jour automatiques:** Push to deploy  
✅ **Aucune configuration réseau:** Pas de port forwarding  
✅ **Gratuit (jusqu'à 500h/mois):** Parfait pour commencer  

**Votre API est maintenant accessible depuis n'importe où, 24/7, de manière professionnelle !**

---

## 🔗 Liens Utiles

- [Railway Dashboard](https://railway.app/dashboard)
- [Railway Documentation](https://docs.railway.app)
- [Railway Community](https://discord.gg/railway)
- [Railway CLI Reference](https://docs.railway.app/develop/cli)

---

**Date:** Novembre 2024  
**Version:** 1.0

