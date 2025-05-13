import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_parent_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaisesRegex(ValueError, "Parent node requires a tag"):
            parent_node.to_html()

    def test_to_html_parent_undef_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", None)
        with self.assertRaisesRegex(ValueError, "Parent node requires a list of children"):
            parent_node.to_html()

    def test_to_html_parent_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_no_variables(self):
        parent_node = ParentNode(None, None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_child_no_tag(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode(None, [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        with self.assertRaisesRegex(ValueError, "Parent node requires a tag"):
            parent_node.to_html()

    def test_to_html_child_undef_children(self):
        child_node = ParentNode("div", None)
        parent_node = ParentNode("div", [child_node])
        with self.assertRaisesRegex(ValueError, "Parent node requires a list of children"):
            parent_node.to_html()

    def test_to_html_child_no_children(self):
        child_node = ParentNode("span", [])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span></span></div>")

    def test_to_html_branching_children(self):
        left_grandchild_node =  LeafNode("span", "left grandchild")
        left_child_node = ParentNode("div", [left_grandchild_node])
        
        right_child_node = LeafNode("span", "right child")
        
        parent_node = ParentNode("div", [left_child_node, right_child_node])

        self.assertEqual(
            parent_node.to_html(),
            "<div><div><span>left grandchild</span></div><span>right child</span></div>"
        )


if __name__ == "__main__":
    unittest.main()