import shutil
import os

from textnode import TextNode

def copy_files(src, dst):
    # Check if paths are valid
    if not os.path.exists(src):
        raise Exception(f"source path {src} does not exist")
    if not os.path.exists(dst):
        raise Exception(f"destination path {dst} does not exist")


    items = os.listdir()
    for item in items:
        if os.path.isfile(item):
            shutil.copy(src=os.path.join(src, item),dst=os.path.join(dst, item))
            print(f"Copying {item} to {dst}")
        else:
            new_src = os.path.join(src, item)
            new_dst = os.path.join(dst, item)
            os.mkdir(new_dst)
            print(f"Created directory: {new_dst}")
            copy_files(new_src, new_dst)

def clear_path(path):
    shutil.rmtree(path)
    print(f"Cleared path {path}")





def main():
    tn = TextNode('This is a text node', 'bold', 'https://www.boot.dev')
    print(tn)

main()
