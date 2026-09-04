from src.ingestion.document_loader import load_document


files = [
    "data/test.pdf",
    "data/test.docx",
    "data/test.pptx",
]


for file_path in files:

    print("\n==============================")
    print("Testing:", file_path)
    print("==============================")

    document = load_document(file_path)

    print("Loaded successfully.")
    print("Type:", type(document).__name__)

    if isinstance(document, list):
        print("Number of items:", len(document))