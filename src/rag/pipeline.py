import json
import os

from src.tools.router import route_query
from src.tools.appointment_tool import appointment_booking_tool
from src.memory.chat_memory import chat_history
from src.rag.prompt import SYSTEM_PROMPT

def healthcare_rag(query, db, llm):

    route = route_query(query)

    if route == "appointment":
        return appointment_booking_tool(query)

    retrieved_docs = db.similarity_search_with_score(query, k=4)

    if not retrieved_docs:

        return {
            "answer": "I could not find this information in the provided documents.",
            "confidence": "low",
            "sources": []
        }

    filtered_docs = []
    similarity_scores = []

    for doc, score in retrieved_docs:

        if score < 1.5:
            filtered_docs.append(doc)
            similarity_scores.append(score)

    if not filtered_docs:

        return {
            "answer": "I could not find this information in the provided documents.",
            "confidence": "low",
            "sources": []
        }

    context = "\n\n".join([doc.page_content for doc in filtered_docs])

    memory_context = "\n".join([
        f"{msg['role']}: {msg['content']}"
        for msg in chat_history
    ])

    final_prompt = f"""
    {SYSTEM_PROMPT}

    CHAT HISTORY:
    {memory_context}

    RETRIEVED CONTEXT:
    {context}

    USER QUESTION:
    {query}
    """

    response = llm.invoke(final_prompt)
    raw_output = response.content.strip()

    try:
        parsed_response = json.loads(raw_output)
        answer = parsed_response.get("answer", "Invalid response format.")
    except:
        answer = raw_output

    sources = [
        {"file": os.path.basename(doc.metadata.get("source", "unknown"))}
        for doc in filtered_docs
    ]

    avg_score = sum(similarity_scores) / len(similarity_scores)

    if avg_score < 0.5:
        confidence = "high"
    elif avg_score < 1.0:
        confidence = "medium"
    else:
        confidence = "low"

    chat_history.append({"role": "user", "content": query})
    chat_history.append({"role": "assistant", "content": answer})

    return {
        "answer": answer,
        "confidence": confidence,
        "sources": sources
    }