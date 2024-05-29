import unittest

from block_markdown import BlockType, markdown_to_blocks, block_to_block_type

class TestBlockMarkdownToTextConversion(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""
        blocks = markdown_to_blocks(text)
        self.assertEqual(blocks, ['This is **bolded** paragraph',
        """This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line""",
        """* This is a list
* with items"""])

    def test_block_type_heading1(self):
        text = '#Heading1'
        self.assertEqual(block_to_block_type(text), BlockType.block_type_heading1)

    def test_block_type_heading2(self):
        text = '##Heading2'
        self.assertEqual(block_to_block_type(text), BlockType.block_type_heading2)

    def test_block_type_heading3(self):
        text = '###Heading3'
        self.assertEqual(block_to_block_type(text), BlockType.block_type_heading3)

    def test_block_type_heading4(self):
        text = '####Heading4'
        self.assertEqual(block_to_block_type(text), BlockType.block_type_heading4)

    def test_block_type_heading5(self):
        text = '#####Heading5'
        self.assertEqual(block_to_block_type(text), BlockType.block_type_heading5)

    def test_block_type_heading6(self):
        text = '######Heading6'
        self.assertEqual(block_to_block_type(text), BlockType.block_type_heading6)

    def test_block_type_code(self):
        text = '```SELECT * FROM USER```'
        self.assertEqual(block_to_block_type(text), BlockType.block_type_code)

    def test_block_type_code_incorrect(self):
        text = '```SELECT * FROM USER``'
        self.assertEqual(block_to_block_type(text), BlockType.block_type_paragraph)
    
    def test_block_type_quote(self):
        text = '>this is a quote'
        self.assertEqual(block_to_block_type(text), BlockType.block_type_quote)

    def test_block_type_ul(self):
        text = '* one item\n* other item\n- different item'
        self.assertEqual(block_to_block_type(text), BlockType.block_type_ul)

    def test_block_type_ul_incorrect(self):
        text = '* one item\n* other item\n# different item'
        self.assertEqual(block_to_block_type(text), BlockType.block_type_paragraph)

    def test_block_type_ol(self):
        text = '1. first\n2. second\n3. third'
        self.assertEqual(block_to_block_type(text), BlockType.block_type_ol)
    
    def test_block_type_ol_incorrect(self):
        text = '1. first\n3. second\n3. third'
        self.assertEqual(block_to_block_type(text), BlockType.block_type_paragraph)

if __name__ == "__main__":
    unittest.main()


