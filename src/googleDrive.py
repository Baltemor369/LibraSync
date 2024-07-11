from src.const import *

import os.path
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive"]

class GoogleAuth:
    def __init__(self):
        self.creds = None
        
    def authentification(self):
        print("Authentification...")
        if os.path.exists(TOKEN):
            self.creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(CREDS, SCOPES)
                    self.creds = flow.run_local_server(port=0)

                    with open(TOKEN, "w") as token:
                        token.write(self.creds.to_json())
                    return True
                except Exception as error:
                    print(f"[Error101] In authentification : {error}")
                    return False

        return self.creds.valid if self.creds else False

    def load(self):
        print("Loading data...")
        try:
            # build the object to interact with Google Drive API
            service = build("drive", "v3", credentials=self.creds)
        except Exception as error:
            print(f"[Error201] In building service: {error}")
            return False
        try:
            # get the list of files named 'data.db' in the root directory of the Google Drive account
            query = f"name='{DATA_FILE}'"
            results = service.files().list(q=query, fields='files(id, name)').execute()
            items = results.get('files', [])
        except Exception as error:
            print(f"File '{DATA_FILE}' not found.")
        
        if not items:
            try:
                print(f"File {DATA_FILE} not found. Creation...")
                file_metadata = {"name": DATA_FILE}
                media = MediaFileUpload(DATA_FILE, mimetype="application/octet-stream")
                service.files().create(body=file_metadata, media_body=media).execute()
                print(f"File {DATA_FILE} created successfully")
            except Exception as e:
                print(f"[Error203] Cannot create file {DATA_FILE} : {e}")
                return False
            try:
                # update the request to get the ID of the file created
                results = service.files().list(q=query, fields='files(id, name)').execute()
                items = results.get('files', [])
            except Exception as e:
                print(f"[Error204] Cannot update the request to get files : {e}")
                return False
        
        try:
            file_id = items[0]['id']
        except Exception as e:
            print(f"[Error205] Cannot get file ID: {e}")
            return False
        
        try:
            request = service.files().get_media(fileId=file_id)

            fh = io.FileIO(DATA_FILE, "wb")
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            print(f"File {DATA_FILE} loaded successfully")
            return True
        except Exception as e:
            print(f"[Error206] In loading: {e}")
            return False

    def save(self):
        print("Saving data...")
        try:
            # build the object to interact with Google Drive API
            service = build("drive", "v3", credentials=self.creds)
        except Exception as e:
            print(f"[Error301] In building service: {e}")
            return False
        try:
            query = f"name='{DATA_FILE}'"
            results = service.files().list(q=query, fields='files(id, name)').execute()
            items = results.get('files', [])
            file_id = items[0]['id']
        except Exception as e:
            print(f"[Error302] In getting file ID: {e}")
            return False
        try:
            # create a MediaFileUpload object
            media = MediaFileUpload(DATA_FILE, mimetype="application/octet-stream", resumable=True)
            # update the file on Google Drive
            request = service.files().update(fileId=file_id, media_body=media)
            # execute the request
            response = None
            while response is None:
                status, response = request.next_chunk()
            print(f"File {DATA_FILE} saved successfully on Google Drive")
            return True
        except Exception as e:
            print(f"[Error302] In saving: {e}")
            return False
