import os
import sys
from dotenv import load_dotenv
from google import genai

# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("ERROR: GEMINI_API_KEY not found")
    sys.exit(1)

# ---------------------------------------------------------
# Initialize Gemini Client (NEW SDK)
# ---------------------------------------------------------
client = genai.Client(api_key=API_KEY)

# ---------------------------------------------------------
# System Prompt
# ---------------------------------------------------------
SYSTEM_PROMPT = """
You are a healthcare information assistant.

Rules:
- Provide HIGH-LEVEL, GENERAL, NON-DIAGNOSTIC health information only
- Do NOT give medical diagnosis or prescriptions
- Answer clearly and politely
"""

# ---------------------------------------------------------
# Chat loop
# ---------------------------------------------------------
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
                ],
                # ✅ ONLY ADDITION: token limit
                config=genai.types.GenerateContentConfig(
                    max_output_tokens=300
                )
            )

            # Correct response reading (NEW SDK)
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

# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------
if __name__ == "__main__":
    run_chatbot()