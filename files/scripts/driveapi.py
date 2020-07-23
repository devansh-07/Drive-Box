from __future__ import print_function
import pickle
import os.path
import io
import shutil
import requests
from mimetypes import MimeTypes
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

class DriveAPI:
    global SCOPES
    SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/userinfo.profile']

    def __init__(self):
        self.creds = None
        self.auth = 1

        if os.path.exists('files/important/token.pickle'):
            with open('files/important/token.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            self.auth = 0

    def _getAuth(self):
        if self.creds and self.creds.expired and self.creds.refresh_token:
            self.creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('files/important/credentials.json', SCOPES)
            self.creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('files/important/token.pickle', 'wb') as token:
            pickle.dump(self.creds, token)

    def _callAPI(self):
        try:
            self.service = build('drive', 'v3', credentials=self.creds)
            self.ppl = build('people', 'v1', credentials=self.creds)
        except:
            return False

    def getFileList(self, pgs=20):
        results = self.service.files().list(pageSize=200, fields="nextPageToken, files(id, name)").execute()
        self.items = results.get('files', [])

        return self.items

    def FileDownload(self, idx, pg):
        file_id = self.items[idx]['id']
        file_name = self.items[idx]['name']
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request, chunksize=204800)
        done = False
        try:
            while not done:
                status, done = downloader.next_chunk()
                pg[0] = str(round(status.progress()*100, 7)).zfill(10)

            fh.seek(0)
            with open(file_name, 'wb') as f:
                shutil.copyfileobj(fh, f)

            return True
        except:
            return False

    def FileUpload(self, filename):
        name = filename.split('/')[-1]
        mimetype = MimeTypes().guess_type(name)[0]
        file_metadata = {'name': name}
        try:
            media = MediaFileUpload(filename, mimetype=mimetype)
            file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        except:
            raise UploadError("Can't Upload File.")

    def _getProfile(self):
        prf = self.ppl.people().get(resourceName='people/me', personFields='names,addresses,photos').execute()

        name = prf['names'][0]['displayName']
        url = prf['photos'][0]['url']

        return (name, url)
