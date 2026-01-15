# 📚 Research Paper RAG Assistant

A professional Retrieval-Augmented Generation (RAG) system designed to interactively analyze and query research papers using **GROBID** for high-quality text extraction and **Groq's Gpt OSS 120b** for intelligent reasoning.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Required-blue?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Key Features

*   **📂 Multi-PDF Management**: Place multiple research papers in a dedicated `source/` directory.
*   **🤖 Interactive CLI**: Browses your library and lets you select which paper to analyze via a simple menu.
*   **🧠 Advanced Extraction**: Uses **GROBID** (GeneRation Of BIbliographic Data) to accurately parse PDF structures (titles, abstracts, sections) rather than just raw text.
*   **⚡ High-Speed Inference**: Powered by **Groq's LPU™ Inference Engine** running `llama-3.3-70b-versatile` for near-instant answers.
*   **🔍 Semantic Search**: Uses **FAISS** vector store and **HuggingFace** embeddings (`all-MiniLM-L6-v2`) for precise context retrieval.
*   **💾 Smart Caching**: Extracted data is cached in the `data/` folder, making subsequent queries on the same paper instant.

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

1.  **[Docker Desktop](https://www.docker.com/products/docker-desktop/)** (Required for GROBID service)
2.  **[Python 3.12+](https://www.python.org/downloads/)**
3.  **[Groq API Key](https://console.groq.com/keys)** (Free)

---

## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/RagSystem.git
cd RagSystem
```

### 2. Configure Environment
Create a `.env` file in the project root with your API key:
```bash
GROQ_API_KEY="your_groq_api_key_here"
```

### 3. Install Dependencies
```bash
# Recommended: Create a virtual environment first
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate # Mac/Linux

pip install -r requirements.txt
```

---

## 🏃 Usage Guide

### Step 1: Start the GROBID Service
This system relies on GROBID for PDF processing. You **must** have Docker running.

```bash
docker run -t --rm -p 8070:8070 lfoppiano/grobid:0.8.0
```
*Wait about 30 seconds for the service to fully initialize.*

### Step 2: Add Your Papers
Place your PDF files into the `source/` directory.
```text
RagSystem/
└── source/
    ├── attention_is_all_you_need.pdf
    ├── biology_research.pdf
    └── my_paper.pdf
```

### Step 3: Run the Assistant
```bash
python rag_cli.py
```

### Step 4: Interact
1.  **Select a Paper**: The tool will list all PDFs found in `source/`. Enter the corresponding number.
2.  **Ask Questions**: Once processed, type your questions in natural language.
    *   *"What is the main contribution of this paper?"*
    *   *"Summarize the methodology section."*
    *   *"Compare the results with the baseline."*
3.  **Exit**: Type `quit` or `exit` to stop.

---

## 🏗️ Project Architecture

```
RagSystem/
├── source/               # 📥 INPUT: Place your PDF files here
├── data/                 # 💾 CACHE: Extracted JSON data is stored here
├── rag_cli.py            # 🧠 MAIN: The core application logic
├── converter.py          # 🔄 UTILS: Handles communication with GROBID
├── check_system.py       # 🩺 DIAGNOSTIC: Checks system health
├── docker-compose.yml    # 🐳 DOCKER: Config for GROBID container
└── requirements.txt      # 📋 DEPS: Python dependencies
```

---

## ❓ Troubleshooting

### ❌ `ConnectionError: Cannot connect to GROBID server`
**Cause**: The Docker container is not running or hasn't started yet.
**Fix**:
1.  Open Docker Desktop.
2.  Run `docker-compose up -d` in your terminal.
3.  Verify it's running with `docker ps` (you should see `lfoppiano/grobid`).

### ❌ `ModuleNotFoundError`
**Cause**: Dependencies are missing.
**Fix**: Run `pip install -r requirements.txt`.

### ❌ Model Errors
**Cause**: Groq might have updated their models.
**Fix**: Check `rag_cli.py` and ensure `model_name` is set to a valid model ID (e.g., `llama-3.3-70b-versatile`).

---

## 📜 License

This project is open-source and available under the **MIT License**.
