"""
RAG Mini Project - Interactive Query Tool
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import faiss
import numpy as np
import pickle

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"
VECTOR_STORE_PATH = "vector_store.pkl"
INDEX_PATH = "faiss_index.bin"


def load_vector_store():
    if not Path(INDEX_PATH).exists() or not Path(VECTOR_STORE_PATH).exists():
        print("❌ Vector Store nicht gefunden! Führe erst 'python rag_mini.py' aus.")
        return None, None
    
    index = faiss.read_index(INDEX_PATH)
    with open(VECTOR_STORE_PATH, 'rb') as f:
        metadata = pickle.load(f)
    return index, metadata


def search_similar_chunks(query, index, metadata, top_k=3):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=query
    )
    query_embedding = np.array([response.data[0].embedding]).astype('float32')
    
    distances, indices = index.search(query_embedding, top_k)
    
    results = []
    for i, idx in enumerate(indices[0]):
        results.append({
            'chunk': metadata[idx]['chunk_text'],
            'filename': metadata[idx]['filename'],
            'distance': float(distances[0][i])
        })
    
    return results


def rag_query(query, index, metadata, top_k=3):
    print("\n" + "="*70)
    print(f"QUERY: {query}")
    print("="*70)
    
    print(f"\n🔍 Suche relevante Chunks (Top {top_k})...")
    results = search_similar_chunks(query, index, metadata, top_k)
    
    print(f"\n📚 Gefundene Chunks:")
    for i, result in enumerate(results):
        print(f"\n{i+1}. {result['filename']} (Distance: {result['distance']:.4f})")
        preview = result['chunk'][:150].replace('\n', ' ')
        print(f"   Preview: {preview}...")
    
    context = "\n\n---\n\n".join([
        f"Source: {r['filename']}\n{r['chunk']}" 
        for r in results
    ])
    
    prompt = f"""Du bist ein Cybersecurity-Experte. Beantworte die Frage basierend auf dem bereitgestellten Kontext.

Kontext:
{context}

Frage: {query}

Anleitung:
- Antworte auf Deutsch
- Sei präzise und konkret
- Falls der Kontext die Antwort nicht enthält, sag das
- Erwähne die Quelle, wenn möglich

Antwort:"""
    
    print(f"\n🤖 Generiere Antwort mit {LLM_MODEL}...")
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    
    answer = response.choices[0].message.content
    tokens_used = response.usage.total_tokens
    
    print(f"\n✅ Antwort ({tokens_used} Tokens):")
    print("\n" + "-"*70)
    print(answer)
    print("-"*70)
    
    return {
        'query': query,
        'answer': answer,
        'chunks': results,
        'tokens': tokens_used
    }


def main():
    print("="*70)
    print("RAG INTERACTIVE QUERY TOOL")
    print("="*70)
    
    index, metadata = load_vector_store()
    if index is None:
        return
    
    print(f"\n✅ Vector Store geladen: {index.ntotal} Chunks")
    
    test_queries = [
        "Was ist Multi-Factor Authentication?",
        "Was kann ich gegen Phishing Attacken machen?",
        "Welches ist der beste Passwort-Manager?"
    ]
    
    print("\n" + "="*70)
    print("TESTE DEINE QUERIES")
    print("="*70)
    
    for query in test_queries:
        rag_query(query, index, metadata, top_k=3)
        input("\n⏸️  Drücke ENTER für nächste Query...")
    
    print("\n" + "="*70)
    print("✅ ALLE QUERIES GETESTET!")
    print("="*70)


if __name__ == "__main__":
    main()
