import os
import sys
import json
import argparse
from dotenv import load_dotenv

load_dotenv()

from modules.scraper import scrape_website
from modules.competitor import find_competitors, scrape_competitor
from modules.reviews import get_google_reviews
from modules.funnel import analyze_funnel
from modules.analysis import generate_analysis
from modules.report import generate_pdf

def run_agent(url: str, output_path: str = None) -> str:
    print(f"\n{'='*50}")
    print(f"  21STUDIO AI Sales Intelligence Agent")
    print(f"  Target: {url}")
    print(f"{'='*50}\n")

    print("STEP 1/5 — Scraping target website...")
    scraped = scrape_website(url)
    pages_preview = " ".join([p.get("text","") for p in scraped.get("pages",[])])[:3000]

    print("\nSTEP 2/5 — Finding competitors...")
    competitors = find_competitors(pages_preview, url)
    print("  Scraping competitor websites...")
    competitor_contents = []
    for comp in competitors:
        try:
            content = scrape_competitor(comp["url"])
            competitor_contents.append(content)
        except Exception as e:
            print(f"  [!] Could not scrape {comp['url']}: {e}")
            competitor_contents.append({"url": comp["url"], "content": ""})

    print("\nSTEP 3/5 — Fetching competitor reviews...")
    reviews_data = []
    for comp in competitors[:3]:
        reviews = get_google_reviews(comp["name"])
        reviews_data.append(reviews)

    print("\nSTEP 4/5 — Analyzing acquisition funnel...")
    funnel = analyze_funnel(scraped, competitor_contents)

    print("\nSTEP 5/5 — Generating intelligence report...")
    analysis = generate_analysis(scraped, competitors, competitor_contents, reviews_data, funnel)

    with open("last_analysis.json", "w") as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)

    pdf_path = generate_pdf(analysis, output_path)

    print(f"\n{'='*50}")
    print(f"  DONE! Report saved to: {pdf_path}")
    print(f"{'='*50}\n")

    return pdf_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="21STUDIO AI Sales Intelligence Agent")
    parser.add_argument("url", help="Target company website URL")
    parser.add_argument("--output", "-o", help="Output PDF path", default=None)
    args = parser.parse_args()
    run_agent(args.url, args.output)
