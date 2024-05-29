import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag='a', value='link', props={'href':'https://www.boot.dev'})
        self.assertEqual(node.props_to_html(),'href="https://www.boot.dev"')

    def test_repr(self):
        node = HTMLNode(tag='a', value='link', props={'href':'https://www.boot.dev'})
        self.assertEqual(node.__repr__(), '<a href="https://www.boot.dev">link</a>')


class TestLeafNode(unittest.TestCase):
    def test_to_html_no_props(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html() , '<p>This is a paragraph of text.</p>')

    def test_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

class TestParentNode(unittest.TestCase):
    def test_to_html_no_props(self):
        node = ParentNode(tag="p", children=[
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ])
        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

if __name__ == '__main__':
    unittest.main()
