import os
import json
import anthropic

def analyze_funnel(scraped_data: dict, competitor_data: list) -> dict:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    print("[funnel] Analyzing acquisition funnel...")
    pages_text = " ".join([p.get("text", "") for p in scraped_data.get("pages", [])])[:4000]
    comp_text = "\n".join([f"- {c.get('url','')}: {c.get('content','')[:500]}" for c in competitor_data])
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1500,
        messages=[{
            "role": "user",
            "content": f"""Analyze the acquisition funnel of this business based on its website content.
Return a JSON object with these keys:
- seo_presence: string (strong/medium/weak + brief reason)
- ads_signals: string (any signs of paid advertising)
- email_marketing: string (any newsletter/email capture)
- social_presence: list of detected social channels
- funnel_gaps: list of 3 identified weaknesses
- vs_competitors: string (how their funnel compares to competitors)

Website content: {pages_text}
Competitors overview: {comp_text}

Return ONLY valid JSON, no markdown, no explanation."""
        }]
    )
    text = response.content[0].text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(text)
