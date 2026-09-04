import streamlit as st
from pathlib import Path

from src.chunking.document_chunker import create_document_chunks
from src.embeddings.embedder import load_embedding_model, embed_texts
from src.vectorstore.chroma_store import create_vector_store
from src.pipeline.rag_pipeline import answer_question


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Multimodal RAG Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# --------------------------------------------------
# CUSTOM UI
# --------------------------------------------------

st.markdown(
    """
    <style>

    /* Main page */
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Header */
    .main-header {
        text-align: center;
        padding: 1rem 0 1.5rem 0;
    }

    .main-header h1 {
        font-size: 2.4rem;
        margin-bottom: 0.3rem;
    }

    .main-header p {
        color: #777;
        font-size: 1.05rem;
    }

    /* Upload card */
    .upload-card {
        padding: 1.2rem;
        border-radius: 14px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-bottom: 1.5rem;
    }

    /* Mobile */
    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 1rem;
        }

        .main-header h1 {
            font-size: 1.8rem;
        }

        .main-header p {
            font-size: 0.9rem;
        }

        [data-testid="stFileUploader"] {
            width: 100%;
        }

        [data-testid="stFileUploaderDropzone"] {
            width: 100%;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="main-header">
        <h1>🤖 Multimodal RAG Agent</h1>
        <p>
            Upload a document and ask questions about its contents.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "indexed_file" not in st.session_state:
    st.session_state.indexed_file = None


# --------------------------------------------------
# LOAD EMBEDDING MODEL
# --------------------------------------------------

@st.cache_resource
def get_embedding_model():
    return load_embedding_model()


embedding_model = get_embedding_model()


# --------------------------------------------------
# DOCUMENT UPLOAD
# --------------------------------------------------

st.markdown("### 📄 Upload your document")

st.caption(
    "Supported formats: PDF, DOCX and PPTX"
)

uploaded_file = st.file_uploader(
    "Choose a document",
    type=["pdf", "docx", "pptx"],
    label_visibility="collapsed"
)


# --------------------------------------------------
# PROCESS DOCUMENT
# --------------------------------------------------

if uploaded_file:

    upload_dir = Path("data/uploads")

    upload_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = upload_dir / uploaded_file.name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(
        f"📄 {uploaded_file.name} uploaded successfully"
    )


    # --------------------------------------------------
    # INDEX DOCUMENT
    # --------------------------------------------------

    if st.session_state.indexed_file != uploaded_file.name:

        with st.status(
            "Processing your document...",
            expanded=True
        ):

            # Create chunks
            st.write("📑 Extracting document content...")

            chunks = create_document_chunks(
                str(file_path)
            )

            # Create embeddings
            st.write("🧠 Creating embeddings...")

            texts = [
                chunk["text"]
                for chunk in chunks
            ]

            embeddings = embed_texts(
                texts,
                embedding_model
            )

            # Chroma collection
            st.write("🔎 Building vector index...")

            collection = create_vector_store()

            # Create unique IDs
            ids = [
                f"{uploaded_file.name}_{i}"
                for i in range(len(chunks))
            ]

            # Metadata
            metadatas = []

            for chunk in chunks:

                metadata = {
                    "source": chunk.get(
                        "source",
                        uploaded_file.name
                    ),
                    "type": chunk.get(
                        "type",
                        "text"
                    )
                }

                if "page" in chunk:
                    metadata["page"] = chunk["page"]

                if "slide" in chunk:
                    metadata["slide"] = chunk["slide"]

                if "image_number" in chunk:
                    metadata["image_number"] = (
                        chunk["image_number"]
                    )

                if "path" in chunk:
                    metadata["path"] = chunk["path"]

                metadatas.append(metadata)


            # Store in ChromaDB
            collection.add(
                ids=ids,
                documents=texts,
                embeddings=embeddings.tolist(),
                metadatas=metadatas
            )

            st.session_state.indexed_file = (
                uploaded_file.name
            )

        st.success(
            f"✅ Document indexed successfully — "
            f"{len(chunks)} chunks created."
        )

    else:

        st.info(
            "📚 This document is already indexed."
        )


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("⚙️ Settings")

    st.divider()

    st.markdown("### 📄 Current document")

    if st.session_state.indexed_file:

        st.success(
            st.session_state.indexed_file
        )

    else:

        st.info(
            "No document uploaded yet."
        )

    st.divider()

    if st.button(
        "🗑️ Clear conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# --------------------------------------------------
# CHAT SECTION
# --------------------------------------------------

st.markdown("### 💬 Chat with your document")


# --------------------------------------------------
# WELCOME MESSAGE
# --------------------------------------------------

if not st.session_state.messages:

    st.info(
        "👋 Upload a document above, then ask me "
        "anything about it."
    )

    st.markdown(
        """
        **Try asking:**

        - What is the main objective of this study?
        - What methodology did the authors use?
        - What datasets were used?
        - What are the main findings?
        - What are the limitations of the study?
        - How could this study be improved?
        """
    )


# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

question = st.chat_input(
    "Ask a question about your document..."
)


# --------------------------------------------------
# PROCESS QUESTION
# --------------------------------------------------

if question:

    # User message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)


    # AI response
    with st.chat_message("assistant"):

        with st.spinner(
            "🔎 Searching your document..."
        ):

            result = answer_question(
                question,
                top_k=5,
                chat_history=st.session_state.messages[:-1]
            )

            answer = result["answer"]

        st.markdown(answer)


    # Save AI response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )