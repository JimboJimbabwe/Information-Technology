import xml.etree.ElementTree as ET
import base64
import sys


def parse_burp_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for item in root.findall('item'):
        request = item.find('request')
        if request is not None and request.text:
            decoded_request = base64.b64decode(request.text).decode('utf-8', errors='ignore')
            formatted_request = format_request(decoded_request)
            print(formatted_request)
            print("\n" + "-" * 50 + "\n")


def format_request(decoded_request):
    # Split the request into lines, preserving original line breaks
    lines = decoded_request.split('\r\n')

    # Reconstruct the request, ensuring we don't add extra line breaks
    formatted_lines = []
    headers_done = False
    for line in lines:
        if not headers_done:
            formatted_lines.append(line)
            if line.strip() == '':
                headers_done = True
        else:
            # For the body, we append without adding extra newlines
            formatted_lines.append(line.strip())

    # Join the lines using CRLF (Carriage Return + Line Feed)
    return '\r\n'.join(formatted_lines)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <xml_file>")
        sys.exit(1)

    xml_file = sys.argv[1]
    parse_burp_xml(xml_file)