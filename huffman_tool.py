
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

def print_huffman_tree(node: HuffmanNode, prefix: str= "") -> None:
    """
    Prints the huffma tree in a human readable form.

    Args:
        node (HuffmanNode): The root of the Huffman Tree.
        prefix (str): The prefix for the current node's value.
    """

    if node is not None:
        if node.char is not None:
            print(f"{node.char}: {prefix}")
        print_huffman_tree(node.left, prefix + "0")
        print_huffman_tree(node.right, prefix + "1")


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


def main(file_path: str) -> None:
    """
    Main function to validate the file and count character frequencies if valid.

    Args:
        file_path (str): Path to file to process

    Returns:
        Tuple[bool, Dict[str, int]]: A tuple where the first element indicates file validity and the second is the frequency table.
    """

    if not validate_file(file_path):
        print(f"Error: File {file_path} is not valid or not accessible.")
        return False, {}
    
    try:
        # step 1: count character frequencies
        frequencies = count_character_frequencies(file_path)
        print(f"Character frequencies: {frequencies}")

        # step 2: build the Huffman Tree
        huffman_root = build_huffman_tree(frequencies)

        # step 3: pritn Huffman codes
        print("\nHuffman Codes:")
        print_huffman_tree(huffman_root)

    except Exception as error:
        print(f"An error occured: {error}")

if __name__ == '__main__':
    input_file = input("Enter the file path: ")
    main(input_file)