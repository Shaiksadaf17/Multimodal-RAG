from sentence_transformers import SentenceTransformer


# Local embedding model
MODEL_NAME = "all-MiniLM-L6-v2"


def load_embedding_model():
    """
    Load the local Sentence Transformer embedding model.
    """
    return SentenceTransformer(MODEL_NAME)


def embed_texts(texts, model=None):
    """
    Convert a list of texts into embedding vectors.
    """

    if model is None:
        model = load_embedding_model()

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=False
    )

    return embeddings