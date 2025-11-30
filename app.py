#!/usr/bin/env python3
"""Serveur local pour générer des PDFs avec adresses."""

import csv
import json
import os
import shutil
import tempfile
import zipfile
from io import BytesIO
from pathlib import Path

from flask import Flask, jsonify, request, send_file
from werkzeug.utils import secure_filename

from add_addresses_to_pdf import process_csv_and_pdf, read_and_concatenate_csvs
from functools import wraps

app = Flask(__name__, static_folder='.', static_url_path='')

# Configuration de sécurité
API_KEY = os.environ.get('API_KEY', None)  # Définir une clé API via variable d'environnement
REQUIRE_API_KEY = os.environ.get('REQUIRE_API_KEY', 'False').lower() == 'true'


def require_api_key(f):
    """Décorateur pour protéger les endpoints avec une API key."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not REQUIRE_API_KEY:
            return f(*args, **kwargs)
        
        # Vérifier l'API key dans les headers
        provided_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        
        if not provided_key:
            return jsonify({'error': 'API Key manquante. Fournir X-API-Key header ou ?api_key=...'}), 401
        
        if provided_key != API_KEY:
            return jsonify({'error': 'API Key invalide'}), 403
        
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    """Serve la page principale."""
    return app.send_static_file('index.html')


@app.route('/health')
def health():
    """Health check endpoint - accessible sans API key."""
    return jsonify({
        'status': 'ok',
        'service': 'PDF Generator API',
        'version': '2.1',
        'endpoints': {
            'web': '/',
            'preview': '/preview',
            'upload': '/upload',
            'api': '/api/generate'
        }
    })


@app.route('/api/status')
def api_status():
    """Status de l'API - pour vérifier la configuration."""
    return jsonify({
        'status': 'operational',
        'api_key_required': REQUIRE_API_KEY,
        'host': request.host,
        'remote_addr': request.remote_addr,
        'user_agent': request.headers.get('User-Agent')
    })


@app.route('/preview', methods=['POST'])
def preview():
    """Prévisualise les données des CSV uploadés (concatenés)."""
    csv_files = request.files.getlist('csvFiles')
    
    if not csv_files:
        return jsonify({'error': 'Aucun fichier CSV fourni.'}), 400
    
    temp_dir = tempfile.mkdtemp(prefix='csv_preview_')
    
    try:
        # Sauvegarder temporairement tous les CSV
        csv_paths = []
        for i, csv_file in enumerate(csv_files):
            csv_path = os.path.join(temp_dir, secure_filename(csv_file.filename) or f'file_{i}.csv')
            csv_file.save(csv_path)
            csv_paths.append(csv_path)
        
        # Lire et concaténer les CSV
        all_data, name_column, address_column = read_and_concatenate_csvs(csv_paths)
        
        if not all_data:
            return jsonify({'error': 'Aucune donnée trouvée dans les fichiers CSV.'}), 400
        
        # Préparer les données pour la prévisualisation
        # Les données sont déjà normalisées avec les clés 'name' et 'address'
        preview_data = []
        for i, row in enumerate(all_data, start=1):
            name = row.get('name', '')
            address = row.get('address', '')
            preview_data.append({
                'row': i,
                'name': name,
                'address': address
            })
        
        return jsonify({
            'success': True,
            'total': len(preview_data),
            'nameColumn': name_column,
            'addressColumn': address_column,
            'data': preview_data
        })
        
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


@app.route('/upload', methods=['POST'])
def upload():
    """Traite les CSV et le PDF envoyés et renvoie un ZIP."""
    csv_files = request.files.getlist('csvFiles')
    pdf_file = request.files.get('pdfFile')
    name_position_raw = request.form.get('namePosition')
    address_position_raw = request.form.get('addressPosition')

    if not csv_files or not pdf_file:
        return jsonify({'error': 'Les fichiers CSV et PDF sont requis.'}), 400

    try:
        name_position = json.loads(name_position_raw) if name_position_raw else None
        address_position = json.loads(address_position_raw) if address_position_raw else None
    except json.JSONDecodeError as exc:
        return jsonify({'error': f'Position invalide: {exc}'}), 400

    temp_dir = tempfile.mkdtemp(prefix='pdf_addresses_')

    try:
        # Sauvegarder tous les CSV
        csv_paths = []
        for i, csv_file in enumerate(csv_files):
            csv_path = os.path.join(temp_dir, secure_filename(csv_file.filename) or f'addresses_{i}.csv')
            csv_file.save(csv_path)
            csv_paths.append(csv_path)
        
        pdf_path = os.path.join(temp_dir, secure_filename(pdf_file.filename) or 'template.pdf')
        pdf_file.save(pdf_path)

        output_dir = os.path.join(temp_dir, 'output')
        os.makedirs(output_dir, exist_ok=True)

        import io
        import contextlib

        log_buffer = io.StringIO()
        with contextlib.redirect_stdout(log_buffer):
            process_csv_and_pdf(
                csv_paths, pdf_path, output_dir, 
                single_file=False, 
                name_position=name_position, 
                address_position=address_position
            )
        process_log = log_buffer.getvalue()

        zip_buffer = BytesIO()
        pdf_files = sorted(Path(output_dir).glob('*.pdf'))

        if not pdf_files:
            return jsonify({
                'error': "Aucun PDF n'a été généré.",
                'message': "Vérifiez que votre CSV contient une colonne 'adresse' et que votre PDF est valide.",
                'log': process_log
            }), 400

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for pdf_generated in pdf_files:
                zipf.write(pdf_generated, pdf_generated.name)

        zip_buffer.seek(0)
        return send_file(
            zip_buffer,
            as_attachment=True,
            download_name='pdfs_with_addresses.zip',
            mimetype='application/zip'
        )
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({'error': str(exc)}), 500
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


