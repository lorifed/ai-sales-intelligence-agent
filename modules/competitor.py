import os
import json
import anthropic
from apify_client import ApifyClient

def find_competitors(business_summary: str, original_url: str) -> list:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    print("[competitor] Finding competitors...")
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": f"""Based on this business summary, list 4 direct competitors (real companies with websites).
Return ONLY a JSON array like: [{{"name":"Brand","url":"https://..."}}]
No explanation, no markdown, just the JSON.

Business: {business_summary[:2000]}
Original URL: {original_url}"""
        }]
    )
    text = response.content[0].text.strip().replace("```json", "").replace("```", "").strip()
    competitors = json.loads(text)
    print(f"[competitor] Found: {[c['name'] for c in competitors]}")
    return competitors

def scrape_competitor(url: str) -> dict:
    client = ApifyClient(os.getenv("APIFY_API_KEY"))
    run_input = {
        "startUrls": [{"url": url}],
        "maxCrawlPages": 5,
        "maxCrawlDepth": 1,
        "outputFormats": ["text"],
    }
    run = client.actor("apify/website-content-crawler").call(run_input=run_input)
    dataset_id = run["defaultDatasetId"]
    pages = []
    for item in client.dataset(dataset_id).iterate_items():
        if item.get("text"):
            pages.append(item.get("text", "")[:2000])
    return {"url": url, "content": " ".join(pages)[:5000]}
