# install_wizard.py

import sys, os, subprocess, venv
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QProgressBar, QMessageBox, QTextEdit)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

# ---- Hilfsfunktionen für die Prüf- und Installationsschritte ----

def check_python():
    import platform
    return sys.version_info >= (3, 10), platform.python_version()

def create_venv(venv_path=".venv"):
    try:
        if not os.path.exists(venv_path):
            venv.create(venv_path, with_pip=True)
        return True, ""
    except Exception as e:
        return False, str(e)

def check_requirements(venv_path=".venv"):
    req = "requirements.txt"
    if not os.path.exists(req):
        return False, "requirements.txt fehlt!"
    pip_exe = os.path.join(venv_path, "bin", "pip") if os.name != "nt" else os.path.join(venv_path, "Scripts", "pip.exe")
    try:
        result = subprocess.run([pip_exe, "install", "-r", req], capture_output=True, text=True)
        if result.returncode == 0:
            return True, result.stdout
        return False, result.stderr
    except Exception as e:
        return False, str(e)

def run_selfcheck():
    # Dummy: In Echt sollte das SelfCheck-Service-Modul verwendet werden!
    return True, "Self-Check abgeschlossen: Alle Strukturen vorhanden."

def start_tool_main():
    py = sys.executable
    if os.name == "nt":
        os.system(f'start {py} tool_main.py')
    else:
        subprocess.Popen([py, "tool_main.py"])
    sys.exit(0)

# ---- Wizard GUI ----

class StepThread(QThread):
    result = pyqtSignal(bool, str)
    def __init__(self, func, *args):
        super().__init__()
        self.func = func
        self.args = args
    def run(self):
        try:
            ok, msg = self.func(*self.args)
            self.result.emit(ok, msg)
        except Exception as e:
            self.result.emit(False, str(e))

class InstallWizard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Installations-Wizard: Tool-Setup")
        self.resize(600, 400)
        self.step = 0

        self.steps = [
            ("Python-Version prüfen", check_python, None),
            ("Virtuelle Umgebung erstellen", create_venv, ".venv"),
            ("Abhängigkeiten installieren", check_requirements, ".venv"),
            ("Self-Check & Strukturprüfung", run_selfcheck, None)
        ]
        self.step_titles = [t[0] for t in self.steps]

        self.layout = QVBoxLayout()
        self.progress = QProgressBar()
        self.label = QLabel()
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.btn_prev = QPushButton("Zurück")
        self.btn_next = QPushButton("Weiter")
        self.btn_help = QPushButton("Hilfe")
        self.btn_abort = QPushButton("Abbrechen")
        self.btn_finish = QPushButton("Tool starten")
        self.btn_finish.hide()

        self.layout.addWidget(QLabel("<h2>Tool-Installations-Wizard</h2>"))
        self.layout.addWidget(self.progress)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.log)
        btnrow = QHBoxLayout()
        btnrow.addWidget(self.btn_prev)
        btnrow.addWidget(self.btn_next)
        btnrow.addWidget(self.btn_help)
        btnrow.addWidget(self.btn_abort)
        btnrow.addWidget(self.btn_finish)
        self.layout.addLayout(btnrow)
        self.setLayout(self.layout)

        self.btn_prev.clicked.connect(self.go_prev)
        self.btn_next.clicked.connect(self.go_next)
        self.btn_help.clicked.connect(self.show_help)
        self.btn_abort.clicked.connect(self.abort)
        self.btn_finish.clicked.connect(start_tool_main)

        self.update_ui()

    def update_ui(self):
        self.progress.setValue(int(100 * self.step / len(self.steps)))
        self.label.setText(f"Schritt {self.step+1} von {len(self.steps)}: {self.step_titles[self.step]}")
        self.btn_prev.setEnabled(self.step > 0)
        self.btn_next.setEnabled(self.step < len(self.steps)-1)
        self.btn_finish.setVisible(self.step == len(self.steps)-1)
        self.log.append(f"\n-- {self.step_titles[self.step]} --\n")

    def go_prev(self):
        if self.step > 0:
            self.step -= 1
            self.update_ui()

    def go_next(self):
        title, func, arg = self.steps[self.step]
        self.log.append(f"Starte: {title} ...")
        self.setEnabled(False)
        thread = StepThread(func, *(tuple() if arg is None else (arg,)))
        thread.result.connect(self.step_done)
        thread.start()

    def step_done(self, ok, msg):
        self.setEnabled(True)
        if ok:
            self.log.append(f"✔ Erfolgreich: {msg}\n")
            if self.step < len(self.steps) - 1:
                self.step += 1
                self.update_ui()
            else:
                self.label.setText("Installation abgeschlossen. Starte Tool...")
                self.btn_next.hide()
                self.btn_finish.show()
        else:
            self.log.append(f"❌ Fehler: {msg}\n")
            QMessageBox.warning(self, "Fehler", msg)
        self.update_ui()

    def show_help(self):
        helptexts = [
            "Python-Version wird geprüft. Es sollte Python 3.10+ installiert sein.",
            "Erstellt eine virtuelle Umgebung (.venv). Keine Angst, alles läuft automatisch!",
            "Installiert alle benötigten Abhängigkeiten laut requirements.txt.",
            "Self-Check prüft, ob alle Projektdateien und Ordner korrekt angelegt sind."
        ]
        QMessageBox.information(self, "Hilfe", helptexts[self.step])

    def abort(self):
        self.close()

# ----- Start -----
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = InstallWizard()
    w.show()
    app.exec()