@app.route('/api/generate', methods=['POST'])
@require_api_key
def api_generate():
    """
    API REST pour générer des PDFs avec nom et adresse.
    
    Accepte soit:
    1. JSON avec données directes:
       {
         "data": [{"name": "...", "address": "..."}, ...],
         "namePosition": {"left": 20, "bottom": 250, "width": 80, "height": 30},
         "addressPosition": {"left": 95, "bottom": 20, "width": 100, "height": 40},
         "singleFile": false (optionnel)
       }
    
    2. Form-data avec csvFiles (comme /upload)
    
    Si aucun PDF recto n'est fourni, utilise 'recto.pdf' par défaut.
    """
    temp_dir = tempfile.mkdtemp(prefix='api_pdf_')
    
    try:
        # Vérifier si c'est une requête JSON ou form-data
        if request.is_json:
            # Mode JSON: données directes
            data = request.get_json()
            
            if not data or 'data' not in data:
                return jsonify({'error': 'Le champ "data" est requis'}), 400
            
            entries = data.get('data', [])
            name_position = data.get('namePosition')
            address_position = data.get('addressPosition')
            single_file = data.get('singleFile', False)
            
            # Créer un CSV temporaire à partir des données JSON
            csv_path = os.path.join(temp_dir, 'data.csv')
            with open(csv_path, 'w', encoding='utf-8', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['name', 'address'])
                writer.writeheader()
                for entry in entries:
                    writer.writerow({
                        'name': entry.get('name', ''),
                        'address': entry.get('address', '')
                    })
            
            csv_paths = [csv_path]
            
            # Utiliser recto.pdf par défaut
            default_pdf = Path(__file__).parent / 'recto.pdf'
            if not default_pdf.exists():
                default_pdf = Path(__file__).parent / 'rescto.pdf'
            
            pdf_path = os.path.join(temp_dir, 'recto.pdf')
            shutil.copy(str(default_pdf), pdf_path)
            
        else:
            # Mode form-data: CSV uploadés
            csv_files = request.files.getlist('csvFiles')
            pdf_file = request.files.get('pdfFile')
            
            if not csv_files:
                return jsonify({'error': 'Aucun fichier CSV ou données fournis'}), 400
            
            name_position_raw = request.form.get('namePosition')
            address_position_raw = request.form.get('addressPosition')
            single_file = request.form.get('singleFile', 'false').lower() == 'true'
            
            try:
                name_position = json.loads(name_position_raw) if name_position_raw else None
                address_position = json.loads(address_position_raw) if address_position_raw else None
            except json.JSONDecodeError as exc:
                return jsonify({'error': f'Position invalide: {exc}'}), 400
            
            # Sauvegarder tous les CSV
            csv_paths = []
            for i, csv_file in enumerate(csv_files):
                csv_path = os.path.join(temp_dir, secure_filename(csv_file.filename) or f'data_{i}.csv')
                csv_file.save(csv_path)
                csv_paths.append(csv_path)
            
            # PDF recto: utiliser le fichier uploadé ou recto.pdf par défaut
            if pdf_file:
                pdf_path = os.path.join(temp_dir, secure_filename(pdf_file.filename) or 'recto.pdf')
                pdf_file.save(pdf_path)
            else:
                default_pdf = Path(__file__).parent / 'recto.pdf'
                if not default_pdf.exists():
                    default_pdf = Path(__file__).parent / 'rescto.pdf'
                pdf_path = os.path.join(temp_dir, 'recto.pdf')
                shutil.copy(str(default_pdf), pdf_path)
        
        # Générer les PDFs
        output_dir = os.path.join(temp_dir, 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        import io
        import contextlib
        
        log_buffer = io.StringIO()
        with contextlib.redirect_stdout(log_buffer):
            process_csv_and_pdf(
                csv_paths, pdf_path, output_dir,
                single_file=single_file,
                name_position=name_position,
                address_position=address_position
            )
        process_log = log_buffer.getvalue()
        
        pdf_files = sorted(Path(output_dir).glob('*.pdf'))
        
        if not pdf_files:
            return jsonify({
                'error': "Aucun PDF n'a été généré.",
                'log': process_log
            }), 400
        
        # Si un seul fichier généré, le retourner directement
        if len(pdf_files) == 1:
            return send_file(
                pdf_files[0],
                as_attachment=True,
                download_name='generated.pdf',
                mimetype='application/pdf'
            )
        
        # Sinon, créer un ZIP
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for pdf_file in pdf_files:
                zipf.write(pdf_file, pdf_file.name)
        
        zip_buffer.seek(0)
        return send_file(
            zip_buffer,
            as_attachment=True,
            download_name='generated_pdfs.zip',
            mimetype='application/zip'
        )
        
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8002))
    host = os.environ.get('HOST', '0.0.0.0')  # 0.0.0.0 = accessible depuis n'importe quelle IP
    
    # Mode debug désactivé en production pour la sécurité
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print("\n" + "="*60)
    print("🚀 PDF Generator API Server")
    print("="*60)
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Debug: {debug_mode}")
    print("="*60)
    print("\n🌐 Accès:")
    print(f"   Local:    http://localhost:{port}")
    print(f"   Network:  http://<YOUR_IP>:{port}")
    print(f"   API:      http://<YOUR_IP>:{port}/api/generate")
    print("\n⚠️  ATTENTION: Serveur accessible depuis l'extérieur!")
    print("   Assurez-vous d'avoir une sécurité appropriée.\n")
    
    app.run(host=host, port=port, debug=debug_mode, threaded=True)
