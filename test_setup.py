"""
RAG Mini Project - Setup Test
Tests ob OpenAI API funktioniert
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

def test_api_connection():
    """Teste OpenAI API Connection"""
    
    # 1. Load Environment Variables
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ ERROR: OPENAI_API_KEY nicht in .env gefunden!")
        return False
    
    print("✅ API Key gefunden")
    
    # 2. Initialize OpenAI Client
    try:
        client = OpenAI(api_key=api_key)
        print("✅ OpenAI Client initialisiert")
    except Exception as e:
        print(f"❌ ERROR beim Initialisieren: {e}")
        return False
    
    # 3. Simple Test Call
    try:
        print("\n🔄 Teste API Call...")
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "user", "content": "Say 'API works!' in one sentence."}
            ],
            max_completion_tokens=20
        )
        
        answer = response.choices[0].message.content
        print(f"✅ API Response: {answer}")
        print(f"✅ Tokens used: {response.usage.total_tokens}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR beim API Call: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("RAG MINI PROJECT - SETUP TEST")
    print("=" * 50)
    
    success = test_api_connection()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ SETUP ERFOLGREICH! Du kannst mit Session 1 weitermachen.")
    else:
        print("❌ SETUP FEHLGESCHLAGEN. Prüfe deine .env Datei.")
    print("=" * 50)
