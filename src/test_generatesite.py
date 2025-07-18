import unittest

from generatesite import extract_title


class TestGenerateSite(unittest.TestCase):
    def test_extract_title_basic(self):
        self.assertEqual(extract_title("# Hello"), "Hello")
    def test_extract_title_extraspace(self):
        self.assertEqual(extract_title("#      Hello    "), "Hello")
    def test_extract_title_multiline(self):
        self.assertEqual(extract_title("## not a title\n### still not a title!\n# Hello"), "Hello")
    def test_extract_title_notitle(self):
        with self.assertRaisesRegex(Exception, "no title found"):
            extract_title("## not a title\n### still not a title!")
    def test_extract_title_invalidheader(self):
        with self.assertRaisesRegex(Exception, "no title found"):
            extract_title("#invalid title")


if __name__ == "__main__":
    unittest.main()