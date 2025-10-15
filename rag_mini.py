"""
RAG Mini Project - Main Script v2.0
Mit optimiertem Chunking (300 Tokens + 50 Overlap)
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

# Config - OPTIMIERT!
DOCS_DIR = "docs"
CHUNK_SIZE = 300  # Reduziert von 500
CHUNK_OVERLAP = 50  # NEU!
EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"
VECTOR_STORE_PATH = "vector_store.pkl"
INDEX_PATH = "faiss_index.bin"


def load_documents():
    """Lade alle Markdown-Dateien"""
    docs = []
    docs_path = Path(DOCS_DIR)
    
    if not docs_path.exists():
        print(f"❌ ERROR: {DOCS_DIR}/ nicht gefunden!")
        return []
    
    for file_path in docs_path.glob("*.md"):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            docs.append({
                'filename': file_path.name,
                'content': content
            })
            print(f"✅ Geladen: {file_path.name} ({len(content)} Zeichen)")
    
    return docs


def chunk_text_with_overlap(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """
    Teile Text in Chunks mit Overlap
    """
    paragraphs = text.split('\n\n')
    
    chunks = []
    current_chunk = ""
    all_text = " ".join([p.strip() for p in paragraphs if p.strip()])
    words = all_text.split()
    
    # Sliding window mit Overlap
    chunk_words = chunk_size  # ~1 Token = 0.75 Wörter
    overlap_words = overlap
    
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_words])
        if chunk:
            chunks.append(chunk)
        i += (chunk_words - overlap_words)  # Overlap!
    
    return chunks


def create_embeddings(texts):
    """Erstelle Embeddings"""
    print(f"\n🔄 Erstelle Embeddings für {len(texts)} Chunks...")
    
    embeddings = []
    for i, text in enumerate(texts):
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text
        )
        embedding = response.data[0].embedding
        embeddings.append(embedding)
        
        if (i + 1) % 10 == 0:
            print(f"   Fortschritt: {i + 1}/{len(texts)}")
    
    print(f"✅ Embeddings erstellt!")
    return np.array(embeddings).astype('float32')


def build_vector_store(docs):
    """Baue FAISS Vector Store mit Overlap-Chunks"""
    print("\n" + "="*50)
    print("VECTOR STORE AUFBAUEN (v2.0 mit Overlap)")
    print("="*50)
    
    all_chunks = []
    chunk_metadata = []
    
    for doc in docs:
        chunks = chunk_text_with_overlap(doc['content'])
        print(f"\n📄 {doc['filename']}: {len(chunks)} Chunks (300 Tokens, 50 Overlap)")
        
        for chunk in chunks:
            all_chunks.append(chunk)
            chunk_metadata.append({
                'filename': doc['filename'],
                'chunk_text': chunk
            })
    
    print(f"\n✅ Gesamt: {len(all_chunks)} Chunks aus {len(docs)} Dokumenten")
    print(f"   Verbesserung: {len(all_chunks)} vs. vorher ~7 Chunks!")
    
    embeddings = create_embeddings(all_chunks)
    
    print(f"\n🔄 Erstelle FAISS Index...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    print(f"✅ FAISS Index erstellt mit {index.ntotal} Vektoren")
    
    print(f"\n💾 Speichere Vector Store...")
    faiss.write_index(index, INDEX_PATH)
    with open(VECTOR_STORE_PATH, 'wb') as f:
        pickle.dump(chunk_metadata, f)
    
    print(f"✅ Gespeichert: {INDEX_PATH}, {VECTOR_STORE_PATH}")
    
    return index, chunk_metadata


def load_vector_store():
    """Lade Vector Store"""
    if not Path(INDEX_PATH).exists() or not Path(VECTOR_STORE_PATH).exists():
        return None, None
    
    print("📂 Lade Vector Store...")
    index = faiss.read_index(INDEX_PATH)
    with open(VECTOR_STORE_PATH, 'rb') as f:
        metadata = pickle.load(f)
    print(f"✅ Geladen: {index.ntotal} Vektoren")
    return index, metadata


def search_similar_chunks(query, index, metadata, top_k=3):
    """Suche ähnlichste Chunks"""
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
    """Beantworte Query mit RAG"""
    print("\n" + "="*50)
    print(f"QUERY: {query}")
    print("="*50)
    
    print(f"\n🔍 Suche relevante Chunks (Top {top_k})...")
    results = search_similar_chunks(query, index, metadata, top_k)
    
    print(f"\n📚 Gefundene Chunks:")
    for i, result in enumerate(results):
        print(f"\n{i+1}. {result['filename']} (Distance: {result['distance']:.4f})")
        print(f"   Preview: {result['chunk'][:100]}...")
    
    context = "\n\n---\n\n".join([
        f"Source: {r['filename']}\n{r['chunk']}" 
        for r in results
    ])
    
    prompt = f"""Du bist ein Cybersecurity-Experte. Beantworte die Frage basierend auf dem Kontext.

Kontext:
{context}

Frage: {query}

WICHTIG:
- Antworte auf Deutsch
- Zitiere Quellen in Klammern: [filename.md]
- Sei präzise und konkret
- Falls der Kontext die Antwort nicht enthält, sag das

Antwort:"""
    
    print(f"\n🤖 Generiere Antwort mit {LLM_MODEL}...")
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600
    )
    
    answer = response.choices[0].message.content
    tokens_used = response.usage.total_tokens
    
    print(f"\n✅ Antwort generiert ({tokens_used} Tokens):")
    print("\n" + "="*50)
    print(answer)
    print("="*50)
    
    return answer, results


def main():
    """Main Function"""
    print("="*50)
    print("RAG MINI PROJECT v2.0")
    print("Cybersecurity Knowledge Base")
    print("="*50)
    
    # Lösche alte Vector Stores
    if Path(INDEX_PATH).exists():
        print("\n⚠️  Alter Vector Store gefunden. Wird neu erstellt...")
        os.remove(INDEX_PATH)
        os.remove(VECTOR_STORE_PATH)
    
    # Neu erstellen
    print("\n💡 Erstelle neuen Vector Store mit optimiertem Chunking...")
    docs = load_documents()
    if not docs:
        return
    index, metadata = build_vector_store(docs)
    
    # Test-Queries
    print("\n\n" + "="*50)
    print("TEST QUERIES")
    print("="*50)
    
    test_queries = [
        "Was ist ein VPN?",
        "Wie erkenne ich eine Phishing-Email?",
        "Was ist Multi-Factor Authentication?"
    ]
    
    for query in test_queries:
        rag_query(query, index, metadata, top_k=3)
        print("\n")


if __name__ == "__main__":
    main()
