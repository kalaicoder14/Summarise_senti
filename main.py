import streamlit as st
from groq import Groq
from dotenv import dotenv_values
from pypdf import PdfReader
from docx import Document
import pandas as pd

# Load API key safely-
config = dotenv_values(".env")
client = Groq(api_key=config["GROQ_API_KEY"])

st.title("📂 File Summarizer")

uploaded_file = st.file_uploader(
    "Upload file",
    type=["pdf", "txt", "docx", "csv"]
)

def extract_text(file):
    ext = file.name.split(".")[-1].lower()

    if ext == "pdf":
        reader = PdfReader(file)
        return "".join(p.extract_text() for p in reader.pages)

    if ext == "txt":
        return file.read().decode("utf-8")

    if ext == "docx":
        doc = Document(file)
        return "\n".join(p.text for p in doc.paragraphs)

    if ext == "csv":
        return pd.read_csv(file).to_string(index=False)

if uploaded_file:
    text = extract_text(uploaded_file)
    st.text_area("Preview", text[:3000])

    if st.button("Summarize"):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": text}],
            max_tokens=250
        )
        st.success(response.choices[0].message.content)
