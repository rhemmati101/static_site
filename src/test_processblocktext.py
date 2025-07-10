import unittest

from processblocktext import markdown_to_blocks


class TestProcessBlockText(unittest.TestCase):
        def test_my_sanity(self):
             self.assertEqual("test", "\ntest\n".strip())
        def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )
        def test_markdown_to_blocks_oneblock(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            md = """
This is **bolded** paragraph with a lot after it



"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                ["This is **bolded** paragraph with a lot after it",],
            )
        def test_markdown_to_blocks_empty(self):
            md = """


"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [],
            )
        def test_markdown_to_blocks_extraspace(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line





- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )


if __name__ == "__main__":
    unittest.main()