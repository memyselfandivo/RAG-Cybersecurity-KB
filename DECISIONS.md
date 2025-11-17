# Key Design Decisions - RAG Cybersecurity KB

Dokumentation der wichtigsten technischen und strategischen Entscheidungen beim Bau dieses 
RAG-Systems.

**Kontext:** Diese Entscheidungen wurden während der Entwicklung getroffen und reflektieren 
Trade-offs zwischen Qualität, Kosten, Komplexität und Time-to-Market.

---

## 🎯 Decision 1: FAISS vs. Pinecone (Vector Store)

### Context
Benötigte einen Vector Store für Embedding-basierte Suche über Cybersecurity-Dokumente.

### Options Considered
1. **FAISS** (Facebook AI Similarity Search)
   - Local, kostenlos
   - Installation: `pip install faiss-cpu`
   - Keine API-Limits

2. **Pinecone**
   - Cloud-basiert
   - Skaliert automatisch
   - $70+/Monat für Production

3. **Chroma**
   - Hybrid (lokal + Cloud)
   - Einfache API
   - Noch relativ neu

### Decision
**Gewählt: FAISS**

### Reasoning
- **Kosten:** Komplett kostenlos für Entwicklung und Demo
- **Ausreichend:** Für < 100 Dokumente performt FAISS exzellent
- **Kontrolle:** Lokale Daten, keine Cloud-Abhängigkeit
- **Learning:** Verstehe Low-Level Vector Search besser

### Trade-offs
**✅ Pro:**
- Keine API-Kosten
- Volle Kontrolle
- Einfaches Setup für Portfolio-Projekt

**❌ Contra:**
- Skaliert nicht gut (> 10k Dokumente)
- Kein Auto-Scaling
- Kein Built-in Monitoring

### When to reconsider
Für Production mit > 1000 Dokumenten oder Multi-User-System → Pinecone oder Weaviate besser 
geeignet.

**Status:** ✅ Richtige Wahl für dieses Projekt

---

## 🎯 Decision 2: Chunk Size & Overlap

### Context
Initiales Setup: 500 Tokens/Chunk, kein Overlap → Distance-Werte >1.5, schlechte 
Retrieval-Qualität.

### Options Considered
1. **500 Tokens, kein Overlap** (Initial)
   - 7 Chunks total
   - Problem: Wichtige Infos "zerschnitten"

2. **300 Tokens, kein Overlap**
   - Mehr Chunks (ca. 11)
   - Risiko: Kontext-Verlust an Grenzen

3. **300 Tokens + 50 Token Overlap** ✅
   - 13 Chunks
   - Overlap verhindert Informationsverlust

4. **200 Tokens + 100 Overlap**
   - Maximale Granularität
   - Aber: Zu viele redundante Chunks

### Decision
**Gewählt: 300 Tokens + 50 Overlap**

### Reasoning
- **Empirisch getestet:** Distance-Verbesserung 10-19%
- **Balance:** Genug Granularität ohne Redundanz
- **Best Practice:** Industry-Standard für RAG-Systeme

### Results (Before/After)
| Query | Before (500) | After (300+50) | Improvement |
|-------|--------------|----------------|-------------|
| VPN | 1.54 🟡 | 1.25 🟡 | **19%** ✅ |
| Phishing | 0.96 🟢 | 0.86 🟢 | **10%** ✅ |
| MFA | 1.35 🟡 | 1.31 🟡 | 3% |

### Trade-offs
**✅ Pro:**
- Bessere Retrieval-Qualität
- Keine Edge-Case-Verluste
- Mehr Kontext pro Chunk

**❌ Contra:**
- Mehr API-Calls für Embeddings (einmalig)
- Leicht höhere Latenz (0.2s → 0.3s)

**Status:** ✅ Validiert durch Tests

---

## 🎯 Decision 3: GPT-4o-mini vs. GPT-4o (LLM)

### Context
Brauchte LLM für Antwort-Generierung nach Retrieval.

### Options Considered
1. **GPT-4o**
   - Höchste Qualität
   - $10/1M input tokens
   - Overkill für strukturierte Antworten?

2. **GPT-4o-mini** ✅
   - Gute Qualität
   - $0.15/1M input tokens (~70x günstiger!)
   - Optimiert für Chat/QA

3. **Claude Sonnet 3.5**
   - Ähnliche Qualität wie GPT-4o
   - Noch teurer
   - Redundant mit OpenAI-Stack

### Decision
**Gewählt: GPT-4o-mini**

### Reasoning
- **Kosten:** Bei 1000 Queries/Monat: ~$5 statt ~$50
- **Qualität:** Für RAG-QA mit klarem Context = ausreichend
- **Latenz:** Schneller als GPT-4o (0.8s vs. 1.5s)

