# WIZZARD Tool

Dieses Projekt stellt eine leere Grundstruktur für das WIZZARD Tool bereit. Du kannst damit eine Python-Umgebung aufbauen, Module entwickeln und eine grafische Oberfläche (GUI) starten.

## Schnellstart für Einsteiger

1. **Virtuelle Umgebung** (`virtual environment`):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
   Eine virtuelle Umgebung sorgt dafür, dass Abhängigkeiten nur in diesem Projekt installiert werden.

2. **Pakete installieren** (`dependencies`):
   ```bash
   pip install -r requirements.txt
   ```
   Damit werden die benötigten Bibliotheken installiert.

3. **Wizard starten** (`startup script`):
   ```bash
   bash scripts/start_wizard.sh
   ```
   Dieses Skript würde später das komplette Tool ausführen. Aktuell ist es noch leer.

## Weiterführende Ideen für Anfänger

- Bearbeite die Dateien in `config/`, um Standardwerte anzulegen.
- Lege erste Module unter `modules/` an, z.B. für Audio oder Video.
- Führe `pytest` aus, sobald Tests vorhanden sind:
  ```bash
  pytest -q
  ```

Sieh dir auch die Datei `todo.txt` an und hänge dort eigene Aufgaben an.

## Weitere Schritte fuer Neulinge

4. **Geheimnisse-Datei** (`secrets file`):
   ```bash
   cp config/secrets.example.json config/secrets.json
   ```
   Damit legst du deine persoenliche Schluesseldatei an.

5. **Code formatieren** (`formatter`):
   ```bash
   pip install black
   black .
   ```
   `black` sorgt fuer gleichmaessige Formatierung deines Quellcodes.

6. **Tests ausfuehren** (`testing`):
   ```bash
   pytest -q
   ```
   Damit pruefst du, ob alles fehlerfrei laeuft.
