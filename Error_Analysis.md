# Error Analysis - RAG Mini Project

## Test Query 1: "Was ist Multi-Factor Authentication?"

### Retrieval Performance
- **Top-1**: `password_security.md` (Distance: 1.35) ✅ **Relevant**
- **Top-2**: `network_security.md` (Distance: 1.52) ⚠️ **Grenzwertig**
- **Top-3**: `phishing_detection.md` (Distance: 1.64) ❌ **Nicht relevant**

**Diagnose:** Top-1 ist gut, aber Top-2/3 sind Noise.

### Answer Quality
**Antwort:**
> Multi-Factor Authentication (MFA) ist ein Sicherheitsverfahren, das zur Authentifizierung von Benutzern mehrere Nachweisfaktoren erfordert...

**Bewertung:** ✅ Gut
- Korrekte Definition
- Konkrete Beispiele (SMS, Authenticator, Hardware)
- Statistik korrekt zitiert (99.9%)
- Quelle genannt

**Was fehlt:**
- Könnte ausführlicher sein
- Mehr Kontext (Warum wichtig? Wo einsetzen?)

### Root Cause Analysis

**War es ein Retrieval-Problem?**
- Teilweise. Top-1 war korrekt, aber Top-2/3 verwässern den Kontext.

**War es ein Prompt-Problem?**
- Nein. Der Prompt funktioniert gut.

**War es ein Chunking-Problem?**
- Ja! Mit 7 Chunks aus 4 Docs ist MFA wahrscheinlich mit anderen Themen vermischt.
- **Lösung:** Kleinere Chunks (300 statt 500 Tokens)

### Verbesserungsvorschläge

1. **Chunk-Size reduzieren** auf 300 Tokens
2. **Distance-Threshold** einführen (nur Chunks < 1.5)
3. **Top-K reduzieren** auf 2 statt 3
4. Optional: **Reranking** nach Retrieval

---

## Test Query 2: [Nächste Query hier dokumentieren]


## Test Query 2: "Was kann ich gegen Phishing Attacken machen?"

### Retrieval Performance
- **Top-1**: `phishing_detection.md` (Distance: 0.84) ✅ **Exzellent!**
- **Top-2**: `password_security.md` (Distance: 1.32) ✅ **Relevant** (MFA-Kontext)
- **Top-3**: `incident_response.md` (Distance: 1.33) ✅ **Relevant** (Vorfallsmanagement)

**Diagnose:** Alle Chunks relevant! Bestes Retrieval der 3 Queries.

### Answer Quality
**Bewertung:** 3.5/5 ⚠️ Gut, aber verbesserbar

**Positiv:**
- Strukturiert (nummerierte Liste)
- Praktische Maßnahmen
- "Was tun wenn"-Teil
- Quelle zitiert
- Keine Halluzination

**Negativ:**
- Nur Aufzählung, keine Umsetzungs-Erklärung
- Akronyme nicht erklärt (SPF, DKIM, DMARC)
- Zu oberflächlich

### Root Cause
**Chunking-Problem:** Akronym-Erklärungen sind wahrscheinlich in anderem Chunk oder fehlen im gefundenen Kontext.

---

## Test Query 3: "Welches ist der beste Passwort-Manager?"

### Retrieval Performance
- **Top-1**: `password_security.md` (Distance: 1.03) ✅ **Gut**
- **Top-2**: `network_security.md` (Distance: 1.41) ⚠️ **Grenzwertig**
- **Top-3**: `network_security.md` (Distance: 1.57) ❌ **Zu irrelevant**

**Diagnose:** Top-1 gut, Top-2/3 Noise.

### Answer Quality
**Bewertung:** 2.9/5 ⚠️ Objektiv, aber suggestiv

**Antwort:**
> "Der beste Passwort-Manager hängt von den individuellen Bedürfnissen ab... [listet 1Password, Bitwarden, LastPass auf]"

**Positiv:**
- Keine Halluzination
- Disclaimer ("hängt von Bedürfnissen ab")
- Objektive Auflistung
- Quelle korrekt

**Negativ:**
- Formulierung suggeriert Empfehlung
- Dokument trifft keine Wertung, Antwort klingt aber danach

### Root Cause
**Prompt-Problem:** Der Prompt instruiert nicht, wie mit Fragen umzugehen ist, die die Docs nicht eindeutig beantworten.

**Lösung:** Explizite Anweisung im Prompt:
> "Wenn die Dokumente die Frage nicht direkt beantworten oder keine Wertung treffen, sage das explizit."

---

## Gesamtfazit

### Was funktioniert gut:
- ✅ Retrieval funktioniert (besonders bei fokussierten Queries)
- ✅ Keine Halluzination
- ✅ Quellen werden zitiert

### Verbesserungsbedarf:
1. **Kleinere Chunks** (300 statt 500 Tokens)
2. **Top-K reduzieren** (2 statt 3)
3. **Distance-Threshold** (<1.5)
4. **Prompt verbessern** (Umgang mit Ambiguität)
5. **Chunk-Overlap** einführen (50 Tokens)

### Nächste Schritte:
- Prompt-Pattern-Tests (Session 5)
- Chunking optimieren
- Business-Demo vorbereiten (Session 6-7)

