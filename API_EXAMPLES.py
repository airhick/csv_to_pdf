#!/usr/bin/env python3
"""
Exemples d'utilisation de l'API PDF Generator
Tous les exemples sont prêts à être exécutés.
"""

import requests
import json

# Configuration
API_URL = "http://localhost:8002/api/generate"


def example_1_simple_json():
    """Exemple 1: JSON simple avec positions par défaut"""
    print("\n" + "="*60)
    print("Exemple 1: JSON Simple")
    print("="*60)
    
    data = {
        "data": [
            {
                "name": "Jean Dupont",
                "address": "123 Rue de la République\n75001 Paris\nFrance"
            },
            {
                "name": "Marie Martin",
                "address": "45 Avenue des Champs-Élysées\n75008 Paris\nFrance"
            }
        ]
    }
    
    print("📤 Envoi de 2 entrées...")
    response = requests.post(API_URL, json=data)
    
    if response.status_code == 200:
        with open('example1_output.zip', 'wb') as f:
            f.write(response.content)
        print(f"✅ Succès! ZIP généré: example1_output.zip ({len(response.content)} bytes)")
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(response.text)


def example_2_single_file():
    """Exemple 2: Générer un seul PDF avec toutes les pages"""
    print("\n" + "="*60)
    print("Exemple 2: Single File (un seul PDF)")
    print("="*60)
    
    data = {
        "data": [
            {"name": "Client 1", "address": "Adresse 1\nParis\nFrance"},
            {"name": "Client 2", "address": "Adresse 2\nLyon\nFrance"},
            {"name": "Client 3", "address": "Adresse 3\nMarseille\nFrance"}
        ],
        "singleFile": True
    }
    
    print("📤 Génération d'un PDF unique avec 6 pages (3 recto + 3 verso)...")
    response = requests.post(API_URL, json=data)
    
    if response.status_code == 200:
        with open('example2_single.pdf', 'wb') as f:
            f.write(response.content)
        print(f"✅ Succès! PDF généré: example2_single.pdf ({len(response.content)} bytes)")
    else:
        print(f"❌ Erreur: {response.status_code}")


def example_3_custom_positions():
    """Exemple 3: Positions personnalisées"""
    print("\n" + "="*60)
    print("Exemple 3: Positions Personnalisées")
    print("="*60)
    
    data = {
        "data": [
            {
                "name": "VIP Customer",
                "address": "Special Address\n12345 Custom City\nCountry"
            }
        ],
        "namePosition": {
            "left": 30,      # 30mm depuis la gauche
            "bottom": 260,   # 260mm depuis le bas
            "width": 90,     # 90mm de large
            "height": 25     # 25mm de haut
        },
        "addressPosition": {
            "left": 100,     # 100mm depuis la gauche
            "bottom": 30,    # 30mm depuis le bas
            "width": 95,     # 95mm de large
            "height": 35     # 35mm de haut
        },
        "singleFile": True
    }
    
    print("📤 Génération avec positions personnalisées...")
    print(f"   Nom: left={data['namePosition']['left']}mm, bottom={data['namePosition']['bottom']}mm")
    print(f"   Adresse: left={data['addressPosition']['left']}mm, bottom={data['addressPosition']['bottom']}mm")
    
    response = requests.post(API_URL, json=data)
    
    if response.status_code == 200:
        with open('example3_custom.pdf', 'wb') as f:
            f.write(response.content)
        print(f"✅ Succès! PDF généré: example3_custom.pdf")
    else:
        print(f"❌ Erreur: {response.status_code}")


def example_4_batch_generation():
    """Exemple 4: Génération en masse depuis une liste"""
    print("\n" + "="*60)
    print("Exemple 4: Génération en Masse (Batch)")
    print("="*60)
    
    # Simuler une liste de clients depuis une base de données
    customers = [
        {"name": f"Client {i}", "address": f"Adresse {i}\nVille {i}\nFrance"}
        for i in range(1, 11)  # 10 clients
    ]
    
    data = {
        "data": customers,
        "singleFile": False  # Un PDF par client
    }
    
    print(f"📤 Génération de {len(customers)} PDFs...")
    response = requests.post(API_URL, json=data)
    
    if response.status_code == 200:
        with open('example4_batch.zip', 'wb') as f:
            f.write(response.content)
        print(f"✅ Succès! ZIP avec {len(customers)} PDFs: example4_batch.zip")
    else:
        print(f"❌ Erreur: {response.status_code}")


