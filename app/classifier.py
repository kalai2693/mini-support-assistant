
import json
from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parent.parent

def classify_ticket(ticket, version):
    prompt_file = BASE_DIR / "prompts" / f"classifier_{version}.txt"

    with open(prompt_file, "r", encoding="utf-8") as file:
        prompt = file.read()

    prompt = prompt.replace("{ticket}", ticket)

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0}
        },
        timeout=120
    )

    response.raise_for_status()
    return response.json()["response"].strip()


def run_eval(version):
    dataset_file = BASE_DIR / "data" / "golden.jsonl"

    correct = 0
    total = 0

    with open(dataset_file, "r", encoding="utf-8") as file:
        for line in file:
            item = json.loads(line)
            ticket = item["ticket"]
            expected = item["category"]

            predicted = classify_ticket(ticket, version)

            total += 1

            if predicted.lower() == expected.lower():
                correct += 1

            print(f"Expected: {expected} | Predicted: {predicted}")

    accuracy = (correct / total) * 100

    print(f"\nPrompt {version.upper()} Accuracy:")
    print(f"{correct}/{total} = {accuracy:.2f}%")


if __name__ == "__main__":
    run_eval("v1")
    run_eval("v2")
