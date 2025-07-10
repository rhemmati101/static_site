import unittest

from processblocktext import markdown_to_blocks, BlockType, block_to_blocktype


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

        def test_block_to_blocktype_simpleheading(self):
            self.assertEqual(
                 block_to_blocktype("# this is a basic heading!"),
                 BlockType.HEADING
            )
        def test_block_to_blocktype_tinyheading(self):
            self.assertEqual(
                 block_to_blocktype("###### this is a heading with 6 #'s"),
                 BlockType.HEADING
            )
        def test_block_to_blocktype_invalidheading(self):
            self.assertEqual(
                 block_to_blocktype("####### this is a heading with 7 #'s"),
                 BlockType.PARAGRAPH
            )
        def test_block_to_blocktype_emptyheading(self):
            self.assertEqual(
                 block_to_blocktype("###  "),
                 BlockType.HEADING
            )
        def test_block_to_blocktype_code(self):
            self.assertEqual(
                block_to_blocktype("```\nthis is some code!\n```"),
                BlockType.CODE
            )
        def test_block_to_blocktype_invalidcode1(self):
            self.assertEqual(
                block_to_blocktype("``\nthis is an invalid code block\n```"),
                BlockType.PARAGRAPH
            )
        def test_block_to_blocktype_invalidcode2(self):
            self.assertEqual(
                block_to_blocktype("```\nthis is an invalid code block\n``"),
                BlockType.PARAGRAPH
            )
        def test_block_to_blocktype_simplequote(self):
            self.assertEqual(
                block_to_blocktype("> I...am Steve."),
                BlockType.QUOTE
            )
        def test_block_to_blocktype_multiquote(self):
            self.assertEqual(
                block_to_blocktype("> I...am Steve.\n> applause, I guess"),
                BlockType.QUOTE
            )
        def test_block_to_blocktype_invalidquote(self):
            self.assertEqual(
                block_to_blocktype("> I...am Steve.\nthis is invalid!"),
                BlockType.PARAGRAPH
            )
        def test_block_to_blocktype_simpleunolist(self):
            self.assertEqual(
                block_to_blocktype("- I am a lonely single-line list :("),
                BlockType.UNOLIST
            )
        def test_block_to_blocktype_multiunolist(self):
            self.assertEqual(
                block_to_blocktype("- I have a friend\n- I'm the friend"),
                BlockType.UNOLIST
            )
        def test_block_to_blocktype_invalidunolist(self):
            self.assertEqual(
                block_to_blocktype("- I am a lonely single-line list :(\nnot even a list sadge"),
                BlockType.PARAGRAPH
            )
        def test_block_to_blocktype_nospaceunolist(self):
            self.assertEqual(
                block_to_blocktype("- I am a lonely single-line list :(\n-not even a list sadge"),
                BlockType.PARAGRAPH
            )
        def test_block_to_blocktype_simpleolist(self):
            self.assertEqual(
                block_to_blocktype("1. I am alone ._."),
                BlockType.OLIST
            )
        def test_block_to_blocktype_multiolist(self):
            self.assertEqual(
                block_to_blocktype("1. I\n2. am\n3. a\n4. list?"),
                BlockType.OLIST
            )
        def test_block_to_blocktype_nospaceolist(self):
            self.assertEqual(
                block_to_blocktype("1. I\n2. am\n3.not a\n4. list"),
                BlockType.PARAGRAPH
            )
        def test_block_to_blocktype_nonascendingolist(self):
            self.assertEqual(
                block_to_blocktype("1. I\n2. am\n5. not a\n4. list"),
                BlockType.PARAGRAPH
            )
        def test_block_to_blocktype_badstartolist(self):
            self.assertEqual(
                block_to_blocktype("2. I\n3. am\n4. not a\n5. list"),
                BlockType.PARAGRAPH
            )
        def test_block_to_blocktype_inconsistentolist(self):
            self.assertEqual(
                block_to_blocktype("1. I\n2. am\nnot a\n3. list"),
                BlockType.PARAGRAPH
            )


if __name__ == "__main__":
    unittest.main()