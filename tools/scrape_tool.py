
from typing import Optional
import requests
import trafilatura

# User-Agent header to avoid basic client blocks
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def scrape_url(url: str, timeout: int = 6) -> Optional[str]:
    """
    Fetches full webpage text using Trafilatura, stripping nav, ads, and boilerplate.
    Returns cleaned text string or None if scraping fails/times out.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        if response.status_code != 200:
            print(f"[SCRAPE WARNING] HTTP {response.status_code} for URL: {url}")
            return None

        text = trafilatura.extract(response.text)
        if text and len(text.strip()) > 100:  # Ensure meaningful content was extracted
            return text.strip()
        
        return None
    except Exception as e:
        print(f"[SCRAPE WARNING] Failed to scrape {url}: {e}")
        return None