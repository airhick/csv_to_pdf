# Script d'ajout d'adresses au verso d'un PDF

Ce script permet d'ajouter des adresses de destinataires au verso d'un PDF depuis un fichier CSV. Pour chaque page du PDF original, une nouvelle page verso est créée avec l'adresse positionnée en bas à gauche, visible à travers une fenêtre d'enveloppe lors de l'impression recto-verso.

## Installation

1. Installer les dépendances Python :

```bash
pip install -r requirements.txt
```

Les bibliothèques requises sont :
- `PyPDF2` : pour manipuler les fichiers PDF
- `reportlab` : pour créer les overlays avec les adresses

## Format du fichier CSV

Le fichier CSV doit contenir une colonne nommée `adresse`. Chaque ligne représente une adresse complète. L'adresse peut contenir des sauts de ligne (`\n`) pour séparer les différentes lignes de l'adresse.

Exemple de fichier CSV :

```csv
adresse
Jean Dupont
123 Rue de la République
75001 Paris
France
Marie Martin
45 Avenue des Champs-Élysées
75008 Paris
France
```

**Note** : Si votre adresse est sur plusieurs lignes dans le CSV, vous pouvez utiliser des guillemets et des sauts de ligne :

```csv
adresse
"Jean Dupont
123 Rue de la République
75001 Paris
France"
```

## Utilisation

### Mode par défaut (un PDF par adresse)

Crée un fichier PDF séparé pour chaque adresse :

```bash
python add_addresses_to_pdf.py example_addresses.csv rescto.pdf
```

### Mode fichier unique (toutes les adresses dans un seul PDF)

Crée un seul PDF avec toutes les pages :

```bash
python add_addresses_to_pdf.py example_addresses.csv rescto.pdf --single
```

### Spécifier un dossier de sortie

```bash
python add_addresses_to_pdf.py example_addresses.csv rescto.pdf output/
```

## Structure des PDFs générés

Pour chaque page du PDF original, le script crée :
1. **Page recto** : La page originale du PDF
2. **Page verso** : Une nouvelle page blanche avec l'adresse en bas à gauche

## Positionnement de l'adresse

Par défaut, l'adresse est positionnée sur la page verso :
- **20 mm** depuis le bord gauche
- **30 mm** depuis le bas

Cette position correspond à la zone typique d'une fenêtre d'enveloppe pour le verso. Si vous devez ajuster la position, modifiez les paramètres dans la fonction `create_blank_page_with_address()` :

```python
x_offset_mm=20  # Distance depuis la gauche
y_offset_mm=30  # Distance depuis le bas
font_size=10    # Taille de la police
```

## Structure des fichiers de sortie

- **Mode par défaut** : `rescto_with_address_1.pdf`, `rescto_with_address_2.pdf`, etc.
- **Mode --single** : `rescto_all_addresses.pdf` (un seul fichier avec toutes les pages)

Les fichiers sont créés dans le dossier `output/` par défaut, ou dans le dossier spécifié.

## Notes importantes

- Le script préserve toutes les pages du PDF original
- L'adresse est ajoutée en overlay sur chaque page
- Les adresses vides dans le CSV sont ignorées
- Le script détecte automatiquement le délimiteur du CSV (virgule, point-virgule, etc.)

# csv_to_pdf
