import streamlit as st
import base64
import PyPDF2
import os

def get_pdf_metadata(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    return [f"Page {i+1}" for i in range(len(reader.pages))]

def display_pdf(pdf_file):
    base64_pdf = base64.b64encode(pdf_file.read()).decode("utf-8")
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}#toolbar=0&navpanes=0&scrollbar=0" type="application/pdf" width="100%" height="1000px" />'
    st.markdown(pdf_display, unsafe_allow_html=True)

st.set_page_config(layout="wide")
st.title("Satheesh Portfolio")

st.sidebar.title("Resume")
DEFAULT_PDF_PATH = "SATHEESH_KUMAR_K_RESUME.pdf"

# Ensure the PDF file exists before attempting to read it
if os.path.isfile(DEFAULT_PDF_PATH):
    with open(DEFAULT_PDF_PATH, "rb") as default_file:
        page_list = get_pdf_metadata(default_file)
        st.sidebar.write("Select a page from the list:")
        st.sidebar.write("\n".join(page_list))
        display_pdf(default_file)
else:
    st.error("Default resume file not found. Please check that it's in your GitHub repository and redeploy.")
