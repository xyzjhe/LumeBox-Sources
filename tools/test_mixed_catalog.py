import unittest
from build_catalog import content_types

class MixedDeclarationTest(unittest.TestCase):
    def test_valid_declaration(self):
        self.assertEqual(content_types({'id':'example', 'contentTypes':['video','novel']}), ['video','novel'])

    def test_invalid_declarations_are_rejected(self):
        for value in [None, 'video', [], ['video'], ['video','video'], ['video','invalid'], ['video',7]]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                content_types({'id':'example', 'contentTypes':value})

if __name__ == '__main__':
    unittest.main()
