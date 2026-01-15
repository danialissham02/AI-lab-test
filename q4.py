import streamlit as st
import nltk
from nltk.tokenize import sent_tokenize
from PyPDF2 import PdfReader

# ============================ #
# Streamlit Page Setup
# ============================ #
st.set_page_config(page_title="PDF Sentence Chunking", layout="wide")
st.title("Text Chunking from PDF using NLTK")
st.caption("Extract sentences from your PDF using NLTK's sentence tokenizer")

# ============================ #
# NLTK Setup for Streamlit
# ============================ #
# Ensure punkt is available for sentence tokenization
nltk.download('punkt', quiet=True)

# ============================ #
# PDF File Upload
# ============================ #
uploaded_file = st.file_uploader("Upload your PDF document", type=["pdf"])

if uploaded_file is not None:
    try:
        # Extract text from PDF
        pdf_reader = PdfReader(uploaded_file)
        document_text = ""
        for page in pdf_reader.pages:
            document_text += page.extract_text() or ""  # Extract text from each page

        # Check if any text was extracted
        if not document_text.strip():
            st.warning("No readable text found in this PDF.")
        else:
            st.success("Text extracted successfully!")
            st.subheader("Extracted Text Sample (first 500 characters)")
            st.write(document_text[:500])  # Show the first 500 characters

            # ============================ #
            # Sentence Tokenization
            # ============================ #
            sentences = sent_tokenize(document_text)
            st.subheader(f"Total Sentences: {len(sentences)}")

            # Control to show a specific range of sentences
            start_idx = st.number_input("Show sentences starting from index", min_value=0, max_value=max(len(sentences) - 1, 0), value=0, step=1)
            end_idx = st.number_input("Show sentences up to index (exclusive)", min_value=start_idx + 1, max_value=len(sentences), value=min(start_idx + 10, len(sentences)), step=1)

            st.subheader(f"Displaying Sentences [{start_idx} - {end_idx}]")
            for idx in range(start_idx, end_idx):
                st.write(f"**Sentence {idx}:** {sentences[idx]}")

            # ============================ #
            # Optional: Raw Extracted Text
            # ============================ #
            with st.expander("Show full extracted text (first 2000 characters)"):
                st.text(document_text[:2000])

    except Exception as e:
        st.error(f"Error processing PDF: {e}")
else:
    st.info("Please upload a PDF document to start.")
