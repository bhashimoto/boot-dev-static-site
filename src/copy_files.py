from shutil import copy
import os

def copy_files(src, dst) -> None:
    # Check if paths are valid
    if not os.path.exists(src):
        raise Exception(f"source path {src} does not exist")
    if not os.path.exists(dst):
        raise Exception(f"destination path {dst} does not exist")


    items = os.listdir(src)
    for item in items:
        new_src = os.path.join(src, item)
        new_dst = os.path.join(dst, item)
        print(f"current item: {new_src}")
        if os.path.isfile(new_src):
            copy(src=new_src, dst=new_dst)
            print(f"Copying {new_src} to {new_dst}")
        else:
            os.mkdir(new_dst)
            print(f"Created directory: {new_dst}")
            copy_files(new_src, new_dst)
