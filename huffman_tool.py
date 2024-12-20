
import os
from typing import Dict, Tuple


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


def main(file_path: str) -> Tuple[bool, Dict[str, int]]:
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
    
    frequencies = count_character_frequencies(file_path)
    print(f"Character frequencies: {frequencies}")
    return True, frequencies


if __name__ == '__main__':
    input_file = input("Enter the file path: ")
    main(input_file)