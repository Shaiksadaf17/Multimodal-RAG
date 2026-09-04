import pymupdf
from pathlib import Path


def extract_images_from_pdf(pdf_path, output_dir="data/extracted_images"):
    """
    Extract all embedded images from a PDF.
    """

    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    document = pymupdf.open(pdf_path)

    extracted_images = []

    for page_number, page in enumerate(document, start=1):

        images = page.get_images(full=True)

        for image_number, image in enumerate(images, start=1):

            xref = image[0]

            image_data = document.extract_image(xref)

            image_bytes = image_data["image"]
            image_extension = image_data["ext"]

            image_filename = (
                f"page_{page_number}_image_{image_number}.{image_extension}"
            )

            image_path = output_dir / image_filename

            with open(image_path, "wb") as image_file:
                image_file.write(image_bytes)

            extracted_images.append({
                "page": page_number,
                "image_number": image_number,
                "path": str(image_path)
            })

    document.close()

    return extracted_images
