# AI Chat RAG

A lightweight Retrieval-Augmented Generation (RAG) project built with Streamlit, ChromaDB, and sentence-transformer embeddings for querying internal documents.

## Overview

This project is designed to ingest local educational or internal knowledge documents, convert them into vector embeddings, store them in a persistent Chroma index, and provide a simple web interface for semantic search and context-grounded question answering.

The current implementation is intentionally simple and practical:
- Local document ingestion from the `docs/` folder
- PDF, Markdown, and text support
- Local embedding generation with Sentence Transformers
- Persistent vector storage with ChromaDB
- Streamlit user interface for indexing and retrieval
- Prompt and agent assets saved for reuse in the workspace

## Key Capabilities

- Ingests internal documents into a searchable vector index
- Splits long documents into retrieval-friendly chunks
- Retrieves the most relevant context for user questions
- Displays supporting source chunks with similarity scores
- Supports a clean local-first workflow without requiring a hosted embedding provider
- Includes placeholders for adding an external embedding API later

## Architecture

The application follows a simple RAG pipeline:

1. Documents are loaded from the `docs/` directory.
2. Supported files are parsed into raw text.
3. Text is chunked into overlapping segments.
4. Each chunk is embedded using a sentence-transformer model.
5. Embeddings and metadata are stored in a Chroma persistent collection.
6. A user query is embedded and matched against indexed chunks.
7. Top matching chunks are returned in the Streamlit interface.

## Project Structure

```text
.
|-- .github/
|   |-- agents/
|   `-- skills/
|-- docs/
|-- rag_streamlit/
|   |-- app.py
|   |-- config.py
|   |-- ingest.py
|   |-- rag_engine.py
|   `-- __init__.py
|-- reports/
|-- saved_prompts/
|-- scripts/
|-- .env.example
|-- .gitignore
|-- README.md
`-- requirements.txt
```

## Core Components

### Streamlit App
The main UI lives in `rag_streamlit/app.py`.

It provides:
- Folder configuration for documents and Chroma storage
- Reindex button for ingestion
- Indexed chunk metrics
- Interactive chat input for document Q&A
- Retrieved context with source references and scores

### Ingestion Layer
The ingestion workflow lives in `rag_streamlit/ingest.py`.

It is responsible for:
- Discovering supported files
- Extracting text from PDF, TXT, and Markdown files
- Chunking content with overlap
- Generating embeddings
- Upserting vectors into ChromaDB

### Retrieval Layer
The retrieval logic lives in `rag_streamlit/rag_engine.py`.

It is responsible for:
- Loading the persistent Chroma collection
- Embedding the user query
- Querying top matching chunks
- Returning a response bundle with answer text and supporting contexts

## Technology Stack

- Python
- Streamlit
- ChromaDB
- sentence-transformers
- PyPDF
- NumPy

## Installation

Create and activate a Python environment, then install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Default configuration is defined in `rag_streamlit/config.py`.

Current defaults include:
- Local docs directory: `docs/`
- Local Chroma persistence directory: `.chroma/`
- Embedding model: `sentence-transformers/all-MiniLM-L6-v2`
- Chunk size: `900`
- Chunk overlap: `150`
- Retrieval top-k: `4`

Optional environment template:

```env
# input your API Embeding pls
EMBEDDING_PROVIDER=local
EMBEDDING_API_KEY=
```

At the moment, the app uses local embeddings by default. The API placeholder is included so the project can be extended later with a hosted embedding service.

## Usage

### 1. Ingest Documents

Run ingestion directly:

```bash
python -m rag_streamlit.ingest
```

Or use the Streamlit UI and click `Ingest / Reindex`.

### 2. Start the App

```bash
streamlit run rag_streamlit/app.py
```

### 3. Ask Questions

Open the local Streamlit URL in your browser and ask questions about the indexed documents.

## Input Documents

The current repository already includes source files in `docs/`:
- `Lesson number_1.pptx.pdf`
- `Lesson number_2.pptx.pdf`

These are indexed automatically when ingestion is run against the default docs directory.

## Prompt and Agent Assets

This repository also contains reusable workspace assets under:
- `.github/agents/`
- `.github/skills/`
- `saved_prompts/`

These files capture custom agent and skill prompts created during the project setup, including:
- Stock analysis agent prompt
- Knowledge retrieval agent prompt
- Surf-trade decision skill
- Friendly education explainer skill

## Current Limitations

- The response layer is retrieval-first and does not yet use a full generative LLM answer synthesis step
- Embeddings are local by default; hosted embedding APIs are not yet integrated
- The stock analysis automation scripts currently use placeholder market data unless extended with live data sources
- No deployment pipeline is configured yet

## Recommended Next Steps

- Add an LLM generation layer on top of retrieved context
- Support OpenAI or another hosted embedding provider
- Add document metadata filters and collection management
- Add a production deployment target for Streamlit
- Improve source citation formatting in the answer layer

## Repository Goal

This repository is intended to serve as a practical starting point for:
- internal knowledge retrieval systems
- educational content search tools
- lightweight document Q&A applications
- local-first RAG experimentation

## License

No license file has been added yet. Add one if you plan to distribute the project publicly.
