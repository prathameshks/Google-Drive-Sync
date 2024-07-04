def get_locally_added_files(local_files:dict[str, set[str]], drive_files:dict[str, set[str]])->dict[str,set[str]]:
    locally_added = dict()
    # for each file at drive, check if it exists at local
    local_keys = local_files.keys()
    drive_keys = drive_files.keys()

    for key in local_keys:
        if key not in drive_keys:
            locally_added[key] = local_files[key]
        else: # check if files are same else add files absent in drive
            diff = local_files[key].difference(drive_files[key])
            if(len(diff) > 0):
                locally_added[key] = diff

    return locally_added

def get_locally_deleted_files(local_files:dict[str, set[str]], drive_files:dict[str, set[str]])->dict[str,set[str]]:
    locally_deleted = dict()
    # for each file at local, check if it exists at drive
    local_keys = local_files.keys()
    drive_keys = drive_files.keys()

    for key in drive_keys:
        if key not in local_keys:
            locally_deleted[key] = drive_files[key]
        else: # check if files are same else add files absent in local
            diff = drive_files[key].difference(local_files[key])
            if(len(diff) > 0):
                locally_deleted[key] = diff

    return locally_deleted
    
def get_drive_added_files(local_files:dict[str, set[str]], drive_files:dict[str, set[str]])->dict[str,set[str]]:
    drive_added = dict()
    # for each file at local, check if it exists at drive
    local_keys = local_files.keys()
    drive_keys = drive_files.keys()

    for key in drive_keys:
        if key not in local_keys:
            drive_added[key] = drive_files[key]
        else: # check if files are same else add files absent in local
            diff = drive_files[key].difference(local_files[key])
            if(len(diff) > 0):
                drive_added[key] = diff
                
    return drive_added

def get_drive_deleted_files(local_files:dict[str, set[str]], drive_files:dict[str, set[str]])->dict[str,set[str]]:
    drive_deleted = dict()
    # for each file at local, check if it exists at drive
    local_keys = local_files.keys()
    drive_keys = drive_files.keys()

    for key in local_keys:
        if key not in drive_keys:
            drive_deleted[key] = local_files[key]
        else: # check if files are same else add files absent in local
            diff = local_files[key].difference(drive_files[key])
            if(len(diff) > 0):
                drive_deleted[key] = diff
                
    return drive_deleted

