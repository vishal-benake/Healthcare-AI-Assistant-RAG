from src.db.appointments_db import appointments_db

def appointment_booking_tool(query):

    query_lower = query.lower()

    departments = ["cardiology", "neurology", "orthopedics"]

    days = ["monday", "tuesday", "wednesday", "thursday", "friday"]

    detected_department = None
    detected_day = None

    for dept in departments:
        if dept in query_lower:
            detected_department = dept
            break

    for day in days:
        if day in query_lower:
            detected_day = day
            break

    if not detected_department:

        return {
            "answer": "Please specify a department such as cardiology, neurology, or orthopedics.",
            "confidence": "low",
            "sources": ["appointment_system"]
        }

    dept_data = appointments_db.get(detected_department, {})
    doctor_name = dept_data.get("doctor", "Unknown Doctor")
    available_slots = dept_data.get("available_slots", {})

    if detected_day:

        slots = available_slots.get(detected_day, [])

        if slots:

            return {
                "answer": f"{doctor_name} has available {detected_department} appointments on {detected_day.title()} at: " + ", ".join(slots),
                "confidence": "high",
                "sources": ["appointment_system"]
            }

        else:

            return {
                "answer": f"No appointment slots are available for {detected_department} on {detected_day.title()}.",
                "confidence": "medium",
                "sources": ["appointment_system"]
            }

    available_days = list(available_slots.keys())

    return {
        "answer": f"{doctor_name} is available for {detected_department} appointments on: " + ", ".join(day.title() for day in available_days),
        "confidence": "medium",
        "sources": ["appointment_system"]
    }