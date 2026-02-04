from client import client
from prompt import SYSTEM_PROMPT

def run_chatbot():
    print("Healthcare Information Chatbot (Educational Use Only)")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("User: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye. Stay healthy.")
            break

        if not user_input:
            print("Assistant: Please ask a healthcare-related question.\n")
            continue

        if user_input.lower() in {"hi", "hello", "hii", "hey"}:
            print("Assistant: Hello! Please ask a healthcare-related question.\n")
            continue

        try:
            prompt = f"""
{SYSTEM_PROMPT}

User question:
{user_input}
"""

            response = client.models.generate_content(
                model="models/gemini-flash-latest",
                contents=[
                    {
                        "role": "user",
                        "parts": [{"text": prompt}]
                    }
                ]
            )

            answer = response.candidates[0].content.parts[0].text.strip()

            answer += (
                "\n\nDisclaimer: I am not a medical professional. "
                "This information is for educational purposes only."
            )

            print(f"Assistant: {answer}\n")

        except Exception as e:
            print("ERROR FROM GEMINI:", e)
            print(
                "Assistant: I don't know.\n"
                "Disclaimer: I am not a medical professional. "
                "This information is for educational purposes only.\n"
            )