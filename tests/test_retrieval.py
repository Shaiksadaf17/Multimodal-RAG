from src.retrieval.retriever import retrieve_documents


results = retrieve_documents(
    "What datasets were used in the ECG study?",
    top_k=5
)

print("=" * 40)
print("RETRIEVAL TEST")
print("=" * 40)

print("Results:", len(results))

for i, result in enumerate(results, start=1):

    print(f"\n--- Result {i} ---")

    print("Page:", result["metadata"].get("page"))
    print("Distance:", result["distance"])

    print("Text:")
    print(result["text"][:500])