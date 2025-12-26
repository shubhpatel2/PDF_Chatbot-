import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

# 1. Load Environment Variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    # Fallback/Warning if key is missing
    print("⚠️ Warning: GROQ_API_KEY is missing from .env file")

# 2. Initialize Models (Global Scope for efficiency)
# We load these once so we don't reload them for every question
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
llm = ChatGroq(model_name="llama-3.1-8b-instant", api_key=api_key)

def answer_query(document_text, question):
    """
    This function takes the text extracted from a PDF and a user question,
    builds a RAG pipeline on the fly, and returns the answer.
    """
    
    if not document_text:
        return "No document text found. Please upload a PDF first."

    # Step 3: Split the text into chunks
    # We use a slightly smaller chunk size for better granularity
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([document_text])

    if not chunks:
        return "The document appears to be empty or could not be processed."

    # Step 4: Create FAISS vector store from chunks
    # Note: For very large PDFs, this might take a few seconds
    vectorstore = FAISS.from_documents(chunks, embedding_model)
    
    # Step 5: Create the Retriever
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})

    # Step 6: Define the Prompt Template
    prompt_template = PromptTemplate(
        template="""
        You are a helpful assistant.
        Answer the question based ONLY on the provided context below.
        If the context is insufficient, just say you don't know. Do not make up answers.

        Context:
        {context}

        Question: 
        {question}
        """,
        input_variables=['context', 'question']
    )

    # Step 7: Define the Chain
    # This connects: Retriever -> Format Docs -> Prompt -> LLM -> Output Parser
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt_template
        | llm
        | StrOutputParser()
    )

    # Step 8: Run the chain
    try:
        response = rag_chain.invoke(question)
        return response
    except Exception as e:
        return f"Error during processing: {str(e)}"

# This allows you to test the script independently if you run `python pdf_rag.py`
if __name__ == "__main__":
    # Test with dummy text
    sample_text = "The Segment Anything Model (SAM) is a new AI model from Meta AI."
    sample_q = "What is SAM?"
    print(answer_query(sample_text, sample_q))