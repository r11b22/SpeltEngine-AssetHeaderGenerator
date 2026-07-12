import os
import sys

def binary_to_header(input_path, output_path=None):
    # Determine the output filename if not provided
    if not output_path:
        output_path = os.path.splitext(input_path)[0] + ".h"

    # Generate a clean, safe variable name based on the filename
    base_name = os.path.basename(input_path)
    var_name = "".join(c if c.isalnum() else "_" for c in base_name)

    # Read the binary data
    try:
        with open(input_path, "rb") as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{input_path}' could not be found.")
        return False

    file_size = len(data)
    VERSION_STR = "0.1.0"

    # Write the C++ header file
    with open(output_path, "w", encoding="utf-8") as f:
        # Include guards
        f.write("#pragma once\n\n")

        # Generator information and version tracking
        f.write(f"// Generator Version: {VERSION_STR}\n")
        f.write("// This file was generated using SpeltEngine-AssetHeaderGenerator.\n")
        f.write("// Manually editing this file is not recommended and could lead to unexpected behaviour.\n")
        f.write("\n")

        # Definition of the Asset struct with macro guard to prevent redefinition errors
        f.write("#ifndef EMBEDDED_ASSET_STRUCT\n")
        f.write("#define EMBEDDED_ASSET_STRUCT\n")
        f.write("namespace Spelt {\n")
        f.write("   struct EmbeddedAsset {\n")
        f.write("       const char* version;\n")
        f.write("       const unsigned char* data;\n")
        f.write("       const unsigned int size;\n")
        f.write("   };\n")
        f.write("}\n")
        f.write("#endif // EMBEDDED_ASSET_STRUCT\n\n")

        # Internal raw array definition (marked inline to avoid multiple definitions)
        f.write(f"// Automatically generated raw data from {base_name}\n")
        f.write(f"inline const unsigned char {var_name}_raw_data[] = {{\n")

        # Format bytes into neat rows of 12 hex values
        row_bytes = []
        for i, byte in enumerate(data):
            row_bytes.append(f"0x{byte:02x}")
            if (i + 1) % 12 == 0:
                f.write("    " + ", ".join(row_bytes) + ",\n")
                row_bytes = []

        # Write any remaining bytes left over
        if row_bytes:
            f.write("    " + ", ".join(row_bytes) + "\n")
        else:
            # Clean up trailing comma if rows matched perfectly
            f.seek(f.tell() - 2)
            f.write("\n")

        f.write("};\n\n")

        # Struct instance instantiation
        f.write(f"// Package containing the version, data pointer, and size\n")
        f.write(f"inline const EmbeddedAsset {var_name} = {{\n")
        f.write(f'    "{VERSION_STR}",\n')
        f.write(f"    {var_name}_raw_data,\n")
        f.write(f"    {file_size}\n")
        f.write("};\n")

    print(f"Successfully generated: {output_path} ({file_size} bytes)")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python GenerateAssetHeader.py <input_binary_file> [output_header_file]")
        sys.exit(1)

    in_file = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) > 2 else None
    binary_to_header(in_file, out_file)
