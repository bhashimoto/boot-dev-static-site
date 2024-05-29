import re
from htmlnode import LeafNode
from textnode import TextNode, TextNodeType

def text_node_to_html_node(text_node):
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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextNodeType.text_type_text:
            new_nodes.append(node)
        else:
            texts = node.text.split(delimiter)
            if len(texts) % 2 == 0:
                raise Exception(f"matching delimiter ({delimiter}) not found")
            outside = True
            for text in texts:
                node_type = TextNodeType.text_type_text if outside else text_type
                new_text_node = TextNode(text=text, text_type=node_type)
                new_nodes.append(new_text_node)
                outside = not outside
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        matches = extract_markdown_images(node.text)
        if matches == []:
            new_nodes.append(node)
        else:
            working_text = node.text 
            for idx, match in enumerate(matches):
                splits = working_text.split(f"![{match[0]}]({match[1]})", 1)
                # append left side (must not be empty)
                if splits[0] != "":
                    new_text_node = TextNode(text=splits[0], text_type=node.text_type)
                    new_nodes.append(new_text_node)
                # append image node
                new_image_node = TextNode(text=match[0], text_type=TextNodeType.text_type_image, url=match[1])
                new_nodes.append(new_image_node)
                # append right side (must be last item and not be empty)
                if idx == len(matches) - 1 and  splits[1] != "":
                    new_text_node = TextNode(text=splits[1], text_type=node.text_type)
                    new_nodes.append(new_text_node)
                working_text = splits[1]
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        matches = extract_markdown_links(node.text)
        if matches == []:
            new_nodes.append(node)
        else:
            working_text = node.text 
            for idx, match in enumerate(matches):
                splits = working_text.split(f"[{match[0]}]({match[1]})", 1)
                # append left side (must not be empty)
                if splits[0] != "":
                    new_text_node = TextNode(text=splits[0], text_type=node.text_type)
                    new_nodes.append(new_text_node)
                # append image node
                new_link_node = TextNode(text=match[0], text_type=TextNodeType.text_type_link, url=match[1])
                new_nodes.append(new_link_node)
                # append right side (must be last item and not be empty)
                if idx == len(matches) - 1 and  splits[1] != "":
                    new_text_node = TextNode(text=splits[1], text_type=node.text_type)
                    new_nodes.append(new_text_node)
                working_text = splits[1]
    return new_nodes

def text_to_text_nodes(text):
    text_node = TextNode(text, TextNodeType.text_type_text)
    nodes = [text_node]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    nodes = split_nodes_delimiter(nodes,'**',TextNodeType.text_type_bold)
    nodes = split_nodes_delimiter(nodes,'*',TextNodeType.text_type_italic)
    nodes = split_nodes_delimiter(nodes,'`',TextNodeType.text_type_code)

    return nodes


