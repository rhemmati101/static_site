import unittest

from leafnode import LeafNode
from textnode import TextNode
from textnode import TextType

from processtext import text_node_to_html_node
from processtext import split_nodes_delimiter

class TestProcessText(unittest.TestCase):
    def test_html_to_leaf_plain(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_html_to_leaf_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
    def test_html_to_leaf_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")
    def test_html_to_leaf_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")
    def test_html_to_leaf_link(self):
        node = TextNode("This is a link node", TextType.LINK, url="google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href":"google.com"})
    def test_html_to_leaf_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, url="google.com blah blah")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src":"google.com blah blah", "alt":"This is an image node"})
    def test_html_to_leaf_other_type(self):
        with self.assertRaises(Exception):
            node = TextNode("This is a weird node", TextType.WEIRD)
            # if the above line doesn't fail, the texttype must be valid
            # html_node = text_node_to_html_node(node)

    def test_split_node_delimiter_bold(self):
        node = TextNode("This has **bold** in it", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            [TextNode("This has ", TextType.TEXT),
             TextNode("bold", TextType.BOLD),
             TextNode(" in it", TextType.TEXT)]
        )
    def test_split_node_delimiter_italic(self):
        node = TextNode("This has _italic_ in it", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "_", TextType.ITALIC),
            [TextNode("This has ", TextType.TEXT),
             TextNode("italic", TextType.ITALIC),
             TextNode(" in it", TextType.TEXT)]
        )
    def test_split_node_delimiter_code(self):
        node = TextNode("This has `code` in it", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            [TextNode("This has ", TextType.TEXT),
             TextNode("code", TextType.CODE),
             TextNode(" in it", TextType.TEXT)]
        )
    def test_split_node_delimiter_plain(self):
        node = TextNode("This has nothing special in it", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [node])  
        self.assertEqual(split_nodes_delimiter([node], "_", TextType.ITALIC), [node])
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), [node])
    def test_split_node_delimiter_invalid_markdown(self):
        node = TextNode("This is **not valid markdown code", TextType.TEXT)
        with self.assertRaisesRegex(Exception, "missing matching delimiter"):
            split_nodes_delimiter([node], "**", TextType.BOLD)
    def test_split_node_delimiter_list(self):
        nested_node = TextNode("This has **bold** in it", TextType.TEXT)
        bold_node = TextNode("This node is in bold", TextType.BOLD)
        italic_node = TextNode("This node is **in** italic", TextType.ITALIC)
        self.assertEqual(
            split_nodes_delimiter([nested_node, bold_node], "**", TextType.BOLD),
            [TextNode("This has ", TextType.TEXT),
             TextNode("bold", TextType.BOLD),
             TextNode(" in it", TextType.TEXT),
             TextNode("This node is in bold", TextType.BOLD)
             ]
        )
        self.assertEqual(
            split_nodes_delimiter([nested_node, italic_node], "**", TextType.BOLD),
            [TextNode("This has ", TextType.TEXT),
             TextNode("bold", TextType.BOLD),
             TextNode(" in it", TextType.TEXT),
             TextNode("This node is **in** italic", TextType.ITALIC)]
        )

if __name__ == "__main__":
    unittest.main()