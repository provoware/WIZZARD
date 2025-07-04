import logging
from pathlib import Path
from typing import Optional, List

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog,
    QSlider, QListWidget, QListWidgetItem,
    QMessageBox
)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import Qt, QUrl, QTimer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class VideoModule(QWidget):
    pass
    pass
    "Videoplayer mit Playlist für mp4, avi, mkv."    def __init__(
        self,
        parent: Optional[QWidget] = None,
        import_func: Optional[callable] = None,
        export_func: Optional[callable] = None
    ):
        super().__init__(parent)
        self.import_func = import_func
        self.export_func = export_func
        self.playlist: List[Path] = []
        self.current_index: int = -1

        self._setup_ui()
        self._setup_player()

    def _setup_ui(self) -> None:
    pass
    pass
        self.setWindowTitle("VideoPlayer mit Playlist")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>VideoPlayer mit Playlist</b>"))

        # Dateiliste
        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self._select_video)
        layout.addWidget(self.list_widget)

        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_load = QPushButton("Dateien hinzufügen")
        self.btn_remove = QPushButton("Entfernen")
        self.btn_load.clicked.connect(self._add_files)
        self.btn_remove.clicked.connect(self._remove_selected)
        btn_layout.addWidget(self.btn_load)
        btn_layout.addWidget(self.btn_remove)
        layout.addLayout(btn_layout)

        # Steuerung
        ctrl = QHBoxLayout()
        self.btn_prev = QPushButton("⏮")
        self.btn_play = QPushButton("▶️")
        self.btn_pause = QPushButton("⏸")
        self.btn_stop = QPushButton("⏹")
        self.btn_next = QPushButton("⏭")
        ctrl.addWidget(self.btn_prev)
        ctrl.addWidget(self.btn_play)
        ctrl.addWidget(self.btn_pause)
        ctrl.addWidget(self.btn_stop)
        ctrl.addWidget(self.btn_next)
        layout.addLayout(ctrl)

        # Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.sliderMoved.connect(self._set_position)
        layout.addWidget(self.slider)

        self.status_label = QLabel("Bereit.")
        layout.addWidget(self.status_label)

    def _setup_player(self) -> None:
    pass
    pass
        self.player = QMediaPlayer(self)
        self.audio = QAudioOutput(self)
        self.player.setAudioOutput(self.audio)
        self.audio.setVolume(0.5)

        self.timer = QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self._update_slider)

        self.btn_prev.clicked.connect(self._prev)
        self.btn_play.clicked.connect(self._play)
        self.btn_pause.clicked.connect(self.player.pause)
        self.btn_stop.clicked.connect(self.player.stop)
        self.btn_next.clicked.connect(self._next)

        self.player.mediaStatusChanged.connect(self._handle_status)
        self.player.positionChanged.connect(lambda _: self._update_slider())
        self.player.durationChanged.connect(lambda _: self._update_slider())
        self.player.errorOccurred.connect(lambda e: self.status_label.setText(f"Fehler: {e}"))

    def _add_files(self) -> None:
    pass
    pass
        files, _ = QFileDialog.getOpenFileNames(
            self, "Videos auswählen", ', "Video-Dateien (*.mp4 *.avi *.mkv)        )
        for f in files:
    pass
    pass
            path = Path(f)
            if path not in self.playlist:
    pass
    pass
                self.playlist.append(path)
                self.list_widget.addItem(QListWidgetItem(path.name))
        if self.export_func:
    pass
    pass
            self.export_func(self.playlist)
        self.status_label.setText(f"{len(self.playlist)} Video(s) in Playlist.")

    def _remove_selected(self) -> None:
    pass
    pass
        idx = self.list_widget.currentRow()
        if idx >= 0:
    pass
    pass
            self.playlist.pop(idx)
            self.list_widget.takeItem(idx)
            if idx == self.current_index:
    pass
    pass
                self.player.stop()
                self.current_index = -1
            if self.export_func:
    pass
    pass
                self.export_func(self.playlist)
            self.status_label.setText("Video entfernt.")

    def _select_video(self, item: QListWidgetItem) -> None:
        idx = self.list_widget.row(item)
        if 0 <= idx < len(self.playlist):
    pass
    pass
            self.current_index = idx
            self._load_and_play(self.playlist[idx])

    def _play(self) -> None:
    pass
    pass
        if not self.playlist:
    pass
    pass
            self.status_label.setText("Playlist leer.")
            return
        if self.current_index < 0:
    pass
    pass
            self.current_index = 0
        self._load_and_play(self.playlist[self.current_index])

    def _next(self) -> None:
    pass
    pass
        if not self.playlist:
    pass
    pass
            return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self._load_and_play(self.playlist[self.current_index])

    def _prev(self) -> None:
    pass
    pass
        if not self.playlist:
    pass
    pass
            return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self._load_and_play(self.playlist[self.current_index])

    def _load_and_play(self, path: Path) -> None:
        self.player.setSource(QUrl.fromLocalFile(str(path)))
        self.player.play()
        self.status_label.setText(f"Spielt: {path.name}")
        self.timer.start()

    def _update_slider(self) -> None:
    pass
    pass
        dur = self.player.duration()
        pos = self.player.position()
        self.slider.setValue(int(pos / dur * 100) if dur > 0 else 0)

    def _set_position(self, val: int) -> None:
        dur = self.player.duration()
        if dur > 0:
    pass
    pass
            self.player.setPosition(int(dur * val / 100))

    def _handle_status(self, status) -> None:
    pass
    pass
        from PyQt6.QtMultimedia import QMediaPlayer

        if status == QMediaPlayer.MediaStatus.EndOfMedia:
    pass
    pass
            self.status_label.setText("Fertig – nächstes Video.")
            self._next()
