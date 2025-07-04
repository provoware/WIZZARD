import logging
from pathlib import Path
import subprocess
from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QComboBox, QHBoxLayout, QLabel,
    QListWidget, QPushButton, QTextEdit, QVBoxLayout,
    QMessageBox
)
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Basispfad des Tools (Projektstruktur)
BASE_DIR = Path(__file__).resolve().parent.parent
MODULES_DIR = BASE_DIR / 'modules'
DATA_DIR = BASE_DIR / 'data'
VERSIONS_PATH = DATA_DIR / 'module_versions.json'
HISTORY_PATH = DATA_DIR / 'updates_history.json'
BACKUP_DIR = DATA_DIR / 'backups'

# Sicherstellen, dass Verzeichnisse existieren
DATA_DIR.mkdir(parents=True, exist_ok=True)
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

class UpdateManagerWidget(QWidget):
    """Widget zur Verwaltung von Modulversionen binnen des Tools."""
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        import_func: Optional[callable] = None,
        export_func: Optional[callable] = None
    ):
        super().__init__(parent)
        self.import_func = import_func
        self.export_func = export_func

        self.setWindowTitle("Update- und Modul-Manager")
        self.setMinimumWidth(600)

        self._init_ui()
        self._connect_signals()
        self._load_modules()
        self.show_versions()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>Modul-/Updateverwaltung</b> – ohne ZIP, nur intern"))

        # Controls
        btn_layout = QHBoxLayout()
        self.btn_activate = QPushButton("Ausgewählte Version aktivieren")
        self.btn_undo = QPushButton("Letzte Änderung rückgängig")
        self.btn_snapshot = QPushButton("Jetzt Snapshot anlegen")
        btn_layout.addWidget(self.btn_activate)
        btn_layout.addWidget(self.btn_undo)
        btn_layout.addWidget(self.btn_snapshot)
        layout.addLayout(btn_layout)

        # Module selection
        self.module_combo = QComboBox()
        layout.addWidget(self.module_combo)

        # Versions list
        self.version_list = QListWidget()
        layout.addWidget(self.version_list)

        # History log
        layout.addWidget(QLabel("Update-/Backup-Historie:"))
        self.log_text = QTextEdit(readOnly=True)
        self.log_text.setMinimumHeight(80)
        layout.addWidget(self.log_text)

        # Status bar
        self.status_label = QLabel("Modul auswählen, um Versionen zu sehen.")
        layout.addWidget(self.status_label)
        layout.addStretch()

    def _connect_signals(self) -> None:
        self.module_combo.currentTextChanged.connect(self.show_versions)
        self.btn_activate.clicked.connect(self.activate_version)
        self.btn_undo.clicked.connect(self.undo_change)
        self.btn_snapshot.clicked.connect(self.create_snapshot)

    def _load_modules(self) -> None:
        modules = [p.name for p in MODULES_DIR.iterdir() if p.is_dir()]
        self.module_combo.addItems(modules)

    def show_versions(self) -> None:
        self.version_list.clear()
        mod = self.module_combo.currentText()
        mod_dir = MODULES_DIR / mod
        if not mod_dir.exists():
            self.status_label.setText(f"Modulordner nicht gefunden: {mod}")
            return
        versions = sorted(str(p.name) for p in mod_dir.glob('*.py'))
        self.version_list.addItems(versions)
        self.status_label.setText("Version wählen und 'Aktivieren' klicken.")

    def activate_version(self) -> None:
        mod = self.module_combo.currentText()
        version_item = self.version_list.currentItem()
        if not version_item:
            QMessageBox.warning(self, "Auswahl fehlt", "Keine Version ausgewählt.")
            return

        version = version_item.text()
        mod_dir = MODULES_DIR / mod
        current_file = mod_dir / f"{mod}_modul.py"
        selected_file = mod_dir / version
        backup_file = BACKUP_DIR / f"{mod}_modul_backup.py"

        # Backup
        if current_file.exists():
            backup_file.write_bytes(current_file.read_bytes())

        # Activate
        current_file.write_bytes(selected_file.read_bytes())

        # Log
        with open(HISTORY_PATH, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} – Aktiviert: {version} für Modul {mod}\n")

        self.status_label.setText(f"{version} ist jetzt aktiv.")
        self.log_text.append(f"{version} für {mod} aktiviert.")
        if self.export_func:
            self.export_func(mod, version)

    def undo_change(self) -> None:
        mod = self.module_combo.currentText()
        backup_file = BACKUP_DIR / f"{mod}_modul_backup.py"
        current_file = MODULES_DIR / mod / f"{mod}_modul.py"

        if backup_file.exists():
            current_file.write_bytes(backup_file.read_bytes())
            self.log_text.append(f"Backup für {mod} wiederhergestellt.")
            self.status_label.setText(f"Backup für {mod} aktiviert.")
        else:
            self.status_label.setText("Kein Backup gefunden!")

    def create_snapshot(self) -> None:
        snapshot_dir = BACKUP_DIR / f"snapshot_{datetime.now():%Y%m%d_%H%M%S}"
        subprocess.run(["cp", "-r", str(MODULES_DIR), str(snapshot_dir)])
        self.log_text.append(f"Snapshot gespeichert: {snapshot_dir}")
        self.status_label.setText("Kompletter Modul-Snapshot erstellt.")
