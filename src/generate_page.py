import os
from os.path import isfile
from block_markdown import markdown_to_html_node
from shutil import rmtree

def reset_public() -> None:
    path = 'public'
    rmtree(path)
    os.mkdir(path)
    print(f"Cleared path {path}")

def extract_title(markdown) -> str:
    lines:list[str] = markdown.split('\n')
    for line in lines:
        text = line.lstrip('# ')
        if len(text) == len(line) - 2:
            return text
    raise ValueError('markdown has no title')

def generate_page(from_path, template_path, dest_path) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    f = open(from_path)
    markdown = f.read()
    f.close()

    f = open(template_path)
    template = f.read()
    f.close()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    full_html = template.replace('{{ Title }}', str(title)).replace('{{ Content }}', html)

    head, _ = os.path.split(dest_path)
    os.makedirs(head, exist_ok=True)
    file_name = dest_path.rstrip('md') + 'html'
    with open(file_name, 'w') as f:
        print(full_html, file=f)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    items = os.listdir(dir_path_content)
    for item in items:
        item_path = os.path.join(dir_path_content, item)
        item_dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(item_path):
            generate_page(item_path, template_path, item_dest_path)
        else:
            generate_pages_recursive(item_path, template_path, item_dest_path)
