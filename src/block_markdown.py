from htmlnode import ParentNode
from inline_markdown import text_node_to_html_node, text_to_text_nodes


class BlockType:
    block_type_paragraph = 'paragraph'
    block_type_heading1 = 'heading1'
    block_type_heading2 = 'heading2'
    block_type_heading3 = 'heading3'
    block_type_heading4 = 'heading4'
    block_type_heading5 = 'heading5'
    block_type_heading6 = 'heading6'
    block_type_code = 'code'
    block_type_quote = 'quote'
    block_type_ul = 'ul'
    block_type_ol = 'ol'

    

def markdown_to_blocks(text):
    blocks = text.split('\n\n')
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        filtered_blocks.append(block.strip())
    return filtered_blocks

def block_to_block_type(block):
    if block[0] == '#':
        return 'heading' + str(len(block) - len(block.lstrip('#')))
    
    if block[:3] == '```' and block[-3:] == '```':
        return BlockType.block_type_code

    if block[0] == '>':
        lines = block.split('\n')
        for line in lines:
            if line[0] != '>':
                return BlockType.block_type_paragraph
        return BlockType.block_type_quote
    
    if block[0] in ['*', '-']:
        lines = block.split('\n')
        for line in lines:
            if line[0] not in ['*','-'] or line[1] != ' ':
                return BlockType.block_type_paragraph
        return BlockType.block_type_ul

    if block[0] == '1':
        lines = block.split('\n')
        current = 0
        for line in lines:
            splits = line.split('.', 1)
            if (int(splits[0]) != (current + 1)) or splits[1][0] != ' ':
                return BlockType.block_type_paragraph
            current += 1
        return BlockType.block_type_ol

    return BlockType.block_type_paragraph


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    if len(blocks) == 0:
        raise ValueError("markdown must have at least one block")

    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.block_type_quote:
                nodes.append(create_block_quote_node(block))
            case BlockType.block_type_ul:
                nodes.append(create_ul_node(block))
            case BlockType.block_type_ol:
                nodes.append(create_ol_node(block))
            case BlockType.block_type_code:
                nodes.append(create_code_node(block))
            case block_type if 'heading' in block_type:
                nodes.append(create_heading_node(block))
            case _:
                nodes.append(create_paragraph_node(block))
    return ParentNode(tag='div', children=nodes)


def create_block_quote_node(block):
    text_nodes = text_to_text_nodes(block)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return ParentNode(tag='blockquote', children=html_nodes)

def create_ul_node(block):
    lines = block.split('\n')
    html_nodes = []
    for line in lines:
        html_nodes.append(ParentNode(tag='li',children=text_node_to_html_node(text_to_text_nodes(line))))
    return ParentNode(tag='ul', children=html_nodes)

def create_ol_node(block):
    lines = block.split('\n')
    html_nodes = []
    for line in lines:
        html_nodes.append(ParentNode(tag='li',children=text_node_to_html_node(text_to_text_nodes(line))))
    return ParentNode(tag='ol', children=html_nodes)

def create_code_node(block):
    lines = block.split('\n')
    html_nodes = []
    for line in lines:
        html_nodes.append(text_node_to_html_node(text_to_text_node(line)))
    return ParentNode(tag='pre', children=[ParentNode(tag='code', children=html_nodes)])

def create_heading_node(block):
    text = block.lstrip('#')
    num = len(block) - len(text)
    return ParentNode(tag=f'h{len(num)}', children=text_node_to_html_node(text_to_text_nodes(text)))

def create_paragraph_node(block):
    return ParentNode(tag='p', children=text_to_text_nodes(text_to_text_nodes(block)))
    
