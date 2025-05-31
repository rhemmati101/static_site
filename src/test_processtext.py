import unittest

from leafnode import LeafNode
from textnode import TextNode
from textnode import TextType

from processtext import text_node_to_html_node
from processtext import split_nodes_delimiter
from processtext import extract_markdown_images
from processtext import extract_markdown_links
from processtext import split_nodes_image
from processtext import split_nodes_link
from processtext import text_to_textnodes

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
    def test_split_node_delimiter_multi_delim(self):
        node = TextNode("This has **bold** in **it**", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            [TextNode("This has ", TextType.TEXT),
             TextNode("bold", TextType.BOLD),
             TextNode(" in ", TextType.TEXT),
             TextNode("it", TextType.BOLD),]
        )
    def test_split_node_delimiter_delim_at_start(self):
        node = TextNode("_This_ is a crafting table", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "_", TextType.ITALIC),
            [TextNode("This", TextType.ITALIC),
             TextNode(" is a crafting table", TextType.TEXT)]
        )

    def test_extract_markdown_images_basic(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images(
        "This has no images"
        )
        self.assertListEqual([], matches)
    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
        "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                              ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")],
                              matches)
    def test_extract_markdown_images_link(self):
        matches = extract_markdown_images(
        "This is text with a [link](https://google.com)"
        )
        self.assertListEqual([], matches)
    def test_extract_markdown_links_basic(self):
        matches = extract_markdown_links(
        "This is text with a [link](https://google.com)"
        )
        self.assertListEqual([("link", "https://google.com")], matches)
    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links(
        "This is text with no links"
        )
        self.assertListEqual([], matches)
    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
        "This is text with a [link](https://google.com) and [another](https://youtube.com)"
        )
        self.assertListEqual([("link", "https://google.com"),
                              ("another", "https://youtube.com")],
                              matches)
    def test_extract_markdown_links_image(self):
        matches = extract_markdown_links(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_split_images_ends_in_img(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_images_no_img(self):
        node = TextNode(
            "This is text without an image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is text without an image", TextType.TEXT)],
            new_nodes,
        )
    def test_split_images_non_text_nodes(self):
        nodes = [
            TextNode("This is text without an image",TextType.TEXT,),
            TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",TextType.TEXT),
            TextNode("This isn't a text node", TextType.BOLD)
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual([
            TextNode("This is text without an image", TextType.TEXT),
            TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            TextNode("This isn't a text node", TextType.BOLD)
        ],
            new_nodes,
        )
    def test_split_images_ends_in_text(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and some text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and some text", TextType.TEXT)
            ],
            new_nodes,
        )
    def test_split_images_starts_w_img(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_images_with_link(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://i.imgur.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a [link](https://i.imgur.com)", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_split_images_multi_node(self):
        nodes = [
            TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://i.imgur.com)", TextType.TEXT),
            TextNode("This is text with another ![image](https://google.com???)", TextType.TEXT)
        ]

        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a [link](https://i.imgur.com)", TextType.TEXT),
                TextNode("This is text with another ",TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://google.com???")
            ],
            new_nodes,
        )
    
    def test_split_links_starts_n_ends_w_link(self):
        node = TextNode(
            "[link](https://google.com) and another [second link](https://youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://youtube.com"
                ),
            ],
            new_nodes,
        )
    def test_split_links_starts_n_ends_w_text(self):
        node = TextNode(
            "This has a [link](https://google.com) and another...somewhere",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This has a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://google.com"),
                TextNode(" and another...somewhere", TextType.TEXT)
            ],
            new_nodes,
        )
    def test_split_links_no_links(self):
        node = TextNode("This has no links :c",TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This has no links :c",TextType.TEXT)],
            new_nodes,
        )
    def test_split_links_with_image(self):
        node = TextNode(
            "[link](https://google.com) and an ![image](https://img.pokemondb.net/artwork/large/leafeon.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://google.com"),
                TextNode(" and an ![image](https://img.pokemondb.net/artwork/large/leafeon.jpg)", TextType.TEXT)
            ],
            new_nodes,
        )
    def test_split_links_multinode(self):
        nodes = [
            TextNode("[link](https://google.com) and another [second link](https://youtube.com)",TextType.TEXT,),
            TextNode("This is in bold", TextType.BOLD),
            TextNode("This has another [link](https://pokemondb.net/pokedex/ledian).", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://youtube.com"),
                TextNode("This is in bold", TextType.BOLD),
                TextNode("This has another ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://pokemondb.net/pokedex/ledian"),
                TextNode(".", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_text_to_textnodes_all_types(self):
        text = TextNode("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.TEXT)

        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )
    def test_text_to_textnodes_double_delimiters(self):
        text = TextNode("This is **text** _with_ **two** _double_ delimiters", TextType.TEXT)

        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("with", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("double", TextType.ITALIC),
                TextNode(" delimiters", TextType.TEXT),
            ]
        )

if __name__ == "__main__":
    unittest.main()