### Test Results
Paralleltests mit 10 Queries:
- GPT-4o: Perfekte Antworten, aber keine merkliche Verbesserung
- GPT-4o-mini: 9/10 perfekt, 1/10 leicht unschärfer (akzeptabel)

### Trade-offs
**✅ Pro:**
- Massive Kosteneinsparung
- Schnellere Responses
- Ausreichend für Business-Case

**❌ Contra:**
- Bei sehr komplexen Queries minimal schlechter
- Weniger "kreativ" bei Edge-Cases

### When to reconsider
Wenn User-Feedback zeigt: "Antworten zu oberflächlich" → Upgrade zu GPT-4o.

**Status:** ✅ Optimal für Cost/Quality-Balance

---

## 🎯 Decision 4: Prompt Pattern "Cite Sources"

### Context
Musste Prompt-Pattern wählen für Antwort-Generierung. Ziel: Balance zwischen Hilfsbereitschaft und 
Transparenz.

### Options Considered
**Pattern A: "Answer ONLY from context"**
```python
"If information not in context, say 'Keine Info verfügbar.'"
```
- ✅ Pro: Keine Halluzinationen
- ❌ Contra: Oft zu restriktiv, unhilfreich

**Pattern B: "Context + General Knowledge"**
```python
"Use context primarily, supplement with knowledge if needed."
```
- ✅ Pro: Vollständigere Antworten
- ❌ Contra: Schwer zu tracen, was aus Docs vs. Modell-Wissen

**Pattern C: "Cite Sources explicitly"** ✅
```python
"Answer based on context. Cite sources in brackets: [file.md]"
```
- ✅ Pro: Transparent, nachvollziehbar
- ✅ Pro: LLM bleibt context-focused
- ⚠️ Neutral: Etwas verbose

### Decision
**Gewählt: Pattern C (Cite Sources)**

### Reasoning
- **Transparenz:** User sieht, woher Info kommt
- **Vertrauen:** Explizite Quellen → höhere Glaubwürdigkeit
- **Debugging:** Bei falscher Antwort → Check Source direkt
- **Business-fit:** Ideal für Customer Support, Compliance

### Test Results (Query: "Welcher ist der beste Password-Manager?")
- Pattern A: "Keine Info verfügbar" (technisch korrekt, aber unhilfreich)
- Pattern B: Suggestive Empfehlung ohne Quellenangabe
- Pattern C: Liste + Disclaimer + Sources (✅ beste Balance)

### Trade-offs
**✅ Pro:**
- Vertrauenswürdigkeit
- Nachvollziehbarkeit
- Professioneller Eindruck

**❌ Contra:**
- Antworten etwas länger
- Citations manchmal redundant bei offensichtlichen Fakten

**Status:** ✅ Beste Wahl für Business-Use-Case

---

## 🎯 Decision 5: "One Document = One Major Topic"

### Context
Musste entscheiden: Wenige große Dokumente oder viele kleine, fokussierte Dokumente?

### Options Considered
1. **Ein großes "Cybersecurity_Guide.md"**
   - Alle Topics in einem Dokument
   - Einfacher zu maintainen (1 File)
   - Problem: Chunks mischen Topics

2. **Ein Dokument pro Kategorie**
   - `passwords.md`, `network.md`, `threats.md`
   - Moderat granular
   - Problem: MFA in Passwords oder Network?

3. **Ein Dokument pro Major Topic** ✅
   - `phishing_detection.md`, `vpn_guide.md`, `mfa_setup.md`
   - Maximum Focus
   - Problem: Mehr Files zu managen

### Decision
**Gewählt: One Document = One Major Topic**

### Reasoning
**Empirische Beobachtung:**
- Phishing (eigenes Doc) → Distance 0.86 🟢
- MFA (Unter-Topic) → Distance 1.31 🟡

**Warum?**
- Chunks bleiben thematisch konsistent
- Keine Topic-Vermischung
- Updates isoliert (ändere VPN-Doc ohne Passwords zu touchen)
- Bessere Semantic Separation

### Implementation
```
docs/
├─ phishing_detection.md      ← Haupt-Thema
├─ password_security.md        ← Haupt-Thema
├─ network_security.md         ← Enthält VPN + Firewalls
└─ (future) mfa_guide.md       ← MFA auslagern
```

### Trade-offs
**✅ Pro:**
- Bessere Retrieval-Qualität
- Klarere Verantwortlichkeiten (wer updated was?)
- Einfacher zu erweitern

**❌ Contra:**
- Mehr Dateien zu verwalten
- Redundanz möglich (z.B. "Passwords" in Phishing + Password-Doc)

