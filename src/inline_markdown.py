import re
from htmlnode import LeafNode
from textnode import TextNode, TextNodeType

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextNodeType.text_type_text:
        return LeafNode(value=text_node.text)
    if text_node.text_type == TextNodeType.text_type_bold:
        return LeafNode(tag='b', value=text_node.text)
    if text_node.text_type == TextNodeType.text_type_italic:
        return LeafNode(tag='i', value=text_node.text)
    if text_node.text_type == TextNodeType.text_type_code:
        return LeafNode(tag='code', value=text_node.text)
    if text_node.text_type == TextNodeType.text_type_link:
        return LeafNode(tag='a', value=text_node.text, props={'href':text_node.url})
    if text_node.text_type == TextNodeType.text_type_image:
        return LeafNode(tag='img', value='', props={'src':text_node.url, 'alt':text_node.text})
    raise Exception(f"Invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextNodeType.text_type_text:
            new_nodes.append(node)
        else:
            texts: list[str] = node.text.split(delimiter)
            if len(texts) % 2 == 0:
                raise Exception(f"matching delimiter ({delimiter}) not found")
            is_outside = True
            for text in texts:
                if text != "":
                    node_type = TextNodeType.text_type_text if is_outside else text_type
                    new_text_node = TextNode(text=text, text_type=node_type)
                    new_nodes.append(new_text_node)
                is_outside = not is_outside
    return new_nodes

def extract_markdown_images(text: str) -> list[str]:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text: str) -> list[str]:
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextNodeType.text_type_text:
            new_nodes.append(node)
            continue
        
        original_text = node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})",1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            new_nodes.append(TextNode(sections[0], TextNodeType.text_type_text))
            new_nodes.append(TextNode(image[0], TextNodeType.text_type_image, image[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(text=original_text, text_type=TextNodeType.text_type_text))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextNodeType.text_type_text:
            new_nodes.append(node)
            continue
        
        original_text = node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})",1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            new_nodes.append(TextNode(sections[0], TextNodeType.text_type_text))
            new_nodes.append(TextNode( link[0], TextNodeType.text_type_link, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(text=original_text, text_type=TextNodeType.text_type_text))

    return new_nodes

def text_to_text_nodes(text: str) -> list[TextNode]:
    text_node = TextNode(text, TextNodeType.text_type_text)
    nodes = [text_node]

    nodes = split_nodes_delimiter(nodes,'**',TextNodeType.text_type_bold)
    nodes = split_nodes_delimiter(nodes,'*',TextNodeType.text_type_italic)
    nodes = split_nodes_delimiter(nodes,'`',TextNodeType.text_type_code)

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


