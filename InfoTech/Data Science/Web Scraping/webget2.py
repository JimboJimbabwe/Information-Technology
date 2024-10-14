import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
import concurrent.futures
import threading
import time
import sys

# Global variables
visited = set()
visited_lock = threading.Lock()
endpoints = set()
endpoints_lock = threading.Lock()
total_urls = 0
processed_urls = 0
start_time = None

def get_base_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"

def crawl_url(url, base_url, depth, max_depth):
    global visited, endpoints, total_urls, processed_urls

    with visited_lock:
        if url in visited or depth > max_depth:
            return
        visited.add(url)

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            
            with endpoints_lock:
                for link in links:
                    href = link['href']
                    full_url = urljoin(base_url, href)
                    if full_url.startswith(base_url):
                        endpoints.add(full_url)

            with visited_lock:
                processed_urls += 1
                if processed_urls % 10 == 0:
                    elapsed_time = time.time() - start_time
                    print(f"\rProcessed {processed_urls}/{total_urls} URLs. Elapsed time: {elapsed_time:.2f} seconds", end="")
                    sys.stdout.flush()

            if depth < max_depth:
                with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                    futures = [executor.submit(crawl_url, link, base_url, depth + 1, max_depth) 
                               for link in endpoints if link not in visited]
                    concurrent.futures.wait(futures)

    except requests.RequestException as e:
        print(f"\nError crawling {url}: {e}")

def analyze_endpoints(base_url, max_depth, timeout, max_urls, output_file):
    global total_urls, processed_urls, start_time, endpoints

    print(f"Analyzing endpoints for: {base_url}")
    start_time = time.time()
    total_urls = 1
    processed_urls = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future = executor.submit(crawl_url, base_url, base_url, 0, max_depth)
        try:
            future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            print(f"\nCrawl timed out after {timeout} seconds.")

    elapsed_time = time.time() - start_time
    print(f"\n\nCrawl completed in {elapsed_time:.2f} seconds.")
    print(f"Total unique endpoints found: {len(endpoints)}")

    # Write endpoints to file
    with open(output_file, 'w') as f:
        for endpoint in sorted(endpoints):
            f.write(f"{endpoint}\n")

    print(f"Endpoints written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze endpoints of a URL for bug bounty testing")
    parser.add_argument("url", help="The base URL to analyze")
    parser.add_argument("--max-depth", type=int, default=3, help="Maximum crawling depth (default: 3)")
    parser.add_argument("--timeout", type=int, default=300, help="Maximum execution time in seconds (default: 300)")
    parser.add_argument("--max-urls", type=int, default=1000, help="Maximum number of URLs to process (default: 1000)")
    parser.add_argument("--output", default="endpoints.txt", help="Output file name (default: endpoints.txt)")
    args = parser.parse_args()

    base_url = get_base_url(args.url)
    analyze_endpoints(base_url, args.max_depth, args.timeout, args.max_urls, args.output)
