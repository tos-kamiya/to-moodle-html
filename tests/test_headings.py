import unittest

from bs4 import BeautifulSoup

from to_moodle_html.to_moodle_html import convert_headings_to_paragraphs


class HeadingConversionTests(unittest.TestCase):
    def test_heading_converted_to_bold_paragraph(self):
        soup = BeautifulSoup("<div><h2>Title <em>em</em></h2></div>", "html.parser")
        convert_headings_to_paragraphs(soup)
        self.assertEqual(
            str(soup.div),
            "<div><p><strong>Title <em>em</em></strong></p></div>",
        )

    def test_document_without_headings_is_unchanged(self):
        markup = "<div><p>No headings here.</p></div>"
        soup = BeautifulSoup(markup, "html.parser")
        convert_headings_to_paragraphs(soup)
        self.assertEqual(str(soup.div), markup)


if __name__ == "__main__":
    unittest.main()
