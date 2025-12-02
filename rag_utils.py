import os
import json
from docx import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document as LCDoc

def docx_to_text(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

def load_and_process_corpus(corpus_dir="data/corpus"):
    docs = []
    files = [f for f in os.listdir(corpus_dir) if f.endswith(".docx")]
    en_files = [f for f in files if not f.endswith(".tr.docx")]
    for en_file in en_files:
        tr_file = en_file.replace(".docx", ".tr.docx")
        if tr_file in files:
            en_text = docx_to_text(os.path.join(corpus_dir, en_file))
            tr_text = docx_to_text(os.path.join(corpus_dir, tr_file))
            metadata = {"id": en_file.replace(".docx", ""), "length_type": "short" if len(en_text.split()) <= 50 else "long"}
            docs.append(LCDoc(page_content=f"İngilizce: {en_text}\nTürkçe: {tr_text}", metadata=metadata))
    return docs

def setup_vectorstore(corpus_dir="data/corpus", persist_dir="chroma_db"):
    docs = load_and_process_corpus(corpus_dir)
    embedding = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(docs, embedding, persist_directory=persist_dir)
    vectorstore.persist()
    return vectorstore

def retrieve_context(query: str, length_type: str, top_k=3):
    embedding = OpenAIEmbeddings()
    vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embedding)
    results = vectorstore.similarity_search(query, k=top_k)
    if length_type == "short":
        return [r.page_content for r in results if r.metadata.get("length_type") == "short"]
    else:
        return [r.page_content for r in results]
    