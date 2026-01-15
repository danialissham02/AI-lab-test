import streamlit as st
import nltk
import os
from nltk.tokenize import sent_tokenize
from PyPDF2 import PdfReader

# ============================ #
# Page Setup #
# ============================ #
st.set_page_config(
    page_title="Text Chunking with NLTK",
    layout="wide"
)

# Custom Title Styling
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Text Chunking Web App</h1>", unsafe_allow_html=True)
st.caption("Extract and chunk sentences semantically from PDF text using NLTK")

# ============================ #
# NLTK Setup for Streamlit #
# ============================ #
# Set NLTK data path to the temporary directory
nltk_data_path = '/tmp/nltk_data'
if not os.path.exists(nltk_data_path):
    os.makedirs(nltk_data_path)

nltk.data.path.append(nltk_data_path)

# Download both 'punkt' and 'punkt_tab' to ensure compatibility
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt', download_dir=nltk_data_path)
    nltk.download('punkt_tab', download_dir=nltk_data_path)

# ============================ #
# Step 1: PDF File Upload #
# ============================ #
st.sidebar.header("Upload Your PDF Document")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:

    # ============================ #
    # Step 2: Extract Text from PDF #
    # ============================ #
    pdf_reader = PdfReader(uploaded_file)
    document_text = ""

    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            document_text += extracted + " "

    # ============================ #
    # Step 3: Sentence Tokenization #
    # ============================ #
    if document_text.strip():
        tokenized_sentences = sent_tokenize(document_text)

        st.subheader("Sample Extracted Sentences (Index 58–68)")

        if len(tokenized_sentences) >= 69:
            sample = tokenized_sentences[58:69]
            for idx, sentence in enumerate(sample, start=58):
                st.write(f"**Sentence {idx}:** {sentence}")
        else:
            st.warning(f"The document only contains {len(tokenized_sentences)} sentences. Not enough to show the 58-68 range.")

        # ============================ #
        # Step 4: Sentence Chunking Output #
        # ============================ #
        st.subheader("🔍 Semantic Sentence Chunking Output")

        chunk_data = {
            "Sentence Index": list(range(len(tokenized_sentences))),
            "Sentence": tokenized_sentences
        }

        st.dataframe(chunk_data, use_container_width=True)

        st.info(
            "NLTK's sentence tokenizer segments unstructured text into meaningful, "
            "sentence-level chunks that can be further analyzed for semantics."
        )
    else:
        st.error("Could not extract any text from this PDF. It might be an image-only scan.")

# ============================ #
# Additional Section for Instructions #
# ============================ #
with st.expander("How it works"):
    st.write("""
        - **Upload**: You can upload any PDF document to be processed by the app.
        - **Extract**: The app extracts the text from the PDF.
        - **Tokenization**: The text is broken down into individual sentences using the NLTK sentence tokenizer.
        - **Chunking**: The sentences are displayed along with their index, and the process is ready for further semantic analysis.
    """)
