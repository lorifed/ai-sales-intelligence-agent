import os
from apify_client import ApifyClient

def scrape_website(url: str) -> dict:
    client = ApifyClient(os.getenv("APIFY_API_KEY"))
    print(f"[scraper] Scraping {url}...")
    run_input = {
        "startUrls": [{"url": url}],
        "maxCrawlPages": 10,
        "maxCrawlDepth": 2,
        "outputFormats": ["text"],
    }
    actor_run = client.actor("apify/website-content-crawler").call(run_input=run_input)
    dataset_id = actor_run.get("defaultDatasetId") if isinstance(actor_run, dict) else getattr(actor_run, "default_dataset_id", None) or getattr(actor_run, "defaultDatasetId", None)
    items = []
    for item in client.dataset(dataset_id).iterate_items():
        if item.get("text"):
            items.append({
                "url": item.get("url", ""),
                "title": item.get("metadata", {}).get("title", "") if isinstance(item.get("metadata"), dict) else "",
                "text": item.get("text", "")[:3000]
            })
    print(f"[scraper] Got {len(items)} pages")
    return {"url": url, "pages": items}
