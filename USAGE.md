# Guide d'utilisation rapide

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation de base

### 1. Préparer votre fichier CSV

Votre CSV doit avoir une colonne nommée `adresse`. Chaque ligne représente une adresse complète.

**Format recommandé** (avec guillemets pour les adresses multi-lignes) :

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

**Format alternatif** (une seule ligne avec \n) :

```csv
adresse
"Jean Dupont\n123 Rue de la République\n75001 Paris\nFrance"
```

### 2. Exécuter le script

**Mode par défaut** (un PDF par adresse) :
```bash
python add_addresses_to_pdf.py votre_fichier.csv rescto.pdf
```

**Mode fichier unique** (toutes les adresses dans un seul PDF) :
```bash
python add_addresses_to_pdf.py votre_fichier.csv rescto.pdf --single
```

### 3. Résultats

Les fichiers PDF générés seront dans le dossier `output/` :
- Mode par défaut : `rescto_with_address_1.pdf`, `rescto_with_address_2.pdf`, etc.
- Mode `--single` : `rescto_all_addresses.pdf`

## Structure des PDFs

Chaque PDF généré contient :
- **Page 1 (recto)** : La page originale du PDF `rescto.pdf`
- **Page 2 (verso)** : Une nouvelle page blanche avec l'adresse en bas à gauche

## Ajustement de la position

Si l'adresse n'est pas bien positionnée pour votre enveloppe, modifiez les paramètres dans le script (ligne 93-100) :

```python
def create_blank_page_with_address(page_width, page_height, address):
    overlay_pdf = create_address_overlay(address, page_width, page_height, 
                                        x_offset_mm=20,   # ← Ajustez cette valeur
                                        y_offset_mm=30,   # ← Ajustez cette valeur
                                        font_size=10,    # ← Ajustez cette valeur
                                        position='left')
```

- `x_offset_mm` : Distance depuis le bord gauche (augmentez pour déplacer vers la droite)
- `y_offset_mm` : Distance depuis le bas (augmentez pour déplacer vers le haut)
- `font_size` : Taille de la police

## Dépannage

**Erreur : "La colonne 'adresse' n'existe pas"**
- Vérifiez que votre CSV a bien une colonne nommée `adresse` (sans accent sur le 'e' si nécessaire)
- Vérifiez l'encodage du fichier (UTF-8 recommandé)

**L'adresse n'apparaît pas au bon endroit**
- Ajustez `x_offset_mm` et `y_offset_mm` dans la fonction `create_address_overlay`
- Testez avec une seule adresse d'abord

**Les adresses multi-lignes ne fonctionnent pas**
- Utilisez des guillemets autour de l'adresse dans le CSV
- Ou utilisez `\n` pour les sauts de ligne

