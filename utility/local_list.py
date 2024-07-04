import os

def get_local_file_list(local_path:str)->dict[str, set[str]]:
    """
    Returns a list of all files and folders within the given local path.

    Parameters:
        local_path (str): The path to the local directory to search.

    Returns:
        dict: A dictionary containing the relative path as key and a set of files at the path as value.
    """
    
    file_list = dict()
    for root, dirs, files in os.walk(local_path):
        # remove local path from beginning ex 'D:/IMP Docs\\' using os relpath relative path
        root = os.path.relpath(root, local_path)
        file_list[root] = set(files)

    return file_list

if __name__ == "__main__":
    local_list = get_local_file_list("D:/IMP Docs")
    print(local_list)