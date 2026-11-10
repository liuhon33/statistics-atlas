"""Pure transformation regression tests; no writes to the vault."""
import unittest
from fold_note_provenance import transform, MARKER


class ProvenanceFolding(unittest.TestCase):
    def test_preserves_frontmatter_heading_and_next_section(self):
        text = '---\nid: x\n---\n# Title\nMain\n\n## Origin\n\nText\n\nMore\n\n## Connections\n- link\n'
        after, sections = transform(text)
        self.assertEqual(sections, ['origin'])
        self.assertEqual(after, text.replace('Text\n\nMore', MARKER + '\n> Text\n>\n> More'))
        self.assertEqual(transform(after), (after, []))

    def test_fences_are_not_sections(self):
        text = '```markdown\n## Origin\nExample\n```\n'
        self.assertEqual(transform(text), (text, []))

    def test_crlf_and_nested_content(self):
        text = '## Origin\r\n\r\nA\r\n### Detail\r\n> quote\r\n\r\n## End\r\n'
        after, _ = transform(text)
        self.assertIn('> ### Detail\r\n> > quote\r\n', after)
        self.assertEqual(after.count('\r\n'), text.count('\r\n') + 1)
        self.assertTrue(after.endswith('## End\r\n'))

    def test_no_empty_or_topic_callout(self):
        for text in ['# Data provenance and consent\nTopic text\n', '## Origin\n\n## Next\nBody\n']:
            self.assertEqual(transform(text), (text, []))

    def test_multiple_sections(self):
        text = '## Source coverage\n\nA\n\n## Preserved original bytes\n\nB\n'
        after, sections = transform(text)
        self.assertEqual(len(sections), 2)
        self.assertEqual(after.count(MARKER), 2)
        self.assertEqual(transform(after), (after, []))


if __name__ == '__main__':
    unittest.main()
