import unittest

from leafnode import LeafNode
from leafnode import text_node_to_html_node
from textnode import TextNode
from textnode import TextType


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "testing")
        self.assertEqual(node.to_html(), "<h1>testing</h1>")
    def test_leaf_to_html_notag(self):
        node = LeafNode(None, "i have no tag")
        self.assertEqual(node.to_html(), "i have no tag")
    def test_leaf_to_html_novalue(self):
        node = LeafNode("p", None)
        with self.assertRaisesRegex(ValueError, "Leaf node must have a value"):
            node.to_html()
    def test_leaf_to_html_empty(self):
        node = LeafNode(None, None)
        with self.assertRaisesRegex(ValueError, "Leaf node must have a value"):
            node.to_html()

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

