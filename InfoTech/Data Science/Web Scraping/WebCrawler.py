import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
import time
import sys
import os

def get_base_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"

def crawl_url(url, base_url, visited, endpoints, depth=0, max_depth=3, timeout=300):
    if depth > max_depth or url in visited or time.time() - crawl_url.start_time > timeout:
        return
    visited.add(url)
    try:
        response = requests.get(url, timeout=10)  # 10-second timeout for each request
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(base_url, href)
                
                if full_url.startswith(base_url):
                    endpoints.add(full_url)
                    crawl_url(full_url, base_url, visited, endpoints, depth + 1, max_depth, timeout)
        # Print progress
        elapsed_time = time.time() - crawl_url.start_time
        print(f"\rProcessed URLs: {len(visited)}, Unique endpoints: {len(endpoints)}, Time elapsed: {elapsed_time:.2f}s", end="")
        sys.stdout.flush()
    except requests.RequestException as e:
        print(f"\nError crawling {url}: {e}")
    if time.time() - crawl_url.start_time > timeout:
        print("\nTimeout reached. Stopping the crawl.")
        return

crawl_url.start_time = 0  # This will be set in analyze_endpoints

def analyze_endpoints(base_url, output_file):
    print(f"Analyzing endpoints for: {base_url}")
    visited = set()
    endpoints = set()
    max_depth = 3
    timeout = 300
    crawl_url.start_time = time.time()
    crawl_url(base_url, base_url, visited, endpoints, max_depth=max_depth, timeout=timeout)
    print("\n\nDiscovered endpoints:")
    for endpoint in sorted(endpoints):
        print(endpoint)
    
    print(f"\nTotal unique endpoints found: {len(endpoints)}")
    print(f"Total time elapsed: {time.time() - crawl_url.start_time:.2f} seconds")
    
    if output_file:
        with open(output_file, 'w') as f:
            for endpoint in sorted(endpoints):
                f.write(f"{endpoint}\n")
        print(f"\nEndpoints written to {output_file}")

def sanitize_filename(filename):
    return ''.join(c for c in filename if c.isalnum() or c in ('-', '_', '.')).rstrip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze endpoints of a URL for bug bounty testing")
    parser.add_argument("--root_dir", required=True, help="Root directory for output")
    parser.add_argument("--business", required=True, help="Business name")
    parser.add_argument("--asset_type", required=True, help="Asset type")
    parser.add_argument("--asset_value", required=True, help="Asset value (URL to analyze)")
    args = parser.parse_args()

    # Construct the output directory path
    output_dir = os.path.join(args.root_dir, args.business, args.asset_type, args.asset_value)
    os.makedirs(output_dir, exist_ok=True)

    # Sanitize the asset_value for use as a filename
    sanitized_asset_value = sanitize_filename(args.asset_value)

    # Construct the output file path
    output_file = os.path.join(output_dir, f"{sanitized_asset_value}.txt")

    # Get the base URL from the asset_value, adding https:// if not present
    base_url = get_base_url(args.asset_value)

    # Run the analysis
    analyze_endpoints(base_url, output_file)
