# main.py
import openai

openai.api_key = "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"
openai.api_base = "https://api.groq.com/openai/v1"  # Optional if using Groq

def ask_llm(company_name, homepage_text):
    prompt = f"""
    Analyze the following company's homepage and provide:
    1. A brief summary of what the company does.
    2. Who is the company's target customer?
    3. Suggest a custom AI automation idea QF Innovate could pitch.

    Company: {company_name}
    Homepage Content:
    {homepage_text[:4000]}  # Limit to avoid token overflow
    """

    response = openai.ChatCompletion.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']