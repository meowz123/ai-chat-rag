from __future__ import annotations

from pathlib import Path

import streamlit as st

from rag_streamlit.config import CHROMA_DIR, DOCS_DIR, TOP_K
from rag_streamlit.ingest import ingest_documents
from rag_streamlit.rag_engine import RAGEngine


st.set_page_config(page_title="Simple RAG (Chroma + Streamlit)", layout="wide")
st.title("Simple RAG Knowledge Retrieval")
st.caption("Ingest local docs, index with Chroma, and query via semantic retrieval.")

with st.sidebar:
    st.subheader("Settings")
    docs_path = st.text_input("Docs folder", value=str(DOCS_DIR))
    chroma_path = st.text_input("Chroma folder", value=str(CHROMA_DIR))
    top_k = st.slider("Top K context chunks", min_value=1, max_value=10, value=TOP_K)

    if st.button("Ingest / Reindex", type="primary"):
        with st.spinner("Indexing documents..."):
            stats = ingest_documents(doc_dir=Path(docs_path), chroma_dir=Path(chroma_path))
        st.success(stats.get("status", "Done"))
        st.write(f"Documents: {stats.get('documents', 0)}")
        st.write(f"Chunks: {stats.get('chunks', 0)}")

engine = RAGEngine(chroma_dir=Path(chroma_path))
index_stats = engine.stats()

c1, c2 = st.columns(2)
c1.metric("Indexed Chunks", index_stats.get("chunks", 0))
c2.metric("Top-K", top_k)

query = st.chat_input("Ask questions about your ingested documents...")
if query:
    with st.spinner("Retrieving context..."):
        response = engine.ask(query, top_k=top_k)

    st.subheader("Answer")
    st.write(response["answer"])

    st.subheader("Retrieved Context")
    for idx, ctx in enumerate(response["contexts"], start=1):
        score = f"{ctx['score']:.4f}" if ctx["score"] is not None else "N/A"
        st.markdown(
            f"**{idx}. Source:** `{ctx['source']}` | **Chunk:** {ctx['chunk_index']} | "
            f"**Score:** {score}"
        )
        st.write(ctx["text"])
        st.divider()
