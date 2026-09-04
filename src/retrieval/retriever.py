from pathlib import Path

from src.embeddings.embedder import load_embedding_model, embed_texts
from src.vectorstore.chroma_store import create_vector_store


def retrieve_documents(query, top_k=5):
    """
    Retrieve the most relevant document chunks from ChromaDB.
    """

    # Load embedding model
    model = load_embedding_model()

    # Create/load ChromaDB collection
    collection = create_vector_store()

    # Convert user query into an embedding
    query_embedding = embed_texts(
        [query],
        model
    )

    # Search ChromaDB
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k
    )

    retrieved_documents = []

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        retrieved_documents.append({
            "text": document,
            "metadata": metadata,
            "distance": distance
        })

    return retrieved_documents