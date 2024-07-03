from utility.google_connection import get_service
import os


def get_drive_file_list(root_folder_id : str) -> dict[str, list[str]]:
    """Retrieves a list of files and folders from Google Drive.

    Args:
        root_folder_id (str): The ID of the folder to list files in.

    Returns:
        dict: A dictionary containing the relative path as key and a list of files at the path as value.
    """
    
    service = get_service()

    files_and_folders = dict()

    def _get_files_in_folder(folder_id, path):
        """Retrieves files within a specific folder and recursively calls itself for subfolders.

        Args:
            folder_id: The ID of the folder to list files in.
            path: The current path to the folder (used for building the final path).
        """
        query = f"'{folder_id}' in parents"
        results = (
            service.files()
            .list(q=query, fields="nextPageToken, files(id, name, mimeType)")
            .execute()
        )
        items = results.get("files", [])
        item_list = []
        for item in items:
            if item["mimeType"] == "application/vnd.google-apps.folder":
                sub_path = os.path.join(path, item["name"])
                _get_files_in_folder(item["id"], sub_path)
            else:
                item_list.append(item["name"])

        files_and_folders[path] = item_list 

    # Get the root folder (change 'root' to a specific folder ID if needed)
    results = (
        service.files()
        .list(q=f"'{root_folder_id}' in parents", fields="nextPageToken, files(id, name, mimeType)")
        .execute()
    )
    items = results.get("files", [])
    item_list = []
    for item in items:
        if item["mimeType"] == "application/vnd.google-apps.folder":
            _get_files_in_folder(item["id"], item["name"])
        else:
            item_list.append(item["name"])

    files_and_folders['.'] = item_list

    return files_and_folders

if __name__ == "__main__":
    files_and_folders = get_drive_file_list("root")
    print(files_and_folders)
