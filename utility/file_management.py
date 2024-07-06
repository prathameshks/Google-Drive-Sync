import os
from utility.google_connection import get_service
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from utility.settings import get_drive_root_folder


def get_folder_id(folder_path: str, root: str = get_drive_root_folder(), service = get_service()) -> str:
    """Returns the ID of the folder at the given path. If the folder is not present, it will be created.

    Args:
        root (str): The ID of the root folder.
        folder_path (str): The path (relative path from root, "." for root) of the folder to retrieve the ID of.
        service: The service object to use.

    Returns:
        str: The ID of the folder at the given path.
    """
    folder_path = folder_path.strip("\\")
    # Handle root
    if folder_path == "." or folder_path == "":
        return root

    path = folder_path.split("\\")
    current_folder_name = path[0]
    remaining_path = "\\".join(path[1:]) if len(path) > 1 else ""

    results = (
        service.files()
        .list(
            q=f"'{root}' in parents and mimeType = 'application/vnd.google-apps.folder' and name = '{current_folder_name}'",
            spaces="drive",
            fields="nextPageToken, files(id, name)",
        )
        .execute()
    )
    items = results.get("files", [])

    if not items:
        # Create the folder
        file_metadata = {
            "name": current_folder_name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [root],
        }
        file = service.files().create(body=file_metadata, fields="id").execute()
        folder_id = file.get("id")
    else:
        folder_id = items[0].get("id")

    if not remaining_path:
        return folder_id

    return get_folder_id(remaining_path, folder_id, service)

def upload_file(local_path: str, drive_folder_id: str, service = get_service()) -> str:
    """Uploads a file to Google Drive.

    Args:
        local_path (str): The path to the local file to upload.
        drive_folder_id (str): The ID of the folder to upload the file to.
        service: The service object to use.

    Returns:
        str: The ID of the uploaded file.
    """
    file_metadata = {"name": os.path.basename(local_path), "parents": [drive_folder_id]}
    media = MediaFileUpload(local_path, mimetype="application/octet-stream")
    file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    return file.get("id")

def download_file(drive_file_id: str, local_path: str, service = get_service()) -> None:
    """Downloads a file from Google Drive.

    Args:
        drive_file_id (str): The ID of the file to download.
        local_path (str): The path to the local file to download to.
        service: The service object to use.
    """
    request = service.files().get_media(fileId=drive_file_id)
    fh = open(local_path, "wb")
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

    fh.close()
    
def get_file_id(file_name: str, drive_folder_path: str, service = get_service()) -> str:
    """Returns the ID of the file at the given path. If the file is not present, return None.

    Args:
        file_name (str): The name of the file to retrieve the ID of.
        drive_folder_path (str): The path (relative path from root, "." for root) of the folder to retrieve the ID of.
        service: The service object to use.

    Returns:
        str: The ID of the file at the given path.
    """
    drive_folder_id = get_folder_id(drive_folder_path, get_drive_root_folder(), service)
    results = (
        service.files()
        .list(
            q=f"'{drive_folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and name = '{file_name}'",
            spaces="drive",
            fields="nextPageToken, files(id, name)",
        )
        .execute()
    )
    items = results.get("files", [])
    
    if(not items):
        return None

    return items[0].get("id")

def delete_drive_file(drive_file_id: str, service = get_service()) -> None:
    """Deletes a file from Google Drive.

    Args:
        drive_file_id (str): The ID of the file to delete.
        service: The service object to use.
    """
    service.files().delete(fileId=drive_file_id).execute()

def delete_drive_folder(drive_folder_id: str, service = get_service()) -> None:
    """Deletes a folder from Google Drive.

    Args:
        drive_folder_id (str): The ID of the folder to delete.
        service: The service object to use.
    """
    service.files().delete(fileId=drive_folder_id).execute()

def delete_local_folder(local_folder_path: str) -> None:
    """Deletes a local folder.

    Args:
        local_folder_path (str): The path to the local folder to delete.
    """
    os.remove(local_folder_path)
    
def delete_local_file(local_file_path: str) -> None:
    """Deletes a local file.

    Args:
        local_file_path (str): The path to the local file to delete.
    """
    os.remove(local_file_path)
    

    