**Status:** ✅ Validiert durch Distance-Improvements

---

## 🎯 Decision 6: Top-K = 3 (Retrieval Strategy)

### Context
Wie viele Chunks sollten für jede Query retrieved werden?

### Options Considered
1. **Top-K = 1**
   - Schnell, günstig
   - Risiko: Bester Chunk könnte falsch sein

2. **Top-K = 3** ✅
   - Standard in RAG-Systemen
   - Balance zwischen Kontext und Redundanz

3. **Top-K = 5**
   - Mehr Kontext
   - Aber: Oft redundant oder irrelevant

4. **Distance-Threshold (adaptive)**
   - Nur Chunks mit Distance <1.5
   - Problem: Manchmal kein Chunk qualifiziert

### Decision
**Gewählt: Top-K = 3 (fixed)**

### Reasoning
- **Standard:** Most RAG implementations use 3-5
- **Balance:** Genug für Multi-Paragraph-Antworten
- **Token-Budget:** 3 Chunks × 300 Tokens = 900 Tokens Context (reasonable)

### Observed Patterns
**Phishing-Query:**
```
Top-1: 0.86 ✅
Top-2: 0.93 ✅
Top-3: 1.45 ⚠️
→ 2/3 relevant, 3rd redundant
```

**MFA-Query:**
```
Top-1: 1.31 ⚠️
Top-2: 1.41 ⚠️
Top-3: 1.49 ⚠️
→ Alle ok, aber keiner exzellent
```

### Trade-offs
**✅ Pro:**
- Robustheit (falls Top-1 suboptimal)
- Multi-Source-Antworten möglich

**❌ Contra:**
- Top-3 oft wenig relevant
- Verschwendet Tokens

### Future Optimization
Erwäge für v3.0:
```python
# Adaptive Top-K basierend auf Top-1 Distance
if top1_distance < 1.0:
    k = 2  # Top-1 ist perfekt, brauche nur 1-2 mehr
else:
    k = 5  # Top-1 schwach, hole mehr Optionen
```

**Status:** ✅ Funktioniert, aber optimierbar

---

## 🎯 Decision 7: Python 3.12 vs. 3.10

### Context
Musste Python-Version wählen für Development.

### Problem Encountered
Initial: Python 3.14 (Beta) → Incompatible mit vielen Packages

### Decision
**Gewählt: Python 3.12** (Downgrade von 3.14)

### Reasoning
- **Kompatibilität:** Alle Dependencies (FAISS, OpenAI SDK) stable
- **Long-term:** 3.12 LTS bis 2028
- **Performance:** Marginal schneller als 3.10

### Trade-offs
**✅ Pro:**
- Stabil, Production-ready
- Community-Support

**❌ Contra:**
- Verpasste neue Features aus 3.13+

**Status:** ✅ Pragmatische Wahl

---

## 📊 Decision Summary Matrix

| Decision | Impact | Confidence | Would Change? |
|----------|--------|------------|---------------|
| FAISS vs Pinecone | High | High | ❌ No |
| 300+50 Chunking | High | High | ❌ No |
| GPT-4o-mini | High | High | ❌ No |
| Cite Sources Pattern | High | High | ❌ No |
| One Doc = One Topic | High | High | ❌ No |
| Top-K = 3 | Medium | Medium | ⚠️ Maybe (adaptive) |
| Python 3.12 | Low | High | ❌ No |

---

## 🔄 Decisions to Revisit for v3.0

### 1. Hybrid Search (Semantic + BM25)
**Why:** Akronyme/Fachbegriffe schlecht mit Semantic Search
**Expected Impact:** +15% für Technical Queries

### 2. Reranking (Cross-Encoder)
**Why:** Top-K enthält oft irrelevante Chunks
**Expected Impact:** +10% Average Relevance

### 3. Adaptive Top-K
**Why:** Fixed K = 3 suboptimal für verschiedene Query-Types
**Expected Impact:** -20% Token-Waste

---

## 🎓 Meta-Learning: Decision-Making Process

**Pattern, der funktioniert hat:**
1. **Measure First:** Distance-Werte als Baseline
2. **Hypothesis:** "Kleinere Chunks = bessere Distance"
3. **Test:** 500 → 300 Tokens
4. **Validate:** 10-19% Improvement
5. **Document:** In diesem File

**Lessons Learned:**
- Empirisches Testen > Vermutungen
- Distance-Werte = objektive Metrik
- Trade-offs explizit machen (Cost vs. Quality)
- "Good enough" besser als "perfekt aber nie fertig"

---

**Created:** [Datum]  
**Last Updated:** [Datum]  
**Version:** 1.0
