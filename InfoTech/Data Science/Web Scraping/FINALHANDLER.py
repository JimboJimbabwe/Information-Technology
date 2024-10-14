import os
import shutil
import argparse

# Hardcoded source folder path
SOURCE_FOLDER = "/home/kali/Desktop/ATest"

def move_file(root_dir, business, asset_type, asset_value):
    # Construct the destination path
    dest_path = os.path.join(root_dir, business, asset_type, asset_value)
    
    # Ensure the destination directory exists
    os.makedirs(dest_path, exist_ok=True)
    
    # Get the list of files in the source folder
    files = os.listdir(SOURCE_FOLDER)
    
    if not files:
        print(f"No files found in {SOURCE_FOLDER}")
        return
    
    if len(files) > 1:
        print(f"Warning: Multiple files found in {SOURCE_FOLDER}. Moving the first file.")
    
    # Get the first file
    file_to_move = files[0]
    source_file_path = os.path.join(SOURCE_FOLDER, file_to_move)
    
    # Construct the destination file path
    dest_file_path = os.path.join(dest_path, file_to_move)
    
    # Move the file
    shutil.move(source_file_path, dest_file_path)
    
    print(f"Moved {file_to_move} to {dest_file_path}")

def main():
    parser = argparse.ArgumentParser(description="Move file based on provided flags")
    parser.add_argument("--root_dir", required=True, help="Root directory for destination")
    parser.add_argument("--business", required=True, help="Business name")
    parser.add_argument("--asset_type", required=True, help="Asset type")
    parser.add_argument("--asset_value", required=True, help="Asset value")
    
    args = parser.parse_args()
    
    move_file(args.root_dir, args.business, args.asset_type, args.asset_value)

if __name__ == "__main__":
    main()
