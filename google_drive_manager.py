import io
import json
import os
import tempfile

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload


class GoogleDriveManager:
    def __init__(self, client_credentials_file):
        self.client_credentials_file = client_credentials_file
        self.scopes = ['https://www.googleapis.com/auth/drive']
        self.credentials = self.get_credentials()

        if self.credentials:
            self.drive_service = build('drive', 'v3', credentials=self.credentials)

    def get_credentials(self):
        flow = InstalledAppFlow.from_client_secrets_file(self.client_credentials_file, self.scopes)
        credentials = flow.run_local_server(port=0)
        return credentials

    def create_folder(self, folder_name, parent_folder_id=None):
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_folder_id:
            file_metadata['parents'] = [parent_folder_id]

        folder = self.drive_service.files().create(body=file_metadata, fields='id').execute()
        return folder.get('id')

    def get_folder_id(self, folder_path):
        folders = folder_path.split('/')
        folder_id = 'root'
        for folder in folders:
            folder_id = self._get_sub_folder_id(folder, folder_id)
            if not folder_id:
                return None
        return folder_id

    def _get_sub_folder_id(self, folder_name, parent_folder_id):
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and '{parent_folder_id}' in parents and trashed=false"
        response = self.drive_service.files().list(q=query, fields='files(id)').execute()
        folders = response.get('files', [])
        if folders:
            return folders[0]['id']
        else:
            return None

    def write_json_to_drive(self, data, sub_folder_name, file_name):
        base_folder_id = self.get_folder_id('Projects/MovieReviews')
        if not base_folder_id:
            base_folder_id = self.get_folder_id('Projects')
            if not base_folder_id:
                base_folder_id = self.create_folder('Projects')
            base_folder_id = self.create_folder('MovieReviews', base_folder_id)

        sub_folder_id = self.get_folder_id(f'Projects/MovieReviews/{sub_folder_name}')
        if not sub_folder_id:
            sub_folder_id = self.create_folder(sub_folder_name, base_folder_id)

        temp_file_path = None
        try:
            temp_file_path = tempfile.mktemp(suffix='.json')
            with open(temp_file_path, 'w') as temp_file:
                json.dump(data, temp_file)

            file_metadata = {
                'name': file_name,
                'parents': [sub_folder_id],
                'mimeType': 'application/json'
            }

            media = MediaFileUpload(temp_file_path, mimetype='application/json')
            self.drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(f'File "{file_name}" uploaded successfully to Google Drive.')
        except Exception as e:
            print(f'An error occurred while saving "{file_name}" to Google Drive: {e}')
        finally:
            if temp_file_path:
                os.remove(temp_file_path)

    def read_json_from_drive(self, sub_folder_name, file_name):
        sub_folder_id = self.get_folder_id(f'Projects/MovieReviews/{sub_folder_name}')
        if not sub_folder_id:
            print(f'Subfolder "{sub_folder_name}" not found.')
            return None

        query = f"name='{file_name}' and mimeType='application/json' and '{sub_folder_id}' in parents and trashed=false"
        response = self.drive_service.files().list(q=query, fields='files(id)').execute()
        files = response.get('files', [])
        if not files:
            print(f'File "{file_name}" not found in subfolder "{sub_folder_name}".')
            return None

        file_id = files[0]['id']
        request = self.drive_service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            _, done = downloader.next_chunk()

        file.seek(0)
        return json.load(file)

    def delete_file(self, file_id):
        try:
            self.drive_service.files().delete(fileId=file_id).execute()
            print(f'File with ID "{file_id}" deleted successfully from Google Drive.')
        except Exception as e:
            print(f'An error occurred: {e}')

    def delete_folder_and_contents(self, folder_id):
        try:
            # Get a list of all files in the folder
            files = self.drive_service.files().list(q=f"'{folder_id}' in parents", fields="files(id)").execute()
            for file in files.get('files', []):
                self.delete_file(file['id'])

            # Recursively delete subfolders
            subfolders = self.drive_service.files().list(
                q=f"mimeType='application/vnd.google-apps.folder' and '{folder_id}' in parents",
                fields="files(id)").execute()
            for subfolder in subfolders.get('files', []):
                self.delete_folder_and_contents(subfolder['id'])

            # Finally, delete the folder itself
            self.delete_file(folder_id)
            print(f'Folder with ID "{folder_id}" and its contents deleted successfully from Google Drive.')
        except Exception as e:
            print(f'An error occurred: {e}')


# Example usage:
if __name__ == "__main__":
    credentials_file_path = 'credentials_client_id.json'
    drive = GoogleDriveManager(credentials_file_path)

    folder_id = drive.get_folder_id('Projects/MovieReviews')
    print(folder_id)

    # Write data to Google Drive
    data = {"movies": ["Movie1", "Movie2", "Movie3"]}
    sub_folder_name = "movies"
    file_name = "movies.json"
    drive.write_json_to_drive(data, sub_folder_name, file_name)

    # Read data from Google Drive
    read_data = drive.read_json_from_drive(sub_folder_name, file_name)
    print("Data read from Google Drive:", read_data)
