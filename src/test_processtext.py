import unittest

from leafnode import LeafNode
from textnode import TextNode
from textnode import TextType

from processtext import text_node_to_html_node

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

if __name__ == "__main__":
    unittest.main()