import streamlit as st
import nltk
from PyPDF2 import PdfReader

# Step 3 (Partial): Ensure NLTK punkt is available for tokenization
nltk.download("punkt", quiet=True)

st.set_page_config(page_title="Q4: PDF Sentence Chunker", layout="wide")
st.title("Question 4: Semantic Text Chunking Web App")

# Step 1: File Uploader using PyPDF2's PdfReader
uploaded_file = st.file_uploader("Step 1: Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    try:
        # Step 1: Import the PDF file using PdfReader
        reader = PdfReader(uploaded_file)
        
        # Step 2: Extract textual content from the uploaded PDF
        pages_text = []
        for page in reader.pages:
            page_text = page.extract_text() or ""
            pages_text.append(page_text)
        full_text = " ".join(pages_text).strip()

        if not full_text:
            st.warning("No text could be extracted from this PDF.")
        else:
            # Step 4: Apply NLTK's sentence tokenizer (Semantic Chunking)
            sentences = nltk.sent_tokenize(full_text)
            
            st.success(f"Total sentences detected: {len(sentences)}")

            # Step 3: Display a sample of the extracted text for indices 58 to 68
            st.subheader("Step 3: Extracted Sentences (Indices 58 to 68)")
            
            # Boundary check to ensure indices exist
            start_idx, end_idx = 58, 69 # 69 is exclusive to include index 68
            
            if len(sentences) > start_idx:
                # Iterate through the specific requested range
                for i in range(start_idx, min(end_idx, len(sentences))):
                    st.markdown(f"**Sentence {i}**: {sentences[i]}")
            else:
                st.info(f"The PDF only has {len(sentences)} sentences. Indices 58-68 are out of range.")

            # Optional: Original dynamic controls from your code
            with st.expander("View custom range of sentences"):
                custom_start = st.number_input("Start index", 0, len(sentences)-1, 0)
                custom_end = st.number_input("End index", custom_start+1, len(sentences), min(custom_start+10, len(sentences)))
                for j in range(custom_start, custom_end):
                    st.write(f"{j}: {sentences[j]}")

    except Exception as e:
        st.error(f"Error processing PDF: {e}")
else:
    st.info("Please upload a PDF to proceed with Question 4.")
