from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import pickle

print(" Étape 1 : Authentification")
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', 
        ['https://www.googleapis.com/auth/drive.file']
    )
    creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

print(' Étape 2 : Construction du service')
drive_service = build('drive', 'v3', credentials=creds)

print(" Étape 3 : Téléchargement du fichier")
file_metadata = {
    'name': 'data.db',
    'mimeType': 'application/octet-stream'
}
media = MediaFileUpload('data\data.db', mimetype='application/octet-stream')
file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

print("Vérification du succès du téléchargement")
if file:
    print('Fichier téléchargé avec succès, ID:', file.get('id'))
else:
    print('Le téléchargement a échoué')
