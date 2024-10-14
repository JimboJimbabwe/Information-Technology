import xml.etree.ElementTree as ET
import base64
import sys
import json
import shlex


def parse_burp_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for item in root.findall('item'):
        request = item.find('request')
        if request is not None and request.text:
            decoded_request = base64.b64decode(request.text).decode('utf-8', errors='ignore')
            print_request_details(decoded_request)
            print(format_as_burp_curl(decoded_request))
            print("\n" + "-" * 50 + "\n")


def print_request_details(decoded_request):
    lines = decoded_request.split('\n')
    if lines:
        first_line = lines[0].strip().split()
        if len(first_line) >= 3:
            method, path, http_version = first_line
            print(f"Method: {method}")
            print(f"Path: {path}")
            print(f"HTTP Version: {http_version}")

        print("Headers:")
        headers = []
        body_start = 0
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == '':
                body_start = i + 1
                break
            headers.append(line.strip())
            print(f"  {line.strip()}")

        if body_start < len(lines):
            body = '\n'.join(lines[body_start:])
            print("Body:")
            print(body)


def format_as_burp_curl(decoded_request):
    lines = decoded_request.split('\n')
    first_line = lines[0].strip().split()
    method = first_line[0] if len(first_line) > 0 else 'GET'
    path = first_line[1] if len(first_line) > 1 else '/'

    headers = []
    cookies = []
    body = ''
    reading_headers = True
    host = ''

    for line in lines[1:]:
        if reading_headers:
            if line.strip() == '':
                reading_headers = False
                continue
            if line.lower().startswith('cookie:'):
                cookies = line.split(':', 1)[1].strip()
            elif line.lower().startswith('host:'):
                host = line.split(':', 1)[1].strip()
            else:
                headers.append(line.strip())
        else:
            body += line + '\n'

    curl_command = ["curl", "--path-as-is", "-i", "-s", "-k"]
    curl_command.extend(["-X", f"$'{method}'"])

    for header in headers:
        curl_command.extend(["-H", f"$'{header}'"])

    if cookies:
        curl_command.extend(["-b", f"$'{cookies}'"])

    if body.strip():
        curl_command.extend(["-d", f"$'{body.strip()}'"])

    # Construct the full URL
    full_url = f"https://{host}{path}"
    curl_command.append(f"$'{full_url}'")

    return "curl " + " \\\n    ".join(curl_command[1:])


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <xml_file>")
        sys.exit(1)

    xml_file = sys.argv[1]
    parse_burp_xml(xml_file)