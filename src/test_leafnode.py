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



if __name__ == "__main__":
    unittest.main()

