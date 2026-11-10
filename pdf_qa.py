import re
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


def create_vector_store(chunks, pdf_name):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    collection_name = re.sub(
        r"[^a-zA-Z0-9_-]",
        "_",
        pdf_name
    )[:50]

    vector_store = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory="chroma_db"
    )

    return vector_store


def generate_answer(context, question):

    llm = OllamaLLM(
        model="gemma3:1b",
        temperature=0
    )

    prompt = ChatPromptTemplate.from_template("""
    Answer the question using only the context given below.

    If the answer is not available in the context, say:
    The answer is not available in the PDF.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """)

    formatted_prompt = prompt.format(
        context=context,
        question=question
    )

    answer = llm.invoke(formatted_prompt)

    return answer