# Promtior RAG Challenge

## Project Overview
This project implements a **Retrieval-Augmented Generation (RAG)** assistant designed to answer questions about Promtior's services, history, and clients. 

The solution is built using **LangChain** for the orchestration logic and **LangServe** (FastAPI) to expose the chain as a production-ready REST API. It ingests data from two sources:
1. **Public Website:** `https://promtior.ai/` and subpages (Fetched at startup).
2. **Internal Documentation:** `Promtior_Presentation.pdf` (Loaded for enhanced context).

### Key Features
* **Hybrid Data Ingestion:** Combines web content loading with local document loading.
* **Vector Search:** Uses **ChromaDB** with OpenAI Embeddings for semantic retrieval.
* **Production Ready:** Deployed via LangServe with built-in playground and documentation.
* **Scalable Structure:** Modular code organization separating ingestion logic from server configuration.

## Architecture
The system follows a standard RAG pipeline:
1. **Ingest:** Documents are loaded, split, and embedded into ChromaDB.
2. **Retrieve:** User questions trigger a similarity search in the vector store.
3. **Generate:** Retrieved context + question are sent to GPT-3.5-turbo.

![Architecture Diagram](doc/architecture_diagram.png)

## How to Run Locally

### Prerequisites
* Python 3.11+
* OpenAI API Key

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/santrodriguez21/promtior-challenge.git