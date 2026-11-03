import json
import requests

from app.tools import get_customer, get_order_status


def ask_assistant(question):
    prompt = f"""
You are a customer support assistant.

Decide whether the question requires a tool.

Available tools:
1. get_customer(customer_id)
2. get_order_status(order_id)

Return ONLY JSON:
{{
  "calls": [
    {{"tool": "get_customer", "customer_id": 2}}
  ]
}}

If no tool is required, return:
{{"calls": []}}

Question: {question}
"""

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
    decision = json.loads(response.json()["response"])

    results = []

    for call in decision.get("calls", []):
        tool_name = call.get("tool")

        if tool_name == "get_customer":
            result = get_customer(call.get("customer_id"))

        elif tool_name == "get_order_status":
            result = get_order_status(call.get("order_id"))

        else:
            result = {"error": "Unknown tool"}

        results.append({
            "tool": tool_name,
            "result": result
        })

    return results
def test_unknown_tool():
    call = {"tool": "invalid_tool"}
    tool_name = call.get("tool")

    if tool_name == "get_customer":
        result = get_customer(call.get("customer_id"))
    elif tool_name == "get_order_status":
        result = get_order_status(call.get("order_id"))
    else:
        result = {"error": "Unknown tool"}

    return result

if __name__ == "__main__":
    result = ask_assistant(
        "Which plan is customer 2 on and where is order 1042?"
    )
    print(json.dumps(result, indent=2))