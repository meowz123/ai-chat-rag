from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import chromadb
from sentence_transformers import SentenceTransformer

from rag_streamlit.config import CHROMA_DIR, COLLECTION_NAME, EMBED_MODEL_NAME, TOP_K


class RAGEngine:
    def __init__(
        self,
        chroma_dir: Path = CHROMA_DIR,
        collection_name: str = COLLECTION_NAME,
        model_name: str = EMBED_MODEL_NAME,
    ) -> None:
        self._client = chromadb.PersistentClient(path=str(chroma_dir))
        self._collection = self._client.get_or_create_collection(name=collection_name)
        self._model = SentenceTransformer(model_name)

    def stats(self) -> Dict[str, int]:
        count = self._collection.count()
        return {"chunks": count}

    def ask(self, query: str, top_k: int = TOP_K) -> Dict[str, object]:
        q_emb = self._model.encode([query], normalize_embeddings=True).tolist()[0]
        result = self._collection.query(query_embeddings=[q_emb], n_results=top_k)

        docs = result.get("documents", [[]])[0]
        metas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]

        contexts: List[Dict[str, object]] = []
        for doc, meta, dist in zip(docs, metas, distances):
            contexts.append(
                {
                    "text": doc,
                    "source": meta.get("source", "unknown"),
                    "chunk_index": meta.get("chunk_index", -1),
                    "score": float(1 - dist) if dist is not None else None,
                }
            )

        if not contexts:
            return {
                "answer": "I could not find relevant content in the indexed documents.",
                "contexts": [],
            }

        snippets = [c["text"][:350] for c in contexts]
        answer = (
            "Based on the indexed documents, here are the most relevant points:\n\n- "
            + "\n- ".join(snippets)
        )

        return {"answer": answer, "contexts": contexts}
