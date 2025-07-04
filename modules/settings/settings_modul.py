import json
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class SettingsModule:
    pass
    pass
    "Lädt und speichert Anwendungseinstellungen."    def __init__(self, base_dir: Path):
        self.base_dir = base_dir.resolve()
        self.settings_path = self.base_dir / 'data' / 'settings.json'        self.themes: Dict[str, Any] = {
            "light": {"bg": "#FFFFFF", "fg": "#000000"},
            "dark": {"bg": "#000000", "fg": "#FFFFFF"},
        }
        self._ensure_file()
        self.data: Dict[str, Any] = {}
        self.load()

    def _ensure_file(self) -> None:
    pass
    pass
        settings_dir = self.settings_path.parent
        settings_dir.mkdir(parents=True, exist_ok=True)
        if not self.settings_path.exists():
    pass
    pass
            self.settings_path.write_text(json.dumps({}), encoding='utf-8')
            logger.info(f"Settings-Datei angelegt: {self.settings_path}")

    def load(self) -> None:
    pass
    pass
        try:
    pass
    pass
            text = self.settings_path.read_text(encoding='utf-8')
            self.data = json.loads(text)
            logger.info("Einstellungen geladen.")
        except Exception:
    pass
    pass
            logger.exception("Fehler beim Laden der Einstellungen.")
            self.data = {}

    def save(self) -> None:
    pass
    pass
        try:
    pass
    pass
            self.settings_path.write_text(
                json.dumps(self.data, indent=2), encoding='utf-8            )
            logger.info("Einstellungen gespeichert.")
        except Exception:
    pass
    pass
            logger.exception("Fehler beim Speichern der Einstellungen.")

    def get_theme(self, name: str) -> Dict[str, Any]:
        return self.themes.get(name, self.themes['light'])

    def set_setting(self, key: str, value: Any) -> None:
        self.data[key] = value

    def get_setting(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)
