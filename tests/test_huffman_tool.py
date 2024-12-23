import json
import os
import unittest
from huffman_tool import count_character_frequencies, validate_file, build_huffman_tree, HuffmanNode, generate_prefix_code, read_header_and_rebuild_tree

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

    def test_huffman_tree_example(self):
        """
        Test the Huffman Tree with a sample frequenc table.
        """

        frequencies = {'a': 45, 'b': 13, 'c': 12, 'd': 16, 'e': 9, 'f': 5}
        root = build_huffman_tree(frequencies)
        
        # validate the huffman codes for each character
        codes = {}
        def traverse(node, code):
            if node.char is not None: #leaf node
                codes[node.char] = code
            if node.left:
                traverse(node.left, code + "0")
            if node.right:
                traverse(node.right, code + "1")

        traverse(root, "")
        expected_codes = {
        'a': '0',
        'c': '100',
        'b': '101',
        'f': '1100',
        'e': '1101',
        'd': '111'
        }
        self.assertEqual(expected_codes, codes)         

    def test_single_character(self):
        """
        Test the Huffman Tree with a single character.
        """

        frequencies = {'a': 1}
        root = build_huffman_tree(frequencies)

        self.assertEqual(root.char, 'a')
        self.assertEqual(root.freq, 1)
        self.assertIsNone(root.left)
        self.assertIsNone(root.right)


    def test_empty_frequencies(self):
        """
        Test the Huffman Tree with an empty freq table.
        """

        frequencies = {}
        with self.assertRaises(IndexError):
            build_huffman_tree(frequencies)

    
    def test_write_header(self):
        """
        Test if the header (character frequencies) is correctly written to the output file.
        """

        output_file = 'output.huff'
        expected_header = {
            'a': 3,
            'b': 2,
            'c': 1,
            '\n': 1,
            'X': 2,
            't': 2
        }

        # Generate Huffman tree and prefix codes
        frequencies = count_character_frequencies(self.test_file)
        huffman_root = build_huffman_tree(frequencies)
        prefix_code_table = generate_prefix_code(huffman_root)

        # Write to output file
        with open(self.test_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
            header = json.dumps(frequencies)
            outfile.write(header + "\n")  # Write header
            for line in infile:
                compressed_line = ''.join(prefix_code_table[char] for char in line)
                outfile.write(compressed_line)

        # Verify header in output file
        with open(output_file, 'r', encoding='utf-8') as file:
            written_header = file.readline().strip()
            self.assertEqual(json.loads(written_header), expected_header)

        # Cleanup
        if os.path.exists(output_file):
            os.remove(output_file)

        
    def test_header_and_compressed_data_separation(self):
        """
        Test if the header and compressed data are correctly separated in the output file.
        """
        output_file = 'output.huff'

        # Generate Huffman tree and prefix codes
        frequencies = count_character_frequencies(self.test_file)
        huffman_root = build_huffman_tree(frequencies)
        prefix_code_table = generate_prefix_code(huffman_root)

        # Write to output file
        with open(self.test_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
            header = json.dumps(frequencies)
            outfile.write(header + "\n")  # Write header
            for line in infile:
                compressed_line = ''.join(prefix_code_table[char] for char in line)
                outfile.write(compressed_line)

        # Verify separation
        with open(output_file, 'r', encoding='utf-8') as file:
            header = file.readline().strip()  # Read header
            compressed_data = file.read().strip()  # Read compressed data

        self.assertTrue(header)  # Header should not be empty
        self.assertTrue(compressed_data)  # Compressed data should not be empty
        self.assertNotEqual(header, compressed_data)  # Header and data should differ

        # Cleanup
        if os.path.exists(output_file):
            os.remove(output_file)

    
    def test_rebuild_tree_from_header(self):
        encoded_file = 'compressed.huff'

        # Rebuild tree and regenerate prefix-code table
        huffman_root, prefix_code_table = read_header_and_rebuild_tree(encoded_file)

        # Print the prefix-code table for verification
        print("Regenerated Prefix-Code Table:")
        for char, code in prefix_code_table.items():
            print(f"{char}: {code}")