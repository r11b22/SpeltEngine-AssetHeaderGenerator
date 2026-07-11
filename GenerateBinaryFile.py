import os
import re
import sys

def header_to_binary(input_header_path, output_binary_path=None):
    # Read the header file content
    try:
        with open(input_header_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{input_header_path}' could not be found.")
        return False

    # Extract everything inside the curly braces { ... }
    # This matches the array body even if it spans multiple lines
    array_match = re.search(r"=\s*\{([^}]+)\};", content)
    if not array_match:
        print("Error: Could not find a valid C/C++ array format in the header file.")
        return False

    array_body = array_match.group(1)

    # Find all hex tokens (e.g., 0x89, 0x50, 0x0a)
    hex_tokens = re.findall(r"0x[0-9a-fA-F]{2}", array_body)
    if not hex_tokens:
        print("Error: No hex byte tokens (0xXX) found inside the array.")
        return False

    # Convert the text hex tokens into actual bytes
    binary_data = bytearray(int(token, 16) for token in hex_tokens)

    # Determine the output binary path if not provided
    if not output_binary_path:
        # Fallback: remove the .h extension and add a .bin extension
        output_binary_path = os.path.splitext(input_header_path)[0] + ".bin"

    # Write the raw bytes back to disk
    with open(output_binary_path, "wb") as f:
        f.write(binary_data)

    print(f"Successfully restored: {output_binary_path} ({len(binary_data)} bytes)")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python GenerateBinaryFile.py <input_header_file> [output_binary_file]")
        sys.exit(1)

    in_file = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) > 2 else None
    header_to_binary(in_file, out_file)
