
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


def pack_bits(bit_string: str) -> bytes:
    """
    Packs a bit string into bytes.

    Args:
        bit_string (str): a string of '0's and '1's representing bits.

    Returns:
        bytes: The packed binary data. 
    """

    # pad the bit string to make its length a multiple of 8
    padded_bit_string = bit_string + '0' *((8 - len(bit_string) % 8) % 8)

    # convert the padded bit string into a byte array
    byte_array = bytearray()
    for i in range(0, len(padded_bit_string), 8):
        byte_array.append(int(padded_bit_string[i: i + 8], 2))

    
    return bytes(byte_array)


def read_header_and_rebuild_tree(encoded_file: str) -> Tuple[HuffmanNode, Dict[str, int]]:
    """
    Reads the header from the encoded file, rebuilds the Huffman Tree,
    and regenerates the prefix-code table.

    Args:
        encoded_file (str): Path to the encoded file.

    Returns:
        Tuple[HuffmanNode, Dict[str, int]]: The root of the Huffman Tree and the prefix-code table.
    """

    with open(encoded_file, 'rb') as file:
        # read header
        header_line = file.readline().strip()
        frequencies = json.loads(header_line.decode('utf-8'))

        # rebuild Huffman Tree
        huffman_root = build_huffman_tree(frequencies)

        # regenerate prefix-code table.
        prefix_code_table = generate_prefix_code(huffman_root)
    
    return huffman_root, prefix_code_table


def decode_compressed_file(encoded_file: str, output_file: str) -> None:
    """
    Decodes a compressed file using the Huffman tree and writes the decompressed text to an output file.

    Args:
        encoded_file (str): Path to the encoded file.
        output_file (str): Path to the output file for the decompressed text.
    """
    with open(encoded_file, 'rb') as infile:
        # Step 1: Read and parse the header
        header_line = infile.readline().strip()
        header = json.loads(header_line.decode('utf-8'))
        frequencies = header["frequencies"]
        bit_string_length = header["bit_string_length"]

        # Step 2: Rebuild Huffman Tree
        huffman_root = build_huffman_tree(frequencies)

        # Step 3: Read the compressed data
        compressed_data = infile.read()

        # Step 4: Convert binary data to bit string
        bit_string = ''.join(f'{byte:08b}' for byte in compressed_data)

        # Step 5: Truncate bit string to the original length
        bit_string = bit_string[:bit_string_length]

        # Step 6: Decode the bit string using the Huffman Tree
        decoded_text = []
        current_node = huffman_root
        for bit in bit_string:
            if bit == '0':
                current_node = current_node.left
            else:
                current_node = current_node.right

            # If we reach a leaf node, append the character to the output
            if current_node.char is not None:
                decoded_text.append(current_node.char)
                current_node = huffman_root  # Reset to root for the next character

        # Step 7: Write the decoded text to the output file
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write(''.join(decoded_text))

    print(f"Decompressed file written to {output_file}")




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
        # Remove BOM from the frequency table if present
        if '\ufeff' in frequencies:
            del frequencies['\ufeff']
        print(f"Character frequencies: {frequencies}")

        # step 2: build the Huffman Tree
        huffman_root = build_huffman_tree(frequencies)

        # step 3: generate the prefix-code table
        prefix_code_table = generate_prefix_code(huffman_root)
        print("\nHuffman Codes:")
        for char, code in prefix_code_table.items():
            print(f"{char}: {code}")

        # step 4: write the header and the compressed data to the output file
        with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'wb') as outfile:
            # Compress and write binary data
            bit_string = ""
            for line in infile:
                line = line.lstrip('\ufeff')  # Strip BOM if present
                for char in line:
                    if char in prefix_code_table:
                        bit_string += prefix_code_table[char]
                    else:
                        raise ValueError(f"Character '{char}' not in prefix code table.")
            # Write header: include frequencies and original bit string length
            header = {
                "frequencies": frequencies,
                "bit_string_length": len(bit_string)
            }
            outfile.write(json.dumps(header).encode('utf-8') + b'\n')
            
            compressed_data = pack_bits(bit_string)
            outfile.write(compressed_data)

        print(f"Compressed file written to {output_file}")

    except Exception as error:
        print(f"An error occured: {error}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Huffman Compression Tool")
    parser.add_argument("input_file", help="Path to the input file")
    parser.add_argument("output_file", help="Path to the output file")
    parser.add_argument(
        "--mode",
        choices=["compress", "decompress"],
        required=True,
        help="Mode of operation: compress or decompress"
    )
    args = parser.parse_args()

    if args.mode == "compress":
        main(args.input_file, args.output_file)
    elif args.mode == "decompress":
        decode_compressed_file(args.input_file, args.output_file)