import os
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

def is_url_match(url, scope_url):
    parsed_url = urlparse(url)
    parsed_scope = urlparse(scope_url)
    return parsed_url.netloc.endswith(parsed_scope.netloc)

def extract_scoped_xml(base_path, raw_xml_path):
    # Parse the raw XML file
    tree = ET.parse(raw_xml_path)
    root = tree.getroot()

    # Iterate through each folder in the base path
    for business_folder in os.listdir(base_path):
        business_path = os.path.join(base_path, business_folder)
        
        if os.path.isdir(business_path):
            url_folder = os.path.join(business_path, 'URL')
            
            if os.path.exists(url_folder) and os.path.isdir(url_folder):
                urls_file = os.path.join(url_folder, 'urls.txt')
                
                if os.path.exists(urls_file):
                    # Read the URLs for this business
                    with open(urls_file, 'r') as f:
                        urls = [url.strip() for url in f.readlines()]
                    
                    print(f"Processing {business_folder}. Scope URLs: {urls}")

                    # Create a new XML root for this business
                    business_root = ET.Element("business")
                    business_root.set("name", business_folder)

                    # Filter and add relevant entries
                    matched_count = 0
                    for item in root.findall('.//item'):
                        url_elem = item.find('url')
                        if url_elem is not None:
                            url = url_elem.text
                            if any(is_url_match(url, scope_url) for scope_url in urls):
                                business_root.append(item)
                                matched_count += 1
                                print(f"  Matched URL: {url}")

                    print(f"  Total matches for {business_folder}: {matched_count}")

                    # Create a new XML file for this business
                    business_tree = ET.ElementTree(business_root)
                    output_file = os.path.join(url_folder, f"{business_folder}_data.xml")
                    business_tree.write(output_file, encoding="utf-8", xml_declaration=True)
                    
                    print(f"Created {output_file}")

if __name__ == "__main__":
    base_path = "/home/kali/Desktop/BugBountyWork"
    raw_xml_path = "/home/kali/Desktop/ATest/SortMe.xml"  # Adjust this path to your raw XML file
    
    extract_scoped_xml(base_path, raw_xml_path)
    print("Process completed.")
