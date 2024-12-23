# Huffman Compression Tool

## Overview

The Huffman Compression Tool is a Python-based command-line utility for compressing and decompressing text files using Huffman coding. This project implements the complete Huffman encoding and decoding workflow, including:

- Counting character frequencies
- Building the Huffman Tree
- Generating prefix-code tables
- Compressing the text into a binary format
- Decompressing the binary format back into the original text

This project was developed as part of the **[Coding Challenges Weekly](https://codingchallenges.fyi/challenges/challenge-huffman/)** series.

---

## Features

- **Lossless Compression**: Compresses text files while ensuring no data loss.
- **Huffman Coding**: Uses Huffman coding to generate optimal prefix codes for characters based on their frequencies.
- **Command-Line Interface**: Provides an easy-to-use CLI for compressing and decompressing files.
- **Custom Binary Encoding**: Packs prefix-code output into actual binary bytes for efficient storage.

---

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/ZiadRamzy/huffman-compression-tool.git
   cd huffman-compression-tool
   ```

2. **Make the Script Executable**:
   ```bash
   chmod +x huffman_tool.py
   ```

---

## Usage

The Huffman Compression Tool supports two modes: **compress** and **decompress**.

### Compression

To compress a text file:

```bash
python huffman_tool.py <input_file> <compressed_file> --mode compress
```

Example:

```bash
python huffman_tool.py test.txt compressed.huff --mode compress
```

### Decompression

To decompress a file:

```bash
python huffman_tool.py <compressed_file> <output_file> --mode decompress
```

Example:

```bash
python huffman_tool.py compressed.huff decompressed.txt --mode decompress
```

---

## Project Structure

- **huffman_tool.py**: Main script containing the implementation of the Huffman encoding and decoding algorithms.
- **tests/**: Directory containing unit tests for the tool.
- **README.md**: Documentation for the project.

---

## Example Workflow

### Input File (`test.txt`)

```
aaabbc
```

### Compress the File

```bash
python huffman_tool.py test.txt compressed.huff --mode compress
```

### Compressed Output (`compressed.huff`)

- Header (JSON):
  ```json
  { "frequencies": { "a": 3, "b": 2, "c": 1 }, "bit_string_length": 6 }
  ```
- Binary Data:
  A packed binary representation of the Huffman-encoded text.

### Decompress the File

```bash
python huffman_tool.py compressed.huff decompressed.txt --mode decompress
```

### Decompressed Output (`decompressed.txt`)

```
aaabbc
```

---

## Design Details

### Huffman Coding

Huffman coding is a lossless data compression algorithm that assigns variable-length prefix codes to characters based on their frequencies. Characters that occur more frequently are assigned shorter codes, optimizing compression.

### Workflow Steps

1. **Compression**:

   - Count character frequencies.
   - Build a Huffman Tree.
   - Generate a prefix-code table.
   - Encode text using the prefix-code table.
   - Write the header (frequencies and bit string length) and compressed binary data to the output file.

2. **Decompression**:
   - Read and parse the header to reconstruct the Huffman Tree.
   - Decode the binary data back into text using the reconstructed tree.

---

## Limitations

- Designed for text files; binary file support is not implemented.
- Works best with larger files that contain repeated patterns.

---

## References

This project is inspired by the **[Coding Challenges Weekly](https://codingchallenges.fyi/challenges/challenge-huffman/)** series. Special thanks to their excellent challenges for inspiring this implementation.
