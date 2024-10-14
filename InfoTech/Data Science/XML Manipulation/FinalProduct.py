import base64
import xml.etree.ElementTree as ET
import os
import re


def decode_base64(encoded_string):
    try:
        return base64.b64decode(encoded_string).decode('utf-8')
    except Exception as e:
        print(f"Error decoding: {e}")
        return encoded_string


def analyze_xml_file(file_path, wordlist):
    tree = ET.parse(file_path)
    root = tree.getroot()

    results = []

    for item_index, item in enumerate(root.findall('item')):
        request = item.find('request')
        response = item.find('response')

        decoded_request = decode_base64(request.text) if request is not None and request.text else ""
        decoded_response = decode_base64(response.text) if response is not None and response.text else ""

        for word in wordlist:
            if re.search(word, decoded_request, re.IGNORECASE) or re.search(word, decoded_response, re.IGNORECASE):
                results.append(f"File: {file_path}, Item: {item_index}, Matched: {word}")
                break  # Stop checking other words for this item once a match is found

    return results


def process_technique_folder(technique_path):
    wordlist_path = os.path.join(technique_path, 'wordlist.txt')

    # Check if wordlist.txt exists
    if not os.path.exists(wordlist_path):
        print(f"No wordlist.txt found in {technique_path}. Skipping this folder.")
        return

    alarm_path = os.path.join(technique_path, 'Alarm.txt')

    # Read wordlist
    with open(wordlist_path, 'r') as f:
        wordlist = [line.strip() for line in f if line.strip()]

    results = []

    # Process XML files
    for filename in os.listdir(technique_path):
        if filename.endswith('.xml'):
            xml_path = os.path.join(technique_path, filename)
            results.extend(analyze_xml_file(xml_path, wordlist))

    # Write results to Alarm.txt
    if results:
        with open(alarm_path, 'a') as f:
            f.write(f"\n--- Results for {technique_path} ---\n")
            for result in results:
                f.write(result + '\n')
        print(f"Alarms recorded for {technique_path}")
    else:
        print(f"No alarms triggered for {technique_path}")


def navigate_folders(base_url):
    for root, dirs, files in os.walk(base_url):
        if 'Techniques' in dirs:
            techniques_path = os.path.join(root, 'Techniques')
            for technique in os.listdir(techniques_path):
                technique_path = os.path.join(techniques_path, technique)
                if os.path.isdir(technique_path):
                    print(f"Processing technique: {technique_path}")
                    process_technique_folder(technique_path)


# Main execution
if __name__ == "__main__":
    base_url = r"C:\Users\james\PycharmProjects\JSONWebApplicationAttack"
    navigate_folders(base_url)
    print("Processing complete.")