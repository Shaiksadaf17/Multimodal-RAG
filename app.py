import streamlit as st
from pathlib import Path
import shutil

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
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🤖 Multimodal RAG Agent")

st.write(
    "Upload a PDF, DOCX, or PPTX and chat with your document."
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
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("📄 Document")

    uploaded_file = st.file_uploader(
        "Upload your document",
        type=["pdf", "docx", "pptx"]
    )

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
            f"Uploaded: {uploaded_file.name}"
        )

        # Avoid indexing the same file repeatedly
        if st.session_state.indexed_file != uploaded_file.name:

            with st.spinner(
                "Processing document..."
            ):

                # Create chunks
                chunks = create_document_chunks(
                    str(file_path)
                )

                # Create embeddings
                texts = [
                    chunk["text"]
                    for chunk in chunks
                ]

                embeddings = embed_texts(
                    texts,
                    embedding_model
                )

                # Chroma collection
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
                        metadata["image_number"] = chunk[
                            "image_number"
                        ]

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
                f"Indexed {len(chunks)} chunks."
            )

    st.divider()

    if st.button("🗑️ Clear conversation"):

        st.session_state.messages = []

        st.rerun()


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
    "Ask something about your document..."
)


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
            "Thinking..."
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