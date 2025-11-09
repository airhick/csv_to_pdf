#!/usr/bin/env python3
"""
Interface graphique pour ajouter des adresses au verso d'un PDF depuis un fichier CSV.
Utilise les dialogues natifs de macOS.
"""

import subprocess
import sys
import zipfile
import tempfile
import shutil
from pathlib import Path
from add_addresses_to_pdf import process_csv_and_pdf

def choose_file(title, file_types=None):
    """Ouvre un dialogue de sélection de fichier natif macOS"""
    if file_types is None:
        file_types = [("Tous les fichiers", "*")]
    
    # Construire le script AppleScript
    file_type_filter = ""
    if file_types:
        extensions = []
        for desc, ext in file_types:
            if ext.startswith("*."):
                extensions.append(ext[2:])
        if extensions:
            file_type_filter = f'{{"public.filename-extension", {{{", ".join([f'"{ext}"' for ext in extensions])}}}, false}}'
    
    script = f'''
    tell application "System Events"
        activate
        set theFile to choose file with prompt "{title}"'
    end tell
    return POSIX path of theFile
    '''
    
    try:
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def choose_folder(title="Choisir un dossier"):
    """Ouvre un dialogue de sélection de dossier natif macOS"""
    script = f'''
    tell application "System Events"
        activate
        set theFolder to choose folder with prompt "{title}"
    end tell
    return POSIX path of theFolder
    '''
    
    try:
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def show_dialog(title, message, buttons=None):
    """Affiche un dialogue natif macOS"""
    if buttons is None:
        buttons = ["OK"]
    
    buttons_str = ", ".join([f'"{btn}"' for btn in buttons])
    script = f'''
    tell application "System Events"
        activate
        display dialog "{message}" buttons {{{buttons_str}}} default button "{buttons[0]}" with title "{title}"
    end tell
    '''
    
    try:
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            check=True
        )
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False

def main():
    print("=" * 60)
    print("Générateur de PDFs avec Adresses")
    print("=" * 60)
    print()
    
    # Sélectionner le fichier CSV
    print("1. Sélection du fichier CSV...")
    csv_path = choose_file("Sélectionnez le fichier CSV contenant les adresses", 
                          [("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*")])
    
    if not csv_path:
        print("Annulé par l'utilisateur.")
        sys.exit(0)
    
    csv_file = Path(csv_path)
    print(f"   ✓ Fichier CSV sélectionné: {csv_file.name}")
    print()
    
    # Sélectionner le fichier PDF template
    print("2. Sélection du fichier PDF template...")
    
    # Vérifier si rescto.pdf existe dans le répertoire courant
    default_pdf = Path("rescto.pdf")
    if default_pdf.exists():
        use_default = input(f"   Utiliser le fichier par défaut '{default_pdf}'? (o/n): ").lower()
        if use_default == 'o':
            pdf_path = str(default_pdf.absolute())
            pdf_file = default_pdf
        else:
            pdf_path = choose_file("Sélectionnez le fichier PDF template", 
                                  [("Fichiers PDF", "*.pdf"), ("Tous les fichiers", "*")])
            if not pdf_path:
                print("Annulé par l'utilisateur.")
                sys.exit(0)
            pdf_file = Path(pdf_path)
    else:
        pdf_path = choose_file("Sélectionnez le fichier PDF template", 
                              [("Fichiers PDF", "*.pdf"), ("Tous les fichiers", "*")])
        if not pdf_path:
            print("Annulé par l'utilisateur.")
            sys.exit(0)
        pdf_file = Path(pdf_path)
    
    print(f"   ✓ Fichier PDF sélectionné: {pdf_file.name}")
    print()
    
    # Vérifications
    if not csv_file.exists():
        show_dialog("Erreur", f"Le fichier CSV n'existe pas: {csv_file}")
        sys.exit(1)
    
    if not pdf_file.exists():
        show_dialog("Erreur", f"Le fichier PDF n'existe pas: {pdf_file}")
        sys.exit(1)
    
    # Traitement
    print("3. Traitement des fichiers...")
    print("   Lecture du CSV et génération des PDFs...")
    
    try:
        # Créer un dossier temporaire pour les PDFs
        temp_dir = tempfile.mkdtemp()
        print(f"   Dossier temporaire: {temp_dir}")
        
        # Traiter le CSV et créer les PDFs
        process_csv_and_pdf(str(csv_file), str(pdf_file), temp_dir, single_file=False)
        
        # Compter les fichiers PDF créés
        pdf_files = list(Path(temp_dir).glob("*.pdf"))
        print(f"   ✓ {len(pdf_files)} fichier(s) PDF créé(s)")
        
        # Créer le fichier ZIP
        zip_path = csv_file.parent / f"{csv_file.stem}_pdfs.zip"
        print(f"\n4. Création du fichier ZIP...")
        print(f"   Nom: {zip_path.name}")
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for pdf_file_path in sorted(pdf_files):
                zipf.write(pdf_file_path, pdf_file_path.name)
                print(f"   ✓ Ajouté: {pdf_file_path.name}")
        
        # Nettoyer le dossier temporaire
        shutil.rmtree(temp_dir)
        
        print()
        print("=" * 60)
        print("✓ TERMINÉ AVEC SUCCÈS!")
        print("=" * 60)
        print(f"Fichier ZIP créé: {zip_path.name}")
        print(f"Emplacement: {zip_path.parent}")
        print(f"Nombre de PDFs: {len(pdf_files)}")
        print()
        
        # Afficher un dialogue de succès
        show_dialog(
            "Succès",
            f"Traitement terminé!\n\n{len(pdf_files)} PDF(s) créé(s)\n\nFichier ZIP: {zip_path.name}\n\nEmplacement: {zip_path.parent}",
            ["OK"]
        )
        
        # Demander si on veut ouvrir le dossier
        open_folder = input("Voulez-vous ouvrir le dossier contenant le ZIP? (o/n): ").lower()
        if open_folder == 'o':
            subprocess.run(['open', str(zip_path.parent)])
        
    except Exception as e:
        error_msg = f"Erreur lors du traitement: {str(e)}"
        print(f"\n✗ {error_msg}")
        show_dialog("Erreur", error_msg, ["OK"])
        sys.exit(1)

if __name__ == "__main__":
    main()
