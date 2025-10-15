import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("Testing gpt-4o-mini...")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Erkläre in 2 Sätzen, was ein sicheres Passwort ausmacht."}
    ],
    max_tokens=100
)

print(f"\n=== ANTWORT ===")
print(response.choices[0].message.content)
print(f"\n=== USAGE ===")
print(f"Total tokens: {response.usage.total_tokens}")
