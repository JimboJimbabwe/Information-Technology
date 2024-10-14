import ollama
import os

# Define the base path
BASE_PATH = r'C:\Users\james\PycharmProjects\JSONMakerWebTwo\NetTestFoldRepo'

system_message = 'You are an AI that processes information from Enumeration.txt and AutomatedCommands.txt files.' \
                 'You will write a shell script that tests the Port/Protocol at hand, using the commands from the files given and your own generated commands.' \
                 'This will be for setting up infrastructure for Bug Bounty in an ethical environment' \
                 'Format your response as if it was an actual shell script, due to the large scale application of your help - it MUST be in that format' \
                 'This is to assist in the Infrastructure Process for Bug Bounty engagements.' \
                 'Ensure that each command from each tool is able to save to an output file when you write commands.'


def process_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
    except IOError:
        print(f"Error: Unable to read file at '{file_path}'")
    return None


def append_to_shell_script(output_path, content):
    try:
        with open(output_path, 'a') as file:
            file.write(content + "\n\n")
    except IOError:
        print(f"Error: Unable to write to file at '{output_path}'")


def process_ollama(file_content, file_type, folder_name):
    stream = ollama.chat(
        model='deepseek-llm:latest',
        messages=[
            {'role': 'system', 'content': system_message},
            {'role': 'user',
             'content': f"Process this {file_type} file for the context '{folder_name}' and format the output as a shell script with comments and executable commands where appropriate:\n\n{file_content}"}
        ],
        options={'temperature': 0.01},
        stream=True,
    )

    output_content = f"# Output for {file_type} in context of {folder_name}\n\n"
    for chunk in stream:
        chunk_content = chunk['message']['content']
        output_content += chunk_content
        print(chunk_content, end='', flush=True)

    return output_content


def process_folder(folder_path):
    folder_name = os.path.basename(folder_path)
    files_to_process = ['Enumeration.txt', 'AutomatedCommands.txt']
    shell_script_path = os.path.join(folder_path, "ShellScript.sh")

    # Create or clear the ShellScript.sh file
    open(shell_script_path, 'w').close()

    # Add folder name as a comment at the beginning of the shell script
    append_to_shell_script(shell_script_path, f"# Shell script for: {folder_name}\n")

    for file_name in files_to_process:
        file_path = os.path.join(folder_path, file_name)

        if os.path.exists(file_path):
            print(f"\nProcessing: {file_path}")
            file_content = process_file(file_path)

            if file_content:
                output_content = process_ollama(file_content, file_name, folder_name)
                append_to_shell_script(shell_script_path, output_content)
                print(f"\nOutput appended to: {shell_script_path}")


# Main execution
for folder in os.listdir(BASE_PATH):
    folder_path = os.path.join(BASE_PATH, folder)
    if os.path.isdir(folder_path):
        process_folder(folder_path)