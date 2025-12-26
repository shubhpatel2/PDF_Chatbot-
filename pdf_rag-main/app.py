import streamlit as st
import os
import tempfile
import sys

# Add current directory to path
sys.path.append(os.getcwd())

# -----------------------------------------------------------------------------
# IMPORT FUNCTIONS
# -----------------------------------------------------------------------------
try:
    from txt_extractor_from_pdf import extract_text_from_pdf 
except ImportError:
    st.error("Could not find 'txt_extractor_from_pdf.py'. Make sure it is in the same folder.")
    st.stop()

try:
    from pdf_rag import answer_query
except ImportError:
    st.error("Could not find 'pdf_rag.py'. Make sure it is in the same folder.")
    st.stop()

# -----------------------------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(page_title="PDF Chatbot", page_icon="📚", layout="centered")
st.title("📚 Chat with your PDF")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Upload a PDF file in the sidebar, and I'll answer questions based on it."}
    ]

if "document_text" not in st.session_state:
    st.session_state.document_text = None

# -----------------------------------------------------------------------------
# SIDEBAR (File Upload)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("📂 Document Upload")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        if st.button("Process PDF", type="primary"):
            with st.spinner("Analyzing document..."):
                
                # 1. Create a temp file for the PDF
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                    tmp_pdf.write(uploaded_file.getvalue())
                    tmp_pdf_path = tmp_pdf.name

                # 2. Create a temp file path for the OUTPUT text
                # We just generate a name, we don't need to create the file yet
                tmp_txt_path = tmp_pdf_path + ".txt"
                
                try:
                    # FIX: Pass BOTH arguments (PDF path and TXT path)
                    extract_text_from_pdf(tmp_pdf_path, tmp_txt_path)
                    
                    # 3. Read the text back from the file
                    if os.path.exists(tmp_txt_path):
                        with open(tmp_txt_path, "r", encoding="utf-8") as f:
                            extracted_text = f.read()
                        
                        st.session_state.document_text = extracted_text
                        st.success("✅ PDF Processed! Ready to chat.")
                    else:
                        st.error("Error: Text file was not created.")

                except Exception as e:
                    st.error(f"Error processing PDF: {e}")
                
                finally:
                    # Cleanup: Delete both temporary files
                    if os.path.exists(tmp_pdf_path):
                        os.remove(tmp_pdf_path)
                    if os.path.exists(tmp_txt_path):
                        os.remove(tmp_txt_path)

# -----------------------------------------------------------------------------
# MAIN CHAT INTERFACE
# -----------------------------------------------------------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user", avatar="👤").write(msg["content"])
    else:
        st.chat_message("assistant", avatar="🤖").write(msg["content"])

if prompt := st.chat_input("Ask a question about your PDF..."):
    
    if not st.session_state.document_text:
        st.error("Please upload and process a PDF in the sidebar first!")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="👤").write(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            try:
                # Call RAG function
                response = answer_query(st.session_state.document_text, prompt)
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"An error occurred: {e}")