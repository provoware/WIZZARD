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

## Noch mehr Tipps

7. **Eigenes Modul schreiben** (`module`; kleines Code-Stueck):
   ```bash
   echo 'print("Hallo WIZZARD")' > modules/beispiel.py
   python modules/beispiel.py
   ```
   Ein Modul ist eine einzelne Python-Datei, in der du erste Funktionen testen kannst.

8. **Konfiguration bearbeiten** (`configuration`; Einstellungen):
   ```bash
   nano config/defaults.yaml
   ```
   In dieser Datei kannst du zum Beispiel `app_name: WIZZARD` eintragen. Damit steuerst du Standardwerte.

9. **Aenderungen speichern** (`commit`; Sicherungsschritt):
   ```bash
   git status
   git add modules/beispiel.py config/defaults.yaml
   git commit -m "Beispielmodul und Konfiguration"
   ```
   Mit Git bewahrst du den aktuellen Stand deines Projekts auf.

10. **Pre-Commit-Hooks ausfuehren** (`pre-commit`; automatische Pruefungen):
    ```bash
    bash scripts/pre-commit
    ```
    Dieser Schritt startet kleine Tests vor jedem Git-Commit.

11. **Aenderungen online stellen** (`push`; Hochladen zu GitHub):
    ```bash
    git push origin main
    ```
    So landet dein Code in deinem Online-Repository.

Sieh ausserdem in `modul-pool.txt` nach Ideen fuer weitere Module.

## Weitere einfache Vorschlaege

12. **Backup erstellen** (`backup`; Sicherung des Projekts):
    ```bash
    zip -r project_backup.zip .
    ```
    Damit sicherst du alle Dateien in einer Archivdatei.

13. **Text durchsuchen** (`grep`; Suche in Dateien):
    ```bash
    grep -R "Beispiel" .
    ```
    So findest du schnell Stellen mit einem bestimmten Wort.

14. **Abhaengigkeiten einfrieren** (`freeze`; Versionen merken):
    ```bash
    pip freeze > requirements.txt
    ```
    Dadurch speicherst du alle installierten Bibliotheken in `requirements.txt`.
