from src.extraction.pdf_tables import extract_tables_from_pdf


pdf_path = "data/test.pdf"

tables = extract_tables_from_pdf(pdf_path)

print(f"Number of tables extracted: {len(tables)}")

for table in tables:

    print("\n==============================")
    print(f"Page: {table['page']}")
    print(f"Table: {table['table_number']}")
    print("==============================")

    for row in table["data"]:
        print(row)