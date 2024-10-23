import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_not_eq(self):
        node = TextNode("t", TextType.NORMAL)
        node2 = TextNode("t", TextType.NORMAL, "url")
        self.assertNotEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode("p", TextType.NORMAL, "url")
        node2 = TextNode("t", TextType.NORMAL, "url")
        self.assertNotEqual(node, node2)

    def test_type_not_eq(self):
        node = TextNode("t", TextType.NORMAL, "url")
        node2 = TextNode("t", TextType.ITALIC, "url")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("Nice", TextType.IMAGE, "url-ly")
        self.assertEqual(repr(node), "TextNode(Nice, image, url-ly)")

if __name__ == "__main__":
    unittest.main()
