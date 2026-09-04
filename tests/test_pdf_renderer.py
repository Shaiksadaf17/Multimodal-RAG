from src.extraction.pdf_renderer import render_pdf_pages


pdf_path = "data/test.pdf"

pages = render_pdf_pages(pdf_path)

print(f"Number of pages rendered: {len(pages)}")

for page in pages:
    print(page)
    