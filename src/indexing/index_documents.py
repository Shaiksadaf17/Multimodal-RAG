from pathlib import Path

from src.chunking.document_chunker import create_document_chunks
from src.embeddings.embedder import (
    load_embedding_model,
    embed_texts
)
from src.vectorstore.chroma_store import (
    create_vector_store,
    add_documents
)


DATA_DIR = Path("data")


def index_document(file_path, model, collection):
    """
    Load, chunk, embed, and store one document.
    """

    print(f"\nProcessing: {file_path.name}")

    # 1. Create chunks
    chunks = create_document_chunks(file_path)

    print(f"Chunks created: {len(chunks)}")

    if not chunks:
        print("No chunks found.")
        return

    # 2. Get text from chunks
    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    # 3. Generate embeddings
    embeddings = embed_texts(
        texts,
        model
    )

    print(
        f"Embeddings created: {embeddings.shape}"
    )

    # 4. Store in ChromaDB
    add_documents(
        collection,
        chunks,
        embeddings
    )

    print(
        f"Stored {len(chunks)} chunks in ChromaDB."
    )


def main():

    print("Loading embedding model...")

    model = load_embedding_model()

    print("Creating ChromaDB collection...")

    collection = create_vector_store()

    files = list(DATA_DIR.glob("*.pdf"))
    files += list(DATA_DIR.glob("*.docx"))
    files += list(DATA_DIR.glob("*.pptx"))

    print(f"\nDocuments found: {len(files)}")

    for file_path in files:

        index_document(
            file_path,
            model,
            collection
        )

    print("\n==============================")
    print("INDEXING COMPLETE")
    print("==============================")
    print(
        "Total vectors:",
        collection.count()
    )


if __name__ == "__main__":
    main()