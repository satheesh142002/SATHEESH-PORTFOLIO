import streamlit as st
import base64
import PyPDF2

def get_pdf_metadata(pdf_file):
    with open(pdf_file, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        return [f"Page {i+1}" for i in range(len(reader.pages))]

def display_pdf(pdf_file):
    with open(pdf_file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}#toolbar=0&navpanes=0&scrollbar=0" type="application/pdf" width="100%" height="1000px" />'
    st.markdown(pdf_display, unsafe_allow_html=True)

st.set_page_config(layout="wide")
st.title("Satheesh Portfolio")

pdf_path = "SATHEESH_KUMAR_K_RESUME.pdf"
page_list = get_pdf_metadata(pdf_path)

display_pdf(pdf_path)
