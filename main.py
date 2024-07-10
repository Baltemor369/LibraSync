from src.interface import *
from src.const import *

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive"]
creds = None

def authentification():
    global creds
    creds = None
    if os.path.exists(TOKEN):
        creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(CREDS, SCOPES)
                creds = flow.run_local_server(port=0)

                with open(TOKEN, "w") as token:
                    token.write(creds.to_json())
                
            except Exception as error:
                print(f"An error occurred: {error}")

    return creds.valid if creds else False


def load(creds):
    try:
        # build the object to interact with Google Drive API
        service = build("drive", "v3", credentials=creds)

        # get the list of files named 'data.db' in the root directory of the Google Drive account
        query = f"name='{DATA_FILE}'"
        results = service.files().list(q=query, fields='files(id, name)').execute()
        items = results.get('files', [])

        if not items:
            print(f"File {DATA_FILE} not found. Creation...")
            file_metadata = {"name": DATA_FILE}
            media = MediaFileUpload(DATA_FILE, mimetype="application/octet-stream")
            service.files().create(body=file_metadata, media_body=media).execute()
            print(f"File {DATA_FILE} created successfully")
            
            # get the id of the newly created file
            results = service.files().list(q=query, fields='files(id, name)').execute()
            items = results.get('files', [])
            
        file_id = items[0]['id']
        request = service.files().get_media(fileId=file_id)

        with open(DATA_FILE, "wb") as data_file:
            downloader = MediaIoBaseDownload(data_file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
        print(f"File {DATA_FILE} loaded successfully")
        return True
    except Exception as e:
        print(f"A error occured : {e}")
        return False

if __name__ == "__main__":
    if authentification():
        print(f"Google authentification successful")
        if load(creds):
            Interface()
            pass