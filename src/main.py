import os



from copy_files import copy_files
from generate_page import generate_pages_recursive, reset_public




def main():
    src = os.path.join(os.path.curdir, 'static')
    dst = os.path.join(os.path.curdir, 'public')
    print("starting application")
    
    print("clearing path")
    reset_public()
    copy_files(src, dst)

    generate_pages_recursive('content', 'template.html', 'public') 


main()
