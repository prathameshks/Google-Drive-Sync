
DRIVE_ROOT_FOLDER = ""

def get_drive_root_folder() -> str:
    return DRIVE_ROOT_FOLDER

def set_drive_root_folder(drive_root_folder: str):
    global DRIVE_ROOT_FOLDER
    DRIVE_ROOT_FOLDER = drive_root_folder
    
    