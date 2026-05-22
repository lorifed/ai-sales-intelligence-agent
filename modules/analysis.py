import os
import json
import anthropic

def generate_analysis(scraped_data: dict, competitors: list, competitor_contents: list,
                       reviews_data: list, funnel_data: dict) -> dict:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    print("[analysis] Generating full intelligence report...")
    pages_text = " ".join([p.get("text", "") for p in scraped_data.get("pages", [])])[:4000]
    comp_summary = "\n".join([
        f"Competitor: {c.get('url','')}\nContent: {c.get('content','')[:800]}"
        for c in competitor_contents
    ])
    reviews_summary = "\n".join([
        f"Company: {r.get('company','')}, Reviews: {len(r.get('reviews',[]))} | "
        f"Avg rating: {(sum(x.get('rating',0) for x in r.get('reviews',[])) / max(len(r.get('reviews',[])),1)):.1f}"
        for r in reviews_data
    ])
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4000,
        messages=[{
            "role": "user",
            "content": f"""You are a senior business intelligence consultant. Analyze this company and generate a complete Sales Intelligence Report in ITALIAN.

TARGET COMPANY: {scraped_data.get('url','')}
WEBSITE CONTENT: {pages_text}

COMPETITORS:
{comp_summary}

REVIEWS DATA:
{reviews_summary}

FUNNEL ANALYSIS:
{str(funnel_data)}

Return a JSON object with these exact keys:
- company_name: string
- business_overview: string (3-4 sentences about what they do, products, target)
- target_market: string
- value_proposition: string
- competitor_analysis: list of objects with keys: name, url, strengths, weaknesses, pricing_signals
- gap_analysis: list of 5 specific gaps vs competitors
- growth_opportunities: list of 5 prioritized opportunities with title and description
- recommendations: list of 5 actionable recommendations prioritized by impact, each with: priority(1-5), title, action, expected_impact
- review_insights: string (key themes from competitor reviews)
- executive_summary: string (5-6 sentence summary for C-level)

Be specific, data-driven, and actionable. Write everything in Italian.
Return ONLY valid JSON, no markdown."""
        }]
    )
    text = response.content[0].text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(text)
