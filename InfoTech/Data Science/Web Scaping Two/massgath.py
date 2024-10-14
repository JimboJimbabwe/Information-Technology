import requests
import urllib3
from urllib.parse import urlparse, urlunparse

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def add_scheme_if_missing(url, default_scheme='https'):
    parsed = urlparse(url)
    if not parsed.scheme:
        return urlunparse((default_scheme, parsed.netloc or parsed.path, parsed.path if parsed.netloc else '', parsed.params, parsed.query, parsed.fragment))
    return url

def send_to_burp(url, proxy):
    url_with_scheme = add_scheme_if_missing(url)
    try:
        response = requests.get(url_with_scheme, proxies=proxy, verify=False)
        print(f"Sent {url_with_scheme} to Burp")
    except requests.exceptions.RequestException as e:
        print(f"Error sending {url_with_scheme} to Burp: {e}")

if __name__ == "__main__":
    proxy = {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080"
    }

    with open("urls.txt", "r") as file:
        urls = file.read().splitlines()

    for url in urls:
        send_to_burp(url, proxy)

    print("All URLs have been sent to Burp")
