#!/usr/bin/env python3
"""
Script pour ajouter des adresses au verso d'un PDF depuis un fichier CSV.
L'adresse est positionnée pour être visible à travers une fenêtre d'enveloppe.
"""

import sys
import csv
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

def create_address_overlay(address_text, page_width, page_height, 
                          x_offset_mm=20, y_offset_mm=30, font_size=10, position='left', max_width_mm=None):
    """
    Crée un overlay PDF avec l'adresse positionnée pour une fenêtre d'enveloppe.
    Position typique : bas à gauche pour le verso.
    
    Args:
        address_text: Texte de l'adresse (peut contenir \n pour les sauts de ligne)
        page_width: Largeur de la page en points
        page_height: Hauteur de la page en points
        x_offset_mm: Distance depuis le bord (gauche ou droite) en mm (par défaut 20mm)
        y_offset_mm: Distance depuis le bas en mm (par défaut 30mm)
        font_size: Taille de la police (par défaut 10)
        position: 'left' ou 'right' pour positionner à gauche ou à droite
        max_width_mm: Largeur maximale du texte en mm (si None, utilise 50mm par défaut)
    """
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=(page_width, page_height))
    
    # Position pour fenêtre d'enveloppe (bas à gauche pour le verso)
    # Convertir les mm en points (1 mm = 2.83465 points)
    if position == 'left':
        x_position = x_offset_mm * mm  # Depuis la gauche
    else:
        # Pour la droite, on calcule la position de fin du texte (alignement à droite)
        # x_position sera ajusté pour chaque ligne selon sa largeur
        x_position_right = page_width - (x_offset_mm * mm)  # Position de référence à droite
    
    y_position = y_offset_mm * mm
    
    # Configuration du texte
    line_height = 3 * mm  # Espacement réduit entre les lignes
    if max_width_mm is None:
        max_width = 50 * mm  # Largeur par défaut
    else:
        max_width = max_width_mm * mm  # Largeur spécifiée
    
    # Nettoyer et diviser l'adresse en lignes
    lines = [line.strip() for line in address_text.split('\n') if line.strip()]
    
    if not lines:
        can.save()
        packet.seek(0)
        return packet
    
    # Dessiner chaque ligne de l'adresse (de bas en haut)
    # Calculer la position de départ (première ligne en bas)
    y = y_position
    
    # Parcourir les lignes dans l'ordre inverse pour les dessiner de bas en haut
    for line in reversed(lines):
        if line.strip():
            # Découper la ligne si elle est trop longue
            words = line.split()
            current_line = []
            
            # Stocker les sous-lignes pour cette ligne
            sub_lines = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                can.setFont("Helvetica", font_size)
                text_width = can.stringWidth(test_line, "Helvetica", font_size)
                
                if text_width > max_width and current_line:
                    sub_lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    current_line.append(word)
            
            # Ajouter la dernière sous-ligne
            if current_line:
                sub_lines.append(' '.join(current_line))
            
            # Dessiner les sous-lignes de bas en haut
            for sub_line in reversed(sub_lines):
                can.setFont("Helvetica", font_size)
                # Si position est 'right', aligner le texte à droite
                if position == 'right':
                    text_width = can.stringWidth(sub_line, "Helvetica", font_size)
                    # Positionner le texte pour qu'il se termine à x_position_right
                    x_pos = x_position_right - text_width
                    # S'assurer que le texte ne dépasse pas de la zone autorisée
                    # La zone commence à 95mm depuis la gauche (9.5 cm)
                    min_x_pos = 95 * mm
                    if x_pos < min_x_pos:
                        x_pos = min_x_pos  # Commencer à la limite gauche de la zone
                else:
                    x_pos = x_position
                # Dessiner le texte en noir pour s'assurer qu'il est visible
                can.setFillColorRGB(0, 0, 0)  # Noir
                can.drawString(x_pos, y, sub_line)
                y += line_height
    
    can.save()
    packet.seek(0)
    return packet

