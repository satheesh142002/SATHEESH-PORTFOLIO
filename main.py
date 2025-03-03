import streamlit as st
import os
import requests

# Correct GitHub Raw URL for PDF
GITHUB_PDF_URL = "https://raw.githubusercontent.com/satheesh142002/SATHEESH-PORTFOLIO/main/SATHEESH_KUMAR_K_RESUME.pdf"
DEFAULT_PDF_PATH = "SATHEESH_KUMAR_K_RESUME.pdf"

# Function to download PDF from GitHub
def download_pdf(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        return True
    else:
        return False

# Set Streamlit page configuration
st.set_page_config(layout="wide")
st.title("Satheesh Portfolio")

st.sidebar.title("Resume")

# Download the PDF if it doesn’t exist
if not os.path.exists(DEFAULT_PDF_PATH):
    st.info("Downloading resume from GitHub...")
    if not download_pdf(GITHUB_PDF_URL, DEFAULT_PDF_PATH):
        st.error("Failed to download resume. Check the GitHub raw file URL.")
        st.stop()

# Display the PDF using an iframe with pdf.js
st.write("### My Resume")
pdf_viewer_url = f"https://mozilla.github.io/pdf.js/web/viewer.html?file={GITHUB_PDF_URL}#zoom=page-width"
st.markdown(f'<iframe src="{pdf_viewer_url}" width="100%" height="1000px"></iframe>', unsafe_allow_html=True)
