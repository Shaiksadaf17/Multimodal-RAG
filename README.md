# 🤖 Multimodal RAG Agent

<div align="center">

### Upload documents. Ask questions. Retrieve context. Get grounded answers.

A multimodal **Retrieval-Augmented Generation (RAG)** application that allows users to upload **PDF, DOCX, and PPTX documents** and interact with their contents using natural language.

<br>

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-FF6F00?style=for-the-badge)
![Sentence Transformers](https://img.shields.io/badge/Sentence_Transformers-Embeddings-00A67E?style=for-the-badge)
![Gemini](https://img.shields.io/badge/Google_Gemini-LLM-4285F4?style=for-the-badge&logo=google&logoColor=white)

</div>

---

## ✨ Overview

**Multimodal RAG Agent** is a document question-answering application built using a **Retrieval-Augmented Generation pipeline**.

The system allows users to upload research papers, theses, reports, presentations, and other supported documents and ask questions about their contents.

Instead of searching through a large document manually, the application retrieves the most relevant information and provides it as context to a Large Language Model (LLM).

The system is designed to work with multiple document formats:

- 📄 PDF
- 📝 DOCX
- 📊 PPTX

The main goal is to generate answers that are **grounded in the uploaded document** rather than relying only on the LLM's general knowledge.

---

## 🚀 Key Features

- 📄 **Multi-format document upload**
- 🔎 **Semantic similarity search**
- 🧠 **Sentence Transformer embeddings**
- 🗃️ **ChromaDB vector storage**
- 🤖 **Google Gemini LLM integration**
- 🖼️ **Multimodal document processing**
- 📊 **Table and image-aware document handling**
- 💬 **Conversational document Q&A**
- 🧪 **Automated testing**
- ☁️ **Streamlit deployment**

---

## 🔄 How It Works

```text
                    📄 Document
                PDF / DOCX / PPTX
                         │
                         ▼
              ┌────────────────────┐
              │ Document Processing │
              └──────────┬─────────┘
                         │
                         ▼
              ┌────────────────────┐
              │ Text / Tables /    │
              │ Images / Content   │
              └──────────┬─────────┘
                         │
                         ▼
              ┌────────────────────┐
              │     Chunking       │
              │  Document Content  │
              └──────────┬─────────┘
                         │
                         ▼
              ┌────────────────────┐
              │    Embeddings      │
              │ Sentence           │
              │ Transformers       │
              └──────────┬─────────┘
                         │
                         ▼
              ┌────────────────────┐
              │      ChromaDB      │
              │    Vector Store    │
              └──────────┬─────────┘
                         │
                         │
                  💬 User Question
                         │
                         ▼
              ┌────────────────────┐
              │ Semantic Retrieval │
              │    Top-K Chunks    │
              └──────────┬─────────┘
                         │
                         ▼
              ┌────────────────────┐
              │   Google Gemini    │
              │        LLM         │
              └──────────┬─────────┘
                         │
                         ▼
                    🤖 Answer
🧠 RAG Pipeline

The application follows the standard Retrieval-Augmented Generation workflow.

1. 📤 Document Upload

The user uploads a supported document through the Streamlit interface.

PDF
DOCX
PPTX
2. 📑 Document Extraction

The application processes the uploaded document and extracts the available information.

For PDF documents, PyMuPDF is used for document processing.

DOCX and PPTX files are processed using their respective Python libraries.

The pipeline can work with document content such as:

Text
Tables
Images
Figures
Structured content
3. ✂️ Chunking

Large documents are divided into smaller pieces called chunks.

This makes the document easier to search and allows the retrieval system to identify the specific sections relevant to a user's question.

Large Document
       │
       ▼
 ┌─────────────┐
 │   Chunk 1   │
 │   Chunk 2   │
 │   Chunk 3   │
 │     ...     │
 │   Chunk N   │
 └─────────────┘
4. 🧠 Embedding Generation

Each document chunk is converted into a numerical vector using Sentence Transformers.

These embeddings represent the semantic meaning of the text.

For example:

"What datasets were used?"
          │
          ▼
   Embedding Model
          │
          ▼
[0.21, -0.43, 0.72, ...]

The user's question is converted into an embedding using the same process.

5. 🗃️ Vector Storage

The generated embeddings are stored in ChromaDB.

ChromaDB acts as the vector store used by the application to efficiently search for semantically similar document chunks.

Document Chunks
       │
       ▼
   Embeddings
       │
       ▼
   ChromaDB
       │
       ▼
Vector Similarity Search
6. 🔎 Retrieval

When the user asks a question, the system searches the vector database for the most relevant chunks.

For example:

User Question
      │
      ▼
Question Embedding
      │
      ▼
ChromaDB Search
      │
      ▼
Top-K Relevant Chunks

Only the most relevant context is passed to the language model.

7. 🤖 Answer Generation

The retrieved document context and the user's question are passed to Google Gemini.

Gemini generates the final answer based on the retrieved context.

Question
    +
Retrieved Context
    │
    ▼
Google Gemini
    │
    ▼
Grounded Answer
🛠️ Technologies Used
Technology	Purpose
🐍 Python	Core programming language
🎈 Streamlit	Interactive web application
📄 PyMuPDF	PDF processing and extraction
📝 python-docx	DOCX document processing
📊 python-pptx	PPTX document processing
🖼️ Pillow	Image processing
🧠 Sentence Transformers	Semantic text embeddings
🗃️ ChromaDB	Vector database
🤖 Google Gemini	LLM-based answer generation
🔗 google-genai	Gemini API integration
🔥 PyTorch	Deep-learning backend
🖼️ Torchvision	Vision-related dependencies
🌱 python-dotenv	Environment variable management
🧪 Pytest	Testing
🌿 Git & GitHub	Version control
☁️ Streamlit Community Cloud	Deployment
📁 Project Structure
Multimodal-RAG/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│
├── src/
│   │
│   ├── embeddings/
│   │   └── embedder.py
│   │
│   ├── generation/
│   │   └── gemini_client.py
│   │
│   ├── pipeline/
│   │   └── rag_pipeline.py
│   │
│   ├── retrieval/
│   │   └── retriever.py
│   │
│   └── vectorstore/
│       └── chroma_store.py
│
└── tests/
    ├── test_document_loader.py
    ├── test_docx_loader.py
    ├── test_pdf_images.py
    ├── test_pdf_renderer.py
    ├── test_pdf_tables.py
    ├── test_pptx_loader.py
    └── test_retrieval.py
💬 Example Questions

After uploading a document, users can ask questions such as:

What is the main objective of this study?

What datasets were used?

What preprocessing techniques were applied?

Explain the proposed methodology.

Why did the authors choose this model architecture?

What are the main contributions of this study?

What were the main experimental results?

What are the limitations of the study?

How could the proposed approach be improved?

This makes the application particularly useful for:

🎓 Thesis analysis
📚 Research-paper analysis
🔬 Literature review
🧪 Research methodology analysis
📊 Technical reports
🎤 Viva preparation
🔐 Environment Variables

The Gemini API key is stored as an environment variable and should never be committed to GitHub.

For local development:

$env:GEMINI_API_KEY="YOUR_API_KEY"

For Streamlit deployment, the API key should be added using Streamlit Secrets.

💻 Run Locally

Clone the repository:

git clone https://github.com/Shaiksadaf17/Multimodal-RAG.git
cd Multimodal-RAG

Create a virtual environment:

python -m venv .venv_multimodal

Activate it:

.\.venv_multimodal\Scripts\Activate.ps1

Install the dependencies:

pip install -r requirements.txt

Set the Gemini API key:

$env:GEMINI_API_KEY="YOUR_API_KEY"

Run the application:

streamlit run app.py
☁️ Deployment

The application can be deployed using Streamlit Community Cloud.

GitHub Repository
        │
        ▼
Streamlit Community Cloud
        │
        ▼
Install requirements.txt
        │
        ▼
Configure GEMINI_API_KEY
        │
        ▼
      🚀 Deploy

The application is then accessible through a public Streamlit URL.

🌟 Future Improvements
📚 Multi-document RAG
💬 Improved conversation memory
📍 Page-level source citations
📊 Improved table understanding
🖼️ Advanced figure and image retrieval
🔎 Hybrid keyword + semantic search
🧠 Retrieval reranking
🏠 Local LLM support using Ollama
👨‍💻 Author
Shaik Sadaf Patel

MSc Artificial Intelligence
