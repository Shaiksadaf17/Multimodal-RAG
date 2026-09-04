import pymupdf
from pathlib import Path


def render_pdf_pages(pdf_path, output_dir="data/rendered_pages"):
    """
    Render every PDF page as a PNG image.
    """

    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    document = pymupdf.open(pdf_path)

    rendered_pages = []

    for page_number, page in enumerate(document, start=1):

        # Render page at 2x resolution
        matrix = pymupdf.Matrix(2, 2)
        pixmap = page.get_pixmap(matrix=matrix, alpha=False)

        image_filename = f"page_{page_number}.png"
        image_path = output_dir / image_filename

        pixmap.save(str(image_path))

        rendered_pages.append({
            "page": page_number,
            "path": str(image_path)
        })

    document.close()

    return rendered_pages