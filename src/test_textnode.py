import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_empty_url(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(node.url, None)
        
    def test_non_empty_url(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        self.assertEqual(node.url, "https://www.boot.dev")



if __name__ == "__main__":
    unittest.main()

