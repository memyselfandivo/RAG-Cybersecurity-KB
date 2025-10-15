import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("Testing GPT-5-nano mit mehr Tokens...")

response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=[
        {"role": "user", "content": "Erkläre in 2 Sätzen, was ein sicheres Passwort ausmacht."}
    ],
    max_completion_tokens=500  # Mehr Tokens!
)

print(f"\n=== ANTWORT ===")
print(response.choices[0].message.content)
print(f"\n=== USAGE ===")
print(f"Reasoning tokens: {response.usage.completion_tokens_details.reasoning_tokens}")
print(f"Output tokens: {response.usage.completion_tokens - response.usage.completion_tokens_details.reasoning_tokens}")
print(f"Total: {response.usage.total_tokens}")
