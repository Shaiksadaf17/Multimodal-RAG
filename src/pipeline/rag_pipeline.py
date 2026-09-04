from src.retrieval.retriever import retrieve_documents
from src.generation.gemini_client import generate_answer


def answer_question(question, top_k=5, chat_history=None):

    # Retrieve relevant document chunks
    results = retrieve_documents(
        question,
        top_k=top_k
    )

    # Build context
    context_parts = []

    for result in results:

        text = result.get("text", "").strip()

        if text:
            context_parts.append(text)

    context = "\n\n".join(context_parts)

    # Build conversation history
    history_text = ""

    if chat_history:

        history_text = "\n\nPrevious conversation:\n"

        for message in chat_history:

            role = message["role"]
            content = message["content"]

            history_text += f"{role}: {content}\n"

    # Generate answer
    answer = generate_answer(
        question,
        context + history_text
    )

    return {
        "answer": answer,
        "results": results
    }