import unittest

from textnode import TextNode, TextNodeType

from inline_markdown import split_nodes_delimiter, extract_markdown_images, \
    extract_markdown_links, split_nodes_link, split_nodes_image, text_to_text_nodes

class TestInlineMarkdownToTextConversion(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextNodeType.text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", TextNodeType.text_type_code)
        
        self.assertEqual([
            TextNode("This is text with a ", TextNodeType.text_type_text),
            TextNode("code block", TextNodeType.text_type_code),
            TextNode(" word", TextNodeType.text_type_text),
            ], new_nodes)


    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")])

    def test_extract_markdown_images_no_match(self):
        text = "This is a text with no images inside"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("link", "https://www.example.com"), ("another", "https://www.example.com/another")])
        
    def test_extract_markdown_links_no_match(self):
        text = "this is a text with no links inside"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            TextNodeType.text_type_text,
        )
        new_nodes = split_nodes_image([node])

        self.assertEqual(new_nodes,[
            TextNode("This is text with an ", TextNodeType.text_type_text),
            TextNode("image", TextNodeType.text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", TextNodeType.text_type_text),
            TextNode(
                "second image", TextNodeType.text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
            ),
        ] )

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            TextNodeType.text_type_text,
        )
        new_nodes = split_nodes_link([node])

        self.assertEqual(new_nodes,[
            TextNode("This is text with a ", TextNodeType.text_type_text),
            TextNode("link", TextNodeType.text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", TextNodeType.text_type_text),
            TextNode(
                "second link", TextNodeType.text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
            ),
        ] )

    def test_text_to_text_nodes(self):
        text = 'This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)'
        nodes = text_to_text_nodes(text)
        self.assertEqual(nodes, [
            TextNode("This is ", TextNodeType.text_type_text),
            TextNode("text", TextNodeType.text_type_bold),
            TextNode(" with an ", TextNodeType.text_type_text),
            TextNode("italic", TextNodeType.text_type_italic),
            TextNode(" word and a ", TextNodeType.text_type_text),
            TextNode("code block", TextNodeType.text_type_code),
            TextNode(" and an ", TextNodeType.text_type_text),
            TextNode("image", TextNodeType.text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", TextNodeType.text_type_text),
            TextNode("link", TextNodeType.text_type_link, "https://boot.dev")
        ])


if __name__ == "__main__":
    unittest.main()

