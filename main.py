from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        # get the folder from local storage to sync
        folder = input("Enter the folder path to sync: ")
        folder = folder.replace('\\', '/')

        # select the folder in google drive
        folder_id = input("Enter the folder ID in Google Drive: ")
        
        print("Syncing folder: " + folder)
        print("Folder ID: " + folder_id)

        # get the list of files in the folder
        drive_files = []
        local_files = []

        page_token = None
        while True:
            response = service.files().list(q="'" + folder_id + "' in parents",
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name)',
                                            pageToken=page_token).execute()
            for file in response.get('files', []):
                # Process change
                drive_files.append(file.get('name'))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        # get the list of files in the local folder
        for file in os.listdir(folder):
            local_files.append(file)

        # compare the lists
        # files to be uploaded
        upload_files = []
        for file in local_files:
            if file not in drive_files:
                upload_files.append(file)

        # files to be downloaded
        download_files = []
        for file in drive_files:
            if file not in local_files:
                download_files.append(file)

        # display the files to be uploaded
        print("Files to be uploaded:")
        for file in upload_files:
            print(file)

        # display the files to be downloaded
        print("Files to be downloaded:")
        for file in download_files:
            print(file)

        # upload the files
        for file in upload_files:
            file_metadata = {
                'name': file,
                'parents': [folder_id]
            }
            media = MediaFileUpload(folder + "/" + file)
            file = service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
            print('uploaded File ID: %s' % file.get('id'))

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()