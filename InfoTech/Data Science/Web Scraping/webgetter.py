import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
from collections import defaultdict
import concurrent.futures
import threading
from urllib.robotparser import RobotFileParser
import time
import sys

# Global variables
visited = defaultdict(lambda: {'status': None, 'depth': float('inf')})
visited_lock = threading.Lock()
total_urls = 0
processed_urls = 0
start_time = None
url_queue = []
max_urls = 1000  # Default max URLs to process

def get_base_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"

def check_robots_txt(base_url):
    rp = RobotFileParser()
    robots_url = urljoin(base_url, "/robots.txt")
    try:
        rp.set_url(robots_url)
        rp.read()
        return rp
    except:
        print(f"No robots.txt found at {robots_url}, proceeding with crawl.")
        return None

def can_fetch(rp, url):
    if rp is None:
        return True
    return rp.can_fetch("*", url)

def crawl_url(url, base_url, rp, depth=0, max_depth=3):
    global visited, total_urls, processed_urls, url_queue

    with visited_lock:
        if depth > max_depth or (url in visited and depth >= visited[url]['depth']):
            return
        if total_urls >= max_urls:
            return

    if not can_fetch(rp, url):
        print(f"Skipping {url} as per robots.txt")
        return

    try:
        response = requests.get(url, allow_redirects=True, timeout=10)
        status = response.status_code
        final_url = response.url
    except requests.RequestException as e:
        print(f"\nError crawling {url}: {e}")
        status = f'Error: {type(e).__name__}'
        final_url = url

    with visited_lock:
        visited[final_url] = {'status': status, 'depth': depth}
        processed_urls += 1
        if processed_urls % 10 == 0:  # Update progress every 10 URLs
            elapsed_time = time.time() - start_time
            print(f"\rProcessed {processed_urls}/{total_urls} URLs. Elapsed time: {elapsed_time:.2f} seconds", end="")
            sys.stdout.flush()

    if status == 200 and depth < max_depth:
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            with visited_lock:
                for link in links:
                    href = link['href']
                    full_url = urljoin(base_url, href)
                    if full_url.startswith(base_url) and full_url not in visited and total_urls < max_urls:
                        url_queue.append((full_url, depth + 1))
                        total_urls += 1
        except Exception as e:
            print(f"\nError parsing {final_url}: {e}")

def analyze_endpoints(base_url, max_depth=3, timeout=300):
    global total_urls, processed_urls, start_time, url_queue
    print(f"Analyzing endpoints for: {base_url}")
    rp = check_robots_txt(base_url)
    total_urls = 1
    processed_urls = 0
    start_time = time.time()
    url_queue = [(base_url, 0)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        while url_queue and time.time() - start_time < timeout and total_urls <= max_urls:
            futures = []
            for _ in range(min(10, len(url_queue))):
                if url_queue:
                    url, depth = url_queue.pop(0)
                    futures.append(executor.submit(crawl_url, url, base_url, rp, depth, max_depth))
            concurrent.futures.wait(futures)
            time.sleep(0.1)  # Small delay to avoid overwhelming the server

    elapsed_time = time.time() - start_time
    print(f"\n\nCrawl completed in {elapsed_time:.2f} seconds.")
    print(f"Total unique endpoints found: {len(visited)}")
    
    print("\nStatus code distribution:")
    status_counts = defaultdict(int)
    for info in visited.values():
        status_counts[info['status']] += 1
    for status, count in status_counts.items():
        print(f"  {status}: {count}")

    print("\nDiscovered endpoints:")
    for url, info in sorted(visited.items()):
        print(f"{url} - Status: {info['status']}, Depth: {info['depth']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze endpoints of a URL for bug bounty testing")
    parser.add_argument("url", help="The base URL to analyze")
    parser.add_argument("--max-depth", type=int, default=3, help="Maximum crawling depth (default: 3)")
    parser.add_argument("--timeout", type=int, default=300, help="Maximum execution time in seconds (default: 300)")
    parser.add_argument("--max-urls", type=int, default=1000, help="Maximum number of URLs to process (default: 1000)")
    args = parser.parse_args()

    base_url = get_base_url(args.url)
    max_urls = args.max_urls
    analyze_endpoints(base_url, args.max_depth, args.timeout)
