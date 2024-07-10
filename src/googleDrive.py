from src.const import *

import os.path
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
                    
                except Exception as error:
                    print(f"Error occurred in authentification : {error}")

        return self.creds.valid if self.creds else False

    def load(self):
        try:
            # build the object to interact with Google Drive API
            service = build("drive", "v3", credentials=self.creds)

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
            print(f"A error occured in loading: {e}")
            return False

    def save(self):
        try:
            # build the object to interact with Google Drive API
            service = build("drive", "v3", credentials=self.creds)
        except Exception as e:
            print(f"Error occurred in building service: {e}")
        try:
            query = f"name='{DATA_FILE}'"
            results = service.files().list(q=query, fields='files(id, name)').execute()
            items = results.get('files', [])
            file_id = items[0]['id']
        except Exception as e:
            print(f"Error occurred in getting file ID: {e}")
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
        except Exception as e:
            print(f"Error occurred in saving: {e}")
