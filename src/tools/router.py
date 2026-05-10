def route_query(query):

    query_lower = query.lower()

    appointment_keywords = [
        "appointment", "book", "schedule",
        "doctor", "slot", "consultation"
    ]

    if any(k in query_lower for k in appointment_keywords):
        return "appointment"

    return "rag"