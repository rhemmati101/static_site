import shutil
import os

def copy_directory(source_path: str, destination_path: str) -> None:
    if not (os.path.exists(source_path) and os.path.exists(destination_path)):
        raise ValueError("invalid path passed as input")
    
    if not os.path.isdir(source_path) or not os.path.isdir(destination_path):
        raise ValueError("path inputs must be directories")
    
    #delete all files in destination directory
    shutil.rmtree(destination_path)
    os.mkdir(destination_path)

    #copy files from source to destination
    recursive_copy(source_path, destination_path, "")

def recursive_copy(source_path: str, destination_path: str, extension_from_paths: str) -> None:
    curr_source_path: str = os.path.join(source_path, extension_from_paths)
    curr_destination_path: str = os.path.join(destination_path, extension_from_paths)
    
    if not (os.path.exists(curr_source_path) and os.path.exists(curr_destination_path)):
        raise ValueError("invalid path passed as input")
    
    #source path input is a directory if it has made it here
    contents: list[str] = os.listdir(curr_source_path)
    print(f"contents of {curr_source_path}: {contents}")

    for c in contents:
        c_path: str = os.path.join(curr_source_path, c)

        if os.path.isfile(c_path):
            shutil.copy(c_path, curr_destination_path)
            print(f"copying file {c} to the folder {curr_destination_path}")
        elif os.path.isdir(c_path):
            os.mkdir(os.path.join(curr_destination_path, c))
            print(f"making directory {os.path.join(curr_destination_path, c)}")
            recursive_copy(source_path, destination_path, os.path.join(extension_from_paths, c))
        else:
            raise NotImplementedError()