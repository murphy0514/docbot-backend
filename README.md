# DocBot Backend (Flask)

This is a simple Flask API that:
- Accepts a PDF document and a user query
- Extracts the text from the PDF
- Sends the content + query to OpenAI (GPT-4)
- Returns a structured legal-style report

## Setup

1. Add your OpenAI key to `.env` or environment settings
2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run the app:

```
python main.py
```

## Deploy

You can deploy this on Render, Replit, or any Python-compatible server.
