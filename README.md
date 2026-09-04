# 🤖 Multimodal RAG Agent

> An intelligent document-question answering system that allows users to upload **PDF, DOCX, and PPTX documents** and interact with them through a conversational AI interface.

The system combines **document processing, semantic search, vector databases, multimodal document understanding, and LLM-based generation** to retrieve relevant information from uploaded documents and generate grounded answers.

---

## ✨ Overview

**Multimodal RAG Agent** is a Retrieval-Augmented Generation (RAG) application designed to let users communicate with their own documents using natural language.

Instead of manually searching through a long research paper, thesis, report, or presentation, the user can upload the document and ask questions such as:

- What is the main objective of this study?
- What datasets were used?
- Why did the authors choose this model architecture?
- What preprocessing techniques were applied?
- What are the main limitations of the study?
- What were the experimental results?
- How could the proposed approach be improved?

The application retrieves relevant content from the uploaded document and provides it to the language model as context before generating the answer.

The project is particularly designed to handle **multimodal research documents**, where useful information may appear in:

- Text
- Tables
- Figures
- Images
- Captions
- Structured document content

---

## 🧠 Architecture

```text
                    ┌──────────────────────┐
                    │       User           │
                    │  Upload + Question   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Streamlit UI      │
                    └──────────┬───────────┘
                               │
                               ▼
              ┌─────────────────────────────────┐
              │       Document Processing       │
              │                                 │
              │ PDF │ DOCX │ PPTX               │
              └────────────────┬────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Text / Image / Table │
                    │     Extraction       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Chunking          │
                    │  + Text Processing    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Sentence Transformers│
                    │     Embeddings        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      ChromaDB        │
                    │    Vector Store      │
                    └──────────┬───────────┘
                               │
                         User Question
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Semantic Retrieval   │
                    │     Top-K Chunks      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Gemini LLM        │
                    │ Answer Generation    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Grounded Response   │
                    │      to User         │
                    └──────────────────────┘
