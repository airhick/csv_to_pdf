FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances système nécessaires pour ReportLab
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tous les fichiers de l'application
COPY . .

# Exposer le port (Coolify utilisera la variable d'environnement PORT)
EXPOSE 8002

# Commande de démarrage
CMD ["python", "app.py"]

