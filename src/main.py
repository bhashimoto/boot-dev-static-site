import shutil
import os

from textnode import TextNode

def copy_files(src, dst):
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
            shutil.copy(src=new_src, dst=new_dst)
            print(f"Copying {new_src} to {new_dst}")
        else:
            os.mkdir(new_dst)
            print(f"Created directory: {new_dst}")
            copy_files(new_src, new_dst)

def reset_public():
    path = 'public'
    shutil.rmtree(path)
    os.mkdir(path)
    print(f"Cleared path {path}")





def main():
    src = os.path.join(os.path.curdir, 'static')
    dst = os.path.join(os.path.curdir, 'public')
    print("starting application")
    
    print("clearing path")
    reset_public()
    copy_files(src, dst)


    tn = TextNode('This is a text node', 'bold', 'https://www.boot.dev')
    print(tn)

main()
