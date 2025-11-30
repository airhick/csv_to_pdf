# 🎉 Nouvelles Fonctionnalités - Générateur PDF Recto-Verso

## 📋 Vue d'ensemble

Cette application web permet de générer des PDFs recto-verso personnalisés avec nom et adresse, à partir de plusieurs fichiers CSV et d'un template PDF.

## ✨ Fonctionnalités Principales

### 1. **Upload Multiple de CSV** 📁
- Uploadez **plusieurs fichiers CSV simultanément**
- Les fichiers sont automatiquement **concatenés** dans l'ordre
- Détection automatique des délimiteurs (`,`, `;`, `\t`)

### 2. **Détection Intelligente des Colonnes** 🔍
- Détection automatique des colonnes **Name** (ou `nom`, `prenom`, `firstname`, `lastname`)
- Détection automatique des colonnes **Address** (ou `adresse`, `addr`)
- Compatible avec des **noms de colonnes différents** entre les CSV

### 3. **Prévisualisation des Données** 👁️
- Visualisez toutes les données concatenées **avant génération**
- Tableau interactif affichant :
  - Numéro de ligne
  - Nom
  - Adresse
- Statistiques : nombre total de lignes, colonnes détectées

### 4. **Positionnement Visuel Interactif** 🎨
- **2 rectangles draggables** indépendants :
  - 🟢 **Zone Nom** (verte)
  - 🔵 **Zone Adresse** (bleue)
- **Drag & Drop** : déplacez les zones sur la page A4
- **Redimensionnement** : ajustez la taille avec les poignées
- **Coordonnées en temps réel** :
  - Distance depuis les bords (gauche, bas)
  - Largeur et hauteur de chaque zone

### 5. **Génération PDF Recto-Verso** 📄
- **Recto** : votre template PDF (ex: `rescto.pdf`)
- **Verso** : page blanche avec nom et adresse positionnés
- Structure : `Recto 1 → Verso 1 → Recto 2 → Verso 2 → ...`
- Export au format **ZIP** contenant tous les PDFs

## 🚀 Utilisation

### Démarrage du Serveur

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Lancer le serveur sur le port 8002
python app.py
```

Le serveur démarre sur **http://localhost:8002**

### Workflow Complet

1. **Ouvrez votre navigateur** : `http://localhost:8002`

2. **Uploadez vos CSV** :
   - Cliquez sur "Choisir un ou plusieurs fichiers CSV"
   - Sélectionnez tous vos fichiers CSV (CTRL+clic pour multi-sélection)
   - Cliquez sur "👁️ Prévisualiser les données"

3. **Vérifiez la Prévisualisation** :
   - Consultez le tableau avec toutes les données concatenées
   - Vérifiez que les colonnes sont correctement détectées

4. **Uploadez votre PDF Template** :
   - Sélectionnez votre fichier PDF recto (ex: `rescto.pdf`)

5. **Positionnez le Nom et l'Adresse** :
   - **Déplacez** les rectangles verts (nom) et bleu (adresse)
   - **Redimensionnez** si nécessaire
   - Utilisez le bouton "Réinitialiser" pour revenir aux positions par défaut

6. **Générez les PDFs** :
   - Cliquez sur "🎉 Générer les PDFs et créer le ZIP"
   - Le ZIP se télécharge automatiquement

## 📁 Format des Fichiers CSV

### Structure Requise

Vos CSV doivent contenir au minimum **une** des colonnes suivantes :

**Pour le nom** (au moins une de ces colonnes) :
- `name` / `nom` / `prenom` / `firstname` / `lastname`

**Pour l'adresse** (au moins une de ces colonnes) :
- `address` / `adresse` / `addr`

### Exemple 1 : CSV avec colonnes anglaises

```csv
name,address
"Jean Dupont","123 Rue de la République\n75001 Paris\nFrance"
"Marie Martin","45 Avenue des Champs-Élysées\n75008 Paris\nFrance"
```

### Exemple 2 : CSV avec colonnes françaises

```csv
nom,adresse
"Pierre Durand","78 Boulevard Saint-Germain\n75006 Paris\nFrance"
"Sophie Bernard","12 Rue de Rivoli\n75004 Paris\nFrance"
```

### Notes Importantes

- Les **sauts de ligne** dans les adresses : utilisez `\n` ou de vrais sauts de ligne
- Les **guillemets** sont recommandés pour les champs multi-lignes
- Les **colonnes vides** : les lignes sans nom ET sans adresse sont ignorées

## 🔧 Configuration Technique

### Positions par Défaut

**Zone Nom** (🟢) :
- Gauche : 20 mm
- Bas : 250 mm
- Largeur : 80 mm
- Hauteur : 30 mm

**Zone Adresse** (🔵) :
- Gauche : 95 mm
- Bas : 20 mm
- Largeur : 100 mm
- Hauteur : 40 mm

### Dimensions Page

- Format : **A4** (210 mm × 297 mm)
- Orientation : **Portrait**
- Alignement du texte : **À droite** dans chaque zone

## 🎯 Cas d'Usage

### Cas 1 : Envoi de courriers en masse
- Uploadez votre liste de destinataires (plusieurs fichiers CSV)
- Positionnez l'adresse pour correspondre à la fenêtre d'enveloppe
- Générez les PDFs prêts à imprimer

### Cas 2 : Cartes de visite personnalisées
- CSV avec noms et coordonnées
- Positionnez les informations selon votre design
- Imprimez recto-verso

### Cas 3 : Fusion de plusieurs bases de données
- Plusieurs CSV avec des formats différents
- Concatenation automatique
- Export unifié

## 🐛 Résolution de Problèmes

### "Aucune colonne détectée"
- Vérifiez que vos CSV contiennent bien les colonnes `name` ou `address` (ou leurs variantes)
- Utilisez la prévisualisation pour voir les colonnes disponibles

### "Aucun PDF généré"
- Vérifiez que votre template PDF est valide
- Assurez-vous qu'au moins une ligne contient des données

### Le serveur ne démarre pas
```bash
# Vérifier si le port 8002 est déjà utilisé
lsof -i:8002

# Tuer le processus si nécessaire
lsof -ti:8002 | xargs kill -9
```

## 📦 Dépendances

- Python 3.13+
- Flask 3.1.2
- PyPDF2 3.0.1
- ReportLab 4.4.4
- Pillow 12.0.0

## 🔄 Différences avec l'Ancienne Version

| Fonctionnalité | Avant | Maintenant |
|----------------|-------|------------|
| Fichiers CSV | 1 seul | Plusieurs simultanément |
| Colonnes | `adresse` uniquement | `name` + `address` (variantes acceptées) |
| Positionnement | 1 zone (adresse) | 2 zones indépendantes (nom + adresse) |
| Prévisualisation | ❌ | ✅ Tableau interactif |
| Détection colonnes | Sensible à la casse | Insensible + variantes |

## 📝 Notes de Développement

- **Backend** : Flask avec endpoints `/preview` et `/upload`
- **Frontend** : HTML5 + Vanilla JavaScript (pas de framework)
- **PDF** : ReportLab pour la génération, PyPDF2 pour la fusion
- **Drag & Drop** : Implémentation native avec MouseEvents

---

**Version** : 2.0  
**Date** : Novembre 2025  
**Port** : 8002

