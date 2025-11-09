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

def create_blank_page_with_address(page_width, page_height, address, position=None):
    """
    Crée une page blanche avec l'adresse positionnée dans la zone définie.
    
    Args:
        page_width: Largeur de la page (en mm ou points)
        page_height: Hauteur de la page (en mm ou points)
        address: Texte de l'adresse
        position: Dictionnaire avec les clés suivantes (en mm):
            - left: Distance depuis la gauche
            - right: Distance depuis la droite
            - bottom: Distance depuis le bas
            - width: Largeur de la zone
            - height: Hauteur de la zone
    """
    # Créer une page PDF complète avec le canvas
    packet = BytesIO()
    
    # Vérifier si les dimensions sont en mm ou en points
    # Si les dimensions sont petites (< 1000), on suppose que c'est en mm et on convertit
    if page_width < 1000:
        # Les dimensions sont probablement en mm, convertir en points
        page_width_pt = page_width * mm
        page_height_pt = page_height * mm
    else:
        # Les dimensions sont déjà en points
        page_width_pt = page_width
        page_height_pt = page_height
    
    can = canvas.Canvas(packet, pagesize=(page_width_pt, page_height_pt))
    
    # Les dimensions sont en points (1 point = 1/72 inch)
    # Pour une page A4 : 210mm x 297mm = 595.276 points x 841.890 points
    
    # Dimensions de la zone d'adresse (en points)
    # Utiliser les paramètres personnalisés si fournis, sinon valeurs par défaut
    if position:
        left_mm = position.get('left', 95)
        right_mm = position.get('right', 15)
        bottom_mm = position.get('bottom', 20)
        zone_width_mm = position.get('width', 100)
        zone_height_mm = position.get('height', 40)
    else:
        # Valeurs par défaut
        left_mm = 95
        right_mm = 15
        bottom_mm = 20
        zone_width_mm = 100
        zone_height_mm = 40
    
    # Convertir en points
    min_x_pt = left_mm * mm
    x_offset_pt = right_mm * mm
    y_offset_pt = bottom_mm * mm
    zone_width_pt = zone_width_mm * mm
    
    # Position de référence à droite (en points)
    x_position_right = page_width_pt - x_offset_pt
    y_position = y_offset_pt
    
    # Configuration du texte
    font_size = 10  # Taille de police augmentée pour visibilité
    line_height = 4 * mm  # Espacement augmenté
    # La largeur max est la largeur de la zone définie
    max_width_pt = zone_width_pt
    
    # Nettoyer et diviser l'adresse en lignes
    lines = [line.strip() for line in address.split('\n') if line.strip()]
    
    # Dessiner l'adresse ligne par ligne, alignée à droite
    # Pour une fenêtre d'enveloppe, on dessine de bas en haut (pays en bas, nom en haut)
    can.setFillColorRGB(0, 0, 0)
    can.setFont("Helvetica", font_size)
    
    if lines:
        # Calculer la position Y de départ (première ligne en bas)
        # On dessine les lignes de bas en haut
        y = y_position
        
        # Dessiner toutes les lignes dans l'ordre (première ligne = nom en bas, dernière ligne = pays en haut)
        for line in lines:
            if not line.strip():
                continue
                
            # Découper la ligne si elle est trop longue
            words = line.strip().split()
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                test_width = can.stringWidth(test_line, "Helvetica", font_size)
                
                if test_width > max_width_pt and current_line:
                    # Dessiner la ligne actuelle
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
            
            # Dessiner la dernière sous-ligne de cette ligne
            if current_line:
                line_text = ' '.join(current_line)
                line_width = can.stringWidth(line_text, "Helvetica", font_size)
                x_line = x_position_right - line_width
                if x_line < min_x_pt:
                    x_line = min_x_pt
                can.drawString(x_line, y, line_text)
                y += line_height
    
    can.save()
    packet.seek(0)
    
    # Lire la page créée et s'assurer qu'elle contient du contenu
    overlay_reader = PdfReader(packet)
    if len(overlay_reader.pages) == 0:
        raise ValueError("La page verso n'a pas été créée correctement")
    
    verso_page = overlay_reader.pages[0]
    
    # Vérifier que la page a du contenu
    if '/Contents' not in verso_page:
        raise ValueError("La page verso n'a pas de contenu")
    
    return verso_page

