import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"prop1":"happy", "prop2":"sad"})
        self.assertEqual(node.props_to_html(), " prop1=\"happy\" prop2=\"sad\"")
    def test_props_to_html_none(self):
        node = HTMLNode(tag="I have no props!")
        self.assertEqual(node.props_to_html(), "")
    def test_props_to_html_empty(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")


if __name__ == "__main__":
    unittest.main()

