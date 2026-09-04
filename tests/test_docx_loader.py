from src.ingestion.docx_loader import load_docx


file_path = "data/test.docx"

document = load_docx(file_path)

print("Document type:", document["type"])

print("\nParagraphs:")
for paragraph in document["paragraphs"]:
    print(paragraph)

print("\nNumber of tables:", len(document["tables"]))

for table in document["tables"]:
    print("\nTable:", table["table_number"])

    for row in table["data"]:
        print(row)

print("\nNumber of images:", len(document["images"]))

for image in document["images"]:
    print(image)