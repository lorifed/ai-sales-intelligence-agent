# AI Sales Intelligence Agent
### by [21STUDIO](https://21studio.io)

Inserisci l'URL di un'azienda e ricevi un report PDF completo di competitive intelligence in ~10 minuti.

## Cosa fa
1. Scrapa il sito target
2. Trova i competitor automaticamente
3. Analizza prezzi e posizionamento
4. Raccoglie recensioni Google
5. Analizza il funnel di acquisizione
6. Genera un PDF professionale brandizzato

## Setup
```bash
git clone https://github.com/lorifed/ai-sales-intelligence-agent
cd ai-sales-intelligence-agent
pip install -r requirements.txt
cp .env.example .env
```

## Utilizzo
```bash
python agent.py https://example.com
```

## API Keys necessarie
- ANTHROPIC_API_KEY — console.anthropic.com
- APIFY_API_KEY — apify.com

## Stack
Python, Anthropic Claude, Apify, ReportLab

---
Built by [21STUDIO](https://21studio.io)
