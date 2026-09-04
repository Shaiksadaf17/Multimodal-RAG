from src.ingestion.pptx_loader import load_pptx


file_path = "data/test.pptx"

presentation = load_pptx(file_path)

print("Document type:", presentation["type"])

print("\nNumber of slides:", len(presentation["slides"]))

for slide in presentation["slides"]:

    print("\n==============================")
    print("Slide:", slide["slide"])
    print("==============================")

    print("\nText:")
    for text in slide["text"]:
        print(text)

    print("\nTables:", len(slide["tables"]))

    for table in slide["tables"]:
        for row in table:
            print(row)

    print("\nImages:", len(slide["images"]))

    for image in slide["images"]:
        print(image)