def example_5_from_database():
    """Exemple 5: Intégration avec base de données (simulée)"""
    print("\n" + "="*60)
    print("Exemple 5: Intégration Base de Données")
    print("="*60)
    
    # Simuler une requête SQL
    print("📊 Récupération des données depuis la DB...")
    
    # Dans un vrai cas, ce serait quelque chose comme:
    # cursor.execute("SELECT name, address FROM customers WHERE status='active'")
    # customers = cursor.fetchall()
    
    # Simulation
    db_customers = [
        {"id": 1, "name": "Société A", "address": "10 Rue du Commerce\n75001 Paris\nFrance"},
        {"id": 2, "name": "Société B", "address": "20 Avenue de la Liberté\n69001 Lyon\nFrance"},
        {"id": 3, "name": "Société C", "address": "30 Boulevard Central\n13001 Marseille\nFrance"}
    ]
    
    print(f"   → {len(db_customers)} clients trouvés")
    
    # Préparer les données pour l'API
    data = {
        "data": [
            {"name": c["name"], "address": c["address"]}
            for c in db_customers
        ],
        "singleFile": True
    }
    
    print("📤 Génération du PDF...")
    response = requests.post(API_URL, json=data)
    
    if response.status_code == 200:
        filename = 'example5_from_db.pdf'
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"✅ Succès! PDF généré: {filename}")
        
        # Dans un vrai cas, vous pourriez envoyer le PDF par email
        # send_email(to=admin_email, attachment=response.content)
    else:
        print(f"❌ Erreur: {response.status_code}")


def example_6_error_handling():
    """Exemple 6: Gestion des erreurs"""
    print("\n" + "="*60)
    print("Exemple 6: Gestion des Erreurs")
    print("="*60)
    
    # Test avec des données invalides
    invalid_data = {
        # Manque le champ "data" requis
        "singleFile": True
    }
    
    print("📤 Test avec données invalides (volontaire)...")
    try:
        response = requests.post(API_URL, json=invalid_data)
        
        if response.status_code == 200:
            print("✅ Succès (inattendu)")
        else:
            print(f"⚠️  Erreur attendue: {response.status_code}")
            error_data = response.json()
            print(f"   Message: {error_data.get('error', 'Erreur inconnue')}")
    except Exception as e:
        print(f"❌ Exception: {e}")


def example_7_minimal():
    """Exemple 7: Minimal (le plus simple possible)"""
    print("\n" + "="*60)
    print("Exemple 7: Minimal (3 lignes)")
    print("="*60)
    
    # Le plus court possible
    r = requests.post(API_URL, json={"data": [{"name": "Test", "address": "Addr"}]})
    open('example7_minimal.zip', 'wb').write(r.content)
    print("✅ Done! example7_minimal.zip")


def check_server():
    """Vérifier que le serveur est actif"""
    print("\n" + "="*60)
    print("Vérification du serveur")
    print("="*60)
    
    try:
        response = requests.get("http://localhost:8002/")
        if response.status_code == 200:
            print("✅ Serveur actif sur http://localhost:8002")
            return True
        else:
            print(f"⚠️  Serveur répond avec le code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Serveur non accessible!")
        print("   Lancez le serveur avec: python app.py")
        return False


def main():
    """Exécuter tous les exemples"""
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  🚀 EXEMPLES D'UTILISATION DE L'API PDF GENERATOR".ljust(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    if not check_server():
        return
    
    # Exécuter tous les exemples
    examples = [
        ("Simple JSON", example_1_simple_json),
        ("Single File", example_2_single_file),
        ("Custom Positions", example_3_custom_positions),
        ("Batch Generation", example_4_batch_generation),
        ("Database Integration", example_5_from_database),
        ("Error Handling", example_6_error_handling),
        ("Minimal Code", example_7_minimal)
    ]
    
    print("\n📋 Exemples disponibles:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"   {i}. {name}")
    
    print("\n" + "="*60)
    choice = input("Choisir un exemple (1-7, ou 'all' pour tous): ").strip()
    
    if choice.lower() == 'all':
        for name, func in examples:
            try:
                func()
            except Exception as e:
                print(f"❌ Erreur dans {name}: {e}")
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        name, func = examples[int(choice) - 1]
        try:
            func()
        except Exception as e:
            print(f"❌ Erreur: {e}")
    else:
        print("❌ Choix invalide")
    
    print("\n" + "="*60)
    print("✅ Terminé!")
    print("="*60)
    print("\n💡 Fichiers générés:")
    import os
    for f in os.listdir('.'):
        if f.startswith('example') and (f.endswith('.pdf') or f.endswith('.zip')):
            size = os.path.getsize(f)
            print(f"   - {f} ({size:,} bytes)")
    
    print("\n🧹 Pour nettoyer:")
    print("   rm -f example*.pdf example*.zip")


if __name__ == "__main__":
    main()

