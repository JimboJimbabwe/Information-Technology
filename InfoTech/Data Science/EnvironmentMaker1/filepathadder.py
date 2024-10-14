import json
import os

def normalize_path(path):
    return os.path.normpath(path).replace('\\', '/')


def add_folder_paths(json_file, base_folder):
    with open(json_file, 'r') as file:
        data = json.load(file)

    for service, info in data.items():
        # Preserve the original case, just remove special characters
        folder_name = service.replace(' ', '_').replace(',', '').replace('(', '').replace(')', '')
        folder_path = os.path.join(base_folder, folder_name)

        info['folder_path'] = normalize_path(folder_path)

    with open(json_file, 'w') as file:
        json.dump(data, file, indent=2)

    print(f"Updated {json_file} with case-preserved folder_path for each service.")


def main():
    json_file = 'PortDB.json'  # Replace with your JSON file path
    base_folder = r'C:\Users\james\PycharmProjects\JSONMakerWebTwo\NetTestFoldRepo'  # Replace with your desired base folder path

    add_folder_paths(json_file, base_folder)


if __name__ == "__main__":
    main()