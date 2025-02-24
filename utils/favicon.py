import os
import re
import requests

CACHE_DIR = "cache/favicons"
os.makedirs(CACHE_DIR, exist_ok=True)


def download_favicon(url):
    try:
        domain_match = re.search(r"https?://([^/]+)/?", url)
        if not domain_match:
            return None
        domain = domain_match.group(1)
        favicon_path = os.path.join(CACHE_DIR, f"{domain}.ico")
        if os.path.exists(favicon_path):
            return favicon_path
        favicon_url = f"https://{domain}/favicon.ico"
        response = requests.get(favicon_url, timeout=5)
        if response.status_code == 200:
            with open(favicon_path, "wb") as f:
                f.write(response.content)
            return favicon_path
    except Exception as e:
        print(f"Error downloading favicon for {url}: {e}")
    return None