def create_blank_page_with_name_and_address(page_width, page_height, name, address, name_position=None, address_position=None):
    """
    Crée une page blanche avec le nom et l'adresse positionnés dans des zones définies séparément.
    
    Args:
        page_width: Largeur de la page (en mm ou points)
        page_height: Hauteur de la page (en mm ou points)
        name: Texte du nom
        address: Texte de l'adresse
        name_position: Dictionnaire avec les clés suivantes (en mm):
            - left: Distance depuis la gauche
            - right: Distance depuis la droite
            - bottom: Distance depuis le bas
            - width: Largeur de la zone
            - height: Hauteur de la zone
        address_position: Dictionnaire avec les clés suivantes (en mm):
            - left, right, bottom, width, height
    """
    # Créer une page PDF complète avec le canvas
    packet = BytesIO()
    
    # Vérifier si les dimensions sont en mm ou en points
    if page_width < 1000:
        page_width_pt = page_width * mm
        page_height_pt = page_height * mm
    else:
        page_width_pt = page_width
        page_height_pt = page_height
    
    can = canvas.Canvas(packet, pagesize=(page_width_pt, page_height_pt))
    can.setFillColorRGB(0, 0, 0)
    
    # Fonction helper pour dessiner du texte dans une zone
    def draw_text_in_zone(text, position, default_left, default_bottom, default_width, default_height):
        if position:
            left_mm = position.get('left', default_left)
            right_mm = position.get('right', 15)
            bottom_mm = position.get('bottom', default_bottom)
            zone_width_mm = position.get('width', default_width)
            zone_height_mm = position.get('height', default_height)
        else:
            left_mm = default_left
            right_mm = 15
            bottom_mm = default_bottom
            zone_width_mm = default_width
            zone_height_mm = default_height
        
        min_x_pt = left_mm * mm
        x_offset_pt = right_mm * mm
        y_offset_pt = bottom_mm * mm
        zone_width_pt = zone_width_mm * mm
        
        x_position_right = page_width_pt - x_offset_pt
        y_position = y_offset_pt
        
        font_size = 10
        line_height = 4 * mm
        max_width_pt = zone_width_pt
        
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        if lines:
            can.setFont("Helvetica", font_size)
            y = y_position
            
            for line in lines:
                if not line.strip():
                    continue
                
                words = line.strip().split()
                current_line = []
                
                for word in words:
                    test_line = ' '.join(current_line + [word])
                    test_width = can.stringWidth(test_line, "Helvetica", font_size)
                    
                    if test_width > max_width_pt and current_line:
                        line_text = ' '.join(current_line)
                        line_width = can.stringWidth(line_text, "Helvetica", font_size)
                        x_line = x_position_right - line_width
                        if x_line < min_x_pt:
                            x_line = min_x_pt
                        can.drawString(x_line, y, line_text)
                        y += line_height
                        current_line = [word]
                    else:
                        current_line.append(word)
                
                if current_line:
                    line_text = ' '.join(current_line)
                    line_width = can.stringWidth(line_text, "Helvetica", font_size)
                    x_line = x_position_right - line_width
                    if x_line < min_x_pt:
                        x_line = min_x_pt
                    can.drawString(x_line, y, line_text)
                    y += line_height
    
    # Dessiner le nom dans sa zone
    if name:
        draw_text_in_zone(name, name_position, 20, 250, 80, 30)
    
    # Dessiner l'adresse dans sa zone
    if address:
        draw_text_in_zone(address, address_position, 95, 20, 100, 40)
    
    can.save()
    packet.seek(0)
    
    overlay_reader = PdfReader(packet)
    if len(overlay_reader.pages) == 0:
        raise ValueError("La page verso n'a pas été créée correctement")
    
    verso_page = overlay_reader.pages[0]
    
    if '/Contents' not in verso_page:
        raise ValueError("La page verso n'a pas de contenu")
    
    return verso_page

def create_blank_page_with_address(page_width, page_height, address, position=None):
    """
    Fonction de compatibilité pour l'ancienne API (seulement adresse, pas de nom séparé).
    """
    return create_blank_page_with_name_and_address(page_width, page_height, "", address, None, position)

def add_address_to_pdf_verso(input_pdf_path, output_pdf_path, address, position=None):
    """
    Fonction de compatibilité - ajoute une nouvelle page verso avec l'adresse après chaque page du PDF.
    """
    add_name_and_address_to_pdf_verso(input_pdf_path, output_pdf_path, "", address, None, position)

