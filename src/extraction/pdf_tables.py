import pymupdf
from pathlib import Path


def extract_tables_from_pdf(pdf_path):
    """
    Detect and extract tables from a PDF.
    """

    pdf_path = Path(pdf_path)

    document = pymupdf.open(pdf_path)

    extracted_tables = []

    for page_number, page in enumerate(document, start=1):

        table_finder = page.find_tables()

        for table_number, table in enumerate(
            table_finder.tables,
            start=1
        ):

            extracted_tables.append({
                "page": page_number,
                "table_number": table_number,
                "data": table.extract()
            })

    document.close()

    return extracted_tables