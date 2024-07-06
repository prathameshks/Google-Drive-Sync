from utility import get_drive_file_list,get_local_file_list,get_folder_id
from utility.changes import (
    get_drive_added_files,
    get_drive_deleted_files,
    get_locally_added_files,
    get_locally_deleted_files,
)
from utility.log import write_log, write_to_file, pretty_print_dict

# local_files = get_local_file_list(r"D:\Coding\Google-Drive-Sync\test")
# drive_files = get_drive_file_list(r"1t2GDmtyZsa4X_a3tn23UvLR4dcGurba_")

# print(pretty_print_dict(local_files))
# print(pretty_print_dict(drive_files))
def path(folder_path: str) -> str:
    if folder_path == "." or folder_path == "":
        return "root"

    path = folder_path.split("\\")
    current_folder_name = path[0]
    remaining_path = "\\".join(path[1:]) if len(path) > 1 else ""
    print(current_folder_name)
    print(remaining_path)

def test_diff():
    write_to_file("Local files: ")
    write_to_file(pretty_print_dict(local_files))

    write_to_file("Drive Files: ")
    write_to_file(pretty_print_dict(drive_files))

    write_to_file("CHANGES: ")

    write_to_file("Locally added files: ")
    write_to_file(pretty_print_dict(get_locally_added_files(local_files, drive_files)))

    write_to_file("Locally deleted files: ")
    write_to_file(
        pretty_print_dict(get_locally_deleted_files(local_files, drive_files))
    )

    write_to_file("Drive added files: ")
    write_to_file(pretty_print_dict(get_drive_added_files(local_files, drive_files)))

    write_to_file("Drive deleted files: ")
    write_to_file(pretty_print_dict(get_drive_deleted_files(local_files, drive_files)))

print(get_folder_id("1t2GDmtyZsa4X_a3tn23UvLR4dcGurba_","\\se\\"))
# path("college\\se")