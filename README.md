# Multimodal Question Answering – Research Repository

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Status](https://img.shields.io/badge/Status-Research-orange)
![License](https://img.shields.io/badge/License-MIT-green)

This repository contains **research experiments for building a Multimodal Question Answering (QA) system** capable of understanding information from **documents, tables, and images**.

The goal of this project is to explore different components required for a multimodal QA pipeline rather than delivering a finalized production system.
Each collaborator worked on a different module of the system.

---

# Project Goal

The objective of this research is to investigate how information from multiple modalities can be combined to answer questions from research documents.

The system explores three main capabilities:

* Extracting text and layout information from document images
* Retrieving knowledge from research papers using Retrieval-Augmented Generation (RAG)
* Understanding visual information from images

These components together form the foundation for a **Multimodal Question Answering pipeline**.

---

# Contributors & Work Distribution

This repository is a **collaborative research effort**.

### OCR & Document Understanding

Explores text extraction and document structure analysis.

Technologies explored:

* PaddleOCR
* PaddleOCR-VL
* Camelot (table extraction)

Focus areas:

* OCR text detection
* Table structure reconstruction
* Document layout understanding

Branch: `ocr-experiments`

---

### Research Paper RAG Assistant

A Retrieval-Augmented Generation system designed to analyze research papers.

Key capabilities:

* Multi-PDF document processing
* Semantic search using vector embeddings
* Interactive CLI for asking questions about papers
* Fast inference using Groq models
* Structured extraction using GROBID

Technologies used:

* FAISS vector database
* HuggingFace embeddings
* GROBID PDF parser
* Groq LLM inference

Branch: `Rag-System`

---

### Image Understanding Module

This module focuses on analyzing visual content within documents.

Planned capabilities include:

* Image feature extraction
* Visual content interpretation
* Integration with document QA pipeline

This module is currently under development and will be added soon.

---

# System Concept (High Level)

Document / Research Paper / Image -> Information Extraction

**OCR Pipeline:** 
 Text + Table + Layout Extraction

**RAG Pipeline:** 
 Semantic Retrieval + LLM Reasoning

**Image Analysis:** 
 Visual Understanding

---

# Repository Structure

```
multimodal-question-answering
│
├── ocr-experiments/      # OCR research using PaddleOCR & Camelot
├── rag-system/           # Research paper RAG assistant
├── image-module/         # Image understanding experiments (coming soon)
├── README.md
```

---

# Current Status

This repository represents **research exploration and experimentation** toward a multimodal QA system.

Implemented components include:

* OCR-based document text extraction
* Table detection and filtering
* Research paper question answering using RAG

Additional work on **image understanding** will be integrated in future updates.

---

# Technologies Explored

Python
PaddleOCR
Camelot
FAISS
HuggingFace Embeddings
GROBID
Groq LLM Inference
Docker

---

# Future Work

* Integrate OCR results into the RAG pipeline
* Combine text, tables, and image understanding
* Build an end-to-end multimodal QA system
* Evaluate performance across research documents

---

# Why This Repository Exists

This project was created to **experiment with modern document intelligence and multimodal AI techniques**.

It serves as:

* a research exploration
* a learning project
* a demonstration of applied AI components for recruiters and collaborators.

---

## Contributors

| Name | Contribution |
|-----|-----|
| [Koushiki Chakraborty](https://github.com/Koushiki-Chakraborty) | OCR experiments (PaddleOCR, PaddleOCR-VL, Camelot) |
| [Ayan Mazumdar](https://github.com/ayanmazumdar) | Research Paper RAG Assistant |
| [Bristi Kundu](https://github.com/Bristi12-bk) | Image understanding experiments |

---

# License

This project is open-source and available under the MIT License.
