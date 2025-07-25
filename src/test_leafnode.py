import unittest

from leafnode import LeafNode
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



if __name__ == "__main__":
    unittest.main()

