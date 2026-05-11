APPOINTMENTS_DB = {
    "cardiology": {"doctor": "Dr. Sarah Johnson", "available_slots": {"monday": ["10:00 AM", "2:00 PM"], "tuesday": ["11:00 AM"]}},
    "neurology": {"doctor": "Dr. Michael Chen", "available_slots": {"wednesday": ["1:00 PM", "4:00 PM"]}},
    "orthopedics": {"doctor": "Dr. Emily Davis", "available_slots": {"friday": ["9:00 AM"]}}
}

def appointment_booking_tool(query):
    query_lower = query.lower()
    dept = next((d for d in APPOINTMENTS_DB if d in query_lower), None)
    day = next((day for day in ["monday", "tuesday", "wednesday", "thursday", "friday"] if day in query_lower), None)

    if not dept:
        return {"answer": "Please specify a department (Cardiology, Neurology, or Orthopedics).", "confidence": "low", "sources": ["appointment_system"]}

    data = APPOINTMENTS_DB[dept]
    if day:
        slots = data["available_slots"].get(day, [])
        if slots:
            ans = f"{data['doctor']} has {dept} slots on {day.title()} at: {', '.join(slots)}"
            return {"answer": ans, "confidence": "high", "sources": ["appointment_system"]}
        return {"answer": f"No slots for {dept} on {day.title()}.", "confidence": "medium", "sources": ["appointment_system"]}
    
    days = ", ".join([d.title() for d in data["available_slots"].keys()])
    return {"answer": f"{data['doctor']} is available on: {days}", "confidence": "medium", "sources": ["appointment_system"]}