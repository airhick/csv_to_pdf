# Interface Graphique - Générateur de PDFs avec Adresses

## Description

Cette application permet de générer automatiquement des PDFs avec des adresses au verso depuis un fichier CSV. L'application utilise les dialogues natifs de macOS pour sélectionner les fichiers.

## Fonctionnalités

- ✅ Sélection du fichier CSV depuis le Finder (dialogue natif macOS)
- ✅ Sélection du fichier PDF template depuis le Finder
- ✅ Détection automatique de la colonne "adresse" dans le CSV
- ✅ Génération d'un PDF pour chaque ligne du CSV
- ✅ Création automatique d'un fichier ZIP contenant tous les PDFs
- ✅ Interface en ligne de commande avec dialogues natifs macOS

## Utilisation

### Méthode 1 : Double-clic (recommandé)

1. Double-cliquez sur le fichier `lancer_app.command`
2. Suivez les instructions à l'écran :
   - Sélectionnez votre fichier CSV
   - Sélectionnez le fichier PDF template (ou utilisez `rescto.pdf` si présent)
3. Le programme génère automatiquement les PDFs et crée un fichier ZIP

### Méthode 2 : Ligne de commande

```bash
python3 gui_app.py
```

## Format du fichier CSV

Le fichier CSV doit contenir une colonne nommée **`adresse`** (en minuscules). Chaque ligne représente une adresse complète.

**Exemple de fichier CSV :**

```csv
adresse
"Jean Dupont
123 Rue de la République
75001 Paris
France"
"Marie Martin
45 Avenue des Champs-Élysées
75008 Paris
France"
```

**Note :** Les adresses peuvent être sur plusieurs lignes en utilisant des guillemets et des sauts de ligne dans le CSV.

## Résultat

L'application crée :

1. **Un PDF pour chaque adresse** dans le CSV
   - Chaque PDF contient :
     - Page 1 (recto) : La page originale du template PDF
     - Page 2 (verso) : Une page blanche avec l'adresse positionnée

2. **Un fichier ZIP** contenant tous les PDFs
   - Nom du fichier : `[nom_du_csv]_pdfs.zip`
   - Emplacement : Même dossier que le fichier CSV

## Positionnement de l'adresse

L'adresse est positionnée sur la page verso avec :
- **2 cm** depuis le bas de la page
- **2 cm** depuis le côté droit de la page
- Alignée à droite
- Taille de police : 10 points

## Prérequis

- Python 3.x
- Les dépendances installées (voir `requirements.txt`)
- macOS (pour les dialogues natifs)

## Installation des dépendances

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Dépannage

### L'application ne se lance pas

- Vérifiez que Python 3 est installé : `python3 --version`
- Vérifiez que les dépendances sont installées dans le venv
- Essayez de lancer depuis le terminal : `python3 gui_app.py`

### Erreur "colonne 'adresse' n'existe pas"

- Vérifiez que votre CSV contient bien une colonne nommée `adresse` (en minuscules)
- La première ligne du CSV doit contenir les noms de colonnes

### Les PDFs ne s'affichent pas correctement

- Vérifiez que le fichier PDF template est valide
- Vérifiez que les adresses dans le CSV sont bien formatées

