import os
import io
import time
import streamlit as st
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pdf_qa import create_vector_store, generate_answer

st.set_page_config(
    page_title="Smart PDF Assistant",
    page_icon="📚",
    layout="wide"
)

# Sidebar
st.sidebar.title("📚 PDF Assistant")
st.sidebar.write("Your AI-powered PDF Question Answering System")
st.sidebar.divider()
st.sidebar.subheader("About")
st.sidebar.info(
    "Upload multiple PDF documents and ask questions. "
    "You can switch between uploaded PDFs."
)

# Main Title
st.title("📚 Smart PDF Question Answering System")
st.caption("Powered by Streamlit, LangChain, ChromaDB and Ollama")

# Initialize Session State
if "vector_stores" not in st.session_state:
    st.session_state.vector_stores = {}

if "pdf_information" not in st.session_state:
    st.session_state.pdf_information = {}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Multiple PDF Uploader
uploaded_files = st.file_uploader(
    "Choose PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    os.makedirs("dataset/uploaded_files", exist_ok=True)

    for uploaded_file in uploaded_files:

        pdf_name = uploaded_file.name

        if pdf_name not in st.session_state.vector_stores:

            try:
                reader = PdfReader(
                    io.BytesIO(uploaded_file.getvalue())
                )

                text = ""

                for page in reader.pages:
                    page_text = page.extract_text()

                    if page_text:
                        text += page_text + "\n"

                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=500,
                    chunk_overlap=100
                )

                chunks = text_splitter.split_text(text)

                if not chunks:
                    st.warning(
                        f"No readable text found in {pdf_name}."
                    )
                    continue

                # Save Uploaded PDF
                file_path = os.path.join(
                    "dataset/uploaded_files",
                    pdf_name
                )

                with open(file_path, "wb") as file:
                    file.write(uploaded_file.getvalue())

                # Create Vector Store
                vector_store = create_vector_store(
                    chunks,
                    pdf_name
                )

                st.session_state.vector_stores[pdf_name] = vector_store

                st.session_state.pdf_information[pdf_name] = {
                    "pages": len(reader.pages),
                    "chunks": len(chunks)
                }

            except Exception as e:
                st.error(f"Unable to process {pdf_name}: {e}")

    # Show Uploaded PDFs
    available_pdfs = list(
        st.session_state.vector_stores.keys()
    )

    if available_pdfs:

        st.success(
            f"{len(available_pdfs)} PDF document(s) ready!"
        )

        st.subheader("Select a PDF")

        selected_pdf = st.selectbox(
            "Switch between uploaded PDF documents:",
            available_pdfs
        )

        # Selected PDF Information
        pdf_info = st.session_state.pdf_information[selected_pdf]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("PDF File", selected_pdf)

        with col2:
            st.metric("Total Pages", pdf_info["pages"])

        with col3:
            st.metric("Total Chunks", pdf_info["chunks"])

        # Clear Chat History
        st.subheader("Chat History")

        if st.button("🗑️ Clear Chat History"):

            st.session_state.chat_history = []
            st.success("Chat history cleared successfully!")
            st.rerun()

        # Display Previous Conversations
        if st.session_state.chat_history:

            for chat in st.session_state.chat_history:

                st.write("**You:**")
                st.write(chat["question"])

                st.write("**AI Assistant:**")
                st.write(chat["answer"])

                st.divider()

        else:
            st.info("No chat history available.")

        # Ask Question
        st.subheader("Ask Your Question")

        question = st.text_input(
            "Enter your question:",
            key="question_input"
        )

        if st.button("Submit Question"):

            if question.strip():

                vector_store = st.session_state.vector_stores[
                    selected_pdf
                ]

                results = vector_store.similarity_search(
                    question,
                    k=5
                )

                context = "\n\n".join(
                    document.page_content
                    for document in results
                )

                # Calculate Response Generation Time
                start_time = time.time()

                with st.spinner("Generating answer..."):

                    answer = generate_answer(
                        context,
                        question
                    )

                end_time = time.time()

                response_time = end_time - start_time

                # Save Conversation
                st.session_state.chat_history.append({
                    "question": question,
                    "answer": answer
                })

                st.subheader("Generated Answer")
                st.write(answer)

                st.metric(
                    "Response Generation Time",
                    f"{response_time:.2f} seconds"
                )

                st.subheader("Retrieved Relevant Chunks")

                for i, document in enumerate(results, start=1):

                    st.write(f"Chunk {i}")
                    st.write(document.page_content)

            else:
                st.warning("Please enter a question.")

else:
    st.info("Please upload one or more PDF files to get started.")