"""
RAG Cybersecurity Knowledge Base - Demo CLI
Professional interface for demonstrations
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import faiss
import numpy as np
import pickle

# ANSI Color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    """Print colored header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(70)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ {text}{Colors.END}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_query(text):
    """Print query"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}🔍 Query:{Colors.END} {text}")

def print_chunk_info(num, filename, distance):
    """Print chunk information"""
    color = Colors.GREEN if distance < 1.0 else Colors.YELLOW if distance < 1.5 else Colors.RED
    print(f"{color}  {num}. {filename} (Distance: {distance:.4f}){Colors.END}")

# Load environment
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"

def load_vector_store():
    """Load vector store"""
    if not Path("faiss_index.bin").exists():
        print_error("Vector Store nicht gefunden!")
        print_info("Führe zuerst 'python rag_mini.py' aus, um den Vector Store zu erstellen.")
        sys.exit(1)
    
    index = faiss.read_index("faiss_index.bin")
    with open("vector_store.pkl", 'rb') as f:
        metadata = pickle.load(f)
    return index, metadata

def search_chunks(query, index, metadata, top_k=3):
    """Search for similar chunks"""
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=query)
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

def generate_answer(query, chunks):
    """Generate answer with LLM"""
    context = "\n\n---\n\n".join([
        f"Source: {c['filename']}\n{c['chunk']}" 
        for c in chunks
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
    
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600
    )
    
    return {
        'answer': response.choices[0].message.content,
        'tokens': response.usage.total_tokens
    }

def process_query(query, index, metadata):
    """Process a single query"""
    print_query(query)
    
    # Retrieval
    print(f"\n{Colors.BOLD}📚 Relevante Dokumente:{Colors.END}")
    chunks = search_chunks(query, index, metadata, top_k=3)
    
    for i, chunk in enumerate(chunks, 1):
        print_chunk_info(i, chunk['filename'], chunk['distance'])
    
    # Generation
    print(f"\n{Colors.BOLD}💭 Generiere Antwort...{Colors.END}")
    result = generate_answer(query, chunks)
    
    # Output
    print(f"\n{Colors.BOLD}{Colors.GREEN}{'─'*70}{Colors.END}")
    print(f"{Colors.BOLD}Antwort:{Colors.END}\n")
    print(result['answer'])
    print(f"\n{Colors.BOLD}{Colors.GREEN}{'─'*70}{Colors.END}")
    print(f"{Colors.CYAN}Tokens verwendet: {result['tokens']}{Colors.END}")

def show_examples():
    """Show example queries"""
    examples = [
        "Was ist Multi-Factor Authentication?",
        "Wie erkenne ich eine Phishing-Email?",
        "Was mache ich bei einem Security-Vorfall?",
        "Wie erstelle ich ein sicheres Passwort?",
        "Was ist ein VPN und wozu brauche ich es?"
    ]
    
    print(f"\n{Colors.BOLD}💡 Beispiel-Fragen:{Colors.END}")
    for i, example in enumerate(examples, 1):
        print(f"{Colors.CYAN}  {i}. {example}{Colors.END}")

def show_help():
    """Show help message"""
    print(f"\n{Colors.BOLD}📖 Verfügbare Commands:{Colors.END}")
    print(f"{Colors.CYAN}  help{Colors.END}      - Zeige diese Hilfe")
    print(f"{Colors.CYAN}  examples{Colors.END}  - Zeige Beispiel-Fragen")
    print(f"{Colors.CYAN}  clear{Colors.END}     - Bildschirm leeren")
    print(f"{Colors.CYAN}  exit{Colors.END}      - Beenden")
    print(f"\n{Colors.BOLD}Oder stelle direkt eine Frage!{Colors.END}")

def main():
    """Main function"""
    # Header
    print_header("CYBERSECURITY KNOWLEDGE BASE")
    print(f"{Colors.BOLD}Willkommen zum KI-gestützten Security-Assistenten!{Colors.END}")
    print("Stelle Fragen zu: Passwords, Phishing, Network Security, Incident Response\n")
    
    # Load Vector Store
    print_info("Lade Knowledge Base...")
    try:
        index, metadata = load_vector_store()
        print_success(f"Knowledge Base geladen: {index.ntotal} Dokument-Chunks")
    except Exception as e:
        print_error(f"Fehler beim Laden: {e}")
        sys.exit(1)
    
    # Show help
    show_help()
    
    # Interactive loop
    query_count = 0
    
    while True:
        try:
            # Prompt
            user_input = input(f"\n{Colors.BOLD}{Colors.BLUE}🔍 Deine Frage:{Colors.END} ").strip()
            
            if not user_input:
                continue
            
            # Commands
            if user_input.lower() in ['exit', 'quit', 'q']:
                print(f"\n{Colors.GREEN}Auf Wiedersehen! 👋{Colors.END}\n")
                break
            
            elif user_input.lower() == 'help':
                show_help()
                continue
            
            elif user_input.lower() == 'examples':
                show_examples()
                continue
            
            elif user_input.lower() == 'clear':
                os.system('clear' if os.name != 'nt' else 'cls')
                print_header("CYBERSECURITY KNOWLEDGE BASE")
                continue
            
            # Process query
            query_count += 1
            process_query(user_input, index, metadata)
            
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Unterbrochen. Auf Wiedersehen! 👋{Colors.END}\n")
            break
        except Exception as e:
            print_error(f"Fehler: {e}")
            continue
    
    # Summary
    if query_count > 0:
        print(f"\n{Colors.CYAN}Du hast {query_count} Frage(n) gestellt. Danke fürs Nutzen! 🚀{Colors.END}\n")

if __name__ == "__main__":
    main()
