def chunk_text(text, chunk_size=500, overlap=50):
    """
    Split text into overlapping chunks.

    Args:
        text: Input text.
        chunk_size: Maximum number of words per chunk.
        overlap: Number of words shared between consecutive chunks.

    Returns:
        List of text chunks.
    """

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk)

        if end >= len(words):
            break

        start = end - overlap

    return chunks