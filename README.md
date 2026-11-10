📚 Smart PDF Question Answering System

Project Overview

Smart PDF Question Answering System is an AI-powered web application developed using Streamlit, LangChain, ChromaDB, and Ollama.

The application allows users to upload PDF documents, ask questions, retrieve relevant information, and receive AI-generated answers based on the uploaded documents.

Objectives

- Develop an interactive LLM web application using Streamlit.
- Upload and process multiple PDF documents.
- Extract and split PDF text into smaller chunks.
- Store document embeddings using ChromaDB.
- Retrieve relevant information using semantic search.
- Generate answers using the Gemma3:1b model through Ollama.
- Display conversation history and response generation time.

Technologies Used

- Python 3.10
- Streamlit
- LangChain
- ChromaDB
- Sentence Transformers
- Hugging Face Embeddings
- Ollama
- Gemma3:1b
- PyPDF

Project Structure

Streamlit_LLM_App/
│
├── dataset/
│   ├── sample.pdf
│   ├── queries.csv
│   ├── answers.csv
│   └── uploaded_files/
│
├── chroma_db/
│
├── assets/
│   └── screenshots/
│
├── app.py
├── pdf_qa.py
├── README.md
├── requirements.txt
└── venv/

Features

1. Interactive Streamlit web interface.
2. Multiple PDF document upload.
3. PDF-only file selection.
4. Automatic PDF text extraction.
5. Text chunking and embedding generation.
6. ChromaDB vector storage.
7. Semantic search and document retrieval.
8. AI-powered question answering using Ollama.
9. PDF selection and switching.
10. Conversation history.
11. Clear Chat History option.
12. Retrieved relevant chunks display.
13. Response generation time calculation.

Installation and Setup

Step 1: Create Virtual Environment

python -m venv venv

Step 2: Activate Virtual Environment

Windows PowerShell:

.\venv\Scripts\Activate.ps1

Step 3: Install Dependencies

python -m pip install -r requirements.txt

Step 4: Install and Start Ollama

Make sure Ollama is installed and the Gemma3:1b model is available.

ollama pull gemma3:1b

Step 5: Run the Application

streamlit run app.py

The application will open in the web browser.

How to Use

1. Run the Streamlit application.
2. Upload one or more PDF documents.
3. Select the required PDF.
4. Enter a question related to the document.
5. Click Submit Question.
6. View the AI-generated answer.
7. Explore the retrieved relevant chunks.
8. Check response generation time.
9. Clear previous conversations using Clear Chat History.

Conclusion

The Smart PDF Question Answering System provides an interactive way to retrieve information from PDF documents using Large Language Models and Retrieval-Augmented Generation (RAG).

This project demonstrates the integration of Streamlit, LangChain, ChromaDB, Sentence Transformers, and Ollama to build an AI-powered document question-answering application.

Author

Developed as part of the LLM Application Development coursework.