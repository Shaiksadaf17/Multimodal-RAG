from src.extraction.pdf_images import extract_images_from_pdf


pdf_path = "data/test.pdf"

images = extract_images_from_pdf(pdf_path)

print(f"Number of images extracted: {len(images)}")

for image in images:
    print(image)