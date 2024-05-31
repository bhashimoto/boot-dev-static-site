import shutil
import os

from block_markdown import markdown_to_html_node
from htmlnode import HTMLNode
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


def extract_title(markdown):
    html = markdown_to_html_node(markdown)
    return extract_title_from_html(html)

def extract_title_from_html(html:HTMLNode):
    if html.tag == 'h1':
        return html.value
    
    if html.children is None:
        return None

    for child in html.children:
        if extract_title_from_html(child) is not None:
            return child.value
    raise Exception('markdown has no title')

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    f = open(from_path)
    markdown = f.read()
    f.close()

    f = open(template_path)
    template = f.read()
    f.close()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    full_html = template.replace('{{ Title }}', title).replace('{{ Content }}', html)

    os.makedirs(dest_path, exist_ok=True)
    with open(dest_path, 'w') as f:
        print(full_html, file=f)

def main():
    src = os.path.join(os.path.curdir, 'static')
    dst = os.path.join(os.path.curdir, 'public')
    print("starting application")
    
    print("clearing path")
    reset_public()
    copy_files(src, dst)

    generage_page('content/index.md', 'template.html', 'public/index.html') 


    tn = TextNode('This is a text node', 'bold', 'https://www.boot.dev')
    print(tn)

main()
