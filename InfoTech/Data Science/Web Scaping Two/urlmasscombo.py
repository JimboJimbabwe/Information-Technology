import os

def consolidate_url_files(base_path, output_file):
    # Open the output file
    with open(output_file, 'w') as outfile:
        # Iterate through each folder in the base path
        for business_folder in os.listdir(base_path):
            business_path = os.path.join(base_path, business_folder)
            
            # Check if it's a directory
            if os.path.isdir(business_path):
                url_folder = os.path.join(business_path, 'URL')
                
                # Check if URL folder exists
                if os.path.exists(url_folder) and os.path.isdir(url_folder):
                    urls_file = os.path.join(url_folder, 'urls.txt')
                    
                    # Check if urls.txt exists in the URL folder
                    if os.path.exists(urls_file):
                        # Read and write the contents of urls.txt
                        with open(urls_file, 'r') as infile:
                            outfile.write(infile.read())
                        
                        print(f"Added URLs from {business_folder}")

if __name__ == "__main__":
    base_path = "/home/kali/Desktop/BugBountyWork"
    output_file = "/home/kali/Desktop/urlsMasse.txt"
    
    consolidate_url_files(base_path, output_file)
    print(f"Process completed. All URLs consolidated in {output_file}")
