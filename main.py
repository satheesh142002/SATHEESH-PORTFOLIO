import streamlit as st
import os
import requests
import pdfplumber
import numpy as np
import google.generativeai as genai
from sentence_transformers import SentenceTransformer

# Set up page configuration
st.set_page_config(page_title="🤖 Satheesh's Resume Chatbot", layout="wide", initial_sidebar_state="expanded")

# --- CONFIGURATION ---
GITHUB_PDF_URL = "https://raw.githubusercontent.com/satheesh142002/SATHEESH-PORTFOLIO/main/SATHEESH_KUMAR_K_RESUME.pdf"
DEFAULT_PDF_PATH = "SATHEESH_KUMAR_K_RESUME.pdf"

# Secure API Key Retrieval
GENAI_API_KEY = os.getenv("GENAI_API_KEY", st.secrets.get("GENAI_API_KEY", ""))
if not GENAI_API_KEY:
    st.error("❌ Google Gemini API Key Missing! Set it in .streamlit/secrets.toml or as an environment variable.")
    st.stop()

# Configure Gemini AI
genai.configure(api_key=GENAI_API_KEY)
available_models = [m.name for m in genai.list_models()]
MODEL_NAME = "models/gemini-1.5-pro" if "models/gemini-1.5-pro" in available_models else available_models[0]

# --- FUNCTIONS ---
def download_pdf(url, save_path):
    """Downloads a PDF from a URL."""
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        return True
    return False

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            text += extracted + "\n" if extracted else ""
    return text.strip()

def chunk_text(text, chunk_size=300):
    """Splits text into smaller chunks."""
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def cosine_similarity(query_embedding, stored_embeddings):
    """Computes cosine similarity between query and stored embeddings."""
    return [np.dot(query_embedding, emb) / (np.linalg.norm(query_embedding) * np.linalg.norm(emb)) for emb in stored_embeddings]

def retrieve_relevant_text(query, model, chunks, chunk_embeddings):
    """Retrieves the most relevant text chunk based on query."""
    query_embedding = model.encode(query)
    similarities = cosine_similarity(query_embedding, chunk_embeddings)
    top_indices = np.argsort(similarities)[::-1][:3]
    return [chunks[i] for i in top_indices]

SYSTEM_PROMPT = """You are an AI chatbot answering questions about Satheesh Kumar K's resume. If a question is out of scope, politely decline."""

def generate_response(user_query, model, chunks, chunk_embeddings):
    """Generates a response using Gemini AI."""
    retrieved_docs = retrieve_relevant_text(user_query, model, chunks, chunk_embeddings)
    prompt = f"{SYSTEM_PROMPT}\n\nContext:\n{retrieved_docs}\n\nUser Query: {user_query}\nAnswer:"
    
    try:
        gemini_model = genai.GenerativeModel(MODEL_NAME)
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Error generating response: {str(e)}"

# --- CHATBOT PAGE ---
st.title("🤖 Satheesh's Resume Chatbot")

# Load and process the resume
model = SentenceTransformer("all-MiniLM-L6-v2")
if not os.path.exists(DEFAULT_PDF_PATH):
    st.info("Downloading resume from GitHub...")
    if not download_pdf(GITHUB_PDF_URL, DEFAULT_PDF_PATH):
        st.error("Failed to download resume.")
        st.stop()

text_data = extract_text_from_pdf(DEFAULT_PDF_PATH)
chunks = chunk_text(text_data)
chunk_embeddings = [model.encode(chunk) for chunk in chunks]

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message("user" if message["is_user"] else "assistant"):
        st.markdown(message["content"])

# User Input
user_query = st.chat_input("Ask anything about my resume")
if user_query:
    # Append user message
    st.session_state.messages.append({"content": user_query, "is_user": True})

    # Generate response
    response = generate_response(user_query, model, chunks, chunk_embeddings)

    # Append response message
    st.session_state.messages.append({"content": response, "is_user": False})

    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(response)
