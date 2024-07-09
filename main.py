from src.interface import *
from src.const import *

import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
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


def  load(creds):
    # build the object to interact with Google Drive API
    service = build("drive", "v3", credentials=creds)
    # get the list of files named 'data.db'
    results = service.files().list(q=f"name={DATA_FILE}").execute()
    print(results)
    items = results.get("files", [])

    # if no file named 'data.db' is found, create it
    if not items:
        file_metadata = {"name": DATA_FILE}
        media = MediaFileUpload(DATA_FILE, mimetype="application/octet-stream")
        service.files().create(body=file_metadata, media_body=media).execute()
        print(f"File {DATA_FILE} created.")
    # if the file named 'data.db' is found, load its content
    else:
        file_id = items[0]["id"]
        request = service.files().get(fileId=file_id)
        with open(DATA_FILE, "wb") as data_file:
            data = json.dumps(request.execute())
            data_file.write(data.encode())


if __name__ == "__main__":
    if authentification():
        load(creds)
        # Interface()