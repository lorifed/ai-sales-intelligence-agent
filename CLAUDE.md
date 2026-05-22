# Sales Intelligence Agent — CLAUDE.md

## Scopo
Agente che analizza un'azienda target e genera un report PDF di competitive intelligence.

## Struttura
- `agent.py` — orchestratore principale, entry point CLI
- `modules/scraper.py` — scraping sito via Apify
- `modules/competitor.py` — identificazione + scraping competitor
- `modules/reviews.py` — recensioni Google via Apify
- `modules/funnel.py` — analisi funnel acquisizione
- `modules/analysis.py` — analisi completa via Claude
- `modules/report.py` — generazione PDF con reportlab

## Utilizzo
```bash
python agent.py https://example.com
```

## Env vars richieste
- ANTHROPIC_API_KEY
- APIFY_API_KEY
