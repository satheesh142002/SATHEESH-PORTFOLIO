import streamlit as st
import base64
import PyPDF2
import os
import requests

# GitHub RAW file URL (replace with your latest raw file link)
GITHUB_PDF_URL = "https://raw.githubusercontent.com/satheesh142002/SATHEESH-PORTFOLIO/main/SATHEESH_KUMAR_K_RESUME.pdf"
DEFAULT_PDF_PATH = "SATHEESH_KUMAR_K_RESUME.pdf"

# Function to download PDF from GitHub
def download_pdf(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
    else:
        st.error("Failed to download resume. Please check the GitHub file URL.")

# Function to extract metadata (page numbers)
def get_pdf_metadata(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    return [f"Page {i+1}" for i in range(len(reader.pages))]

# Function to display PDF in Streamlit
def display_pdf(pdf_file):
    base64_pdf = base64.b64encode(pdf_file.read()).decode("utf-8")
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}#toolbar=0&navpanes=0&scrollbar=0" type="application/pdf" width="100%" height="1000px" />'
    st.markdown(pdf_display, unsafe_allow_html=True)

# Set page layout
st.set_page_config(layout="wide")
st.title("Satheesh Portfolio")

st.sidebar.title("Resume")

# Download PDF if it doesn't exist
if not os.path.exists(DEFAULT_PDF_PATH):
    st.info("Downloading resume file from GitHub...")
    download_pdf(GITHUB_PDF_URL, DEFAULT_PDF_PATH)

# Check if the PDF file exists after download
if os.path.isfile(DEFAULT_PDF_PATH):
    with open(DEFAULT_PDF_PATH, "rb") as default_file:
        page_list = get_pdf_metadata(default_file)
        st.sidebar.write("Select a page from the list:")
        st.sidebar.write("\n".join(page_list))
        display_pdf(default_file)
else:
    st.error("Resume file not found. Check if the file exists in your GitHub repository.")
