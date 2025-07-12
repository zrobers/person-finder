import os
import requests
from dotenv import load_dotenv

load_dotenv()

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"

def perplexity_search(prompt, output_schema=None, model="sonar-pro"):
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    if output_schema:
        payload["output_schema"] = output_schema

    response = requests.post(PERPLEXITY_API_URL, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()