def add_name_and_address_to_pdf_verso(input_pdf_path, output_pdf_path, name, address, name_position=None, address_position=None):
    """
    Ajoute une nouvelle page verso avec le nom et l'adresse après chaque page du PDF.
    Structure: Page 1 (recto) -> Page 2 (verso avec nom+adresse) -> ...
    
    Args:
        input_pdf_path: Chemin vers le PDF d'entrée
        output_pdf_path: Chemin vers le PDF de sortie
        name: Texte du nom
        address: Texte de l'adresse
        name_position: Dictionnaire avec les paramètres de position du nom (optionnel)
        address_position: Dictionnaire avec les paramètres de position de l'adresse (optionnel)
    """
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    
    first_page = reader.pages[0]
    page_width = float(first_page.mediabox.width)
    page_height = float(first_page.mediabox.height)
    
    for page_num, page in enumerate(reader.pages):
        writer.add_page(page)
        verso_page = create_blank_page_with_name_and_address(
            page_width, page_height, name, address, name_position, address_position
        )
        writer.add_page(verso_page)
    
    with open(output_pdf_path, 'wb') as output_file:
        writer.write(output_file)

def detect_column(fieldnames, possible_names):
    """
    Détecte une colonne parmi plusieurs noms possibles (insensible à la casse).
    
    Args:
        fieldnames: Liste des noms de colonnes disponibles
        possible_names: Liste des noms possibles à rechercher
    
    Returns:
        Le nom exact de la colonne trouvée, ou None
    """
    if not fieldnames:
        return None
    
    for field in fieldnames:
        if field and field.lower().strip() in [name.lower() for name in possible_names]:
            return field
    return None

def read_and_concatenate_csvs(csv_paths):
    """
    Lit plusieurs fichiers CSV et retourne les données concatenées.
    Détecte automatiquement les colonnes 'name' et 'address' pour chaque CSV.
    Normalise les données pour avoir des clés cohérentes.
    
    Args:
        csv_paths: Liste de chemins vers les fichiers CSV
    
    Returns:
        Tuple (data_rows, name_column_label, address_column_label)
        où data_rows est une liste de dictionnaires normalisés avec les clés 'name' et 'address'
    """
    all_data = []
    detected_name_columns = []
    detected_address_columns = []
    
    for csv_path in csv_paths:
        csv_path = Path(csv_path)
        
        if not csv_path.exists():
            print(f"Avertissement: Le fichier CSV '{csv_path}' n'existe pas, ignoré.")
            continue
        
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            # Détection du délimiteur
            sample = csvfile.read(1024)
            csvfile.seek(0)
            
            delimiter = ','
            try:
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter
            except:
                for test_delim in [',', ';', '\t']:
                    csvfile.seek(0)
                    test_reader = csv.DictReader(csvfile, delimiter=test_delim)
                    try:
                        first_row = next(test_reader)
                        delimiter = test_delim
                        break
                    except:
                        continue
                csvfile.seek(0)
            
            reader = csv.DictReader(csvfile, delimiter=delimiter)
            
            # Détecter les colonnes name et address pour CE CSV
            name_col = detect_column(reader.fieldnames, ['name', 'nom', 'prenom', 'firstname', 'lastname'])
            address_col = detect_column(reader.fieldnames, ['address', 'adresse', 'addr'])
            
            if name_col:
                detected_name_columns.append(name_col)
            if address_col:
                detected_address_columns.append(address_col)
            
            # Lire toutes les lignes et normaliser les clés
            for row in reader:
                normalized_row = {
                    'name': row.get(name_col, '') if name_col else '',
                    'address': row.get(address_col, '') if address_col else ''
                }
                all_data.append(normalized_row)
    
    # Retourner le premier nom de colonne détecté comme label
    name_label = detected_name_columns[0] if detected_name_columns else None
    address_label = detected_address_columns[0] if detected_address_columns else None
    
    return all_data, name_label, address_label

