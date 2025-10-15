"""
Quick Test: GPT-5-nano Response
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("Testing GPT-5-nano...")

response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=[
        {"role": "system", "content": "Du bist ein hilfsbereiter Assistent."},
        {"role": "user", "content": "Erkläre in 2 Sätzen, was ein sicheres Passwort ausmacht."}
    ],
    max_completion_tokens=100
)

print("\n=== RESPONSE DEBUG ===")
print(f"Choices: {len(response.choices)}")
print(f"Finish reason: {response.choices[0].finish_reason}")
print(f"Message role: {response.choices[0].message.role}")
print(f"Message content type: {type(response.choices[0].message.content)}")
print(f"Message content length: {len(response.choices[0].message.content) if response.choices[0].message.content else 0}")
print(f"\nMessage content:")
print(f"'{response.choices[0].message.content}'")
print(f"\nUsage: {response.usage}")
print("======================")
