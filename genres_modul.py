from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

# Qt-Import mit Fallback
try:
    pass
    pass
    from PyQt6.QtCore import Qt
    from PyQt6.QtWidgets import (
        QHBoxLayout,
        QLabel,
        QLineEdit,
        QListWidget,
        QMessageBox,
        QPushButton,
        QTextEdit,
        QVBoxLayout,
        QWidget,
    )

    _QT_AVAILABLE = True
except ImportError:
    pass
    pass
    _QT_AVAILABLE = False
    logging.warning("PyQt6 nicht gefunden. Dummy-Stubs werden verwendet.")

    class _Dummy(QWidget if False else object):  # verhindert Qt-Abhängigkeit
        def __init__(self, *args, **kwargs):
    pass
    pass
            pass

        def __getattr__(self, name):
    pass
    pass
            return self

        def __call__(self, *args, **kwargs):
    pass
    pass
            return self

    QWidget = _Dummy
    QVBoxLayout = _Dummy
    QHBoxLayout = _Dummy
    QLabel = _Dummy
    QLineEdit = _Dummy
    QTextEdit = _Dummy
    QListWidget = _Dummy
    QPushButton = _Dummy
    QMessageBox = _Dummy
    Qt = _Dummy

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# Konfigurations- und Speicherklassen
class Config:
    pass
    pass
    def __init__(self, base_dir: Optional[Path] = None):
        base = (base_dir or Path.cwd()).resolve()
        self.data_dir = base / "data        self.backup_dir = base / "backup        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.wiki_file = self.data_dir / "wiki.json        self.backup_file = self.backup_dir / "wiki_backup.json

class WikiStorage:
    pass
    pass
    def __init__(self, cfg: Config):
        self._cfg = cfg
        if not cfg.wiki_file.exists():
    pass
    pass
            cfg.wiki_file.write_text("[]", encoding="utf-8")
        self.entries: List[Dict[str, Any]] = []
        self.load_entries()

    def load_entries(self) -> None:
    pass
    pass
        try:
    pass
    pass
            raw = self._cfg.wiki_file.read_text(encoding="utf-8")
            self.entries = json.loads(raw)
            logger.info(f"{len(self.entries)} Einträge geladen.")
        except Exception:
    pass
    pass
            logger.exception("Laden der Wiki-Einträge fehlgeschlagen.")
            self.entries = []

    def save_entries(self) -> None:
    pass
    pass
        try:
    pass
    pass
            # Backup
            self._cfg.backup_file.write_text(
                json.dumps(self.entries, indent=2), encoding="utf-8            )
            # Aktuelles Speichern
            self._cfg.wiki_file.write_text(
                json.dumps(self.entries, indent=2), encoding="utf-8            )
            logger.info("Einträge gespeichert und Backup erstellt.")
        except Exception:
    pass
    pass
            logger.exception("Speichern der Wiki-Einträge fehlgeschlagen.")
            raise


# Haupt-Widget
class WikiModule(QWidget):
    pass
    pass
    def __init__(
        self,
        storage: WikiStorage,
        export_func: Optional[Callable[[List[Dict[str, Any]]], None]] = None,
        import_func: Optional[Callable[[], List[Dict[str, Any]]]] = None,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)
        self.storage = storage
        self.export_func = export_func
        self.import_func = import_func
        self.current_index: Optional[int] = None
        self._build_ui()
        self._refresh_list()

    def _build_ui(self) -> None:
    pass
    pass
        self.setWindowTitle("Wiki-Manager")
        main_layout = QHBoxLayout(self)
        # Eintragsliste
        self.list_widget = QListWidget()
        self.list_widget.currentRowChanged.connect(self._on_select)
        main_layout.addWidget(self.list_widget, stretch=1)
        # Detailbereich
        detail_layout = QVBoxLayout()
        detail_layout.addWidget(QLabel("Title:"))
        self.title_edit = QLineEdit()
        detail_layout.addWidget(self.title_edit)
        detail_layout.addWidget(QLabel("Body:"))
        self.body_edit = QTextEdit()
        detail_layout.addWidget(self.body_edit, stretch=1)
        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self._on_save)
        btn_layout.addWidget(save_btn)
        del_btn = QPushButton("Delete")
        del_btn.clicked.connect(self._on_delete)
        btn_layout.addWidget(del_btn)
        detail_layout.addLayout(btn_layout)
        main_layout.addLayout(detail_layout, stretch=2)

    def _refresh_list(self) -> None:
    pass
    pass
        self.list_widget.clear()
        for entry in self.storage.entries:
    pass
    pass
            title = entry.get("title", "<Untitled>")
            self.list_widget.addItem(title)

    def _on_select(self, idx: int) -> None:
        if idx < 0 or idx >= len(self.storage.entries):
    pass
    pass
            self.current_index = None
            self.title_edit.clear()
            self.body_edit.clear()
            return
        self.current_index = idx
        entry = self.storage.entries[idx]
        self.title_edit.setText(entry.get("title", "))
        self.body_edit.setPlainText(entry.get("body", "))

    def _on_save(self) -> None:
    pass
    pass
        title = self.title_edit.text().strip()
        body = self.body_edit.toPlainText().strip()
        if not title:
    pass
    pass
            QMessageBox.warning(self, "Validation", "Title cannot be empty.")
            return
        record = {"title": title, "body": body}
        if self.current_index is None:
    pass
    pass
            self.storage.entries.append(record)
        else:
    pass
    pass
            self.storage.entries[self.current_index] = record
        try:
    pass
    pass
            self.storage.save_entries()
        except Exception:
    pass
    pass
            QMessageBox.critical(self, "Error", "Speichern fehlgeschlagen.")
        self._refresh_list()

    def _on_delete(self) -> None:
    pass
    pass
        if self.current_index is None:
    pass
    pass
            return
        resp = QMessageBox.question(
            self,
            "Confirm Delete",
            "Eintrag wirklich löschen?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if resp == QMessageBox.StandardButton.Yes:
    pass
    pass
            self.storage.entries.pop(self.current_index)
            try:
    pass
    pass
                self.storage.save_entries()
            except Exception:
    pass
    pass
                QMessageBox.critical(self, "Error", "Löschen fehlgeschlagen.")
            self.current_index = None
            self.title_edit.clear()
            self.body_edit.clear()
            self._refresh_list()
