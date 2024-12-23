
import argparse
import json
import os
import heapq
from typing import Dict, Optional, Tuple

class HuffmanNode:
    """
    Represents a node in the Huffman Tree.
    """

    def __init__(self, char: Optional[str], freq: int, left: Optional['HuffmanNode'] = None, right: Optional['HuffmanNode'] = None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
    
    def __lt__(self, other: 'HuffmanNode') -> bool:
        """
        Less-than comparison for priority queue ordering.
        """

        return self.freq < other.freq
    
def build_huffman_tree(frequencies: Dict[str, int]) -> HuffmanNode:
    """
    Builds a Huffman Tree using the character frequencies.

    Args:
        frequencies (Dict[str, int]): A dictionary with characters as key and their frequencies as value.

    Returns:
        HuffmanNode: The root of the Huffman Tree.
    """

    # create priority queue of nodes
    priority_queue = [HuffmanNode(char, freq)for char, freq in frequencies.items()]
    heapq.heapify(priority_queue)

    # building the tree
    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue) # lowest frequency node
        right = heapq.heappop(priority_queue) # 2nd lowest freq node

        # combine nodes
        merged = HuffmanNode(None, left.freq + right.freq, left, right)
        heapq.heappush(priority_queue, merged)
    
    return priority_queue[0] # root node

def generate_prefix_code(node: HuffmanNode, prefix: str= "", code_table: Optional[Dict[str, int]] = None) -> Dict[str, int]:
    """
    Generates the prefix-code table from the Huffman Tree.

    Args:
        node (HuffmanNode): The root of the Huffman Tree.
        prefix (str): The prefix for the current node's value.
        code_table (Optional[Dict[str, str]]): A dictionary to store the prefix codes.

    Returns:
        Dict[str, str]: A dictionary mapping characters to their prefix codes.
    """
    if code_table is None:
        code_table = {}

    if node is not None:
        if node.char is not None:
            code_table[node.char] = prefix
        generate_prefix_code(node.left, prefix + "0", code_table)
        generate_prefix_code(node.right, prefix + "1", code_table)

    return code_table


def validate_file(file_path: str) -> bool:
    """
    Validates wether the provided file path is valid and accessible.

    Args:
        file_path (str): Path to the file to validate.

    Returns:
        bool: True if the file exists and is readable. False otherwise.
    """

    return os.path.isfile(file_path) and os.access(file_path, os.R_OK)

def count_character_frequencies(file_path: str) -> Dict[str, int]:
    """
    Reads a file and calculates the frequency of each character in the file.
    
    Args: 
        file_path (str): Path to the file to read.

    Returns:
        Dict[str, int]: A dictionary where keys are characters and values are their frequencies
    """

    frequencies = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            for char in line:
                frequencies[char] = frequencies.get(char, 0) + 1
    return frequencies


def main(input_file: str, output_file: str) -> None:
    """
    Main function to validate the file, count character frequencies,
    build the Huffman Tree, generate the prefix code table,
    and write the compressed output file.

    Args:
        input_fie (str): Path to the input file
        output_file (str): Path to the output file
    """

    if not validate_file(input_file):
        print(f"Error: File {input_file} is not valid or not accessible.")
        return False, {}
    
    try:
        # step 1: count character frequencies
        frequencies = count_character_frequencies(input_file)
        print(f"Character frequencies: {frequencies}")

        # step 2: build the Huffman Tree
        huffman_root = build_huffman_tree(frequencies)

        # step 3: generate the prefix-code table
        prefix_code_table = generate_prefix_code(huffman_root)
        print("\nHuffman Codes:")
        for char, code in prefix_code_table.items():
            print(f"{char}: {code}")

        # step 4: write the header and the compressed data to the output file
        with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
            # header in JSON for simplicity
            header = json.dumps(frequencies)
            outfile.write(header + "\n") # separate header from data with a newline

            # write compressed data
            for line in infile:
                compressed_line = ''.join(prefix_code_table[char] for char in line)
                outfile.write(compressed_line)

        print(f"Compressed file written to {output_file}")

    except Exception as error:
        print(f"An error occured: {error}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Huffman Compression Tool")
    parser.add_argument("input_file", help="Path to the input file")
    parser.add_argument("output_file", help="Path to the output file")
    args = parser.parse_args()
    main(args.input_file, args.output_file)