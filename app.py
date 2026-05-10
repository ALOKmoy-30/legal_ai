import streamlit as st
from pypdf import PdfReader
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Groq Client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Streamlit UI
st.set_page_config(page_title="LegalEase AI")

st.title("📄 LegalEase AI")
st.subheader("AI Contract Risk Analyzer")

uploaded_file = st.file_uploader(
    "Upload a legal contract PDF",
    type="pdf"
)

if uploaded_file:

    # Read PDF
    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    # Limit text size
    text = text[:5000]

    st.success("PDF uploaded successfully!")

    with st.spinner("Analyzing contract..."):

        prompt = f"""
        You are a legal assistant for freelancers and small businesses.

        Analyze this contract and provide:

        1. Plain English summary
        2. High-risk clauses
        3. Unfair terms
        4. Missing protections
        5. Risk score out of 10
        6. Whether the user should negotiate before signing

        Contract:
        {text}
        """

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Updated model
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        result = completion.choices[0].message.content

    st.subheader("📌 Analysis Result")

    st.write(result)