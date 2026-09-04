import chromadb


def create_vector_store(
    collection_name="multimodal_documents",
    persist_directory="data/chroma"
):
    """
    Create or load a local ChromaDB collection.
    """

    client = chromadb.PersistentClient(
        path=persist_directory
    )

    collection = client.get_or_create_collection(
        name=collection_name
    )

    return collection


def add_documents(
    collection,
    chunks,
    embeddings
):
    """
    Add document chunks and their embeddings
    to ChromaDB.
    """

    documents = []
    ids = []
    metadatas = []

    for index, chunk in enumerate(chunks):

        documents.append(chunk["text"])

        ids.append(
            f"{chunk['source']}_{index}"
        )

        metadata = {
            "source": chunk["source"],
            "type": chunk["type"]
        }

        if "page" in chunk:
            metadata["page"] = chunk["page"]

        if "slide" in chunk:
            metadata["slide"] = chunk["slide"]

        if "image_number" in chunk:
            metadata["image_number"] = chunk["image_number"]

        if "path" in chunk:
            metadata["path"] = chunk["path"]

        metadatas.append(metadata)

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )


def search_documents(
    collection,
    query_embedding,
    n_results=5
):
    """
    Search the vector store using a query embedding.
    """

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=n_results
    )

    return results