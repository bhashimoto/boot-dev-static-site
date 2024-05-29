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
