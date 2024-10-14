import os

def create_url_list(base_path):
    # Iterate through each folder in the base path
    for business_folder in os.listdir(base_path):
        business_path = os.path.join(base_path, business_folder)
        
        # Check if it's a directory
        if os.path.isdir(business_path):
            url_folder = os.path.join(business_path, 'URL')
            
            # Check if URL folder exists
            if os.path.exists(url_folder) and os.path.isdir(url_folder):
                urls = [f for f in os.listdir(url_folder) if os.path.isdir(os.path.join(url_folder, f))]
                
                # Create urls.txt file
                with open(os.path.join(url_folder, 'urls.txt'), 'w') as f:
                    for url in urls:
                        f.write(f"{url}\n")
                
                print(f"Created urls.txt in {url_folder}")

if __name__ == "__main__":
    base_path = "/home/kali/Desktop/BugBountyWork"
    create_url_list(base_path)
    print("Process completed.")