def add_address_to_pdf_verso(input_pdf_path, output_pdf_path, address, position=None):
    """
    Ajoute une nouvelle page verso avec l'adresse après chaque page du PDF.
    Structure: Page 1 (recto) -> Page 2 (verso avec adresse) -> Page 3 (recto) -> Page 4 (verso avec adresse)...
    
    Args:
        input_pdf_path: Chemin vers le PDF d'entrée
        output_pdf_path: Chemin vers le PDF de sortie
        address: Texte de l'adresse
        position: Dictionnaire avec les paramètres de position (optionnel)
    """
    # Lire le PDF d'entrée
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    
    # Obtenir les dimensions de la première page
    first_page = reader.pages[0]
    page_width = float(first_page.mediabox.width)
    page_height = float(first_page.mediabox.height)
    
    # Pour chaque page du PDF original
    for page_num, page in enumerate(reader.pages):
        # Ajouter la page originale (recto)
        writer.add_page(page)
        
        # Créer une nouvelle page verso avec l'adresse pour chaque page
        # (créer à chaque fois pour éviter les problèmes de référence)
        verso_page = create_blank_page_with_address(page_width, page_height, address, position)
        writer.add_page(verso_page)
    
    # Écrire le PDF de sortie
    with open(output_pdf_path, 'wb') as output_file:
        writer.write(output_file)

def process_csv_and_pdf(csv_path, pdf_path, output_dir=None, single_file=False, position=None):
    """
    Traite le CSV et crée un PDF pour chaque adresse ou un seul PDF combiné.
    
    Args:
        csv_path: Chemin vers le fichier CSV
        pdf_path: Chemin vers le PDF template
        output_dir: Dossier de sortie (par défaut: dossier du CSV/output)
        single_file: Si True, crée un seul PDF avec toutes les pages
        position: Dictionnaire avec les paramètres de position (optionnel)
    """
    csv_path = Path(csv_path)
    pdf_path = Path(pdf_path)
    
    if not csv_path.exists():
        print(f"Erreur: Le fichier CSV '{csv_path}' n'existe pas.")
        return
    
    if not pdf_path.exists():
        print(f"Erreur: Le fichier PDF '{pdf_path}' n'existe pas.")
        return
    
    if output_dir is None:
        output_dir = csv_path.parent / "output"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(exist_ok=True)
    
    # Lire le PDF template une fois
    template_reader = PdfReader(pdf_path)
    template_page = template_reader.pages[0]
    page_width = float(template_page.mediabox.width)
    page_height = float(template_page.mediabox.height)
    
    # Lire le CSV
    addresses = []
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        # Essayer de détecter le délimiteur, avec fallback sur virgule
        sample = csvfile.read(1024)
        csvfile.seek(0)
        
        delimiter = ','  # Délimiteur par défaut
        try:
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample).delimiter
        except:
            # Si la détection échoue, essayer les délimiteurs courants
            for test_delim in [',', ';', '\t']:
                csvfile.seek(0)
                test_reader = csv.DictReader(csvfile, delimiter=test_delim)
                try:
                    # Vérifier si on peut lire au moins une ligne
                    first_row = next(test_reader)
                    if 'adresse' in first_row or 'adresse' in test_reader.fieldnames:
                        delimiter = test_delim
                        break
                except:
                    continue
            csvfile.seek(0)
        
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        
        # Vérifier que la colonne 'adresse' existe
        if 'adresse' not in reader.fieldnames:
            print(f"Erreur: La colonne 'adresse' n'existe pas dans le CSV.")
            print(f"Colonnes disponibles: {', '.join(reader.fieldnames)}")
            return
        
        # Collecter toutes les adresses
        for row_num, row in enumerate(reader, start=1):
            address = row['adresse']
            
            # Nettoyer l'adresse : gérer les sauts de ligne et espaces
            if address:
                # Remplacer les \n littéraux par de vrais sauts de ligne
                address = address.replace('\\n', '\n')
                # Nettoyer les espaces en début/fin de chaque ligne
                address = '\n'.join(line.strip() for line in address.split('\n'))
                address = address.strip()
            
            if not address:
                print(f"Avertissement: Ligne {row_num} - adresse vide, ignorée.")
                continue
            
            addresses.append((row_num, address))
    
    if not addresses:
        print("Aucune adresse valide trouvée dans le CSV.")
        return
    
    if single_file:
        # Créer un seul PDF avec toutes les pages (recto + verso pour chaque adresse)
        writer = PdfWriter()
        
        for row_num, address in addresses:
            print(f"Traitement ligne {row_num}...")
            print(f"  Adresse: {address[:50]}...")
            
            # Ajouter la page template (recto)
            template_page = template_reader.pages[0]
            writer.add_page(template_page)
            
            # Créer et ajouter la page verso avec l'adresse
            verso_page = create_blank_page_with_address(page_width, page_height, address, position)
            writer.add_page(verso_page)
        
        output_path = output_dir / "rescto_all_addresses.pdf"
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        print(f"\n✓ PDF unique créé: {output_path}")
        print(f"  Nombre de pages: {len(addresses) * 2} (recto + verso pour chaque adresse)")
    else:
        # Créer un PDF pour chaque adresse
        for row_num, address in addresses:
            output_filename = f"rescto_with_address_{row_num}.pdf"
            output_path = output_dir / output_filename
            
            print(f"Traitement ligne {row_num}...")
            print(f"  Adresse: {address[:50]}...")
            
            try:
                add_address_to_pdf_verso(pdf_path, output_path, address, position)
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