def process_csv_and_pdf(csv_paths, pdf_path, output_dir=None, single_file=False, name_position=None, address_position=None):
    """
    Traite plusieurs CSV et crée un PDF pour chaque entrée ou un seul PDF combiné.
    
    Args:
        csv_paths: Liste de chemins vers les fichiers CSV (peut être une string pour rétrocompatibilité)
        pdf_path: Chemin vers le PDF template
        output_dir: Dossier de sortie (par défaut: output/)
        single_file: Si True, crée un seul PDF avec toutes les pages
        name_position: Dictionnaire avec les paramètres de position du nom (optionnel)
        address_position: Dictionnaire avec les paramètres de position de l'adresse (optionnel)
    """
    # Rétrocompatibilité: si csv_paths est une string, la convertir en liste
    if isinstance(csv_paths, (str, Path)):
        csv_paths = [csv_paths]
    
    csv_paths = [Path(p) for p in csv_paths]
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        print(f"Erreur: Le fichier PDF '{pdf_path}' n'existe pas.")
        return
    
    if output_dir is None:
        output_dir = Path("output")
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(exist_ok=True)
    
    # Lire et concaténer tous les CSV
    print(f"Lecture de {len(csv_paths)} fichier(s) CSV...")
    all_data, name_column, address_column = read_and_concatenate_csvs(csv_paths)
    
    if not all_data:
        print("Erreur: Aucune donnée trouvée dans les fichiers CSV.")
        return
    
    if not name_column and not address_column:
        print("Erreur: Aucune colonne 'name' ou 'address' détectée dans les CSV.")
        print(f"Colonnes disponibles: {', '.join(all_data[0].keys() if all_data else [])}")
        return
    
    print(f"✓ {len(all_data)} ligne(s) trouvée(s)")
    print(f"  Colonne nom: {name_column or '(non détectée)'}")
    print(f"  Colonne adresse: {address_column or '(non détectée)'}")
    
    # Lire le PDF template
    template_reader = PdfReader(pdf_path)
    template_page = template_reader.pages[0]
    page_width = float(template_page.mediabox.width)
    page_height = float(template_page.mediabox.height)
    
    # Préparer les données (name + address pour chaque ligne)
    # Les données sont déjà normalisées avec les clés 'name' et 'address'
    entries = []
    for row_num, row in enumerate(all_data, start=1):
        name = row.get('name', '')
        address = row.get('address', '')
        
        # Nettoyer les données
        if name:
            name = name.replace('\\n', '\n')
            name = '\n'.join(line.strip() for line in name.split('\n'))
            name = name.strip()
        
        if address:
            address = address.replace('\\n', '\n')
            address = '\n'.join(line.strip() for line in address.split('\n'))
            address = address.strip()
        
        if not name and not address:
            print(f"Avertissement: Ligne {row_num} - nom et adresse vides, ignorée.")
            continue
        
        entries.append((row_num, name, address))
    
    if not entries:
        print("Aucune entrée valide trouvée dans les CSV.")
        return
    
    if single_file:
        # Créer un seul PDF avec toutes les pages (recto + verso pour chaque entrée)
        writer = PdfWriter()
        
        for row_num, name, address in entries:
            print(f"Traitement ligne {row_num}...")
            if name:
                print(f"  Nom: {name[:50]}...")
            if address:
                print(f"  Adresse: {address[:50]}...")
            
            # Ajouter la page template (recto)
            template_page = template_reader.pages[0]
            writer.add_page(template_page)
            
            # Créer et ajouter la page verso avec nom et adresse
            verso_page = create_blank_page_with_name_and_address(
                page_width, page_height, name, address, name_position, address_position
            )
            writer.add_page(verso_page)
        
        output_path = output_dir / "rescto_all_entries.pdf"
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        print(f"\n✓ PDF unique créé: {output_path}")
        print(f"  Nombre de pages: {len(entries) * 2} (recto + verso pour chaque entrée)")
    else:
        # Créer un PDF pour chaque entrée
        for row_num, name, address in entries:
            output_filename = f"rescto_with_address_{row_num}.pdf"
            output_path = output_dir / output_filename
            
            print(f"Traitement ligne {row_num}...")
            if name:
                print(f"  Nom: {name[:50]}...")
            if address:
                print(f"  Adresse: {address[:50]}...")
            
            try:
                add_name_and_address_to_pdf_verso(
                    pdf_path, output_path, name, address, name_position, address_position
                )
                print(f"  ✓ Créé: {output_path}")
            except Exception as e:
                print(f"  ✗ Erreur: {e}")
    
    print(f"\nTerminé! Fichiers créés dans: {output_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python add_addresses_to_pdf.py <fichier.csv> <fichier.pdf> [options]")
        print("\nOptions:")
        print("  [dossier_sortie]     Dossier de sortie (par défaut: output/)")
        print("  --single             Crée un seul PDF avec toutes les pages")
        print("\nExemples:")
        print("  python add_addresses_to_pdf.py addresses.csv rescto.pdf")
        print("  python add_addresses_to_pdf.py addresses.csv rescto.pdf output/")
        print("  python add_addresses_to_pdf.py addresses.csv rescto.pdf --single")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    pdf_file = sys.argv[2]
    
    # Parser les arguments
    single_file = "--single" in sys.argv
    output_directory = None
    
    for arg in sys.argv[3:]:
        if arg != "--single":
            output_directory = arg
            break
    
    process_csv_and_pdf(csv_file, pdf_file, output_directory, single_file)

