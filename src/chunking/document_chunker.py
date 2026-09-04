from pathlib import Path

from src.ingestion.document_loader import load_document
from src.chunking.text_chunker import chunk_text


def create_document_chunks(file_path, chunk_size=500, overlap=50):
    """
    Load a document and convert its content into searchable chunks.

    Supports:
    - PDF text
    - PDF tables
    - PDF images
    - DOCX text
    - PPTX text
    """

    file_path = Path(file_path)

    document = load_document(file_path)

    chunks = []

    document_type = document["type"]

    # =========================================================
    # PDF
    # =========================================================

    if document_type == "pdf":

        # -----------------------------------------------------
        # 1. TEXT CHUNKS
        # -----------------------------------------------------

        for page in document["pages"]:

            page_chunks = chunk_text(
                page["text"],
                chunk_size=chunk_size,
                overlap=overlap
            )

            for chunk_number, text in enumerate(
                page_chunks,
                start=1
            ):

                chunks.append({
                    "text": text,
                    "source": file_path.name,
                    "type": "text",
                    "page": page["page"],
                    "chunk": chunk_number
                })

        # -----------------------------------------------------
        # 2. TABLE CHUNKS
        # -----------------------------------------------------

        for table in document["tables"]:

            table_data = table["data"]

            table_text = "\n".join(
                " | ".join(
                    str(cell) if cell is not None else ""
                    for cell in row
                )
                for row in table_data
            )

            if table_text.strip():

                chunks.append({
                    "text": table_text,
                    "source": file_path.name,
                    "type": "table",
                    "page": table["page"],
                    "table_number": table["table_number"]
                })

        # -----------------------------------------------------
        # 3. IMAGE CHUNKS
        # -----------------------------------------------------

        for image in document["images"]:

            chunks.append({
                "text": "",
                "source": file_path.name,
                "type": "image",
                "page": image["page"],
                "image_number": image["image_number"],
                "path": image["path"]
            })

    # =========================================================
    # DOCX
    # =========================================================

    elif document_type == "docx":

        full_text = "\n".join(
            document["paragraphs"]
        )

        text_chunks = chunk_text(
            full_text,
            chunk_size=chunk_size,
            overlap=overlap
        )

        for chunk_number, text in enumerate(
            text_chunks,
            start=1
        ):

            chunks.append({
                "text": text,
                "source": file_path.name,
                "type": "text",
                "chunk": chunk_number
            })

    # =========================================================
    # PPTX
    # =========================================================

    elif document_type == "pptx":

        for slide in document["slides"]:

            slide_chunks = chunk_text(
                slide["text"],
                chunk_size=chunk_size,
                overlap=overlap
            )

            for chunk_number, text in enumerate(
                slide_chunks,
                start=1
            ):

                chunks.append({
                    "text": text,
                    "source": file_path.name,
                    "type": "text",
                    "slide": slide["slide"],
                    "chunk": chunk_number
                })

    # =========================================================
    # RETURN
    # =========================================================

    return chunks