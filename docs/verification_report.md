# Mini-ZSeries Hardware- & Software-Verifikationsbericht

## 1- Projektübersicht
**Ziel:**  
Kurze Beschreibung deines Mini-ZSeries-Projekts (Batch-Processing + ACID-Transaktionen + Recovery).

**System:**  
| Komponente | Beschreibung |
|-------------|---------------|
| Plattform | Odroid XU4 |
| CPU | 4× Cortex-A15 + 4× Cortex-A7 |
| OS | Ubuntu 22.04 Mate |
| Anwendung | Flask-basierte Bank-Transaktions-Simulation |
| Speicher | Persistent JSON-State |
| KI-Modul | LogisticRegression-Modell (Scikit-Learn), trainiert auf Dummy-Transaktionsdaten |


---

## 2- Testplan (Tag 1 – 3)

| Testphase | Ziel | Testbeschreibung | Erwartetes Ergebnis |
|------------|------|------------------|---------------------|
| Baseline-Messung | Normalzustand erfassen | 10 Transaktionen + Temperatur + CPU-Last messen | Temperatur < 50 °C, keine Fehler |
| Stress-Test | Max-Last validieren | `stress-ng --cpu 8 --timeout 100s` + gleichzeitige Transaktionen | System stabil, kein Crash |
| Recovery-Test | Zustand nach Absturz prüfen | `pkill -9 python3 ` und Strom Absturz, Neustart → Saldo-Vergleich vorher/nachher | Saldo konsistent |
| Persistenz-Test | JSON-Zustand prüfen | Nach Restart Daten identisch | gleich |
| Fraud-Detection-Test | AI-Modell validieren | 100 virtuelle Transaktionen mit 10 % Fraud-Rate simulieren | Fraud-Score ≥ 0.9 bei echten Anomalien |
| Batch-Processing-Test | Sequenzielle Transaktionen verarbeiten | 50 Transaktionen in 5 Sekunden-Batch | Keine Race-Conditions |
| Temperatur-Monitoring | Thermal-Stabilität validieren | `sensors` und `vcgencmd measure_temp` | Max. < 80 °C |
---

## 3- Messergebnisse (Beispiel-Protokoll)

| Zeit | CPU-Last (%) | Temp (°C) | Transaktionen/s | Fehler | Bewertung |
|------|--------------:|-----------:|----------------:|--------|-----------|
| 12:00 | 18 | 45 | 12 | 0 | OK |
| 12:05 | 95 | 78 | 11 | 0 | OK |
| 12:10 | 100 | 84 | – | Crash | NOK |
| 12:12 | nach Restart | 56 | – | 0 | Recovery OK |

---

## 4- Ergebnisse / Pass-Fail-Tabelle

| Test | Bewertung | Kommentar |
|------|-----------|------------|------------|
| CPU-Stabilität | OK | keine Überhitzung |
| Datenpersistenz  | OK | JSON Recovery funktioniert |
| Parallelität | Grenzwertig | leichte Verzögerung bei 8 Threads |
| Transaktionskonsistenz | OK | keine Verluste |
| Fraud-Detection | OK | korrektes Erkennen simulierter Anomalien |
| AI-Latency | OK | leichte Verzögerung (< 100 ms pro Batch) |

---

## 5- Analyse

**Beobachtungen:**  
- Temperaturanstieg bei Stress, aber kein Drosseln.  
- Keine Dateninkonsistenzen nach Crash.  
- Thread-Lock funktioniert korrekt (keine Race Conditions).

**Schwächen:**  
- I/O durch JSON langsamer bei hoher Transaktionsrate.  
- Kein Audit-Trail bei gleichzeitigen Requests.

---

## 6- Verbesserungsvorschläge

| Bereich | Idee | Nutzen |
|----------|------|--------|
| AI-Modell | Upgrade auf ONNX / TensorFlow Lite | Beschleunigung der Inferenz |
| Datenhaltung | SQLite-Transaktionslog statt JSON | robustere Speicherung |
| Fraud-Scoring | Threshold-basierte Risiko-Stufen | bessere Transparenz |
| Logging | Audit-Trail + SHA-Checksum | Revisionssicherheit |
| Monitoring | Flask-Dashboard mit CPU, Fraud-Rate | visuelle Kontrolle |

---

## 7️- Fazit
Das Mini-ZSeries-System demonstriert erfolgreich, dass resiliente Mainframe-Mechanismen  
(Transaktions-Recovery, Batch-Processing, AI-Fraud-Detection) auch auf Embedded-Hardware realisierbar sind.  
Das System liefert konsistente Ergebnisse unter Last und kann als **experimentelle Validierungsplattform**  
für hybride Mainframe-Architekturen genutzt werden.

---

## Anhang
**Dateien:**  
- `accounts.json` – aktueller Kontostand  
- `transaction_log.txt` – Audit-Trail  
- `metrics.csv` – Messdaten (Temperatur, CPU-Last, Fehler)
