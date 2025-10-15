"""
Prompt Pattern Comparison - Simplified
Teste 3 Patterns mit 1 Query
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
import faiss
import numpy as np
import pickle

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_vector_store():
    index = faiss.read_index("faiss_index.bin")
    with open("vector_store.pkl", 'rb') as f:
        metadata = pickle.load(f)
    return index, metadata

def search_chunks(query, index, metadata):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    query_embedding = np.array([response.data[0].embedding]).astype('float32')
    distances, indices = index.search(query_embedding, 3)
    
    results = []
    for i, idx in enumerate(indices[0]):
        results.append({
            'chunk': metadata[idx]['chunk_text'],
            'filename': metadata[idx]['filename'],
            'distance': float(distances[0][i])
        })
    return results

def test_patterns(query, chunks):
    context = "\n\n---\n\n".join([f"Source: {c['filename']}\n{c['chunk']}" for c in chunks])
    
    patterns = {
        "A_ONLY_CONTEXT": f"""Answer based ONLY on the context. If info is missing, say "Diese Information steht nicht in den Dokumenten."

Context:
{context}

Question: {query}

Answer in German:""",
        
        "B_CONTEXT_PLUS": f"""Answer using context as primary source. You may add general knowledge if helpful, but mark it as "[Zusätzlich:]"

Context:
{context}

Question: {query}

Answer in German:""",
        
        "C_CITE_SOURCES": f"""Answer and cite sources in brackets for every fact, like: "MFA reduces breaches [password_security.md]"

Context:
{context}

Question: {query}

Answer in German with citations:"""
    }
    
    results = {}
    
    for name, prompt in patterns.items():
        print(f"\n{'='*70}\n{name}\n{'='*70}")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        
        answer = response.choices[0].message.content
        tokens = response.usage.total_tokens
        
        print(f"\n✅ ({tokens} tokens):\n{answer}")
        
        results[name] = {'answer': answer, 'tokens': tokens}
        
        input("\n⏸️  ENTER für nächstes Pattern...")
    
    return results

# Main
print("="*70)
print("PROMPT PATTERN TEST")
print("="*70)

index, metadata = load_vector_store()
print(f"\n✅ Vector Store: {index.ntotal} Chunks")

query = "Welches ist der beste Passwort-Manager?"

print(f"\n📝 Test-Query: {query}")
print("\n🔍 Suche Chunks...")

chunks = search_chunks(query, index, metadata)

print("\n📚 Gefundene Chunks:")
for i, c in enumerate(chunks, 1):
    print(f"{i}. {c['filename']} (Distance: {c['distance']:.4f})")

input("\n▶️  ENTER zum Starten...")

results = test_patterns(query, chunks)

print("\n" + "="*70)
print("ZUSAMMENFASSUNG")
print("="*70)

for name, res in results.items():
    print(f"\n{name}:")
    print(f"  Tokens: {res['tokens']}")
    print(f"  Länge: {len(res['answer'])} Zeichen")

print("\n✅ FERTIG! Welches Pattern hat am besten funktioniert?")
