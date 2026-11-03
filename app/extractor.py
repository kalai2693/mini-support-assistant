
import requests
from pydantic import ValidationError
from app.models import TicketInfo


def extract_ticket(ticket_text):
    prompt = f"""
Extract the support ticket into JSON.

Required fields:
- customer_name
- product
- issue_type
- urgency (integer from 1 to 5)
- summary

If information is missing, use "Unknown".
Return only valid JSON.

Ticket:
{ticket_text}
"""

    for attempt in range(3):
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": prompt,
                "format": "json",
                "stream": False,
                "options": {"temperature": 0}
            },
            timeout=120
        )

        response.raise_for_status()
        result = response.json()["response"]

        try:
            ticket_info = TicketInfo.model_validate_json(result)
            return ticket_info

        except ValidationError as error:
            print(f"Validation failed. Attempt {attempt + 1}/3")
            prompt += f"\nCorrect these validation errors:\n{error}"

    raise ValueError("Could not extract valid ticket data after 3 attempts.")


if __name__ == "__main__":
    tickets = [
        "I am Ravi. My ProPlan payment page is not working. Urgent!",
        "My name is Priya. I cannot log in to BasicPlan.",
        "John here. My invoice for EnterprisePlan is incorrect.",
        "I am Kumar. The mobile app crashes when I open it.",
        "My name is Anu. Please update my email in ProPlan."
    ]

    for number, ticket in enumerate(tickets, start=1):
        print(f"\nTicket {number}:")
        try:
            result = extract_ticket(ticket)
            print(result.model_dump_json(indent=2))
        except Exception as error:
            print("Extraction failed:", error)
