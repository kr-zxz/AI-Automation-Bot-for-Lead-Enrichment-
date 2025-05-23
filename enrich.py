import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}


def get_company_info_from_domain(domain):
    """Returns only website, fills rest with N/A (industry now handled by LLM)."""
    return {
        "website": f"https://{domain}",
        "industry": "N/A",
        "company_size": "N/A",
        "location": "N/A"
    }


def fetch_homepage_text(website):
    try:
        response = requests.get(website, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        texts = soup.stripped_strings
        visible_text = " ".join(texts)
        return visible_text[:5000]  # limit to first 5000 chars
    except Exception as e:
        return f"Error: {e}"


def query_llm(company_name, homepage_text):
    prompt = f"""
You're analyzing {company_name}'s homepage.

1. Summarize what this company does.
2. Identify the industry this company operates in.
3. Suggest an AI automation idea QF Innovate could pitch them.

Homepage content:
{homepage_text}
"""

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 512
    }

    try:
        res = requests.post(GROQ_API_URL, headers=HEADERS, json=payload)
        res.raise_for_status()
        content = res.json()["choices"][0]["message"]["content"]
        return content
    except Exception as e:
        return f"LLM error: {e}"


def parse_llm_response(response):
    summary, industry, pitch = "N/A", "N/A", "N/A"
    if "1." in response and "2." in response and "3." in response:
        try:
            parts = re.split(r"\n?1\.\s*|\n?2\.\s*|\n?3\.\s*", response)
            _, summary, industry, pitch = parts
        except Exception:
            pass
    return summary.strip(), industry.strip(), pitch.strip()
