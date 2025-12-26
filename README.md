#PDF RAG Chatbot
A simple and efficient Chatbot that uses Retrieval-Augmented Generation (RAG) to answer questions based on your uploaded PDF files. It uses the Groq API for lightning-fast responses.

✨ Features
PDF Upload: Upload any PDF document to chat with it.

Smart Retrieval: Only looks at the relevant parts of the PDF to answer your question.

Fast Inference: Powered by Groq for near-instant AI responses.

Ensemble Logic: Uses a custom MLP and LightGBM approach for processing predictions.

🛠️ Requirements
Python 3.8+

A Groq API Key

🚀 Quick Start
Clone the project:

Bash

git clone https://github.com/yourusername/pdf-rag-chatbot.git
cd pdf-rag-chatbot
Install dependencies:

Bash

pip install -r requirements.txt
Add your API Key: Create a file named .env and add:

Code snippet

GROQ_API_KEY=your_key_here
Run the app:

Bash

python main.py
📂 Project Structure
main.py: The entry point of the application.

models/: Contains the MLP and LightGBM ensemble logic.

utils/: Functions for PDF processing and text chunking.
