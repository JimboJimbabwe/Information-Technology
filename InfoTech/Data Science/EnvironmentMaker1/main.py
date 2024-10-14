import os
import json

def get_techniques(base_path, category, vulnerability):
    techniques_path = os.path.join(base_path, category, vulnerability, "Techniques")
    if os.path.exists(techniques_path):
        return [technique for technique in os.listdir(techniques_path) if os.path.isdir(os.path.join(techniques_path, technique))]
    return []

def process_json_structure(base_path, json_structure):
    result = {}
    for category, vulnerabilities in json_structure.items():
        result[category] = []
        for vulnerability in vulnerabilities:
            techniques = get_techniques(base_path, category, vulnerability)
            result[category].append({
                "name": vulnerability,
                "techniques": techniques
            })
    return result

def main():
    # Define the base path (you can change this to your desired path)
    base_path = r"C:\Users\james\PycharmProjects\JSONWebApplicationAttack"

    # The original JSON structure
    json_structure = {
        "Advanced Topics": [
            "llm-attacks",
            "graphql",
            "deserialization",
            "server-side-template-injection",
            "web-cache-poisoning",
            "host-header",
            "request-smuggling",
            "oauth",
            "jwt",
            "prototype-pollution",
            "essential-skills"
        ],
        "Client-Side Topics": [
            "cross-site-scripting",
            "csrf",
            "cors",
            "clickjacking",
            "dom-based",
            "websockets"
        ],
        "Server-Side Topics": [
            "sql-injection",
            "authentication",
            "file-path-traversal",
            "os-command-injection",
            "logic-flaws",
            "information-disclosure",
            "access-control",
            "file-upload",
            "race-conditions",
            "ssrf",
            "xxe",
            "nosql-injection",
            "api-testing"
        ]
    }

    # Process the JSON structure
    result = process_json_structure(base_path, json_structure)

    # Write the result to a JSON file
    output_file = "vulnerabilities_with_techniques.json"
    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)

    print(f"JSON structure has been written to {output_file}")

if __name__ == "__main__":
    main()