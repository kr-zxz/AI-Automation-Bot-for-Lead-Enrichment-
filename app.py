import streamlit as st
import pandas as pd
from enrich import get_company_info_from_domain, fetch_homepage_text, query_llm, parse_llm_response

# --- Page Config ---
st.set_page_config(page_title="AI Lead Enrichment", page_icon="🤖", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
        .main {
            background-color: #f9f9f9;
            font-family: 'Segoe UI', sans-serif;
        }
        h1 {
            color: #2e86de;
        }
        .stButton button {
            background-color: #2e86de;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.5em 1.5em;
        }
        .stDownloadButton button {
            background-color: #27ae60;
            color: white;
            border-radius: 8px;
        }
        .block-container {
            padding-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1>🤖 AI Automation Bot for Lead Enrichment</h1>", unsafe_allow_html=True)
st.markdown("Upload a CSV of company names and get enriched insights using LLMs. 🚀")

# --- File Upload ---
uploaded_file = st.file_uploader("📤 Upload a CSV file with a `company_name` column", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if "company_name" not in df.columns:
        st.error("❌ CSV must contain a column named `company_name`.")
    else:
        enriched_data = []
        progress = st.progress(0)
        total = len(df)

        for idx, row in df.iterrows():
            company = row["company_name"]
            st.info(f"🔎 Processing: **{company}**")
            try:
                domain = company.lower().replace(" ", "") + ".com"
                info = get_company_info_from_domain(domain)
                homepage_text = fetch_homepage_text(info["website"])
                llm_response = query_llm(company, homepage_text)
                summary, industry, pitch = parse_llm_response(llm_response)

                enriched_data.append({
                    "company_name": company,
                    "website": info["website"],
                    "industry": industry,
                    "summary_from_llm": summary,
                    "automation_pitch_from_llm": pitch
                })
            except Exception as e:
                enriched_data.append({
                    "company_name": company,
                    "website": "Error",
                    "industry": "Error",
                    "summary_from_llm": f"Error: {e}",
                    "automation_pitch_from_llm": ""
                })

            progress.progress((idx + 1) / total)

        result_df = pd.DataFrame(enriched_data)

        st.success("✅ Enrichment complete!")
        st.markdown("### 📊 Enriched Results")
        st.dataframe(result_df, use_container_width=True)

        csv = result_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Enriched CSV", data=csv, file_name="enriched_leads.csv", mime="text/csv")
