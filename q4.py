import streamlit as st
import nltk
from nltk.tokenize import sent_tokenize
from PyPDF2 import PdfReader

# ============================ #
# Page Setup #
# ============================ #
st.set_page_config(
    page_title="Sentence Chunking with NLTK",
    layout="wide"
)

st.title("Text Chunking Web App (NLTK Sentence Tokenizer)")
st.caption("Extract and chunk sentences semantically from PDF text")

# Ensure that the 'punkt' tokenizer is downloaded before using it
nltk.download('punkt')

# ============================ #
# Step 1: PDF File Upload #
# ============================ #
uploaded_file = st.file_uploader("Upload your PDF document", type=["pdf"])

if uploaded_file is not None:

    # ============================ #
    # Step 2: Extract Text from PDF #
    # ============================ #
    pdf_reader = PdfReader(uploaded_file)
    document_text = ""

    for page in pdf_reader.pages:
        document_text += page.extract_text()

    # ============================ #
    # Step 3: Sentence Tokenization #
    # ============================ #
    tokenized_sentences = sent_tokenize(document_text)

    st.subheader("🧩 Sample Extracted Sentences (Index 58–68)")

    if len(tokenized_sentences) >= 69:
        sample = tokenized_sentences[58:69]

        for idx, sentence in enumerate(sample, start=58):
            st.write(f"Sentence {idx}: {sentence}")
    else:
        st.warning("The document does not contain enough sentences to display the sample.")

    # ============================ #
    # Step 4: Sentence Chunking #
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
