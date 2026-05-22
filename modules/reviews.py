import os
from apify_client import ApifyClient

def get_google_reviews(company_name: str, max_reviews: int = 20) -> dict:
    client = ApifyClient(os.getenv("APIFY_API_KEY"))
    print(f"[reviews] Getting reviews for {company_name}...")
    run_input = {
        "searchStringsArray": [company_name],
        "maxReviewsPerQuery": max_reviews,
        "language": "it",
    }
    try:
        run = client.actor("compass/google-maps-reviews-scraper").call(run_input=run_input)
        reviews = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            reviews.append({
                "rating": item.get("stars", 0),
                "text": item.get("text", "")[:500],
                "date": item.get("publishedAtDate", "")
            })
        print(f"[reviews] Got {len(reviews)} reviews for {company_name}")
        return {"company": company_name, "reviews": reviews}
    except Exception as e:
        print(f"[reviews] Error for {company_name}: {e}")
        return {"company": company_name, "reviews": []}
