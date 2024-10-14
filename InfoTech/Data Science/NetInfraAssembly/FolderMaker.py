import json
import os


def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def display_services(services):
    for i, service in enumerate(services.keys(), 1):
        print(f"{i}. {service}")


def get_user_selection(services):
    selected_indices = input("Enter the numbers of the services you want to create folders for (separated by spaces): ")
    selected_indices = [int(i) - 1 for i in selected_indices.split()]
    return [list(services.keys())[i] for i in selected_indices if 0 <= i < len(services)]


def create_folders(selected_services, services, base_path):
    additional_files = [
        "AutomatedCommands.txt",
        "Misconfigurations.txt",
        "Enumeration.txt",
        "DefaultCredentials.txt"
    ]

    for service in selected_services:
        folder_name = service.replace(" ", "_").replace("/", "_")
        folder_path = os.path.join(base_path, folder_name)

        try:
            os.makedirs(folder_path, exist_ok=True)
            print(f"Created folder: {folder_path}")

            # Create a README.md file with service information
            readme_path = os.path.join(folder_path, "README.md")
            with open(readme_path, "w") as readme_file:
                readme_file.write(f"# {service}\n\n")
                readme_file.write(f"Ports: {services[service]['ports']}\n\n")
                readme_file.write(f"Link: {services[service]['link']}\n")

            print(f"Created README.md in {folder_path}")

            # Create additional empty text files
            for file_name in additional_files:
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, "w") as file:
                    pass  # Create an empty file
                print(f"Created {file_name} in {folder_path}")

        except Exception as e:
            print(f"Error creating folder or files for {service}: {str(e)}")


def main():
    json_file = 'updated_services.json'
    base_path = input("Enter the base path where you want to create the folders: ")

    services = load_json(json_file)

    print("Available services:")
    display_services(services)

    selected_services = get_user_selection(services)

    if selected_services:
        create_folders(selected_services, services, base_path)
        print("Folder and file creation complete.")
    else:
        print("No services selected. No folders or files created.")


if __name__ == "__main__":
    main()