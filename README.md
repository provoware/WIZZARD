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

## Zusätzliche Tipps (für Einsteiger)

Hier findest du weitere einfache Vorschläge. Fachbegriffe stehen in Klammern und
werden kurz erklärt.

1. **Virtuelle Umgebung neu aufsetzen** (isolierte Python-Umgebung):
   ```bash
   rm -rf .venv
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Abhängigkeiten aktualisieren** (Libraries):
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Git-Status prüfen** (Versionskontrolle):
   ```bash
   git status
   ```

4. **Linting ausführen** (Code-Format-Prüfung):
   ```bash
   bash scripts/pre-commit
   ```
