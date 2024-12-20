import os
import unittest
from huffman_tool import count_character_frequencies, validate_file

class TestHuffmanTool(unittest.TestCase):
    def setUp(self):
        """
        Set up a temporary for testing. 
        """

        self.test_file = 'test.txt'
        with open(self.test_file, 'w', encoding='utf-8') as file:
            file.write("aaabbc\nXXtt")
    
    def tearDown(self):
        """
        Clean up the temporary file after testing
        """

        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_validate_file(self):
        """
        Test the file validation function
        """

        self.assertTrue(validate_file(self.test_file))
        self.assertFalse(validate_file('nonexistent.txt'))

    def test_count_character_frequencies(self):
        """
        Test character frequency calculation
        """

        expected_frequencies = {
            'a': 3,
            'b': 2,
            'c': 1,
            '\n': 1,
            'X': 2,
            't': 2
        }

        self.assertEqual(count_character_frequencies(self.test_file), expected_frequencies)