import streamlit as st
import nltk
from PyPDF2 import PdfReader

# --- STEP 3 (Part 1): Load NLTK library and download resources ---
# We download 'punkt' and 'punkt_tab' to ensure the sentence tokenizer works in all environments.
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)

st.set_page_config(page_title="Q4: PDF Sentence Chunker", layout="wide")

st.title("Laboratory Test: Question 4")
st.markdown("### Text Chunking Web App using NLTK Sentence Tokenizer")

# --- STEP 1: Import the PDF file using the PdfReader module ---
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    try:
        # Initializing the PdfReader as required by Step 1 
        reader = PdfReader(uploaded_file)
        
        # --- STEP 2: Extract the textual content from the uploaded PDF file ---
        # We iterate through all pages and join them into one unstructured text block [cite: 129]
        pages_text = []
        for page in reader.pages:
            page_text = page.extract_text() or ""
            pages_text.append(page_text)
        
        full_text = " ".join(pages_text).strip()

        if not full_text:
            st.warning("No text could be extracted from this PDF.")
        else:
            # --- STEP 4: Apply NLTK's sentence tokenizer for semantic chunking ---
            # This splits the raw text into a list of meaningful sentences 
            sentences = nltk.sent_tokenize(full_text)
            
            st.success(f"Total semantic chunks (sentences) detected: {len(sentences)}")

            # --- STEP 3 (Part 2): Display a sample of extracted text for indices 58 to 68 ---
            # The instructions specifically require showing this range 
            st.subheader("Sample Extracted Text (Indices 58 to 68)")
            
            start_idx = 58
            end_idx = 68  # Inclusive per lab instructions
            
            if len(sentences) > start_idx:
                # We use end_idx + 1 because Python's range is exclusive at the end
                for i in range(start_idx, min(end_idx + 1, len(sentences))):
                    st.markdown(f"**Index {i}:** {sentences[i]}")
            else:
                st.info(f"The PDF contains {len(sentences)} sentences. Indices 58-68 are unavailable.")

            # Optional: Extra visualization for the user
            with st.expander("Show Full Raw Text (First 1000 characters)"):
                st.text(full_text[:1000])

    except Exception as e:
        st.error(f"Error reading PDF: {e}")
else:
    st.info("Please upload the lab question PDF (or any other PDF) to see the chunking in action.")
