import unittest

from processmarkdown import markdown_to_html_node

class TestProcessMarkdown(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quoteblock(self): #Note: assuming whitespace in between > and text is ignored
        md = """
> This is a quote.
> The quote is continued!
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote.\nThe quote is continued!</blockquote></div>",
        )

    def test_unolistblock(self): #Note: assuming extra whitespace in between - and text is ignored
        md = """
- one
- two
-       three, [tada!](https://www.google.com)
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>one</li><li>two</li><li>three, <a href='https://www.google.com'>tada!</a></li></ul></div>",
        )
    def test_olistblock(self): #Note: assuming extra whitespace in between n. and text is ignored
        md = """
1. one
2.   _two_
3. three
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>one</li><li><i>two</i></li><li>three</li></ol></div>",
        )

    def test_headings(self):    #Note: assuming headings are 1 line
        md = """
# I am big.

##   i'm less big :(

#### i'm small!

###### hahahahahahaaahhahaa ![kitty](https://i.redd.it/bgsi46c1390a1.jpg)
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>I am big.</h1><h2>i'm less big :(</h2><h4>i'm small!</h4><h6>hahahahahahaaahhahaa <img src='https://i.redd.it/bgsi46c1390a1.jpg' alt='kitty' /></h6></div>",
        )



if __name__ == "__main__":
    unittest.main()