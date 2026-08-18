
from typing import Dict, Any, List
from graph.state import AgentState
from tools.scrape_tool import scrape_url

def scraper_node(state: AgentState) -> Dict[str, Any]:
    """
    Iterates over state["search_results"], scrapes full text for each URL,
    and saves successful extracts in state["scraped_docs"].
    """
    search_results = state.get("search_results", [])
    scraped_docs: List[Dict[str, str]] = []
    seen_urls = set()

    print(f"\n--- Executing Web Scraper Node ---")

    for item in search_results:
        url = item.get("url")
        title = item.get("title", "")

        if not url or url in seen_urls:
            continue

        seen_urls.add(url)
        print(f"Scraping: {url}...")

        text = scrape_url(url)
        if text:
            print(f"  [SUCCESS] Extracted {len(text)} characters")
            scraped_docs.append({
                "url": url,
                "title": title,
                "text": text
            })
        else:
            print(f"  [SKIPPED] Extraction returned no usable content")

    return {
        "scraped_docs": scraped_docs
    }