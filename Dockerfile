# Utilisez l'image officielle Python 3.12.3 comme image de base
FROM python:3.12.3

# Définissez le répertoire de travail dans le conteneur
WORKDIR /librasync

# Copiez les fichiers de votre projet dans le répertoire de travail
COPY . /librasync

# Installez tkinter et sqlite3 via le gestionnaire de paquets de l'image
RUN apt-get update && apt-get install -y python3

# Définissez la commande pour exécuter votre application
CMD ["python", "./main.py"]
