# Prompt Pattern Comparison

## Test Setup
- **Query**: "Welches ist der beste Passwort-Manager?"
- **Chunks**: 3 Chunks aus password_security.md, network_security.md
- **Model**: gpt-4o-mini

---

## Pattern A: ONLY Context

**Prompt-Instruction:**
> "Answer based ONLY on context. If info is missing, say 'Diese Information steht nicht in den Dokumenten.'"

**Antwort:**
> "Diese Information steht nicht in den verfügbaren Dokumenten."

**Bewertung:** ✅ Korrekt, aber zu restriktiv
- ✅ Ehrlich und präzise
- ❌ Nicht hilfreich (User bekommt keine Info)
- ❌ Ignoriert verfügbare Context-Infos (die 3 Manager werden erwähnt!)

**Use Case:** 
- Compliance, Legal, Policy-Suche
- Wenn Genauigkeit > Hilfsbereitschaft

**Score:** 2/5 (korrekt, aber unhilfreich für diese Frage)

---

## Pattern B: Context + Knowledge

**Prompt-Instruction:**
> "Answer using context as primary source. You may add general knowledge if helpful, but mark it as '[Zusätzlich:]'"

**Antwort:**
> "Der beste Passwort-Manager hängt von den individuellen Bedürfnissen und Vorlieben ab, jedoch sind die im Dokument genannten Optionen als empfehlenswert hervorzuheben:
> 1. 1Password - Benutzerfreundlich...
> 2. Bitwarden - Open-Source...
> 3. LastPass - Weit verbreitet...
> [Zusätzlich:] Generell sollte man bei der Auswahl..."

**Bewertung:** ⚠️ Gut, aber leicht suggestiv
- ✅ Listet alle 3 Manager
- ✅ Ergänzt mit nützlichem Kontext
- ⚠️ "empfehlenswert hervorzuheben" suggeriert Endorsement
- ⚠️ Zusatz-Info nicht klar als eigenes Wissen markiert

**Use Case:**
- Educational Content
- User-facing Documentation
- Wenn Vollständigkeit wichtig ist

**Score:** 3.5/5 (hilfreich, aber Ton könnte objektiver sein)

---

## Pattern C: Cite Sources

**Prompt-Instruction:**
> "Answer and cite sources in brackets for every fact, like: 'MFA reduces breaches [password_security.md]'"

**Antwort:**
> "Der beste Passwort-Manager hängt von den individuellen Bedürfnissen ab, aber einige der am häufigsten empfohlenen Optionen sind 1Password, Bitwarden und LastPass.
> 1. 1Password ist bekannt für... [password_security.md]
> 2. Bitwarden ist... [password_security.md]
> 3. LastPass... [password_security.md]"

**Bewertung:** ✅ Am besten für diesen Use Case!
- ✅ Objektiver Ton ("am häufigsten empfohlenen")
- ✅ Explizite Quellenangaben für Vertrauen
- ✅ Transparent: User weiß, woher jede Info kommt
- ✅ Keine Halluzination

**Use Case:**
- Research, Audits
- Customer Support
- Knowledge Bases
- **Cybersecurity Documentation (unser Use Case!)**

**Score:** 4/5 (beste Balance aus Hilfe + Transparenz)

---

## Vergleich: Pattern B vs. C

**Inhaltlich sehr ähnlich** bei dieser Frage, weil:
- Beide nutzen gleichen Context
- Frage ist moderat ambiguitiv (nicht völlig unbeantwortbar)
- Beide geben hilfreiche Antworten

**Unterschiede:**
| Aspekt | Pattern B | Pattern C |
|--------|-----------|-----------|
| **Ton** | "empfehlenswert hervorzuheben" (suggestiv) | "am häufigsten empfohlenen" (objektiv) |
| **Transparenz** | Quelle am Ende erwähnt | Jede Aussage einzeln zitiert |
| **Zusatz-Info** | Markiert als "[Zusätzlich:]" | Keine Zusatz-Infos |
| **Vertrauen** | Gut | Besser (durch Citations) |

**Fazit:** Für Business-Use-Cases ist **Pattern C bevorzugt** wegen Transparenz und Objektiv

ität.

---

## Lessons Learned

### Was funktioniert gut:
1. **Explizite Quellenangaben** erhöhen Vertrauen
2. **Objektiver Ton** wichtiger als "Hilfsbereitschaft"
3. Pattern A zu restriktiv für Fragen, wo Context teilweise relevant ist

### Verbesserungsideen:
1. **Hybrid-Pattern**: "Cite Sources" + Option für Zusatz-Wissen
2. **Distance-basiertes Pattern-Switching**:
   - Distance < 1.0 → Pattern C (Cite Sources)
   - Distance > 1.5 → Pattern A (Only Context) mit "Info nicht verfügbar"
3. **Query-Type-Detection**:
   - Faktische Frage → Pattern C
   - Meinungsfrage → Pattern A mit Disclaimer

---

## Empfehlung für Cybersecurity KB

**Pattern C (Cite Sources)** verwenden:
- Maximale Transparenz
- User kann Quellen selbst prüfen
- Objektiver Ton verhindert implizite Empfehlungen
- Professioneller für Business-Context

**Nächste Schritte:**
- Pattern C als Default in `rag_mini.py` implementieren
- Testen mit mehr ambiguitiven Fragen
- Business-Demo vorbereiten
