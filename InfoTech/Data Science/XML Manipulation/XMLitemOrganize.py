import base64
import xml.etree.ElementTree as ET

def decode_base64_in_xml(file_path, output_path, tags_to_decode, items_to_decode=None):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Function to decode Base64 encoded strings
    def decode_base64(encoded_string):
        try:
            return base64.b64decode(encoded_string).decode('utf-8')
        except Exception as e:
            print(f"Error decoding: {e}")
            return encoded_string

    # Recursively search and decode Base64 content for specified tags within specified items
    def decode_elements(element, item_index=None):
        decoded_data = {}
        for index, child in enumerate(element):
            if child.tag == 'item':
                if items_to_decode is None or index in items_to_decode:
                    item_data = decode_elements(child, index)
                    if item_data:
                        decoded_data[index] = item_data
            elif child.tag in tags_to_decode and child.text:
                if items_to_decode is None or item_index in items_to_decode:
                    decoded_text = decode_base64(child.text.strip())
                    if decoded_text != child.text.strip():
                        print(f"Decoded Base64 in item {item_index}, tag '{child.tag}': {decoded_text}")
                        child.text = decoded_text
                        decoded_data[child.tag] = decoded_text
        return decoded_data

    # Start decoding from the root
    decoded_items = decode_elements(root)

    # Save the modified XML to the output file
    tree.write(output_path, encoding='utf-8', xml_declaration=True)

    print(f"Decoding completed. Modified XML saved as '{output_path}'.")
    return decoded_items

# Get user input for file paths, tags to decode, and items to decode
input_file_path = r'C:\Users\james\OneDrive\Desktop\XMLDECODERTEST.xml'
output_file_path = r'C:\Users\james\PycharmProjects\XMLDecoder\decoded_select.xml'
tags_input = input("Enter the XML tags to decode (comma-separated): ")
tags_to_decode = [tag.strip() for tag in tags_input.split(',')]
items_input = input("Enter the item indices to decode (comma-separated, or press Enter for all items): ")
items_to_decode = [int(item.strip()) for item in items_input.split(',')] if items_input else None

# Run the decoding function
decoded_items = decode_base64_in_xml(input_file_path, output_file_path, tags_to_decode, items_to_decode)

# Print decoded items
for item_index, item_data in decoded_items.items():
    print(f"\nDecoded data for item {item_index}:")
    for tag, value in item_data.items():
        print(f"  {tag}: {value}")