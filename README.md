# 🤖 AI Automation Bot for Lead Enrichment

This AI-powered automation bot enriches company data using real-time web scraping and LLM-based analysis. Given a list of company names, it identifies their domain, extracts homepage content, and generates valuable business insights such as a summary, industry type, and a pitch for automation.

---

## 📌 Features

- 🔍 Automatically derives the company website using name-based heuristics
- 🌐 Scrapes homepage content to understand company services
- 🧠 Uses LLMs (via Groq API) to summarize and classify company info
- 🧾 Outputs enriched data including industry and automation pitch
- 📥 Download enriched data as a CSV file
- 🖥️ Streamlit-based UI for easy interaction

---

## 🚀 Demo

> 🎥 **Watch the tool in action below:**

[![Demo Video]

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Web Scraping**: `requests`, `BeautifulSoup`
- **LLM Integration**: Groq API
- **Data Handling**: `pandas`

---

## 📁 File Structure
├── app.py # Streamlit app UI
├── enrich.py # Scraping + LLM query utilities
├── requirements.txt # Python dependencies
├── .env # Store your GROQ_API_KEY securely
└── README.md # Project documentation


---

## 🛠️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ai-lead-enrichment-bot.git
   cd ai-lead-enrichment-bot


GROQ_API_KEY=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
pip install -r requirements.txt
streamlit run app.py
