from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

from rag_streamlit.config import (
    CHROMA_DIR,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    COLLECTION_NAME,
    DOCS_DIR,
    EMBED_MODEL_NAME,
)


@dataclass
class Chunk:
    text: str
    source: str
    chunk_index: int


def _iter_docs(doc_dir: Path) -> Iterable[Path]:
    for path in sorted(doc_dir.glob("**/*")):
        if path.is_file() and path.suffix.lower() in {".pdf", ".txt", ".md"}:
            yield path


def _read_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        reader = PdfReader(str(path))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)
    return path.read_text(encoding="utf-8", errors="ignore")


def _chunk_text(text: str, source: str, size: int, overlap: int) -> List[Chunk]:
    text = " ".join(text.split())
    if not text:
        return []

    chunks: List[Chunk] = []
    start = 0
    idx = 0
    step = max(size - overlap, 1)

    while start < len(text):
        end = start + size
        piece = text[start:end].strip()
        if piece:
            chunks.append(Chunk(text=piece, source=source, chunk_index=idx))
            idx += 1
        start += step
    return chunks


def ingest_documents(
    doc_dir: Path = DOCS_DIR,
    chroma_dir: Path = CHROMA_DIR,
    collection_name: str = COLLECTION_NAME,
    model_name: str = EMBED_MODEL_NAME,
) -> dict:
    chroma_dir.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(chroma_dir))
    collection = client.get_or_create_collection(name=collection_name)

    model = SentenceTransformer(model_name)

    all_chunks: List[Chunk] = []
    docs_seen = 0

    for file_path in _iter_docs(doc_dir):
        docs_seen += 1
        raw_text = _read_text(file_path)
        all_chunks.extend(
            _chunk_text(
                text=raw_text,
                source=str(file_path.relative_to(doc_dir.parent)),
                size=CHUNK_SIZE,
                overlap=CHUNK_OVERLAP,
            )
        )

    if not all_chunks:
        return {"documents": docs_seen, "chunks": 0, "status": "No readable content found."}

    texts = [c.text for c in all_chunks]
    embeddings = model.encode(texts, normalize_embeddings=True).tolist()

    ids = [f"{c.source}::chunk::{c.chunk_index}" for c in all_chunks]
    metadatas = [{"source": c.source, "chunk_index": c.chunk_index} for c in all_chunks]

    collection.upsert(ids=ids, documents=texts, metadatas=metadatas, embeddings=embeddings)

    return {
        "documents": docs_seen,
        "chunks": len(all_chunks),
        "status": "Ingestion completed successfully.",
    }


if __name__ == "__main__":
    result = ingest_documents()
    print(result)
