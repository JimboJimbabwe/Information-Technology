import base64
import xml.etree.ElementTree as ET

def decode_base64_in_xml(file_path, output_path):
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

    # Recursively search and decode Base64 content
    def decode_elements(element):
        for child in element:
            if child.text:
                decoded_text = decode_base64(child.text.strip())
                if decoded_text != child.text.strip():
                    print(f"Decoded Base64 in tag '{child.tag}': {decoded_text}")
                child.text = decoded_text
            decode_elements(child)

    # Start decoding from the root
    decode_elements(root)

    # Save the modified XML to the output file
    tree.write(output_path, encoding='utf-8', xml_declaration=True)

    print(f"Decoding completed. Modified XML saved as '{output_path}'.")

# Usage example
input_file_path = r'C:\Users\james\OneDrive\Desktop\XMLDECODERTEST.xml'
output_file_path = 'decoded_example.xml'
decode_base64_in_xml(input_file_path, output_file_path)