import json
import re

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def extract_service_name(url):
    # Extract the service name from the URL
    match = re.search(r'pentesting-([\w-]+)', url, re.IGNORECASE)
    if match:
        return match.group(1).lower()
    return None

def merge_links_with_services(services, links):
    for link in links:
        service_name = extract_service_name(link)
        if service_name:
            for service in services:
                if service_name in service.lower():
                    services[service]['link'] = link
                    break
    return services

def main():
    services_file = 'services.json'
    links_file = 'extracted_links.json'
    output_file = 'updated_services.json'

    services = load_json(services_file)
    links = load_json(links_file)

    updated_services = merge_links_with_services(services, links)

    save_json(updated_services, output_file)
    print(f"Updated services with links and saved to {output_file}")

if __name__ == "__main__":
    main()