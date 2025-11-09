import json
import zipfile
import tempfile
import shutil
import base64
from pathlib import Path
import sys
import os

# Ajouter le chemin du module parent et du dossier functions
current_dir = os.path.dirname(__file__)
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, '../../'))

try:
    from add_addresses_to_pdf import process_csv_and_pdf
except ImportError as e:
    # Si le module n'est pas disponible, on retourne une erreur
    print(f"Import error: {e}")
    pass

def handler(event, context):
    """Netlify Function handler pour générer les PDFs"""
    
    # Headers CORS
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
    }
    
    # Gérer les requêtes OPTIONS (preflight)
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    # Vérifier la méthode HTTP
    if event.get('httpMethod') != 'POST':
        return {
            'statusCode': 405,
            'headers': headers,
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        # Parser le body JSON
        body = json.loads(event.get('body', '{}'))
        
        # Récupérer les fichiers en base64
        csv_base64 = body.get('csvFile')
        pdf_base64 = body.get('pdfFile')
        csv_filename = body.get('csvFilename', 'addresses.csv')
        pdf_filename = body.get('pdfFilename', 'template.pdf')
        
        if not csv_base64 or not pdf_base64:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'Fichiers CSV et PDF requis'})
            }
        
        # Créer un dossier temporaire
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Décoder les fichiers
            csv_data = base64.b64decode(csv_base64.split(',')[-1] if ',' in csv_base64 else csv_base64)
            pdf_data = base64.b64decode(pdf_base64.split(',')[-1] if ',' in pdf_base64 else pdf_base64)
            
            # Sauvegarder les fichiers temporairement
            csv_path = os.path.join(temp_dir, csv_filename)
            pdf_path = os.path.join(temp_dir, pdf_filename)
            
            with open(csv_path, 'wb') as f:
                f.write(csv_data)
            
            with open(pdf_path, 'wb') as f:
                f.write(pdf_data)
            
            # Créer un dossier de sortie
            output_dir = os.path.join(temp_dir, 'output')
            os.makedirs(output_dir, exist_ok=True)
            
            # Traiter les fichiers
            process_csv_and_pdf(csv_path, pdf_path, output_dir, single_file=False)
            
            # Créer le ZIP
            zip_path = os.path.join(temp_dir, 'pdfs.zip')
            pdf_files = list(Path(output_dir).glob("*.pdf"))
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for pdf_file in sorted(pdf_files):
                    zipf.write(pdf_file, pdf_file.name)
            
            # Lire le ZIP et le convertir en base64
            with open(zip_path, 'rb') as f:
                zip_data = f.read()
            
            zip_base64 = base64.b64encode(zip_data).decode('utf-8')
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/zip',
                    'Content-Disposition': 'attachment; filename="pdfs.zip"',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': zip_base64,
                'isBase64Encoded': True
            }
            
        finally:
            # Nettoyer
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': str(e),
                'details': error_details
            })
        }
