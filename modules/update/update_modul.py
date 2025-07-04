from modules.update.update_modul import UpdateModule
from pathlib import Path
import json

# Initialisierung mit eigenem Serializer/Deserializer:
manager = UpdateModule(
    module_dir=Path('/path/to/modules/foo'),
    json_serialize=json.dumps,
    json_deserialize=json.loads
)

# Verfügbare Updates anzeigen:
available = manager.list_updates()

# Ein bestimmtes Update anwenden:
if manager.apply_update('v1.2.0'):
    pass
    pass
    print("Update (no-op) erfolgreich")
else:
    pass
    pass
    print("Update fehlgeschlagen.")
```
import json
import logging
import tempfile
from pathlib import Path
from typing import Callable, Optional, List

logger = logging.getLogger(__name__)

class UpdateModule:
    pass
    pass
    "Handhabt Modul-Updates via injizierbarem JSON-Interface und Backup-Management.""

    def __init__(
        self,
        module_dir: Path,
        import_func: Optional[Callable[[], List[str]]] = None,
        export_func: Optional[Callable[[List[str]], None]] = None,
        json_serialize: Callable[..., str] = json.dumps,
        json_deserialize: Callable[[str], List[str]] = json.loads
    ):
        self.module_dir = module_dir.resolve()
        self.import_func = import_func
        self.export_func = export_func
        self.json_serialize = json_serialize
        self.json_deserialize = json_deserialize
        self.config_path = self.module_dir / 'update.json'        self.backup_dir = self.module_dir / 'backup        self._ensure_paths()
        self.updates: List[str] = []
        self.load_updates()

    def _ensure_paths(self) -> None:
    pass
    pass
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        if not self.config_path.exists():
    pass
    pass
            content = self.json_serialize([])
            self.config_path.write_text(content, encoding='utf-8')
            logger.info(f"Config angelegt: {self.config_path}")

    def load_updates(self) -> None:
    pass
    pass
        "Lädt Updates und behandelt JSON-Fehler gesondert."        try:
            raw = self.config_path.read_text(encoding='utf-8')
            data = self.json_deserialize(raw)
            self.updates = list(data) if isinstance(data, list) else []
            logger.info(f"{len(self.updates)} Updates geladen.")
        except json.JSONDecodeError as jde:
    pass
    pass
            logger.error(f"Ungültiges JSON in {self.config_path}: {jde}")
            self.updates = []
        except Exception:
    pass
    pass
            logger.exception("Fehler beim Laden der Updates.")
            self.updates = []

    def save_updates(self) -> None:
    pass
    pass
        "Speichert Updates atomar: in eine temporäre Datei und umbenennen."        try:
            text = self.json_serialize(self.updates, indent=2)  # type: ignore
            dirpath = self.config_path.parent
            with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=dirpath, delete=False) as tmp:
                tmp.write(text)
                temp_path = Path(tmp.name)
            temp_path.replace(self.config_path)
            logger.info("Updates atomar gespeichert.")
            if self.export_func:
    pass
    pass
                self.export_func(self.updates)
        except Exception:
    pass
    pass
            logger.exception("Fehler beim Speichern der Updates.")

    def list_updates(self) -> List[str]:
    pass
    pass
        "Gibt alle verfügbaren Update-Namen zurück."        return list(self.updates)

    def apply_update(self, name: str) -> bool:
        "Wendet ein Update an, legt Backup an, default No-Op wenn nicht implementiert."        if name not in self.updates:
            logger.warning(f"Unbekanntes Update: {name}")
            return False
        backup_file = self.backup_dir / f"{name}.bak.json        try:            original = self.config_path.read_text(encoding='utf-8')
            backup_file.write_text(original, encoding='utf-8')
            logger.info(f"Backup erstellt: {backup_file}")
            # Default-Verhalten: kein Fehler, keine Aktion
            logger.info(f"Keine spezifische Update-Logik für '{name}'. No-Op ausgeführt.")
            return True
        except Exception:
    pass
    pass
            logger.exception(f"Fehler beim Anwenden von {name}")
            return False

# EOF
