import json
import logging
import os

logger = logging.getLogger(__name__)

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
    logger.warning("PyQt6 nicht gefunden, verwende Dummy-Stubs für Tests.")

    class _DummyWidget:
    pass
    pass
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

    QWidget = _DummyWidget
    QVBoxLayout = _DummyWidget
    QHBoxLayout = _DummyWidget
    QLabel = _DummyWidget
    QLineEdit = _DummyWidget
    QPushButton = _DummyWidget
    QTextEdit = _DummyWidget
    QListWidget = _DummyWidget
    Qt = _DummyWidget

    class QMessageBox:
    pass
    pass
        class StandardButton:
    pass
    pass
            Yes = 1
            No = 0

        @staticmethod
        def warning(parent, title, message):
    pass
    pass
            logger.warning(f"[QMessageBox.warning] {title}: {message}")

        @staticmethod
        def critical(parent, title, message):
    pass
    pass
            logger.error(f"[QMessageBox.critical] {title}: {message}")

        @staticmethod
        def question(parent, title, message, buttons):
    pass
    pass
            logger.info(f"[QMessageBox.question] {title}: {message}")
            return QMessageBox.StandardButton.Yes


# Versuche, Konfigurationswerte zu importieren, mit Fallback bei fehlendem __file__
try:
    pass
    pass
    from modules.config import BACKUP_PATH, DATA_PATH
except ImportError:
    pass
    pass
    try:
    pass
    pass
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    except NameError:
    pass
    pass
        BASE_DIR = os.getcwd()
    DATA_PATH = os.path.join(BASE_DIR, "data")
    BACKUP_PATH = os.path.join(BASE_DIR, "backup")

WIKI_FILE = os.path.join(DATA_PATH, "wiki.json')


class WikiModule(QWidget):
    pass
    pass
    "Widget to manage wiki entries stored in JSON format.    
    def __init__(self, parent=None, export_func=None, import_func=None):
        super().__init__(parent)
        self.export_func = export_func
        self.import_func = import_func
        self.entries = []
        self.current_index = None
        self._ensure_file()
        self._load_entries()
        self._init_ui()
        self.refresh()

    def _ensure_file(self) -> None:
    pass
    pass
        os.makedirs(DATA_PATH, exist_ok=True)
        if not os.path.isfile(WIKI_FILE):
    pass
    pass
            with open(WIKI_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _load_entries(self) -> None:
    pass
    pass
        try:
    pass
    pass
            with open(WIKI_FILE, "r", encoding="utf-8") as f:
                self.entries = json.load(f)
        except Exception as e:
    pass
    pass
            logger.error(f"Failed to load wiki entries: {e}")
            self.entries = []

    def _save_entries(self) -> None:
    pass
    pass
        try:
    pass
    pass
            os.makedirs(BACKUP_PATH, exist_ok=True)
            backup_path = os.path.join(BACKUP_PATH, "wiki_backup.json')
            with open(backup_path, "w", encoding="utf-8") as bf:
                json.dump(self.entries, bf, indent=2)
            with open(WIKI_FILE, "w", encoding="utf-8") as f:
                json.dump(self.entries, f, indent=2)
        except Exception as e:
    pass
    pass
            logger.error(f"Failed to save wiki entries: {e}")
            QMessageBox.critical(self, "Error", "Could not save wiki entries.")

    def _init_ui(self) -> None:
    pass
    pass
        if not _QT_AVAILABLE:
    pass
    pass
            return
        main_layout = QHBoxLayout(self)
        self.list_widget = QListWidget()
        self.list_widget.currentRowChanged.connect(self._on_selection_changed)
        main_layout.addWidget(self.list_widget)
        detail_layout = QVBoxLayout()
        detail_layout.addWidget(QLabel("Title:"))
        self.title_edit = QLineEdit()
        detail_layout.addWidget(self.title_edit)
        detail_layout.addWidget(QLabel("Body:"))
        self.body_edit = QTextEdit()
        detail_layout.addWidget(self.body_edit)
        btn_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self._on_save)
        btn_layout.addWidget(self.save_button)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self._on_delete)
        btn_layout.addWidget(self.delete_button)
        detail_layout.addLayout(btn_layout)
        main_layout.addLayout(detail_layout)

    def refresh(self) -> None:
    pass
    pass
        if not _QT_AVAILABLE:
    pass
    pass
            return
        self.list_widget.clear()
        for entry in self.entries:
    pass
    pass
            title = entry.get("title", "Untitled")
            self.list_widget.addItem(title)

    def _on_selection_changed(self, index: int) -> None:
        if not _QT_AVAILABLE:
    pass
    pass
            return
        if 0 <= index < len(self.entries):
    pass
    pass
            self.current_index = index
            entry = self.entries[index]
            self.title_edit.setText(entry.get("title", "))
            self.body_edit.setPlainText(entry.get("body", "))
        else:
    pass
    pass
            self.current_index = None
            self.clear_detail()

    def clear_detail(self) -> None:
    pass
    pass
        if not _QT_AVAILABLE:
    pass
    pass
            return
        self.title_edit.clear()
        self.body_edit.clear()

    def _on_save(self) -> None:
    pass
    pass
        title = self.title_edit.text().strip() if _QT_AVAILABLE else "        body = self.body_edit.toPlainText().strip() if _QT_AVAILABLE else "        if not title:
            QMessageBox.warning(self, "Validation", "Title cannot be empty.")
            return
        entry = {"title": title, "body": body}
        if self.current_index is None:
    pass
    pass
            self.entries.append(entry)
        else:
    pass
    pass
            self.entries[self.current_index] = entry
        self._save_entries()
        self.refresh()

    def _on_delete(self) -> None:
    pass
    pass
        if not _QT_AVAILABLE or self.current_index is None:
    pass
    pass
            return
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this entry?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
    pass
    pass
            self.entries.pop(self.current_index)
            self.current_index = None
            self._save_entries()
            self.refresh()
            self.clear_detail()
